from ExifEndPoint import ExifEndPoint
import unittest
import os
from pymongo import MongoClient
import pymongo


class TestEXIFExtractionFlow(unittest.TestCase):

    test_folder = 'photos'

    def setUp(self):
        for img in os.listdir(self.test_folder):
            img_path = os.path.join(self.test_folder, img)
            try:
                if os.path.isfile(img_path):
                    os.unlink(img_path)
            except Exception as e:
                print(e)


    # searches for the wrong bucket and throws an exception
    def test_01_wrong_bucket_name(self):    
        s3_bucket = 'waldo-recruiti'
        endPoint = ExifEndPoint(s3_bucket)      

        self.assertEqual(endPoint.download_bucket_images(self.test_folder), ["There is no bucket with this address !"])     
        
    #selects a wrong folder to put the images and throws an exception
    def test_02_wrong_folder(self):     
        s3_bucket = 'waldo-recruiting'
        endPoint = ExifEndPoint(s3_bucket)
        directory = 'photoss'

        self.assertEqual(endPoint.download_bucket_images(directory), ["There is no folder named photoss"])              


    #Test for a single image download that there isn't in the bucket
    def test_03_downloading_wrong_image(self):      
        s3_bucket = 'waldo-recruiting'              
        endPoint = ExifEndPoint(s3_bucket)      

        class Key:
            key = ''

        key = Key()
        key.key = "wrong_image.jpg"

        self.assertEqual(endPoint.s3_serv.download_single_image(key, self.test_folder), (False, "Image wrong_image.jpg not found"))


    #Test for a single image download that exists on the bucket
    def test_04_downloading_right_image(self):      
        s3_bucket = 'waldo-recruiting'              
        endPoint = ExifEndPoint(s3_bucket)      

        class Key:
            key = ''

        key = Key()
        key.key = "01545ec6-e621-4d87-a343-c4d41556d1b7.663307bb-4513-4f97-8e2a-12349a23f7b9.jpg"

        self.assertEqual(endPoint.s3_serv.download_single_image(key, self.test_folder), (True, None))


    #main download flow process
    def test_05_download_bucket(self):      
        s3_bucket = 'waldo-recruiting'              
        endPoint = ExifEndPoint(s3_bucket)      

        class Key:
            key = ''

        key = Key()
        key.key = "01545ec6-e621-4d87-a343-c4d41556d1b7.663307bb-4513-4f97-8e2a-12349a23f7b9.jpg"

        self.assertEqual(endPoint.s3_serv.download_single_image(key, self.test_folder), (True, None))                   

        result = endPoint.download_bucket_images(self.test_folder)        

        self.assertEqual(len(result), 4)                
        self.assertEqual(result[0], "Access Denied.")
        self.assertEqual(result[1], "Access Denied.")
        self.assertEqual(result[2], "Image 01545ec6-e621-4d87-a343-c4d41556d1b7.663307bb-4513-4f97-8e2a-12349a23f7b9.jpg has already been downloaded")              
        self.assertEqual(result[3], "126 of 129 images downloaded with success!")

        self.process_exif()


    #EXIF extraction process
    def process_exif(self):
        s3_bucket = 'waldo-recruiting'      
        endPoint = ExifEndPoint(s3_bucket)
        concurrency_mode = 'PARALLEL'

        exif_result = endPoint.process_directory(self.test_folder, concurrency_mode)        

        self.assertEqual(len(exif_result), 4)       
        self.assertIn('There is no photos/0188017b-0d90-4cab-9009-bbb74501c3d5.ede96cc7-5500-4b3a-8828-26aabcaa2f4c.jpg in photos folder', exif_result)
        self.assertIn('Attribute Error on image photos/01891213-d911-4562-9947-8548dac09119.undefined.jpg', exif_result)
        self.assertIn('Attribute Error on image photos/002B40A7-048B-4554-9EF1-8E4CB167375D.3912d78a-ec4e-405b-8280-e1a769567ba0.jpg', exif_result)
        self.assertIn('Attribute Error on image photos/01302d0f-c5a6-4ce4-bea3-f9a0566550ae.d22b891e-8c80-454b-b26b-1ef65f7ed025.jpg', exif_result)


    #Query by id with an inexistent id 
    def test_06_find_wrong(self):
        s3_bucket = 'waldo-recruiting'      
        endPoint = ExifEndPoint(s3_bucket)
        concurrency_mode = 'PARALLEL'

        doc = endPoint.find('0015A5C3-D186-471J-A032-9E952CFF3CC6.8fedf4a8-8000000000')        

        self.assertEqual(len(doc), 1)
        self.assertEqual(doc[0], 'There is no EXIF with this object id')


    #Query exif by object key and param name
    def test_07_find(self):
        try:
            s3_bucket = 'waldo-recruiting'      
            endPoint = ExifEndPoint(s3_bucket)
            concurrency_mode = 'PARALLEL'

            doc = endPoint.find('0015A5C3-D186-471F-A032-9E952CFF3CC6.8fedf4e8-8695-4d6d-ad1e-b686daa713a1')                                     

            self.assertEqual(len(doc), 1) 
            self.assertEqual(doc[0]['_id'], '0015A5C3-D186-471F-A032-9E952CFF3CC6.8fedf4e8-8695-4d6d-ad1e-b686daa713a1')               

            doc2 = endPoint.find_by_param('ExifImageHeight', '4016')

            self.assertEqual(len(doc2), 14)
        finally:
            self.client = MongoClient()
            self.client.test.drop_collection('exif')

    

if __name__ == '__main__':
    unittest.main()
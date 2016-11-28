import botocore
import boto3
import copy
import os

#Here all exceptions are handled and where all main services concerning s3 manipulation are implementated
class s3Service:

    def __init__(self, s3_address): 
        #Init of s3 variables        
        s3 = boto3.resource('s3')  
        self.s3_bucket = s3.Bucket(s3_address)         
        self.s3_client = boto3.client('s3')  
        self.s3_address = s3_address       


    #Download all images and saves in the 'directory' folder
    def download_images(self, directory):            
        status_list = []
        err_list = []
        #Return false if it is the directory doesn't exist
        if not os.path.isdir(directory):
            status_list.append(False), err_list.append("There is no folder named "+directory)
        #iterates through all images from the bucket and download each one if necessary
        else: 
            #initialize the number of successfully downloads and the num of images in the bucket
            success = 0
            num_images = 0
            try:
                for key in self.s3_bucket.objects.all():
                    #if it's not an image the counter of images in the buckets decreases in 1                    
                    if key.key[len(key.key)-4:len(key.key)] not in ['.jpg', '.png', '.JPG', '.PNG']: 
                        num_images -= 1
                        continue
                    #if the path is an already downloaded image, then the just pass
                    num_images += 1
                    if os.path.isfile(directory+'/'+key.key):
                        status, err = True, "Image "+key.key+" has already been downloaded"
                        status_list.append(status), err_list.append(err)
                    #if there isn't an image with this key in the directory, download it
                    else:
                        status, err = self.download_single_image(key, directory)  
                        if status: success += 1                    
                        #if status returned from any operations contains an error, append it to the error list to be printed later
                        if not status:
                            status_list.append(status), err_list.append(err)
                #append how much images downloaded successfully
                status_list.append(True), err_list.append(str(success)+" of "+str(num_images)+" images downloaded with success!")
            #Exception handling
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchBucket':
                    status_list.append(False), err_list.append("There is no bucket with this address !")
            except botocore.exceptions.NoCredentialsError as e:
                status_list.append(False), err_list.append("Unable to locate AWS Client credentials!! Please update your security credentials in aws configure")
        return status_list, err_list        


    #Method that download a single image from the bucket through its key 
    def download_single_image(self, key, directory):
        try:            
            #Download the image from the bucket using boto API, if success doesn't return any message
            self.s3_client.download_file(self.s3_address, key.key, directory+'/'+key.key)
            return True, None
        #Exception handling
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:
                return False, "Access Denied."     
            else:
                return False, "Image "+key.key+" not found"
                
import botocore
import boto3
import os
from s3Service import s3Service
from ExifService import ExifService  
from ParallelService import ParallelService 
from pprint import pprint

class ExifEndPoint:

    def __init__(self, s3_address):
        self.s3_serv = s3Service(s3_address)          


    def process_directory(self, directory, CONCURRENCY_MODE):
        if CONCURRENCY_MODE not in ['SERIAL', 'PARALLEL']: 
            return False
            print("Error setting concurrency mode. "+CONCURRENCY_MODE+" is not an allowed mode. Use SERIAL or PARALLEL.")

        err_list = []

        if CONCURRENCY_MODE == 'SERIAL':
            for img in os.listdir(directory):                         
                status, err = ExifService.extract_and_insert_EXIF(directory, img)
                if not status:                               
                    err_list.append(err)
        elif CONCURRENCY_MODE == 'PARALLEL':
            status, err_list = ParallelService.parallelize(ExifService.extract_and_insert_EXIF, [directory for i in range(len(os.listdir(directory)))], os.listdir(directory))        

        for err in err_list: print err


    def download_bucket_images(self, directory):
        status_list, err_list = self.s3_serv.download_images(directory)
        for err in err_list: print(err) 
       

    def find(self,id):        
        for doc in ExifService.find(id):
            pprint(doc)

    
import botocore
import boto3
import os
from s3Service import s3Service
from ExifService import ExifService  
from ParallelService import ParallelService 
from pprint import pprint

#Class that provides services for other classes and print all excewptions handled by service classes
class ExifEndPoint:

    def __init__(self, s3_address):
        self.s3_serv = s3Service(s3_address)          

    #Method that extract the EXIFs from images contained in 'directory'
    def process_directory(self, directory, CONCURRENCY_MODE):
        if CONCURRENCY_MODE not in ['SERIAL', 'PARALLEL']:             
            print("Error setting concurrency mode. "+CONCURRENCY_MODE+" is not an allowed mode. Use SERIAL or PARALLEL.")
            return False

        err_list = []

        #Verify if this directory contains any image
        if os.listdir(directory):
            # if yes it chooses the mode selected by the user and iterates by each image extracting its EXIF
            if CONCURRENCY_MODE == 'SERIAL':
                for img in os.listdir(directory):                         
                    status, err = ExifService.extract_and_insert_EXIF(directory, img)
                    #if extraction get any errors it appends the error message to the list of printed errors
                    if not status:                               
                        err_list.append(err)
            elif CONCURRENCY_MODE == 'PARALLEL':
                status, err_list = ParallelService.parallelize(ExifService.extract_and_insert_EXIF, [directory for i in range(len(os.listdir(directory)))], os.listdir(directory))        
        else:
            err_list.append('No photo to process')

        #print all errors
        return err_list

    #Download all images from the bucket 's3_address'
    def download_bucket_images(self, directory):
        #Just call the service that download all images from the bucket defined in s3_address
        status_list, message_list = self.s3_serv.download_images(directory)
        return message_list
       
    #Find EXIF data by image id
    def find(self,id):
        return [doc for doc in ExifService.find(id)]        


    #Find EXIF data by param_name=param_value
    def find_by_param(self,param_name, param_value):        
        return [doc for doc in ExifService.find_by_param(param_name, param_value)]
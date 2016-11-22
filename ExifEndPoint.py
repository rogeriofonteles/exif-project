import botocore
import boto3
import os
from s3Service import s3Service
from ExifService import ExifService  
from ParallelService import ParallelService 

class ExifEndPoint:

    def __init__(self, s3_address):
        self.s3Serv = s3Service(s3_address)          


    def processDirectory(self, directory, CONCURRENCY_MODE):
        if CONCURRENCY_MODE != 'SERIAL' and CONCURRENCY_MODE != 'PARALLEL': 
            return False
            print("Error setting concurrency mode. "+CONCURRENCY_MODE+" is not a allowed mode. Use SERIAL or PARALLEL.")

        if CONCURRENCY_MODE == 'SERIAL':
            for img in os.listdir(directory):            
                status, err = ExifService.extractAndInsertEXIF(directory, img)                               
        elif CONCURRENCY_MODE == 'PARALLEL':
            status, err = ParallelService.parallelize(ExifService.extractAndInsertEXIF, [directory for i in range(len(os.listdir(directory)))], os.listdir(directory))        

        print(err if not status else "All EXIFs inserted with success!")
       


    
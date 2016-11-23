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
        if not os.path.isdir(directory):
            status_list.append(False), err_list.append("There is no folder named "+directory)
        else: 
            try:
                for key in self.s3_bucket.objects.all():
                    status, err = self.download_single_image(key, directory)  
                    if not status:
                        status_list.append(status), err_list.append(err)
                if not status_list:        
                    status_list.append(True), err_list.append("All images downloaded with success!")
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchBucket':
                    status_list.append(False), err_list.append("There is no bucket with this address !")
        return status_list, err_list        

    #Method that download a single image from the bucket through its key 
    def download_single_image(self, key, directory):
        try:
            self.s3_client.download_file(self.s3_address, key.key, directory+'/'+key.key)
            return True, None
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:
                return False, "Image "+key.key+" not found"
            else:
                return False, "Access Denied."     
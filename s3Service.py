import botocore
import boto3
import copy


class s3Service:

    def __init__(self, s3_address): 
        #Init of s3 variables        
        s3 = boto3.resource('s3')  
        self.s3_bucket = s3.Bucket(s3_address)         
        self.s3_client = boto3.client('s3')  
        self.s3_address = s3_address       

    
    def downloadImages(self):            
        for key in self.s3_bucket.objects.all():
            status, err = self.downloadSingleImage(key)                                     
        return True, "All images downloaded with success!"        


    def downloadSingleImage(self, key):
        try:
            self.s3_client.download_file(self.s3_address, key.key, 'photos/'+key.key)
            return True, None
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:
                return False, "Image"+key.key+" not found"
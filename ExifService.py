import PIL.Image
import PIL.ExifTags
import os
import sys
import exceptions
from ExifDAO import ExifDAO

class ExifService:

    dao = ExifDAO()    

    @staticmethod
    def extract_exif(img_addr):
        try:            
            img_file = PIL.Image.open(img_addr)
            tags = {PIL.ExifTags.TAGS[k]: v for k, v in img_file._getexif().items() if k in PIL.ExifTags.TAGS}
            return tags, None          
        except exceptions.IOError as e:            
            return None, 'There is no '+img_addr+' in photos folder'
        except AttributeError as e:
            return None, 'Attribute Error'


    @staticmethod
    def extract_and_insert_EXIF(directory, img):
        exif_data, err = ExifService.extract_exif(directory+'/'+img)
        if not exif_data: 
            return exif_data, err             
        else: 
            flag, err = ExifService.dao.create(exif_data, img)            
            return flag, err    


    @staticmethod
    def find(id):
        return dao.find(id)    

    
        
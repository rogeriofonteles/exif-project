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
            if not tags:
                return None, 'There is no EXIF data for '+img_addr
            return tags, 'Image '+img_addr+' added on DB with success!'          
        except exceptions.IOError as e:            
            return None, 'There is no '+img_addr+' in photos folder'
        except AttributeError as e:
            return None, 'Attribute Error on image '+img_addr

    @staticmethod
    def extract_and_insert_EXIF(directory, img):
        exif_data, err = ExifService.extract_exif(directory+'/'+img)
        if not exif_data: 
            return False, err
        else: 
            exif_data, err = ExifService.dao.create(exif_data, img)            
            return True, err    


    @staticmethod
    def find(id):
        docs = ExifService.dao.find(id)        
        if docs.count() == 0:            
            return ['There is no EXIF with this object id']
        return docs

    
        
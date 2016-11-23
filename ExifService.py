import PIL.Image
import PIL.ExifTags
import os
import sys
import exceptions
from ExifDAO import ExifDAO

#Here all exceptions are handled and where all main services concerning EXIF extraction are implementated
class ExifService:

    dao = ExifDAO()    

    #EXIF extraction from a single image
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

    #EXIF extraction and creation of the document to be inserted on the collection
    @staticmethod
    def extract_and_insert_EXIF(directory, img):
        exif_data, err = ExifService.extract_exif(directory+'/'+img)
        if not exif_data: 
            return False, err
        else: 
            exif_data, err = ExifService.dao.create(exif_data, img)            
            return True, err    

    #Find by id method
    @staticmethod
    def find(id):
        docs = ExifService.dao.find(id)        
        if docs.count() == 0:            
            return ['There is no EXIF with this object id']
        return docs

    #Find by id method
    @staticmethod
    def find_by_param(param_name, param_value):
        docs = ExifService.dao.find_by_param(param_name, param_value)        
        if docs.count() == 0:            
            return ['There is no EXIF with '+param_name+'='+param_value]
        return docs

    
        
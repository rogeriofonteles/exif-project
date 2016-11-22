import PIL.Image
import PIL.ExifTags
import os
import sys
import exceptions
from ExifDAO import ExifDAO

class ExifService:

    dao = ExifDAO()    

    @staticmethod
    def extractExif(img_addr):
        try:            
            img_file = PIL.Image.open(img_addr)
            tags = {PIL.ExifTags.TAGS[k]: v for k, v in img_file._getexif().items() if k in PIL.ExifTags.TAGS}
            return tags, None          
        except exceptions.IOError as e:            
            return None, 'There is no '+img_addr+' in photos folder'
        except AttributeError as e:
            return None, 'Attribute Error'


    @staticmethod
    def extractAndInsertEXIF(directory, img):
        exif_data, err = ExifService.extractExif(directory+'/'+img)                                   
        if exif_data is not None: ExifService.dao.create(exif_data, img)
        return exif_data, err    


    @staticmethod
    def find(id)
        return dao.find(id)    
    
    
        
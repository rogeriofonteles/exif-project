# exif-project
EXIF project for Waldo Photos job application

This project dependencies are inside requirements.txt

This project uses:

  - Python 2.7
  - MongoDB 2.6
  - pymongo 3.3.1
  - boto3 API to manipulate s3 services
  - pathos multiprocessing lib
    - This will make this project to run just on Linux since the multiprocessing module was able to execute just in this SO.
  - pillow lib to extract EXIF data
  
The main has the following workflow:

  - Images are downloaded by s3Service method called by the end point.
  - After this, EXIF data is extracted by the ExifService and put into the Database by the DAO object
  - Find methods were implemented to make the queries by id and by field if you wish.

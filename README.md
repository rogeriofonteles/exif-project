# exif-project
EXIF project for Waldo Photos job application

This project dependencies are inside requirements.txt

This project uses:

  - Python 2.7
  - MongoDB 3.2
  - boto3 API to manipulate s3 services
  - pathos multiprocessing lib
    - This will make this project to run just on Linux since the multiprocessing module was able to execute just in this SO.
  - pillow lib 3.4.2 to extract EXIF data
  - pymongo 3.3.1  

Install:

  - Create a virtualenv and source it
  - Execute: pip install -r requirements.txt
  - Install mongodb as explained in https://docs.mongodb.com/v3.2/installation/

Tests:

  - python tests.py
  
The main has the following workflow:

  - Images are downloaded by s3Service method called by the end point.
  - After this, EXIF data is extracted by the ExifService and put into the Database by the DAO object
  - Find methods were implemented to make the queries by id and by field if you wish.

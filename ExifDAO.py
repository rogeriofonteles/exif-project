from pymongo import MongoClient
import pymongo

#Class interfacing Application and DB
class ExifDAO:	

	#Create method for EXIF
	def create(self, exif_data, id):
		#Creates the connection with MongoDB
		self.client = MongoClient()
		self.db = self.client.test

		#remove .jpg or .png from image in order to make the id for the document
		new_id = id[:-4]

		try: 
			#Insert data
			json_data = self.create_json(exif_data, new_id)			
			result = self.db.exif.insert_one(json_data)
			return True, "Image "+id+" added in EXIF collection"
		except pymongo.errors.DuplicateKeyError as e:
			return False, "The image "+id+" already exists in the collection"


	#Find method by Id
	def find(self, id_param):
		#Creates the connection with MongoDB
		self.client = MongoClient()
		self.db = self.client.test

		#Find the data by id_param _id
		exif_data = self.db.exif.find({'_id': id_param})
		return exif_data

	#Find method by Arbitrary param
	def find_by_param(self, param_name, param_value):
		#Creates the connection with MongoDB
		self.client = MongoClient()
		self.db = self.client.test

		exif_data = self.db.exif.find({param_name: param_value})
		return exif_data

	#Delete by id method
	def delete(self, id_param):
		#Creates the connection with MongoDB
		self.client = MongoClient()
		self.db = self.client.test

		exif_data = self.db.exif.delete_one({'_id': id_param})
		return exif_data

	#Creation of the JSon to insert in the DB
	def create_json(self, exif_data, id):
		json_data={'_id': id}		
		for tag in exif_data.keys():
			if tag not in ('MakerNote'):
				try:
					#Creates the dict with parsed data
					json_data[str(tag)] = str(exif_data[tag]).encode('utf8')	
				except UnicodeEncodeError as e:
					print("Unicode error in image "+id)
					continue
				except UnicodeDecodeError as e:
					print("Unicode decode error in image "+id)
					continue

		return json_data
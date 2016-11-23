from pymongo import MongoClient
import pymongo

#Class interfacing Application and DB
class ExifDAO:	

	#Create method for EXIF
	def create(self, exif_data, id):
		self.client = MongoClient()
		self.db = self.client.test

		new_id = id[:-4]

		try: 
			json_data = self.create_json(exif_data, new_id)			
			result = self.db.exif.insert_one(json_data)
			return True, "Image "+id+" added in EXIF collection"
		except pymongo.errors.DuplicateKeyError as e:
			return False, "The image "+id+" already exists in the collection"


	#Find method by Id
	def find(self, id_param):
		self.client = MongoClient()
		self.db = self.client.test

		exif_data = self.db.exif.find({'_id': id_param})
		return exif_data

	#Find method by Arbitrary param
	def find_by_param(self, param_name, param_value):
		self.client = MongoClient()
		self.db = self.client.test

		exif_data = self.db.exif.find({param_name: param_value})
		return exif_data

	#Method for JSon building in order to insert in DB
	def create_json(self, exif_data, id):
		json_data={'_id': id}		
		for tag in exif_data.keys():
			if tag not in ('MakerNote'):
				try:
					json_data[str(tag)] = str(exif_data[tag]).encode('utf8')	
				except UnicodeEncodeError as e:
					print("Unicode error in image "+id)
					continue
				except UnicodeDecodeError as e:
					print("Unicode decode error in image "+id)
					continue

		return json_data
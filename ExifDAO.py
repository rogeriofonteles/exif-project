from pymongo import MongoClient
import pymongo

class ExifDAO:	

	def create(self, exif_data, id):
		self.client = MongoClient()
		self.db = self.client.test

		try: 
			json_data = self.createJson(exif_data, id)			
			result = self.db.exif.insert_one(json_data)
			return True, None
		except pymongo.errors.DuplicateKeyError as e:
			return False, "The image "+id+" already exists in the collection"


	def find(self, id_param):
		self.client = MongoClient()
		self.db = self.client.test

		exif_data = self.db.exif.find({'id': id_param})
		return exif_data


	def createJson(self, exif_data, id):
		json_data={'_id': id}		
		for tag in exif_data.keys():
			if tag not in ('MakerNote'):
				try:
					json_data[str(tag)] = str(exif_data[tag])		
				except UnicodeEncodeError as e:
					print("Unicode error in image "+id)
					continue
		return json_data
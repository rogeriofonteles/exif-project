from ExifEndPoint import ExifEndPoint

if __name__ == '__main__':

	#s3 bucket name
	s3_bucket = 'waldo-recruiting'

	#choose concurrency_mode between PARALLEL or SERIAL
	concurrency_mode = 'PARALLEL'

	#EndPoint Instanciation
	endPoint = ExifEndPoint(s3_bucket)	

	#Download and extract exif data
	# endPoint.download_bucket_images('photos')
	# endPoint.process_directory('photos', concurrency_mode)
	endPoint.find('0015A5C3-D186-471J-A032-9E952CFF3CC6.8fedf4a8-8695-4d6d-ad1e-b686daa713a2')
	endPoint.find_by_param('ExifImageHeight', '4016')








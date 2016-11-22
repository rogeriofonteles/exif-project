from ExifEndPoint import ExifEndPoint

if __name__ == '__main__':

	#s3 bucket name
	s3_bucket = 'waldo-recruiting'

	#choose concurrency_mode between PARALLEL or SERIAL
	concurrency_mode = 'PARALLEL'

	endPoint = ExifEndPoint(s3_bucket)	

	#Download and extract exif data
	endPoint.download_bucket_images('photos')
	endPoint.process_directory('photos', concurrency_mode)








from ExifEndPoint import ExifEndPoint

if __name__ == '__main__':

	#s3 bucket name
	s3_bucket = 'waldo-recruiting'

	#choose concurrency_mode between PARALLEL or SERIAL
	concurrency_mode = 'PARALLEL'

	endPoint = ExifEndPoint(s3_bucket)	

	endPoint.s3Service.downloadImages()
	endPoint.processDirectory('photos', concurrency_mode)






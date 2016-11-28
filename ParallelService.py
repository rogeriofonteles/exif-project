from pathos.multiprocessing import ProcessingPool as Pool

#A general class that makes a function to use a pool of process
class ParallelService:

    pool_size = 8   

    @classmethod
    def parallelize(cls, func, *arg):
        #Creates the pool        
        pool = Pool(cls.pool_size)                            
        #Execute 'func' using the process pool
        status_output = pool.map(func, *arg)
        #Wait for the tasks to finish
        pool.close()
        #Wrap current tasks
        pool.join()

        #Join the error messages from each EXIF extraction and put them into a list
        status_list, err_list = zip(*status_output)
        errors = [zipped[1] for zipped in zip(status_list, err_list) if zipped[0] == False]        
        if errors:            
            return None, errors
        else:
            return True, None
        
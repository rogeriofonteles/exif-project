from pathos.multiprocessing import ProcessingPool as Pool

class ParallelService:

    pool_size = 8   

    @classmethod
    def parallelize(cls, func, *arg):
        print arg        
        pool = Pool(cls.pool_size)                            
        status_output = pool.map(func, *arg)
        #Wait for the tasks to finish
        pool.close()
        #Wrap current tasks
        pool.join()

        status_list, err_list = zip(*status_output)
        errors = [zipped[1] for zipped in zip(status_list, err_list) if zipped[0] == False]        
        if errors:            
            return None, errors
        else:
            return True, None
        
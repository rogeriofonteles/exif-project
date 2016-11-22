from pathos.multiprocessing import ProcessingPool as Pool

class ParallelService:

    pool_size = 8   

    @classmethod
    def parallelize(cls, func, arg1, arg2):        
        pool = Pool(cls.pool_size)                            
        status_output = pool.map(func, arg1, arg2)
        #Wait for the tasks to finish
        pool.close()
        #Wrap current tasks
        pool.join()

        status_list, err_list = zip(*status_output)
        index = [status_list.index(i) for i in status_list if i == False]
        if index:            
            return status_list[index[0]], err_list[index[0]]
        else:
            return True, None
        
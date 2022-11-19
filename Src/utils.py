import time
from functools import wraps

def glob2rel(global_position, bounds):
    x = (global_position[0] - bounds.left)/ (bounds.right-bounds.left)
    y = (bounds.top - global_position[1] )/ (bounds.top-bounds.bottom)
    return [x,y]

def rel2img(rel_position, image_size):
    return [int(rel_position[i] * image_size[1-i]) for i in range(2)]

def glob2img(global_position, bounds, image_size):
    return rel2img(glob2rel(global_position= global_position, bounds=bounds),image_size)

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Method {func.__name__} tooks {total_time:.4f} seconds for execution')
        return result
    return timeit_wrapper
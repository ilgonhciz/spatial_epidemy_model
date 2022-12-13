import time
import cv2 as cv
import numpy as np
from functools import wraps
from file import File


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

def generate_video_from_result():
    file = File()
    fig_path = file.get_fig_path(['map','total'])
    fig_path = np.array(fig_path).transpose().tolist()
    video = cv.VideoWriter(file.result_folder + "test.avi", 0, fps=25, frameSize = (1600,1000))
    for [fig_map, fig_total] in fig_path:
        map_image = cv.imread(fig_map)
        map_image = cv.resize(map_image,(1600,700))
        plot_image = cv.imread(fig_total)
        plot_image = cv.resize(plot_image,(1600,300))
        combined = cv.vconcat([map_image, plot_image])
        video.write(combined)
        """ cv.imshow("test1", map_image)
        cv.imshow("test2", plot_image)
        cv.waitKey(0)
        """
    cv.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    generate_video_from_result()
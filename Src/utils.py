
def glob2rel(global_position, bounds):
    x = (global_position[0] - bounds.left)/ (bounds.right-bounds.left)
    y = (bounds.top - global_position[1] )/ (bounds.top-bounds.bottom)
    return [x,y]

def rel2img(rel_position, image_size):
    return [int(rel_position[i] * image_size[1-i]) for i in range(2)]

def glob2img(global_position, bounds, image_size):
    return rel2img(glob2rel(global_position= global_position, bounds=bounds),image_size)
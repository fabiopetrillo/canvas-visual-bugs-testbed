import numpy as np

from sprite_similarity.utils import walltimeit
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

# TODO do 5crop and then calculate similarity across all 6
# then use the lowest similarity as the flag

@walltimeit
def get_pixel_sims(object_images, asset_images):
    return get_scores(object_images, asset_images, calc_pbpsim)

@walltimeit
def get_struc_sims(object_images, asset_images):
    return get_scores(object_images, asset_images, calc_ssim)

@walltimeit
def get_mean_squared_errors(object_images, asset_images):
    return get_scores(object_images, asset_images, mean_squared_error)

def get_scores(object_images, asset_images, score_fn):
    scores = []
    for obj_img, asset_img in zip(object_images, asset_images):
        s = calculate_score(obj_img, asset_img, score_fn)
        scores.append(s)
    return np.array(scores)

def calculate_score(obj_img, asset_img, score_fn):
    obj_size = obj_img.size
    asset_size = asset_img.size
    if obj_size != asset_size:
        errMsg = "Size mismatch: {} and {}".format(obj_size, asset_size)
        raise ValueError(errMsg)
    
    obj_arr = np.array(obj_img)
    asset_arr = np.array(asset_img)
    
    return score_fn(obj_arr, asset_arr)

def calc_pbpsim(obj_arr, asset_arr):
    """
    Pixel-by-pixel similarity
    """
    same = (obj_arr == asset_arr).sum()
    total = np.product(obj_arr.shape)
    return same/total

def calc_ssim(obj_arr, asset_arr):
    """
    Structural similarity
    """
    # 255 bit images
    return ssim(obj_arr, asset_arr, data_range=255, channel_axis=2)

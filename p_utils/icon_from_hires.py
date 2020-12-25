


import sys, os
import imageio

def convert_exr_to_jpg(exr_file, jpg_file):
    if not os.path.isfile(exr_file):
        return False

    filename, extension = os.path.splitext(exr_file)
    if not extension.lower().endswith('.exr'):
        return False

    # imageio.plugins.freeimage.download() #DOWNLOAD IT
    image = imageio.imread(exr_file, format='EXR-FI')

    # remove alpha channel for jpg conversion
    image = image[:,:,:3]

    # normalize the image
    data = image.astype(image.dtype) / image.max() # normalize the data to 0 - 1
    data = 255 * data # Now scale by 255
    rgb_image = data.astype('uint8')
    # rgb_image = imageio.core.image_as_uint(rgb_image, bitdepth=8)

    imageio.imwrite(jpg_file, rgb_image, format='jpeg')
    return True


if __name__ == '__main__':

    exr = r"P:\Arena\sequences\SQA\sh020\out\hires\SQA_sh020_hires.1001.exr"
    jpg = r"P:\Arena\sequences\SQA\sh020\out\hires\SQA_sh020_hires.1001.jpg"

    convert_exr_to_jpg(exr, jpg)
import os
from PIL import Image, ImageOps
from custom_augmenter import augmentation

# The boolean double_augmenter determines, whether only the images and masks in initial_dataset/images_1 (set it to
# False)and initial_dataset/masks_1 are augmented or all images and masks in the folder initial_dataset (set it to True)
# If all are augmented, the images_1/masks_1 and images_2/masks_2 are augmented with the same parameters.
double_augmenter = True

# The label or pixel value of the masks. Depending on the label one wants, this has to be set accordingly.
label = 250

# Opening images and masks from directory initial_dataset/images_1 and initial_dataset/masks_1
directory_images = 'initial_dataset/images_1'
directory_masks = 'initial_dataset/masks_1'
images = os.listdir(directory_images)
masks = os.listdir(directory_masks)

# If double_augmenter is True, open the images and masks from directory initial_dataset/images_2 and
# initial_dataset/masks_2
if double_augmenter:
    directory_images_not_cleaned = 'initial_dataset/images_2'
    directory_masks_not_cleaned = 'initial_dataset/masks_2'
    images_not_cleaned = os.listdir(directory_images_not_cleaned)
    masks_not_cleaned = os.listdir(directory_masks_not_cleaned)

# Getting the image's and mask's width and height
directory_image0 = directory_images + '/' + images[0]
image0 = Image.open(directory_image0)
width, height = image0.size

# Directory to the pink and black image
directory_pink = 'background.png'
directory_black = 'black.png'

# Looping through the images
for i in range(len(images)):
    # Loading the black and pink images, turning black image to grayscale and getting access to pixel values of black
    # and pink image
    pink = Image.open(directory_pink)
    black = Image.open(directory_black)
    black = ImageOps.grayscale(black)
    pix_pink = pink.load()
    pix_black = black.load()

    # Accessing image and mask name of at current position
    image_name = images[i]
    mask_name = masks[i]
    image_directory = directory_images + '/' + image_name
    mask_directory = directory_masks + '/' + mask_name

    # Opening image and mask, resizing mask to the size of the image, and turn mask to grayscale
    image = Image.open(image_directory)
    mask = Image.open(mask_directory)
    mask = mask.resize((width, height))
    mask = ImageOps.grayscale(mask)

    if double_augmenter:
        # Create copy of pink and black image, and get access to their pixel values
        pink_nc = pink.copy()
        black_nc = black.copy()
        black_nc = ImageOps.grayscale(black_nc)
        pix_pink_nc = pink_nc.load()
        pix_black_nc = black_nc.load()

        # Opening images and masks from folder initial_dataset/images_2 and initial_dataset/masks_2
        image_not_cleaned_name = images_not_cleaned[i]
        mask_not_cleaned_name = masks_not_cleaned[i]
        image_nc_dir = directory_images_not_cleaned + '/' + image_not_cleaned_name
        mask_nc_dir = directory_masks_not_cleaned + '/' + mask_not_cleaned_name
        img_nc = Image.open(image_nc_dir)
        mask_nc = Image.open(mask_nc_dir)
        mask_nc = mask_nc.resize((width, height))
        mask_nc = ImageOps.grayscale(mask_nc)

    # If double_augmenter is True, augmentation from all images and masks in folder initial_dataset. Else, only form
    # images_1 and masks_1.
    if double_augmenter:
        augmentation(double_augmenter, image_name, image, pink, pix_pink, mask, black, pix_black, width, height, label,
                     img_nc, pink_nc, pix_pink_nc, mask_nc, black_nc, pix_black_nc)
    else:
        augmentation(double_augmenter, image_name, image, pink, pix_pink, mask, black, pix_black, width, height, label)

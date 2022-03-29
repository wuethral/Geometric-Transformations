import random
from custom_rotate import check_pixel_pink


def zoom_in(*args):
    '''This method zooms into the image and mask, making the object larger. It then saves the image and mask int the
    folder 'zoom_folder' '''

    # Accessing values in list args
    double_augmenter = args[0]
    image_name = args[1]
    img = args[2]
    mask = args[3]
    width = args[4]
    height = args[5]
    counter = args[6]
    label = args[7]

    # If double_augmenter is True, accessing additional values in list args
    if double_augmenter:
        img_nc = args[8]
        mask_nc = args[9]

    # random_nr determines, how much is zoomed in
    random_nr = 1 - 0.5 * random.random()

    # Determining the left, right, top and bottom coordinates for cropping
    left = int(width / 2 - (random_nr * width) / 2)
    right = int(width / 2 + (random_nr * width) / 2)
    top = int(height / 2 - (random_nr * height) / 2)
    bottom = int(height / 2 + (random_nr * height) / 2)

    # Cropping the images and masks and getting access to the pixels of the cropped images and masks
    img = img.crop((left, top, right, bottom))
    mask = mask.crop((left, top, right, bottom))
    initial_size = (width, height)
    img = img.resize(initial_size)
    mask = mask.resize(initial_size)
    img_pixel = img.load()
    mask_pixel = mask.load()

    if double_augmenter:
        img_nc = img_nc.crop((left, top, right, bottom))
        mask_nc = mask_nc.crop((left, top, right, bottom))
        img_nc = img_nc.resize(initial_size)
        mask_nc = mask_nc.resize(initial_size)
        img_nc_pixel = img_nc.load()
        mask_nc_pixel = mask_nc.load()

    # This loop guarantees that the mask matches the object on the image
    for x in range(width):
        for y in range(height):
            if check_pixel_pink(img_pixel, x, y):
                mask_pixel[x,y] = 0
            else:
                mask_pixel[x,y] = label
            if double_augmenter:
                if check_pixel_pink(img_nc_pixel, x, y):
                    mask_nc_pixel[x,y] = 0
                else:
                    mask_nc_pixel[x,y] = label

    # Saving the images and masks
    save_name_image = 'zoom_folder/images_1/' + image_name[:-4] +'_' + str(counter) + '.png'
    save_name_mask = 'zoom_folder/masks_1/' + image_name[:-4] + '_' + str(counter) + '.png'
    img.save(save_name_image)
    mask.save(save_name_mask)

    if double_augmenter:
        save_name_image_nc = 'zoom_folder/images_2/' + image_name[:-4] +'_' + str(counter) + '.png'
        save_name_mask_nc = 'zoom_folder/masks_2/' + image_name[:-4] + '_' + str(counter) + '.png'
        img_nc.save(save_name_image_nc)
        mask_nc.save(save_name_mask_nc)


def zoom_out(*args):
    '''This method zooms out of the image and mask, making the object smaller. It then saves the image and mask int the
    folder 'zoom_folder' '''

    # Accessing values in list args
    double_augmenter = args[0]
    image_name = args[1]
    img = args[2]
    mask = args[3]
    black = args[4]
    width = args[5]
    height = args[6]
    pink = args[7]
    counter = args[8]
    label = args[9]

    # If double_augmenter is True, accessing additional values in list args
    if double_augmenter:
        img_nc = args[10]
        mask_nc = args[11]
        black_nc = args[12]
        pink_nc = args[13]

    # random_nr determines, how much is zoomed out
    random_nr = random.random() * 0.5
    # Generating the new width and height of the images and masks
    new_width = int((1 + random_nr) * width)
    new_height = int((1 + random_nr) * height)
    zoom_out_size = (new_width, new_height)
    # Resizing the pink and black images
    pink = pink.resize(zoom_out_size)
    black = black.resize(zoom_out_size)
    pink_pix = pink.load()
    black_pix = black.load()
    img_pix = img.load()
    mask_pix = mask.load()

    if double_augmenter:
        black_nc = black_nc.resize(zoom_out_size)
        pink_nc = pink_nc.resize(zoom_out_size)
        pink_for_clean_pix = pink_nc.load()
        black_for_clean_pix = black_nc.load()
        img_nc_pix = img_nc.load()
        mask_nc_pix = mask_nc.load()

    # Variables for the difference of the new width and old width, divided by 2
    difference_in_width_div_by_two = int((new_width - width) /2)
    # Variables for the difference of the new height and old height, divided by 2
    difference_in_height_div_by_two = int((new_height - height) / 2)

    # Writing the image's and mask's pixels on the pink and black images, so that image and mask are placed
    # approximately in the middle of the pink and black image. Without the of set of - 2 at the end, the range is out
    # of bounds
    for x in range(difference_in_width_div_by_two, new_width - difference_in_width_div_by_two - 2):
        for y in range(difference_in_height_div_by_two, new_height - difference_in_height_div_by_two - 2):
            pink_pix[x, y] = img_pix[x-difference_in_width_div_by_two, y-difference_in_height_div_by_two]
            black_pix[x, y] = mask_pix[x-difference_in_width_div_by_two, y-difference_in_height_div_by_two]

            if double_augmenter:
                pink_for_clean_pix[x, y] = img_nc_pix[x - difference_in_width_div_by_two, y -
                                                      difference_in_height_div_by_two]
                black_for_clean_pix[x, y] = mask_nc_pix[x - difference_in_width_div_by_two, y -
                                                        difference_in_height_div_by_two]

    # This loop guarantees that the mask matches the object on the image
    for x in range(width):
        for y in range(height):
            if check_pixel_pink(pink_pix, x, y):
                black_pix[x,y] = 0
            else:
                black_pix[x,y] = label
            if double_augmenter:
                if check_pixel_pink(pink_for_clean_pix, x, y):
                    black_for_clean_pix[x,y] = 0
                else:
                    black_for_clean_pix[x,y] = label

    # Resizing the pink and black images and saving them in the zoom folder
    pink.resize((width,height))
    black.resize((width,height))
    save_name_image = 'zoom_folder/images_1/' + image_name[:-4] + '_' + str(counter) + '.png'
    save_name_mask = 'zoom_folder/masks_1/' + image_name[:-4] + '_' + str(counter) + '.png'
    pink.save(save_name_image)
    black.save(save_name_mask)
    if double_augmenter:
        pink_nc.resize((width,height))
        black_nc.resize((width,height))
        save_name_image_nc = 'zoom_folder/images_2/' + image_name[:-4] + '_' + str(counter) + '.png'
        save_name_mask_nc = 'zoom_folder/masks_2/' + image_name[:-4] + '_' + str(counter) + '.png'
        pink_nc.save(save_name_image_nc)
        black_nc.save(save_name_mask_nc)
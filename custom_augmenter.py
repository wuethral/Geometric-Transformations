from PIL import Image, ImageOps

from custom_translation import making_pixels_pink, making_pixels_pink_2, translate, check_all_edge_pixel_black_y_axis, \
    check_all_edge_pixel_black_x_axis
from custom_rotate import rotation_making_black_pixels_pink, turn_pink_2, turn_black
from custom_zoom import zoom_in, zoom_out
from random import random


def augmentation(*args):
    '''In this method, all the augmentation methods for zoom, rotation and translation are called'''

    # Accessing values in list args
    double_augmenter = args[0]
    image_name = args[1]
    image = args[2]
    pink = args[3]
    pix_pink = args[4]
    mask = args[5]
    black = args[6]
    pix_black = args[7]
    width = args[8]
    height = args[9]
    label = args[10]

    # If double_augmenter is True, accessing rest of values in list args
    if double_augmenter:
        img_nc = args[11]
        pink_nc = args[12]
        pix_pink_nc = args[13]
        mask_nc = args[14]
        black_nc = args[15]
        pix_black_nc = args[16]

    # This number decides, how many augmentations images should be generated for the current image
    number_of_augmentations = 2

    # Creating an augmented image with every loop
    for i in range(number_of_augmentations):

        # Incrementing i
        i = i + 1

        # random() creates number between 0 and 1. zoom_random_nr is for deciding if it should be zoomed in or out
        zoom_random_nr = random()
        # if zoom_random_nr is smaller than 0.5, we zoom in (call method zoom in)
        if zoom_random_nr < 0.5:
            # If double_augmenter is True, zoom_in for all images/masks in initial_dataset
            if double_augmenter:
                zoom_in(double_augmenter, image_name, image, mask, width, height, i, label, img_nc, mask_nc)
            # Else zoom_in only for images and masks in initial_dataset/images_1 and initial_dataset/masks_1
            else:
                zoom_in(double_augmenter, image_name, image, mask, width, height, i, label)
        # else zoom out (method zoom_out)
        else:
            # If double_augmenter is True, zoom_out for all images/masks in initial_dataset
            if double_augmenter:
                zoom_out(double_augmenter, image_name, image, mask, black, width, height, pink, i, label, img_nc, mask_nc,
                         black_nc, pink_nc)
            # Else zoom_out only for images and masks in initial_dataset/images_1 and initial_dataset/masks_1
            else:
                zoom_out(double_augmenter, image_name, image, mask, black, width, height, pink, i, label)

        # Opening images and masks that have been saved into the folders zoom_folder/images_1 and zoom_folder/masks_1 in
        # the methods zoom_in and zoom_out.
        directory_zoom_img = 'zoom_folder/images_1/' + image_name[:-4] + '_' + str(i) + '.png'
        directory_zoom_mask = 'zoom_folder/masks_1/' + image_name[:-4] + '_' + str(i) + '.png'

        # If double_augmenter is True
        if double_augmenter:
            # Opening images and masks that have been saved into the folders zoom_folder/images_2 and
            # zoom_folder/masks_2 in the methods zoom_in and zoom_out.
            directory_zoom_img_not_cleaned = 'zoom_folder/images_2/' + image_name[:-4] + '_' + str(i) + '.png'
            directory_zoom_mask_not_cleaned = 'zoom_folder/masks_2/' + image_name[:-4] + '_' + str(i) + '.png'

        # Opening images and masks and pixel value of masks in dir initial_images/images_1 and initial_images/masks_1
        img_zoom = Image.open(directory_zoom_img)
        mask_zoom = Image.open(directory_zoom_mask)
        mask_zoom = ImageOps.grayscale(mask_zoom)
        pix_zoom = mask_zoom.load()
        pixel = pix_zoom

        # If double_augmenter is True, opening images and masks and pixel value of masks in dir initial_images/images_2
        # and initial_images/masks_2
        if double_augmenter:
            img_zoom_nc = Image.open(directory_zoom_img_not_cleaned)
            mask_zoom_nc = Image.open(directory_zoom_mask_not_cleaned)
            mask_zoom_nc = ImageOps.grayscale(mask_zoom_nc)
            pix_zoom_nc = mask_zoom_nc.load()
            pixel = pix_zoom_nc

        # Generating variable with random number between 0 and 360. This number determines the rotation of the images
        # and masks
        random_rotate_nr = int(random() * 360)
        # The method check_all_edge_pixel_black_y_axis checks for the mask, if the pixel on the left and right edge are
        # black. If they are not black, the objects is cut of by the edge and random_rotate_nr is set to 0.
        check_all_black_y_axis = check_all_edge_pixel_black_y_axis(pixel, width, height)
        if check_all_black_y_axis == False:
            random_rotate_nr = 0

        # The method check_all_edge_pixel_black_x_axis checks for the mask, if the pixel on the top and bottom edge are
        # black. If they are not black, the objects is cut of by the edge and random_rotate_nr is set to 0.
        check_all_black_x_axis = check_all_edge_pixel_black_x_axis(pixel, width, height)
        if check_all_black_x_axis == False:
            random_rotate_nr = 0
        # Rotate the images and masks and accessing their pixel values
        rotated_img = img_zoom.rotate(random_rotate_nr)
        rotated_mask = mask_zoom.rotate(random_rotate_nr)
        pix_image = rotated_img.load()
        pix_mask = rotated_mask.load()

        # Rotate the images and masks and accessing their pixel values
        if double_augmenter:
            rotated_img_nc = img_zoom_nc.rotate(random_rotate_nr)
            rotated_mask_nc = mask_zoom_nc.rotate(random_rotate_nr)
            pix_image_nc = rotated_img_nc.load()
            pix_mask_nc = rotated_mask_nc.load()

        # For every y value, call method rotation_making_black_pixels_pink, which turns the pixels becoming black during
        # the rotation pink again.
        for y in range(height):
            rotation_making_black_pixels_pink(y, width, pix_image, pix_mask)
            if double_augmenter:
                rotation_making_black_pixels_pink(y, width, pix_image_nc, pix_mask_nc)

        # x_trans and y_trans determine, the translations along the x-axis and y-axis. With this setting, the value for
        # x_trans can be any random number between 0 and the image's width divided by 3; For y_trans any value between 0
        # and the image's height divided by 3.
        x_trans = int(width / 3 * random())
        y_trans = int(height / 3 * random())

        # Checking again, if all right and left edge pixels are black. If they are, x_trans is not changed. if the
        # object is on the edge, x_trans is set to 0, because there should be no translation along the x-axis.
        check_all_black_y_axis = check_all_edge_pixel_black_y_axis(pix_zoom, width, height)
        if check_all_black_y_axis == False:
            x_trans = 0

        # Checking again, if all top and bottom edge pixels are black. If they are, y_trans is not changed. if the
        # object is on the edge, y_trans is set to 0, because there should be no translation along the y-axis.
        check_all_black_x_axis = check_all_edge_pixel_black_x_axis(pix_zoom, width, height)
        if check_all_black_x_axis == False:
            y_trans = 0

        # random_number_for_x_dir and random_number_for_y_dir determine, whether the translations are in the positive or
        # negative x- and y-direction.
        random_number_for_x_dir = random()
        random_number_for_y_dir = random()

        # random_number_for_x_dir smaller than 0.5 initiates a translation in the positive x-direction;
        # Larger than 0.5 a translation in the positive x-direction.
        if random_number_for_x_dir < 0.5:
            x_trans_positiv = True
        else:
            x_trans_positiv = False

        # random_number_for_y_dir smaller than 0.5 initiates a translation in the positive y-direction;
        # Larger than 0.5 a translation in the positive y-direction.
        if random_number_for_y_dir < 0.5:
            y_trans_positiv = True
        else:
            y_trans_positiv = False

        # Translation in the positive x-direction. Calling the method making_pixels_pink
        if x_trans_positiv:
            # Looping through the coordinates form 0 to x_trans
            for x_coord in range(x_trans):
                making_pixels_pink(x_coord, height, pix_pink, pix_black)
                if double_augmenter:
                    making_pixels_pink(x_coord, height, pix_pink_nc, pix_black_nc)
        # Translation in the negative x-direction. Calling the method making_pixels_pink
        else:
            # Looping through the coordinates form (width - x_trans) to width
            for x_coord in range(width - x_trans, width):
                making_pixels_pink(x_coord, height, pix_pink, pix_black)
                if double_augmenter:
                    making_pixels_pink(x_coord, height, pix_pink_nc, pix_black_nc)

        # Translation in the positive y-direction. Calling the method making_pixels_pink
        if y_trans_positiv:
            # Looping through the coordinates from 0 to y_trans
            for y_coord in range(y_trans):
                making_pixels_pink_2(y_coord, width, pix_pink, pix_black)
                if double_augmenter:
                    making_pixels_pink_2(y_coord, width, pix_pink_nc, pix_black_nc)
        # Translation in the negative y-direction. Calling the method making_pixels_pink
        else:
            # Looping through the coordinates from (height - y_trans) to height
            for y_coord in range(height - y_trans, height):
                making_pixels_pink_2(y_coord, width, pix_pink, pix_black)
                if double_augmenter:
                    making_pixels_pink_2(y_coord, width, pix_pink_nc, pix_black_nc)

        # Positive x-translation
        if x_trans_positiv:
            # Looping through x_coord to width
            for x_coord in range(x_trans, width):
                # Positive y-translation
                if y_trans_positiv:
                    # Looping through y_trans to height
                    for y_coord in range(y_trans, height):
                        # Create the translated image
                        translate(x_trans, y_trans, x_coord, y_coord, pix_image, pix_mask, pix_pink, pix_black,
                                  x_trans_positiv, y_trans_positiv)
                        if double_augmenter:
                            translate(x_trans, y_trans, x_coord, y_coord, pix_image_nc, pix_mask_nc, pix_pink_nc, pix_black_nc,
                                      x_trans_positiv, y_trans_positiv)
                # Negative y-translation
                else:
                    # Looping through 0 to (height-y_trans)
                    for y_coord in range(0, height - y_trans):
                        # Create the translated image
                        translate(x_trans, y_trans, x_coord, y_coord, pix_image, pix_mask, pix_pink, pix_black,
                                  x_trans_positiv, y_trans_positiv)
                        if double_augmenter:
                            translate(x_trans, y_trans, x_coord, y_coord, pix_image_nc, pix_mask_nc, pix_pink_nc,
                                      pix_black_nc, x_trans_positiv, y_trans_positiv)
        # Negative x-translation
        else:
            # Looping through x_coord to (width - x_trans)
            for x_coord in range(0, width - x_trans):
                # Positive y-translation
                if y_trans_positiv:
                    # Looping through y_trans to height
                    for y_coord in range(y_trans, height):
                        # Create the translated image
                        translate(x_trans, y_trans, x_coord, y_coord, pix_image, pix_mask, pix_pink, pix_black,
                                  x_trans_positiv, y_trans_positiv)
                        if double_augmenter:
                            translate(x_trans, y_trans, x_coord, y_coord, pix_image_nc, pix_mask_nc, pix_pink_nc,
                                      pix_black_nc, x_trans_positiv, y_trans_positiv)
                # Negative y-translation
                else:
                    # Looping through y_coord to (height - y_trans)
                    for y_coord in range(0, height - y_trans):
                        # Create the translated image
                        translate(x_trans, y_trans, x_coord, y_coord, pix_image, pix_mask, pix_pink, pix_black,
                                  x_trans_positiv, y_trans_positiv)
                        if double_augmenter:
                            translate(x_trans, y_trans, x_coord, y_coord, pix_image_nc, pix_mask_nc, pix_pink_nc,
                                      pix_black_nc, x_trans_positiv, y_trans_positiv)

        # Saving the augmented images and masks in the folders augmented_dataset/augmented_images_1 and
        # augmented_dataset/augmented_masks_1
        save_name_img = 'augmented_dataset/augmented_images_1/' + image_name[:-4] + '_' +  str(i) + '.png'
        pink.save(save_name_img)
        save_name_mask = 'augmented_dataset/augmented_masks_1/' + image_name[:-4] + '_' +  str(i) + '.png'
        black.save(save_name_mask)

        # Saving the augmented images and masks in the folders augmented_dataset/augmented_images_2 and
        # augmented_dataset/augmented_masks_2
        if double_augmenter:
            save_name_img_nc = 'augmented_dataset/augmented_images_2/' + image_name[:-4] + '_' +  str(i) + '.png'
            pink_nc.save(save_name_img_nc)
            save_name_mask_nc = 'augmented_dataset/augmented_masks_2/' + image_name[:-4] + '_' +  str(i) + '.png'
            black_nc.save(save_name_mask_nc)

        # Turning the black and pink images black and pink again, for fresh usage for the next image for augmentation
        for x in range(0,width):
            for y in range(0,height):
                turn_pink_2(x, y, pix_pink)
                turn_black(x, y, pix_black)
                if double_augmenter:
                    turn_pink_2(x,y, pix_pink_nc)
                    turn_black(x,y, pix_black_nc)

        # Line 268-280 check, if all pixels on the mask have either the pixel value of the label or 0 (background).
        # If this is not the case, there is a warning on the console. This is for safety, that later no wrong masks are
        # feed into the training of the Mask R-CNN
        warning_pixels_masks = False
        for x in range(width):
            for y in range(height):
                if black.load()[x, y] != 0 and black.load()[x, y] != label:
                    warning_pixels_masks = True
                if double_augmenter:
                    if black_nc.load()[x, y] != 0 and black_nc.load()[x, y] != label:
                        warning_pixels_masks = True

        if warning_pixels_masks:
            print('WARNING, Masks have wrong pixels!')
            print(' ')
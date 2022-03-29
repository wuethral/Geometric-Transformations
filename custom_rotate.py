def check_pixel_pink(pix, x, y):
    '''Method to check if pixel is pink or not'''

    if pix[x,y][0] == 250 and pix[x,y][1] == 14 and pix[x,y][2] == 191:
        return True
    else:
        return False


def turn_pink(x_2, y, pix, width):
    '''Method to turn pixel in range [x_2, width] pink'''

    for x in range(x_2, width):
        pix[x, y] = (250,14,191)


def turn_pink_2(x,y,pix):
    '''Method to turn single pixel pink'''
    pix[x, y] = (250, 14, 191)


def turn_black(x,y,pix):
    '''Method to turn single pixel black'''
    pix[x, y] = 0


def rotation_making_black_pixels_pink(y, width, pix_image, pix_mask):
    '''Method that changes all pixels that became black during the rotation back to pink'''


    if pix_image[0, y][0] == 0 and pix_image[0, y][1] == 0 and pix_image[0, y][2] == 0:
        flag_pink = False
        x = 0

        while flag_pink == False:

            if pix_image[x, y][0] != 0 or pix_image[x, y][1] != 0 or pix_image[x, y][2] != 0:
                flag_pink = True
            else:
                pix_image[x, y] = (250, 14, 191)
                x += 1

    flag_pink_black = False

    while flag_pink_black == False:

        for x_2 in range(0, width-1):
            if ((pix_image[x_2, y][0] != 0 and pix_image[x_2, y][1] != 0 and pix_image[x_2, y][2] != 0))\
                    and ((pix_image[x_2 + 1, y][0] == 0 and pix_image[x_2 + 1, y][1] == 0
                          and pix_image[x_2 + 1, y][2] == 0)) and pix_mask[x_2, y] == 0:

                turn_pink(x_2, y, pix_image, width)
                flag_pink_black = True

        flag_pink_black = True
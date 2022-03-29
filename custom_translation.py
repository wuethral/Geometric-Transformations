def making_pixels_pink(x_coord, height, pix_pink, pix_black):
    ''' This method turns a pixel pink (for image) and turns pixel black (for mask) in the range height'''

    for i in range(height):
        pix_pink[x_coord, i] = (250, 14, 191)
        pix_black[x_coord, i] = 0


def making_pixels_pink_2(y_coord, width, pix, pix_black):
    '''This method turns a pixel pink (for image) and turns pixel black (for mask) in the range width'''
    for i in range(width):
        pix[i, y_coord] = (250, 14, 191)
        pix_black[i, y_coord] = 0


def translate(x_trans, y_trans,x_coord, y_coord, pix_original, pix_mask, pix, pixel_black, x_trans_positiv,
              y_trans_positiv):
    '''Method that translate whole image and mask'''

    # Translation in positive x and y directions
    if x_trans_positiv and y_trans_positiv:
        pix[x_coord, y_coord] = pix_original[x_coord-x_trans, y_coord-y_trans]
        pixel_black[x_coord, y_coord] = pix_mask[x_coord-x_trans, y_coord-y_trans]

    # Translation in positive x and negative y directions
    elif x_trans_positiv and not y_trans_positiv:
        pix[x_coord, y_coord] = pix_original[x_coord - x_trans, y_coord + y_trans]
        pixel_black[x_coord, y_coord] = pix_mask[x_coord - x_trans, y_coord + y_trans]

    # Translation in negative x and positive y directions
    elif not x_trans_positiv and y_trans_positiv:
        pix[x_coord, y_coord] = pix_original[x_coord + x_trans, y_coord - y_trans]
        pixel_black[x_coord, y_coord] = pix_mask[x_coord + x_trans, y_coord - y_trans]

    # Translation in negative x and y directions
    else:
        pix[x_coord, y_coord] = pix_original[x_coord + x_trans, y_coord + y_trans]
        pixel_black[x_coord, y_coord] = pix_mask[x_coord + x_trans, y_coord + y_trans]


def check_all_edge_pixel_black_y_axis(pix_zoom, width, height):
    '''Method to check, if pixels on the mask's edge on the left and right are black'''

    check_pixel_black = True

    for y in range(height):
        if pix_zoom[0, y] != 0:
            check_pixel_black = False
            break
        elif pix_zoom[width-1, y] != 0:

            check_pixel_black = False
            break

    return check_pixel_black


def check_all_edge_pixel_black_x_axis(pix_zoom, width, height):
    '''Method to check, if pixels on the mask's edge on the bottom and top are black'''

    check_pixel_black = True
    for x in range(width):
        if pix_zoom[x,0] != 0:
            check_pixel_black = False
            break
        elif pix_zoom[x, height-1] != 0:
            check_pixel_black = False
            break

    return check_pixel_black
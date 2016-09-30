from collections import defaultdict


def transpose(image):
    transposed = [[image[col][row] for col in range(len(image))]
                  for row in range(len(image[0]))]
    return transposed


def gray_pixel(pixel):
    gray_pixel = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
    pixel = (gray_pixel, gray_pixel, gray_pixel)
    return pixel


def grayscale(func):
    def gray_image(*args):
        gray_image = [[gray_pixel((args[0][row][col]))
                       for col in range(len((args[0][0])))]
                      for row in range(len((args[0])))]
        if len(args) == 1:
            return func(gray_image)
        else:
            return func(gray_image, args[1])
    return gray_image


@grayscale
def rotate_right(image):
    rotated_image = transpose(image)
    rotated_image = [rotated_image[row][::-1]
                     for row in range(len(rotated_image))]
    return rotated_image


@grayscale
def rotate_left(image):
    rotated_image = [image[col][::-1] for col in range(len(image))]
    rotated_image = transpose(rotated_image)
    return rotated_image


def invert_pixel(pixel):
    pixel = (255 - pixel[0], 255 - pixel[1], 255 - pixel[2])
    return pixel


@grayscale
def invert(image):
    inverted_image = [[invert_pixel(image[row][col])
                       for col in range(len(image[0]))]
                      for row in range(len(image))]
    return inverted_image


def lighten_pixel(pixel, coef):
    pixel = (pixel[0] + int(coef * (255 - pixel[0])), pixel[1] +
             int(coef * (255 - pixel[1])), pixel[2] +
             int(coef * (255 - pixel[2])))
    return pixel


@grayscale
def lighten(image, coef):
    light_image = [[lighten_pixel(image[row][col], coef)
                    for col in range(len(image[0]))]
                   for row in range(len(image))]
    return light_image


def darken_pixel(pixel, coef):
    pixel = (pixel[0] - int(coef * (pixel[0] - 0)), pixel[1] -
             int(coef * (pixel[1] - 0)), pixel[2] - int(coef * (pixel[2] - 0)))
    return pixel


@grayscale
def darken(image, coef):
    dark_image = [[darken_pixel(image[row][col], coef)
                   for col in range(len(image[0]))]
                  for row in range(len(image))]
    return dark_image


def create_histogram(image):
    histogram = {'red': defaultdict(int), 'green': defaultdict(int),
                 'blue': defaultdict(int)}
    for row in range(len(image)):
        for col in range(len(image[0])):
            pixel = image[row][col]
            histogram['red'][pixel[0]] += 1
            histogram['green'][pixel[1]] += 1
            histogram['blue'][pixel[2]] += 1
    return histogram

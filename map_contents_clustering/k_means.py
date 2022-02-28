from itertools import product
from random import uniform
from math import sqrt
from PIL import Image
from Pixel import Pixel


def load_map_data(map_file):
    """ Loads map data with pillow library from .jpg or .png file. Returns
    list of Pixel objects.

    Arguments:
    map_file - path to an image in .jpg or .png format. """

    map_image = Image.open(map_file)
    map_image = map_image.convert('RGB')
    width, height = map_image.size
    pixels = list()

    # itertools.product() calculates Cartesian product for given iterable
    # objects.
    for coordinates in product(range(width), range(height)):
        x, y = coordinates[0], coordinates[1]
        r, g, b = map_image.getpixel(coordinates)
        pixels.append(Pixel(x, y, r, g, b))

    return pixels


def draw_layer(source_map_file, layer_pixels, file_name='layer'):
    """ Create a file with given pixels on their positions. Other pixels are
    painted with white (RGB: (255, 255, 255).

    Arguments:
    source_map_file - path to map image on which clustering was proceeded;
    layer_pixels - list of pixels to be drawn;
    file_name - name of a new file to save. """

    source_map_file = Image.open(source_map_file)
    layer_image = Image.new('RGB', source_map_file.size, (255, 255, 255))

    for pixel in layer_pixels:
        layer_image.putpixel(
            (pixel.x, pixel.y), (pixel.r, pixel.g, pixel.b))

    layer_image.save(file_name, 'PNG')


def proceed_clustering(pixels, clusters, iterations=2):
    """ Divide a list of pixels into k groups by pixel's RGB components.
    Returns a list of clustered pixels with layer != None.
    Warning: this function doesn't create new list of pixels, it changes the
    modifies one!

    Arguments:
    pixels - list of class "Pixel" objects;
    k - integer value, representing number of clusters. """

    cluster_centers = generate_random_cluster_centers(clusters)

    for i in range(iterations):
        recalculate_cluster_centers(pixels, cluster_centers)
        distribute_to_clusters(pixels, cluster_centers)


def generate_random_cluster_centers(k):
    """ Generate k class "Pixel" objects with random RGB components. Returns
    list of class "Pixel" objects.

    Arguments:
    k - integer value, representing number of clusters. """

    pixels = list()

    for i in range(k):
        values = [round(uniform(0, 255), 1) for i in range(3)]
        pixels.append(
            Pixel(None, None, values[0], values[1], values[2],
                  layer='cluster center'))

    return pixels


def calculate_euclidean_distance(pixel_1, pixel_2):
    """ Calculate Euclidean distance between two pixels. Returns float value,
    representing distance.

    Arguments:
    pixel_1, pixel_2 - objects of class "Pixel". """

    return sqrt(pow(pixel_1.r - pixel_2.r, 2) +
                pow(pixel_1.g - pixel_2.g, 2) +
                pow(pixel_1.b - pixel_2.b, 2))


def recalculate_cluster_centers(pixels, cluster_centers):
    """ Using Euclidean distance finds for each pixel the closest cluster
    center and calculates for this cluster center new coordinates as
    arithmetic average between each RGB component of each pixel, respectively.
    Warning: this function doesn't create new list of cluster centers, it
    modifies the given one!

    Attributes:
    pixels - list of class "Pixel" objects;
    cluster_centers - list of class "Pixel" objects, representing cluster
    centers. """

    for pixel in pixels:
        max_distance = 1024
        closest_cluster_center = None

        for cluster_center in cluster_centers:
            distance = calculate_euclidean_distance(pixel, cluster_center)

            if distance < max_distance:
                max_distance = distance
                closest_cluster_center = cluster_center

        closest_cluster_center.r = round(
            (closest_cluster_center.r + pixel.r) / 2, 1)
        closest_cluster_center.g = round(
            (closest_cluster_center.g + pixel.g) / 2, 1)
        closest_cluster_center.b = round(
            (closest_cluster_center.b + pixel.b) / 2, 1)


def distribute_to_clusters(pixels, cluster_centers):
    """ Calculates Euclidean distance between each pixel and each cluster
    center and sets layer of each pixel equal to RGB components of the nearest
    cluster center.
    Warning: this function doesn't create new list of pixels, it changes the
    modifies one!

    Attributes:
    pixels - list of class "Pixel" objects;
    cluster_centers - list of class "Pixel" objects, representing cluster
    centers. """

    for pixel in pixels:
        max_distance = 1024
        closest_cluster_center = None

        for cluster_center in cluster_centers:
            distance = calculate_euclidean_distance(pixel, cluster_center)

            if distance < max_distance:
                max_distance = distance
                closest_cluster_center = cluster_center.rgb_to_string()

        pixel.layer = closest_cluster_center

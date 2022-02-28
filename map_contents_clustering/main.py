import os
import k_means

from itertools import product
from datetime import datetime
from shutil import make_archive
from shutil import rmtree


MAPS = [
    '../resources/topographic_map_example.png',
    '../resources/topographic_map_example_2.png',
]

CLUSTERS = [
    4,
    5,
    6,
    7,
    8,
]

ITERATIONS = [
    16,
    32,
    64,
]


# TODO: need to add check if files in MAPS exist.
def main():
    # Archiving previous results and clear folder for new ones.
    archive_previous_results()

    # Creating folders for results for each map.
    for path_to_map in MAPS:
        map_name = os.path.basename(path_to_map)
        map_name_no_extension = os.path.splitext(map_name)
        os.mkdir(
            f'../resources/map_contents_clustering/{map_name_no_extension[0]}')

    # itertools.product() calculates Cartesian product for given iterable
    # objects.
    for parameters in product(MAPS, CLUSTERS, ITERATIONS):
        path_to_map = parameters[0]
        clusters_number = parameters[1]
        iterations_number = parameters[2]

        for i in range(3):
            # Proceed clustering.
            pixels = k_means.load_map_data(path_to_map)
            k_means.proceed_clustering(pixels, clusters=clusters_number,
                                       iterations=iterations_number)

            # Divide into layers.
            layers = dict()

            for pixel in pixels:
                if pixel.layer not in layers:
                    layers[pixel.layer] = list()
                    layers[pixel.layer].append(pixel)

                else:
                    layers[pixel.layer].append(pixel)

            # Create k images representing clustered layers.
            folder = f'../resources/map_contents_clustering/' \
                     f'{os.path.splitext(os.path.basename(path_to_map))[0]}/' \
                     f'clus{clusters_number}iter{iterations_number}_{i + 1}'
            os.mkdir(folder)

            for layer, layer_pixels in layers.items():
                k_means.draw_layer(path_to_map, layer_pixels, f'{folder}/{layer.replace(".", "_")}.png')


def archive_previous_results():
    """ If results folder (../resources/map_contents_clustering) is not
    empty, archives its contents and saves zip into
    ../resources/archives as "date_time".zip. Then deletes all contents from
    results folder. """
    folders = os.listdir('../resources/map_contents_clustering')

    if len(folders) != 0:
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        make_archive(f'../resources/archives/{current_datetime}', 'zip',
                     '../resources/map_contents_clustering')

        # Clearing folder for new results.
        for folder in os.listdir('../resources/map_contents_clustering'):
            rmtree(f'../resources/map_contents_clustering/{folder}')


if __name__ == '__main__':
    main()

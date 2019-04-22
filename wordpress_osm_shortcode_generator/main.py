#!/usr/bin/env python3

import os
import click
import magic
import gpxpy
import gpxpy.gpx
import logging
import pickle

from workout import Workout
from marker import Marker
from constants import EQUATORIAL_CIRCUMFERENCE, workout_type_to_color

class WordpressOSMShortcodeGenerator:


    def __init__(self, *, xml_path, base_url, uploads_folder, output_dir, relative_remote_paths):
        if not os.path.exists(xml_path):
            raise RuntimeError(f'Path ({xml_path}) to xml files does not exists')
        self.xml_path = xml_path.rstrip('/')
        self.base_url = base_url.rstrip('/')
        self.uploads_folder = uploads_folder.rstrip('/')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        if os.listdir(output_dir):
            response = input(f'Output path ({output_dir}) is not empty, continue? [Y/n]: ')
            if response.lower() == 'n':
                raise RuntimeError('Aborted due to user response')
            elif response.lower() not in ['y', 'n'] and not response == '':
                raise ValueError('Response must be either y or n')
        self.output_dir = output_dir.rstrip('/')
        self.relative_remote_paths = relative_remote_paths

        self.workouts = []

        if os.path.exists(os.path.join(self.output_dir, 'workouts.pkl')):
            response = input('Old procecced workouts file found in output path, restore? [Y/n]: ')
            if response.lower() == 'y' or response == '':
                with open(os.path.join(self.output_dir, 'workouts.pkl'), 'rb') as f:
                    self.workouts = pickle.load(f)

    def process_workouts(self):

        if len(self.workouts) > 0:
            response = input('Reload workouts? [y/N]: ')
            if not response.lower() == 'y':
                return

        self.workouts.clear()

        for path in sorted(os.listdir(self.xml_path)):
            full_path = os.path.join(self.xml_path, path)
            mime = magic.Magic(mime=True).from_file(full_path)
            if not mime == 'text/xml':
                logging.warning(f'{full_path} is not a valid xml file. Skipping ...')
                continue

            logging.info(f'Processing workout {os.path.splitext(path)[0]}')

            with open(full_path, 'r') as f:
                try:
                    workout = gpxpy.parse(f)
                except gpxpy.gpx.GPXException as e:
                    logging.info(f'{full_path}: {str(e)}\n')
                    with open(os.path.join(self.output_dir, 'failed.txt'), 'a+') as f:
                        f.write(f'{full_path}: {str(e)}\n')
                    continue

            self.workouts.append(Workout(workout=workout, path=path))

            logging.info(f'\tType: {self.workouts[-1].workout_type}')

        with open(os.path.join(self.output_dir, 'workouts.pkl'), 'wb') as f:
            pickle.dump(self.workouts, f)

    def create_shortcode(self, map_center='43.7586,6.9242', zoom=2, width='100%', height='450'):
        base_url = '' if self.relative_remote_paths else self.base_url
        file_list = ','.join([base_url + '/wp-content/uploads/' + self.uploads_folder + '/' + workout.path for
                              workout in self.workouts])
        file_list += f',{base_url}/wp-content/uploads/{self.uploads_folder}/marker.xml'
        color_list = ','.join([workout_type_to_color[workout.workout_type] for workout in self.workouts])
        color_list += ',black'

        output = f'''[osm_map_v3 map_center={map_center} zoom={zoom} width={width} height={height} 
file_list="{file_list}" file_color_list="{color_list}"]'''

        with open(os.path.join(self.output_dir, 'shortcode.txt'), 'w') as f:
            f.write(output)

    def create_markers_xml(self, name, description):
        base_url = '' if self.relative_remote_paths else self.base_url
        marker_xml = Marker.create_marker_xml(name=name, description=description, workouts=self.workouts).format(
            uploads_folder=self.uploads_folder, base_url=base_url)

        with open(os.path.join(self.output_dir, 'marker.kml'), 'w') as f:
            f.write(marker_xml)

    def print_total_statistics(self):
        total_length_2d = sum([workout.length_2d for workout in self.workouts]) / 1000.0
        total_length_3d = sum([workout.length_3d for workout in self.workouts]) / 1000.0
        total_duration = sum([workout.duration for workout in self.workouts]) // (60*60)

        total_workouts = {}
        for workout in self.workouts:
            if workout.workout_type in total_workouts:
                total_workouts[workout.workout_type] += 1
            else:
                total_workouts[workout.workout_type] = 1

        print(f'Total distance 2d: {total_length_2d}km, Total distance 3d: {total_length_3d}km, Total duration: {total_duration}h')
        print(', '.join([f'{key}: {value}' for key, value in total_workouts.items()]))
        print(f'Distance traveled along equator: {total_length_2d/EQUATORIAL_CIRCUMFERENCE*100:.2f}%')

@click.command()
@click.option('--xml-path', help='path to xml files')
@click.option('--base-url', help='url of website')
@click.option('--relative-remote-paths/--no-relative-remote-paths', default=False, help='discard base-url in all path specifications')
@click.option('--uploads-folder', default='workouts', help='folder in uploads dir')
@click.option('--output-dir', help='output dir')
def main(**kwargs):

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)

    file_handler = logging.FileHandler(os.path.join(kwargs['output_dir'], 'log.txt'))
    file_handler.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    shortcode_generator = WordpressOSMShortcodeGenerator(**kwargs)
    shortcode_generator.process_workouts()
    shortcode_generator.create_shortcode()
    shortcode_generator.create_markers_xml('test', 'test')
    shortcode_generator.print_total_statistics()

if __name__ == '__main__':
    main()

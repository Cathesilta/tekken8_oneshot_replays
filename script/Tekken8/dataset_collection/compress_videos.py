import os
import sys
import shutil
import subprocess as sb
script_dir = os.path.dirname(__file__)  # Gets the directory of the current script
parent_dir = os.path.dirname(script_dir)  # Gets the parent directory
parent_of_parent_dir = os.path.dirname(parent_dir)  # Gets the parent directory
parent_of_parent_of_parent_dir = os.path.dirname(parent_of_parent_dir)
sys.path.append(parent_of_parent_of_parent_dir)
from src.load_configure import load_configure
from helper_func.string_operations import *

parent_directory = "./videos/doneuploadingTK8^"


configure_yaml_path = './configure/Tekken8.yml'
config_data = load_configure(configure_yaml_path)
config_data.yml_data['Video_Quality']['resolution'] = '480:360'
config_data.yml_data['Video_Quality']['bitrate'] = '1M'
config_data.yml_data['Path']['video_process_dir'] = './videos/doneuploadingTK8^'


for path, directories, _ in os.walk(config_data.yml_data['Path']['video_process_dir']):
    for dir in directories:
        current_sub_path = os.path.join(path, dir)
        
        
        # remove all dir without a .mp4 in it
        remove_current_sub_dir = True
        for f_under_current_sub_dir in os.listdir(current_sub_path):
            specific_file_under_current_sub_dir = os.path.join(current_sub_path,f_under_current_sub_dir)
            if os.path.isfile(specific_file_under_current_sub_dir) and specific_file_under_current_sub_dir.endswith('.mp4'):
                remove_current_sub_dir = False
        if remove_current_sub_dir:
            shutil.rmtree(current_sub_path)
                
        # skip for sub-directories where scoreboard video has been generated
        if os.path.isfile(os.path.join(current_sub_path, config_data.yml_data['Filename']['concat_video_filename'])):
            print(f'You\'ve compressed this video, skip for this match, current path:{current_sub_path}.')
            continue
        print('SF6 one-shot youtuber processing for path:',current_sub_path)
        
        command = [
            'ffmpeg',
            '-i', os.path.join(current_sub_path,config_data.yml_data['Filename']['scoreboarded_video_filename']),
            '-b:v', config_data.yml_data['Video_Quality']['bitrate'],
            '-s', config_data.yml_data['Video_Quality']['resolution'],
            '-c:a', 'copy',
            os.path.join(current_sub_path,config_data.yml_data['Filename']['concat_video_filename'])
            ]
        try:
            sb.run(command, check=True)
            print(f'Video compressed successfully: {os.path.join(current_sub_path,config_data.yml_data['Filename']['concat_video_filename'])}')
        except sb.CalledProcessError as e:
            print(f'Error compressing video: {e}')
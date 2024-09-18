import os
import yaml
import sys
script_dir = os.path.dirname(__file__)  # Gets the directory of the current script
parent_dir = os.path.dirname(script_dir)  # Gets the parent directory
parent_of_parent_dir = os.path.dirname(parent_dir)  # Gets the parent directory
sys.path.append(parent_of_parent_dir)
from configure.hyperparameters import hyperparameters
from src.Tekken8.thumbnailing import thumbnailing
from src.Tekken8.find_keyframes import find_keyframes
from src.Tekken8.trim_and_concat_videos import trim_and_concat_videos
from src.Tekken8.draw_scoreboard import scoreboard
from src.load_configure import load_configure
from helper_func.string_operations import *


configure_yaml_path = './configure/Tekken8.yml'

config_data = load_configure(configure_yaml_path)
    
video_process_dir = config_data.yml_data['Path']['video_process_dir']
character_avatar_dir = config_data.yml_data['Path']['character_avatar_dir']
anchor_image_dir = config_data.yml_data['Path']['anchor_image_dir']
video_recording_dir = config_data.yml_data['Path']['video_recording_dir']
scoreboarded_video_filename = config_data.yml_data['Filename']['scoreboarded_video_filename']
concat_video_filename = config_data.yml_data['Filename']['concat_video_filename']
bitrate = config_data.yml_data['Video_Quality']['bitrate']
resolution = config_data.yml_data['Video_Quality']['resolution']


for path, directories, _ in os.walk(video_process_dir):
    for dir in directories:
        current_sub_path = os.path.join(path, dir)
        
        
        if os.path.isfile(os.path.join(current_sub_path, scoreboarded_video_filename)):
            print(f'You\'ve made this video, skip for this match, current path:{current_sub_path}.')
            continue
        
        print('SF6 one-shot youtuber processing for path:',current_sub_path)
        with open(os.path.join(current_sub_path, 'match_info.yml'), 'r') as file:
            yml_data = yaml.safe_load(file)
        hyperparameters.player_1 = yml_data['Match']['player1']
        hyperparameters.player_2 = yml_data['Match']['player2']
        hyperparameters.scoreboard = yml_data['Match']['scoreboard']
        print(f'match info loaded from yml file, player 1: {hyperparameters.player_1}, player 2:{hyperparameters.player_2},\
            scoreboard:{hyperparameters.scoreboard}')
            
            
            
        thumbnailing(current_sub_path, config_data.yml_data)
  
        fkf = find_keyframes(current_sub_path, config_data.yml_data)
        if os.path.isfile(os.path.join(video_process_dir,concat_video_filename)):
            os.remove(os.path.join(video_process_dir,concat_video_filename))
            print('deleted the existing \'concatenate_video.mp4\', now make a new one.')
            #deleted the existing 'processed_video.mp4',    
        trim_and_concat_videos(fkf, config_data.yml_data)
        scoreboard(fkf, current_sub_path, config_data.yml_data)
import os
import sys
script_dir = os.path.dirname(__file__)  # Gets the directory of the current script
parent_dir = os.path.dirname(script_dir)  # Gets the parent directory
parent_of_parent_dir = os.path.dirname(parent_dir)  # Gets the parent directory
sys.path.append(parent_of_parent_dir)
import yaml
from configure.hyperparameters import hyperparameters
from src.Tekken8.thumbnailing import thumbnailing
from src.load_configure import load_configure





current_path =  './videos/Tekken8/001'

configure_yaml_path = './configure/Tekken8.yml'

config_data = load_configure(configure_yaml_path)

config_data.yml_data['Hyperparameters']['vs_screen_time'] = 9
            
with open(os.path.join(current_path, 'match_info.yml'), 'r') as file:
    yml_data = yaml.safe_load(file)
    hyperparameters.player_1 = yml_data['Match']['player1']
    hyperparameters.player_2 = yml_data['Match']['player2']
    hyperparameters.P1_title = yml_data['Match']['player1_title']
    hyperparameters.P2_title = yml_data['Match']['player2_title']
    hyperparameters.p1_character = yml_data['Match']['player1_character']
    hyperparameters.p2_character = yml_data['Match']['player2_character']
    hyperparameters.scoreboard = yml_data['Match']['scoreboard']
    
    
    print(f'match info loaded from yml file, player 1: {hyperparameters.player_1}, player 2:{hyperparameters.player_2},\
        character 1:{hyperparameters.p1_character}, character 2:{hyperparameters.p2_character},scoreboard:{hyperparameters.scoreboard}')
    
thumbnailing(current_path, config_data.yml_data)
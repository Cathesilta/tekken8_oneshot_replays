import cv2
import numpy as np
import pyautogui
import time
from datetime import datetime
from pynput.keyboard import Key, Controller
import pyautogui
from PIL import ImageGrab
import pytesseract
import yaml
import os
import sys
import shutil
script_dir = os.path.dirname(__file__)  # Gets the directory of the current script
parent_dir = os.path.dirname(script_dir)  # Gets the parent directory
parent_of_parent_dir = os.path.dirname(parent_dir)  # Gets the parent directory
sys.path.append(parent_of_parent_dir)
from helper_func.string_operations import Levenshtein_distance, remove_spaces, format_number_to_3_digit
import subprocess as sb

Total_Matches = 5
configure_yaml_path = './configure/Tekken8.yml'
Ending_box_Region = (545, 473, 830, 130)


Match_Box_1_1_Pos = [(149,266),(149,358)]
Match_Box_1_2_Pos = [(149,403),(149,497)]
Match_Box_1_3_Pos = [(149,541),(149,634)]
Match_Box_1_4_Pos = [(149,679),(149,773)]
Match_Box_1_5_Pos = [(149,817),(149,911)]
Match_Box_2_1_Pos = [(149,314),(149,407)]
Match_Box_2_2_Pos = [(149,452),(149,546)]
Match_Box_2_3_Pos = [(149,590),(149,684)]
Match_Box_2_4_Pos = [(149,728),(149,821)]
Match_Box_2_5_Pos = [(149,866),(149,960)]
Match_Box_Pos_List = [Match_Box_1_1_Pos, Match_Box_1_2_Pos, Match_Box_1_3_Pos, Match_Box_1_4_Pos, Match_Box_1_5_Pos,\
                    Match_Box_2_1_Pos, Match_Box_2_2_Pos, Match_Box_2_3_Pos, Match_Box_2_4_Pos, Match_Box_2_5_Pos]
Match_Box_1_1_Area = (148,265,1250,94)
Match_Box_1_2_Area = (148,403,1250,94)
Match_Box_1_3_Area = (148,541,1250,94)
Match_Box_1_4_Area = (148,680,1250,94)
Match_Box_1_5_Area = (148,818,1250,94)
Match_Box_2_1_Area = (148,314,1250,94)
Match_Box_2_2_Area = (148,452,1250,94)
Match_Box_2_3_Area = (148,590,1250,94)
Match_Box_2_4_Area = (148,728,1250,94)
Match_Box_2_5_Area = (148,866,1250,94)
Match_Box_Area_List = [Match_Box_1_1_Area, Match_Box_1_2_Area, Match_Box_1_3_Area, Match_Box_1_4_Area, Match_Box_1_5_Area,\
                    Match_Box_2_1_Area, Match_Box_2_2_Area, Match_Box_2_3_Area, Match_Box_2_4_Area, Match_Box_2_5_Area]

# detect_match_and_read_info
def scan_matchbox(win_botton_anchor_image,current_processing_video_dir,anchor_ids):
    
    no_of_matchbox, _ = find_highlighted_match_box(Match_Box_Pos_List)
    
    anchor_screenshot_match_box = pyautogui.screenshot(region=Match_Box_Area_List[no_of_matchbox])
    anchor_screenshot_match_box = np.array(anchor_screenshot_match_box)
    anchor_screenshot_match_box_gray = cv2.cvtColor(anchor_screenshot_match_box, cv2.COLOR_BGR2GRAY)

    player_1_id = pytesseract.image_to_string(anchor_screenshot_match_box_gray[9:45,45:210], lang='eng',config ='--psm 7')
    player_2_id = pytesseract.image_to_string(anchor_screenshot_match_box_gray[9:45,1064:1229], lang='eng',config ='--psm 7')

    print('player_1_id:',player_1_id)
    print('player_2_id:',player_2_id)
    player_ids = [player_1_id, player_2_id]
    
    match_score = cv2.matchTemplate(anchor_screenshot_match_box_gray[5:25,680:700], win_botton_anchor_image, cv2.TM_CCOEFF_NORMED)
    match_score_2 = cv2.matchTemplate(anchor_screenshot_match_box_gray[5:25,744:764], win_botton_anchor_image, cv2.TM_CCOEFF_NORMED)
    if match_score > match_score_2:
        winner_side = 1
    else:
        winner_side = 2

    yml_data = {}
    yml_data['Match'] = {}
    yml_data['Match']['player1'] = remove_spaces(player_1_id)
    yml_data['Match']['player2'] = remove_spaces(player_2_id)
    yml_data['Match']['player1_title'] = ''
    yml_data['Match']['player2_title'] = ''
    yml_data['Match']['player1_character'] = ''
    yml_data['Match']['player2_character'] = ''
    yml_data['Match']['scoreboard'] = []
    continuity = ''
    
    yml_data['Episode'] = {}
    # Make episode title - new added - wait for debugging
    yml_data['Episode']['title'] = f'Tekken8 ➤ {remove_spaces(player_1_id)} () vs {remove_spaces(player_2_id)} () ✎ FT2'
    
    if anchor_ids[0]==anchor_ids[1] =='':
        
        yml_data['Match']['scoreboard'] = [winner_side]         #if this is the new match
        
        continuity = 'new match'  
        # print(f'this is {continuity}, scoreboard:{yml_data['Match']['scoreboard']}') 
        with open(os.path.join(current_processing_video_dir,'match_info.yml'), 'w') as file:
            yaml.dump(yml_data, file, default_flow_style=False)
    ######## found a match not new ########
    elif (anchor_ids==player_ids):
        with open(os.path.join(current_processing_video_dir,'match_info.yml'),'r') as file:
            loaded_yml_data = yaml.safe_load(file)
        scoreboard_list = loaded_yml_data['Match']['scoreboard']
        scoreboard_list.append(winner_side)
        yml_data['Match']['scoreboard'] = scoreboard_list
        continuity = 'continuing match'
        # print(f'this is {continuity}, scoreboard:{yml_data['Match']['scoreboard']}') 
        with open(os.path.join(current_processing_video_dir,'match_info.yml'), 'w') as file:
            yaml.dump(yml_data, file, default_flow_style=False)
    ######## found a match not new ########
    elif (Levenshtein_distance(anchor_ids[0].lower(),player_ids[0].lower())>1 or  Levenshtein_distance(anchor_ids[1].lower(),player_ids[1].lower())>1) \
            and ((anchor_ids[0] != 0) or (anchor_ids[1] != 0)):
        
        continuity = 'another match'
    
    

    
    
    return continuity, player_ids


def is_red_pixel(pixel):
    # Assuming pixel is in the format (B, G, R)
    red_ratio = pixel[0] / (pixel[0] + pixel[1] + pixel[2] + 1e-6)  # Adding a small value to avoid division by zero

    # print('current blue_ratio is:',blue_ratio)
    # You can adjust the threshold based on your needs
    red_threshold = 0.5  # Example threshold, adjust as needed

    return red_ratio > red_threshold

def find_highlighted_match_box(match_box_pos_list):
    for h,i in enumerate(match_box_pos_list):
        rgb = get_rgb_at_position(i[0][0],i[0][1])
        # print('current rgb:',rgb)
        if is_red_pixel(rgb):
            rgb = get_rgb_at_position(i[1][0],i[1][1])
            # print('current rgb:',rgb)
            if is_red_pixel(rgb):
                print(f'the {h}th box is what you want')
                return h, i
    print('unable to find the selected match box, check something went wrong')
    return None,None

def get_rgb_at_position(x, y):
    # Capture the screen
    screenshot = ImageGrab.grab()

    # Get the RGB value at the specified position
    rgb_value = screenshot.getpixel((x, y))

    return rgb_value


def move_videos_to_process_path(source_directory,destination_directory):
    if not os.path.exists(source_directory) or not os.path.exists(destination_directory):
        print("Source or destination directory does not exist.")
        return
    else:
        for filename in os.listdir(source_directory):
            if filename.endswith('.mp4'):
                # Construct the full paths for source and destination
                source_path = os.path.join(source_directory, filename)
                destination_path = os.path.join(destination_directory, filename)

                # Move the file to the destination directory
                shutil.move(source_path, destination_path)

                print(f"Moved: {filename} from {source_directory} to {destination_directory}")

def record_a_Tekken8_match(ending_box_image, keyboard):
    
    
    time.sleep(1)
    # Start Recording
    start_or_end_nvidia_recording(keyboard)
    
    for i in range(0,3):
        keyboard.press('j')
        time.sleep(0.03)
        keyboard.release('j')
        time.sleep(0.7)
    
    


    # time.sleep(55)
    while True:
        
        time.sleep(6)
        screenshot_for_ending_box = pyautogui.screenshot(region=Ending_box_Region)
        screenshot_for_ending_box = np.array(screenshot_for_ending_box)
        screenshot_for_ending_box = cv2.cvtColor(screenshot_for_ending_box, cv2.COLOR_BGR2GRAY)
        
        match_score = cv2.matchTemplate(screenshot_for_ending_box, ending_box_image, cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.7
        print(f'debug - current ending box matchscore {match_score}')
        if match_score>threshold:
            print(f'found the ending box, matchscore is {match_score}')
            # End Recording
            start_or_end_nvidia_recording(keyboard)
            keyboard.press('s')
            time.sleep(0.03)
            keyboard.release('s')
            time.sleep(0.35)
            keyboard.press('j')
            time.sleep(0.03)
            keyboard.release('j')
            time.sleep(1.5)
            keyboard.press('w')
            time.sleep(0.03)
            keyboard.release('w')
            time.sleep(0.35)
            keyboard.press('j')
            time.sleep(0.03)
            keyboard.release('j')
            time.sleep(0.2)

            return
    
    
    
    

def start_or_end_nvidia_recording(keyboard):
    keyboard.press(Key.alt)
    # Press F9 key
    keyboard.press(Key.f9)
    time.sleep(0.02)
    keyboard.release(Key.alt)
    # Press F9 key
    keyboard.release(Key.f9)
    time.sleep(0.02)





if __name__ == "__main__":
    print(f'start {__file__}')
    time.sleep(2)
    
    
    # Load parameters from yaml
    with open(os.path.join(configure_yaml_path), 'r') as file:
        yml_data = yaml.safe_load(file)
        
    video_process_dir = yml_data['Path']['video_process_dir']
    character_avatar_dir = yml_data['Path']['character_avatar_dir']
    anchor_image_dir = yml_data['Path']['anchor_image_dir']
    video_recording_dir = yml_data['Path']['video_recording_dir']
    
    
    
    win_botton_anchor_image = cv2.imread(os.path.join(anchor_image_dir,'tekken_win_botton.png'), 0)
    ending_box_image = cv2.imread(os.path.join(anchor_image_dir,'ending_box.png'), 0)
    
    
    
    # Any Preparation
    keyboard = Controller()
    
    maximum_directory_num = 0
    for p,d,_ in os.walk(video_process_dir):
        int_list_of_d = [int(item) for item in d]
        try:
            maximum_directory_num = max(int_list_of_d)
        except:
            maximum_directory_num = 0
        break
    maximum_directory_num += 1
    time.sleep(2)
    Match_number = 0
    Match_count = 1
    
    while (True):
        print('maximum_directory_num:',maximum_directory_num)
        current_video_dir = os.path.join(video_process_dir, format_number_to_3_digit(maximum_directory_num))
        print('creating directory:',current_video_dir)
        os.makedirs(current_video_dir, exist_ok=True)
        anchor_ids = ['','']
        player_ids = ['','']
        
        while (True):
            time.sleep(2)
            keyboard.press('c')
            time.sleep(0.03)
            keyboard.release('c')
            time.sleep(0.2)
            continuity,player_ids = scan_matchbox(win_botton_anchor_image,current_video_dir,anchor_ids)              # haha can be 'new match', 'continuing match', 'another match'
            if continuity == 'new match':
                print('this is a new match')
                anchor_ids = player_ids
                record_a_Tekken8_match(ending_box_image, keyboard)
                time.sleep(8)
                keyboard.press('s')
                time.sleep(0.03)
                keyboard.release('s')
                time.sleep(0.2)
            elif continuity == 'continuing match':
                print('Match continue between the players')
                is_new_match = False
                record_a_Tekken8_match(ending_box_image, keyboard)
                time.sleep(8)
                keyboard.press('s')
                time.sleep(0.03)
                keyboard.release('s')
                time.sleep(0.2)
            elif continuity == 'another match' :
                print('this is another match, moving videos to process dir...')
                # finish the last match and move .mp4 videos to processing dir
                move_videos_to_process_path(video_recording_dir,current_video_dir)
                time.sleep(2)
                keyboard.press('c')
                time.sleep(0.03)
                keyboard.release('c')
                time.sleep(0.2)
                break
            
            

            
        
    
        if Match_count >= Total_Matches:
            break
        Match_count +=1
        maximum_directory_num += 1

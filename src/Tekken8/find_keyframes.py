# Now, there is no other game extension, only SF6 available

##experiment:
####when you matchscore the gray image of the total black image, the threshold of matchscore should be set 0.1
####if not gray image, 0.7 is enough
####if you're gonna find "Round1" matchtemplate, threshold should be 0.72
 

import cv2
import os
import time
from configure.hyperparameters import hyperparameters
from helper_func.string_operations import *
# import pytesseract
import numpy as np

class find_keyframes():
    
    def __init__(self, video_dir, config_yml_data):
        
        self.config_yml_data = config_yml_data
        
        self.video_file_paths = self.read_video_files(video_dir)
        self.Ref_Img_01 = cv2.imread(self.config_yml_data['Anchors']['round1_path'], 0)
        self.Ref_Img_02 = cv2.imread(self.config_yml_data['Anchors']['ending_box_path'], 0)
        
        self.start_time, self.start_frame, self.end_time, self.end_frame, self.win_time, self.win_frame, self.winner_side = [],[],[],[],[],[],[]
        for no, current_video_path in enumerate(self.video_file_paths):
            s_t, s_f = self.find_trim_start(current_video_path,threshold=self.config_yml_data['Hyperparameters']['threshold_1'])
            e_t, e_f, ebd_t, edd_f = self.find_trim_end(current_video_path,threshold=self.config_yml_data['Hyperparameters']['threshold_2'])
            #for the first match, let play cutscene
            if 0==no:
                s_t = s_t + self.config_yml_data['Trim']['cutscene_play_before_round_1']
                s_f = s_f + self.config_yml_data['Trim']['cutscene_play_before_round_1']*58
                
            # for the last match, let play the end cutscene
            if len(self.video_file_paths)-1 == no:
                e_t = ebd_t  -1.5                   #in most of the case, ebd_t(ending box disappearing) time is the time the edb haven't disappeared completely, hence we set an offset to wait for disappearing 
                e_f = edd_f  -1.5 * 58              
                
            self.start_time.append(s_t)
            self.start_frame.append(s_f)
            self.end_time.append(e_t)
            self.end_frame.append(e_f)
            self.win_time.append(ebd_t)       # in Tekken8, win_time is actually the time ending box disappear(in reverse order)
            self.win_frame.append(edd_f)
            
            

            self.winner_side = hyperparameters.scoreboard

        self.num_of_videos = len(self.start_frame)
        
        
        try:
            self.num_of_videos > 0
        except AssertionError as e:
            print('video number 0, check either video path or self.start_frame variable; AssertionError:',e)
            raise
        
    def read_video_files(self, video_dir):
        video_file_paths = []
        for filename in os.listdir(video_dir):
            file_path = os.path.join(video_dir, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.mp4')):
                video_file_paths.append(file_path)
        return video_file_paths
        
        
            
    def find_trim_start(self, video_path, threshold=0.3):
    
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error opening video file, check the video path or process yourself")
            return None,None
        fps = cap.get(cv2.CAP_PROP_FPS)     #check if 60fps
        print('the video fps is:',fps)
        
        # Set the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.config_yml_data['Trim']['start_searching_time'] * fps)
        
        print(f'{self.find_trim_start.__name__}: scanning the frames...')
        for frame_no in range(int(self.config_yml_data['Trim']['start_searching_time']*fps), 
                              int(self.config_yml_data['Trim']['start_searching_until_time']*fps) ,
                              int(self.config_yml_data['Trim']['searching_time_interval']*fps)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            if not ret:
                print(f'{self.find_trim_end.__name__}:some errors occur when reading the frame')
                break          
            # crop the image, Hard code
            frame = frame[430:649,706:1311]
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            

            match_score = cv2.matchTemplate(gray_frame, self.Ref_Img_01, cv2.TM_CCOEFF_NORMED)
            

            # print(f'{self.find_trim_start.__name__}: at frame {frame_no}, {frame_no/fps} sec, the match_score is: {match_score}')
            if match_score > threshold:
                # Frame found that matches the reference
                # Round 1 will start after 5 sec from the black screen 
                start_trim_time = frame_no/fps + self.config_yml_data['Trim']['start_before_round_1'] #sec
                start_trim_frame = int(frame_no + self.config_yml_data['Trim']['start_before_round_1']*fps) #frame
                
                
                print(f'{self.find_trim_start.__name__}: matchscore {match_score} past the threshold {threshold}')
                print(f"{self.find_trim_start.__name__}: The start end time at {start_trim_time} seconds, {start_trim_frame} fps")
                cap.release()
                return start_trim_time, start_trim_frame
            
        print(f'{self.find_trim_start.__name__}: no match pattern within {self.config_yml_data['Trim']['start_searching_until_time']}sec, you may need to process this video MANUALLY')
        cap.release()
        return None,None
    
    def find_trim_end(self, video_path, threshold=0.88):  
        # in time-reverse order, check WIN text
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error opening video file")
            return None,None,None,None
        fps = cap.get(cv2.CAP_PROP_FPS)     #check if 60fps
        print('the video fps is:',fps)
        
        #calculate the total frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print('total_frames are {}'.format(total_frames))
        
        
        
        found_ending_box = False
        print(f'{self.find_trim_end.__name__}: scanning the frames...')
        # Check frame from -181 frame to -600 frame
        for frame_no in range(int(total_frames - self.config_yml_data['Trim']['start_reverse_searching_time']), 
                              int(total_frames - self.config_yml_data['Trim']['reverse_searching_until_time']*fps), 
                              -int(self.config_yml_data['Trim']['searching_time_interval']*fps)):  # it's 180 frame between wins and box 
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            if not ret:
                print(f'{self.find_trim_end.__name__}: some errors occur when reading the frame')
                break
            
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cropped_frame = gray_frame[473:603,545:1375]
            

            # st = int(round(time.time()*1000))
            match_score = cv2.matchTemplate(cropped_frame, self.Ref_Img_02, cv2.TM_CCOEFF_NORMED)
            # et = int(round(time.time()*1000))
            # print(f'proceesed {et-st} ms')
            
            # print(f'{self.find_trim_end.__name__}: at frame {frame_no}, {frame_no/fps} sec, the match_score is: {match_score}')
            if match_score > threshold:
                found_ending_box = True
            if (match_score < threshold) and found_ending_box:
                end_trim_time = (frame_no + self.config_yml_data['Trim']['trim_end_offset']*fps) / fps
                end_trim_frame = int(frame_no + self.config_yml_data['Trim']['trim_end_offset']*fps)
                ending_box_disappear_time = frame_no/fps
                ending_box_disappear_frame = frame_no
                

                
                print(f'{self.find_trim_end.__name__}: matchscore {match_score} is the first time when lower than the threshold {threshold}, which passes the judgement')
                print(f"{self.find_trim_end.__name__}: The trim end time at {end_trim_time} seconds, {end_trim_frame} fps")
                cap.release()
                return end_trim_time, end_trim_frame, ending_box_disappear_time, ending_box_disappear_frame
            
        cap.release()
        print(f'{self.find_trim_end.__name__}: no match pattern within {self.config_yml_data['Trim']['reverse_searching_until_time']}sec, you may need to process this video MANUALLY')
        return None,None,None,None
    
    def compare_who_wins(self, winner_text, p1_text,p2_text):
        dis_1 = Levenshtein_distance(p1_text,winner_text)
        dis_2 = Levenshtein_distance(p2_text,winner_text)
        print('player1_text:',p1_text,';player2_text:',p2_text,';winner_text:',winner_text)
        print('dist_1:',dis_1,'dis_2:',dis_2)
        if dis_1 > dis_2:
            return 2
        elif dis_1 < dis_2:
            return 1 
        elif dis_1 == dis_2:
            print('I can\' distinguish who wins from the same character! Do it mannually.')
            return None
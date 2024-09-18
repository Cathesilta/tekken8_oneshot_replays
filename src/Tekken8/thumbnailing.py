# I have left extensions for other games, but haven't implemented yet

import cv2
import os
import yaml
from PIL import Image, ImageDraw, ImageFont
import pygame
from configure.hyperparameters import hyperparameters
from helper_func.file_reader import read_video_files
from helper_func.image_process import apply_gradient_shadow_top, apply_symmetric_gradient_banners_Tekken8
from helper_func.text_rendering import create_gold_gradient, getsize

class thumbnailing():
    
    def __init__(self, video_path, config_yml_data):

        self.video_path = video_path
        self.vs_screen_time = config_yml_data['Hyperparameters']['vs_screen_time']
        self.thumbnail_temp_path = os.path.join(config_yml_data['Path']['video_process_dir'],'thumbnail_temp.png')
        self.thumbnail_output_path = os.path.join(self.video_path, 'thumbnail.jpg')
        self.font_size = config_yml_data['Hyperparameters']['font_size']
        self.PN_y = config_yml_data['Hyperparameters']['PN_y']
        self.font_path = config_yml_data['Path']['font_path']
        self.config_yml_data = config_yml_data
        self.__thumbnailing__()
        
        

        
        
    # this function is a business function
    def __thumbnailing__(self):
        try:
            self.video = read_video_files(self.video_path)[0]        # Hard code use the first video
        except:
            print("Unable to load the second video for thumbnail capturing")
            

        thumbnail_base_image = self.capture_the_vs_screen(self.video, self.vs_screen_time)
        
        cv2.imwrite(self.thumbnail_temp_path, thumbnail_base_image,[cv2.IMWRITE_PNG_COMPRESSION, 0])
        # now we want pillow image, so we have to load it by pillow from what cv2 has saved
        thumbnail_base_image = Image.open(self.thumbnail_temp_path)
        thumbnail_base_image = self.apply_gradient_shadow(thumbnail_base_image)
        
        ## Draw Player id text
        thumbnail_image_with_playerid = self.add_player_name(thumbnail_base_image)
        
        ## Draw title
        thumbnail_image_with_title = self.draw_title(thumbnail_image_with_playerid)
        
        ## Draw Character
        thumbnail_image = self.draw_character(thumbnail_image_with_title)
        thumbnail_image.save(self.thumbnail_output_path,'JPEG')
        
        
        ## Apply Legend or Master img
    
    def capture_the_vs_screen(self, video, time):
        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            print("Error opening video file, check the video path or process yourself")
            return
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.set(cv2.CAP_PROP_POS_FRAMES, time * fps)
        ret, frame = cap.read()
        if not ret:
            print('some errors occur when reading the frame')
            return
        
        return frame
        # self.thumbnail_base = frame[0:882, :]  # cut the bottom information part

        
    def apply_gradient_shadow(self, image):
        
        image = apply_symmetric_gradient_banners_Tekken8(image)
        
        return image
        
        
    def add_player_name(self, image):
        
        
        
        d = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, self.font_size)
        try:
            P1_text_width, _ = font.getsize(hyperparameters.player_1)                               # the text height no needed
            P2_text_width, _ = font.getsize(hyperparameters.player_2)                               # we need the width to calculate the center alignment position
        except:
            P1_text_width, _ = getsize(font, hyperparameters.player_1)
            P2_text_width, _ = getsize(font, hyperparameters.player_2)
        image_width, _ = image.size
        
        center_alignment_cofficient = 0.5           #hard code, less than 0.5 means more scattered
        PN_x = (center_alignment_cofficient*image_width-P1_text_width)/2
        P2N_x =  (center_alignment_cofficient*image_width-P2_text_width)/2 + (1-center_alignment_cofficient)*(image_width)
        
        # draw player 1 id text
        d.text((PN_x + self.config_yml_data['Font']['player_1_text_shadow_offset'][0], 
                self.PN_y + self.config_yml_data['Font']['player_1_text_shadow_offset'][1]), hyperparameters.player_1, font=font, fill=tuple(self.config_yml_data['Font']['player_1_text_shadow_color']))
        d.text((PN_x, self.PN_y),  hyperparameters.player_1, font=font, fill=tuple(self.config_yml_data['Font']['player_text_color']))
        
        # draw player 2 id text
        d.text((P2N_x + self.config_yml_data['Font']['player_2_text_shadow_offset'][0], 
                self.PN_y + self.config_yml_data['Font']['player_2_text_shadow_offset'][1]), hyperparameters.player_2, font=font, fill=tuple(self.config_yml_data['Font']['player_2_text_shadow_color']))
        d.text((P2N_x, self.PN_y), hyperparameters.player_2, font=font, fill=tuple(self.config_yml_data['Font']['player_text_color']))
        
        return image
    
    def draw_title(self,image):
        
        # currently no title for tekken8
        
        return image
    
    def draw_character(self, image):

        return image
        
        
        
        
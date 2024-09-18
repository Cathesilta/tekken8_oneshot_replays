# Now, there is no other game extension, only SF6 available


import os
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, ImageClip
# import sys
# sys.append('../')
# from src import hyperparameters
from configure.hyperparameters import hyperparameters


class scoreboard():
    
    def __init__(self, find_keyframes_obj, match_path, config_yml_data):
        
        self.config_yml_data = config_yml_data
        
        video = VideoFileClip(os.path.join(config_yml_data['Path']['video_process_dir'],config_yml_data['Filename']['concat_video_filename']))
        self.scoreboarded_video_output_path = os.path.join(match_path,config_yml_data['Filename']['scoreboarded_video_filename'])
        self.composite_list = [video]
        
        self.player1_win_count = 0
        self.player2_win_count = 0
        
        self.winner_side = hyperparameters.scoreboard
        self.start_time = find_keyframes_obj.start_time
        self.end_time = find_keyframes_obj.end_time
        self.win_time = find_keyframes_obj.win_time
        self.num_of_match = find_keyframes_obj.num_of_videos
        
        self.concat_video_time = video.duration # you should get the concat video time from a video reading function
        
        self.draw_text_on_video()
        
    def draw_text_on_video(self):
        
        self.draw_scoreboard()
        
        self.draw_subscription_invitation()
        
        self.composite_scoreboard()
        
    def draw_scoreboard(self):
        
        print('calculating information for the scoreboard ...')
        print('self.start_time[0]:',self.start_time[0])
        
        self.draw_scoreboard_for_one_match(-self.config_yml_data['Trim']['cutscene_play_before_round_1']+2,
                                           self.end_time[0]-self.start_time[0])

        
        accumulated_video_time = self.end_time[0]-self.start_time[0]
        print('winner_side_list:',self.winner_side)
        for match_no in range(1,self.num_of_match):
            print('the {} match'.format(match_no+2))
            if 1 == int(self.winner_side[match_no-1]):
                self.player1_win_count += 1
            elif 2 == int(self.winner_side[match_no-1]):
                self.player2_win_count += 1
            # print('current player 1 wins: {}; player 2 wins {}'.format(self.player1_win_count,self.player2_win_count))
            ######## calculate the time point
            duration_for_this_match = self.end_time[match_no] - self.start_time[match_no]
            if match_no < self.num_of_match -1:
                print('accumulated_video_time:',accumulated_video_time)
                end_time_for_this_match = accumulated_video_time + duration_for_this_match
                
                self.draw_scoreboard_for_one_match(accumulated_video_time, end_time_for_this_match)
                accumulated_video_time = end_time_for_this_match
            
            elif match_no == self.num_of_match -1:
                # last match, there will be a change at the end of the match after K.O |-------------1:1----------------|--1:2--|
                
                first_chunk_start_time = accumulated_video_time
                first_chunk_end_time = accumulated_video_time+self.win_time[match_no]-self.start_time[match_no] - 8
                # draw for the beginning period of time
                self.draw_scoreboard_for_one_match(first_chunk_start_time,first_chunk_end_time)
                
                # check in the last match who won
                if 1 == int(self.winner_side[-1]):
                    self.player1_win_count += 1
                elif 2 == int(self.winner_side[-1]):
                    self.player2_win_count += 1
                
                second_chunk_start_time = first_chunk_end_time
                second_chunk_end_time = second_chunk_start_time+2    #very short, should fade before the end victory cutscene
                
                # set a time for subscription start timming
                self.subscription_text_start_time = second_chunk_end_time + 0.3
                
                # draw for the last small period of time
                self.draw_scoreboard_for_one_match(second_chunk_start_time,second_chunk_end_time)
                
        # only one match for this match
        if 1 == self.num_of_match:
            self.subscription_text_start_time = self.end_time[0] - 3
            
        
        
    def draw_scoreboard_for_one_match(self, start_time, end_time):
        font_color = self.config_yml_data['Scoreboard']['font_color']
        fontsize = self.config_yml_data['Scoreboard']['fontsize']
        scoreboard_color = self.config_yml_data['Scoreboard']['scoreboard_color']
        stroke_line_color = self.config_yml_data['Scoreboard']['stroke_line_color']
        sb_p1_pos = self.config_yml_data['Scoreboard']['sb_p1_pos']
        sb_p2_pos = self.config_yml_data['Scoreboard']['sb_p2_pos']
        sb_p1_size = self.config_yml_data['Scoreboard']['sb_p1_size']
        sb_p2_size = self.config_yml_data['Scoreboard']['sb_p2_size']
        stroke_p1_pos = [self.config_yml_data['Scoreboard']['sb_p1_pos'][0] - self.config_yml_data['Scoreboard']['stroke_offset'],
                         self.config_yml_data['Scoreboard']['sb_p1_pos'][1] - self.config_yml_data['Scoreboard']['stroke_offset']]
        stroke_p1_size = [self.config_yml_data['Scoreboard']['sb_p1_size'][0] + 2*self.config_yml_data['Scoreboard']['stroke_offset'], 
                          self.config_yml_data['Scoreboard']['sb_p1_size'][1] + 2*self.config_yml_data['Scoreboard']['stroke_offset']]
        stroke_p2_pos = [self.config_yml_data['Scoreboard']['sb_p2_pos'][0] - self.config_yml_data['Scoreboard']['stroke_offset'],
                         self.config_yml_data['Scoreboard']['sb_p2_pos'][1] - self.config_yml_data['Scoreboard']['stroke_offset']]
        stroke_p2_size = [self.config_yml_data['Scoreboard']['sb_p2_size'][0] + 2*self.config_yml_data['Scoreboard']['stroke_offset'], 
                          self.config_yml_data['Scoreboard']['sb_p2_size'][1] + 2*self.config_yml_data['Scoreboard']['stroke_offset']]  
        
        
        # Here, a lot of hyperparameters to be changed 
        duration = end_time - start_time
        
        print(f'draw_scoreboard for this match, p1score:{self.player1_win_count}, p2score:{self.player2_win_count};start_time:{start_time},end_time:{end_time},duration:{duration}')
        
        # define stroke line size
        bordered_txt_clip = TextClip(" ", fontsize=24, color='white', bg_color=stroke_line_color, size=stroke_p1_size)
        
        # player 1
        bordered_txt_clip = bordered_txt_clip.set_pos(stroke_p1_pos).set_duration(duration) #attach stroke line at specific position

        txt_clip = TextClip(f"{str(self.player1_win_count)}", fontsize=fontsize, color=font_color, 
                            bg_color=scoreboard_color,size=sb_p1_size)
        txt_clip = txt_clip.set_pos(sb_p1_pos).set_duration(duration)
        
        
        # player 2
        bordered_txt_clip_2 = bordered_txt_clip.set_pos(stroke_p2_pos).set_duration(duration)

        txt_clip_2 = TextClip(f"{str(self.player2_win_count)}", fontsize=fontsize, color=font_color, 
                            bg_color=scoreboard_color,size=sb_p2_size)
        txt_clip_2 = txt_clip_2.set_pos(sb_p2_pos).set_duration(duration)
        
        self.composite_list.extend([bordered_txt_clip.set_start(start_time),txt_clip.set_start(start_time),
                                    bordered_txt_clip_2.set_start(start_time), txt_clip_2.set_start(start_time)])

    def draw_subscription_invitation(self):
        
        subscribe_invitation_text_line_1 = "Like and subscribe"         # hard code
        subscribe_invitation_text_line_2 = "Get more TK8 Content !"        # hard code
        
        text_pos_1 = [400,250]                                          # hard code
        text_pos_2 = [400,390]                                          # hard code
        
        font_zise = 170                                                 # hard code
        shadow_offset = 5                                               # hard code

        shadow = TextClip(subscribe_invitation_text_line_1, fontsize=font_zise, color='#5E12A2', font=self.config_yml_data['Path']['font_path'])
        shadow = shadow.set_pos((text_pos_1[0],text_pos_1[1]))
        text = TextClip(subscribe_invitation_text_line_1, fontsize=font_zise, color='white', font=self.config_yml_data['Path']['font_path'])
        text = text.set_position(lambda t: (text_pos_1[0]+shadow_offset, text_pos_1[1]+shadow_offset))
        
        shadow_2 = TextClip(subscribe_invitation_text_line_2, fontsize=font_zise, color='#CE4BD5', font=self.config_yml_data['Path']['font_path'])
        shadow_2 = shadow_2.set_pos((text_pos_2[0],text_pos_2[1]))
        text_2 = TextClip(subscribe_invitation_text_line_2, fontsize=font_zise, color='white', font=self.config_yml_data['Path']['font_path'])
        text_2 = text_2.set_position(lambda t: (text_pos_2[0]+shadow_offset, text_pos_2[1]+shadow_offset))
        
        

        
        
        
        
        self.composite_list.extend([shadow.set_start(self.subscription_text_start_time),text.set_start(self.subscription_text_start_time),
                                    shadow_2.set_start(self.subscription_text_start_time),text_2.set_start(self.subscription_text_start_time)])  # hard code
        
    def composite_scoreboard(self):
        print('drawing the scoreboard ...')
        composite = CompositeVideoClip(self.composite_list).subclip(0, self.concat_video_time)
        
        composite.write_videofile(self.scoreboarded_video_output_path,
                                  codec='h264_nvenc',
                                  bitrate=self.config_yml_data['Video_Quality']['bitrate'])
        
        
    
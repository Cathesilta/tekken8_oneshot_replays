# Now, there is no other game extension, only SF6 available

import subprocess
import os
from src.Tekken8.find_keyframes import find_keyframes
from configure.hyperparameters import hyperparameters
from helper_func.time_management import convert_seconds_to_hms





class trim_and_concat_videos():
    
    def __init__(self, find_keyframes_obj, config_yml_data):
        self.video_path_list = find_keyframes_obj.video_file_paths
        self.start_time_list = []
        self.end_time_list = []
        self.concatenated_video_path = os.path.join(config_yml_data['Path']['video_process_dir'],config_yml_data['Filename']['concat_video_filename'])
        self.bitrate = config_yml_data['Video_Quality']['bitrate']
        self.resolution = config_yml_data['Video_Quality']['resolution']
        print('start_time:',find_keyframes_obj.start_time)
        print('end_time:',find_keyframes_obj.start_time)
        for i in find_keyframes_obj.start_time:
            self.start_time_list.append(convert_seconds_to_hms(i))
        for i in find_keyframes_obj.end_time:
            self.end_time_list.append(convert_seconds_to_hms(i))
            
        self.concat_videos()
        
        
    def process_video(self, video, start_time, end_time):
        # FFmpeg command to trim the video using GPU and output to a pipe
        command = [
            'ffmpeg','-hwaccel','cuda', '-ss', start_time, '-to', end_time, '-i', video,
            '-c:v', 'h264_nvenc', '-b:v',self.bitrate, '-vf',f'scale={self.resolution}', '-f', 'mpegts', 'pipe:1'
        ]
        return subprocess.Popen(command, stdout=subprocess.PIPE)

    def concat_videos(self):
        # Start FFmpeg processes for each video to trim and output to pipes
        processes = [self.process_video(video, start_time, end_time) for video,start_time,end_time, in zip(self.video_path_list,self.start_time_list,self.end_time_list)]

        # Start another FFmpeg process to concatenate the videos from the pipes
        concat_command = ['ffmpeg', '-f', 'mpegts','-i', 'pipe:0', 
                        '-c:v','copy',
                        self.concatenated_video_path]
        with subprocess.Popen(concat_command, stdin=subprocess.PIPE) as ffmpeg_concat:
            for proc in processes:
                while True:
                    data = proc.stdout.read(1024)
                    if not data:
                        break
                    ffmpeg_concat.stdin.write(data)
                proc.stdout.close()
            ffmpeg_concat.stdin.close()
            ffmpeg_concat.wait()

        # Close all the trimming processes
        for proc in processes:
            proc.wait()
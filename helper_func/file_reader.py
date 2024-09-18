import os



def read_video_files(video_dir):
    video_file_paths = []
    for filename in os.listdir(video_dir):
        file_path = os.path.join(video_dir, filename)
        # currently, only read Street fighter or Desktop or Polaris, if you want to add other file, add a 'startswith' letters
        if os.path.isfile(file_path) and filename.lower().endswith(('.mp4')) and (filename.lower().startswith(('s')) or filename.lower().startswith(('d')) or
                                                                                  filename.lower().startswith(('p')) or filename.lower().startswith(('t'))):
            video_file_paths.append(file_path)
    return video_file_paths
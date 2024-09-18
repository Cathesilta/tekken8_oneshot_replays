import os
import sys
script_dir = os.path.dirname(__file__)  # Gets the directory of the current script
parent_dir = os.path.dirname(script_dir)  # Gets the parent directory
parent_of_parent_dir = os.path.dirname(parent_dir)  # Gets the parent directory
sys.path.append(parent_of_parent_dir)

parent_directory = "./videos/doneuploadingTK8^"

seriously = input('you will be deleting scoreborded_video.mp4, seriuosly? input \'y\' to make sure')

if seriously != 'y':
    exit(0)

## Remove original videos
for p,d,f in os.walk(parent_directory):
    
    for sub_d in d:
        for pp,_,ff in os.walk(os.path.join(p,sub_d)):
            for current_f in ff:
                # if current_f[:16] == 'Street Fighter 6' and current_f.endswith('.mp4'):
                if current_f == 'scoreboarded_video.mp4':
                    os.remove(os.path.join(pp,current_f))
            break
    break
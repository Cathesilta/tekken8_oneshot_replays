import os
import subprocess as sb


parent_directory = "./videos/doneuploadingTK8^"

folders = os.listdir(parent_directory)
max_number = 63
for fol in folders:
    if fol[:5] == 'data_':
        number = int(fol[5:]) 
        if number > max_number: max_number = number
max_number+=1

# print(max_number)

for fol in folders:
    if fol[:5] != 'data_':
        
        old_directory_path = os.path.join(parent_directory, fol)
        new_directory_name = f"data_{max_number:08d}"
        new_directory_path = os.path.join(parent_directory, new_directory_name)
        
        os.rename(old_directory_path, new_directory_path)
        max_number+=1

import os
import shutil

def move_and_delete_files(base_folder, sub_folder_list, song_folder_list):
    for sub_folder in sub_folder_list:
        for song_folder in song_folder_list:
            file_name = file_name_now
            
            if not file_name.lower().endswith('.wav'):
                print(f"Skipped: {file_name} is not a .wav file.")
                continue
            # Construct the full path to the source file
            source_file_path = os.path.join(base_folder, sub_folder, song_folder, file_name)
            
            # Print the source file path for debugging
            print(f"Attempting to access: {source_file_path}")
            
            # Construct the full path to the destination folder
            dest_folder_path = os.path.join(base_folder)
            
            # Construct the full path to the destination file (with song name)
            dest_file_path = os.path.join(base_folder, f"{sub_folder}_{song_folder}_{file_name}")

            # Check if the source file exists
            if os.path.exists(source_file_path):
                # Copy and rename the file to the destination folder
                shutil.copy(source_file_path, dest_file_path)
                print('###############################')
                # Remove the original folder with vocals inside of it
                #shutil.rmtree(os.path.join(base_folder, sub_folder, song_folder))
            else:
                print(f"Source file for {song_folder} in {sub_folder} does not exist.")


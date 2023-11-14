#exec(open(f"/Users/yerik/_apple_source/PY/GLOBAL/_1_paths.py",encoding="utf-8").read()) #paths

import pandas as pd
import os

def parse_m3u8_folder(folder_path):
    """
    Parse all m3u8 files in a folder and retrieve track_id_rk, Name, Path, 
    playlist_name, and source directory name.
    
    Args:
    - folder_path (str): Path to the folder containing m3u8 files.
    
    Returns:
    - DataFrame: A DataFrame containing columns 'track_id_rk', 'Name', 'Path', 
                 'playlist_name', and 'source_dir'.
    """
    all_entries = []
    source_dir = os.path.basename(folder_path)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.m3u8'):
            playlist_name = os.path.splitext(filename)[0]  # Get filename without extension
            full_path = os.path.join(folder_path, filename)
            
            with open(full_path, 'r') as file:
                lines = file.readlines()

            track_id_rk = None
            name = None
            path = None
            
            for line in lines:
                line = line.strip()  # Remove whitespace
                if line.startswith("#EXTINF:"):
                    # Extract track_id_rk and Name
                    track_info = line.split(",", 1)
                    track_id_rk = track_info[0].split(":")[1]
                    name = track_info[1] if len(track_info) > 1 else None
                elif line and not line.startswith("#"):
                    path = line
                    if track_id_rk and name:
                        entry = {
                            'track_id_rk': track_id_rk, #this is just SECONDS
                            'Name': name, 
                            'Path': path, 
                            'playlist_name': playlist_name,
                            'source_dir': source_dir
                        }
                        all_entries.append(entry)
                        track_id_rk = None
                        name = None
                        path = None
    
    df = pd.DataFrame(all_entries)
    return df

# Assuming path_ms_all_data is already defined
directory_path = f'{path_ms_all_data}/m3u8_playlists/TIMELESS_dj_TOOLS_purge'
df_TM_pr = parse_m3u8_folder(directory_path)
df_TM_pr.head()

# Assuming path_ms_all_data is already defined
directory_path = f'{path_ms_all_data}/m3u8_playlists/years_23_purge'
df_23 = parse_m3u8_folder(directory_path)
df_23.head()

# Assuming path_ms_all_data is already defined
directory_path = f'{path_ms_all_data}/m3u8_playlists/years_23_purge/combos'
df_23_comb = parse_m3u8_folder(directory_path)
df_23_comb.head()

# Assuming path_ms_all_data is already defined
directory_path = f'{path_ms_all_data}/m3u8_playlists/years_22_purge'
df_22 = parse_m3u8_folder(directory_path)
df_22.head()

# Assuming path_ms_all_data is already defined
directory_path = f'{path_ms_all_data}/m3u8_playlists/years_22_purge'
df_22_comb = parse_m3u8_folder(directory_path)
df_22_comb.head()

# Recently ADDED
directory_path = f'{path_ms_all_data}/m3u8_playlists/added_pl'
df_23_added = parse_m3u8_folder(directory_path)
df_23_added.head()

#Merge all and export
df_pl_ALL = pd.concat([df_TM_pr, df_23_comb , df_23,df_22_comb,df_22,df_23_added], ignore_index=True)
#export data frame 
#df_pl_ALL.to_pickle('m3u8_df_all_playlists_purge.pkl')

print('m3u8 df ::: df_pl_ALL')


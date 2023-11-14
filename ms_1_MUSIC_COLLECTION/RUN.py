
# Description:
# The program organizes and filters a music collection by analyzing file metadata and other criteria, ensuring that only songs meeting quality standards are added to a refined collection. To ensure the accuracy of all song metadata fields, the program relies on the ffmpeg audio processing capabilities from Python and employs heavy Python libraries renowned for data science tasks.The process involves:

# Reading metadata from music files.
# Cleaning the dataset by removing unwanted entries.
# Comparing the cleaned data with an existing collection to find new additions and missing entries.
# Computing song duration and bitrate for the new additions.
# Filtering songs based on duration and bitrate criteria.
# Identifying and handling duplicates.
# Moving files based on the filtering results for an optimized music collection by song quality treshhold
# Prompting the user for confirmation before safely deleting unwanted files.
# Updating the refined collection

#                                                     +----------------------+
#                                                     | Read Music Metadata  |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     |  Clean Dataset       |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     | Compare with Existing|
#                                                     | Collection           |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     | Compute Song Duration|
#                                                     | & Bitrate            |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     | Filter by Duration & |
#                                                     | Bitrate              |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     | Handle Duplicates    |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     | Move Files           |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     | User Confirmation to |
#                                                     | Delete Files         |
#                                                     +----------+-----------+
#                                                                |
#                                                                v
#                                                     +----------+-----------+
#                                                     | Update Refined       |
#                                                     | Collection           |
#                                                     +----------------------+


#-------------------
# ---------------------------------------
# PACKAGES and TABLES
# ---------------------------------------
import pandas as pd
import shutil
import os
from tqdm import tqdm

# import sys;import io ; original_stdout = sys.stdout ; sys.stdout = io.StringIO()          # Suppress this output
# exec(open(f"/Users/yerik/_apple_source/PY/GLOBAL/_1_paths.py", encoding="utf-8").read())  # GLOBAL
# direc = curr_direc ; sys.stdout = original_stdout                                         # Reset Suppress
# print('GLOBAL-RAN')

collection_table = '0_coll.pkl'

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
exec(open(f"{direc}/ms_2_music_files_export_table.py", encoding="utf-8").read())

# Clean the data
df = df_AU_ALL[~df_AU_ALL['Name'].str.startswith('._')].copy()
df = df[df['Type'] != 'Directory']

# Load collection table
df_id = pd.read_pickle(f'{direc}/{collection_table}')
print('Data in collection table "df_id":', len(df_id))
print('Data in folder "df":', len(df))

# ---------------------------------------
# DATA DIFFERENCES
# ---------------------------------------
# Finding discrepancies between two datasets
missing_in_df_id = df[~df['Path'].isin(df_id['Path'])]
missing_in_df = df_id[~df_id['Path'].isin(df['Path'])]

print("Paths in df but not in df_id: ", len(missing_in_df_id))
print("Paths in df_id but not in df: ", len(missing_in_df))
missing_in_files = missing_in_df['Name']
print(missing_in_files)    
input('Enter to acknoladge\delete from COLL_TABLE that the avobe FILES have been DELETED from DB')

# Update the collection table
df_id = df_id[df_id['Path'].isin(df['Path'])]

# Update df for further computations
df = missing_in_df_id.copy()

# ---------------------------------------
# COMPUTE DURATION and BITRATE
# ---------------------------------------
# Calculate duration
exec(open(f"{direc}/_ms_fields_1_duration.py", encoding="utf-8").read())
df['Duration'] = [get_duration(path) for path in tqdm(df['Path'], desc="DURATION:::Processing files")]

# Calculate bitrate
exec(open(f"{direc}/_ms_fields_2_bitrate.py", encoding="utf-8").read())
df['bitrate'] = df.apply(lambda row: compute_bitrate(row['Path'], row['Duration']), axis=1)

# Convert duration to minutes and filter
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
df['duration_minutes'] = df['Duration'] / 60

df_short_erase = df[df['duration_minutes'] < 2].copy()
df_long_erase = df[df['duration_minutes'] > 12].copy()
df_filtered = df[(df['duration_minutes'] > 2) & (df['duration_minutes'] < 12)].copy()

print('Durations to erase:', len(df_short_erase), len(df_long_erase), 'Will check:', len(df_filtered))

# Bitrate filtering
df_investigate = df_filtered[df_filtered['bitrate'] >= 320].copy()
df_bitrate_erase = df_filtered[df_filtered['bitrate'] < 320].copy()

print('Bitrates to erase:', len(df_bitrate_erase))

# ---------------------------------------
# HANDLE DUPLICATES by special id
# ---------------------------------------
# Create identifiers
df_investigate['Size (MB) id'] = df_investigate['Size (MB)'].astype(str)
df_investigate['file_id'] = df_investigate['Name']+ '-MB-' +df_investigate['Size (MB) id']+ df_investigate['Extension']

df_result = pd.concat([df_id, df_investigate], ignore_index=True, sort=False)
df_result['Size (MB) id'] = df_result['Size (MB)'].astype(str)
df_result['file_id'] = df_result['Name']+ '-MB-' +df_result['Size (MB) id']+ df_result['Extension']

# Identify unique and duplicated entries
df_unique = df_result[~df_result['file_id'].duplicated(keep='first')].copy()
df_duplicates = df_result[df_result['file_id'].duplicated(keep='first')].copy()

print('Unique & Duplicates:')
print('Unique:', len(df_unique), 'Duplicates:', len(df_duplicates))

df_unique = df_unique.drop('Size (MB) id', axis=1).copy()
# ---------------------------------------
# FILE OPERATIONS
# ---------------------------------------
def move_files(df, destination):
    """
    Move files from the 'Path' column of the dataframe to the specified destination.
    """
    for file_path in tqdm(df['Path'], desc="Moving files", unit="file"):
        try:
            shutil.copy(file_path, destination)
        except Exception as e:
            print(f"Error moving {file_path} to {destination}: {e}")

move_files(df_bitrate_erase, "/Volumes/HD_back_UP/ALL_MUSIC/UNWANTED_songs")
move_files(df_short_erase, "/Volumes/HD_back_UP/ALL_MUSIC/Music_back_up/_2_source_PROD/PROD_check")
move_files(df_long_erase, "/Volumes/HD_back_UP/ALL_MUSIC/Music_back_up/_6_SETS/SETS_check")
move_files(df_duplicates, "/Volumes/HD_back_UP/ALL_MUSIC/UNWANTED_songs/_DUPLICATES")

df_delete = pd.concat([df_bitrate_erase, df_short_erase, df_long_erase, df_duplicates], ignore_index=True)
print('Files to delete:', len(df_delete))

def delete_files_safely(df):
    """
    Safely delete the files listed in the 'Path' column of the dataframe.
    Bypass and print any errors encountered.
    """
    for file_path in tqdm(df['Path'], desc="Deleting files", unit="file"):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

input_delete = input('ATTN:: Delete these files? [y/n]   ')
if input_delete == 'y':
    delete_files_safely(df_delete)

if df.empty:
    print("Nothing to add, exiting...")
else:

    # Add pl info  FIELDS # if lufs are empty ...    
    df = df_unique[df_unique['lufs'].isna()] # rows to process
    df_coll_now = df_unique[df_unique['lufs'].notna()] #rows already process to concat
    ################################################                                       1) id TAGS
    exec(open(f"{direc}/_ms_pl_info_1a_all-id-tags.py", encoding="utf-8").read())
    ################################################                                       2)  LUFS
    exec(open(f"{direc}/_ms_pl_info_2_all_LUFS.py",encoding="utf-8").read())
    df['lufs'] = compute_lufs_for_paths(df['Path'])
    ################################################                                       3)  BPM
    exec(open(f"{direc}/_ms_pl_info_3_BPM.py",encoding="utf-8").read())
    df['BPM'] = [compute_bpm(x) if x.endswith(tuple(audio_extensions)) else None for x in tqdm(df['Path'], desc="Computing BPM")]
    #
    print(len(df_coll_now),len(df))

    # CLEAN and concat collection and adding tracks to collection

    df_unique = pd.concat([df_coll_now, df], ignore_index=True)



# Update the pickle file

 df_unique.to_pickle(f'{direc}/{collection_table}')


################################################ END

###############changes from 

#df = pd.read_pickle(f'{direc}/{collection_table}')
































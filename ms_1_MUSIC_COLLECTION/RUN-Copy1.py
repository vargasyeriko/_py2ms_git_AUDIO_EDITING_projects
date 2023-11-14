

# PACKAGES and TABLES
direc = '/Users/yerik/_apple_source/PY/JUPY/py2ms/ms_MUSIC_COLLECTION/'
collection_table ="1_song_quality_fields_unique.pkl"
####################################


exec(open(f"{direc}/ms_2_music_files_export_table.py",encoding="utf-8").read())

# CLEAN
df = df_AU_ALL[~df_AU_ALL['Name'].str.startswith('._')].copy()
df = df[df['Type'] != 'Directory']

# bring up # Bring in data collection table
df_id = pd.read_pickle(f'{direc}/{collection_table}')


print('This is the amount in collection table :"df_id":',len(df_id),'\n\n Amount in folder just read :"df":',len(df)) 

import pandas as pd


# Paths in df but not in df_id
missing_in_df_id = df[~df['Path'].isin(df_id['Path'])]

# Paths in df_id but not in df
missing_in_df = df_id[~df_id['Path'].isin(df['Path'])]

print("Elements in df['Path'] Folders that are NOT in df_id['Path']: TABLE \n\n WE WANT THIS TO HAVE more if NEW added\n")
missing_in_df_id


# erase from collection table (my df data frame)the elements I have erased in folder i dont want in collection table

# Removing rows from df_id that have the Path values missing in df
df_id = df_id[df_id['Path'].isin(df['Path'])]

print("\nElements in df_id['Path'] aka Table that are NOT in df['Path']: FOLDERS \n\n WE WANT THIS TO HAVE none, if one or two ERASE\n")
missing_in_df

print('After fixing table at the beggining now we have the uptaded Collection Table with ', len(df_id), 
      f'+ {len(missing_in_df_id)} to be checked/add')


# compute DURATION of missing_in_df_id # BEAUTY THE two I need to add becomes df now
df = missing_in_df_id.copy()


#1# COMPPUTE ---------------------- DURATION
exec(open(f"{direc}/_ms_fields_1_duration.py",encoding="utf-8").read())
df['Duration'] = [get_duration(path) for path in tqdm(df['Path'], desc="DURATION:::Processing files")]

#2# COMPPUTE ---------------------- BITRATE
exec(open(f"{direc}/_ms_fields_2_bitrate.py",encoding="utf-8").read());print('BITRATE :::Processing files : DONE')
df['bitrate'] = df.apply(lambda row: compute_bitrate(row['Path'], row['Duration']), axis=1)

df['bitrate'].dtype,df['Duration'].dtype


# Convert 'duration' column to numeric, coercing errors to NaN
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')


# make a new variable
df['duration_minutes'] = df['Duration'] / 60
#filter songs below 2 min long
df_short_erase = df[df['duration_minutes'] < 2].copy()
#filter songs over 12 min long
df_long_erase = df[df['duration_minutes'] > 12].copy()
#filter songs within range (2,12)
df_filtered = df[(df['duration_minutes'] > 2) & (df['duration_minutes'] < 12)].copy()

print('will be ERASE from DURATION::',len(df_short_erase), len(df_long_erase),'will be taken next check', len(df_filtered))

df_investigate = df_filtered[df_filtered['bitrate'] >= 320].copy()
# erase 
df_bitrate_erase = df_filtered[df_filtered['bitrate'] < 320].copy()
print('\n\nwill be ERASE from BITRATE ::',len(df_bitrate_erase))

# taking 320 bitrate as the lowest quality accepted, we move forward and export the table for futher investigation
# remember the goal of this project is to filter songs for ultimate collection where we can play without so much 
# worrying of what is the quality and DO INVESTIGATE in case you have 319 through DF_FILETERED first
df_bitrate_erase['bitrate'].value_counts().sort_index(ascending=True)


print(df_investigate['Size (MB)'].sum()/1024,
      ' GB to be added to collection . GB in df_id::',df_id['Size (MB)'].sum()/1024) 
print('\n !!! Following will be adding minus duplicates NEXT')
len(df_investigate)

# Make DF the same for identifier

df_investigate['Size (MB) id'] = df_investigate['Size (MB)'].astype(str)
df_investigate['file_id'] = df_investigate['Name']+ '-MB-' +df_investigate['Size (MB) id']+ df_investigate['Extension']

df_result = pd.concat([df_id,df_investigate], ignore_index=True, sort=False)

len(df_result)

df_result['Size (MB) id'] = df_result['Size (MB)'].astype(str)

df_result['file_id'] = df_result['Name']+ '-MB-' +df_result['Size (MB) id']+ df_result['Extension']

# CHECK UNIQUE and/repeated
# Rows without duplicated SHA256 values (keeping only the first occurrence)
df_unique = df_result[~df_result['file_id'].duplicated(keep='first')].copy()
    
    # Rows with duplicated SHA256 values (excluding the first occurrence)
df_duplicates = df_result[df_result['file_id'].duplicated(keep='first')]

print('UNIQUE & DUPLICATES based on New name' )
print('UNIQUE     :::',len(df_unique), '  \nDUPLICATES :::' ,len(df_duplicates))

#df_tags

import shutil
import pandas as pd

def move_files(df, destination):
    """
    Move files from the 'Path' column of the dataframe to the specified destination.
    """
    for file_path in tqdm(df['Path'], desc="Moving files", unit="file"):
        try:
            shutil.copy(file_path, destination)
        except Exception as e:
            print(f"Error moving {file_path} to {destination}: {e}")


# Move files based on the dataframe's intended destination

# e_1_a # BITRATE erase to UNWANTED SONGS  "Music_misc/UNWANTED_songs"
move_files(df_bitrate_erase, "/Volumes/HD_back_UP/ALL_MUSIC/Music_misc/UNWANTED_songs")

# e_1_b # DURATION erase

# send to possible PRODUCTION MATERIAL "_2_source_PROD/PROD_check"
move_files(df_short_erase, "/Volumes/HD_back_UP/ALL_MUSIC/Music_back_up/_2_source_PROD/PROD_check")
# send to possible SETS to keep         "_4_SETS/SETS_check"
move_files(df_long_erase, "/Volumes/HD_back_UP/ALL_MUSIC/Music_back_up/_4_SETS/SETS_check")

# e_2 # DUPLICATES
move_files(df_duplicates, "/Volumes/HD_back_UP/ALL_MUSIC/Music_misc/UNWANTED_songs/_DUPLICATES")



df_delete = pd.concat([df_bitrate_erase, df_short_erase, df_long_erase, df_duplicates], ignore_index=True)
print('Following will be deleted::', len(df_delete))
df_delete


import os
from tqdm import tqdm
import pandas as pd

def delete_files_safely(df):
    """
    Safely delete the files listed in the 'Path' column of the dataframe.
    Bypass and print any errors encountered.
    """
    for file_path in tqdm(df['Path'], desc="Deleting files", unit="file"):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e} : OPPENING FILES")

input_delete = input('ATTN:: To delete this files [y]   ')

if input_delete == 'y' :
    delete_files_safely(df_delete)



df_unique.to_pickle(f'{direc}/{collection_table}')




























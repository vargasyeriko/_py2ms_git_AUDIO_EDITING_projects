
print('------------------------------------------------------------------------- for On DEMAND = Music_2022')

# Get all Music extension to a ***df*** and frequency of results as  ***results***

path_songs = f'/Volumes/HD_back_UP/ALL_MUSIC/Music_back_up/_0_source_DJ_ON-DEMAND/Music_2022' 

my_folder_path = path_songs
exec(open(f"{direc}/ms_1_music_files.py",encoding="utf-8").read()) #paths

df_AU_2022 = df_AU.copy()
df_AU_2022

print('------------------------------------------------------------------------- for On DEMAND = Music_2023')

# Get all Music extension to a ***df*** and frequency of results as  ***results***

path_songs = f'/Volumes/HD_back_UP/ALL_MUSIC/Music_back_up/_0_source_DJ_ON-DEMAND/Music_2023' 

my_folder_path = path_songs
exec(open(f"{direc}/ms_1_music_files.py",encoding="utf-8").read()) #paths

df_AU_2023 = df_AU.copy()
df_AU_2023

print('----------------------------------------------------------------------- for On SOURCE = source')
# Get all Music extension to a ***df*** and frequency of results as  ***results***

path_songs = f'/Volumes/HD_back_UP/ALL_MUSIC/Music_back_up/_1_source_DJ' 

my_folder_path = path_songs
exec(open(f"{direc}/ms_1_music_files.py",encoding="utf-8").read()) #paths

df_AU_source = df_AU.copy()
df_AU_source

# ######################## Stack dataframes
print('----------------------------------------------------------------------- MERGED ALL df_AU_(1-3) together')

df_AU_ALL= pd.concat([df_AU_2022, df_AU_2023,df_AU_source], ignore_index=True)


print('\nATTN ::::: df_AU_ALL :::::: M22 M23 and SOURCE in one df')
print('\nALL MUSIC FILES in HD_bu :: total BYTES ', df_AU_ALL['Size (MB)'].sum(), '  total music Files ',len(df_AU_ALL))

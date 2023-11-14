
# Program to get all music files to a df

#exec(open(f"/Users/yerik/_apple_source/PY/GLOBAL/_1_paths.py",encoding="utf-8").read()) #paths

# Check files within a directory with  my_folder_path
# 
my_folder_path = path_songs
#

exec(open(f"/Users/yerik/_apple_source/PY/GLOBAL/_2_read_file_paths.py",encoding="utf-8").read()) #paths

# List of audio extensions
audio_extensions = ['.m4a','.mp3', '.MP3','.Mp3' ,'.wav', '.WAV', '.flac', '.FLAC', '.aac',
                     '.ogg', '.wma', '.au', '.aif', '.aiff']

# Filter DataFrame based on the extensions
df_AU = df[df['Extension'].isin(audio_extensions)].copy()

# Step 1: Group by Extension Type and Calculate Frequency
frequency_by_extension = df_AU['Extension'].value_counts().reset_index()
frequency_by_extension.columns = ['Extension', 'frequency']

# # Step 2: Group by Extension Type and Sum the Sizes
total_size_by_extension = df_AU.groupby('Extension')['Size (MB)'].sum().reset_index()
total_size_by_extension.columns = ['Extension', 'total_size_in_mb']

# # Step 3: Merge the Two Tables
result = pd.merge(frequency_by_extension, total_size_by_extension, on='Extension')

print('\n\n FREQUENCY TABLE of \n\n', audio_extensions,'\n\n\n')
print('total music files : ',result['frequency'].sum(), '\n\n',result)
print(f' \n ATTN -> \nDF with ALL files ::: df :{len(df)}:: & \nDF with just audio_extensions ::: df_AU ::{len(df_AU)}:')

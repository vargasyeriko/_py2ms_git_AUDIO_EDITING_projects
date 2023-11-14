
# CHECK UNIQUE and/repeated
# Rows without duplicated SHA256 values (keeping only the first occurrence)
df_unique = df_pl_ALL[~df_pl_ALL['Path'].duplicated(keep='first')]
    
    # Rows with duplicated SHA256 values (excluding the first occurrence)
df_duplicates = df_pl_ALL[df_pl_ALL['Path'].duplicated(keep='first')]

print('UNIQUE & DUPLICATES based on New name' )
print('UNIQUE     :::',len(df_unique), '  \nDUPLICATES :::' ,len(df_duplicates))

#df_tags

file_paths = df_unique['Path'].tolist()

#file_path_erase = [path for path in file_paths if path not in file_playlists_keep]

non_existent_files = []


for path in file_paths:
    if not os.path.exists(path):
        non_existent_files.append(path)

# Print the files that don't exist
if non_existent_files:
    print("The following files do not exist:")
    for file in non_existent_files:
        print(file)
    print(len(non_existent_files))
else:
    print("All files paths in all playlists purged _ exist.")

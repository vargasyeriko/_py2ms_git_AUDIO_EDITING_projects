#df_tags

file_paths = df_unique['Path'].tolist()

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
    print("----> ATTN :: All files paths in all EXIST")

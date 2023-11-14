import pandas as pd

def select_playlist(df):
    # Get unique playlist names
    unique_playlists = df['playlist_name'].unique().tolist()
    
    # Print out playlists with a numbering
    for idx, playlist in enumerate(unique_playlists, 1):
        print(f"{idx}. {playlist}")
    
    # Prompt user for a choice
    while True:
        try:
            choice = int(input("Enter the number corresponding to your playlist choice: "))
            if 1 <= choice <= len(unique_playlists):
                break
            else:
                print("Number out of range. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Get the selected playlist name
    chosen_playlist = unique_playlists[choice-1]
    
    # Filter the dataframe by the selected playlist
    filtered_df = df[df['playlist_name'] == chosen_playlist]
    
    return filtered_df

# Pick 2 - 4 playlists
filtered_df_0 = select_playlist(df_pl_ALL)
filtered_df_1 = select_playlist(df_pl_ALL)
filtered_df_2 = select_playlist(df_pl_ALL)
filtered_df_3 = select_playlist(df_pl_ALL)

filtered_df_4 = select_playlist(df_pl_ALL)
filtered_df_5 = select_playlist(df_pl_ALL)
filtered_df_6 = select_playlist(df_pl_ALL)
filtered_df_7 = select_playlist(df_pl_ALL)


#############
df_pl_1 = pd.concat([filtered_df_0, filtered_df_1, filtered_df_2, filtered_df_3,
                     filtered_df_4, filtered_df_5, filtered_df_6, filtered_df_7], ignore_index=True)
df_pl_1['base_name'] = df_pl_1['Path'].apply(os.path.basename)

# CHECK UNIQUE and/repeated
# Rows without duplicated SHA256 values (keeping only the first occurrence)
df_pl_1_unique = df_pl_1[~df_pl_1['base_name'].duplicated(keep='first')]
    
    # Rows with duplicated SHA256 values (excluding the first occurrence)
f_pl_1_dup = df_pl_1[df_pl_1['base_name'].duplicated(keep='first')]

print('UNIQUE & DUPLICATES based on New name' )
print('UNIQUE     :::',len(df_pl_1_unique), '----------:: total to be the list exported as m3u8: df_pl_1_unique  \nDUPLICATES :::' ,
      len(f_pl_1_dup))

#df_tags

print('Total in Playlists combined :: ',len(df_pl_1),   'in df_pl_1')

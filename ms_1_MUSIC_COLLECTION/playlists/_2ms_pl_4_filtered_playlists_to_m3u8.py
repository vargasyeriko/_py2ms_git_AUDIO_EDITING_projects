def dataframe_to_m3u8(df, output_filepath):
    """
    Generate an m3u8 file from the first 10 rows of the DataFrame.
    
    Args:
    - df (DataFrame): The DataFrame containing 'track_id_rk', 'Name', and 'Path' columns.
    - output_filepath (str): The desired path for the output m3u8 file.
    """
    # Take the first 10 rows
    subset_df = df
    
    with open(output_filepath, 'w') as file:
        # Add header if desired (you can remove this line if not needed)
        file.write("#EXTM3U\n")

        for _, row in subset_df.iterrows():
            file.write(f"#EXTINF:{row['track_id_rk']},{row['Name']}\n")
            file.write(f"{row['Path']}\n")



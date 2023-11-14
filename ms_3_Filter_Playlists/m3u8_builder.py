exec(open(f"/Users/yerik/_apple_source/PY/GLOBAL/_1_paths.py",encoding="utf-8").read()) #paths

import os
import pandas as pd

# Read all playlists
df_id = pd.read_pickle(f'{path_ms_tables}/_4_rkb_m3u8_LUFS_repeated_existing_all.pkl')
df_pl_ALL = df_id[~df_id['Name'].str.startswith('._')].copy()
print(len(df_pl_ALL))
df_pl_ALL.head(3)

##fn
exec(open(f"_2_select_4_m3u8_playlists.py",encoding="utf-8").read()) #paths
print('Total unique counts in playlists' , len(df_pl_1_unique))



df =df_pl_1_unique.copy()
median = df['vol_lufs'].median()
print(f"Median of 'lufs': {median}")
df.describe()

print('filtering for vol_lufs (-7,-11)')
filtered_df = df[(df['vol_lufs'] > -11) & (df['vol_lufs'] < -7)]
print('T\n otal after applying LUFS filter',len(filtered_df))
##fn
# here to export your paths
df_unique_m3u8 = filtered_df

# EXPORT lufs ALL
#LL.to_pickle(f'{path_ms_tables}/_4_rkb_m3u8_LUFS_repeated_existing_all.pkl')

exec(open(f"_3_export_4_m3u8_desktop.py",encoding="utf-8").read()) #paths

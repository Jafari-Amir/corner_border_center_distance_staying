import os
import pandas as pd
import glob
import numpy as np

txt = 'zzzzz'
path = f'/Users/xxxxxxxxx/Downloads/{txt}/'
all_files = glob.glob(os.path.join(path, "*.csv"))
df_single = []
for f in all_files:
    df_primary = pd.read_csv(f)
    df = df_primary.drop(df_primary.index[np.where(df_primary.index > 9000)])
    df = df[df['ROI_transition'] == True]
    df['total_transition'] = df['ROI_transition'].cumsum()
    categories_lists = [['c1', 'c2', 'c3', 'c4'], ['c1_b1','c1_b4','c2_b1','c2_b2','c3_b3','c3_b4','c4_b4','c4_b3'],
                        ['b1', 'b2', 'b3', 'b4'], ['b1_center', 'b2_center', 'b3_center', 'b4_center'], ['center']]
    cor = ['c1', 'c2', 'c3', 'c4']
    cr_br = ['c1_b1','c1_b4','c2_b1','c2_b2','c3_b3','c3_b4','c4_b4','c4_b3']
    bor = ['b1', 'b2', 'b3', 'b4']
    br_cen = ['b1_center', 'b2_center', 'b3_center', 'b4_center']
    ct = ['center']
    
    df['cor_entrance_sum'] = df['ROI_location'].isin(cor).cumsum(axis=0)
    df['cr_br_entrance_sum'] = df['ROI_location'].isin(cr_br).cumsum(axis=0)
    df['bor_entrance_sum'] = df['ROI_location'].isin(bor).cumsum(axis=0)
    df['br_cen_entrance_sum'] = df['ROI_location'].isin(br_cen).cumsum(axis=0)
    df['ct_entrance_sum'] = df['ROI_location'].isin(ct).cumsum(axis=0) 
    df['File_name'] = os.path.basename(f)
    df_single.append(df)
    # concatenate the dataframes and save the result to a CSV file
s = pd.concat(df_single, axis=1)
#here we need to be selective in the choice of result to avoide any further copy paste action
specified_columns = ['File_name','cor_entrance_sum', 'bor_entrance_sum','ct_entrance_sum', 'br_cen_entrance_sum', 'cr_br_entrance_sum','total_transition']
df_filtered = s[specified_columns]
# extract the last row of each repeated DataFrame
last_rows = [df_filtered[-1:] for df_filtered in df_single]
# concatenate the list of last rows into a single DataFrame
result = pd.concat(last_rows, axis=0)
df_filtered = result.drop(columns=[col for col in result.columns if col not in specified_columns], inplace=False)
df_filtered.to_excel(f'_{txt}.xlsx', index=False)
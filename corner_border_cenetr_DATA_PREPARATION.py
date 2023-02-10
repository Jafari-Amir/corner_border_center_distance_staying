import os
import pandas as pd
import glob
import numpy as np
path = '/Users/zz/zz/zz/'
all_files = glob.glob(os.path.join(path, "*.csv"))
df_single = []
for f in all_files:
    df_primary = pd.read_csv(f)
    df = df_primary.drop(df_primary.index[np.where(df_primary.index > 9000)])
    df['Dis_cm'] = df['Distance_cm'].cumsum()
    df['ROI_TT_S'] = df['ROI_transition'].cumsum()
    categories_lists = [['c1', 'c2', 'c3', 'c4'], ['c1_b1','c1_b4','c2_b1','c2_b2','c3_b3','c3_b4','c4_b4','c4_b3'],
                        ['b1', 'b2', 'b3', 'b4'], ['b1_center', 'b2_center', 'b3_center', 'b4_center'], ['center']]
    cor = ['c1', 'c2', 'c3', 'c4']
    cr_br = ['c1_b1','c1_b4','c2_b1','c2_b2','c3_b3','c3_b4','c4_b4','c4_b3']
    bor = ['b1', 'b2', 'b3', 'b4']
    br_cen = ['b1_center', 'b2_center', 'b3_center', 'b4_center']
    ct = ['center']
    
    df['ROI_cor'] = df['ROI_location'].isin(cor).cumsum(axis=0)
    df['ROI_cr_br'] = df['ROI_location'].isin(cr_br).cumsum(axis=0)
    df['ROI_bor'] = df['ROI_location'].isin(bor).cumsum(axis=0)
    df['ROI_br_cen'] = df['ROI_location'].isin(br_cen).cumsum(axis=0)
    df['ROI_ct'] = df['ROI_location'].isin(ct).cumsum(axis=0)
    df_single.append(df)
    # concatenate the dataframes and save the result to a CSV file
s = pd.concat(df_single, axis=1)
#here we need to be selective in the choice of result to avoide any further copy paste action
specified_columns = ['ROI_cor', 'ROI_cr_br', 'ROI_bor', 'ROI_br_cen', 'ROI_ct','ROI_TT_S', 'Dis_cm']
df_filtered = s[specified_columns]
# extract the last row of each repeated DataFrame
last_rows = [df_filtered[-1:] for df_filtered in df_single]
# concatenate the list of last rows into a single DataFrame
result = pd.concat(last_rows, axis=0)
df_filtered = result.drop(columns=[col for col in result.columns if col not in specified_columns], inplace=False)
df_filtered.to_csv('/Users//result.csv', index=False)
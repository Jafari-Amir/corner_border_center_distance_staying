import os
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
selected_locations = {"corners": ['c1', 'c2', 'c3', 'c4'], "border": ['b1', 'b2', 'b3', 'b4'],"center": ['center']}
s1 = pd.DataFrame()
s2 = pd.DataFrame()
s3 = pd.DataFrame()
txt = 'Male_Sac_CNTL'
path = f'/Users/amir1/Downloads/{txt}/'
all_files = glob.glob(os.path.join(path, "*.csv"))
results = pd.DataFrame(columns=['location', 'slope', 'intercept', 'file_name', 'data_range'])
selected_locations = {"corners": ['c1', 'c2', 'c3', 'c4'], "borders": ['b1', 'b2', 'b3', 'b4'], "center": ['center']}
for f in all_files:
    df = pd.read_csv(f)
    df = df.drop(df.index[np.where(df.index > 9000)])
    df = df[df['ROI_transition'] == True]
    df['Frame'] = df['Frame'] / 1800
        # split the data into different ranges of the index
    s1 = df[(df.index >= 1) & (df.index <= 3000)].fillna(0)
    s2 = df[(df.index >= 3000) & (df.index <= 6000)].fillna(0)
    s3 = df[(df.index >= 6000) & (df.index <= 9000)].fillna(0)
    file_name = os.path.basename(f)
        # process each location and save the results
    for location_name, locations in selected_locations.items():
        for i, s in enumerate([s1, s2, s3]):
            # filter the data for the current location and range
            df_location = s[s["ROI_location"].isin(locations)]
            if df_location.empty:
                continue
                # pivot the data
            pivoted = df_location.pivot_table(values="ROI_transition", index=["Frame"], columns=["ROI_location"]).fillna(0)
            cumsum_df = pivoted.cumsum(axis=1)
            sum_of_locations = cumsum_df.iloc[:, -1].cumsum()
            pivoted['sum_of_locations'] = sum_of_locations
                        # linear regression on the sum_of_locations column
            x = pivoted.index.values.reshape(-1, 1)
            y = pivoted['sum_of_locations'].values
            slope, intercept = np.polyfit(x.ravel(), y, 1)
            
            # append the results to the DataFrame
            results = results.append({
                'location': location_name,
                'slope': slope,
                'intercept': intercept,
                'file_name': file_name,
                'data_range': f'{i+1}' if s['ROI_transition'].count() > 0 else np.nan
            }, ignore_index=True)
        # replace repeated 's' values with numbers under each other
results.to_excel(f'between_{txt}.xlsx', index=False)
# read the data
dddf = pd.read_excel(f'/Users/amir1/Downloads/between_{txt}.xlsx')
cor = dddf[dddf['location'] == 'corners']
bor = dddf[dddf['location'] == 'borders']
ct = dddf[dddf['location'] == 'center']

cor = cor.groupby(['data_range'])['slope'].apply(list).reset_index()
bor = bor.groupby(['data_range'])['slope'].apply(list).reset_index()
ct = ct.groupby(['data_range'])['slope'].apply(list).reset_index()

remove_brackets = lambda x: str(x).replace('[','').replace(']','')
cor['slope'] = cor['slope'].apply(remove_brackets)
bor['slope'] = bor['slope'].apply(remove_brackets)
ct['slope'] = ct['slope'].apply(remove_brackets)
# concatenate the dataframes
seperated = pd.concat([cor, bor, ct])
seperated.to_excel(f'within_{txt}.xlsx', index=False)
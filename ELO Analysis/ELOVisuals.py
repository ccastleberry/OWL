import pandas as pd 
import matplotlib.pyplot as plt



TEAM_COLOR_DICT = {
    'LDN': '#78c9e5',
    'DAL': '#2f72c7',
    'SHD': '#000000',
    'SFS': '#e85609',
    'BOS': '#264b92',
    'PHI': '#f49d00',
    'SEO': '#a78a2c',
    'NYE': '#265ae1',
    'FLA': '#b50004',
    'VAL': '#eace00',
    'HOU': '#a1c861',
    'GLA': '#6d3eb9'
}

def plot_elo_by_match(df, title="Elo by Match", figsize=(12,12)):
    
    # Create team list
    team_list = list(df["Team"].unique())

    # get highest match
    df = df.sort_values(by='Match Number', ascending=False).reset_index(drop=True)
    top_match = df.iloc[0]['Match Number']

    # Build individual df's
    team_elo_dfs = {}
    for team in team_list:
        temp_elo_df = df[df["Team"]==team]
        team_elo_dfs[team] = temp_elo_df

    plt.figure(figsize=figsize)
    for key, value in team_elo_dfs.items():
        plt.plot(value['Match Number'], value['Elo'], label=key, marker='o', color=TEAM_COLOR_DICT[key])
    plt.xlim([0,top_match+2])
    plt.xlabel("Match Number")
    plt.ylabel("Elo")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()
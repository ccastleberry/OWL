'''
Contains any functions pertaining to the computation of Elo or
other ranking systems.

All functions here should be sport/esport agnostic.
'''

import pandas as pd



def get_current_elo(df, team, date):
    df = df[(df["Team"] == team) & (df['Date'] <= date)]
    df = df.sort_values(by=['Date', 'Match Number'], ascending=False).reset_index(drop=True)
    elo = df.iloc[0]['Elo']
    return elo


def get_current_match_number(df, team, date):
    df = df[(df["Team"] == team) & (df['Date'] <= date)]
    df = df.sort_values(by='Match Number', ascending=False).reset_index(drop=True)
    match_num = df.iloc[0]['Match Number']
    return match_num


def elo_probabilities(elo_a, elo_b):
    q_a = 10**(elo_a/400)
    q_b = 10**(elo_b/400)
    e_a = q_a / (q_a + q_b)
    e_b = q_b / (q_a + q_b)
    return e_a, e_b


def update_elo(elo_a, elo_b, a_win, K=20):
    q_a = 10**(elo_a/400)
    q_b = 10**(elo_b/400)
    e_a = q_a / (q_a + q_b)
    e_b = q_b / (q_a + q_b)
    
    
    r_a = elo_a + K * (a_win - e_a)
    r_b = elo_b + K * ((1-a_win) - e_b)
    return r_a, r_b


def compute_elo_table(df, K=20, elo_start=1000):
    '''
    Takes in a dataframe with match results
    and returns dataframe with a list of all elo changes

    args:
        df: pandas dataframe
            columns = ['Date', 'Match of the Day', 'Team A', 'Team B', 'Winner']
            types = [str 'yyyy-mm-dd' format, int,  str, str, str=(Team A, Team B, Tie)]
        K: int
            the elo update factor
    
    returns:
        df: Pandas dataframe
            columns = ['Date', 'Match Number', "Team", 'Elo']
    '''
    # Generate list of all teams
    team_a_list = set(df["Team A"].unique())
    team_b_list = set(df["Team B"].unique())
    team_list = list(team_a_list.union(team_b_list))

    # sort df and get date of first match
    df = df.sort_values(by=['Date', 'Match of the Day'], ascending=True).reset_index(drop=True)
    start_date = df.iloc[0]['Date']
    start_date = start_date[:-2] + "{:02}".format(int(start_date[-2:])-1)

    # Create list of dicts for initial elo's
    team_elo_start = []
    for team in team_list:
        team_elo = {
            "Date": start_date,
            "Team": team, 
            "Elo": elo_start,
            "Match Number": 0
        }
        team_elo_start.append(team_elo)
    
    # Create elo dataframe
    elo_df = pd.DataFrame(team_elo_start)

    # Main Loop through match results (input df)
    for i in range(df.shape[0]):
        current_match = df.iloc[i]
        team_a = current_match['Team A']
        team_b = current_match['Team B']
        match_date = current_match['Date']
        winner = current_match['Winner']
        if winner == 'Team A':
            a_win = 1
        elif winner == 'Team B':
            a_win = 0
        else:
            a_win = 0.5
            
        a_elo = get_current_elo(elo_df, team_a, match_date)
        b_elo = get_current_elo(elo_df, team_b, match_date)
        a_map = get_current_match_number(elo_df, team_a, match_date) + 1
        b_map = get_current_match_number(elo_df, team_b, match_date) + 1
        new_a_row = {
            'Date': match_date,
            'Team': team_a,
            'Match Number': a_map
        }
        new_b_row = {
            'Date': match_date,
            'Team': team_b,
            'Match Number': b_map
        }
        new_a_row['Elo'], new_b_row['Elo'] = update_elo(a_elo, b_elo, a_win=a_win, K=K)
        temp_df = pd.DataFrame([new_a_row, new_b_row])
        #print(temp_df.head())
        elo_df = pd.concat([elo_df, temp_df])
    # Return the dataframe sorted by date and match with reset indices
    return elo_df.sort_values(by=['Date', 'Match Number'], ascending=True).reset_index(drop=True)
        




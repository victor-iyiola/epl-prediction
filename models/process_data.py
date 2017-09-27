import os.path
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale

DATASET_DIR = '../datasets/'
DATA_FILES = ['epl-2015-2016.csv', 'epl-2016-2017.csv', 'epl-2017-2018.csv']
IMPORTANT_FEATURES = []
CURR_SEASON_DATA = os.path.join(DATASET_DIR, DATA_FILES[-1])


def load_data():
    dataset = []
    for d_file in DATA_FILES:
        d_file = os.path.join(DATASET_DIR, d_file)
        data = pd.read_csv(d_file, skiprows=0)
        dataset.append(data)
    return dataset


def get_remaining_features(home, away):
    df = pd.read_csv(CURR_SEASON_DATA)
    # Home team and Away team
    home_team = df['HomeTeam'].values
    away_team = df['AwayTeam'].values
    # Get the indexes for home and away team
    home_idx = get_index(home_team.tolist(), home)
    away_idx = get_index(away_team.tolist(), away)
    # Drop string columns
    df.drop(['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTR', 'HTR', 'Referee'], axis=1, inplace=True)
    # Get rows where the home and away team shows up respectively
    home_data = df.values[home_idx]
    away_data = df.values[away_idx]
    return np.average(home_data, axis=0), np.average(away_data, axis=0)


def get_index(teams, value):
    value = value.title()
    indexes = [i for i, team in enumerate(teams) if team == value]
    return indexes


# home_data, away_data = get_remaining_features(home='arsenal', away='chelsea')
# print(home_data, '\n')
# print(away_data)

def process(filename):
    data = pd.read_csv(filename)
    # FTR = full time result
    X_all = data.drop(['FTR'], axis=1)
    y_all = data['FTR']
    # Center to the mean and component wise scale to unit variance
    # cols = [['HTGD', 'ATGD', 'HTP', 'ATP', 'DiffLP']]
    # for col in cols:
    #     X_all[col] = scale(X_all[col])

    # last 3 wins for both sides
    # X_all.HM1 = X_all.HM1.astype('str')
    # X_all.HM2 = X_all.HM2.astype('str')
    # X_all.HM3 = X_all.HM3.astype('str')
    # X_all.AM1 = X_all.AM1.astype('str')
    # X_all.AM2 = X_all.AM2.astype('str')
    # X_all.AM3 = X_all.AM3.astype('str')
    X_all = preprocess_features(X_all)
    # X_all = scale(X_all)
    print(X_all.tail(3))


def preprocess_features(X):
    # init new output dataframe
    output = pd.DataFrame(index=X.index)
    # investigate each feature col for data
    for col, col_data in X.iteritems():
        # if data is categorical, convert to dummy variables
        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix=col)
        # collect the converted cols
        output = output.join(col_data)
    return output


process(CURR_SEASON_DATA)

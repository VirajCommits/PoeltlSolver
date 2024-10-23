from flask import Flask, request, jsonify
import requests
import pandas as pd
from datetime import datetime
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

API_KEY = '9d9174b6f1d04b068b8514d6765fff0e'
URL = f'https://api.sportsdata.io/v3/nba/scores/json/PlayersActiveBasic?key={API_KEY}'

# Dictionary for mapping teams to conferences and divisions
team_info = {
    'ATL': {'Conference': 'Eastern', 'Division': 'Southeast'},
    'BOS': {'Conference': 'Eastern', 'Division': 'Atlantic'},
    'BKN': {'Conference': 'Eastern', 'Division': 'Atlantic'},
    'CHA': {'Conference': 'Eastern', 'Division': 'Southeast'},
    'CHI': {'Conference': 'Eastern', 'Division': 'Central'},
    'CLE': {'Conference': 'Eastern', 'Division': 'Central'},
    'DAL': {'Conference': 'Western', 'Division': 'Southwest'},
    'DEN': {'Conference': 'Western', 'Division': 'Northwest'},
    'DET': {'Conference': 'Eastern', 'Division': 'Central'},
    'GSW': {'Conference': 'Western', 'Division': 'Pacific'},
    'HOU': {'Conference': 'Western', 'Division': 'Southwest'},
    'IND': {'Conference': 'Eastern', 'Division': 'Central'},
    'LAC': {'Conference': 'Western', 'Division': 'Pacific'},
    'LAL': {'Conference': 'Western', 'Division': 'Pacific'},
    'MEM': {'Conference': 'Western', 'Division': 'Southwest'},
    'MIA': {'Conference': 'Eastern', 'Division': 'Southeast'},
    'MIL': {'Conference': 'Eastern', 'Division': 'Central'},
    'MIN': {'Conference': 'Western', 'Division': 'Northwest'},
    'NOP': {'Conference': 'Western', 'Division': 'Southwest'},
    'NYK': {'Conference': 'Eastern', 'Division': 'Atlantic'},
    'OKC': {'Conference': 'Western', 'Division': 'Northwest'},
    'ORL': {'Conference': 'Eastern', 'Division': 'Southeast'},
    'PHI': {'Conference': 'Eastern', 'Division': 'Atlantic'},
    'PHO': {'Conference': 'Western', 'Division': 'Pacific'},
    'POR': {'Conference': 'Western', 'Division': 'Northwest'},
    'SAC': {'Conference': 'Western', 'Division': 'Pacific'},
    'SAS': {'Conference': 'Western', 'Division': 'Southwest'},
    'TOR': {'Conference': 'Eastern', 'Division': 'Atlantic'},
    'UTA': {'Conference': 'Western', 'Division': 'Northwest'},
    'WAS': {'Conference': 'Eastern', 'Division': 'Southeast'}
}


def calculate_age(birthdate_str):
    """Calculate age from birthdate string in ISO format."""
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%dT%H:%M:%S")
    today = datetime.today()
    age = today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )
    return age


# Fetch data from the API when the app starts
try:
    response = requests.get(URL)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Failed to fetch data: {e}")
    players = pd.DataFrame()
else:
    data = response.json()
    players = pd.DataFrame(data)
    players['Age'] = players['BirthDate'].apply(calculate_age)
    players['Conference'] = players['Team'].map(
        lambda x: team_info.get(x, {}).get('Conference', 'Unknown')
    )
    players['Division'] = players['Team'].map(
        lambda x: team_info.get(x, {}).get('Division', 'Unknown')
    )
    players['Name'] = players['FirstName'] + ' ' + players['LastName']
    players['Height'] = pd.to_numeric(players['Height'], errors='coerce')
    players['Age'] = pd.to_numeric(players['Age'], errors='coerce')
    players['Jersey'] = pd.to_numeric(players['Jersey'], errors='coerce')


def calculate_age(birthdate_str):
    """Calculate age from birthdate string in ISO format."""
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%dT%H:%M:%S")
    today = datetime.today()
    age = today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )
    return age


# Fetch data from the API when the app starts
try:
    response = requests.get(URL)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Failed to fetch data: {e}")
    players = pd.DataFrame()
else:
    data = response.json()
    players = pd.DataFrame(data)
    players['Age'] = players['BirthDate'].apply(calculate_age)
    players['Conference'] = players['Team'].map(
        lambda x: team_info.get(x, {}).get('Conference', 'Unknown')
    )
    players['Division'] = players['Team'].map(
        lambda x: team_info.get(x, {}).get('Division', 'Unknown')
    )
    players['Name'] = players['FirstName'] + ' ' + players['LastName']
    players['Height'] = pd.to_numeric(players['Height'], errors='coerce')
    players['Age'] = pd.to_numeric(players['Age'], errors='coerce')
    players['Jersey'] = pd.to_numeric(players['Jersey'], errors='coerce')
    players['PlayerID'] = players['PlayerID']
    players['TeamName'] = players['Team']  # Adjust if needed
    players['Position'] = players['PositionCategory']  # Adjust if needed


@app.route('/guess', methods=['POST'])
def guess():

    data = request.get_json()
    guesses = data.get('guesses', [])
    # print(guesses)

    if not guesses:
        return jsonify({'error': 'No guesses provided'}), 400

    # Initialize cumulative filters
    cumulative_filters = initialize_filters()

    # Process each guess to update filters
    for guess_entry in guesses:
        player = guess_entry.get('player')
        difference = guess_entry.get('difference')

        # print("player", player)
        # print("difference", difference)

        if not player or not difference:
            continue  # Skip invalid entries

        process_guess(player, difference, cumulative_filters)

    # Apply filters to the players DataFrame
    filtered_players = apply_filters(players, cumulative_filters)

    # Exclude previous guesses
    filtered_players = exclude_previous_guesses(filtered_players, guesses)

    # Prepare the filtered players to return
    filtered_players_json = filtered_players[['Name', 'TeamName', 'Conference', 'Division', 'Position', 'Height', 'Age', 'Jersey']].astype(
        object).where(pd.notnull(filtered_players), None).to_dict(orient='records')

    return jsonify({'filtered_players': filtered_players_json}), 200


def initialize_filters():
    return {
        'Conference': set(),
        'Exclude_Conference': set(),
        'Division': set(),
        'Exclude_Division': set(),
        'TeamName': set(),
        'Exclude_TeamName': set(),
        'Position': set(),
        'Exclude_Position': set(),
        'Height': [],
        'Age': [],
        'Jersey': []
    }


def process_guess(player, difference, filters):
    # Extract player attributes
    guessed_player = {
        'Conference': player.get('conference'),
        'Division': player.get('division'),
        'TeamName': player.get('teamname'),
        'Position': player.get('position'),
        'Height': player.get('height'),
        'Age': player.get('age'),
        'Jersey': int(player.get('number')) if player.get('number') else None
    }

    print(" ------------- ", difference)

    # Process categorical attributes
    process_categorical_attribute('Conference', difference.get(
        'conference'), guessed_player['Conference'], filters)
    process_categorical_attribute('Division', difference.get(
        'division'), guessed_player['Division'], filters)
    process_categorical_attribute('TeamName', difference.get(
        'team'), guessed_player['TeamName'], filters)
    process_categorical_attribute('Position', difference.get(
        'position'), guessed_player['Position'], filters)

    # Process numerical attributes
    process_numerical_attribute('Height', difference.get(
        'height'), guessed_player['Height'], filters)
    process_numerical_attribute('Age', difference.get(
        'age'), guessed_player['Age'], filters)
    process_numerical_attribute('Jersey', difference.get(
        'number'), guessed_player['Jersey'], filters)


def process_categorical_attribute(attr_name, difference_value, guessed_value, filters):
    if not guessed_value:
        return

    if difference_value == 'equal':
        filters[attr_name].add(guessed_value)
    # elif difference_value == 'far' or difference_value == "higherFar":
    elif difference_value == 'far':
        exclude_key = f'Exclude_{attr_name}'
        print(exclude_key)
        filters[exclude_key].add(guessed_value)


def process_numerical_attribute(attr_name, difference_value, guessed_value, filters):
    if guessed_value is None:
        return
    print(" ++++++++++", difference_value)

    if difference_value == 'higherFar':
        filters[attr_name].append(('<', guessed_value-3))
    elif difference_value == 'higherClose':
        filters[attr_name].append(('<', guessed_value))
    elif difference_value == 'equal':
        filters[attr_name].append(('==', guessed_value))
    elif difference_value == 'lowerClose':
        filters[attr_name].append(('>', guessed_value))
    elif difference_value == 'lowerFar':
        filters[attr_name].append(('>', guessed_value+3))


def apply_filters(players_df, filters):
    filtered_df = players_df.copy()

    # Apply categorical filters
    for attr in ['Conference', 'Division', 'TeamName', 'Position']:
        include_values = filters[attr]
        exclude_values = filters.get(f'Exclude_{attr}', set())

        if include_values:
            filtered_df = filtered_df[filtered_df[attr].isin(include_values)]
        if exclude_values:
            filtered_df = filtered_df[~filtered_df[attr].isin(exclude_values)]

    # Apply numerical filters
    for attr in ['Height', 'Age', 'Jersey']:
        for op, value in filters[attr]:
            if op == '>':
                filtered_df = filtered_df[filtered_df[attr] > value]
            elif op == '<':
                filtered_df = filtered_df[filtered_df[attr] < value]
            elif op == '==':
                filtered_df = filtered_df[filtered_df[attr] == value]

    return filtered_df


def exclude_previous_guesses(players_df, guesses):
    guessed_player_ids = [guess['player']['id']
                          for guess in guesses if 'player' in guess and 'id' in guess['player']]
    return players_df[~players_df['PlayerID'].isin(guessed_player_ids)]


if __name__ == "__main__":
    app.run(debug=True)

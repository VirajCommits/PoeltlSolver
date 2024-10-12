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


@app.route('/guess', methods=['POST'])
def guess():
    print("Hitting endpoint!")
    data = request.get_json()

    # Get the cumulative filters from the request, or initialize if not provided
    cumulative_filters = data.get('cumulative_filters', None)
    if cumulative_filters is None:
        cumulative_filters = {
            'Conference': set(),
            'Division': set(),
            'Team': set(),
            'Position': set(),
            'Height': [],
            'Age': [],
            'Jersey': []
        }
    else:
        # Convert lists back to sets for 'Conference', 'Division', 'Team', 'Position'
        for key in ['Conference', 'Division', 'Team', 'Position']:
            cumulative_filters[key] = set(cumulative_filters.get(key, []))
        # For 'Height', 'Age', 'Jersey', keep as lists
        for key in ['Height', 'Age', 'Jersey']:
            cumulative_filters[key] = cumulative_filters.get(key, [])

    guess_name = data.get('guess')
    feedback = data.get('feedback', {})

    if not guess_name:
        return jsonify({'error': 'Guess name is required'}), 400

    # Check if the player exists
    if guess_name not in players['Name'].values:
        return jsonify({'error': 'Player not found'}), 400

    # Get the guessed player data
    guess = players[players['Name'] == guess_name].iloc[0]

    # Process the feedback to update cumulative_filters
    conference_input = feedback.get('conference_input', 'n').strip().lower()
    if conference_input == 'y':
        cumulative_filters['Conference'].add(guess['Conference'])
    else:
        cumulative_filters['Conference'].add(f"not_{guess['Conference']}")

    division_input = feedback.get('division_input', 'n').strip().lower()
    if division_input == 'y':
        cumulative_filters['Division'].add(guess['Division'])
    else:
        cumulative_filters['Division'].add(f"not_{guess['Division']}")

    team_input = feedback.get('team_input', 'n').strip().lower()
    if team_input == 'y':
        cumulative_filters['Team'].add(guess['Team'])
    else:
        cumulative_filters['Team'].add(f"not_{guess['Team']}")

    position_hint = feedback.get('position_hint', '').strip()
    if position_hint:
        cumulative_filters['Position'].add(position_hint)

    height_comparison = feedback.get('height_comparison', '').strip().lower()
    if height_comparison in ["bigger", "smaller"]:
        cumulative_filters['Height'].append(
            (height_comparison, int(guess['Height'])))

    age_comparison = feedback.get('age_comparison', '').strip().lower()
    if age_comparison in ["older", "younger"]:
        cumulative_filters['Age'].append((age_comparison, int(guess['Age'])))

    jersey_comparison = feedback.get('jersey_comparison', '').strip().lower()
    if jersey_comparison in ["bigger", "smaller"]:
        cumulative_filters['Jersey'].append(
            (jersey_comparison, int(guess['Jersey'])))

    # Apply the cumulative filters to the players DataFrame
    filtered_players = players.copy()

    # Apply cumulative Conference filters
    for conf in cumulative_filters['Conference']:
        if conf.startswith("not_"):
            filtered_players = filtered_players[filtered_players['Conference'] != conf.replace(
                "not_", "")]
        else:
            filtered_players = filtered_players[filtered_players['Conference'] == conf]

    # Apply cumulative Division filters
    for div in cumulative_filters['Division']:
        if div.startswith("not_"):
            filtered_players = filtered_players[filtered_players['Division'] != div.replace(
                "not_", "")]
        else:
            filtered_players = filtered_players[filtered_players['Division'] == div]

    # Apply cumulative Team filters
    for team in cumulative_filters['Team']:
        if team.startswith("not_"):
            filtered_players = filtered_players[filtered_players['Team'] != team.replace(
                "not_", "")]
        else:
            filtered_players = filtered_players[filtered_players['Team'] == team]

    # Apply Position filters
    if cumulative_filters['Position']:
        filtered_players = filtered_players[filtered_players['PositionCategory'].isin(
            cumulative_filters['Position'])]

    # Apply Height comparisons
    for comp, value in cumulative_filters['Height']:
        if comp == "bigger":
            filtered_players = filtered_players[filtered_players['Height'] > value]
        elif comp == "smaller":
            filtered_players = filtered_players[filtered_players['Height'] < value]

    # Apply Age comparisons
    for comp, value in cumulative_filters['Age']:
        if comp == "older":
            filtered_players = filtered_players[filtered_players['Age'] > value]
        elif comp == "younger":
            filtered_players = filtered_players[filtered_players['Age'] < value]

    # Apply Jersey comparisons
    for comp, value in cumulative_filters['Jersey']:
        if comp == "bigger":
            filtered_players = filtered_players[filtered_players['Jersey'] > value]
        elif comp == "smaller":
            filtered_players = filtered_players[filtered_players['Jersey'] < value]

    # Prepare the filtered players to return
    filtered_players_json = filtered_players[['Name', 'Team', 'Conference', 'Division', 'PositionCategory', 'Height', 'Age', 'Jersey']].astype(
        object).where(pd.notnull(filtered_players), None).to_dict(orient='records')

    # Convert sets in cumulative_filters to lists for JSON serialization
    cumulative_filters_serializable = {key: list(value) if isinstance(
        value, set) else value for key, value in cumulative_filters.items()}

    # Return the updated cumulative_filters and filtered_players
    response = {
        'cumulative_filters': cumulative_filters_serializable,
        'filtered_players': filtered_players_json
    }

    print("This is the response I am getting:", response)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)

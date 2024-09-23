import requests
import pandas as pd
from datetime import datetime
import requests

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


def filter_players(players_df, team_hint=None, position_hint=None):
    """Filter players based on team and position hints."""
    filtered = players_df.copy()
    if team_hint:
        filtered = filtered[filtered['Team'] == team_hint]
    if position_hint:
        filtered = filtered[filtered['PositionCategory'] == position_hint]
    return filtered


def filter_comparison(filtered_players, attribute, guess_value, comparison):
    """Filter players based on comparison of an attribute."""
    if comparison in ["bigger", "older"]:
        return filtered_players[filtered_players[attribute] > guess_value]
    elif comparison in ["smaller", "younger"]:
        return filtered_players[filtered_players[attribute] < guess_value]
    return filtered_players


def make_guess(players_df):
    """Interactive function to make a guess and filter players based on feedback."""
    # Initialize cumulative filters
    cumulative_filters = {
        'Conference': set(),
        'Division': set(),
        'Team': set(),
        'Position': set(),
        'Height': [],
        'Age': [],
        'Jersey': []
    }

    filtered_players = players_df.copy()

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    while True:
        player_name = input("Enter your guess (player's name): ").strip()

        if player_name not in players_df['Name'].values:
            print("Player not found! Try again.")
            continue

        # Get the guessed player data
        guess = players_df[players_df['Name'] == player_name].iloc[0]

        # Ask for feedback
        conference_input = input(
            "Is the conference correct? (y/n): ").strip().lower()
        division_input = input(
            "Is the division correct? (y/n): ").strip().lower()
        team_input = input("Is the team correct? (y/n): ").strip().lower()
        position_hint = input(
            "What is the correct position, if known? (leave blank if unsure): ").strip()
        height_comparison = input(
            "Is the player's height bigger or smaller than the guess? (bigger/smaller): ").strip().lower()
        age_comparison = input(
            "Is the player's age older or younger than the guess? (older/younger): ").strip().lower()
        jersey_comparison = input(
            "Is the player's jersey number bigger or smaller than the guess? (bigger/smaller): ").strip().lower()

        # Update cumulative filters based on feedback
        if conference_input == 'y':
            cumulative_filters['Conference'].add(guess['Conference'])
        else:
            cumulative_filters['Conference'].add(f"not_{guess['Conference']}")

        if division_input == 'y':
            cumulative_filters['Division'].add(guess['Division'])
        else:
            cumulative_filters['Division'].add(f"not_{guess['Division']}")

        if team_input == 'y':
            cumulative_filters['Team'].add(guess['Team'])
        else:
            cumulative_filters['Team'].add(f"not_{guess['Team']}")

        if position_hint:
            cumulative_filters['Position'].add(position_hint)

        # Apply height, age, and jersey comparisons
        if height_comparison in ["bigger", "smaller"]:
            cumulative_filters['Height'].append(
                (height_comparison, guess['Height']))

        if age_comparison in ["older", "younger"]:
            cumulative_filters['Age'].append((age_comparison, guess['Age']))

        if jersey_comparison in ["bigger", "smaller"]:
            cumulative_filters['Jersey'].append(
                (jersey_comparison, guess['Jersey']))

        # Start with the original DataFrame
        filtered_players = players_df.copy()

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
            filtered_players = filtered_players[filtered_players['PositionCategory'] == list(
                cumulative_filters['Position'])[0]]

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

        # Display the filtered player suggestions
        print("\nFiltered player suggestions:")
        print(filtered_players[['Name', 'Team', 'Conference',
              'Division', 'PositionCategory', 'Height', 'Age', 'Jersey']])


def main():
    """Main function to execute the NBA player guessing game."""
    # Fetch data from the API
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    # Parse the response data
    data = response.json()

    # Convert to DataFrame
    players = pd.DataFrame(data)

    # Calculate age for each player
    players['Age'] = players['BirthDate'].apply(calculate_age)

    # Map Conference and Division based on team
    players['Conference'] = players['Team'].map(
        lambda x: team_info.get(x, {}).get('Conference', 'Unknown')
    )
    players['Division'] = players['Team'].map(
        lambda x: team_info.get(x, {}).get('Division', 'Unknown')
    )

    # Combine first and last names into 'Name'
    players['Name'] = players['FirstName'] + ' ' + players['LastName']

    # Ensure numeric types for comparisons
    players['Height'] = pd.to_numeric(players['Height'], errors='coerce')
    players['Age'] = pd.to_numeric(players['Age'], errors='coerce')
    players['Jersey'] = pd.to_numeric(players['Jersey'], errors='coerce')

    # Run the guessing function
    make_guess(players)


if __name__ == "__main__":
    main()

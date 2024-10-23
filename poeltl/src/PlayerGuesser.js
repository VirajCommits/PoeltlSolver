import React , {useState} from 'react'

function PlayerGuesser() {



    const [suggestions, setSuggestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearchPlayers = async () => {
      console.log("HANDLING SEARCHING OF PLAYERS ")
        setLoading(true);
        setError(null);

        try{
            const currentPlayerStats = {
                    guess: "Kyrie Irving",
                    feedback: {
                      conference_input: "n",
                      division_input: "n",
                      team_input: "n",
                      position_hint: "G",
                      height_comparison: "bigger",
                      age_comparison: "younger",
                      jersey_comparison: "bigger"
                    },
                    cumulative_filters: {
                      Conference: [],
                      Division: [],
                      Team: [],
                      Position: [],
                      Height: [],
                      Age: [],
                      Jersey: []
                },
              };

            const response = await fetch('http://127.0.0.1:5000/guess', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(currentPlayerStats),
                });
            
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                  }

                const data = await response.json();

                // Update the suggestions
                setSuggestions(data.filtered_players);
                } catch (error) {
                  console.error('Error fetching suggestions:', error);
                } finally {
                  setLoading(false);
                }
        
        

    };
  return (
    <div style = {{padding:'20px'}} >
        <h1>Welcome to Poeltl</h1>
        <button onClick={handleSearchPlayers} >Search Players</button>

        {loading &&  <p>Loading guesses...</p>}

        {!loading && suggestions.length > 0 && (
            <div
                style={{
                marginTop: '20px',
                maxHeight: '400px',
                overflowY: 'scroll',
                border: '1px solid #ccc',
                padding: '10px',
                }}
            >

                {/* Traverse the suggestions loop and get all possible guesses and print them */}
                {suggestions.map((player, index) => (
                <div
                key={index}
                style={{
                    marginBottom: '10px',
                    borderBottom: '1px solid #eaeaea',
                    paddingBottom: '10px',
                }}
                >
                <strong>{player.Name}</strong>
                <p>
                    Team: {player.Team} <br />
                    Conference: {player.Conference} <br />
                    Division: {player.Division} <br />
                    Position: {player.PositionCategory} <br />
                    Height: {player.Height} <br />
                    Age: {player.Age} <br />
                    Jersey: {player.Jersey}
                </p>
                </div>
            ))}
            </div>
        )}
        {/* No guesses found */}

        {!loading && !error && suggestions.length === 0 && (
        <p>No Player guesses available. Click "Search Players" to get started.</p>
      )}
    </div>
  )
}

export default PlayerGuesser

import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';

// Styled Components

const Container = styled.div`
  padding: 20px;
  background: linear-gradient(135deg, #f0f2f5, #cfd9df);
  min-width: 300px;
  max-width: 400px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25);
  font-family: 'Roboto', sans-serif;
`;

const Title = styled.h1`
  text-align: center;
  color: #333;
  margin-bottom: 20px;
`;

const Button = styled.button`
  background-color: #4a90e2;
  color: #fff;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #357ab8;
  }

  &:disabled {
    background-color: #a0c4e8;
    cursor: not-allowed;
  }
`;

const Loader = styled.div`
  margin: 20px auto;
  border: 6px solid #f3f3f3;
  border-top: 6px solid #4a90e2;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const SuggestionsContainer = styled.div`
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 10px;
`;

const PlayerCard = styled.div`
  margin-bottom: 15px;
  padding: 15px;
  border-bottom: 1px solid #eaeaea;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #f9f9f9;
  }
`;

const PlayerName = styled.strong`
  display: block;
  font-size: 18px;
  color: #333;
  margin-bottom: 8px;
`;

const PlayerDetails = styled.p`
  margin: 0;
  color: #555;
  line-height: 1.5;
`;

const Message = styled.p`
  text-align: center;
  color: #666;
  margin-top: 20px;
`;

const ErrorMessage = styled.p`
  text-align: center;
  color: #ff4d4f;
  margin-top: 20px;
`;

// Main Component

function PlayerGuesser() {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearchPlayers = async () => {
    setLoading(true);
    setError(null);

    try {
      // Fetch data from the Flask '/sync' endpoint
      const syncResponse = await fetch('http://127.0.0.1:5000/sync');
      console.log(syncResponse);

      if (!syncResponse.ok) {
        throw new Error(`Sync request failed with status ${syncResponse.status}`);
      }

      const currentPlayerStats = await syncResponse.json();

      // Send the guesses to the Flask '/guess' endpoint
      const response = await fetch('http://127.0.0.1:5000/guess', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(currentPlayerStats),
      });

      if (!response.ok) {
        throw new Error(`Guess request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Update the suggestions
      setSuggestions(data.filtered_players);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      setError(`Failed to fetch player suggestions: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Title>Welcome to Poeltl</Title>
      <Button onClick={handleSearchPlayers} disabled={loading}>
        {loading ? 'Searching...' : 'Search Players'}
      </Button>

      {loading && <Loader />}

      {!loading && suggestions.length > 0 && (
        <SuggestionsContainer>
          {suggestions.map((player, index) => (
            <PlayerCard key={index}>
              <PlayerName>{player.Name}</PlayerName>
              <PlayerDetails>
                <strong>Team:</strong> {player.Team} <br />
                <strong>Conference:</strong> {player.Conference} <br />
                <strong>Division:</strong> {player.Division} <br />
                <strong>Position:</strong> {player.Position} <br />
                <strong>Height:</strong> {player.Height} <br />
                <strong>Age:</strong> {player.Age} <br />
                <strong>Jersey:</strong> {player.Jersey}
              </PlayerDetails>
            </PlayerCard>
          ))}
        </SuggestionsContainer>
      )}

      {!loading && !error && suggestions.length === 0 && (
        <Message>No Player guesses available. Click "Search Players" to get started.</Message>
      )}

      {error && <ErrorMessage>{error}</ErrorMessage>}
    </Container>
  );
}

export default PlayerGuesser;

import playerDict from './playerDictionary.json'; 

// Assume you have a list or a way to get previous guesses
let previousGuesses = []; // This should be maintained across guesses

// Load playerDict.json (you might fetch this from your server)

// Function to get the player's ID from the name
function getPlayerId(playerName) {
  return playerDict[playerName];
}

// Function to send the guess to the backend
async function sendGuessToBackend(playerName) {
  const playerId = getPlayerId(playerName);
  if (!playerId) {
    console.error("Player not found");
    return;
  }

  try {
    // Fetch data from Poeltl API
    const poeltlResponse = await fetch(`https://poeltl.nbpa.com/api/guess?id=${playerId}`);
    const poeltlData = await poeltlResponse.json();

    // Prepare data to send to your backend
    const dataToBackend = {
      apiResponse: poeltlData,
      previousGuesses: previousGuesses
    };

    // Send data to your backend
    const backendResponse = await fetch('http://127.0.0.1:5000/guess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dataToBackend)
    });

    const result = await backendResponse.json();

    // Update the previous guesses
    previousGuesses.push(playerName);

    // Display possible guesses to the user
    displayPossibleGuesses(result.possibleGuesses);
  } catch (error) {
    console.error('Error:', error);
  }
}

// Function to display possible guesses
function displayPossibleGuesses(guesses) {
  // Implement this function to update your UI
  console.log('Possible Guesses:', guesses);
}

// Example usage
sendGuessToBackend('Kyrie Irving');

// Required modules
const axios = require('axios');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

// URL of the page containing the HTML
const url = 'https://poeltl.nbpa.com/';
CORS(app, resources={r,"/guess": {"origins": "http://localhost:3000"}})

// Function to extract the most recent guessed player's name
async function getMostRecentGuess(url) {
  try {
    // Fetch the HTML content from the URL
    const response = await axios.get(url);
    const htmlContent = response.data;

    // Parse the HTML content using JSDOM
    const dom = new JSDOM(htmlContent);
    const document = dom.window.document;

    // Select all guess rows
    const guesses = document.querySelectorAll('.guess');

    // Iterate over the guesses to find the most recent one with data
    for (let i = 0; i < guesses.length; i++) {
      const guess = guesses[i];
      const playerNameCell = guess.querySelector('.name span');
      if (playerNameCell && playerNameCell.textContent.trim() !== '') {
        const playerName = playerNameCell.textContent.trim();
        return playerName;
      }
    }
    return null;
  } catch (error) {
    console.error('Error fetching or parsing the page:', error);
  }
}

// Call the function and output the result
getMostRecentGuess(url).then((mostRecentGuessName) => {
  if (mostRecentGuessName) {
    console.log('Most recent guessed player:', mostRecentGuessName);
  } else {
    console.log('No guesses found.');
  }
});

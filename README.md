# PoeltlSolver

PoeltlSolver is an interactive browser extension designed for NBA enthusiasts who love to engage in player-guessing games. Whether you're playing solo or challenging friends, PoeltlSolver leverages real-time NBA data to provide accurate and exciting player suggestions based on your guesses. With a sleek React frontend and a robust Flask backend, this project offers a seamless and engaging user experience.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Frontend Details](#frontend-details)
- [Backend Details](#backend-details)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Interactive Player Guessing:** Make guesses based on player attributes and receive filtered suggestions.
- **Real-Time Data Integration:** Fetches active NBA player data from the SportsData API.
- **User-Friendly Interface:** Intuitive UI built with React for a smooth user experience.
- **Browser Extension:** Easily accessible as a Chrome extension, enhancing convenience.
- **Dynamic Filtering:** Apply multiple filters based on conference, division, team, position, height, age, and jersey number.
- **Comprehensive Logging:** Detailed console logs for monitoring and debugging.

## Technology Stack

- **Frontend:**
  - React
  - Styled Components
  - Axios
  - Chrome Extensions API

- **Backend:**
  - Flask
  - Pandas
  - Requests
  - Flask-CORS

- **Others:**
  - Docker (optional for containerization)
  - Git & GitHub for version control

## Getting Started

Follow these instructions to set up the project locally on your machine for development and testing purposes.

### Prerequisites

- **Node.js** and **npm** installed on your machine. [Download here](https://nodejs.org/)
- **Python 3.7+** installed. [Download here](https://www.python.org/downloads/)
- **Git** installed. [Download here](https://git-scm.com/downloads/)
- **Chrome Browser** for testing the extension.

### Installation

#### Setup Backend (Flask API)

1. **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**

    Create a `.env` file in the `backend` directory and add your SportsData API key:

    ```env
    API_KEY=your_sportsdata_api_key
    SECRET_KEY=your_flask_secret_key
    ```

5. **Run the Flask Server:**

    ```bash
    python app.py
    ```

    The server should be running at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

#### Setup Frontend (React App)

1. **Open a new terminal window/tab.**

2. **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

3. **Install dependencies:**

    ```bash
    npm install
    ```

4. **Build the React App:**

    ```bash
    npm run build
    ```

    This will generate a `build` folder with the production-ready files.

#### Setup Chrome Extension

1. **Open Chrome and navigate to** [chrome://extensions/](chrome://extensions/).

2. **Enable Developer mode** by toggling the switch on the top right.

3. **Click on** **Load unpacked** **and select the** `frontend/build` **directory.**

4. The PoeltlSolver extension should now appear in your Chrome toolbar.

## Usage

1. **Launch the Extension:**

    - Click on the PoeltlSolver icon in the Chrome toolbar to open the popup.

2. **Search Players:**

    - Click the **Search Players** button to fetch and display player suggestions based on your current guesses.

3. **Interact with Suggestions:**

    - View detailed player information including team, conference, division, position, height, age, and jersey number.
    - Use this information to refine your next guess and continue the game.

4. **Monitor Logs:**

    - Open the Chrome Developer Tools within the extension popup (Right-click > Inspect) to view detailed logs for debugging and monitoring.

## API Endpoints

### `/sync` [GET]

Fetches data from an external API using predefined cookies and headers.

- **URL:** `http://127.0.0.1:5000/sync`
- **Method:** GET
- **Headers:**
  - `User-Agent`: Custom user agent string.
  - `Accept`: `application/json`
  - `Cookie`: Manually set cookie string.
- **Response:**
  - **Success:** JSON data from the external API.
  - **Error:** JSON with error message and status code 500.

### `/guess` [POST]

Processes player guesses and returns filtered player suggestions based on the guesses.

- **URL:** `http://127.0.0.1:5000/guess`
- **Method:** POST
- **Headers:**
  - `Content-Type`: `application/json`
- **Body:**

    ```json
    {
      "guesses": [
        {
          "player": {
            "id": 123,
            "conference": "Eastern",
            "division": "Atlantic",
            "teamcode": "BOS",
            "position": "SG",
            "height": 6.5,
            "age": 28,
            "number": 30
          },
          "difference": {
            "conference": "equal",
            "division": "equal",
            "team": "equal",
            "position": "equal",
            "height": "equal",
            "age": "equal",
            "number": "equal"
          }
        }
      ]
    }
    ```

- **Response:**
  - **Success:** JSON with `filtered_players` array.
  - **Error:** JSON with error message and appropriate status code.

## Frontend Details

The frontend is built using React and styled-components to create a modern and responsive user interface. Key components include:

### PlayerGuesser.js:

- **Handles fetching player suggestions from the backend.**
- **Manages UI states such as loading, error, and displaying suggestions.**
- **Styled with enhanced aesthetics for an engaging user experience.**

### App.js:

- **Serves as the main entry point, rendering the** `PlayerGuesser` **component.**

### Styling Enhancements

- **Responsive Design:** Ensures the extension looks great on various popup sizes.
- **Interactive Elements:** Buttons and player cards have hover effects and transitions.
- **Loader Animation:** Provides visual feedback during data fetching.
- **Dark Mode (Optional):** Toggle between light and dark themes for user preference.

## Backend Details

The backend is a Flask application that serves as an API to fetch and process NBA player data. Key functionalities include:

### Data Fetching:

- **Retrieves active NBA player data from the SportsData API.**
- **Processes and enriches data with additional attributes like age, conference, and division.**

### Endpoints:

- **`/sync`:** Fetches data from an external API using specific cookies and headers.
- **`/guess`:** Processes user guesses to filter and return relevant player suggestions.

### Data Processing:

- **Utilizes Pandas for data manipulation and filtering based on user inputs.**
- **Implements comprehensive logging for monitoring and debugging.**

### Logging Enhancements

- **Detailed print statements added throughout the application to track:**
  - **API requests and responses.**
  - **Data processing steps.**
  - **Errors and exceptions.**

### CORS Configuration

- **Configured with** `Flask-CORS` **to allow cross-origin requests from the frontend extension.**
- **Supports credentials to handle secure communications.**

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create your Feature Branch**

    ```bash
    git checkout -b feature/AmazingFeature
    ```

3. **Commit your Changes**

    ```bash
    git commit -m 'Add some AmazingFeature'
    ```

4. **Push to the Branch**

    ```bash
    git push origin feature/AmazingFeature
    ```

5. **Open a Pull Request**

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

*This project is developed by Viraj Murab as part of his portfolio to showcase machine learning, web development, and full-stack engineering skills.*

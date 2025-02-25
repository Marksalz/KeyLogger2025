# KeyLogger Project

This project is a keylogger application that captures keystrokes and sends the data to a backend server for storage and retrieval.
The backend server is built using Flask and provides several API endpoints to interact with the logged data.

## Project Structure

- `backend/`: Contains the Flask application.
  - `app.py`: Main application file for the Flask server.
- `KeyLoggerAgent/`: Contains the keylogger agent.
  - `keyLoggerManager.py`: Manages the keylogger service and data transmission.
  - `keyLoggerService.py`: Implements the keylogger functionality.
  - `encryptor.py`: Provides encryption and decryption for the logged data.
  - `fileWriter.py`: Writes logged data to a file.
  - `networkWriter.py`: Sends logged data to the backend server.
  - `buffer.py`: Implements a buffer for storing logged data.
  - `interfaceManager.py`: Manages the user interface for the keylogger.
- `frontend/`: Contains the frontend application.
  - `index.html`: Main page to display the list of machines.
  - `login.html`: Login page to access the keylogger data.
  - `machine.html`: Page to display logs for a specific machine.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Requirements

- Python 3.x
- Flask
- Flask-CORS
- pynput
- getmac
- requests

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/keylogger-project.git
   cd keylogger-project
   
## Usage

### Running the Backend Server

1. Navigate to the `backend` directory:
   ```sh
   cd backend
   
2. Run the Flask application:
   ```sh
    python app.py
   
### Running the KeyLogger Agent
1. Navigate to the `KeyLoggerAgent` directory:
    ```sh
   cd KeyLoggerAgent
   
2. Run the keylogger manager:
    ```sh
    python keyLoggerManager.py
   
### Running the Frontend Application
1. Navigate to the `frontend` directory:
    ```sh
   cd frontend
   
2. Open the `login.html` file in a web browser:
   ```sh
   start login.html    
    
   

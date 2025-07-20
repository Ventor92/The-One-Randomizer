# Project Title: The One Randomizer

## Description
The One Randomizer is a FastAPI application designed for managing dice rolls in tabletop role-playing games. It provides an API for recording and retrieving roll history, as well as WebSocket support for real-time interactions.

## Project Structure
```
web_app
├── backend
│   ├── main.py               # Entry point of the FastAPI application
│   ├── routes
│   │   ├── rollHistory.py    # Endpoints for adding and retrieving roll history
│   │   └── websocket.py       # WebSocket connection handling
│   └── models
│       └── __init__.py       # Placeholder for data models
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd web_app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Activate Virtual Environment
   ```
   source .venv/Scripts/activate
   ```
   
1. Start the FastAPI application:
   ```
   uvicorn main_be_app:app --reload
   ```
2. Start the database MySQL:
   ``` 
   net start "MySQL80"
   ```

3. Access the API documentation at `http://127.0.0.1:8000/docs`.

## WebSocket Support
The application includes WebSocket support for real-time communication. The WebSocket routes are defined in `backend/routes/websocket.py`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.
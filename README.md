
# Chatbot Web Application

This is a Flask-based chatbot application that allows users to communicate with an AI chatbot. The user interface supports customization by allowing users to change their icons during conversation. The app is deployed on AWS, making it accessible from anywhere.

## Features
- **User-friendly Interface:** A simple and intuitive layout using HTML, CSS, and JavaScript.
- **Dynamic User Icons:** Users can change their icons while chatting.
- **AI-Powered Responses:** Integrated with OpenAI for generating conversational responses.
- **Database Integration:** Uses MongoDB to store and retrieve conversation data.

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MongoDB
- **Deployment:** AWS EC2

## Prerequisites
To run this project locally, you'll need:
- Python 3.6 or later
- Flask
- OpenAI API key
- MongoDB Atlas account and connection string

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:** Create a `.env` file in the root directory with your keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   MONGODB_URI=your_mongodb_connection_string
   ```

5. **Run the application:**
   ```bash
   flask run
   ```

## Deployment
This project is deployed on AWS EC2. Follow these steps to deploy:
1. Set up an EC2 instance.
2. SSH into the instance and configure it for Flask and MongoDB connectivity.
3. Copy your application files to the EC2 instance.
4. Install dependencies and start the Flask app on the server.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Duke - Relationship Mediation App

A couples therapy AI application that helps partners communicate more effectively with turn-based mediation.

## Setup Instructions

### 1. MongoDB Setup (Ubuntu WSL)
```bash
# Import MongoDB public GPG key
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor

# Create list file for MongoDB
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Reload package database
sudo apt-get update

# Install MongoDB packages
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
# OR
sudo service mongod start

# Check MongoDB status
sudo systemctl status mongod
# OR
sudo service mongod status
```

### 2. Python Virtual Environment Setup

#### Creating a virtual environment
```bash
# Navigate to your project directory
cd ~/PyCharm/Duke/duke-ai

# Create virtual environment (use python3 explicitly on Ubuntu)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### Installing dependencies
```bash
# With virtual environment activated
pip install fastapi uvicorn motor requests

# Or if you have a requirements.txt file
pip install -r requirements.txt

# Generate requirements.txt for future use
pip freeze > requirements.txt
```

#### PyCharm Configuration
1. Open PyCharm settings (File > Settings)
2. Navigate to Project: Duke > Python Interpreter
3. Click the gear icon and select "Add"
4. Choose "WSL" and navigate to your venv Python: `/home/gav/PyCharm/Duke/duke-ai/venv/bin/python3`
5. Click OK/Apply

### 3. Ollama Setup
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Create the Duke model
ollama create duke -f Modelfile

# Verify the model is available
ollama list
```

### 4. Running the Application
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Make sure MongoDB is running
sudo service mongod status

# Make sure Ollama is running
ps aux | grep ollama
# If not running: ollama serve

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
Interactive documentation is at `http://localhost:8000/docs`

### 5. Testing the Application

1. Create a session:
```bash
curl -X 'POST' \
  'http://localhost:8000/sessions/create' \
  -H 'Content-Type: application/json' \
  -d '{
    "creator_name": "person1",
    "partner_name": "person2"
}'
```

2. Join the session:
```bash
curl -X 'POST' \
  'http://localhost:8000/sessions/join/{invite_code}' \
  -H 'Content-Type: application/json' \
  -d '{
    "participant_name": "person2"
}'
```

3. Send messages:
```bash
curl -X 'POST' \
  'http://localhost:8000/sessions/{session_id}/message' \
  -H 'Content-Type: application/json' \
  -d '{
    "content": "I feel overwhelmed because I need more emotional support",
    "sender_name": "person1"
}'
```

## Troubleshooting

### Virtual Environment Issues
If PyCharm doesn't recognize installed packages:
1. Verify your virtualenv is activated when installing packages
2. Check that PyCharm is using the correct Python interpreter
3. Try reinstalling packages within PyCharm's terminal

### MongoDB Connection Issues
If MongoDB fails to start:
```bash
# Check logs
sudo cat /var/log/mongodb/mongod.log

# Verify the service name
systemctl list-unit-files | grep mongo

# Check if it's running
ps aux | grep mongod
```

### Ollama Issues
If AI mediation fails:
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama if needed
ollama serve

# Verify model exists
ollama list

# Test the model directly
ollama run duke "Test message"
```

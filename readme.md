# Duke 

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
sudo service mongod start

# Check MongoDB status
sudo service mongod status
```

### 2. Python Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install fastapi uvicorn motor
```

### 3. Running the Application
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
Interactive documentation is at `http://localhost:8000/docs`

### 4. Testing MongoDB Connection
Use MongoDB shell to check data:
```bash
# Start MongoDB shell
mongosh

# Show databases
show dbs

# Use our database
use duke_db

# Show collections
show collections

# View messages
db.messages.find().pretty()
```
# FriendZone2
This is the updated version of FriendZone. Serves as the Backend API to Friendzone_front_end

~~~~
FriendZone2
├── FriendZone
│   └── __pycache__
├── api
│   ├── __pycache__
│   └── migrations
│       └── __pycache__
├── staticfiles
└── venv
~~~~

### Step 1. Set up virtual environment (if you don't have a virtual environment)
  Run commands to create virtual environment
~~~~
  virtualenv venv --python=python3
 ~~~~
  Run command to activate virtual environment
  ~~~~
  source venv/bin/activate
  ~~~~

### Step 2. Install dependencies:
  Run command in the root folder
  ~~~~
  pip install requirements.txt
  ~~~~
  
### Step 3. Handle migrations:
  Run commands
  ~~~~
  python3 manage.py makemigrations
  python3 manage.py migrate
  ~~~~

### Step 4. Runserver on localhost
  Run command in the root folder
  ~~~~
  python3 manage.py runserver
  ~~~~

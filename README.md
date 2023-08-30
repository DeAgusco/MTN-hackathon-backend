# MTN-hackathon-backend
 This repository is the Python Backend for MTN hackathon 2023, team `kobbyisreal_66fb`
 
# Running This Repository
- Create a virtual environment using `python -m venv venv` on both Mac and windows.
- On windows, run `.\venv\Scripts\activate` ro activate your virtual environment.
- On Unix or MacOS, using the bash shell: `source /path/to/venv/bin/activate`.
- On Unix or MacOS, using the csh shell: `source /path/to/venv/bin/activate.csh`.
- On Unix or MacOS, using the fish shell: `source /path/to/venv/bin/activate.fish`.
- Run `pip install -r requirements.txt` to install all dependencies needed for this build.
- Run `python manage.py migrate` to activate the database.
- Run `python manage.py runserver` to start the local server.
- This build requires a redist server to run perfectly and send automatic notifications.
- Run these line by line on windows bash or Ubuntu:
- `sudo apt-add-repository ppa:redislabs/redis`.
- `sudo apt-get update`.
- `sudo apt-get upgrade`.
- `sudo apt-get install redis-server`.
- On Mac, Run these line by line:
- `brew tap redis-stack/redis-stack`.
- `brew install --cask redis-stack`.
- `redis-stack-server`.
- Happy Coding.

# work-log-updater
1. `pip install -r requirements.txt`
2. generate your own credentials file by following instructions on [this link](https://developers.google.com/sheets/quickstart/python)
3. fill in **config_template.json** accordingly, change the filename to **config.json**

possible improvements:
- more parsing ought to be done with parser.py
- filter by date range

other notes:
- date range for commits can be changed in msg.sh, see [git log](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History), under *Limiting Log Output*

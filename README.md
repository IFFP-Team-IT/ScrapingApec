https://www.ionos.fr/digitalguide/sites-internet/developpement-web/fichier-readme/

To launch the program on the server, you must first place yourself in a virtual environment as follows:
1- python3 -m venv my_env(here venv otherwise do
mkdir environments
cd environments
then python3 -m venv my_env(in this example environments)
)
- source my_env/bin/activate
2- Then install all the neccessaire package:
pip install -r requirements.txt


3- Run the script with the following command:
python Extrapec.py

NB: if python does not exist do as follows:
sudo apt update
sudo apt -y upgrade
python3 -V or python --version

If pip(allows you to install python modules) does not exist
sudo apt install -y python3-pip

To install a package
pip3 install package_name(Ex:pip install pandas)

In a virtual environment pip3 <=> pip and python3 <=> python


Find where to drop chromedriver:
Just run this little script for it to show you the path
import os
import sys
print(os.path.dirname(sys.executable))


How the program is running *********

When the program launches, it retrieves the page number registered in the program_data file (folder...)
Then it will create every day a file in apec_aaaammjj.xlsx format in the BDD folder and also created the hand sheets, skills, lang, trumps, nb_moments_cles. This file recovers all the items that the robot will scrape.

It checks whether it is allowed to use a proxy or not(Boolean variable useproxy created in scr_hlp and initialize in Extrapec.py)
Then loads the page to scrape while checking if an internet connection is active
and checks if the page has been loaded correctly. (load_page function and load_page_helper in class scr_hlp)

Opens a usernames.xlsx file containing the username and password to connect to the site.
It makes a connection to the site with the first user and moves to the next user when , when the latter has reached his vistelimit(registered in the variable visitlimits)

Then, it checks the number of candidates to scraper on a page and also checks if there are still pages to scraper (function scr_hlp.is_next_page_exists).

It retrieves the link to each profile (line 93 to 96 in Extrapec.py)

Before loading the page, it checks if the profile id already exists in the db, if so skip otherwise loads the page and retrieves everything.

It repeats the action until all users in the usernames.xlsx file have made their required number of visits. Knowing that each user pauses between each visit according to the variable retrieved in the Number of visits before the pause field of the Config file.xlsx

Before stopping the program it checks if all zipped files have been unzipped in the FILES folder and puts the number of user visits back to zero in the usernames file.xlsx.

NB: LOG, BDD and FILES folders are created automatically

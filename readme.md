# CryptoKatana2

Bootcamp Zero - IV Edition Final Project | KeepCoding

Classic Web Flask application: The project was created over several weeks on VCS, written in Python, using the Flask micro web framework.

* **Changelog 0.0.1**

- As of 13/08/2021, Werkzeug could not successfully import url_encode in version 2.0.1. Fixed by retrograding flask and werkzeug versions in requirements.txt (now versions 1.1.2 and 0.16.1, respectively).
- Cosmetic change in forms.py by correcting description of currency_to field.

# Installation Requirements

* **Create your virtual environment**

if you are running this package on a Mac:

<python(version)> -m venv </path/to/new/virtual/environment>

* **Activate the virtual environment**

. <virtual_environment_name>/bin/activate

* **Install requirements:**

pip install -r requirements.txt

* **Connect your API**

Using the following link, login (or create an account and select the 'basic' plan), and generate/copy your APIKEY:

https://pro.coinmarketcap.com/login/

Assign the variable my_api in the routes.py to your <APIKEY>.

* **Run the application** 

flask run

* **Suggestions/Comments**

-IT IS HIGHLY RECOMMENDED THAT THIS WEB APP IS VIEWED ON AN 18-INCH+ MONITOR. The CSS was modified and designed using a large external monitor, and so unfortunately the error messages appear halfway off the bottom of the screen. For best quality, use a large external monitor. I promise I will take CSS lessons in the future.

-Review the currencyvalues table in the movements.db file. If you wish to subtract or add to the total amount of Euros, which is defaulted to 10000, feel free.

-The username page is only used to personalize the error messages. Unfortunately, the code does not store names in the database and I do not know why. As it is not part of the project, I decided to stop wasting time on it. If you can figure out why it doesn't store data, please let me know. In the meantime, if you want personalized errors, you will have to go into the username table in movements.db and change the name value manually.

-Due to not wanting to rock the boat so late in the trip, I left the movements.db database as is. However, if I were to start again, I'd call it the "data.db" database. I will change this once the program has been evaluated.

# Developer

* **Trefor Meirion Jones**

GitHub: treformeirion(https://github.com/treformeirion)
website: treformeirion.com

# CryptoKatana2

Bootcamp Zero - IV Edition Final Project | KeepCoding

Classic Web Flask application: The project was created over several weeks on VCS, written in Python, using the Flask micro web framework.

# Installation Requirements

* **Activate the virtual environment**
```
. <virtual_environment_name>/bin/activate
```
* **Install requirements:**
```
pip install -r requirements.txt
```
* **Connect your API**

Using the following link, login (or create an account and select the 'basic' plan), and generate/copy your APIKEY:

https://pro.coinmarketcap.com/login/

Assign the variable API_KEY in the routes.py to your APIKEY.

* **Review the currencyvalues table in the movements.db file**

If you wish to subtract or add to the total amount of Euros, which is defaulted to 1000, feel free.

* **Run the application** 
```
flask run
```
# Insights
```
You cannot store a float value in a database because it will be transformed into binary and therefore become inaccurate and useless immediately upon storage.
```
You should definitely work on the code before the css.

# Developer

* **Trefor Meirion Jones**

GitHub: treformeirion(https://github.com/treformeirion)
website: treformeirion.com

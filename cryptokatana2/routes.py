from datetime import date
import time
from cryptokatana2 import app
from flask import render_template, request, redirect, url_for, flash, json, session
from cryptokatana2.forms import MovementsForm, NameForm
import sqlite3
import urllib

# Access the api by providing an api key.

my_api = '65bcaa07-93bc-428d-a65e-6d2dbe67eb79'

# Returns an accurate calculation of the quantity you'll be getting for the unit price of the currency the client will be converting to

def calculateKatana(u1, cf, ct, my_api):

    conversion_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(u1, cf, ct, my_api)

    operurl = urllib.request.urlopen(conversion_url)
    data = operurl.read()
    cmcDict = json.loads(data)

    quantity_to = cmcDict['data']['quote'][ct]['price']

    return quantity_to

# Returns the unit price of Euro or Cryptourrency.

def calculateUnitPrice(u1, cf, ct, my_api):

    conversion_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(u1, cf, ct, my_api)

    operurl = urllib.request.urlopen(conversion_url)
    data = operurl.read()
    cmcDict = json.loads(data)

    quantity_to = cmcDict['data']['quote'][ct]['price']
    unit_price = (quantity_to/float(u1))

    return unit_price
    
# Profit or loss Message Function

def profitorlossMssg(crypto_value, total_invest):
    profit_message = "You have made a profit of: "
    loss_message = "You have made a loss of: "
    if (crypto_value > total_invest):
        return profit_message
    else:
        return loss_message

# Query the SQL table (Borrowed from our kakebo lessons)

def querySQL(query, parameters=[]):

    connection = sqlite3.connect("movements.db")
    cur = connection.cursor()
    cur.execute(query, parameters)
    keys = cur.description
    rows = cur.fetchall()
    result = []
    for row in rows:
        d = {}
        for tkey, value in zip(keys, row):
            d[tkey[0]] = value
        result.append(d)

    connection.close()
    return result

def modifySQL(query, parameters=[]):

    connection = sqlite3.connect("movements.db")
    cur = connection.cursor()
    cur.execute(query, parameters)
    connection.commit()
    connection.close()

def modifySQL2(query):

    connection = sqlite3.connect("movements.db")
    cur = connection.cursor()
    cur.executescript(query)
    connection.commit()
    connection.close()

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

'''username page:
                1. Invites the client to insert their username
                2. Inserts the username into the database and accesses the transaction page'''

@app.route('/', methods=['GET', 'POST'])
def index():

    form = NameForm()

    name_query = "INSERT INTO name_page (username) VALUES (?)"

    if request.method == 'GET':

        return render_template('login.html', form=form)
    
    else:

        if request.values.get('submit_name'):
            if form.validate():
                name = request.values.get("username")
                print(name)

                try:
                    name_insert = modifySQL(name_query, [name])

                    return render_template('movements.html', form=form, name_insert=name_insert)

                except sqlite3.Error as the_error:
                    print("Error in SQL INSERT: ", the_error)
                    flash("There has been an issue with the database. The samurai are comitting sepukku in shame", "error")

                    return render_template('login.html', form=form)

            return render_template('login.html', form=form)
        
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

'''Movements/Transactions page:
                                1. All of the transactions comitted to the Movements table in the database'''

@app.route('/movements', methods=['GET', 'POST'])
def movements():

    no_movement_message = "NO MOVEMENTS"

    query = "SELECT * FROM MOVEMENTS WHERE 1 = 1"
    parameters = []
        
    movements = querySQL(query, parameters)
    if movements == []:
        flash(no_movement_message)

    return render_template('movements.html', data = movements)

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

''' Purchase Page:
                    1. Select which currency to spend
                    2. Select which currency to purchase
                    3. Input quantity of currency to spend
                    4. Calculate the quantity of currency to buy
                    5. Quantity of unit to buy
                    6. 1-1 unit conversion (from, to)
                    7. Purchase the currency
                    '''

@app.route('/purchase', methods = ['GET', 'POST'])
def katana():

    form = MovementsForm()
    quantity_to_price = '0'
    unit_price = '0'
    user_query = querySQL("SELECT username FROM name_page WHERE id='1'")
    username = user_query[0]['username'].upper()


    if request.method == 'GET':

        return render_template('purchase.html', form=form, quantity_to_price=quantity_to_price, unit_price=unit_price)

    else:
        if request.values.get("calculate"):
            if form.validate():
                #parameters = []
                cf = request.form.get("currency_from")
                ct = request.form.get("currency_to")
                u1 = request.form.get("quantity_from")
                
                # Shameful error messages

                no_error_message = ""
                error_message_1 = "YOU CANNOT BUY ANY CURRENCY WITH THE SAME CURRENCY, {}-SAN".format(username)
                error_message_2 = "YOU MAY ONLY BUY {} WITH OTHER CRYPTOCURRENCIES, {}-SAN".format(ct, username)
                error_message_3 = "YOU MAY ONLY SELL BITCOIN TO BUY EUROS, {}-SAN".format(username)
                error_message_4 = "YOU MUST INPUT AN AMOUNT IF YOU WISH TO PURCHASE A CURRENCY, {}-SAN".format(username)
                error_message_4_5 = "YOU MUST NOT WRITE STRINGS IN THE SACRED QUANTITY FROM FIELD, {}-SAN".format(username)
                try:
                    
                    if cf == ct:
                        flash(error_message_1)
                    elif cf == "EUR" and ct != "BTC":
                        flash(error_message_2)
                    elif cf != "BTC" and ct == "EUR":
                        flash(error_message_3)
                    elif float(u1) == 0:
                        flash(error_message_4)
                    elif u1 == '':
                        flash(error_message_4_5)
                    else:
                         quantity_to_price = calculateKatana(u1, cf, ct, my_api)
                         unit_price = calculateUnitPrice(u1, cf, ct, my_api)
                         flash(no_error_message)

                    return render_template('purchase.html', form = form, quantity_to_price=quantity_to_price, unit_price=unit_price)

                except sqlite3.Error as the_error:
                    print("Unexpected error in the calculation: ", the_error)
                    flash("There has been a shameful error in calculation:", "error")
                    return render_template('purchase.html', form=form)

            return render_template('purchase.html', form=form, quantity_to_price=quantity_to_price, unit_price=unit_price)

        if request.values.get("crypto_katana"):
            if form.validate():
                cf = request.form.get("currency_from")
                ct = request.form.get("currency_to")
                u1 = request.form.get("quantity_from")

                currency_query_from = querySQL("SELECT value FROM currencyvalues WHERE currency='{}'".format(cf))
                av_bal_fromSTR = currency_query_from[0]['value']
                av_bal_from = float(av_bal_fromSTR)
                
                u2 = calculateUnitPrice(u1, cf, ct, my_api)
                tq = calculateKatana(u1, cf, ct, my_api)

                error_message_5 = "YOU DO NOT POSSESS THE NECESSARY FUNDS IN {} TO COMPLETE THIS TRANSACTION, {}-SAN".format(cf, username)

                try:

                    if av_bal_from < int(u1):
                        flash(error_message_5)

                    else:

                        currency_query_to = querySQL("SELECT VALUE FROM CURRENCYVALUES WHERE currency='{}'".format(ct))
                        av_bal_toSTR = currency_query_to[0]['value']
                        av_bal_to = float(av_bal_toSTR)

                        # currency_from_balance
                        cfb = av_bal_from - float(u1)
                        # currency_to_balance
                        ctb = av_bal_to + float(tq)
                        # Insert addition and subtraction (and trapped euro value)
                        cfbSTR = str(cfb)
                        ctbSTR = str(ctb)
                        u1STR = str(u1)
                        
                        final_currency_insert_query = modifySQL2("""UPDATE currencyvalues SET value=({}) WHERE currency='{}';
                                                                UPDATE currencyvalues SET value=({}) WHERE currency='{}';
                                                                UPDATE currencyvalues SET euro_value=({}) WHERE currency = '{}'; """.format(cfbSTR, cf, ctbSTR, ct, u1STR, ct))

                        today_date = date.today()
                        tdate = today_date.strftime("%d/%m/%Y")

                        localtime = time.localtime()
                        ttime = time.strftime("%H:%M:%S", localtime)

                        transactionQuery = """INSERT INTO movements (date, time, currency_from, currency_to, quantity_from, quantity_to, unit_price) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)"""

                        transaction_time_message = 'Purchase recorded on {} at {}'.format(tdate, ttime)
                        flash(transaction_time_message)

                        transaction = modifySQL(transactionQuery, [tdate, ttime, form.currency_from.data, form.currency_to.data, form.quantity_from.data,
                                            tq, u2])

                        return render_template('purchase.html', form=form, quantity_to_price=quantity_to_price, unit_price=unit_price, transaction=transaction, fciq = final_currency_insert_query)

                except sqlite3.Error as the_error:
                    print("Error in SQL INSERT: ", the_error)
                    flash("There has been an issue with the database. The samurai are comitting sepukku in shame", "error")
                    return render_template('purchase.html', form = form, quantity_to_price=quantity_to_price, unit_price=unit_price)
                
            return render_template('purchase.html', form = form, quantity_to_price=quantity_to_price, unit_price=unit_price)

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

'''Investment Page: 
                    1. Total Investment
                    2. Total Cryptocurrency Value
                    3. Profit/Loss'''

@app.route('/investment', methods = ['GET'])
def investment():

    parameters=[]

    # Total invested Euros
    euro_invest_query = querySQL("SELECT SUM(quantity_from) FROM movements WHERE currency_from='EUR'", parameters)
    if euro_invest_query[0] == {'SUM(quantity_from)': None}:
        pass
    else:
        total_investSTR = euro_invest_query[0]['SUM(quantity_from)']
        total_invest = float(total_investSTR)

    # Trapped Value of Cryptocurrencies in Euros (upon purchase). Unused.
    trapped_crypto_currency_query = querySQL("SELECT SUM(euro_value) FROM currencyvalues WHERE NOT currency='EUR'", parameters)
    trapped_crypto_value = trapped_crypto_currency_query[0]['SUM(euro_value)']
    trapped_crypto_valueSTR = trapped_crypto_value

    # Current value of Cryptocurrencies
   
    crypto_dict_1 = {"EUR": 0.0, "ETH": 0.0, "LTC": 0.0, "BNB": 0.0, "EOS": 0.0, "XLM": 0.0, "TRX": 0.0, "BTC": 0.0, "XRP": 0.0, "BCH": 0.0, "USDT": 0.0, "BSV": 0.0, "ADA": 0.0}
    crypto_dict_2 = {"EUR": 0.0, "ETH": 0.0, "LTC": 0.0, "BNB": 0.0, "EOS": 0.0, "XLM": 0.0, "TRX": 0.0, "BTC": 0.0, "XRP": 0.0, "BCH": 0.0, "USDT": 0.0, "BSV": 0.0, "ADA": 0.0}

    # This for loop jsonifies the code.

    i = 0
    for ckey in crypto_dict_1:
        if len(crypto_dict_1) >= i:
            iterate_a_crypto = querySQL("SELECT value FROM currencyvalues WHERE currency='{}'".format(ckey))
            crypto_value = iterate_a_crypto[0]['value']
            if ckey != "EUR":
                crypto_dict_2.update({ckey:crypto_value})
            else:
                pass
        else:
            pass
        i += 1

    # Here, the crypto dictionary pops the EUR so that it doesn't iterate over an empty list:

    crypto_dict_2.pop("EUR")

    # Returns the trapped value of each crypto in the database, and calculates its current value against the euro.

    t = 0
    evalue = "EUR"
    invest_list = []
    if len(crypto_dict_2) >= t:
        for crypto in crypto_dict_2:
            cvalue = crypto_dict_2[crypto]
            fcvalue = float(cvalue)
            if fcvalue != 0:
                euro_value_in_crypto = calculateKatana(fcvalue, crypto, evalue, my_api)
                invest_list.append(euro_value_in_crypto)
            else:
                pass
        t += 1

    # Adds up all of the cryptocurrencies in their current value

    cryptokatana_final_investment_value = sum(invest_list)

    # La regla de tres

    profit_or_loss = cryptokatana_final_investment_value - total_invest
    profit_lossSTR = profit_or_loss

    # Profit or loss message:
    
    pol_message = profitorlossMssg(cryptokatana_final_investment_value, total_invest)

    return render_template('investment.html', cv=cryptokatana_final_investment_value, ti=total_investSTR, pol=profit_lossSTR, pol_message=pol_message)
    

                
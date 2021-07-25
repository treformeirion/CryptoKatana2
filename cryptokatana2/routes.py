from datetime import date
import time
from cryptokatana2 import app
from flask import render_template, request, redirect, url_for, flash, json, session
from cryptokatana2.forms import MovementsForm
import sqlite3
import urllib

# Namepage code. Please enter your name and password here so that it works.

'''THE BIG ISSUE: DOES MY BITCOINS TRANSFER INTO SINGLE UNITS OR DO I JUST HAVE ALMOST NOTHING IN BITCOINS?'''
'''THIS MIGHT BE A HUGE PROBLEM. WHEN I BUY MY BITCOINS, ALTHOUGH THEIR VALUE IN EUROS IS THAT MUCH, I SHOULD HAVE
SO AND SO MANY BITCOINS. FOR EXAMPLE. IF I BUY '''
''' ALSO THE UNIT PRICE CHANGES. WHY?'''

name = "Trefor"

user = {"username": name}

# Access the api by providing an api key.

my_api = '65bcaa07-93bc-428d-a65e-6d2dbe67eb79'

# The Great Catalogue of Messages:

profit_message = "You have made a profit of: "
loss_message = "You have made a loss of: "
no_movement_message = "NO MOVEMENTS"
    
# Returns an accurate calculation of the quantity you'll be getting for the unit price of the currency the client will be converting to

def calculateKatana(u1, cf, ct, my_api):

    conversion_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(u1, cf, ct, my_api)

    operurl = urllib.request.urlopen(conversion_url)
    data = operurl.read()
    cmcDict = json.loads(data)

    quantity = cmcDict['data']['amount']
    unit_price = cmcDict['data']['quote'][ct]['price']

    quantityTo = (quantity*unit_price)

    #quantityTo = cmcDict['quote'][ct]['price']*cmcDict[u1]

    return quantityTo

# Returns the unit price.

def calculateUnitPrice(u1, cf, ct, my_api):

    conversion_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(u1, cf, ct, my_api)

    operurl = urllib.request.urlopen(conversion_url)
    data = operurl.read()
    cmcDict = json.loads(data)

    unit_price = cmcDict['data']['quote'][ct]['price']

    return unit_price

# Returns the entire cryptocurrency table value
    
# Profit or loss Message Function

def profitorlossMssg(crypto_value, total_invest):
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

'''Name page:
                1. Invites the client to insert their name
                2. Inserts the name into the database and accesses the transaction page'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')

        return render_template('movements.html', username=username)

    return render_template('login.html')

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

'''Movements/Transactions page:
                                1. All of the transactions comitted to the Movements table in the database'''

@app.route('/movements', methods=['GET'])
def movements():

    query = "SELECT * FROM MOVEMENTS WHERE 1 = 1"
    parameters = []
        
    movements = querySQL(query, parameters)
    if movements == []:
        flash(no_movement_message)

    return render_template('movements.html', data = movements, name=name)

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

    if request.method == 'GET':

        return render_template('purchase.html', form=form, quantity_to_price=quantity_to_price, unit_price=unit_price)

    else:
        if request.values.get("calculate"):
            if form.validate():
                parameters = []
                cf = request.form.get("currency_from")
                ct = request.form.get("currency_to")
                u1 = request.form.get("quantity_from")
                
                # Shameful error messages

                no_error_message = ""
                error_message_1 = "YOU CANNOT BUY ANY CURRENCY WITH THE SAME CURRENCY, {}-SAN".format(name)
                error_message_2 = "YOU MAY ONLY BUY {} WITH OTHER CRYPTOCURRENCIES, {}-SAN".format(ct, name)
                error_message_3 = "YOU MAY ONLY SELL BITCOIN TO BUY EUROS, {}-SAN".format(name)
                error_message_4 = "YOU MUST INPUT AN AMOUNT IF YOU WISH TO PURCHASE A CURRENCY, {}-SAN".format(name)

                try:
                    
                    if cf == ct:
                        flash(error_message_1)
                    elif cf == "EUR" and ct != "BTC":
                        flash(error_message_2)
                    elif cf != "BTC" and ct == "EUR":
                        flash(error_message_3)
                    elif u1 == 0:
                        flash(error_message_4)
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
                parameters = []
                cf = request.form.get("currency_from")
                ct = request.form.get("currency_to")
                u1 = request.form.get("quantity_from")

                # To subtract the amount from any currency's value, I need to take the available balance info, and
                # add or subtract the amount and then insert the available balance into the values column.

                currency_query_from = querySQL("SELECT VALUE FROM CURRENCYVALUES WHERE currency='{}'".format(cf))
                available_balance_from = currency_query_from[0]['value']
                print(available_balance_from)
                u2 = calculateUnitPrice(u1, cf, ct, my_api)
                tq = calculateKatana(u1, cf, ct, my_api)

                error_message_5 = "YOU DO NOT POSSESS THE NECESSARY FUNDS IN {} TO COMPLETE THIS TRANSACTION, {}-SAN".format(cf, name)

                try:

                    if available_balance_from < int(u1):
                        flash(error_message_5)

                    else:

                        currency_query_to = querySQL("SELECT VALUE FROM CURRENCYVALUES WHERE currency='{}'".format(ct))
                        available_balance_to = currency_query_to[0]['value']

                        # currency_from_balance
                        cfb = available_balance_from - int(u1)
                        # currency_to_balance
                        ctb = available_balance_to + int(tq)

                        final_currency_insert_query = modifySQL2("""UPDATE currencyvalues SET value=({}) WHERE currency='{}';
                                                                UPDATE currencyvalues SET value=({}) WHERE currency='{}';
                                                                UPDATE currencyvalues SET euro_value=({}) WHERE currency = '{}'; """.format(cfb, cf, ctb, ct, u1, ct))

                        today_date = date.today()
                        tdate = today_date.strftime("%d/%m/%Y")

                        localtime = time.localtime()
                        ttime = time.strftime("%H:%M:%S", localtime)

                        transactionQuery = """INSERT INTO MOVEMENTS (date, time, currency_from, currency_to, quantity_from, quantity_to, unit_price) 
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
    total_invest = euro_invest_query[0]['SUM(quantity_from)']
    total_investSTR = total_invest

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

    ct = "EUR"
    invest_list = []
    for crypto in crypto_dict_2:
        value = crypto_dict_2[crypto]
        print(crypto)
        print(value)
        calculate_the_value = calculateUnitPrice(value, crypto, ct, my_api)
        invest_list.append(calculate_the_value)
    cryptokatana_final_investment_value = sum(list)


    #cryptokatana_final_investment_value = total_cryptos_value / total_invest

    # Have you made a profit or a loss?
    profit_or_loss = ''
    profit_lossSTR = profit_or_loss

    # Profit or loss message:
    pol_message = profitorlossMssg(cryptokatana_final_investment_value, total_invest)

    return render_template('investment.html', cv=cryptokatana_final_investment_value, ti=total_investSTR, pol=profit_lossSTR, pol_message=pol_message)
    

                
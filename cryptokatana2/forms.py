from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, FloatField, BooleanField, HiddenField, TimeField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, ValidationError

class NameForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])

    submit_name = SubmitField('Enter Name')

class MovementsForm(FlaskForm):
    id = HiddenField()

    currency_from = SelectField('Currency From', validators = [DataRequired()], choices = [('EUR', 'Euro (EUR)'), ('ETH', 'Etherum (ETH)'), ('LTC','Litecoin (LTC)'),                                                                     
                                                                                ('BNB','Binance (BNB)'), ('EOS', 'EOS'), ('XLM', 'Stellar (XLM)'), 
                                                                                ('TRX', 'Tron (TRX)'), ('BTC', 'Bitcoin (BTC)'), ('XRP', 'Ripple (XRP)'), 
                                                                                ('BCH', 'Bitcoin Cash (BCH)'), ('USDT', 'Tether (USDT)'), ('BSV', 'Bitcoin SV (BSV)'), 
                                                                                ('ADA', 'Cardadno (ADA)')], description="Choose the currency you would like to conver into")
    currency_to = SelectField('Currency To', validators = [DataRequired()], choices = [('EUR', 'Euro (EUR)'), ('ETH', 'Etherum (ETH)'), ('LTC','Litecoin (LTC)'),                                                                     
                                                                                ('BNB','Binance (BNB)'), ('EOS', 'EOS'), ('XLM', 'Stellar (XLM)'), 
                                                                                ('TRX', 'Tron (TRX)'), ('BTC', 'Bitcoin (BTC)'), ('XRP', 'Ripple (XRP)'), 
                                                                                ('BCH', 'Bitcoin Cash (BCH)'), ('USDT', 'Tether (USDT)'), ('BSV', 'Bitcoin SV (BSV)'), 
                                                                                ('ADA', 'Cardadno (ADA)')], description="Choose the currency you would like to conver into")
    quantity_from = FloatField('Qty From', validators= [InputRequired()])
    quantity_to = FloatField('Qty To')

    unit_price = FloatField('Unit Price')
    

    calculate = SubmitField('Calculate')
    crypto_katana = SubmitField('Katana')
    

from flask import Flask
from flask_restful import Api, Resource
from flask_restful import reqparse
import pymarketstore as pymkts
import talib
import pandas as pd

app = Flask(__name__);
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('exchange_symbol', type=str, default='binance-BTCUSDT', help='Provide exchange_symbol')
parser.add_argument('interval', type=str, default='1Min', help='Provide interval')



class RSI(Resource):
  def get(self):
    args = parser.parse_args()
    # exchange_symbol = 'binance-BTCUSDT'
    # args['interval'] = '1Min'
    datatype = 'OHLCV'


    param = pymkts.Params(args['exchange_symbol'], args['interval'], datatype)

    cli = pymkts.Client('http://206.189.216.139:5993/rpc')

    reply = cli.query(param)
    data = reply.first().df()
    close = data['Close']
    rsi = talib.RSI(close, timeperiod=12)

    # print(rsi.to_json())

    return 'rsi.to_json(), 201'

api.add_resource(RSI, '/')


if __name__ == '__main__':
  app.run(debug=True)



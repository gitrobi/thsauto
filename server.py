import functools
from flask import Flask, request, jsonify
from thsauto import ThsAuto
import time
import sys

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

auto = ThsAuto()

last_time = 0
interval = 4

APP = 't'
BALANCE = 'bal'
POSITION = 'pos'
ORD_ACTIVE = 'act'
ORD_FILLED = 'fil'
BUY = 'buy'
SELL = 'sel'
CANCEL = 'can'
CANCEL_ALL = 'cal'


def interval_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global last_time
        global interval
        now = time.time()
        if now - last_time < interval:
            time.sleep(interval - (now - last_time))
        last_time = now
        rt = func(*args, **kwargs)
        return rt
    return wrapper


def error_handle(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = '{}'.format(e)
            return {'success': False, 'msg': message}, 400
    return wrapper


@app.route('/{}/{}'.format(APP, BALANCE), methods = ['GET'])
@error_handle
@interval_call
def get_balance():
    result = auto.get_balance()
    return jsonify(result), 200

@app.route('/{}/{}'.format(APP, POSITION), methods = ['GET'])
@error_handle
@interval_call
def get_position():
    result = auto.get_position()
    return jsonify(result), 200

@app.route('/{}/{}'.format(APP, ORD_ACTIVE), methods = ['GET'])
@error_handle
@interval_call
def get_active_orders():
    result = auto.get_active_orders()
    return jsonify(result), 200

@app.route('/{}/{}'.format(APP, ORD_FILLED), methods = ['GET'])
@error_handle
@interval_call
def get_filled_orders():
    result = auto.get_filled_orders()
    return jsonify(result), 200

@app.route('/{}/{}'.format(APP, SELL), methods = ['GET'])
@error_handle
@interval_call
def sell():
    stock = request.args['code']
    amount = request.args['amount']
    price = request.args['price']
    result = auto.sell(stock_no=stock, amount=int(amount), price=float(price))
    return jsonify(result), 200

@app.route('/{}/{}'.format(APP, BUY), methods = ['GET'])
@error_handle
@interval_call
def buy():
    stock = request.args['code']
    amount = request.args['amount']
    price = request.args['price']
    result = auto.buy(stock_no=stock, amount=int(amount), price=float(price))
    return jsonify(result), 200

@app.route('/{}/{}'.format(APP, CANCEL), methods = ['GET'])
@error_handle
@interval_call
def cancel():
    entrust_no = request.args['entrust_no']
    result = auto.cancel(entrust_no=entrust_no)
    return jsonify(result), 200

@app.route('/{}/{}'.format(APP, CANCEL_ALL), methods = ['GET'])
@error_handle
@interval_call
def cancel_all():
    direct = request.args['direct']
    result = auto.cancel_all(direct=direct)
    return jsonify(result), 200


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 7979
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    app.run(host=host, port=port)
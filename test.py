# -*- coding: utf-8 -*-
from thsauto import ThsAuto

import time

if __name__ == '__main__':
    
    auto = ThsAuto()                                        # 连接客户端

    print('可用资金')
    t1 = time.time()
    print(auto.get_balance())                               # 获取当前可用资金
    print(time.time() - t1)

    print('持仓')
    t1 = time.time()
    print(auto.get_position())                              # 获取当前持有的股票
    print(time.time() - t1)

    # print('卖出')
    # t1 = time.time()
    # print(auto.sell(stock_no='511850', amount=100, price=100))   # 卖出股票
    # print(time.time() - t1)

    print('买入')
    t1 = time.time()
    result = auto.buy(stock_no='512880', amount=100, price=0.410)  # 买入股票
    print(result)
    result = auto.buy(stock_no='512880', amount=100, price=0.410)  # 买入股票
    print(result)

    # print(time.time() - t1)
    #
    # print('已成交')
    # t1 = time.time()
    # print(auto.get_filled_orders())                                 # 获取已成交订单
    # print(time.time() - t1)
    #
    # print('未成交')
    # t1 = time.time()
    # print(auto.get_active_orders())                                 # 获取未成交订单
    # print(time.time() - t1)

    # if result and result['success']:                                # 如果买入下单成功，尝试撤单
    #     print('撤单')
    #     t1 = time.time()
    #     print(auto.cancel(entrust_no=result['entrust_no']))
    #     print(time.time() - t1)

    print('撤单')
    #print(auto.cancel('1292674029'))
    print(auto.cancel_all())


import stock_wrapper

import yfinance
import robin_stocks
import pandas as pd
import numpy as np

import datetime


class data:
    __switcher = {
        'day': '1d',
        'week': '5d',
        'month': '1mo',
        '3month': '3mo',
        'year': '1y',
        'max': 'max'
    }

    def __init__(self):
        pass

    @classmethod
    def get_daily_history(cls, ticker_symbol, span='day'):
        """Takes a single Ticker Symbol to build a list of tuples representing a time_frame and its respective price
        :param stock: single Ticker Symbol
        :type: str
        :param span: width of the history of the selected stock, can be day, week, month, 3month, year, max
        :type: str
        :param time_zone: one of the global time zones,
        :type: str
        :return: [list]: (timeframe <datetime.datetime>, price <int>)
        """

        historicals = []
        history = yfinance.Ticker(ticker_symbol).history(period=cls.__switcher[span])
        for row in history.head().itertuples():
            object = {}
            object['date'] = row.Index
            object['open'] = row.Open
            object['close'] = row.Close
            object['high'] = row.High
            object['low'] = row.Low
            object['volume'] = row.Volume

            historicals.append(object)

        return historicals

    @classmethod
    def get_historical_prices(cls, ticker_symbol, span='day'):
        """Takes a single Ticker Symbol to build a list of tuples representing a time_frame and its respective price
        :param stock: single Ticker Symbol
        :type: str
        :param span: width of the history of the selected stock
        :type: str
        :param time_zone: one of the global time zones,
        :type: str
        :return: [list]: (timeframe <datetime.datetime>, price <int>)
        """

        historicals = []
        history = robin_stocks.get_historicals(ticker_symbol, span=span)
        for time_frame in history:
            time = cls.__get_time(time_frame['begins_at'])
            price = (float(time_frame['open_price']) + float(time_frame['close_price'])) / 2
            historicals.append((time, float(price)))

        return historicals

    @staticmethod
    def __get_time(time, conversion=-5):
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=conversion)

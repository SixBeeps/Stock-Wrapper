import stock_wrapper

import yfinance
import robin_stocks
import pandas as pd
import os
import numpy as np

import json
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

    @classmethod
    def get_history(cls, tickers, span='week', interval='1m', calculate_averages=True, cache=False, extended=False):
        """Takes in a ticker object and returns a pandas dataframe containing price,
        :param ticker_symbols: Single Ticker object or list of Ticker objects
        :type ticker_symbols: str
        :param span: How much data to retrieve
        :type span: str, [day, week, month, 3month, year, max]
        :param interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        :type interval: str
        :param calculate_averages: Whether or not to calculate moving averages
        :type calculate_averages: bool
        :param cache: whether or not to retrieve/store in cache
        :type cache: bool
        :return: pandas dataframe
        """
        # if cache and cls.cache.exists(ticker_symbol, span, interval):
        #     return pd.read_json(cls.cache.read_file(ticker_symbol, span, interval))
        # else:
        if isinstance(tickers, stock_wrapper.Stock):
            tickers = [tickers]

        ticker_symbols = ''
        for ticker in tickers:
            ticker_symbols += ticker.ticker + ' '

        if True:
            history = yfinance.download(tickers=ticker_symbols, period=cls.__switcher[span], group_by='ticker', prepost=extended, interval=interval).reset_index()
            print(history)
            # history['Average'] = (history['High'] + history['Low']) / 2
            #
            # def __build_average(period):
            #     name = (str(period) + '_SMA')
            #
            #     if len(history) > period:
            #         history.loc[0:period, name] = np.nan
            #
            #         index = period + 1
            #         while index < len(history):
            #             history.iloc[index, history.columns.get_loc(name)] = history.iloc[index - period:index]['Close'].sum() / period
            #             index += 1
            #
            # if calculate_averages:
            #     __build_average(10)
            #     __build_average(20)
            #     __build_average(100)
            #     __build_average(200)
            #
            # if history.columns.values[0] != 'Date':
            #     headers = history.columns.values
            #     headers[0] = 'Date'
            #     history.columns = headers
            #
            # cls.cache.write_file(ticker_symbol, span, interval, history.to_json())

        return history

    @classmethod
    def get_historical_prices(cls, ticker_symbol, span='day'):
        """Takes a single Ticker Symbol to build a list of tuples representing a time_frame and its respective price
        :param ticker_symbol: single Ticker Symbol
        :type ticker_symbol: str
        :param span: width of the history of the selected stock
        :type: str
        :return: [list]: (timeframe <datetime.datetime>, price <int>)
        """

        history = robin_stocks.get_historicals(ticker_symbol, span=span)
        for time_frame in history:
            time_frame['begins_at'] = cls.__get_time(time_frame['begins_at'])

        historicals_df = pd.DataFrame(history).astype({'open_price': 'float32', 'close_price': 'float32'})
        historicals_df['Average'] = historicals_df.apply(lambda row: (row.open_price + row.close_price) / 2, axis=1)
        historicals_df = historicals_df.rename(columns={'begins_at':'Date', 'open_price':'Open', 'close_price':'Close', 'high_price':'High', 'low_price':'Low', 'symbol':'Symbol', 'volume':'Volume', 'session':'Session', 'interpolated':'Interpolated'})
        return historicals_df

    @staticmethod
    def __get_time(time, conversion=-5):
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=conversion)

    @classmethod
    def clear_cache(cls):
        cls.cache.clear()

    class cache:
        @classmethod
        def read_file(cls, ticker_name, span, interval):
            path = cls.__get_path(ticker_name, span, interval)
            with open(path) as json_file:
                data = json.load(json_file)

            return data

        @classmethod
        def write_file(cls, ticker_name, span, interval, data):
            if not os.path.exists(os.path.abspath('__stock_cache__')):
                os.makedirs(os.path.abspath('__stock_cache__'))

            path = cls.__get_path(ticker_name, span, interval)
            with open(path, 'w+') as outfile:
                json.dump(data, outfile)

        @classmethod
        def exists(cls, ticker_name, span, interval):
            path = cls.__get_path(ticker_name, span, interval)
            return os.path.exists(path)

        @staticmethod
        def clear():
            if os.path.exists(os.path.abspath('__stock_cache__')):
                dirpath = os.path.abspath('__stock_cache__/')
                for path in os.listdir(dirpath):
                    os.remove(os.path.abspath('__stock_cache__/' + path))

        @classmethod
        def __get_path(cls, ticker_name, span, interval):
            return os.path.abspath('__stock_cache__/' + ticker_name + '_' + span + '_' + interval + '.py')
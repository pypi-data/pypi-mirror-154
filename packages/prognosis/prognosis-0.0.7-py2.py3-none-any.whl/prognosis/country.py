# -*- coding: utf-8 -*-
"""
Created on Fri May 20 12:30:58 2022

@author: oriol
"""

import pandas as pd
from prognosis.helper import get
from prognosis.com import topic_tickers


class Country():
    def __init__(self, country_code):
        self.country_code = country_code

    def get_group(self, name):
        codes = [x % self.country_code for x in topic_tickers[name]]
        return get(codes)

    def national_accounts(self):
        """
        RGDP: Real gross domestic product
        RPRC: Real private consumption
        RPUC: Real public sector consumption
        RGFCF: Real gross fixed capital formation
        REXP: Real exports
        RIMP: Real imports

        Note: Real refers to inflation adjusted indicators
        """
        return self.get_group('national_accounts')

    def prices(self):
        return self.get_group('prices')

    def monthly_trade(self):
        return self.get_group('monthly_trade')

    def government_accounts(self):
        return self.get_group('government')

    def yield_curve(self):
        return self.get_group('yield_curve')

    def retail_sales(self):
        return self.get_group('retail_sales')

    def ip(self):
        return self.get_group('ip')

    def energy(self):
        """
        OILPROD: Oil production, thousands barrels per day
        OILDEM: Oil demand, thousands barrels per day
        GASODEM: Gasoline demand, thousands barrels per day
        GASOPROD: Gasoline production, thousands barrels per day
        GASDEM: Gas demand, millions of cubic meters per month
        GASPROD: Gas production, millions of cubic meters per month
        """
        return self.get_group('energy')

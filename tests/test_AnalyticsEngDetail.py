

import json
import logging
import os
import pandas as pd
import json
import pytest

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

class test_retrieveDetailReport():

    def __init__(self, test_read_config_file:object) -> None:

        LOGGER.debug('retrieveDetailReport:: init start')
        self.title = 'retrieveAnalyticsDetailedReport'
        self.author = 'VW'
        self.URL = test_read_config_file['urls']['url']
        self.URL_api_interval = test_read_config_file['urls']['url_AnalyticsintervalDetailed']
        self.URL_api_daily = test_read_config_file['urls']['url_AnalyticsDailyDetailed']
        self.s = 'null'     # session request
        self.DetailedReportInterval_df = 'null'
        self.response_dict = 'null'
        self.token = 'null'
        self.payload = {}
        self.headers = {}
        self.session = 'null'
        self.retry = 'null'
        self.adapter = 'null'

        LOGGER.debug('retrieveDetailReport:: init finished')
        return

    def test_buildIntervalRequest(self, getToken):

        LOGGER.debug('test_buildIntervalRequest:: started')
        self.token = getToken
        assert getToken, 'token not retrieved'
        token_append = 'Bearer '+ getToken        # cat Bearer to token, include space after 'Bearer '

        LOGGER.debug('test_buildIntervalRequest:: token retrieved and assembled')

        self.payload = {}
        self.headers = {
            'Accept': 'application/json',
            'Authorization': token_append,
            'User-Agent': 'Avaya-API-Analytics'
        }

        print('dump headers: {session.headers}')

        # create a sessions object
        self.session = requests.Session()
        assert self.session, 'session not created'
        self.retry = Retry(connect=25, backoff_factor=0.5)
        self.adapter = HTTPAdapter(max_retries=self.retry)
        self.session.mount('https://', self.adapter)
        self.session.mount('http://', self.adapter)
        # Set the Content-Type header to application/json for all requests in the session
        self.session.headers.update(self.headers)
        print(f'dump headers: {self.session.headers}')
        LOGGER.debug('test_buildIntervalRequest:: finished')
        return

    def test_sendRequestInterval(self):

        LOGGER.debug('test_sendRequestInterval:: start')

        try:
            self.s = self.session.get(self.URL + self.URL_api_interval,  timeout=25, verify=False)
            self.s.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("test_sendRequestInterval Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("test_sendRequestInterval Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("test_sendRequestInterval Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("test_sendRequestInterval OOps: Something Else", err)

        assert self.s.status_code == 200, 'session request response not 200 OK'

        print(f'test_sendRequestInterval session resp received code: {self.s.status_code}')
        LOGGER.debug('test_sendRequestInterval:: response received')

        self.response_dict = json.loads(self.s.text)

        if self.s.status_code == 200:
            # normalise data
            self.DetailedReportInterval_df = pd.json_normalize(self.response_dict)
            # print(f'test_getEngReportInterval, returned data: {DetailedReportInterval_df.head}')
            self.DetailedReportInterval_df.to_json('./output/EngDetailedReport/IntervaloutputEngDetail.json', orient='table')
        else:
            self.DetailedReportInterval_df = 'null'

        assert not self.DetailedReportInterval_df.empty, 'No DetailedReportInterval_df returned'

        LOGGER.debug('test_sendRequestInterval:: finished')
        return self.DetailedReportInterval_df




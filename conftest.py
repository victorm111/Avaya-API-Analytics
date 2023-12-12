import requests
import json
import hashlib
import os
import pytest
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

load_dotenv()  # take environment variables from .env.

@pytest.fixture(scope='function')
def getToken():

  LOGGER.debug('conftest:: start getToken')
  url = "https://wfo.a31.verintcloudservices.com/wfo/rest/core-api/auth/token"

  payload = json.dumps({
    "user": "api_user@verintnew01.prodreleasev2.com",
    "password": "1_Abc_123"
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload, timeout=25, verify=False)

  LOGGER.debug('conftest:: getToken response received')
  print(response.text)
  print("token is:", {response.content})

  json_response = response.json()
  print(f'token is: {json_response["AuthToken"]["token"]}')

  # remove quotes at each end

  os.environ["TOKEN"] = json.dumps(json_response["AuthToken"]["token"])[1:-1]


  LOGGER.debug('conftest:: finish getToken')
  yield

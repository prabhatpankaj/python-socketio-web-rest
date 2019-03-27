import json
import requests

def caruser_info(plateText):
  headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json'}
  url = 'http://127.0.0.1:8081/userdata'
  try:
    requests.post(url, params=plateText, headers=headers)
    return True
  except:
    return False

if __name__ == '__main__':
  plateText = {"customername":"value1", "carnumber":"value2"}
  caruser_info(plateText)

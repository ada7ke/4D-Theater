import requests
import json

# Kodi server details
KODI_URL = 'http://192.168.0.113:8080/jsonrpc'

def get_current_timestamp():
    headers = {'Content-Type': 'application/json'}
    
    # Request payload to get the current timestamp
    payload = {
        "jsonrpc": "2.0",
        "method": "Player.GetProperties",
        "params": {
            "playerid": 1,
            "properties": ["time"]
        },
        "id": "2"
    }
    
    response = requests.post(KODI_URL, headers=headers, data=json.dumps(payload))
    data = response.json()
    
    if 'result' in data:
        time = data['result']['time']
        timestamp = f"{time['hours']:02}:{time['minutes']:02}:{time['seconds']:02}"
    else:
        timestamp = "No timestamp available"
    
    return timestamp + ".000"

if __name__ == "__main__":
    timestamp = get_current_timestamp()
    print(f"Current timestamp: {timestamp}")

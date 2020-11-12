import json
import requests

resp = requests.get('http://tele3dprinting.com/2019/process.php?api=list')

# Perfect case
# resp = resp.json()
resp = [
    {
        "school_id": "1",
        "user_id": "144",
        "file_id": "236",
        "file": "FIBO Tag.3w",
        "file_download": "2020-11-06 11-04-40 (144) (FIBO Tag.3w).0.3w"
    },
    {
        "school_id": "13",
        "user_id": "2",
        "file_id": "235",
        "file": "FishSupportBase.3w",
        "file_download": "2020-11-03 16-41-03 (2) (FishSupportBase.3w).0.3w"
    }
]

SC_ID = "1"
for obj in resp:
    if obj['school_id'] == SC_ID:
        pass



# content = str(resp.content)[6:-6]
# content = content.replace('\\n', '')
# print(content)
# data = json.loads(content)
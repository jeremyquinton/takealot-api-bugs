import urllib.request
import urllib.parse
import json

API_KEY = ""
BASE_URL = "https://marketplace-api.takealot.com/v1/returns"

date_from = "2026-03-26"
date_to = "2026-04-14"

continuation_token = None

while True:
    # 👇 Only include filters on first request
    if continuation_token:
        params = {
            "continuation_token": continuation_token
        }
    else:
        params = {
            "return_date__gte": date_from,
            "return_date__lte": date_to,
            "limit": 50
        }

    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    print(url);
    req = urllib.request.Request(
        url,
        headers={
            "X-API-Key": API_KEY,
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

            items = data.get("items", [])
            print(f"Fetched {len(items)} items")

            # 👇 Get next continuation token
            continuation_token = data.get("continuation_token")

            if not continuation_token:
                break

    except urllib.error.HTTPError as e:
        print("HTTP error:", e.code)
        print(e.read().decode())
        break

print("Done")

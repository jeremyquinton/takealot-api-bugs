import urllib.request
import urllib.parse
import json

API_KEY = ""
BASE_URL = "https://marketplace-api.takealot.com/v1/offers"

continuation_token = None
total_offers = 0
item_count = None
page = 1

while True:
    # Only include filters/expands on first request
    if continuation_token:
        params = {
            "continuation_token": continuation_token
        }
        url = BASE_URL + "?" + urllib.parse.urlencode(params)
    else:
        params = {
            "limit": 100,
            "include_count": "true"
        }
        url = BASE_URL + "?" + urllib.parse.urlencode(params) + "&expands=takealot_warehouse_stock"

    print(f"[Page {page}] GET {url}")

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

            if item_count is None:
                item_count = data.get("count")
                print(f"Total offers available (item_count): {item_count}")

            items = data.get("items", [])
            total_offers += len(items)

            print(f"[Page {page}] Fetched {len(items)} offers. Total so far: {total_offers}")

            for offer in items:
                print(
                    f"  offer_id={offer.get('offer_id')} "
                    f"sku={offer.get('sku')} "
                    f"status={offer.get('status')} "
                    f"title={offer.get('title', '')[:50]}"
                )

            continuation_token = data.get("continuation_token")

            if not continuation_token:
                break

            page += 1

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code}")
        print(e.read().decode())
        break

print(f"\nDone. item_count from API: {item_count}, total fetched: {total_offers}")

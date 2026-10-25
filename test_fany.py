import requests
import time

BASE_URL = "https://ticket.fany.lol"

PARAMS = {
    "keywords": "ドンデコルテ",
    "search_type": "search_string"
}

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja-JP,ja;q=0.9"
})


def check(name, url, params=None, headers=None):
    print(f"\n[TEST] {name}")

    try:
        response = session.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )

        print(f"status={response.status_code}")
        print(f"server={response.headers.get('server')}")
        print(f"x-cache={response.headers.get('x-cache')}")
        print(f"cf-pop={response.headers.get('x-amz-cf-pop')}")

        if response.status_code == 200:
            if name == "FANY_API":
                data = response.json()

                print(
                    "performances=",
                    len(data.get("performances", []))
                )

                print(
                    "load_count=",
                    data.get("load_count")
                )
        else:
            print("Request was not successful.")

        return response.status_code

    except requests.RequestException as e:
        print(f"Request error: {type(e).__name__}")
        return None

    except ValueError:
        print("Response was not valid JSON.")
        return None


check(
    "FANY_TOP",
    BASE_URL + "/"
)

time.sleep(2)

check(
    "FANY_SEARCH",
    BASE_URL + "/search/event",
    params=PARAMS
)

time.sleep(2)

api_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE_URL + "/search/event"
}

api_params = {
    **PARAMS,
    "offset": 0
}

check(
    "FANY_API",
    BASE_URL + "/search/event_more",
    params=api_params,
    headers=api_headers
)
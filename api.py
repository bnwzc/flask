import requests

API_URL = "http://127.0.0.1:5000"


def post_score(data):
    try:
        req = requests.post(API_URL + "/api/score", json=data)
    except Exception as e:
        if isinstance(e, requests.exceptions.RequestException):
            print(f"Connection to the API failed: {e}")
            return
    else:
        if req.status_code == 200 and req.json().get("success"):
            print("Score posted successfully")


if __name__ == "__main__":
    post_score({
        "user_token": "58c2096c4e7de7aee98a404d5fbd8eea",
        "score": 1455
})
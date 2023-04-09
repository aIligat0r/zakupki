import requests
import fake_headers


def requester(url: str):
    headers = fake_headers.Headers().generate()
    for retry in range(5):
        try:
            response = requests.get(url, headers=headers)
            return response
        except:
            pass
    return

from urllib.parse import quote
import requests, json

api_key = ""
base_string = "http://localhost:8989/api/v3"
key_string = f"&apikey={api_key}"

def lookup(search):
    query = quote(search)
    result = requests.get(f"{base_string}/series/lookup?term={query}" + key_string).json()
    title = ""
    if title != "":
        print(f"Found: {title} ({network})")

    tv_id = ""
    return tv_id
    # TODO: Add more return info

def listSeries():
    series = requests.get(f"{base_string}/series" + key_string).json()
    for i in range(len(series[0])):
        print(f"{i + 1}. {series[0][i]["title"]} ({series[0][i]["network"]})")
        print(f"\tOverview: {series[0][i]["overview"]}")

def deleteShow(search):
    show_id = lookup(search)
    result = requests.get(f"{base_string}/series/{show_id}" + key_string).json()
    # TODO: show details and confirm
    requests.delete(f"{base_string}/series/{show_id}", )
    

def addShow(search):
    pass

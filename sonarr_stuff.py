from urllib.parse import quote
import requests, json

api_key = "5471ca175deb4424a552743adc4b7300"
base_string = "http://192.168.1.101:8989/api/v3"
key_string = f"&apikey={api_key}"
key_string_2 = f"?apikey={api_key}"

def lookup(search):
    query = quote(search)
    result = requests.get(f"{base_string}/series/lookup?term={query}" + key_string).json()[0]
    title = result["title"]
    year = result["year"]
    print(f"Found: {title} ({year})")
    tvdb_id = result["tvdbId"]
    tvrage_id = result["tvRageId"]
    #profile_id = result["profileId"]
    title_slug = result["titleSlug"]
    images = result["images"]
    seasons = result["seasons"]
    for i in range(len(seasons)):
        seasons[i]["monitored"] = True
    path = f"/tv/{title}"
    opts = {
        "ignoreEpisodesWithFiles": False,
        "ignoreEpisodesWithoutFiles": False,
        "searchForMissingEpisodes": True
    }
    json_data = {
            "title": title,
            "images": images,
            "seasons": seasons,
            "path": path,
            "profileId": 6,
            "monitored": True,
            "qualityProfileId": 6,
            "languageProfileId": 1,
            "tvRageId": tvrage_id,
            "tvdbId": tvdb_id,
            "titleSlug": title_slug,
            "addOptions": opts
    }
    return json_data
    # TODO: Make it search better (currently grabs the top result because of the programmer's laziness)


def listSeries():
    series = requests.get(f"{base_string}/series" + key_string_2).json()
    for i in range(len(series)):
        print(f"{i + 1}. {series[i]['title']} ({series[i]['network']})")

def deleteShow(search):
    show_id = lookup(search)
    result = requests.get(f"{base_string}/series/{show_id}" + key_string).json()
    # TODO: show details and confirm
    requests.delete(f"{base_string}/series/{show_id}", )
    

def addShow(search):
    info = lookup(search)
    print(str(info))
    print(requests.post(f"{base_string}/series" + key_string_2, data=json.dumps(info)).json())


#series = requests.get(f"{base_string}/series" + key_string_2).json()[1]
#print(series)
#listSeries()
#lookup("Mad Men")

addShow("tvdb:368207")

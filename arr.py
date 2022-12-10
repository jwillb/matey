from urllib.parse import quote
import requests, json

class SonarrInstance:
    def __init__(self, api_key, base_url):
        self.__api_key = api_key
        self.__base_url = base_url
    def lookup(self, term):
        result = requests.get(f"{self.__base_url}/series/lookup?term={quote(term)}&apikey={self.__api_key}").json()[0]
        #for i in range(5):
        #    print(f"{i + 1}. {result[i]['title']}")
        #result = result[int(input("> ")) - 1]
        #print(f"Selected {result['title']} ({result['year']})")
        
        title = result["title"]
        year = result["year"]

        tvdb_id = result["tvdbId"]
        tvrage_id = result["tvRageId"]
        title_slug = result["titleSlug"]
        
        images = result["images"]
        seasons = result["seasons"]
        
        for i in range(len(seasons)):
            seasons[i]["monitored"] = True
        
        path = f"/tv/{title}"
        opts = {
            "ignoreEpisodesWithFiles": False,
            "ignoreEpisodesWithoutFiles": False,
            "searchForMissingEpisodes": True,
            "monitor": "all"
        }

        json_data = {
                "title": title,
                "images": images,
                "seasons": seasons,
                "path": path,
                "profileId": 4, # 6 is 720/1080, 4 is 1080
                "monitored": True,
                "qualityProfileId": 4,
                "languageProfileId": 1,
                "tvRageId": tvrage_id,
                "tvdbId": tvdb_id,
                "titleSlug": title_slug,
                "addOptions": opts
        }
        return json.dumps(json_data), title, year

    def listSeries(self):
        series = requests.get(f"{self.__base_url}/series?apikey={self.__api_key}").json()
        answer = ""
        for i in range(len(series)):
            answer += (f"{i + 1}. {series[i]['title']} ({series[i]['network']})\n")
        return answer

    def addSeries(self, show):
        code = requests.post(f"{self.__base_url}/series?apikey={self.__api_key}", data=show)
        return code

class RadarrInstance:
    def __init__(self, api_key, base_url):
        self.__api_key = api_key
        self.__base_url = base_url

    def listMovies(self):
        result = requests.get(f"{self.__base_url}/movie?apikey={self.__api_key}").json()
        answer = ""
        for i in range(len(result)):
            answer += f"{i + 1}. {result[i]['title']} ({result[i]['year']})\n"
        return answer

    def lookup(self, term):
        result = requests.get(f"{self.__base_url}/movie/lookup?term={quote(term)}&apikey={self.__api_key}").json()[0]
        #for i in range(len(result)):
        #    print(f"{i + 1}. {result[i]['title']} ({result[i]['year']})")
        #result = result[int(input("> ")) - 1]
        #print(f"Selected {result['title']} ({result['year']})")

        title = result["title"]
        year = result["year"]

        quality = 4
        tmdb_id = result["tmdbId"]

        opts = {
            "monitor": "movieOnly",
            "searchForMovie": True

        }

        json_data = {
            "title": title,
            "path": f"/movies/{title} ({year})",
            "qualityProfileId": quality,
            "monitored": True,
            "tmdbId": tmdb_id,
            "addOptions": opts
        }
        #return json.dumps(json_data)
        return json.dumps(json_data), title, year

    def addMovie(self, movie):
        headers = {"Content-type": "application/json"}
        code = requests.post(f"{self.__base_url}/movie?apikey={self.__api_key}", data=movie, headers=headers)
        return code


if __name__ == "__main__":
    sonarr = SonarrInstance(s_api_key, s_base_string)
    radarr = RadarrInstance("8c81cce814564c40a74902bc9252bca8", "http://192.168.1.101:7878/api/v3")
    movie = radarr.lookup("uncut gems")
    radarr.addMovie(movie)








'''
def lookup(search):
    query = quote(search)
    result = requests.get(f"{base_string}/series/lookup?term={query}" + key_string).json()[0]
    title = result["title"]
    year = result["year"]
    print(f"Found: {title} ({year})")
    tvdb_id = result["tvdbId"]
    tvrage_id = result["tvRageId"]
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
            "profileId": 4, # 6 is 720/1080, 4 is 1080
            "monitored": True,
            "qualityProfileId": 4,
            "languageProfileId": 1,
            "tvRageId": tvrage_id,
            "tvdbId": tvdb_id,
            "titleSlug": title_slug,
            "addOptions": opts
    }
    return json_data
    # TODO: Make it search better (currently grabs the top result because of the programmer's laziness)



def deleteShow(search):
    show_id = lookup(search)
    result = requests.get(f"{base_string}/series/{show_id}" + key_string).json()
    # TODO: show details and confirm
    requests.delete(f"{base_string}/series/{show_id}", )
    

def addShow(search):
    info = lookup(search)
    print(requests.post(f"{base_string}/series" + key_string_2, data=json.dumps(info)).json())


series = requests.get(f"{base_string}/series" + key_string_2).json()[0]
print(series)
#listSeries()

addShow(input("Show to add: "))
'''

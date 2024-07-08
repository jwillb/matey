from urllib.parse import quote
import requests, json

class SonarrInstance:
    def __init__(self, api_key, base_url):
        self.__api_key = api_key
        self.__base_url = base_url
    def lookup(self, term):
        result = requests.get(f"{self.__base_url}/series/lookup?term={quote(term)}&apikey={self.__api_key}").json()[0]
        
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
        return json.dumps(json_data), title, year

    def addMovie(self, movie):
        headers = {"Content-type": "application/json"}
        code = requests.post(f"{self.__base_url}/movie?apikey={self.__api_key}", data=movie, headers=headers)
        return code

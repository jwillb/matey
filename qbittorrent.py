import requests

class qBittorrentInstance:
    def __init__(self, base_url, username, password):
        self.__base_url = base_url
        self.__api_url = self.__base_url + "/api/v2"
        self.__header = {"Referer": base_url}
        self.__login_data = {"username": username, "password": password}
        self.__auth_cookie = None
    
    def login(self):
        self.__auth_cookie = requests.post(self.__api_url + "/auth/login", data=self.__login_data, headers = self.__header).cookies.get_dict()
    
    def __queryApi(self, endpoint):
        return requests.post(self.__api_url + endpoint, cookies=self.__auth_cookie, headers=self.__header)
    def __postApi(self, endpoint, post_data):
        status_code = requests.post(self.__api_url + endpoint, data=post_data, cookies=self.__auth_cookie, headers=self.__header)
        return status_code

    def getInfo(self):
        version = self.__queryApi("/app/version").text
        web_version = self.__queryApi("/app/webapiVersion").text
        bitness = self.__queryApi("/app/buildInfo").json()["bitness"]
        info_string = f"qBittorrent {version} (web version: {web_version}) {bitness}-bit"
        return info_string

    def getSpeeds(self):
        json_data = self.__queryApi("/transfer/info").json()
        down_speed = json_data["dl_info_speed"]
        up_speed = json_data["up_info_speed"]
        return (down_speed, up_speed)

    def getTorrentList(self):
        torrents_json = self.__queryApi("/torrents/info").json()
        torrent_list = []
        for i in range(len(torrents_json)):
            torrent_list.append((torrents_json[i]["name"][:30], torrents_json[i]["category"], torrents_json[i]["dlspeed"], round(torrents_json[i]["ratio"], 2)))
        return torrent_list

    def addTorrent(self, magnet, category):
        status_code = self.__postApi("/torrents/add", {"urls": magnet, "category": category})
        return status_code


if __name__ == "__main__":
    qbit_instance = qBittorrentInstance("http://192.168.1.101:8080", "admin", "adminadmin")
    qbit_instance.login()
    qbit_instance.addTorrent("magnet:?xt=urn:btih:35e11d5099dc8f2bfe93b963ea51543ae5c021bf&tr=https://ipleak.net/announce.php%3Fh%3D35e11d5099dc8f2bfe93b963ea51543ae5c021bf&dn=ipleak.net+torrent+detection", "discord")

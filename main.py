from riot_api import RiotAPI
import decouple

APIKEY = decouple.config("token")
region = "americas"
platform_id = "na1"
myapp = RiotAPI(region, platform_id, APIKEY)

myapp.GET_players()
request = myapp.request_queue.queue.pop()
request.attempt_request()
results = request.request_results.json()
for player in results:
    myapp.GET_summoner_by_summoner_id(player["summonerId"])
    _request = myapp.request_queue.queue.pop()
    _request.attempt_request()
    _results = _request.request_results.json()
    print("summoner info",player)
    print("player info:",_results)
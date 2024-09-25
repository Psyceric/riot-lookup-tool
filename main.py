from league_relay import LeagueRelay
import decouple

api_key = decouple.config("APIKEY")
regions = eval(decouple.config("REGIONS"))
_region = "americas"
platform_id = "na1"
rank = "CHAMPION"
tier = "I"

league_relay = LeagueRelay(_region, platform_id, rank, tier, api_key)
league_relay.test()

print("All Platforms in this enviorment\n---------------------------------")
for region in regions.items():
    for platform in region[1]:
        print(":".join((str(region[0]), str(platform))))
print("---------------------------------")
        
# myapp.GET_players()
# request = myapp.request_queue.queue.pop()
# request.attempt_request()
# results = request.request_results.json()


# print(cur.lastrowid)

# #for player in results:
# myapp.GET_summoner_by_summoner_id(player["summonerId"])
# _request = myapp.request_queue.queue.pop()
# _request.attempt_request()
# _results = _request.request_results.json()

# myapp.GET_matches(puuid=_results['puuid'], count=100)
# _r2 = myapp.request_queue.queue.pop()
# _r2.attempt_request()
# _res2 = _r2.request_results.json()

# #cur.execute("INSERT INTO newtable VALUES (?,?)",(1,1))
# print("summoner info",player)
# print("player info:",_results)
# store_profile(player|_results)
# print("matches:", _res2)

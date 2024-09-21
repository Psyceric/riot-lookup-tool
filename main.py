from riot_api import RiotAPI
import decouple, sqlite3

api_key = decouple.config("APIKEY")
regions = eval(decouple.config("REGIONS"))
_region = "americas"
platform_id = "na1"
myapp = RiotAPI(_region, platform_id, api_key)

league = sqlite3.connect("LeagueOfLegends.db")
cur = league.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS application_info (app_launch datetime, game_version text, ddragon_version text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS player_info (local_player_id int primary key,  puuid text, summonerId text, 
            game_name text, tag_line text, tier text, rank text, profileIconId int, wins int, losses int, region text, 
            platform_id text, last_modified datetime, revisionDate datetime)""")

cur.execute("""CREATE TABLE IF NOT EXISTS player_matches (local_player_id int, match_id text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS match_info (matchId text, platformId text, region text, gameMode text, mapId int, 
            gameStartTimestamp datetime, gameDuration int, winner int, player1_par_id int, player1_loc_id int, player2_par_id int,
             player2_loc_id int, player3_par_id int, player3_loc_id int, player4_par_id int, player4_loc_id int, player5_par_id int,
             player5_loc_id int, player6_par_id int, player6_loc_id int, player7_par_id int, player7_loc_id int, player8_par_id int,
             player8_loc_id int, player9_par_id int, player9_loc_id int, player10_par_id int, player10_loc_id int)""")

cur.execute("""CREATE TABLE IF NOT EXISTS player_performance(player_performance_id int primary key, matchId text, 
            local_player_id int, participantId int, championId int, championName text, championLevel int, role text, 
            teamPosition text, kills int, deaths, int, assists int, goldEarned int, goldSpent int, summoner1Id int, 
            summoner2Id int, item0 int, item1 int, item2 int, item3 int, item4 int, item5 int, item6 int, vissionScore int, 
            physicalDamageDealt int, physicalDamageDealthToChampions int, physicalDamageTaken int, magicDamageDealth int, 
            magicDamageDealthToChampions int, magicDamageTaken int, tueDamageDealt int, trueDamageDealtToChampions int, 
            trueDamageTaken int, totalDamageDealt int, totalDamageDealtToChampions int, totalDamageTaken int, totalHeal int, 
            totalMinionsKilled int, win bool)""")

league.commit()

values = {}
# cur.execute(
#     """INSERT INTO Media (id, title, type, onchapter, chapters, status)
#      VALUES (:id, :title, :type, :onchapter, :chapters, :status);""", 
#     values
# )

# TODO: COMBINE THE INFORMATION FROM PLAYER INFO WITH OUR NEW DATA <---

for region in regions.items():
    for platform in region[1]:
        print(":".join((str(region[0]), str(platform))))
        
myapp.GET_players()
request = myapp.request_queue.queue.pop()
request.attempt_request()
results = request.request_results.json()

for player in results:
    myapp.GET_summoner_by_summoner_id(player["summonerId"])
    _request = myapp.request_queue.queue.pop()
    _request.attempt_request()
    _results = _request.request_results.json()

    myapp.GET_matches(puuid=_results['puuid'], count=100)
    _r2 = myapp.request_queue.queue.pop()
    _r2.attempt_request()
    _res2 = _r2.request_results.json()

    #cur.execute("INSERT INTO newtable VALUES (?,?)",(1,1))
    print("summoner info",player)
    print("player info:",_results)
    print("matches:", _res2)
    

    # How do I make this continue to do the things it needs to, and decides for itself.
    # Every time we get a page of players, We must than loop through all 
    
    # match Data : 
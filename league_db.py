import decouple, sqlite3
from league_relay import LeagueInterfact
class LeagueDatabase(LeagueInterfact):
    PROFILE = eval(decouple.config("PROFILE"))
    database_connection = None
    cursor = None
    name = "LeagueDatabase"
    def __init__(self):
        self.database_connection = sqlite3.connect("LeagueOfLegends.db")
        self.cursor = self.database_connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS application_info (app_launch datetime, game_version text, ddragon_version text)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS player_profiles (local_user_id INTEGER PRIMARY KEY,  puuid text, summonerId text, 
                    game_name text, tag_line text, tier text, rank text, profileIconId int, wins int, losses int, region text, 
                    platform_id text, last_modified datetime, revisionDate datetime)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS player_matches (local_user_id int, match_id text, player_id int)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS match_info (matchId text, platformId text, region text, gameMode text, mapId int, 
                    gameStartTimestamp datetime, gameDuration int, winner int, par_id_p1 int, par_id_p2 int, par_id_p3 int, 
                    par_id_p4 int, par_id_p5 int, par_id_p6 int, par_id_p7 int, par_id_p8 int, par_id_p9 int, par_id_p10 int)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS player_performance(player_performance_id int primary key, matchId text, 
                    local_user_id int, participantId int, championId int, championName text, championLevel int, role text, 
                    teamPosition text, kills int, deaths, int, assists int, goldEarned int, goldSpent int, summoner1Id int, 
                    summoner2Id int, item0 int, item1 int, item2 int, item3 int, item4 int, item5 int, item6 int, vissionScore int, 
                    physicalDamageDealt int, physicalDamageDealthToChampions int, physicalDamageTaken int, magicDamageDealth int, 
                    magicDamageDealthToChampions int, magicDamageTaken int, tueDamageDealt int, trueDamageDealtToChampions int, 
                    trueDamageTaken int, totalDamageDealt int, totalDamageDealtToChampions int, totalDamageTaken int, totalHeal int, 
                    totalMinionsKilled int, win bool)""") #change to player_participation 
        self.database_connection.commit()

def store_profile(self,account_info):
    # Hard code last_modified, rank, tier, platform, region
    player_profile = dict(self.PROFILE, **account_info)
    self.cursor.execute("""
        INSERT INTO player_profiles (puuid, summonerId, game_name, tag_line, tier, rank, profileIconId, wins, losses, region, platform_id, last_modified, revisionDate)
        VALUES (:puuid, :summonerId, :game_name, :tag_line, :tier, :rank, :profileIconId, :wins, :losses, :region, :platform_id, :last_modified, :revisionDate); 
        """,player_profile)
    self.database_connection.commit()

def store_match(self, match_info):
    # get region from breaking down match name, first part is platform, and use regions .env to find "key" - check if previously stored in matches db.
    #str.split('-')[0]?
  
    match_details = dict(self.MATCH, **match_info)
    #TODO: sqlite3 insert command 
    pass

def store_participation(self, participation_info):
    participation_details = dict(self.PARTICIPANT, **participation_info)
    #TODO: sqlite3 insert command in player_performance - triggered by relay
    pass

def application_init(self):
    # Get information about league and DDragon, and if we need to update DDragon.
    #Z
    pass
def get_loc_from_nametag(self, game_name, tag_line):
    # Get the local_user_id from name and tag
    pass
def create_shallow_player(self, puuid, summonerId , game_name, tag_line, profIconId, region, platform_id):
    # Using the most available information to create a player profile
    pass
def create_deep_player(self, puuid, summonerId, game_name, tag_line, profIconId, region, platform_id, tier, rank, wins, losses, revisionDate):
    # Given all the required information create a new entry deep player entry into the DB
    pass
def upgrade_shallow_to_deep(self, local_user_id, tier, rank, wins, losses, region, platform_id, revision_date):
    # Upgrades an existing Shallow player profile to one with complete information
    pass
def upgrade_participation_to_shallow(self, participation_dict):
    # Store participation information in DB, and create a new shallow player profile if it is not in they are not in the DB already
    pass
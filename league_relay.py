class LeagueRelay():

    league_database = None
    riot_api = None
    requests_manager = None
    region = None
    platform_id = None

    def __init__(self, region, platform_id, rank, tier, api_key) -> None:
        from league_db import LeagueDatabase
        from riot_api import RiotAPI
        from requests_manager import RequestManager
        self.league_database = LeagueDatabase()
        self.league_database._connect(self)
        self.riot_api = RiotAPI(api_key)
        self.riot_api._connect(self)
        self.requests_manager = RequestManager()
        self.requests_manager._connect(self)

        self.region = region
        self.platform_id = platform_id
        self.rank = rank
        self.tier = tier

    def find_player(self):
        self.league_database.find_player()

    def test(self):
        self.league_database.print_name()
        self.riot_api.print_name()
        self.requests_manager.print_name()

class LeagueInterfact():
    league_relay = None
    def _connect(self, league_relay):
        self.league_relay = league_relay
    @property
    def region(self):
        return self.league_relay.region
    @region.setter
    def set_region(self,region):
       self.league_relay.region = region
    @property
    def platform_id(self):
        return self.league_relay.platform_id
    @platform_id.setter
    def set_platform_id(self,platform_id):
        self.league_relay.platform_id = platform_id
    @property
    def rank(self):
        return self.league_relay.platform_id
    @rank.setter
    def set_rank(self,rank):
        self.league_relay.rank = rank
    @property
    def tier(self):
        return self.league_relay.tier
    @tier.setter
    def set_tier(self,tier):
        self.league_relay.tier = tier
        
    def print_name(self):
        print(self.name)
    
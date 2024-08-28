import requests
from ratelimit import limits, sleep_and_retry, RateLimitException
from backoff import on_predicate, on_exception, expo
from threading import Thread, _active
import time
import sqlite3
import ctypes

class RiotAPI():
    region : str
    api_key : str
    cache = []
    variable_name : Thread


    RATE_LIMIT_SECOND = 20 
    RATE_LIMIT_TWO_MINUTE = 60

    def learning(self):
        for x in range(0,90):
            #print(x)
            self.attempt_request(x)
        pass

    def __init__(self, api_key : str, region : str):
        self.variable_name = Thread(target = self.learning, daemon = True)
        self.variable_name.start()
        time.sleep(3)
        print("TEST")
        self.api_key = api_key
        self.region = region
        _name = "Psyceric"
        _tag = "773"
        test  = "https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{NAME}/{TAG}".format(REGION = region, NAME = _name, TAG = _tag)
        url = RiotAPI.assemble_url(test, api_key = api_key, count = 1)
        self.variable_name.join()
        time.sleep(5)
        print("Slept")

    @limits(calls = RATE_LIMIT_SECOND, period = 1)
    @limits(calls = RATE_LIMIT_TWO_MINUTE, period = 120)
    def attempt_request(self, url):
            print(url)
            time.sleep(.05)

    @staticmethod
    def assemble_url(url, **parameters):
        if parameters is not None:
            for count, param in enumerate(parameters.items()):
                url_id = '&'
                if count == 0:
                    url_id = '?'
                url += '{url_id}{key}={value}'.format(url_id = url_id, key=param[0],value = param[1])
        return url

    """def account_info(self, username, tag):
        pass

    def get_PUUID(self, username):

        # RIOT API Call to get PUUID from username
        # https://{region}.api.riotgames.com
        # /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?{api_key =Key}
        # https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/psyceric/773?api_key=RGAPI-90c6c992-0078-4122-b166-cf437de40b0b

        # Returns:
        # {"puuid":"g8qIcET1Jh994x69PaN5rJ0UcEbo8TtAJGDd66MwezLG9MzlhBUlCma5H--87m8tqYXpEFZsluLBqw","gameName":"Psyceric","tagLine":"773"} dict

        pass
    def get_matches(self, count, PUUID):
        # RIOT API Call to get dict of previous games
        # /lol/match/v5/matches/by-puuid/{puuid}/ids&{api_key = Key}

        # Returns 
        # [
        # "NA1_4887498560",
        # "NA1_4887465300",
        # "NA1_4887425408",
        # ...]

        pass

    def get_summoner(self, PUUID):
        # RIOT API Call to get summoner Mastery
        # /lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}&{count = count}&{api_key = Key}

        # Returns 
        # {
        # "id": "5SMTK8DTh8kMHOEl_zkw2667KsMBxTROCloaOboQ-JDz19Q",
        # "accountId": "A1d4SbmmvKDzRBls753FJjmOeu5M5vir7KUwFLkgYimma4A",
        # "puuid": "paTeopWaB8znvUgQRJtgUsIxXNOoxH9d7N1DD0TtsfDrnekdOC5Y0wyycrP8h6EvQqyn9i8fs1iVXg",
        # "profileIconId": 5408,
        # "revisionDate": 1704939516000,
        # "summonerLevel": 75
        # }
        pass

    def get_assets(self, character_id):
        # RIOT API Call to get character assets from DDragon
        pass"""

if __name__ == "__main__":   
     
    key = r"RGAPI-90c6c992-0078-4122-b166-cf437de40b0b"
    region = "americas"
    myapp = RiotAPI(key, region)
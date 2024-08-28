import requests
from threading import Thread, _active, Event, RLock
import sys
from math import floor
import time

now = time.monotonic if hasattr(time, 'monotonic') else time.time

class RateLimit():
    def __init__(self, calls=15, period=900, clock=now):
        self.clamped_calls = max(1, min(sys.maxsize, floor(calls)))
        self.period = period
        self.clock = clock

        # Initialise the decorator state.
        self.last_reset = clock()
        self.num_calls = 0

        # Add thread safety.
        self.lock = RLock()

    def __period_remaining(self):
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed

    def __call__(self):
        with self.lock:
            period_remaining = self.__period_remaining()

            # If the time window has elapsed then reset.
            if period_remaining <= 0:
                self.num_calls = 0
                self.last_reset = self.clock()

            # Increase the number of attempts to call the function.
            self.num_calls += 1

            # If the number of attempts to call the function exceeds the
            # maximum then raise an exception.
            if self.num_calls > self.clamped_calls:
                return True
            return False

class RiotAPI():
    region : str
    api_key : str
    cache = []
    _attempt_thread : Thread

    # Create QUEUE of requests that are set to be sent out.

    def learning(self):
        for x in range(0,90):
            #print(x)
            self.attempt_request(x)
        pass

    # def __init__(self, api_key : str, region : str):
    #     self.variable_name = Thread(target = self.learning, daemon = True)
    #     self.variable_name.start()
    #     time.sleep(3)
    #     print("TEST")
    #     self.api_key = api_key
    #     self.region = region
    #     _name = "Psyceric"
    #     _tag = "773"
    #     test  = "https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{NAME}/{TAG}".format(REGION = region, NAME = _name, TAG = _tag)
    #     url = RiotAPI.assemble_url(test, api_key = api_key, count = 1)
    #     self.variable_name.join()
    #     time.sleep(5)
    #     print("Slept")

    def __init__(self, api_key : str, region : str):
        self.current_request = r"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/psyceric/773?api_key=RGAPI-90c6c992-0078-4122-b166-cf437de40b0b"
        self.limitA = RateLimit(calls=20, period=1)
        self.limitB = RateLimit(calls=60, period=120)
        for x in range(0,100):
            self.attempt_request(x)
            

    def attempt_request(self, url):
        _failure_event = Event()
        self._attempt_thread = Thread(target=self.send_request, kwargs = {'_fail_event' : _failure_event, 'url' : url})
        self._attempt_thread.start()
        self._attempt_thread.join()
        if _failure_event.is_set():
            print("Rate Limited :", now())
        time.sleep(.1)

    def send_request(self, _fail_event , url):
        if self.limitA() or self.limitB():
            _fail_event.set()
        else:
            print(url) # Try Request...
        

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
import requests
from threading import Thread, _active, Event, RLock
import sys
from save_thread_result import ThreadWithResult, _runOverrideThreadWithResult
from math import floor
from queue import Queue
import time
import json

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

class ExponentialTimer():
    current_iteration : int = 0
    enabled : bool  = True
    hold_time : float 
    total_elapsed : float 
    def __init__(self, give_up_threshold : float, multiplier : float = .5, exponent : float = 2, offset_y : float = 0, offset_x : float = 0):
        self.multiplier = multiplier
        self.exponent = exponent
        self.offset_y = offset_y
        self.offset_x = offset_x
        self.give_up_threshold = give_up_threshold
        self.hold_time = 0
        self.total_elapsed = 0

    def iterate(self):
        self.current_iteration += 1
        print(self.give_up_threshold , " - ", self.current_iteration)
        self.hold_time = ((self.multiplier * self.current_iteration) + self.offset_x) ** self.exponent + self.offset_y
        self.total_elapsed = self.total_elapsed + self.hold_time
        print("Elapsed Time : {0}\nTrying Again in... {1}".format(self.total_elapsed, self.hold_time))
        if self.give_up_threshold <= 0: return self.hold_time
        if self.give_up_threshold <= self.current_iteration :
            self.enabled = False
            return False
        return self.hold_time

            
        

class MyRequest():
    attempt_thread : ThreadWithResult
    rate_limits : list[RateLimit]
    request_results : json

    def __init__(self, request_url, rate_limits: list[RateLimit] | RateLimit = RateLimit(20,1), retry : bool = True, intreval : int = 10, **kwargs):
        self.request_url = request_url
        self.payload = dict(kwargs)
        self.rate_limits = rate_limits
        self.retry = retry
        self.interval = intreval

    def attempt_request(self):

        """
        
        #TODO: Impliment Locks to create threads safely, Impliment Request Retry with exponential cooldown
        
        """

        _rate_overflow_event = Event()
        _fail_event = Event()
        _expo_timer = ExponentialTimer(give_up_threshold=0)
        response : _runOverrideThreadWithResult = None
        status_code = 0
        while _expo_timer.enabled and status_code is not 200:
            self.attempt_thread = ThreadWithResult(target=self.send_request, kwargs = {'_rate_overflow_event' : _rate_overflow_event, '_fail_event' : _fail_event})
            self.attempt_thread.start()
            self.attempt_thread.join()
            response = self.attempt_thread
            if hasattr(response.result, "status_code"):
                status_code = response.result.status_code
                if status_code == 200:
                    print("Fetching Response Value...\n",response.result.json(), "\n")
                    return response.result.json()
            print("--------",status_code)
            if _rate_overflow_event.is_set():
                print("Rate Overflow... Retrying")
            elif _fail_event.is_set():
                print("Unable to complete request... Status Code : ", status_code)
            _expo_timer.iterate()
            if _expo_timer.enabled: 
                time.sleep(_expo_timer.hold_time)


    def send_request(self, _rate_overflow_event, _fail_event):
        if [x for x in self.rate_limits if x() is True]:
            _rate_overflow_event.set()
            return
        #print("Base" , r"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/psyceric/773?api_key=RGAPI-60922bae-ab77-41a3-b37a-67de1ae7ebe1")
        my_response = requests.get(self.request_url, params= self.payload)
        self.pretty_print_POST(my_response.request)
        if my_response.status_code is not 200:
            _fail_event.set()
            return
        print('Response Code :' , my_response.status_code)
        return my_response
        #print(my_response.json()['puuid'])
        

    def pretty_print_POST(self,req):
        """
        At this point it is completely built and ready
        to be fired; it is "prepared".

        However pay attention at the formatting used in 
        this function because it is programmed to be pretty 
        printed and may differ from the actual request.
        """
        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

class RiotAPI():  
    region : str
    api_key : str
    request_queue : Queue
    

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
        self.current_request = r"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/psyceric/773"
        self.request_queue = Queue()
        limitA = RateLimit(calls=20, period=1)
        limitB = RateLimit(calls=60, period=120)
        for x in range(0,90):
            #print(x)
            my_request = MyRequest(self.current_request,[limitA, limitB], api_key = api_key)
            my_request.attempt_request()


    def queue_request(self, url):
        self.request_queue.put(url)



    
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
     
    key = r"RGAPI-c1ae88f9-5189-4281-a2bc-b699f2be919d"
    region = "americas"
    myapp = RiotAPI(key, region)
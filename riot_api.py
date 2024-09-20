import sys, time, json, requests
from threading import Thread, _active, Event, RLock
from save_thread_result import ThreadWithResult, _runOverrideThreadWithResult
from math import floor
from queue import Queue

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
    name = "JOE"

    def __init__(self, request_url, rate_limits: list[RateLimit] | RateLimit = RateLimit(20,1), **payload):
        self.request_url = request_url
        self.payload = dict(payload)
        self.rate_limits = rate_limits

    def attempt_request(self):
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
                    #print("Fetching Response Value...\n",response.result.json(), "\n")
                    print("Fetching Results")
                    return response.result.json()
            print("--------",status_code)
            if _rate_overflow_event.is_set():
                print("Rate Overflow... Retrying")
            elif _fail_event.is_set():
                print("Unable to complete request... Status Code : ", status_code)
            _expo_timer.iterate()
            if _expo_timer.enabled: 
                time.sleep(_expo_timer.hold_time)
    # Add logger logic to document status codes and association to the request event.
    # TODO : Properly pass in attempt_request information, regarding URL, and Payload. 

    def send_request(self, _rate_overflow_event, _fail_event):
        if [x for x in self.rate_limits if x() is True]:
            _rate_overflow_event.set()
            return
        #print("Base" , r"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/psyceric/773?api_key=RGAPI-60922bae-ab77-41a3-b37a-67de1ae7ebe1")
        my_response = requests.get(self.request_url, params = self.payload)
        self.pretty_print_POST(my_response.request)
        if my_response.status_code is not 200:
            _fail_event.set()
            return
        print('Response Code :' , my_response.status_code)
        self.request_results = my_response
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
    platform_id : str
    APIKEY : str
    request_queue : Queue
    rate_limits : list[RateLimit]

    def __init__(self, region : str, platform_id : str, api_key : str):
        
        self.region = region
        self.platform_id = platform_id
        self.APIKEY = api_key
        self.request_queue = Queue()
        limitA = RateLimit(calls=20, period=1)
        limitB = RateLimit(calls=60, period=120)
        self.rate_limits = [limitA, limitB]

    def queue_request(self, url, **payload):
        self.request_queue.put(MyRequest(url, self.rate_limits, **payload))

    def GET_puuid(self, game_name, tag_line):
        url = "https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{_game_name}/{_tag_line}".format(region = self.region, _game_name = game_name, _tag_line = tag_line)
        payload = {"api_key" : self.APIKEY}
        self.queue_request(url=url, **payload)

    def GET_matches(self, puuid, count = 20, **params):
        url = "https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{_puuid}/ids".format(region = self.region, _puuid = puuid)
        payload = dict(params) | {"count" : count, "api_key" : self.APIKEY}
        self.queue_request(url=url, **payload)

    def GET_players(self, queue = "RANKED_SOLO_5x5", tier = "CHALLENGER", division = "I", page = 1):
        url = "https://{platform}.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}".format(platform = self.platform_id, queue = queue, tier = tier, division = division)
        payload = {"page" : page, "api_key" : self.APIKEY}
        self.queue_request(url=url, **payload)

    def GET_match_data(self, match_id):
        url = "https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}".format(region = self.region, match_id = match_id)
        payload = {"api_key" : self.APIKEY}
        self.queue_request(url=url, **payload)
    
    def GET_summoner_by_summoner_id(self, summoner_id):
        url = "https://{platform_id}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}".format(platform_id = self.platform_id, summoner_id = summoner_id)
        payload = {"api_key" : self.APIKEY}
        self.queue_request(url=url, **payload)
    
    def GET_summoner_by_puuid(self, puuid):
        url = "https://{platform_id}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}".format(platform_id = self.platform_id, puuid = puuid)
        payload = {"api_key" : self.APIKEY}
        self.queue_request(url=url, **payload)

    def GET_account_by_puuid(self, puuid):
        url = "https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
        payload = {"api_key" : self.APIKEY}
        self.queue_request(url=url, **payload)

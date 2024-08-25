from tkinter import *
from enum import Enum
from riot_api import RiotAPI
import requests
# Search bar
    # Validate Username
    # Search Username
    # Override Username


class AppController():
    
    class Scenes(Enum):
        ERROR = -1
        STARTUP = 0
        PLAYER_STATS = 1

    scene_directory = {}

    class RiotSearchbar():
        search_callback : callable
        def __init__(self, root : Tk, callback : callable):
            self.search_callback = callback
            # Create GUI elements in Root frame
            # Assign Callback function to to search_username when hitting Enter
            pass

        def search_username(self, username):
            # If user_id passes Regex
            # get PUUID
            # Return PUUID w/ callback
            pass

        def override_username(self, new_name):
            # Set text of Entry to be new value
            pass

    def __init__(self):
        # Create multiple 'scenes' and assign them into the scene_directory dict - scene_dictionary[Scenes.Startup] = Frame
        pass

    def swap_scene(self, scene : Scenes):
        # Set scene_directory[scene] to the top visibility layer
        pass
# -------------------------- API CALLS -------------------

    
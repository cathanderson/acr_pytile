import asyncio
from pytile import async_login
from aiohttp import ClientSession
from datetime import datetime
import time
import json
from dotenv import load_dotenv
import os
import pytz

load_dotenv()

email = CHANGE THIS -- REFER TO SETUP INSTRUCTIONS
password = CHANGE THIS -- REFER TO SETUP INSTRUCTIONS

# Custom JSON encoder class
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
    
def time_since_calc(tile):
    elapsed = datetime.utcnow() - tile.last_timestamp
    if (elapsed.days <= 0) and ((elapsed.seconds // 3600) <= 0):
        elapsed_time_str = ("%02d minutes" % (elapsed.seconds // 60 % 60))
        if elapsed_time_str[0] == '0':
            elapsed_time_str = elapsed_time_str[1:]
    elif elapsed.days <= 0:
        elapsed_time_str = ("%02d hours %02d minutes" % (elapsed.seconds // 3600, elapsed.seconds // 60 % 60))
        if elapsed_time_str[-10] == '0':
            elapsed_time_str = elapsed_time_str[0:-10]+elapsed_time_str[-11:]
        if elapsed_time_str[0] == '0':
            elapsed_time_str = elapsed_time_str[1:]
    else:
        elapsed_time_str = ("%02d days %02d hours %02d minutes" % (elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60))
        if elapsed_time_str[-10] == '0':
            elapsed_time_str = elapsed_time_str[0:-10]+elapsed_time_str[-11:]
        if elapsed_time_str[8] == '0':
            elapsed_time_str = elapsed_time_str[0:8]+elapsed_time_str[9:]
        if elapsed_time_str[0] == '0':
            elapsed_time_str = elapsed_time_str[1:]

    # print("%02d days %02d hours %02d minutes" % (elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60))
    return elapsed_time_str

# while True:
#     time.sleep(900)
async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login(email, password, session)

        # tiles is a dict with tile uuids as keys pointing to tile objects as values
        tiles = await api.async_get_tiles()

        # CBA tile for testing
        # tile = tiles['79846e2286a49c92']

        #create empty dictionary
        data_dict = {}

        for tile_uuid, tile in tiles.items():
            #get time_elapsed_str from helper function
            elapsed_time_str = time_since_calc(tile)
            # print(tile.name)
            # print(elapsed_time_str)
        
            #destructure Tile object into python dict so json doesn't have to direct interact with Tile object
            entry = {
                    'Name': tile.name,
                    'Last Updated': tile.last_timestamp,
                    'Time Since Last Updated': elapsed_time_str,
                    'Longitude': tile.longitude, 
                    'Latitude': tile.latitude,
                    'Accuracy': tile.accuracy,
                    'UUID': tile.uuid,
                    'Dead?': tile.dead
                }
            
            data_dict[tile.name] = entry
            
        # converts dict to json
        json_data = json.dumps(data_dict, cls=DateTimeEncoder)

        # print(json_data)

        with open("C:/Users/cathanderson/OneDrive - A Crane Rental/tiles_data/dead_acr_tiles_json.json", "w") as outfile:
            json.dump(json_data, outfile)



asyncio.run(main())

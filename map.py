from selenium import webdriver
from discord.ext import commands
import discord
import base64
import time
import json

def get_pictures(only_gb=False):
    browser = webdriver.Chrome()
    browser.get('https://www.mapcrunch.com/')

    options = browser.find_element_by_id('options-button')
    options.click()

    urban = browser.find_element_by_id('cities')
    urban.click()

    stealth = browser.find_element_by_id('stealth')
    stealth.click()

    tour = browser.find_element_by_id('tour')
    tour.click()

    if only_gb:
        only_gb = browser.find_element_by_css_selector('.gb') 
        only_gb.click()
    time.sleep(1)
    go_button = browser.find_element_by_id('go-button')
    go_button.click()
    time.sleep(1)
    for i in range(4):
        canvas = browser.find_element_by_css_selector('.widget-scene-canvas')
        canvas_base64 = browser.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

        canvas_png = base64.b64decode(canvas_base64)

        with open(f'canvas_{i}.png', 'wb') as f:
            f.write(canvas_png)

        time.sleep(1.25)
    
    share = browser.find_element_by_id('share-button')
    share.click()
    
    share_url = browser.find_element_by_id('link')
    print(share_url.get_attribute('value'))
    
    with open(f'solution.txt', 'w') as f:
        solution = share_url.get_attribute('value').split('/')[-1]
        solution = solution.split('_')[:2]
        f.write(' '.join(solution))

    browser.close()

bot = commands.Bot(command_prefix='~')
global is_playing 

@bot.command(name='new', help='Starts a new game')
async def new_game(ctx, only_gb: bool=False):
    get_pictures(only_gb)
    files = [discord.File(f'canvas_{i}.png', f'clue_{i}.png') for i in range(4)]
    await ctx.send('Here are your four clues, please submit your answer by writing `~guess` and then a latitude and longitude!', files=files)

@bot.command(name='guess', help='Make a guess for the current game')
async def make_guess(ctx, user_lat: float, user_lon: float):
    with open('solution.txt', 'r') as f:
        contents = f.read()
        lat, lon = contents.split(' ')
        lat = float(lat)
        lon = float(lon)
    

    if abs(user_lat - lat) < 0.01 and abs(user_lon - lon) < 0.01:
        await ctx.send('Congratulations! You have solved this problem. Type `~new` to play another!')
    else:
        await ctx.send('Try again!')


    


with open('auth.json') as f:
    data = json.load(f)

bot.run(data["token"])

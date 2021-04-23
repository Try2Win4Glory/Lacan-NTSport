from bs4 import BeautifulSoup
from json import loads
from re import findall
from requests import get
import json
import aiohttp
import os, copy, random
import time
from compsmongo import DBClient
from mongoclient import DBClient as clientDB
from packages.nitrotype import Racer, Team, cars
from packages.utils import Embed
def player_data(racer):
    newdata = {}
    response = get(f'https://www.nitrotype.com/racer/{racer}').content
    soup = BeautifulSoup(response, 'html5lib')
    for script in soup.find('head'):
        if 'RACER_INFO' in str(script):
            newdata = loads(findall('{".+}', str(script))[0])
            return newdata

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def create_comp(team, compid, endcomptime, authorid):
    async with aiohttp.ClientSession() as session:
        page = await fetch(session, f'https://www.nitrotype.com/api/teams/{team}')
    info = json.loads(page)
    dbclient = DBClient()
    data = {
        "data": {
            "compid": str(compid),
            "players": [],
            "other": {}
        }
    }
    for elem in info['data']['members']:
        if elem['displayName'] != None:
            displayname = elem['displayName']
        else:
            displayname = elem['username']
        try:
            racer = await Racer(elem['username'])
        except:
            continue
        try:
            typed = racer.season_pre['typed']
            secs = racer.season_pre['secs']
            errs = racer.season_pre['errs']
        except:
            typed = 0
            secs = 0
            errs = 0
        data['data']['players'].append({
            "username": elem['username'],
            "starting-races": elem['played'],
            "ending-races": elem['played'],
            "total-races": 0,
            "display": displayname,
            "stillinteam": True,
            "starting-typed": typed,
            "ending-typed": typed, 
            "starting-secs": float(secs), 
            "ending-secs": float(secs),
            "starting-errs": (errs), "ending-errs": (errs)
        })
    data['data']['other'] = {
        "team": team,
        "endcomptime": endcomptime,
        "author": authorid,
        "ended": False
    }
    await dbclient.create_doc(dbclient.db.test, data['data'])
    return True

async def update_comp(compid):
    dbclient = DBClient()
    collection = dbclient.db['test']
    data = await dbclient.get_array(collection, {'$and': [{'compid': compid}, {'compid': compid}]})
    async for d in data:
        data = d
        old = copy.deepcopy(data)
    other = data['other']
    players = data['players']
    team = other['team']
    if round(time.time()) >= other['endcomptime']:
        return
    async with aiohttp.ClientSession() as session:
        page = await fetch(session, f'https://www.nitrotype.com/api/teams/{team}')
    info = json.loads(page)
    try:
        for user in players:
            for elem in info['data']['members']:
                if user['username'] == elem['username']:
                    try:
                        racer = await Racer(user['username'])
                    except:
                        continue
                    try:
                        typed = float(racer.season_pre['typed'])
                        secs = float(racer.season_pre['secs'])
                        errs = float(racer.season_pre['errs'])
                    except:
                        typed = 0
                        secs = 0
                        errs = 0
                    user['ending-races'] = elem['played']
                    user['total-races'] = user['ending-races'] - user['starting-races']
                    user['display'] = elem['displayName']
                    user['stillinteam'] = True
                    user['ending-typed'] = typed
                    user['ending-secs'] = float(secs)
                    user['ending-errs'] = errs
                    try:
                        user['wpm'] = (user['ending-typed']-user['starting-typed'])/5/float(user['ending-secs']-user['starting-secs'])*60
                        user['accuracy'] = 100-(((user['ending-errs']-user['starting-errs'])/(user['ending-typed']-user['starting-typed']))*100)
                        user['points'] = user['total-races']*(100+(user['wpm']/2))*user['accuracy']/100
                    except:
                        user['wpm'] = 0
                        user['accuracy'] = 0
                        user['points'] = 0
                    break
            else:
                user['stillinteam'] = False
        res = [ sub['username'] for sub in players ]
        for elem in info['data']['members']:
            if elem['username'] in res:
                continue
            else:
                players.append({
                    "username": elem['username'],
                    "starting-races": elem['played'],
                    "ending-races": elem['played'],
                    "total-races": 0,
                    "display": elem['displayName'] or elem['username'],
                    "stillinteam": True,
                    "starting-typed": elem['typed'],
                    "ending-typed": elem['typed'], 
                    "starting-secs": float(elem['secs']), 
                    "ending-secs": float(elem['secs']),
                    "starting-errs": (elem['errs']), "ending-errs": (elem['errs'])
                })
    except Exception as e:
        return
    await dbclient.update_array(collection, old, data)
    return data
async def l(compid, category="races"):
    await update_comp(compid)
    dbclient = DBClient()
    collection = dbclient.db['test']
    data = await dbclient.get_array(collection, {'$and': [{'compid': compid}, {'compid': compid}]})
    async for d in data:
        data = d
    usernames = []
    displays = []
    categorylist = []
    for user in data['players']:
        if user['stillinteam'] == False:
            continue
        usernames.append(user['username'].lower())
        displays.append(user['display'])
        if category == "races":
            categorylist.append(user['total-races'])
        elif category == "points":
            categorylist.append(user['points'])
        elif category == "speed":
            categorylist.append(user['wpm'])
        elif category == "accuracy":
            categorylist.append(user['accuracy'])
    sortcategory = sorted(categorylist, reverse=True)
    zipped_lists = zip(categorylist, usernames, displays)
    sorted_zipped_lists = sorted(zipped_lists, reverse=True)
    cleanresult = []
    for t in sorted_zipped_lists:
        cleanresult.append((t[1], t[2], t[0]))

    return ('nothing LMAO', cleanresult)
async def NT_to_discord(id, bypass_verified=False):
    from mongoclient import DBClient
    dbclient = DBClient()
    collection = dbclient.db.NT_to_discord
    data = await dbclient.get_big_array(collection, 'registered')
    for elem in data['registered']:
        if str(id) == elem['userID'] or str(id) == elem['NTuser']:
            if elem['verified'] == 'true' or bypass_verified:
                racer = await Racer(elem['NTuser'])
                return True, racer
            else:
                embed = Embed('Error!', 'You\'re not verified yet!', 'warning')
                return False, embed
    else:
        try:
            return True, await Racer(str(id))
        except:
            embed = Embed('Error!', 'Couldn\'t find that user', 'warning')
            return False, embed
async def get_username(string, bypass=False):
    string = list(str(string))
    if ''.join(string[:3]) == "<@!":
        return await NT_to_discord(''.join(string[3:-1]), bypass)
    if ''.join(string[:2]) == "<@":
        return await NT_to_discord(''.join(string[2:-1]), bypass)
    if len(string) in [17, 18]:
        return await NT_to_discord(''.join(string), bypass)
    else:
        return await NT_to_discord(''.join(string), bypass)
async def check_perms(userid, perms: dict):
    racer = await get_username(userid)
    if racer[0] == False:
        return racer[1]
    racer = racer[1]
    for k in perms.keys():
        if k == "team":
            team = await Team(racer['tag'])
            if perms[k].lower() in [racer['tag'].lower(), team.info['name'].lower()]:
                continue
            else:
                return False
        if k == "membership":
            if perms[k].lower() == 'gold' and racer.membership.lower() == 'gold':
                continue
            elif perms[k].lower() == "basic" and racer.membership.lower() == "basic":
                continue
            else:
                return False
    else:
        return True
async def verify(ctx):
    dbclient = clientDB()
    collection = dbclient.db.NT_to_discord
    dbdata = await dbclient.get_big_array(collection, 'registered')
    for elem in dbdata['registered']:
        if elem['userID'] == str(ctx.author.id):
            racer = await Racer(elem['NTuser'])
            if elem['verified'] == 'false':
                if len(racer.carIDs) > 1:
                    while True:
                        verifycar = cars[random.choice(racer.carIDs)]
                        if verifycar == racer.current_car:
                            continue
                        else:
                            break
                    embed = Embed('Instructions', 'Go to your [Garage](https://nitrotype.com/garage), switch your car to **__' + verifycar + '__** and type `n.verify` again. \n\n *(Please note that this could take up to 15 minutes to work.)*', 'clipboard')
                    

                    await embed.send(ctx)
                    elem['verifyCar'] = verifycar
                    elem['verified'] = 'in progress'
                    #requests.post('https://test-db.nitrotypers.repl.co', data={"key": dbkey, "data": json.dumps(dbdata)})
                    dbclient = clientDB()
                    collection = dbclient.db.NT_to_discord
                    await dbclient.update_big_array(collection, 'registered', dbdata)
                    break
                if len(racer.carIDs) <= 1:
                    embed = Embed('Error', 'Get another car before trying to verifying!', 'warning')
            if elem['verified'] == 'in progress':
                if elem['verifyCar'] == racer.current_car:
                    elem['verified'] = 'true'
                    #requests.post('https://test-db.nitrotypers.repl.co', data={"key": dbkey, "data": json.dumps(dbdata)})
                    dbclient = clientDB()
                    collection = dbclient.db.NT_to_discord
                    await dbclient.update_big_array(collection, 'registered', dbdata)
                    embed = Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server do `n.update` to update your roles.')
                    await embed.send(ctx)
                    break
                else:
                    embed = Embed('<a:error:800338727645216779>  Oh No!', f'Remember to switch your car to **__{elem["verifyCar"]}__**. \nIf there is a problem, just wait a few minutes before trying again. \n\n***(If you just registered, make sure to wait 15 minutes so that I can recognize your equipped car.)*** \n\nIf any problems occur, please make sure to ping / DM **one** of the following people who are able to register you: \n\n**__Developers:__** \n<@505338178287173642> \n<@637638904513691658> \n<@396075607420567552> \n\n**__Helpers:__**\n<@630761745140547625>\n<@731041476322263050> \n<@527937153817116704>')
                    await embed.send(ctx)
                    break
            if elem['verified'] == 'true':
                embed = Embed('LOL', 'You already registered and verified silly!\nIn case this is a premium 💠 server do `n.update` to update your roles.', 'rofl')

                if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
                    embed.footer('Make sure to use n.verify after waiting 15 minutes!\n Become a premium 💠 member today! Run n.premium for more info.', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
                else: 
                    embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')

                await embed.send(ctx)
                break
    #if the for loop doesn't "break"
    else:
        embed = Embed('<a:error:800338727645216779>  Error!', 'Your account isn\'t registered yet.\nAlready registered? Make sure to run `n.verify` to verify your ownership!')
        await embed.send(ctx)
        return
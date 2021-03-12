from bs4 import BeautifulSoup
from json import loads
from re import findall
from requests import get
import json
import aiohttp
import os, copy
import time
from compsmongo import DBClient
from packages.nitrotype import Racer, Team
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
                    "starting-typed": typed,
                    "ending-typed": typed, 
                    "starting-secs": float(secs), 
                    "ending-secs": float(secs),
                    "starting-errs": (errs), "ending-errs": (errs)
                })
    except Exception as e:
        raise e
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
async def NT_to_discord(id):
    from mongoclient import DBClient
    dbclient = DBClient()
    collection = dbclient.db.NT_to_discord
    data = await dbclient.get_big_array(collection, 'registered')
    for elem in data['registered']:
        if str(id) == elem['userID'] or str(id) == elem['NTuser']:
            if elem['verified'] == 'true':
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
async def get_username(string):
    string = list(str(string))
    if ''.join(string[:3]) == "<@!":
        return await NT_to_discord(''.join(string[3:-1]))
    if ''.join(string[:2]) == "<@":
        return await NT_to_discord(''.join(string[2:-1]))
    if len(string) in [17, 18]:
        return await NT_to_discord(''.join(string))
    else:
        return await NT_to_discord(''.join(string))
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
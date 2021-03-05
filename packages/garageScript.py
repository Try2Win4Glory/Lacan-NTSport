import json
from io import BytesIO
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
carsdict = {
    "Lamborgotti Mephisto SS": 1,
    "Lamborgotti Mephisto": 2,
    "Jeepers Rubricorn": 3,
    "Portch Picante": 4,
    "Bantly Super Sport": 5,
    "The Rolls": 6,
    "Winston Citroen": 7,
    "Winston Agile": 8,
    "Rental Car": 9,
    "Mission Accomplished": 10,
    "Buggani Vyrus SS": 11,
    "Auttie B9": 13,
    "Nitsua Lance 722": 14,
    "Misoux Lion": 15,
    "Misoux Toad": 16,
    "Minnie the Cooper": 17,
    "Nizza 350x": 18,
    "One Ace": 19,
    "Cougar Ace": 20,
    "Rand Rover R/T": 21,
    "B-Team Van": 22,
    "Mercedex Bens V-20": 23,
    "Mercedex Bens C-64": 24,
    "Portch Spyder": 25,
    "Auttie Roadster": 26,
    "Bimmer M2.0": 27,
    "Bimmer 9.0t": 28,
    "Thunder Cougarbird": 29,
    "Rat Rod Skully": 30,
    "Outtie R11": 31,
    "The Flamerod": 33,
    "Valent Performo": 34,
    "Portch GT3 RS": 35,
    "Ponce de Leon": 36,
    "'67 Shellback GT-500": 37,
    "Road Warrior": 38,
    "Linux Elise": 39,
    "'69 Shellback RT-500": 40,
    "The Gator": 42,
    "Bastok Suprillia": 43,
    "The Judge": 44,
    "The Stallion": 45,
    "The Macro": 46,
    "The Fastback": 47,
    "The Covenant": 48,
    "The Trifecta": 49,
    "8 Bit Racer": 50,
    "Mini Sherman": 51,
    "Typiano Pizza Car": 52,
    "Rocket Man": 53,
    "All Terrain Vehicle": 54,
    "MP 427": 55,
    "The Wambulance": 56,
    "The Hotdog Mobile": 57,
    "F-35 JSF": 58,
    "NASA Shuttle": 59,
    "Caterham Racer": 60,
    "Mack Daddy": 61,
    "Big Hauler": 62,
    "Big Blue": 63,
    "Fort GT40": 64,
    "Dom Vipper GST-R": 65,
    "Alpha Romero 8Ω": 66,
    "Blazing Buggy": 67,
    "F4U Corsair": 68,
    "Rocket Sleigh": 69,
    "XMaxx Tree Racer": 70,
    "Shadow XMaxx Tree": 71,
    "Party Sleigh": 72,
    "Zonday Tricolore": 73,
    "The Monster": 74,
    "Flux Capacitor": 75,
    "The Gotham": 76,
    "The Pirc": 77,
    "Suziki GXRS 1200": 78,
    "EZ Rider": 79,
    "Lamborgotti AdventX": 80,
    "Summer Classic": 81,
    "Hang Ten": 82,
    "'41 Woodie Deluxx": 83,
    "Hang Eleven": 84,
    "'41 Woodie Sunshine": 85,
    "The Xcelsior V12": 86,
    "'68 Roadtripper": 87,
    "Hang Fifteen": 88,
    "Wach 6": 89,
    "Fort F-125": 90,
    "Wisker Electric": 91,
    "'67 Vette": 92,
    "MSG 01": 93,
    "Fort Stallion": 94,
    "Police Bimmer": 95,
    "Auttie R-8.1": 96,
    "Wampus": 97,
    "Pumpkin Hauler": 98,
    "Wreath Racer": 99,
    "Santa's Buggy": 100,
    "Travis' Car": 101,
    "Dark Elf": 102,
    "The Golden Gift": 103,
    "Corndogs Car": 104,
    "14 Mantaray": 105,
    "Ferreti Samsher 458": 106,
    "Lacan Hypersport": 107,
    "Sun Buggie": 108,
    "Hammer Wheels": 110,
    "Kringle 4000": 111,
    "Buddy's Snowmobile": 112,
    "Kringle 4000 XL": 113,
    "Buddy's Snowmorocket": 114,
    "Six Four": 115,
    "Six Four Plus Three": 116,
    "The Midnight Hauler": 117,
    "The Candy Hauler": 118,
    "Kringle 5000": 119,
    "Wrapped Wracer": 120,
    "Wrapped Wracer GT": 121,
    "Holiday Hero": 122,
    "Kringle 5000 L.T.": 123,
    "Mercedex McLaro SLR": 124,
    "Floaty Blue": 125,
    "B.O.A.T.": 126,
    "I'm Spicy!": 127,
    "Y.A.C.H.T.": 128,
    "Mercedex McLaro SLR 12.5": 129,
    "Nitr-o'-Lantern": 130,
    "Nitr-o'-the-Wisp": 131,
    "Xmaxx Xxpress": 132,
    "XMaxx Xxpress XXL": 133,
    "Gilded Xxpress": 134,
    "Lamborgotti Xmaxx LT": 135,
    "Lamborgotti Xmaxx LT-C": 136,
    "Mercedex McLaro SHS 15.0": 137,
    "Strykist 1300": 138,
    "Range Runner": 139,
    "Strykist 1300 XT-LR": 140,
    "Track-o-Lantern": 141,
    "Gingerbread Racer": 142,
    "Gingerbread Racer H&T": 143,
    "Missile Toe": 144,
    "Missile Toe H&T": 145,
    "The Dark Chocolate Knight": 146,
    "Tegglsa": 149,
    "Egg Beater": 150,
    "Eggcedes": 151,
    "Egg Hauler": 152,
    "Mercedex GT 20.0": 153,
    "Rocky Roo": 154,
    "NitroPAC": 155,
    "Matchbox": 156,
    "Lucky Number 7": 157,
    "Easy Breezy": 158,
    "HoverJet 5000 Mk. 3": 159,
    "Golden Breeze": 160,
    "B.U.S.": 161,
    "S'cool B.U.S.": 162,
    "AU-79": 163,
    "The Underachiever": 164,
    "The Overachiever": 165,
    "The Wildflower": 166,
    "Jolly RS": 167,
    "Jolly GTX LG": 168,
    "The Goldray": 169,
    "can hav nt g0ld plx?": 170,
    "The Wraptor": 171,
    "Travis' Truck": 172,
    "The Wraptor GG": 173,
    "The Silent Knight": 174,
    "NT Gold": 175,
    "Lamborgotti Tiesto": 176,
    "Portch Cobalt": 177,
    "Alpha Romero 123Ω": 178,
    "Travis' Big Truck": 179,
    "Bright Idea": 180,
    "The Sandstorm": 181,
    "The Jury": 182,
    "The Goldfish": 183,
    "Shock Value": 184,
    "Gold Standard": 185,
    "Solar Roller": 186,
    "H2GO": 187,
    "The DevasTater": 188,
    "Creepy Crawler": 189,
    "The Goblin": 190,
    "Something Wicked": 191,
    "Frosted Roller": 192,
    "Gingerbread GT": 193,
    "Holiday Heat": 194,
    "Cold Snap": 195,
    "The Snowy Knight": 196,
    "The Rocket Klaus": 197,
    "Golden Ticket": 198,
    "Wavebreaker": 199,
    "Broadwing": 200,
    "Bimmer Prism i20": 201,
    "Heartbreaker": 202,
    "The Danger 9": 203,
    "The Wild 500": 204,
    "Tigreen": 205,
    "X1 Eclipse": 206,
    "Error 500": 207,
    "Vapor": 208,
    "9 Bit Racer": 209,
    "Chompus\' Wild Ride": 210,
    'Whiplash XS': 211,
    'The Hydro Planer': 212,
    'Timber Speeder': 213,
    'Wampus\' Waffle Wagon': 214,
    'Webmobile Spider': 215,
    'Rand Rover Evar': 216,
    'SpaceZ Crew Draco': 217,
    'MacLaro Sienna': 218,
    'Calculatron': 219,
    'Screw Tank': 220,
    'Hoverbike': 221,
    'Jet Bicycle': 222,
    'Wrapped Flyer': 223,
    'The Festivtank': 224,
    'Bimmer M6': 241,
    'The Dominator': 242,
    'Heartbreaker LV-2': 243
}


async def fetchText(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetchRaw(session, url):
    async with session.get(url) as response:
        return await response.content.read()




async def get_profile(session, username: str):
    playerstat = await fetchText(session, 'https://www.nitrotype.com/racer/'+username)
    soup = BeautifulSoup(playerstat, 'html5lib')
    for script in soup.find('head'):
        if 'RACER_INFO' in str(script):
            newdata = json.loads(re.findall('{".+}', str(script))[0])
            return newdata


async def get_car(session, car_id, car_hue: int = 0, size: str = 'large'):
    host = 'https://www.nitrotype.com/cars'

    if car_hue != 0:
        host += '/painted/%s_%s_1_%s.png' % (car_id, size, car_hue)
    else:
        host += '/%s_%s_1.png' % (car_id, size)
    #r = requests.get(host, stream = True)
    r = await fetchRaw(session, host)
    b = BytesIO()
    #b.write(r.raw.read())
    b.write(r)
    b.seek(0)
    return b



async def compileProfile(username):
    async with aiohttp.ClientSession() as session:
        playerInfo = await get_profile(session, username)
        return playerInfo


async def compileBytes(car_id, car_hue: int = 0, size: str = 'large'):
    async with aiohttp.ClientSession() as session:
        a = await get_car(session, car_id, car_hue, size)
        return a



async def compileProfileAsync(username):
    return await compileProfile(username)


async def compileCarAsync(car_id, car_hue: int = 0, size: str = 'large'):
    return await compileBytes(car_id, car_hue, size)
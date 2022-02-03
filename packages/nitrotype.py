from requests import get, post
import aiocfscrape
from bs4 import BeautifulSoup
from re import findall
from json import loads
import json, re
import datetime
from datetime import date, datetime
from random import randint, choice
from packages.misc import format_number as fn
import aiohttp
import math
import cloudscraper
import functools, asyncio
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
async def api_get(endpoint, session):
    data = await fetch(session, f'https://www.nitrotype.com/api/{endpoint}')
    return data
countries = {
	'AD': 'Andorra',
	'AE': 'United Arab Emirates',
	'AF': 'Afghanistan',
	'AG': 'Antigua & Barbuda',
	'AI': 'Anguilla',
	'AL': 'Albania',
	'AM': 'Armenia',
	'AN': 'Netherlands Antilles',
	'AO': 'Angola',
	'AQ': 'Antarctica',
	'AR': 'Argentina',
	'AS': 'American Samoa',
	'AT': 'Austria',
	'AU': 'Australia',
	'AW': 'Aruba',
	'AZ': 'Azerbaijan',
	'BA': 'Bosnia and Herzegovina',
	'BB': 'Barbados',
	'BD': 'Bangladesh',
	'BE': 'Belgium',
	'BF': 'Burkina Faso',
	'BG': 'Bulgaria',
	'BH': 'Bahrain',
	'BI': 'Burundi',
	'BJ': 'Benin',
	'BM': 'Bermuda',
	'BN': 'Brunei Darussalam',
	'BO': 'Bolivia',
	'BR': 'Brazil',
	'BS': 'Bahama',
	'BT': 'Bhutan',
	'BV': 'Bouvet Island',
	'BW': 'Botswana',
	'BY': 'Belarus',
	'BZ': 'Belize',
	'CA': 'Canada',
	'CC': 'Cocos (Keeling) Islands',
	'CF': 'Central African Republic',
	'CG': 'Congo',
	'CH': 'Switzerland',
	'CI': 'Côte D\'ivoire (Ivory Coast)',
	'CK': 'Cook Iislands',
	'CL': 'Chile',
	'CM': 'Cameroon',
	'CN': 'China',
	'CO': 'Colombia',
	'CR': 'Costa Rica',
	'CU': 'Cuba',
	'CV': 'Cape Verde',
	'CX': 'Christmas Island',
	'CY': 'Cyprus',
	'CZ': 'Czech Republic',
	'DE': 'Germany',
	'DJ': 'Djibouti',
	'DK': 'Denmark',
	'DM': 'Dominica',
	'DO': 'Dominican Republic',
	'DZ': 'Algeria',
	'EC': 'Ecuador',
	'EE': 'Estonia',
	'EG': 'Egypt',
	'EH': 'Western Sahara',
	'ER': 'Eritrea',
	'ES': 'Spain',
	'ET': 'Ethiopia',
	'FI': 'Finland',
	'FJ': 'Fiji',
	'FK': 'Falkland Islands (Malvinas)',
	'FM': 'Micronesia',
	'FO': 'Faroe Islands',
	'FR': 'France',
	'FX': 'France, Metropolitan',
	'GA': 'Gabon',
	'GB': 'United Kingdom (Great Britain)',
	'GD': 'Grenada',
	'GE': 'Georgia',
	'GF': 'French Guiana',
	'GH': 'Ghana',
	'GI': 'Gibraltar',
	'GL': 'Greenland',
	'GM': 'Gambia',
	'GN': 'Guinea',
	'GP': 'Guadeloupe',
	'GQ': 'Equatorial Guinea',
	'GR': 'Greece',
	'GS': 'South Georgia and the South Sandwich Islands',
	'GT': 'Guatemala',
	'GU': 'Guam',
	'GW': 'Guinea-Bissau',
	'GY': 'Guyana',
	'HK': 'Hong Kong',
	'HM': 'Heard & McDonald Islands',
	'HN': 'Honduras',
	'HR': 'Croatia',
	'HT': 'Haiti',
	'HU': 'Hungary',
	'ID': 'Indonesia',
	'IE': 'Ireland',
	'IL': 'Israel',
	'IN': 'India',
	'IO': 'British Indian Ocean Territory',
	'IQ': 'Iraq',
	'IR': 'Islamic Republic of Iran',
	'IS': 'Iceland',
	'IT': 'Italy',
	'JM': 'Jamaica',
	'JO': 'Jordan',
	'JP': 'Japan',
	'KE': 'Kenya',
	'KG': 'Kyrgyzstan',
	'KH': 'Cambodia',
	'KI': 'Kiribati',
	'KM': 'Comoros',
	'KN': 'St. Kitts and Nevis',
	'KP': 'Korea, Democratic People\'s Republic of',
	'KR': 'Korea, Republic of',
	'KW': 'Kuwait',
	'KY': 'Cayman Islands',
	'KZ': 'Kazakhstan',
	'LA': 'Lao People\'s Democratic Republic',
	'LB': 'Lebanon',
	'LC': 'Saint Lucia',
	'LI': 'Liechtenstein',
	'LK': 'Sri Lanka',
	'LR': 'Liberia',
	'LS': 'Lesotho',
	'LT': 'Lithuania',
	'LU': 'Luxembourg',
	'LV': 'Latvia',
	'LY': 'Libyan Arab Jamahiriya',
	'MA': 'Morocco',
	'MC': 'Monaco',
	'MD': 'Moldova, Republic of',
	'MG': 'Madagascar',
	'MH': 'Marshall Islands',
	'ML': 'Mali',
	'MN': 'Mongolia',
	'MM': 'Myanmar',
	'MO': 'Macau',
	'MP': 'Northern Mariana Islands',
	'MQ': 'Martinique',
	'MR': 'Mauritania',
	'MS': 'Monserrat',
	'MT': 'Malta',
	'MU': 'Mauritius',
	'MV': 'Maldives',
	'MW': 'Malawi',
	'MX': 'Mexico',
	'MY': 'Malaysia',
	'MZ': 'Mozambique',
	'NA': 'Namibia',
	'NC': 'New Caledonia',
	'NE': 'Niger',
	'NF': 'Norfolk Island',
	'NG': 'Nigeria',
	'NI': 'Nicaragua',
	'NL': 'Netherlands',
	'NO': 'Norway',
	'NP': 'Nepal',
	'NR': 'Nauru',
	'NU': 'Niue',
	'NZ': 'New Zealand',
	'OM': 'Oman',
	'PA': 'Panama',
	'PE': 'Peru',
	'PF': 'French Polynesia',
	'PG': 'Papua New Guinea',
	'PH': 'Philippines',
	'PK': 'Pakistan',
	'PL': 'Poland',
	'PM': 'St. Pierre & Miquelon',
	'PN': 'Pitcairn',
	'PR': 'Puerto Rico',
	'PT': 'Portugal',
	'PW': 'Palau',
	'PY': 'Paraguay',
	'QA': 'Qatar',
	'RE': 'Réunion',
	'RO': 'Romania',
	'RU': 'Russian Federation',
	'RW': 'Rwanda',
	'SA': 'Saudi Arabia',
	'SB': 'Solomon Islands',
	'SC': 'Seychelles',
	'SD': 'Sudan',
	'SE': 'Sweden',
	'SG': 'Singapore',
	'SH': 'St. Helena',
	'SI': 'Slovenia',
	'SJ': 'Svalbard & Jan Mayen Islands',
	'SK': 'Slovakia',
	'SL': 'Sierra Leone',
	'SM': 'San Marino',
	'SN': 'Senegal',
	'SO': 'Somalia',
	'SR': 'Suriname',
	'ST': 'Sao Tome & Principe',
	'SV': 'El Salvador',
	'SY': 'Syrian Arab Republic',
	'SZ': 'Swaziland',
	'TC': 'Turks & Caicos Islands',
	'TD': 'Chad',
	'TF': 'French Southern Territories',
	'TG': 'Togo',
	'TH': 'Thailand',
	'TJ': 'Tajikistan',
	'TK': 'Tokelau',
	'TM': 'Turkmenistan',
	'TN': 'Tunisia',
	'TO': 'Tonga',
	'TP': 'East Timor',
	'TR': 'Turkey',
	'TT': 'Trinidad & Tobago',
	'TV': 'Tuvalu',
	'TW': 'Taiwan, Province of China',
	'TZ': 'Tanzania, United Republic of',
	'UA': 'Ukraine',
	'UG': 'Uganda',
	'UM': 'United States Minor Outlying Islands',
	'US': 'USA',
	'UY': 'Uruguay',
	'UZ': 'Uzbekistan',
	'VA': 'Vatican City State (Holy See)',
	'VC': 'St. Vincent & the Grenadines',
	'VE': 'Venezuela',
	'VG': 'British Virgin Islands',
	'VI': 'United States Virgin Islands',
	'VN': 'Vietnam',
	'VU': 'Vanuatu',
	'WF': 'Wallis & Futuna Islands',
	'WS': 'Samoa',
	'YE': 'Yemen',
	'YT': 'Mayotte',
	'YU': 'Yugoslavia',
	'ZA': 'South Africa',
	'ZM': 'Zambia',
	'ZR': 'Zaire',
	'ZW': 'Zimbabwe'
}

cars = {
    1 : 'Lamborgotti Mephisto SS',
    2 : 'Lamborgotti Mephisto',
    3 : 'Jeepers Rubicorn',
    4 : 'Portch Picante',
    5 : 'Bantly Super Sport',
    6 : 'The Rolls',
    7 : 'Winston Citroen',
    8 : 'Winston Agile',
    9 : 'Rental Car',
    10 : 'Mission Accomplished',
    11 : 'Buggani Vyrus SS',
    13 : 'Auttie B9',
    14 : 'Nitsua Lance 722',
    15 : 'Misoux Lion',
    16 : 'Misoux Toad',
    17 : 'Minnie the Cooper',
    18 : 'Nizza 350x',
    19 : 'One Ace',
    20 : 'Cougar Ace',
    21 : 'Rand Rover R/T',
    22 : 'B-Team Van',
    23 : 'Mercedex Bens V-20',
    24 : 'Mercedex Bens C-64',
    25 : 'Portch Spyder',
    26 : 'Auttie Roadster',
    27 : 'Bimmer M2.0',
    28 : 'Bimmer 9.0t',
    29 : 'Thunder Cougarbird',
    30 : 'Rat Rod Skully',
    31 : 'Outtie R11',
    33 : 'The Flamerod',
    34 : 'Valent Performo',
    35 : 'Portch GT3 RS',
    36 : 'Ponce de Leon',
    37 : '\'67 Shellback GT-500',
    38 : 'Road Warrior',
    39 : 'Linux Elise',
    40 : '\'69 Shellback RT-500',
    42 : 'The Gator',
    43 : 'Bastok Suprillia',
    44 : 'The Judge',
    45 : 'The Stallion',
    46 : 'The Macro',
    47 : 'The Fastback',
    48 : 'The Covenant',
    49 : 'The Trifecta',
    50 : '8 Bit Racer',
    51 : 'Mini Sherman',
    52 : 'Typiano Pizza Car',
    53 : 'Rocket Man',
    54 : 'All Terrain Vehicle',
    55 : 'MP 427',
    56 : 'Wambulance',
    57 : 'Hotdog Mobile',
    58 : 'F-35 JSF',
    59 : 'NASA Shuttle',
    60 : 'Caterham Racer',
    61 : 'Mack Daddy',
    62 : 'Big Hauler',
    63 : 'Big Blue  ',
    64 : 'Fort GT40',
    65 : 'Dom Vipper GST-R',
    66 : 'Alpha Romero 8Ω',
    67 : 'Blazing Buggy',
    68 : 'F4U Corsair',
    69 : 'Rocket Sleigh',
    70 : 'XMaxx Tree Racer',
    71 : 'Shadow Xmaxx Tree',
    72 : 'Party Sleigh',
    73 : 'Zonday Tricolore',
    74 : 'The Monster',
    75 : 'Flux Capacitor',
    76 : 'The Gotham',
    77 : 'The Pirc',
    78 : 'Suziki GXRS 1200',
    79 : 'EZ Rider',
    80 : 'Lamborgotti AdventX',
    81 : 'Summer Classic',
    82 : 'Hang Ten',
    83 : '\'41 Woodie Deluxx',
    84 : 'Hang Eleven',
    85 : '\'41 Woodie Sunshine',
    86 : 'The Xcelsior V12',
    87 : '\'68 Roadtripper',
    88 : 'Hang Fifteen',
    89 : 'Wach 6',
    90 : 'Fort F-125',
    91 : 'Wisker Electric',
    92 : '\'67 Vette',
    93 : 'MSG 01',
    94 : 'Fort Stallion',
    95 : 'Police Bimmer',
    96 : 'Auttie R-8.1',
    97 : 'Wampus',
    98 : 'Pumpkin Hauler',
    99 : 'Wreath Racer',
    100 : 'Santa\'s Buggy',
    101 : 'Travis\' Car',
    102 : 'Dark Elf',
    103 : 'The Golden Gift',
    104 : 'Corndog\'s Car',
    105 : '\'14 Mantaray',
    106 : 'Ferreti Samsher 458',
    107 : 'Lacan Hypersport',
    109 : 'Sun Buggie',
    110 : 'Hammer Wheels',
    111 : 'Kringle 4000',
    112 : 'Buddy\'s Snowmobile',
    113 : 'Kringle 4000 XL',
    114 : 'Buddy\'s Snowmorocket',
    115 : 'Six Four',
    116 : 'Six Four Plus Three',
    117 : 'The Midnight Hauler',
    118 : 'The Candy Hauler',
    119 : 'Kringle 5000',
    120 : 'Wrapped Wracer',
    121 : 'Wrapped Wracer GT',
    122 : 'Holiday Hero',
    123 : 'Kringle 5000 L.T.',
    124 : 'Mercedex McLaro SLR',
    125 : 'Floaty Blue',
    126 : 'B.O.A.T.',
    127 : 'I\'m Spicy!',
    128 : 'Y.A.C.H.T.',
    129 : 'Mercedex McLaro SLR 12.5',
    130 : 'Nitr-o\'-Lantern',
    131 : 'Nitr-o\'-the-Wisp',
    132 : 'Xmaxx Xxpress',
    133 : 'XMaxx Xxpress XXL',
    134 : 'Gilded Xxpress',
    135 : 'Lamborgotti Xmaxx LT',
    136 : 'Lamborgotti Xmaxx LT-C',
    137 : 'Mercedex McLaro SHS 15.0',
    138 : 'Strykist 1300',
    139 : 'Range Runner',
    140 : 'Strykist 1300 XT-LR',
    141 : 'Track-o\'-Lantern',
    142 : 'Gingerbread Racer',
    143 : 'Gingerbread Racer H&T',
    144 : 'Missile Toe',
    145 : 'Missile Toe H&T',
    146 : 'The Dark Chocolate Knight',
    149 : 'Teggsla',
    150 : 'Egg Beater',
    151 : 'Eggcedes',
    152 : 'Egg Hauler',
    153 : 'Mercedex GT 20.0',
    154 : 'Rocky Roo',
    155 : 'NitroPAC',
    156 : 'Matchbox',
    157 : 'Lucky Number 7',
    158 : 'Easy Breezy',
    159 : 'HoverJet 5000 Mk. 3',
    160 : 'Golden Breeze',
    161 : 'B.U.S.',
    162 : 'S\'cool B.U.S.',
    163 : 'AU-79',
    164 : 'The Underachiever',
    165 : 'The Overachiever',
    166 : 'The Wildflower',
    167 : 'Jolly RS',
    168 : 'Jolly GTX LG',
    169 : 'The Goldray',
    170 : 'can hav nt g0ld plx?',
    171 : 'The Wraptor',
    172 : 'Travis\' Truck',
    173 : 'The Wraptor GG',
    174 : 'The Silent Knight',
    175 : 'NT Gold',
    176 : 'Lamborgotti Tiesto',
    177 : 'Portch Cobalt',
    178 : 'Alpha Romero 123Ω',
    179 : 'Travis\' Big Truck',
    180 : 'Bright Idea',
    181 : 'Sandstorm',
    182 : 'The Jury',
    183 : 'The Goldfish',
    184 : 'Shock Value',
    185 : 'Gold Standard',
    186 : 'Solar Roller',
    187 : 'H2GO',
    188 : 'The DevasTater',
    189 : 'Creepy Crawler',
    190 : 'The Goblin',
    191 : 'Something Wicked',
    192 : 'Frosted Roller',
    193 : 'Gingerbread GT',
    194 : 'Holiday Heat',
    195 : 'Cold Snap',
    196 : 'The Snowy Knight',
    197 : 'The Rocket Klaus',
    198 : 'Golden Ticket',
    199 : 'Wavebreaker',
    200 : 'Broadwing',
    201 : 'Bimmer Prism i20',
    202 : 'Heartbreaker',
    203 : 'The Danger 9',
    204 : 'The Wild 500',
    205 : 'Tigreen',
    206 : 'X1 Eclipse',
    207 : 'Error 500',
    208 : 'Vapor',
    209 : '9 Bit Racer',
    210 : 'Chompus\' Wild Ride',
    211 : 'Whiplash XS',
    212 : 'The Hydro Planer',
    213 : 'Timber Speeder',
    214 : 'Wampus\' Waffle Wagon',
    215 : 'Webmobile Spider',
    216 : 'Rand Rover Evar',
    217 : 'SpaceZ Crew Draco',
    218 : 'MacLaro Sienna',
    219 : 'Calculatron',
    220 : 'Screw Tank',
    221 : 'Hoverbike',
    222 : 'Jet Bicycle',
    223: 'Wrapped Flyer',
    224: 'The Festivitank',
    225: 'Typiano Pizza Car',
    226: 'Buggani Vyrus LR',
    227: 'Jet Powered Truck',
    228: 'Lamborgotti Vengeance',
    230: 'X2 Eclipse',
    232: 'Monster Truck Redux',
    233: 'Covenant Leo',
    234: 'Zonday Tricolore 2021',
    235: 'Strykist 1300',
    236: 'The Glamrod',
    237: 'Linux Elipse',
    238: 'Road Warrior Rally',
    239: 'Furious Maxx',
    241: 'Bimmer M6',
    242: 'The Dominator',
    243: 'Heartbreaker LV-2',
    244: 'Ice Hauler',
    245: 'The Kelvin',
    246: 'Buggani Vyrus LR',
    247: 'Error 503',
    249: 'Sprinter \'90',
    252: 'Koromoto DJ Cruiser',
    253: 'Koromoto GT-R',
    254: 'Koromoto GT-R LS',
    255: 'Stingtec Technotruck',
    256: 'Four Leaf Rover',
    257: 'Corsa Iris',
    258: 'Sprinter \'90 Vapor',
    259: 'Winson Track\'d',
    261: 'Stingtec Marianas',
    262: 'Personal Water Craft',
    263: 'Blitz T8 Roadster',
    264: 'Liberty Demon XRT',
    266: 'Mongoose SU-5'

}

class NewsClass:
    def __init__(self):
        return
    async def create_attr(self):
        loop = asyncio.get_running_loop()
        scraper = cloudscraper.create_scraper()
        fut = await loop.run_in_executor(None, functools.partial(scraper.get,f'https://www.nitrotype.com/api/news'))
        raw_data = json.loads(fut.text)
        '''async with aiocfscrape.CloudflareScraper() as session:
            raw_data = loads(await api_get('news', session))'''

        if not raw_data['success']:
            raise Exception("News couldn't be fetched")
        
        raw_data = [news for idx, news in enumerate(raw_data['data']) if idx < 5]

        self.data = []
        
        for news in raw_data:
            news_dictionary = {
                'title' : news['title'],
                'description' : news["shortBody"],
                'author' : news['writtenBy'],
                'created' : date.fromtimestamp(news['createdStamp']).strftime('%d %B %Y'),
                'link' : f'https://nitrotype.com/news/read/{news["blogID"]}/{news["slug"]}',
                'image' : f'https://www.nitrotype.com/uploads/newsimage/{news["blogID"]}/{news["lastModified"]}'
            }

            self.data.append(news_dictionary)
async def News():
    news = NewsClass()
    await news.create_attr()
    return news
shadowcars = {
    1:'https://cdn.discordapp.com/attachments/763376521674620928/763376541270671400/H1wjIAAAAASUVORK5CYII.png',
    2:'https://cdn.discordapp.com/attachments/763376521674620928/763377013800697876/wdegexqaZNU2AAAAABJRU5ErkJggg.png',
    3:'https://cdn.discordapp.com/attachments/763376521674620928/763377157409210388/UbKHC2vdl48AAAAASUVORK5CYII.png',
    4:'https://cdn.discordapp.com/attachments/763376521674620928/763377459314950174/Db2Bzxd3hkFQAAAABJRU5ErkJggg.png',
    5:'https://media.discordapp.net/attachments/763376521674620928/763377566274682940/rKbI2a6LwP8DnU2eCbYj11sAAAAASUVORK5CYII.png',
    6:'https://cdn.discordapp.com/attachments/763376521674620928/763377705797419028/TbNz0VKupqAyzAalc0RPpum76Cvz91HuRoKAJJnQAAAABJRU5ErkJggg.png',
    7:'https://cdn.discordapp.com/attachments/763376521674620928/763378262746857522/HiMXriMAAAAASUVORK5CYII.png',
    8:'https://cdn.discordapp.com/attachments/763376521674620928/763378531395960872/wF13UXz2IpR1AAAAABJRU5ErkJggg.png',
    9:'https://cdn.discordapp.com/attachments/763376521674620928/763378679216341032/BWprAAAAAElFTkSuQmCC.png',
    10:'https://cdn.discordapp.com/attachments/763376521674620928/763378801060872192/mVLCNRAIIa2B4sWew1EciAnzDbXkWRCcnYsjGxPOKf0XW6KcPQhcEAIhpAsC9gJO6wxuD5fhEiihOmTlwlL6L6AOWUQOINACOnqd.png',
    11:'https://cdn.discordapp.com/attachments/763376521674620928/763378968640225300/WSMZEBnySMYAAAAASUVORK5CYII.png',
    12:'https://cdn.discordapp.com/attachments/763376521674620928/763379096867569684/UQAAAABJRU5ErkJggg.png',
    13:'https://cdn.discordapp.com/attachments/763376521674620928/763379271397539860/YpqVx5WZ9D3RFqV19V8156qYTzLrjafxxIRCLaZ7j3SdKrT05c1b3POFIqw8NgRDT4YwoYxkNzeGM51H35H8BmFMViClzfbIAAAA.png',
    14:'https://cdn.discordapp.com/attachments/763376521674620928/763379380663222303/YPANQRCKBGKIBAEZkMghDIblDlREAgCIZTIQBAIArMhEEKZDcqcKAgEgRBKZCAIBIHZEAihzAZlThQEgkAIJTIQBILAbAiEUGaDM.png',
    15:'https://cdn.discordapp.com/attachments/763376521674620928/763379508820181022/wPiXXtBu70QPgAAAABJRU5ErkJggg.png',
    16:'https://media.discordapp.net/attachments/764077712641228860/764082932335378442/AQ2jkqSLUU6aAAAAAElFTkSuQmCC.png',
    17:'https://cdn.discordapp.com/attachments/763376521674620928/763379783853277226/UQAAAABJRU5ErkJggg.png',
    18:'https://cdn.discordapp.com/attachments/763376521674620928/763379890103517204/4Bx1AG25eDQx5JBvew5wt8zkH2dhGX0ob8Hs9gx97ZOnFImW1F1lSvSuJ6ezsQyrAiCnVgFzIpzddsN6mN7ZAjHDfVwJkS1ynF3K.png',
    19:'https://cdn.discordapp.com/attachments/763376521674620928/763379996152430592/wPg4Jr42BbUjgAAAABJRU5ErkJggg.png',
    20:'https://cdn.discordapp.com/attachments/763376521674620928/763380234875174992/O6TffOFD6N8FOn6Qj8P929XVjxDFcpAAAAAElFTkSuQmCC.png',
    21:'https://cdn.discordapp.com/attachments/763376521674620928/763380351111659540/xeLHpXBMKDMSAAAAABJRU5ErkJggg.png',
    22:'https://cdn.discordapp.com/attachments/763376521674620928/763380510113923072/txm0ydQ64TG33kLYzVNYUfC4cbiGe7WKGCcEKB4GrxJMR0ArxoPGg2UA2pA3gxWdWbDZtDjxEoHNtELhQCIR4tnen93VANMSTYWZ.png',
    23:'https://cdn.discordapp.com/attachments/763376521674620928/763380615910522941/zm7sPj2AAAAABJRU5ErkJggg.png',
    24:'https://cdn.discordapp.com/attachments/763376521674620928/763380742079512576/7RKAAAAAElFTkSuQmCC.png',
    25:'https://cdn.discordapp.com/attachments/763376521674620928/763380838908952627/NBdcHgIhhuX1aVoUBE5GIMRwMoS5QBBYHgIhhuX1aVoUBE5GIMRwMoS5QBBYHgIhhuX1aVoUBE5G4P8AtUSZ4zs9Y7YAAAAASUVO.png',
    26:'https://cdn.discordapp.com/attachments/763376521674620928/763381005700169728/A5jZ00nnAqeXAAAAAElFTkSuQmCC.png',
    27:'https://media.discordapp.net/attachments/763376521674620928/763381135170076682/A3eCtLu7IBUFAAAAAElFTkSuQmCC.png',
    28:'https://media.discordapp.net/attachments/763376521674620928/763381224403763220/oAAAAASUVORK5CYII.png',
    29:'https://media.discordapp.net/attachments/763376521674620928/763381315688726528/E3o1sDeRdbAAAAABJRU5ErkJggg.png',
    30:'https://media.discordapp.net/attachments/763376521674620928/763381403772911636/AHFKLz3DlzwnAAAAAElFTkSuQmCC.png',
    31:'https://media.discordapp.net/attachments/763376521674620928/763381522614714388/t0EmBhr94AMAAAAASUVORK5CYII.png',
    32: None,
    33:'https://media.discordapp.net/attachments/763376521674620928/763381718656614420/44SPEY2QTWY3XtrG167exPdFRCKHtO8Dnwc6T38JY2hbG6LmiAMy5kq4HlyvKjJ9OnFqsPYxwQx9hlFso6GNyN8faZ528saqPJbk.png',
    34:'https://media.discordapp.net/attachments/763376521674620928/763381811497664542/vjUOEDT122wAAAAASUVORK5CYII.png',
    35:'https://media.discordap.net/attachments/763376521674620928/763381944662491136/tZjlpbqIGPlb6MNrXWwOmthSSMIUSxB6bT2marTHhv4Rdp3j3hNtvSLAHla3Sd3GwSCwNYIhCi2hi4HBoFEAhR9FPXKWkQ2BqBEM.png',
    36:'https://media.discordapp.net/attachments/763376521674620928/763382076362719232/oSti36BeaLBSJNCoA55qpHKtfyagO8QPlqSVwcnBseJXYTaCyFdhFpKGddAwKacx9bZt7m2X9PZ1DXZ8WiCEyGkNUQ9z7xICGxKY.png',
    37:'https://media.discordapp.net/attachments/763376521674620928/763382166108766279/4ZGZh4ExK5AAAAABJRU5ErkJggg.png',
    38:'https://media.discordapp.net/attachments/764077712641228860/764084799509757972/wcogBlLc1nzLgAAAABJRU5ErkJggg.png',
    39:'https://media.discordapp.net/attachments/763376521674620928/763382425827934288/Icdgx3Pm7fEThuh9n3u9DYe0n6iq7pK49gGzLOOWEEiC2BKQO7pN3V5JDDsCfq2PSYJYa8tnvROBDgSSIDpAylMSgbUi8P89z37b.png',
    40:'https://media.discordapp.net/attachments/763376521674620928/763382528295305226/IVNMe1qQAAAAASUVORK5CYII.png',
    #41 not available
    42:'https://media.discordapp.net/attachments/763376521674620928/763382677457469480/ORhqMiEse1RAIYTMUgsCCEAhhF9RZqWoQCGEzBoLAghAIYRfUWalqEAhhMwaCwIIQCGEX1FmpahAIYTMGgsCCEAhhF9RZqWoQCGE.png',
    43:'https://media.discordapp.net/attachments/763376521674620928/763382779823652864/dch3IvfWLX3kf1bmofmaneaa0ULCq1WbiOxeoTt7US6QXkxIhIBGUeS923kPRnuYkB1fCtCgrHtIHPQH0PMpY7qUm7WvYNNSqNNS.png',
    44:'https://media.discordapp.net/attachments/764077712641228860/764085796088578078/kB1npIUaITkvTHqiDxAdvwDmuqUuQvSDXTqHbuwJlddVhvsMFE3hbULinPBNy251X1eQmj5k7PKb1sPf15bUVVrBYuo1MhmmiQM8.png',
    45:'https://media.discordapp.net/attachments/763376521674620928/763382962443911168/xuv9oDtvMVgAAAABJRU5ErkJggg.png',
    46:'https://media.discordapp.net/attachments/763376521674620928/763383043469475881/5HeTZMNXLrgAAAAASUVORK5CYII.png',
    47:'https://media.discordapp.net/attachments/763376521674620928/763383125266530314/YAuIrjmeAAAAAASUVORK5CYII.png',
    48:'https://media.discordapp.net/attachments/763376521674620928/763383266715238400/msrpdJwPQAAAAASUVORK5CYII.png',
    49:'https://media.discordapp.net/attachments/763376521674620928/763383356674539570/weMDN4TswKgQAAAABJRU5ErkJggg.png',
    50:'https://media.discordapp.net/attachments/763376521674620928/763383460538613790/weHAwW4eFcw3AAAAABJRU5ErkJggg.png',
    51:'https://media.discordapp.net/attachments/763394761397633045/763394959826223144/5JhUxd09gBgAAAABJRU5ErkJggg.png',
    #52 not available
    53:'https://media.discordapp.net/attachments/763394761397633045/763395111245447218/FreYOzI5iiwAAAABJRU5ErkJggg.png',
    54:'https://media.discordapp.net/attachments/763394761397633045/763395195165212712/LlgG9deqIXwAAAABJRU5ErkJggg.png',
    55:'https://media.discordapp.net/attachments/763394761397633045/763395275062509588/NJmxwiYAAAAAElFTkSuQmCC.png',
    56:'https://media.discordapp.net/attachments/763394761397633045/763395355185512458/ASE9jOXUWKbsAAAAAElFTkSuQmCC.png',
    57:'https://media.discordapp.net/attachments/763394761397633045/763395440691380254/f9gIQpTFcnJDwAAAABJRU5ErkJggg.png',
    58:'https://media.discordapp.net/attachments/763394761397633045/763395581623271474/Lh3hejAAAAAElFTkSuQmCC.png',
    59:'https://media.discordapp.net/attachments/763394761397633045/763395671952457788/V2vFbJOsyUUAAAAASUVORK5CYII.png',
    60:'https://media.discordapp.net/attachments/763394761397633045/763395945760292874/1Ft9gCnTA3uDO76Pgr8H7oCrp5reoKAAAAAElFTkSuQmCC.png',
    61:'https://media.discordapp.net/attachments/763394761397633045/763396029194043452/wNfBApFrfXj0QAAAABJRU5ErkJggg.png',
    62:'https://media.discordapp.net/attachments/763394761397633045/763396113096900648/oGD7AAAAABJRU5ErkJggg.png',
    63:'https://media.discordapp.net/attachments/763394761397633045/763396239445852200/wcmxATGgtG3CAAAAABJRU5ErkJggg.png',
    64:'https://media.discordapp.net/attachments/763394761397633045/763396359340425246/DzEhKF3LHBWAAAAABJRU5ErkJggg.png',
    65:'https://media.discordapp.net/attachments/763394761397633045/763396448003686420/A66MChZyNceAAAAAElFTkSuQmCC.png',
    66:'https://media.discordapp.net/attachments/763394761397633045/763396522489937920/WunUTuUXl32CvKk4DOdx3GRxYkCIScTBILAegTD6TiVKG6rbiHAAAAAElFTkSuQmCC.png',
    67:'https://media.discordapp.net/attachments/763394761397633045/763396738756509737/QiIaaN4qo7Pa19X1SYKUUSICslPz58HWnQAJk3Uco27dSCvwfWOJXPX42G4gAAAAASUVORK5CYII.png',
    68:'https://media.discordapp.net/attachments/763394761397633045/763397156476157962/gwgcg4oOoZR1PLLeTYDN9LfOOA1MgAWcewSPowMW4jCq1vBCnABuLVLHYWKR3zBHtAmTW2wAsAA9cjAEGkLGeBqCJZu8Em3nrmHc.png',
    69:'https://media.discordapp.net/attachments/763394761397633045/763397242790608906/OE8H2QNhSvAAAAAASUVORK5CYII.png',
    70:'https://media.discordapp.net/attachments/763394761397633045/763397329541398578/0fNvlPJIdfMzu8AljjMeSF8ep4AAAAASUVORK5CYII.png',
    71:'https://media.discordapp.net/attachments/763394761397633045/763397970506022932/li9nfa3NH9rGqbhyhYOOILQs9vKnEwzDJYv2UpaZqTopCD1Vd12spBZu8FEFll4lYmlJ4XxloZL5VYcvBIt2vTMMvT1ZinZUr9dn.png',
    72:'https://media.discordapp.net/attachments/763394761397633045/763398095147892786/AzY1hFTIP984AAAAAElFTkSuQmCC.png',
    73:'https://media.discordapp.net/attachments/763394761397633045/763398171233484840/M9gvACf66REAAAAASUVORK5CYII.png',
    74: 'https://media.discordapp.net/attachments/764077712641228860/764078308605296640/NrBIc7MokJwAAAAASUVORK5CYII.png',
    75:'https://media.discordapp.net/attachments/763394761397633045/763398403152543784/wMMZ4fFgoqwwAAAABJRU5ErkJggg.png',
    76:'https://media.discordapp.net/attachments/764077712641228860/764091371791056946/D5u3Jb4m82BLAAAAAElFTkSuQmCC.png',
    77:'https://media.discordapp.net/attachments/763394761397633045/763398555934785566/IBVW5XvMCzHzHdF38eWlYDXpBUFtPIOoLySI4mJ3Qmw8gjP2jb5J9W70C2AAAAAElFTkSuQmCC.png',
    78:'https://media.discordapp.net/attachments/763394761397633045/763398712813944862/wdX9ZIhwjVgAAAABJRU5ErkJggg.png',
    79:'https://media.discordapp.net/attachments/763394761397633045/763398804875509760/AeTD43kmJUBOAAAAAElFTkSuQmCC.png',
    80:'https://media.discordapp.net/attachments/763394761397633045/763398888156954624/0yOOw5UAAAAAElFTkSuQmCC.png',
    81:'https://media.discordapp.net/attachments/763394761397633045/763398971510489088/lAAAAAElFTkSuQmCC.png',
    82:'https://media.discordapp.net/attachments/763394761397633045/763399179032592405/QP4G84CzMRy1Cgei9dlVKyiWz6yKnK63GwnZLNFwDGdBS8dVVX89UqywlnjdXYTWBvMQUyGcsSQHmZAQzkhkJTPkfTkonu9pq3Ll.png',
    83:'https://media.discordapp.net/attachments/763394761397633045/763399246225080360/84BKmgMAAAAASUVORK5CYII.png',
    84:'https://media.discordapp.net/attachments/763394761397633045/763399329141620736/MZKp669nw5Ekt3NJJA3MQzZiQ4KGMwAlZAU0pla6z5dL3qq0ysWh7RUBrStuzFuYvDH3HRWlQ083IdAAAAAElFTkSuQmCC.png',
    85:'https://media.discordapp.net/attachments/763394761397633045/763399408838246440/bTofCZIfuqbbGVsCpJ9WpqG7zquoXkdmQvbMnLSuuoS5k9WpXRVZJzNuHAkV33uK2AeTObzJfEAT2gIDND72necg7XY9ZRlRnqiH.png',
    86:'https://media.discordapp.net/attachments/763394761397633045/763399505995366407/xliL05bVHWwAAAAAElFTkSuQmCC.png',
    87:'https://media.discordapp.net/attachments/763394761397633045/763399574823763978/CyI8qIofsM5yGwB8dg1qOiynWRLb4fU74gRH1jgICuSsGwAAAABJRU5ErkJggg.png',
    88:'https://media.discordapp.net/attachments/763394761397633045/763399646772985886/RVNgJwUa7DtJ1Bc0BS6DAg32yjHfoumwE4KNNh3kqgvaApcBgXH8zyY2KjTABfAAAAAElFTkSuQmCC.png',
    89:'https://media.discordapp.net/attachments/763394761397633045/763399721158705182/3PYU9gQ0po6FYnJDEqohnv9ki8H8E1A8fOEAAawAAAABJRU5ErkJggg.png',
    90:'https://media.discordapp.net/attachments/763394761397633045/763399805623205888/Wev0AxXNedQ2lsKe4tgb5E75mBHNIzjbKxCuEFtxu31yvwxOdOTLRtE3H8f1BgFwr8PxFZjnlqUXUGAAAAAElFTkSuQmCC.png',
    91:'https://media.discordapp.net/attachments/763394761397633045/763399884564332565/oo4jECIYyBUAAAAASUVORK5CYII.png',
    92:'https://media.discordapp.net/attachments/763394761397633045/763399959805952011/B5BwXQXuKLEjAAAAAElFTkSuQmCC.png',
    93:'https://media.discordapp.net/attachments/763394761397633045/763400040340914227/9hQN8lLCrdQAAAAASUVORK5CYII.png',
    94:'https://media.discordapp.net/attachments/763394761397633045/763400110771535893/wTDKgAzkRT8AAAAASUVORK5CYII.png',
    95:'https://media.discordapp.net/attachments/763394761397633045/763400179298598952/UjqFmMP4hZt30LAohosNp66O70v8HVcmF3dZEelkAAAAASUVORK5CYII.png',
    96:'https://media.discordapp.net/attachments/763394761397633045/763400250022690816/AfYFogGBFu96AAAAAElFTkSuQmCC.png',
    97:'https://media.discordapp.net/attachments/763394761397633045/763400325012127744/YMMQAAAABJRU5ErkJggg.png',
    98:'https://media.discordapp.net/attachments/763394761397633045/763400418150580234/r5rMv8ZowAAAABJRU5ErkJggg.png',
    99:'https://media.discordapp.net/attachments/763394761397633045/763400510265884685/CMI7BcCx5lgxuwzJgEmf1V5eiPgYd4JX4s9YI5D4fsaQWl39CZSO8xry7GCwLFF4DgTzJR9xt6HbbwXh3ETxjwp9lj5ug7jXDlGE.png',
    100:'https://media.discordapp.net/attachments/763394761397633045/763400586162339840/4zlLOnchKuAAAAAElFTkSuQmCC.png',
    101:'https://media.discordapp.net/attachments/763401031341834241/763401046109585408/V5BxbGXBzvSObAhw4AtEYDhzShQ8ciopcJbLvcEuZt00egf8HHKK2Q9C9Q8IAAAAASUVORK5CYII.png',
    102:'https://media.discordapp.net/attachments/763401031341834241/763401131388567552/SmGlHFGHJdg6pDenFNGymGusbFTpKRQEt0MoDDOvyDksliLh6awQagS0iGKoSY7A1Tia43DMIQUoIoczyU7CFrKuzI5HyNpULcDp.png',
    103:'https://media.discordapp.net/attachments/763401031341834241/763401214318477343/APWQjcU3xkrwAAAAAElFTkSuQmCC.png',
    104:'https://media.discordapp.net/attachments/764077712641228860/764097060151492628/wNdNukunu0CsgAAAABJRU5ErkJggg.png',
    105:'https://media.discordapp.net/attachments/764077712641228860/764097376922632222/1yAQKmADoAAAAASUVORK5CYII.png',
    106:'https://media.discordapp.net/attachments/763401031341834241/763401496800788501/iuR7oq3aPlKMR1TGUEZh1LPXkOgW0i8L847QO2Nwyq7AAAAABJRU5ErkJggg.png',
    107:'https://media.discordapp.net/attachments/763401031341834241/763401629859840080/A8dZzqeMKUhOAAAAAElFTkSuQmCC.png',
    #108:Not available.
    109:'https://media.discordapp.net/attachments/763401031341834241/763401773243170826/Hy7MXAS6WGAAAAAAElFTkSuQmCC.png',
    110:'https://media.discordapp.net/attachments/763401031341834241/763401854004101130/WISmAC0GUvtgKRmKF8BOoBG6CTio20nxmjcpm857cfMQlMALrOC61AlGhhZwZCgCfRude52jzLlMAjIoEJQNd9kfvkOTWf68p5nu.png',
    111:'https://media.discordapp.net/attachments/763401031341834241/763401976637554728/xcUkBIHG49UZQAAAABJRU5ErkJggg.png',
    112:'https://media.discordapp.net/attachments/763401031341834241/763402054781632572/wMhWnJclHJO6AAAAABJRU5ErkJggg.png',
    113:'https://media.discordapp.net/attachments/763401031341834241/763402136423104522/et9EDwZDrSYmK8tVNzvZC68LKwmUBKYlgf8H1KpmB83vXWQAAAAASUVORK5CYII.png',
    114:'https://media.discordapp.net/attachments/763401031341834241/763402264559747122/gHnEC69FFgdVToDju6qewBnCKFCjgnuKs15hXT4EC7uqnsAZwihQo4J7irNeYV0BAu7qp7AGcIoUKOCe4qzXmFdPgQLu6qewBnCK.png',
    115:'https://media.discordapp.net/attachments/764077712641228860/764094370437529620/9e1ItC6HnJAAAAABJRU5ErkJggg.png',
    116:'https://media.discordapp.net/attachments/764077712641228860/764094665418604585/KCYekXl5ZqgAAAABJRU5ErkJggg.png',
    117:'https://media.discordapp.net/attachments/763401031341834241/763402518829989918/1486DAoMBCCgzAWkiwcfmgwKDA8SgwAOt4tB9vHhQYFFhIgQFYCwk2Lh8UGBQ4HgUGYB2P9uPNgwKDAgsp8P8BAD1a08vtxLwAAA.png',
    118:'https://media.discordapp.net/attachments/764077712641228860/764093905926357022/ksQPWaBMd5zkUVGBCL4QRC1hoSIxIPRIGpt5spHSxiyHlieNPI3mOPhMrdMoutmYWYgoxWF9zSUYrtD9XlUCMQ9WOcQes89AkAVc.png',
    119:'https://media.discordapp.net/attachments/763401031341834241/763402682685325322/3S2g0n5kUmBS4EQpMCetGGmJWY1JgUuA0BSZgnabRvGNSYFLgRigwAetGGmJWY1JgUuA0BSZgnabRvGNSYFLgRigwAetGGmJWY1J.png',
    120:'https://media.discordapp.net/attachments/763401031341834241/763402760678014996/B6ttJvy1dAQ2AAAAAElFTkSuQmCC.png',
    121:'https://media.discordapp.net/attachments/763401031341834241/763403013564923944/h91LEsHP0MIwAAAABJRU5ErkJggg.png',
    122:'https://media.discordapp.net/attachments/764077712641228860/764091598552039424/B4xPmpEX9LPXAAAAAElFTkSuQmCC.png',
    123:'https://media.discordapp.net/attachments/763401031341834241/763403184206250024/cQJWygYZ3UknqQ92Pp5tPMSkwKDABa7LCpMCkwMVQYALWxQzV7OikwKTABKzJA5MCkwIXQ4EJWBczVLOjkwKTAhOwJg9MCkwKXAw.png',
    124:'https://media.discordapp.net/attachments/764077712641228860/764098687173263410/V4ynecuMwOoAAAAASUVORK5CYII.png',
    125:'https://media.discordapp.net/attachments/763401031341834241/763403350569517066/4qSNfaLOPRgAAAABJRU5ErkJggg.png',
    126:'https://media.discordapp.net/attachments/764077712641228860/764095875722117120/az5CmBKYEGCUxYNQhrJp0SmBI4ngQmrI4n1nylMCUQIMEJqwahDWTTglMCRxPAhNWx5P9LHlKYEqgQQITVg3CmkmnBKYEjieBCav.png',
    127:'https://media.discordapp.net/attachments/763401031341834241/763403508878671872/ARjjWDFwzSLbAAAAAElFTkSuQmCC.png',
    128:'https://media.discordapp.net/attachments/763401031341834241/763403599455059978/TRQIsM53IkcwqdCpIWd1bdvaVKdnIFWX1Z8nu55tTmvKXY2WT0FhKk8z5WhGMNkEmN4VTs2f70yl9bVUIMCa97SOIDMFOfZck61X.png',
    129:'https://media.discordapp.net/attachments/764077712641228860/764098875702378516/B8dUJehQYxhWgAAAABJRU5ErkJggg.png',
    130:'https://media.discordapp.net/attachments/763401031341834241/763403800286986250/8P1c5cZjbPv5wAAAAASUVORK5CYII.png',
    131:'https://media.discordapp.net/attachments/763401031341834241/763403946336845855/A9LlkQPPH8NAAAAAElFTkSuQmCC.png',
    132:'https://media.discordapp.net/attachments/763401031341834241/763404031166906399/AjrJwQt0gi2AAAAAElFTkSuQmCC.png',
    133:'https://media.discordapp.net/attachments/763401031341834241/763404104675360778/wMk98gQVxA7QAAAABJRU5ErkJggg.png',
    134:'https://media.discordapp.net/attachments/763401031341834241/763404185110577152/8xFkF6DxA6xCoBDYIwJFWHsEv6ouBAqBeQgUYc3Dq84uBAqBPSJQhLVH8KvqQqAQmIdAEdY8vOrsQqAQ2CMCRVh7BLqLgQKgXkIF.png',
    135:'https://media.discordapp.net/attachments/763401031341834241/763404257063206922/wHiJpjj2MdKQAAAABJRU5ErkJggg.png',
    136:'https://media.discordapp.net/attachments/763401031341834241/763404405932032000/wFvFGjjybrLMAAAAABJRU5ErkJggg.png',
    137:'https://media.discordapp.net/attachments/764077712641228860/764099073706819584/y17r0HFhT2CcwtkBDtQcJBNtpZdLaz1QHp9u6NAB5Xd0X6rLSu4S3ultDWCqGaFtWuTIuCChKI9JkfjNt3q5G2hXx1UtjAL2yDwE.png',
    138:'https://media.discordapp.net/attachments/763401031341834241/763404658764283914/z7BT4f7ByedbJcVXAAAAAElFTkSuQmCC.png',
    139:'https://media.discordapp.net/attachments/763401031341834241/763405014949167124/h9lpCo2EfgVTwAAAABJRU5ErkJggg.png',
    140:'https://media.discordapp.net/attachments/763401031341834241/763405092987731968/z7BT4f7ByedbJcVXAAAAAElFTkSuQmCC.png',
    141:'https://media.discordapp.net/attachments/763401031341834241/763405175930748928/AybkvhmHGMOsAAAAAElFTkSuQmCC.png',
    142:'https://media.discordapp.net/attachments/763401031341834241/763405255731445850/AsRSNK2ri9Y6AAAAAElFTkSuQmCC.png',
    143:'https://media.discordapp.net/attachments/763401031341834241/763405366243098704/hgAAAABJRU5ErkJggg.png',
    144:'https://media.discordapp.net/attachments/763401031341834241/763405451656036412/zQZhqzAAAAAElFTkSuQmCC.png',
    145:'https://media.discordapp.net/attachments/763401031341834241/763405529724485663/wKUAAAAASUVORK5CYII.png',
    146:'https://media.discordapp.net/attachments/764077712641228860/764091833184681984/WLASCN1I0dC0o1slttC3UqgKYFWf22FxOjmu3IWv8D1RROkhdrT0MAAAAASUVORK5CYII.png',
    #147:'',o no hoe no pee pee picture
    #148:'',o no hoe no pee pee picture
    149:'https://media.discordapp.net/attachments/763401031341834241/763405795135062026/eObeUHkAAAAAElFTkSuQmCC.png',
    150:'https://media.discordapp.net/attachments/763401031341834241/763405877201076244/sAAAAAElFTkSuQmCC.png',
    151:'https://media.discordapp.net/attachments/763406131431079966/763406204281552936/C8p6kL641icdByy7dM0B6eLb6XIWI36WiqN2ifv6fIVdwtCp93WA9NRJPF5wUgoMkJ6UguPU6fAAOmpk3i84KQUDc5vM9bsewTgA.png',
    152:'https://media.discordapp.net/attachments/764077712641228860/764093703882932244/GAyC6ACgm0AAAAASUVORK5CYII.png',
    153:'https://media.discordapp.net/attachments/763406131431079966/763406359605149736/wG18VTj1HLY0AAAAABJRU5ErkJggg.png',
    154:'https://media.discordapp.net/attachments/763406131431079966/763406438776569886/wftJ2jyqx79kwAAAABJRU5ErkJggg.png',
    155:'https://media.discordapp.net/attachments/763406131431079966/763406528203194389/6seAOyeCVQJLB4AvJYLyaSMaSouiRvULUZxMUo79xSUOZ0VbTm9GjgwCyxEIwWxvhDgoDXXJkcsQCi5P9HmKclEs3bE9eBHwIL2l.png',
    156:'https://media.discordapp.net/attachments/763406131431079966/763406615163437066/JGNLQAAAAAElFTkSuQmCC.png',
    157:'https://media.discordapp.net/attachments/763406131431079966/763406697830023218/8PJEM7YOQJkGwAAAAASUVORK5CYII.png',
    158:'https://media.discordapp.net/attachments/763406131431079966/763406778276642827/gek6OnczGrmgAAAABJRU5ErkJggg.png',
    159:'https://media.discordapp.net/attachments/763406131431079966/763406867312803840/mkJzr7KDZXI0aeoLpT1Svr9RYvMpUAAAAAElFTkSuQmCC.png',
    160:'https://media.discordapp.net/attachments/763406131431079966/763406941447782430/WOFyrnW2X8FbmSuIuqf1aNdFD8NXwP66fqiTvKroJ70erfS3wMBi5DfiPAGf5nNTC2DoyAAAAAElFTkSuQmCC.png',
    161:'https://media.discordapp.net/attachments/763406131431079966/763407083546083328/fdz7PmQydPGkOgtndvAu5Xpsa0pNllIoQVgQ8CQeDEIBDCOjFNlYIGgSAQwooMBIEgcGIQCGGdmKZKQYNAEAhhRQaCQBA4MQj8Py.png',
    162:'https://media.discordapp.net/attachments/763406131431079966/763407143763836938/dmNMMm0PBEqmJtcpvj8tqhzG5K1qfIxdO2pLVJJ1ARUicgktMiTGKszJqTeYuqJqcaaKrlNfa6Fx58qQlpEUGOtoSkPvKwHqIBPF.png',
    163:'https://media.discordapp.net/attachments/763406131431079966/763407262495539230/O2o84VpTfGmzYU41wWB40WgDxztI9FXefKpnM9l0pTD558hIhP8F6AAAAAElFTkSuQmCC.png',
    164:'https://media.discordapp.net/attachments/763406131431079966/763407351830675486/wPVqma3tswwwAAAABJRU5ErkJggg.png',
    165:'https://media.discordapp.net/attachments/763406131431079966/763407431996014600/isFsw8fn5ywAAAABJRU5ErkJggg.png',
    166:'https://media.discordapp.net/attachments/763406131431079966/763407522081669170/UHzIIAAAAASUVORK5CYII.png',
    167:'https://media.discordapp.net/attachments/763406131431079966/763407612120924160/7OsLTbw9ExPh0QAAAABJRU5ErkJggg.png',
    168:'https://media.discordapp.net/attachments/763406131431079966/763407693046087690/aAAAAAElFTkSuQmCC.png',
    169:'https://media.discordapp.net/attachments/763406131431079966/763407779024470046/4T1MjMQTBgXAAAAAElFTkSuQmCC.png',
    170:'https://media.discordapp.net/attachments/763406131431079966/763407871106482186/AXgH4IOuG8giAAAAAElFTkSuQmCC.png',
    171:'https://media.discordapp.net/attachments/763406131431079966/763407954752962590/AAAAAElFTkSuQmCC.png',
    172:'https://media.discordapp.net/attachments/763406131431079966/763408028267315230/0UBMXSshmm8M37Gey8pmEw3R9UOfJU0EghLVZJdmWx7b4kjYLwaRm0giEsCZdvMlcEJgWAiGsaZVnchMEJo1ACGvSxZvMBYFpIRD.png',
    173:'https://media.discordapp.net/attachments/763406131431079966/763408133447876648/70g4jq4mTmNsFgeOFQAjreJTHskGHrn6OR2qTiiCwJQRCWFsCPo8NAkFgfQRCWOtjln8EgSCwJQRCWFsCPo8NAkFgfQRCWOtjln8.png',
    174:'https://media.discordapp.net/attachments/764077712641228860/764092052740767784/FmimkVk4wpKkVq6hrnWQLkGSqDlXRrkuiIA8xM4eu5Bzc80kwNrRLdpe1Cykzny8dLSjtYOENYRGIgdFXfrt3rWgOXqwFvA5Jx27.png',
    175:'https://media.discordapp.net/attachments/763406131431079966/763408346895351868/OoAAAAASUVORK5CYII.png',
    176:'https://media.discordapp.net/attachments/763406131431079966/763408460581699584/K4muDuAAAAAElFTkSuQmCC.png',
    177:'https://media.discordapp.net/attachments/763406131431079966/763408528001073183/wNLBnkB30BkQAAAABJRU5ErkJggg.png',
    178:'https://media.discordapp.net/attachments/763406131431079966/763408603482030086/wff7B3YMrxdRgAAAABJRU5ErkJggg.png',
    179:'https://media.discordapp.net/attachments/763406131431079966/763408680167014441/8OAkFgIARCVgMBnccEgSCwGgIhq9Xwy7DQBAYCIGQ1UBA5zFBIAishkDIajX88u8gEAQGQiBkNRDQeUwQCAKrIfBfUxA8g8hoKvk.png',
    180:'https://media.discordapp.net/attachments/763406131431079966/763408769161232394/AAAAABJRU5ErkJggg.png',
    181:'https://media.discordapp.net/attachments/763406131431079966/763408856377458708/wF3fwj2Z3e1fgAAAABJRU5ErkJggg.png',
    182:'https://media.discordapp.net/attachments/764077712641228860/764085597806919690/Bj7uubuy4O1NUeBFdzTiIKfREE40FInLWnBD8NN04O11XNPgRXc04uAHwI8yJDJ9CRY77APCvwfiEaOxwMwhF4AAAAASUVORK5CY.png',
    183:'https://media.discordapp.net/attachments/764077712641228860/764096148654391296/AGifbmfOUwJRAZwlMYHUW6MxuSmBKYJwEJrDGyXbmPCUwJdBZAhNYnQU6s5sSmBIYJ4EJrHGynTlPCUwJdJbABFZngc7spgSmBMZ.png',
    184:'https://media.discordapp.net/attachments/763406131431079966/763409103162703922/wVuKloQAvA4FQAAAABJRU5ErkJggg.png',
    185:'https://media.discordapp.net/attachments/763406131431079966/763409193737781298/aMbgkec6Lmi5OMG82XtRBqS2CmrkGgCQTBX50uOQ3P0WAAAAAElFTkSuQmCC.png',
    186:'https://media.discordapp.net/attachments/763406131431079966/763409330975801344/f9fF15BdUXX0AAAAAElFTkSuQmCC.png',
    187:'https://media.discordapp.net/attachments/763406131431079966/763409419697913856/wGmIWeTd5724gAAAABJRU5ErkJggg.png',
    188:'https://media.discordapp.net/attachments/763406131431079966/763409492813414461/ZDCU55nwKwJBR66sy1LgrAEawsAZ9xjMUk8HrCWwTtjoWlQAAAABJRU5ErkJggg.png',
    189:'https://media.discordapp.net/attachments/763406131431079966/763409569288290344/IbMV1C6S0oAAAAASUVORK5CYII.png',
    190:'https://media.discordapp.net/attachments/764077712641228860/764083678250401852/BWDfIY5iuzVpCiQYDFsdtbxGe5tHUcw7FFk7yZBgf8HiB6xJ92bCKoAAAAASUVORK5CYII.png',
    191:'https://media.discordapp.net/attachments/763406131431079966/763409719330865184/BR2RwqncgvVAAAAAElFTkSuQmCC.png',
    192:'https://media.discordapp.net/attachments/763406131431079966/763409791925878814/ASoWlHSHCBfnAAAAAElFTkSuQmCC.png',
    193:'https://media.discordapp.net/attachments/763406131431079966/763409890286239764/1fz8L9ewLpSadXq7bRjZ4Zs8s0Yxev8BHZMORgkRie4AAAAASUVORK5CYII.png',
    194:'https://media.discordapp.net/attachments/763406131431079966/763409963196219442/r71AAAAAElFTkSuQmCC.png',
    195:'https://media.discordapp.net/attachments/763406131431079966/763410048755040326/YuhYjG537pKzzQJ7HOZkYJGhgg3TW1R3mTKHAsQI1RyjWibs9xJ73sxJuipwawPaedWMS4bVBgtxT4PyWbvmH0TSwKAAAAAElFTk.png',
    196:'https://media.discordapp.net/attachments/764077712641228860/764092337978474496/0j2KYBkidmoAAAAASUVORK5CYII.png',
    197:'https://media.discordapp.net/attachments/763406131431079966/763410273436172358/AgAAAAASUVORK5CYII.png',
    198:'https://media.discordapp.net/attachments/763406131431079966/763410351093579797/AYaSLoqhJQJRAAAAAElFTkSuQmCC.png',
    199:'https://media.discordapp.net/attachments/764077712641228860/764082244087447562/4W2cbCY0dn4AAAAASUVORK5CYII.png',
    200:'https://media.discordapp.net/attachments/764077712641228860/764084640537247744/zKgniBzfAAAAAElFTkSuQmCC.png',
    201:'https://media.discordapp.net/attachments/763410769986977874/763410823116226610/B0IXcQygPVTwAAAABJRU5ErkJggg.png',
    202:'https://media.discordapp.net/attachments/763410769986977874/763410892725026846/7JKHBO8Vp2YAAAAASUVORK5CYII.png',
    203:'https://media.discordapp.net/attachments/764077712641228860/764098176566296656/35YG2ZwI1KwAAAABJRU5ErkJggg.png',
    205:'https://media.discordapp.net/attachments/763410769986977874/763411158488055828/TQSsGWwTzeO9lvpOGXmaIUoIEkcj59EM0ACUoq3EltGmwR4vBP63bSJgMtgmmidzLXnAlaSlrE3NeahZlcqm5E53JqR1MrD5X1sE.png',
    206:'https://media.discordapp.net/attachments/763410769986977874/763411257276629002/uiE0Ap71lmQy0EPIZZUDXYpb2s097767i6P8H0zUvXeEwbjEAAAAASUVORK5CYII.png',
    207:'https://media.discordapp.net/attachments/763410769986977874/763411340937003038/f3EWsD1tJc3AZ0VfOKiR3OpRbKSrxXQKVuaxGtnOPbq0Tnq6B5wShTY0mnAKg4fLPxIa8bnljehPyXpgShCtdYFjeoPeVlI0Ma51.png',
    208:'https://media.discordapp.net/attachments/763410769986977874/763411419483734056/UlhFk2OSaxUfL6XxtwgpTa2CJuAAAAAElFTkSuQmCC.png',
    209:'https://media.discordapp.net/attachments/763410769986977874/763411513088016395/wHcXLUyYCrGwAAAABJRU5ErkJggg.png',
    210:'https://media.discordapp.net/attachments/763410769986977874/763411605718695957/Eorb0d9sAAAAASUVORK5CYII.png',
    211:'https://media.discordapp.net/attachments/763410769986977874/763411684592975912/RJ0Ipy5mlgAAAAASUVORK5CYII.png',
    212:'https://media.discordapp.net/attachments/763410769986977874/763411780239491122/wEFBDRa9XJG6wAAAABJRU5ErkJggg.png',
    213:'https://media.discordapp.net/attachments/763410769986977874/763411885046628382/CYwanvgdqlE8cU0qR7ilTTRHALVPeS0RqN656haP16gJ5oi37f8B2d9AQ9fZkcYAAAAASUVORK5CYII.png',
    214:'https://media.discordapp.net/attachments/763410769986977874/763411968198705172/dGSUxdXP8PwCWzgNlwKvkAAAAASUVORK5CYII.png',
    215:'https://media.discordapp.net/attachments/764077712641228860/764092574720851999/GvCAAAAAElFTkSuQmCC.png',
    217:'https://media.discordapp.net/attachments/763410769986977874/763412439718428762/aRzlOMAAAAAElFTkSuQmCC.png',
    218:'https://media.discordapp.net/attachments/763410769986977874/763412520752906340/sqzqG0PR2QYAAAAASUVORK5CYII.png',
    219:'https://media.discordapp.net/attachments/763410769986977874/763412609843855420/Sy6aNllZGYAboD3iUpE7VqKGzhb4uIGBmyqSjxKAflONlYHrJBeha1G3rFGMHDTzxlS8BBZreof9ndn2MrVuPtt5LNEhq4VYX7zT.png',
    220:'https://cdn.discordapp.com/attachments/763410769986977874/780712746437574696/221_shadowed.png',
    221:'https://cdn.discordapp.com/attachments/763410769986977874/780713081403211826/222_shadowed.png',
    222:'https://cdn.discordapp.com/attachments/763410769986977874/780713219589144576/223_shadowed.png', 
}

class RacerClass:
    def __init__(self, racer=None):
        self.racer = racer
    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()
    async def create_attr(self):
        racer = self.racer
        if racer == None:
            self.success = False
            return

        newdata = {}
        '''async with aiocfscrape.CloudflareScraper() as session:
            response = await self.fetch(session, f'https://www.nitrotype.com/racer/{racer}')'''
        loop = asyncio.get_running_loop()
        scraper = cloudscraper.create_scraper()
        fut = await loop.run_in_executor(None, functools.partial(scraper.get,f'https://www.nitrotype.com/racer/{racer}'))
        response = fut.text
        #print(response)
        newdata = ('{"'+re.search(r'RACER_INFO: \{\"(.*)\}', response.strip()).group(1)+'}')
        newdata = json.loads(newdata)
        self.newdata = newdata
        print(newdata)
        if newdata == {}:
            self.success = False
            return

        try:
            if not newdata['tag']:
                self.tag = ''
            else:
                self.tag = f"[{newdata['tag']}]"
        except KeyError:
            self.tag = ''
        self.userid = newdata['userID']
        #Just Space So that I don\'t have to move everything
        space1 = 'space'
        if space1 == 'space':
            try:
              space2 = 'space'
              if space2 == 'space':
                
                self.success = True
                if self.success:
                  fut = await loop.run_in_executor(None, functools.partial(
                      scraper.post,
                      'https://www.nitrotype.com/api/v2/payments/products/',
                      data={
                          'username': racer,
                          'type': 'gold'
                          }
                      )
                  )
                  response = fut.json()
                  print(response)
                  '''
                self.success = True
                self.lifetime_gold = False
                '''
                try:
                    self.lifetime_gold = True if response['status'] == "INVALID_REQUEST" and 'lifetime' in response['results']['username'] else False
                except Exception as e:
                    print(e)
                    self.lifetime_gold=False
            except:
              pass

            if self.lifetime_gold == False and newdata['membership'] == 'gold':
              self.gold_until = response['results']['user']['goldUntil']
              last_purchase = response['results']['user']['lastPurchase']
              last_purchase = last_purchase[0:8]
              lpyear = last_purchase[0:4]
              lpmonth = last_purchase[4:6]
              lpday = last_purchase[6:8]
              dt = datetime(
              year=int(lpyear),
              month=int(lpmonth),
              day=int(lpday)
              )
              self.last_purchase = int(dt.timestamp())
              

            self.carIDs = []
            for elem in newdata['cars']:
                if elem[1] == 'owned':
                    self.carIDs.append(elem[0])

            self.username = newdata['username'].title()

            display_name = newdata['displayName'] or self.username
            self.name = display_name

            self.title = newdata['title'].title()

            try:
                self.racelogs = newdata['raceLogs']
            except:
                pass
            self.tag_and_name = f'[{self.tag}{display_name}\n"{newdata["title"].title()}"](https://nitrotype.com/racer/{racer})'

            self.membership = newdata['membership']


            '''try:
                    if re.search(str({newdata["carID"]}).lower(), str({newdata["carID"]}).lower()).group():
                      cardata = elem
                      self.car = f'https://www.nitrotype.com/cars/{cardata}_large_1.png'
            except:
              print('no u')'''
            '''self.car = f'https://www.nitrotype.com/cars/{newdata["carHueAngle"]}_large_1.png'''
            fut = await loop.run_in_executor(None, functools.partial(scraper.get,'https://www.nitrotype.com/index/d8dad03537419610ef21782a075dde2d94c465c61266-1266/bootstrap.js'))
            text = fut.text
            result = re.search(r'(\[\{\"id\"\:\d+,\"carID\":\d+.*\]\])(?:,\[\"P)', text).group(1)
            data = json.loads('{"list": '+''.join(list(result)[:-1])+'}')
            for elem in data['list']:
                for v in elem.values():
                    try:
                        if str(v) == str(newdata['carID']):
                            if newdata['carHueAngle'] != 0:
                                self.car = 'https://www.nitrotype.com/cars/painted/'+elem['options']['largeSrc'].replace('.png', '_'+str(newdata['carHueAngle']))+'.png'
                            else:
                                self.car = 'https://www.nitrotype.com/cars/'+elem['options']['largeSrc']
                            break
                    except:
                        continue
                else:
                    continue
                break
            '''
            if newdata['carHueAngle'] == 0:
                self.car = f'https://www.nitrotype.com/cars/{newdata["carID"]}_large_1.png'
            else:
                self.car = f'https://www.nitrotype.com/cars/painted/{newdata["carID"]}_large_1_{newdata["carHueAngle"]}.png'
            '''
            
            self.level = fn(newdata['level'])
            self.experience = fn(newdata['experience'])
            #self.points = fn(newdata['achievementPoints'])
            #self.country = countries.get(newdata['country'], 'Unknown')
            #if self.country != 'Unknown':
                #self.country += f' :flag_{newdata["country"].lower()}: '
            self.views = fn(newdata['profileViews'])
            #self.created = date.fromtimestamp(newdata['createdStamp']).strftime('%d %B %Y')
            self.created = date.fromtimestamp(newdata['createdStamp']).strftime('%d %B %Y')
            '''if B =='January':
              mn = '01'
          elif B == 'February':
              mn = '02'
          elif B == 'March':
              mn = '03'
          elif B == 'April':
              mn = '04'
          elif B == 'May':
              mn = '05'
          elif B == 'June':
              mn = '06'
          elif B == 'July':
              mn = '07'
          elif B == 'August':
              mn = '08'
          elif B == 'September':
              mn = '09'
          elif B == 'Oktober':
              mn = '10'
          elif B == 'November':
              mn = '11'
          elif B == 'Dezember':
              mn = '12'
        else:
              mn = B'''
            self.cars_owned = 0
            self.cars_sold = 0
            self.cars_total = 0
            for car in newdata['cars']:
                if car[1] == 'owned':
                    self.cars_owned += 1
                elif car[1] == 'sold':
                    self.cars_sold += 1
                self.cars_total += 1
            self.car_collector = self.cars_owned
            self.cars_owned = fn(self.cars_owned)
            self.cars_sold = fn(self.cars_sold)
            self.cars_total = fn(self.cars_total)
            #self.current_car = cars.get(newdata['carID'])
            self.carid = newdata['carID']

            self.nitros = newdata['nitros']
            self.nitros_used = newdata['nitrosUsed']
            self.nitro_enthusiast = self.nitros_used
            self.nitros_total = self.nitros + self.nitros_used
            self.nitros = fn(self.nitros)
            self.nitros_used = fn(self.nitros_used)
            self.nitros_total = fn(self.nitros_total)
	
		

            self.races = newdata['racesPlayed']
	
            #self.first = newdata['placed1']
            #self.second = newdata['placed2']
            #self.third = newdata['placed3']
            #try:
                #self.first_perc = round((self.first/self.races)*100, 2)
            #except ZeroDivisionError:
                #self.first_perc = 0
            #try:
                #self.second_perc = round((self.second/self.races)*100, 2)
            #except ZeroDivisionError:
                #self.second_perc = 0
            #try:
                #self.third_perc = round((self.third/self.races)*100, 2)
            #except ZeroDivisionError:
                #self.third_perc = 0
            self.races = fn(self.races)
            #self.first = fn(self.first)
            #self.second = fn(self.second)
            #self.third = fn(self.third)
            self.longest_session = fn(newdata['longestSession'])

            self.wpm_average = fn(newdata['avgSpeed'])
            self.wpm_high = fn(newdata['highestSpeed'])
	
            # Fun Roles
            self.created_timestamp = newdata['createdStamp']
            self.popular_views = newdata['profileViews']
            self.longest_session_sessionist = newdata['longestSession']
            self.nitro_enthusiast = self.nitro_enthusiast
            self.car_collector = self.car_collector
            self.high_speed = newdata['highestSpeed']
            self.average_speed = newdata['avgSpeed']
		
            try:
                self.trailid = newdata['loot'][0]['lootID']
                self.trailname = newdata['loot'][0]['name']
                self.trail_asset = newdata['loot'][0]['assetKey']
                self.trail_rarity = newdata['loot'][0]['options']['rarity']
                self.trail_image = newdata['loot'][0]['options']['src']
                self.trail_created = date.fromtimestamp(newdata['loot'][0]['createdStamp']).strftime('%d %B %Y')
            except:
                self.trailid = 'None'
                self.trailname = 'None'
                self.trail_asset = 'None'
                self.trail_rarity = 'None'
                self.trail_image = 'None'
                self.trail_created = 'None'
            '''
            self.money = newdata['money']
            self.money_spent = newdata['moneySpent']
            self.money_total = self.money + self.money_spent
            self.money = fn(self.money)
            self.money_spent = fn(self.money_spent)
            self.money_total = fn(self.money_total)
            '''
            '''self.boards = newdata['racingStats']
            try:
                for board in self.boards:
                    if str(board['board']) == "daily":
                        self.daily_pre = board
                        break
                self.daily_races = self.daily_pre['played']
                self.daily_speed = int(self.daily_pre['typed'])/5/float(self.daily_pre['secs'])*60
                self.daily_accuracy = 100-((int(self.daily_pre['errs'])/int(self.daily_pre['typed']))*100)
                self.daily_points = (self.daily_races*(100+(self.daily_speed/2))*self.daily_accuracy/100)
            except:
                self.daily_races = 0
                self.daily_speed = 0
                self.daily_accuracy = 0
                self.daily_points = 0
            try:
                for board in self.boards:
                    if str(board['board']) == "season":
                        self.season_pre = board
                        break
                self.season_races = self.season_pre['played']
                self.season_speed = int(self.season_pre['typed'])/5/float(self.season_pre['secs'])*60
                self.season_accuracy = 100-((int(self.season_pre['errs'])/int(self.season_pre['typed']))*100)
                self.season_points = (self.season_races*(100+(self.season_speed/2))*self.season_accuracy/100)
            except:
                self.season_races = 0
                self.season_speed = 0
                self.season_accuracy = 0
                self.season_points = 0
            '''
            self.speed_rounded = int(math.floor(int(self.wpm_average)/10)*10)
            if self.speed_rounded > 220:
                self.speed_role = '220+ WPM'
            else:
                self.speed_role = f'{str(self.speed_rounded)}-{str(self.speed_rounded+9)} WPM'
            '''
            try:
                accuracy = int(round(self.season_accuracy, 1))
            except:
                accuracy = int(round(self.daily_accuracy, 1))
            accuracy_roles = [">99% Accuracy", "99% Accuracy", "98% Accuracy", "97% Accuracy", "96% Accuracy", "94-95% Accuracy", "90-93% Accuracy", "87-89% Accuracy", "84-86% Accuracy", "80-83% Accuracy", "75-79% Accuracy", "<75% Accuracy"]
            for role in accuracy_roles:
                if '>' in role and accuracy > 99:
                    self.accuracy_role = '>99% Accuracy'
                    break
                if '-' in role.split('%')[0]:
                    new_role = role.split('%')[0].split('-')
                    the_range = tuple(range(int(new_role[0]), int(new_role[1])+1))
                    if math.floor(accuracy) in the_range:
                        self.accuracy_role = role
                        break
                    continue
                if '<' in role and accuracy < 75:
                    self.accuracy_role = "<75% Accuracy"
                    break
                else:
                    new_role = role.split('%')
                    if math.floor(accuracy) == int(new_role[0].replace('>', '').replace('<', '')):
                        self.accuracy_role = role
                        break
            else:
                print(accuracy)
                self.accuracy_role = '<75% Accuracy'
            '''
            '''self.race_roles = ["500000+ Races", "250000-499999 Races", "200000-249999 Races", "150000-199999 Races", "100000-149999 Races", "75000-99999 Races", "50000-74999 Races", "40000-49999 Races", "30000-39999 Races", "20000-29999 Races", "10000-19999 Races", "5000-9999 Races", "3000-4999 Races", "1000-2999 Races","500-999 Races", "100-499 Races", "50-99 Races", "1-49 Races"]
            self.race_zones = [(int(x.split('+')[0]),) if '+' in x else range(int(x.split('-')[0].strip().replace(' Races', '')), int(x.split('-')[1].strip().replace(' Races', ''))) for x in self.race_roles]'''
            races = newdata['racesPlayed']
            kotr_roles = ['"I < 3 Typing!"', '"I Really Love Typing"', '"Bonkers About Typing"', '"Bananas About Typing"', '"You\'ve Gotta Be Kidding"', '"Corsair"', '"Pirc"', '"Carrie"', '"Anne"', '"Lackin\' Nothin\'"', '"Outback Officer"', '"I Love Shoes 2"', '"I Love Shoes 12.5"', '"I Love Shoes 15.0"', '"I Love Shoes 20.0"', '"The Wildest of Flowers"', '"The Wild Legend"']
            #kotr_roles = kotr_roles.reverse()
            '''index = 0
            races = newdata['racesPlayed']
            for zone in self.race_zones:
                if int(races) in zone:
                    self.race_role = self.race_roles[index]
                    break
                index += 1'''
            if int(races) >= 500000:
                self.race_role = kotr_roles[16]
            elif int(races) >= 250000:
                self.race_role = kotr_roles[15]
            elif int(races) >= 200000:
                self.race_role = kotr_roles[14]
            elif int(races) >= 150000:
                self.race_role = kotr_roles[13]
            elif int(races) >= 125000:
                self.race_role = kotr_roles[12]
            elif int(races) >= 100000:
                self.race_role = kotr_roles[11]
            elif int(races) >= 75000:
                self.race_role = kotr_roles[10]
            elif int(races) >= 50000:
                self.race_role = kotr_roles[9]
            elif int(races) >= 40000:
                self.race_role = kotr_roles[8]
            elif int(races) >= 30000:
                self.race_role = kotr_roles[7]
            elif int(races) >= 20000:
                self.race_role = kotr_roles[6]
            elif int(races) >= 10000:
                self.race_role = kotr_roles[5]
            elif int(races) >= 5000:
                self.race_role = kotr_roles[4]
            elif int(races) >= 1000:
                self.race_role = kotr_roles[3]
            elif int(races) >= 500:
                self.race_role = kotr_roles[2]
            elif int(races) >= 100:
                self.race_role = kotr_roles[1]
            elif int(races) >= 0:
                self.race_role = kotr_roles[0]

            if self.membership == 'basic':
            	self.gold_role = None
		#self.lifetime_gold_role = None
		#self.yearly_gold_role = None
            else:
                self.classic_gold_role = 'Gold Member'
                if self.lifetime_gold == True:
                    self.gold_role = 'Lifetime Gold'
                if self.lifetime_gold == False:
                    self.gold_role = 'Yearly Gold'
            self.friend_reqs_allowed = ':white_check_mark: ' if newdata['allowFriendRequests'] == 1 else ':negative_squared_cross_mark:'
            self.looking_for_team = ':white_check_mark: ' if newdata['lookingForTeam'] == 1 else ':negative_squared_cross_mark:'
async def Racer(username):
    r = RacerClass(username)
    await r.create_attr()
    return r
class Guesser:
    def __init__(self, shadow=False):
        if shadow == True:
            exceptions = [12, 32, 41, 108, 147, 148]
            id = randint(1, 219)
            while id in exceptions: id = randint(1, 219)

            self.pic = shadowcars.get(id)

            self.options = {'a' : '',
                    'b' : '',
                    'c' : '',
                    'd' : ''}

            used = []
            self.correct = choice('abcd')
            used.append(id)
            self.options[self.correct] = cars.get(id)
            
            for option in self.options:
                if not option == self.correct:
                    id = randint(1, 219)
                    while id in exceptions and id in used: id = randint(1, 219)

                    used.append(id)
                    
                    self.options[option] = cars.get(id)

            
            self.formatted = ''

            for option in self.options:
                self.formatted += f':regional_indicator_{option}:  {self.options.get(option)}\n'
            return
        #if not shadowed

        self.options = {'a' : '',
                'b' : '',
                'c' : '',
                'd' : ''}

        used = []
        self.correct = choice('abcd')
        scraper = cloudscraper.create_scraper()
        loop = asyncio.get_event_loop()
        fut = scraper.get(f'https://www.nitrotype.com/index//bootstrap.js')
        text = fut.text
        result = re.search(r'(\[\{\"id\"\:\d+,\"carID\":\d+.*\]\])(?:,\[\"P)', text).group(1)
        data = json.loads('{"list": '+''.join(list(result)[:-1])+'}')
        scars = data['list']
        correct_car = choice(scars)
        self.pic = f'https://www.nitrotype.com/cars/{correct_car["options"]["largeSrc"]}'
        self.options[self.correct] = correct_car['name']
        used.append(correct_car['id'])
        for option in self.options:
            if not option == self.correct:
                car_data = choice(scars)
                id = car_data['id']
                while id in used:
                    car_data = choice(scars)
                    id = car_data['id']

                used.append(id)
                
                self.options[option] = car_data['name']

        
        self.formatted = ''

        for option in self.options:
            self.formatted += f':regional_indicator_{option}:  {self.options.get(option)}\n'
class TeamClass:
    def __init__(self, team):
        self.team = team
    async def create_attr(self):
        team = self.team
        team = team.upper()
        try:
            '''async with aiocfscrape.CloudflareScraper() as session:
                self.data = loads(await api_get(f'teams/{team}', session))'''
            loop = asyncio.get_running_loop()
            scraper = cloudscraper.create_scraper()
            fut = await loop.run_in_executor(None,functools.partial(scraper.get,f'https://www.nitrotype.com/api/v2/teams/{team}'))
            print(fut.text)
            try:
              self.data = json.loads(fut.text)
            except Exception as e:
              print(e)
            self.success = True
            if self.data['status'] != "OK":
                print('fail')
                self.success = False
                self.data = {}
                return
        except:
            self.data = {}
        else:
            self.data = self.data["results"]
            self.info = self.data["info"]
            print(self.info)

            try:
                self.daily_pre = self.data['stats'][1]
                self.daily_races = self.daily_pre['played']
                self.daily_speed = int(self.daily_pre['typed'])/5/self.daily_pre['secs']*60
                self.daily_accuracy = 100-((int(self.daily_pre['errs'])/int(self.daily_pre['typed']))*100)
                self.daily_points = (self.daily_races*(100+(self.daily_speed/2))*self.daily_accuracy/100)
            except:
                self.daily_pre = 0
                self.daily_races = 0
                self.daily_speed = 0
                self.daily_accuracy = 0
                self.daily_points = 0

            try:
                self.season_pre = self.data['stats'][2]
                self.season_races = self.season_pre['played']
                self.season_speed = int(self.season_pre['typed'])/5/self.season_pre['secs']*60
                self.season_accuracy = 100-((int(self.season_pre['errs'])/int(self.season_pre['typed']))*100)
                self.season_points = (self.season_races*(100+(self.season_speed/2))*self.season_accuracy/100)
            except:
                self.season_pre = 0
                self.season_races = 0
                self.season_speed = 0
                self.season_accuracy = 0
                self.season_points = 0

            try:
                self.alltime_pre = self.data['stats'][0]
                self.alltime_races = self.alltime_pre['played']
                self.alltime_speed = int(self.alltime_pre['typed'])/5/self.alltime_pre['secs']*60
                self.alltime_accuracy = 100-((int(self.alltime_pre['errs'])/int(self.alltime_pre['typed']))*100)
                self.alltime_points = (self.alltime_races*(100+(self.alltime_speed/2))*self.alltime_accuracy/100)
            except:
                self.alltime_pre = 0
                self.alltime_races = 0
                self.alltime_speed = 0
                self.alltime_accuracy = 0
                self.alltime_points = 0

            self.teamid = self.info["teamID"]
            self.enrollment = self.info["enrollment"]
            self.activeperc = self.info["activePercent"]
            self.lastact = date.fromtimestamp(self.info["lastActivity"]).strftime('%d %B %Y')
            self.lastmod = date.fromtimestamp(self.info["lastModified"]).strftime('%d %B %Y')

            self.leaders = []
            self.captain = (self.info['username'], self.info['displayName'])
            for elem in self.data['members']:
                if elem['role'] == "officer" and elem['username'] != self.captain[0]:
                    self.leaders.append((elem['username'], elem['displayName']))
            self.embed_title = self.info["displayName"]
            if self.embed_title.endswith('s'):
                self.embed_title += "'"
            else:
                self.embed_title += "'s"
            self.embed_title += ' Team'
            self.tag_and_name = f'[ [{self.info["tag"].upper()}] {self.info["name"]} ](https://www.nitrotype.com/team/{self.info["tag"].upper()})'
async def Team(team):
    teamclass = TeamClass(team)
    await teamclass.create_attr()
    return teamclass

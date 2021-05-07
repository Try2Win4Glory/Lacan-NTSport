from PIL import Image
from math import ceil, floor
from PIL import Image
from io import BytesIO
import numpy, aiohttp
import time, asyncio, logging
async def compileRawGarageAsync(username):
    import re
    from bs4 import BeautifulSoup
    from garageScript.requests_html import AsyncHTMLSession
    sesh = AsyncHTMLSession()
    r = await sesh.get(f'https://www.nitrotype.com/racer/{username}')
    await r.html.render(timeout=10)
    #print(r.html.html)
    html = re.sub('&quot;', '', r.html.html)
    soup = BeautifulSoup(html, 'html.parser')
    with open('test.html', 'w') as f:
        f.write(soup.prettify())
    parent = (soup.find('div', class_='garage'))
    children = (parent.findChildren('div', class_='garage-spot'))
    for child in children:
        search = (re.search(r'background\-image: url\((.{40,100})\)', str(child)))
        if search:
            yield (search.group(1))
        else:
            yield ('')
async def fetchRaw(session, url):
    async with session.get(url) as response:
        return await response.content.read()
async def compileCarAsync(link):
    cached = True
    try:
        with open('garageScript/'+link.split('.com/')[-1], 'rb') as f:
            r = f.read()
    except:
        async with aiohttp.ClientSession() as session:
            r = await fetchRaw(session, link)
            cached = False
    b = BytesIO()
    #b.write(r.raw.read())
    b.write(r)
    b.seek(0)
    if cached == False:
        with Image.open(b) as c:
            with BytesIO() as byt:
                c.save('garageScript/'+link.split('.com/')[-1])
                byt.seek(0)
    return b
async def compileProfileAsync(username):
    async for car in compileRawGarageAsync(username):
        if car == '':
            yield ''
            continue
        yield await compileCarAsync(car)
async def compileGarage(username):
    print(time.time())
    profile = [car async for car in  compileProfileAsync(username)]
    width = 913 + 24
    height = 30 + (ceil(len(profile) / 30) * 291)
    with Image.new('RGBA', (width, height)) as img:

        # Pasting lots
        with Image.open('packages/parking_spots_all.png') as lots:
            for i in range(ceil(len(profile) / 30)):
                img.paste(lots, (12, 15 + (291 * i)), lots)
        garage = numpy.reshape(profile,
                            (ceil(len(profile) / 15), 15))
        for y, row in enumerate(garage):
            for x, id in enumerate(row):
                if id == '':
                    continue
                car = id
                with Image.open(car) as c:
                    width = c.size[1]
                    length = c.size[0]
                    with c.rotate(90 if y % 2 == 0 else -90,
                                expand=True,
                                resample=Image.NEAREST) as temp:
                        _x = 12 + ((x * 61) + (30 - floor(width / 2)))
                        _y = 20 + (48 -
                                floor(length / 2)) + (y * 181 -       (floor(y / 2) * 71))
                        '''with BytesIO() as b:
                            c.save(id.split('.com/')[-1])
                            b.seek(0)'''
                        img.paste(temp, (_x, _y))
                car.close()

        with BytesIO() as b:
            img.save("garage.png", 'PNG')
            b.seek(0)
        print(time.time())
'''async def get_all_normal_cars():
    for f in list(os.listdir('cars/painted')):
        suffix = re.sub(r'1\_\d{1,3}', '1', f)
        await compileCarAsync(f'https://www.nitrotype.com/cars/{suffix}')
asyncio.run(get_all_normal_cars())'''

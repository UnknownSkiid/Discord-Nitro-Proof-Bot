from bs4 import BeautifulSoup
from discord.ext import commands
from playwright.async_api import async_playwright
from PIL import Image
import discord
import requests
import time
import json
import random
import string
import datetime
import re
import os


tk = "TOKEN"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")

class Nitro:

    def __init__(self):
        self.start_time = str(datetime.datetime.now().time())[0:5]
        self.dir = os.path.dirname(os.path.abspath(__file__))

    def find_replace(self,soup,looking_for, replacing_with):
        t = soup.find_all(string=re.compile(looking_for))
        for x in t:
            x.replace_with(x.replace(looking_for,replacing_with))
        return True

    def edit(self,ctx,user,msg):
        html = open("src/boost.html","r").read()
        soup = BeautifulSoup(html,features="html.parser")
        x = str(soup).replace("THEURLFORFIRSTUSER",ctx.author.avatar.url)
        try:
            y = x.replace("SECONDAUTHORURL",user.avatar.url)
        except:
            print("User doesnt have a pfp, setting random pfp.")
            y = x.replace("SECONDAUTHORURL","https://api.lorem.space/image/car?w=512&h=512")
        soup = BeautifulSoup(y,features="html.parser")
        self.find_replace(soup,"THEFIRSTAUTHOR",ctx.author.name)
        self.find_replace(soup,"FIRSTAUTHORDATE","Today at {}".format(self.start_time))
        self.find_replace(soup,"SECONDAUTHORDATE","Today at {}".format(self.start_time))
        self.find_replace(soup,"uBKuv3Ygb5Q4R9m7","".join(random.choice(string.ascii_letters) for i in range(len("uBKuv3Ygb5Q4R9m7"))))
        self.find_replace(soup,"THESECONDAUTHOR",user.name)
        self.find_replace(soup,"RESPONSETONITRO",msg)
        self.find_replace(soup, "Expires in 47 hours","Expiers in {} hours".format(str(random.randint(1,47))))
        return str(soup)

    def image_crop(self,img):
        image = Image.open(img)
        rgb_im = image.convert('RGB')
        new_image = rgb_im.crop((0, 0, 800, 350))
        new_image.save(img)
        return img

    async def screenshot(self,path):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            await page.goto('http://127.0.0.1:3000')
            await page.screenshot(path=path)
            await browser.close()
        return path

@bot.command()
async def nitro(ctx, user: discord.User=None,*, msg=None):
    if user == None or msg==None:
        return await ctx.send(embed=discord.Embed(color=discord.Colour.red(),description="You need to add args!"))
    message = await ctx.send(embed=discord.Embed(color=discord.Colour.green(),description="Creating your image..."))
    try:
        os.remove("editing/new.html")
    except:
        open("editing/new.html", 'a')
    cl = Nitro()
    soup = cl.edit(ctx,user,msg)
    open("editing/new.html","a").write(str(soup))
    path = await cl.screenshot(path="editing/capture.png")
    path = cl.image_crop(path)
    await message.delete()
    await ctx.send(ctx.author.mention,file=discord.File(path))

@bot.command()
async def help(ctx):
    return await ctx.send(embed=discord.Embed(
        colour=discord.Colour.green(),
        title="Nitro Proof Automation",
        description="The only command, !nitro (mention) (message)\n\nCreated by Detective Voke#9226",
    ))

bot.run(tk)

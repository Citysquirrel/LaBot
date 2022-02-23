import os
import discord
import asyncio
from discord.ext import commands
from discord.commands import Option
import aiohttp
import nest_asyncio
import calmodule
nest_asyncio.apply()

client = commands.Bot()
token = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print("Bot is online")

async def get_req(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json()
            return (response)

async def get_req2(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            valresponse = await resp.text()
            if "오류 발생" in valresponse:
                return ({"Result":"Failed"})
            else:
                response = await resp.json()
                return (response)

@client.slash_command(name="정보",description="해당 닉네임 유저의 정보를 조회합니다.")
async def 정보(ctx: discord2.ApplicationContext, 닉네임: Option(str, "닉네임을 적으세요.", required=True, default=None)):
    if ctx.guild is None:
        await ctx.respond("DM금지")
    else:
        try:
            await ctx.defer(ephemeral=True)

            message = await ctx.interaction.original_message()

            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(get_req2('http://152.70.248.4:5000/userinfo/'+str(닉네임)))

            if not response["Result"] == "Failed":
                if not response["Result"] == "1레벨":

                    embedresult = calmodule.embedresult(response)

                    embedresult_lister = calmodule.embedresult_lister(response)
                    
                    embedskill = calmodule.embedskill(response)
                    
                    embedresult_jewlist = calmodule.embedresult_jewlist(response)

                    embedresult_goldget = calmodule.embedresult_goldget(response)
                    
                    embedresult_sasalist = calmodule.embedresult_sasalist(response["Sasa"], 닉네임)                    

                    embedresult_gearlist = calmodule.embedresult_gearlist(response)

                    embedresult_gear2list = calmodule.embedresult_gear2list(response)

                    await message.edit("", embed=embedresult, view=InfoOptions(ctx, 닉네임, message, embedresult, embedresult_lister, embedskill, embedresult_jewlist, embedresult_goldget, embedresult_sasalist, embedresult_gearlist, embedresult_gear2list))
                else:
                    embedtoolow = discord2.Embed(title="해당 캐릭터는 레벨이 1 미만입니다.", color=discord2.Color.dark_gold())
                    await message.edit("", embed=embedtoolow, view=None)
            else:
                embederr = discord2.Embed(title="정보처리 과정 중 알 수 없는 오류가 발생했습니다.\n(없는 캐릭터,너무 많은 조회로 인한 서버이용 불가 등)", color=discord2.Color.red())
                await message.edit("", embed=embederr, view=None)
        except Exception as error:
            embederr = discord2.Embed(title="정보처리 과정 중 알 수 없는 오류가 발생했습니다.\n(없는 캐릭터,너무 많은 조회로 인한 서버이용 불가 등)", color=discord2.Color.red())
            await ctx.respond("", embed=embederr, view=None)
            print(error)

@client.slash_command(name="정보_표시",description="해당 닉네임 유저의 정보를 조회합니다.(다른 사람에게 표시)")
async def 정보_표시(ctx: discord2.ApplicationContext, 닉네임: Option(str, "닉네임을 적으세요.", required=True, default=None)):
    if ctx.guild is None:
        await ctx.respond("DM금지")
    else:
        try:
            await ctx.defer(ephemeral=False)

            message = await ctx.interaction.original_message()

            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(get_req2('http://152.70.248.4:5000/userinfo/'+str(닉네임)))

            if not response["Result"] == "Failed":
                if not response["Result"] == "1레벨":

                    embedresult = calmodule.embedresult(response)

                    embedresult_lister = calmodule.embedresult_lister(response)
                    
                    embedskill = calmodule.embedskill(response)
                    
                    embedresult_jewlist = calmodule.embedresult_jewlist(response)

                    embedresult_goldget = calmodule.embedresult_goldget(response)
                    
                    embedresult_sasalist = calmodule.embedresult_sasalist(response["Sasa"], 닉네임)                    

                    embedresult_gearlist = calmodule.embedresult_gearlist(response)

                    embedresult_gear2list = calmodule.embedresult_gear2list(response)

                    await message.edit("", embed=embedresult, view=InfoOptions(ctx, 닉네임, message, embedresult, embedresult_lister, embedskill, embedresult_jewlist, embedresult_goldget, embedresult_sasalist, embedresult_gearlist, embedresult_gear2list))
                else:
                    embedtoolow = discord2.Embed(title="해당 캐릭터는 레벨이 1 미만입니다.", color=discord2.Color.dark_gold())
                    await message.edit("", embed=embedtoolow, view=None)
            else:
                embederr = discord2.Embed(title="정보처리 과정 중 알 수 없는 오류가 발생했습니다.\n(없는 캐릭터,너무 많은 조회로 인한 서버이용 불가 등)", color=discord2.Color.red())
                await message.edit("", embed=embederr, view=None)
                print(error)
        except Exception as error:
            embederr = discord2.Embed(title="정보처리 과정 중 알 수 없는 오류가 발생했습니다.\n(없는 캐릭터,너무 많은 조회로 인한 서버이용 불가 등)", color=discord2.Color.red())
            await ctx.respond("", embed=embederr, view=None)
            print(error)

@client.slash_command(name="모험섬",description="모험섬 확인")
async def 모험섬(ctx: discord2.ApplicationContext):
    if ctx.guild is None:
        await ctx.respond("DM금지")
    else:
        try:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(get_req('http://152.70.248.4:5000/adventureisland/'))

            embedresult_island = calmodule.embedresult_island(response)
            
            await ctx.respond("", embed=embedresult_island)
        except Exception as error:
            embederr = discord2.Embed(title="알 수 없는 오류가 발생했습니다./몇 시간 이후 다시 시도해주세요.", color=discord2.Color.red())
            await ctx.respond("", embed=embederr, view=None)
            print(error)

@client.slash_command(name="사사게",description="사사게 확인")
async def 사사게(ctx: discord2.ApplicationContext, 닉네임: Option(str, "닉네임을 적으세요.", required=True, default=None)):
    if ctx.guild is None:
        await ctx.respond("DM금지")
    else:
        try:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(get_req('http://152.70.248.4:5000/sasa/'+str(닉네임)))
            
            embedresult_sasalist = calmodule.embedresult_sasalist(response, 닉네임)
            
            await ctx.respond("", embed=embedresult_sasalist, ephemeral=True)
        except Exception as error:
            embederr = discord2.Embed(title="정보처리 과정 중 알 수 없는 오류가 발생했습니다.\n(없는 캐릭터,너무 많은 조회로 인한 서버이용 불가 등)", color=discord2.Color.red())
            await ctx.respond("", embed=embederr, view=None, ephemeral=True)
            print(error)

@client.slash_command(name="입찰",description="경매 입찰 가격 최적화")
async def 입찰(ctx: discord2.ApplicationContext, 가격: Option(int, "아이템 가격을 적으세요.", required=True, default=None)):
    if ctx.guild is None:
        await ctx.respond("DM금지")
    else:
        try:            
            embedresult_auction = calmodule.embedresult_auction(가격)

            await ctx.respond("", embed=embedresult_auction)
        except Exception as error:
            embederr = discord2.Embed(title="알 수 없는 오류가 발생했습니다.", color=discord2.Color.red())
            await ctx.respond("", embed=embederr, view=None)
            print(error)

@client.slash_command(name="시세",description="크리스탈 시세 확인")
async def 시세(ctx: discord2.ApplicationContext):
    if ctx.guild is None:
        await ctx.respond("DM금지")
    else:
        try:          
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(get_req('http://152.70.248.4:5000/crystal/'))

            embedresult_crystal = calmodule.embedresult_crystal(response)
            
            await ctx.respond("", embed=embedresult_crystal)
        except Exception as error:
            embederr = discord2.Embed(title="알 수 없는 오류가 발생했습니다.", color=discord2.Color.red())
            await ctx.respond("", embed=embederr, view=None)
            print(error)

class InfoOptions(discord2.ui.View):
    def __init__(self, ctx: commands.Context, 닉네임: str, msg: discord2.Message, embedres: discord2.Embed, embedres2: discord2.Embed, embedres3: discord2.Embed, embedres4: discord2.Embed, embedres5: discord2.Embed, embedres6: discord2.Embed, embedres7: discord2.Embed, embedres8: discord2.Embed):
        super().__init__()
        self.ctx = ctx
        self.닉네임 = 닉네임
        self.msg = msg
        self.embedres = embedres
        self.embedres2 = embedres2    
        self.embedres3 = embedres3
        self.embedres4 = embedres4
        self.embedres5 = embedres5
        self.embedres6 = embedres6
        self.embedres7 = embedres7
        self.embedres8 = embedres8
        self.add_item(discord2.ui.Button(label="문의", url="https://discord.gg/Bgsb7WkwVg", row=3))
        # self.add_item(discord.ui.Select(options=[
        #     discord.SelectOption(
        #         label="test"
        #     )
        # ]))

    @discord2.ui.button(label="캐릭터 정보", style=discord2.ButtonStyle.gray, custom_id="Chainfo")
    async def Chainfo(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].author.name)) == self.닉네임:
            await interaction.response.edit_message(embed=self.embedres, view=self)

    @discord2.ui.button(label="스킬", style=discord2.ButtonStyle.gray, custom_id="ChaSkill")
    async def ChaSkill(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].title)) == "스킬":
            await interaction.response.edit_message(embed=self.embedres3, view=self)

    @discord2.ui.button(label="보석&카드", style=discord2.ButtonStyle.gray, custom_id="ChaJewl")
    async def ChaJewl(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].title)) == "보석&카드":
            await interaction.response.edit_message(embed=self.embedres4, view=self)    

    @discord2.ui.button(label="장비", style=discord2.ButtonStyle.gray, custom_id="Chatnwlq")
    async def Chatnwlq(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].title)) == "장비":
            await interaction.response.edit_message(embed=self.embedres7, view=self) 

    @discord2.ui.button(label="악세서리", style=discord2.ButtonStyle.gray, custom_id="Dkrtptjfl")
    async def Dkrtptjfl(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].title)) == "악세서리":
            await interaction.response.edit_message(embed=self.embedres8, view=self)    

    @discord2.ui.button(label="주급", style=discord2.ButtonStyle.gray, custom_id="ChaGold")
    async def ChaGold(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].title)) == "주급":
            await interaction.response.edit_message(embed=self.embedres5, view=self)

    @discord2.ui.button(label="사사게", style=discord2.ButtonStyle.gray, custom_id="ChaSasa")
    async def ChaSasa(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].title)) == "사사게":
            await interaction.response.edit_message(embed=self.embedres6, view=self)

    @discord2.ui.button(label="캐릭터 목록", style=discord2.ButtonStyle.gray, custom_id="ChaList")
    async def ChaList(self, button: discord2.ui.Button, interaction: discord2.Interaction):
        if not (str(interaction.message.embeds[0].title)) == "캐릭터 목록":
            await interaction.response.edit_message(embed=self.embedres2, view=self)  

client.run(token)
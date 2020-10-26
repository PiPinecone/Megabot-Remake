import discord
from discord.ext import commands
from datetime import datetime
from pymongo import MongoClient
from secrets import MURL


mcli = MongoClient(MURL)
db = mcli.feedback
col = db.suggestions


class Feedback(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        name="suggest"
    )
    @commands.guild_only()
    async def suggest(self, ctx: commands.Context, *content: str):
        if "|" in content:
            try:
                stri = " ".join(content)
                indx = stri.find("|")
                title = stri[0:indx]
                description = stri[indx + 1:len(stri) + 1]
                num = db.suggestions.count() + 1
                embed = discord.Embed(title=title, description=description, color=0x3499DB)
                embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text=f"Category • {datetime.today().strftime('%m-%d-%Y')}")
                await ctx.send(embed=embed)
                suggestion = {
                    "fid": num,
                    "title": title,
                    "description": description
                }
                fb = db.suggestions.insert_one(suggestion)
                channel = self.client.get_channel(768231762705907743)
                fb_id = fb.inserted_id
                embed_2 = discord.Embed(title=title, description=description, color=0x4c2bbe)
                embed_2.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                embed_2.add_field(name="Opinion", value="0", inline=True)
                embed_2.add_field(name="Votes", value="0", inline=True)
                embed_2.add_field(name="Comments", value="0", inline=True)
                embed_2.set_footer(text=f"Category • Suggestion ID: {fb_id}")
                msg = await channel.send(embed=embed_2)
                await msg.add_reaction("<:upvote:767964478570496030>")
                await msg.add_reaction("<:downvote:767964478574690304>")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")
        else:
            try:
                stri = " ".join(content)
                title = stri
                num = db.suggestions.count() + 1
                embed = discord.Embed(title=stri, description=None, color=0x3499DB)
                embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Opinion", value="0", inline=True)
                embed.add_field(name="Votes", value="0", inline=True)
                embed.add_field(name="Comments", value="0", inline=True)
                embed.set_footer(text=f"Category • {datetime.today().strftime('%m-%d-%Y')}")
                await ctx.send(embed=embed)
                suggestion = {
                    "fid": num,
                    "title": title
                }
                fb = db.suggestions.insert_one(suggestion)
                channel = self.client.get_channel(768231762705907743)
                fb_id = fb.inserted_id
                embed_2 = discord.Embed(title=title, description=None, color=0x4c2bbe)
                embed_2.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                embed_2.add_field(name="Opinion", value="0", inline=True)
                embed_2.add_field(name="Votes", value="0", inline=True)
                embed_2.add_field(name="Comments", value="0", inline=True)
                embed_2.set_footer(text=f"Category • Suggestion ID: {fb_id}")
                msg = await channel.send(embed=embed_2)
                await msg.add_reaction("<:upvote:767964478570496030>")
                await msg.add_reaction("<:downvote:767964478574690304>")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")

    # @commands.command(
        # name="comment"
    # )
    # @commands.guild_only()
    # async def comment(self, ctx: commands.Context, *content: str):
        # try:
            # stri = " ".join(content)
            # embed = discord.Embed(title="Comment added:", description=stri, color=0x3499DB)
            # embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
            # embed.set_footer(text=f"Category • Suggestion ID: {fb_id}")
            # await ctx.send(embed=embed)
        # except discord.HTTPException as err:
            # await ctx.send(f"Error: {err.text}")

    # @commands.command(
    #     name="info"
    # )
    # @commands.guild_only()
    # async def info(self, ctx: commands.Context):


def setup(client: commands.Bot):
    client.add_cog(Feedback(client))

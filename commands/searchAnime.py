import discord
from queries.idQuery import SearchByID
from queries.titleQuery import SearchByTitle
from variables.idVar import GetByID
from variables.titleVar import GetByTitle
from queries.runQuery import run_query
from misc.clean import removeTags

def animeSearch(title):
    if title.isnumeric():
        query = SearchByID()
        variables = GetByID('anime', title)
    elif not title.isnumeric():
        query = SearchByTitle()
        variables = GetByTitle('anime', title)
    if variables:
        result = run_query(query, variables)
        if not result:
            return discord.Embed(description="There does not exist an anime with a title/ID of {}.".format(title))
        x = result["data"]["Media"]["studios"]["edges"]
        studio_name = x[0]["node"]["name"]
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=('{} ({}) {}'.format(result["data"]["Media"]["title"]["romaji"],
                                       result["data"]["Media"]["title"]["english"],
                                       result["data"]["Media"]["format"])),
            url=result["data"]["Media"]["siteUrl"],
            description=(removeTags(result["data"]["Media"]["description"])).replace("&quot;", '"')
        )
        embed.add_field(name="Status", value=result["data"]["Media"]["status"].upper(), inline=True)
        embed.add_field(name="Season",
                        value='{} {}'.format(result["data"]["Media"]["season"], result["data"]["Media"]["seasonYear"]),
                        inline=True)
        embed.add_field(name="Number of Episodes", value=result["data"]["Media"]["episodes"], inline=True)
        embed.add_field(name="Duration",
                        value='{} minutes/episode'.format(result["data"]["Media"]["duration"], inline=True))
        embed.add_field(name="Favourites", value=result["data"]["Media"]["favourites"], inline=True)
        embed.add_field(name="Average Score", value='{}%'.format(result["data"]["Media"]["averageScore"], inline=True))
        embed.add_field(name="Studio", value=f"**{studio_name}**", inline=False)
        embed.set_thumbnail(url=result["data"]["Media"]["coverImage"]["large"])
        return embed

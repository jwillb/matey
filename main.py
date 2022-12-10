import discord
import os
import requests
from arr import RadarrInstance, SonarrInstance
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("BOT_TOKEN")


bot = discord.Bot()

sonarr_instance = SonarrInstance(os.environ.get("SONARR_API_KEY"), os.environ.get("SONARR_BASE_URL"))
radarr_instance = SonarrInstance(os.environ.get("RADARR_API_KEY"), os.environ.get("RADARR_BASE_URL"))

@bot.event
async def on_ready():
    print(f"{bot.user} is ready to go!")

@bot.slash_command(name = "download", description = "Download a file")
async def dl_file(ctx, link, file_name):
    await ctx.respond(f"Attempting to downloading from URL: {link}")
    response = requests.get(link, allow_redirects=True)
    with open(file_name, 'wb') as f:
        f.write(response.content)

media = discord.SlashCommandGroup("media", "Commands to manage movies/tv")
sonarr = media.create_subgroup("sonarr", "Search for and download TV shows")
radarr = media.create_subgroup("radarr", "Search for and download movies")

@sonarr.command()
async def list(ctx):
    await ctx.respond(sonarr_instance.listSeries())

@sonarr.command()
async def add(ctx, search_term):
    await ctx.defer()
    show, title, year = sonarr_instance.lookup(search_term)
    response_code = sonarr_instance.addSeries(show)
    await ctx.respond(f"Search for `{search_term}` returned `{response_code}` (Show found: `{title} ({year})`)")

@radarr.command()
async def list(ctx):
    await ctx.respond(radarr_instance.listMovies())

@radarr.command()
async def add(ctx, search_term):
    await ctx.defer()
    movie, title, year = radarr_instance.lookup(search_term)
    response_code = radarr_instance.addMovie(movie)
    await ctx.respond(f"Search for `{search_term}` returned `{response_code}` (Movie found: `{title} ({year})`)")

bot.add_application_command(media)

token = "MTA1MDkxNDUxMzE2OTQxNjM0Mg.GoyC3N.aR4vcsnBmdsSAhS0yAOVMzz92Uwkk92xBso2jg"

bot.run(token)


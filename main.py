import discord
import os
import requests
from subprocess import call
from arr import RadarrInstance, SonarrInstance
from qbittorrent import qBittorrentInstance
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("BOT_TOKEN")


bot = discord.Bot()

sonarr_instance = SonarrInstance(os.environ.get("SONARR_API_KEY"), os.environ.get("SONARR_BASE_URL"))
radarr_instance = SonarrInstance(os.environ.get("RADARR_API_KEY"), os.environ.get("RADARR_BASE_URL"))
qbit_instance = qBittorrentInstance(os.environ.get("QBIT_BASE_URL"), os.environ.get("QBIT_USERNAME"), os.environ.get("QBIT_PASSWORD"))
qbit_instance.login()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready to go!")

media = discord.SlashCommandGroup("media", "Commands to manage movies/tv")
sonarr = media.create_subgroup("sonarr", "Search for and download TV shows")
radarr = media.create_subgroup("radarr", "Search for and download movies")
download = discord.SlashCommandGroup("download", "Download files")
torrent = download.create_subgroup("torrent", "Add and view torrents in qBittorrent")

@download.command()
async def aria2(ctx, link):
    await ctx.respond("Download started")
    return_value = call(f"aria2c -d ./downloads {link}", shell=True)
    print(return_value)

@torrent.command()
async def add(ctx, magnet_link):
    status_code = qbit_instance.addTorrent(magnet_link, "discord_bot")
    await ctx.respond(f"Received: `{status_code}`")

@torrent.command()
async def list(ctx):
    await ctx.respond("Partial Torrent Name | Category | Download Speed | Ratio")
    torrent_list = qbit_instance.getTorrentList()
    message = ""
    for i in torrent_list:
        message = message + f"{i[0]} | {i[1]} | {i[2]} | {i[3]}" + "\n"
    if len(message) > 2000:
        for i in range(len(message) // 2000):
            await ctx.send(message[i*2000:((i*2000)+2000)])
    else:
        await ctx.send(message)

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
bot.add_application_command(download)

token = "MTA1MDkxNDUxMzE2OTQxNjM0Mg.GoyC3N.aR4vcsnBmdsSAhS0yAOVMzz92Uwkk92xBso2jg"

bot.run(token)


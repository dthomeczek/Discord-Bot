# This file handles the bulk of the Discord bot functionality
import discord
from discord.ext import commands
import googleapiclient.discovery
import asyncio
import custom_help

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents, help_command=custom_help.CustomHelpCommand())
token = ' ' # Replace whitespace with your Discord bot token


youtube_api_key = ' ' # Replace whitespace with your YouTube Data API key
youtube_channel_id = ' '  # Replace whitespace with your YouTube channel ID
youtube_notifs = 'YouTube Notifs' # Replace with the name of the role you would like to notify

# Function to fetch the latest video from your YouTube channel
async def get_latest_youtube_video():
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.search().list(
        part='id',
        channelId=youtube_channel_id,
        maxResults=1,
        order='date'
    )
    response = request.execute()
    if 'items' in response:
        return response['items'][0]['id']['videoId']
    return None

# Function to load announced video IDs from a file with name announced_video_ids.txt to prevent announcing the same video again
def load_announced_video_ids():
    try:
        with open('announced_video_ids.txt', 'r') as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

# Function to save announced video IDs to a file with name announced_video_ids.txt to prevent announcing the same video again
def save_announced_video_ids(video_ids):
    with open('announced_video_ids.txt', 'w') as file:
        file.write('\n'.join(video_ids))

# Bot connection verification
@client.event
async def on_ready():
    print('Logged in as a bot {0.user}'.format(client))

    # Schedule the background tasks when the bot is ready
    await start_background_tasks()

# Gets the message and sends a response along with splitting the username in the event they use the old '#' username identifiers
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)

    print(f'Message {user_message} by {username}')

    if message.author == client.user:
        return

    await client.process_commands(message)

# A simple command for pinging the bot to get a simple pong response
@client.command()
async def ping(ctx):
    '''Pong!'''
    await ctx.send('Pong!')

# Information tied to my social media pages
@client.command()
async def links(ctx):
    '''This brings up my social links!'''
    embed = discord.Embed(
        title='My Socials',
        description='Here are some of my social media profiles and links:',
        color=0x00ff00  # Change the color as needed
    )
    # Replace whitespace in the value portion with a link to your social media pages
    embed.add_field(name='Instagram', value=' ', inline=False) 
    embed.add_field(name='Twitter (X)', value=' ', inline=False)
    # Add more fields for other links
    await ctx.send(embed=embed)

# Information tied to my Twitch channel
@client.command()
async def twitch(ctx):
    '''This contains my Twitch channel!'''
    embed = discord.Embed(
        title='My Twitch Channel',
        description='Check out my Twitch channel:',
        color=0x00ff00  # Change the color as needed
    )
    
    # Replace 'twitch_image.png' with the actual file path of your local PNG image for your channel icon
    file = discord.File('twitch_image.png', filename='twitch_image.png')
    embed.set_image(url='attachment://twitch_image.png')
    embed.add_field(name=' ', value=' ') # Replace whitespace in name with your Twitch username and the whitespace in value with your Twitch channel URL
    await ctx.send(embed=embed, file=file)

# Information tied to my YouTube channel
@client.command()
async def youtube(ctx):
    '''This contains my YouTube channel!'''
    embed = discord.Embed(
        title='My YouTube Channel',
        description='Subscribe to my YouTube channel:',
        color=0x00ff00  # Change the color as needed
    )

    # Replace 'twitch_image.png' with the actual file path of your local PNG image for your channel icon
    file = discord.File('twitch_image.png', filename='twitch_image.png')
    embed.set_image(url='attachment://twitch_image.png')
    embed.add_field(name='YouTube Channel URL', value=' ') # Replace whitespace in name with your YouTube username and the whitespace in value with your YouTube channel URL
    await ctx.send(embed=embed, file=file)

# Function to check for new YouTube videos and send announcements
async def check_for_new_youtube_videos():
    await client.wait_until_ready()  # Wait until the bot is ready

    # Load the previously announced video IDs
    announced_video_ids = load_announced_video_ids()

    while not client.is_closed():
        latest_video_id = await get_latest_youtube_video()
        if latest_video_id and latest_video_id not in announced_video_ids:
            # Get the announcements channel
            youtube_announce_channel = discord.utils.get(client.guilds[0].text_channels, name=' ') # Replace whitespace in name with your YouTube video notifications channel name
            youtube_notifs_role = discord.utils.get(client.guilds[0].roles, name=youtube_notifs)
            if youtube_announce_channel and youtube_notifs_role:
                video_url = f'https://www.youtube.com/watch?v={latest_video_id}'
                announcement_message = f'{youtube_notifs_role.mention} <username> uploaded a new video! Go check it out!\n {video_url}' # Replace <username> with your username
                await youtube_announce_channel.send(announcement_message)
                announced_video_ids.add(latest_video_id)  # Add the video ID to prevent duplicates
                save_announced_video_ids(announced_video_ids)  # Save the updated set to the file
        print('YouTube API Check')
        await asyncio.sleep(1800)  # Check every half hour (1800 seconds)

# Define the function to schedule the background task
async def start_background_tasks():
    client.loop.create_task(check_for_new_youtube_videos())

client.run(token)
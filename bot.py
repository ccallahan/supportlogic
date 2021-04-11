import requests, uuid, json, discord
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='sl!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def trans(ctx, *message: str):
    # Translates message automatically using Azure.
    # Add your subscription key and endpoint
    subscription_key = "INSERT_KEY_HERE"
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "global"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': ['en']
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    tmp1 = ' '.join(message)
    body = [{
        'text': str(tmp1)
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    trans = response[0]["translations"][0]["text"]
    trans_lang = response[0]['detectedLanguage']['language']
    trans_conf = response[0]['detectedLanguage']['score']

    if trans_conf == 1.0:
        await ctx.reply("SupportLogic::Translate::Azure::" + trans_lang + "::Result $$ " + trans)
    if trans_conf <= 0.75:
        await ctx.reply("SupportLogic::Translate::Azure::" + trans_lang + "::Result::Caution $$ " + trans)
    if trans_conf <= 0.5:
        await ctx.reply("SupportLogic::Translate::Azure::" + trans_lang + "::Result::Warning $$ " + trans)

bot.run('</lol>')

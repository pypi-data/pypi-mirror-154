olekps.py
==========

.. image:: https://discord.com/api/guilds/972499131044069396/embed.png
   :target: https://discord.gg/GChBnwVEHv
   :alt: Discord server invite


olekps.py libraly


Installing
~~~~~~~~~~



.. code:: sh

    # Linux/macOS
    pip3 install -U olekps.py

    # Windows
    pip install -U olekps.py


Level Card Example
~~~~~~~~~~~~~~~~~~

.. code:: py

   from discord.ext import commands
   from mariocard import *

   client = commands.Bot(command_prefix=".")

   @client.command()
   async def card(ctx):
       #creating levelcard object
       levelcard = LevelCard()
       
       #setting avatar url for image
       levelcard.avatar = ctx.author.avatar_url
       
       #setting background file path or link
       levelcard.path = "https://raw.githubusercontent.com/mario1842/mariocard/main/bg.png"
       
       #setting member name
       levelcard.name = ctx.author
       
       #setting xp for bar on card
       levelcard.xp = 10
       
       #setting required xp for bar on card
       levelcard.required_xp = 20
       
       #setting level to text on crad
       levelcard.level = 2

       #sending image to discord channel
       await ctx.send(file=await levelcard.create())

   client.run("token")

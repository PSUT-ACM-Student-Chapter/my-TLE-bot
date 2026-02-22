import os
import discord
from discord.ext import tasks, commands

class AutoScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gudgitters_task.start()

    def cog_unload(self):
        self.gudgitters_task.cancel()

    @tasks.loop(hours=24) 
    async def gudgitters_task(self):
        # Fetch the channel ID from environment variables
        channel_id_str = os.environ.get('LOGGING_COG_CHANNEL_ID')
        
        if not channel_id_str:
            print("Scheduler: LOGGING_COG_CHANNEL_ID environment variable is missing.")
            return
            
        try:
            # Discord IDs must be integers
            channel_id = int(channel_id_str)
        except ValueError:
            print("Scheduler: LOGGING_COG_CHANNEL_ID must be a valid integer.")
            return

        channel = self.bot.get_channel(channel_id)
        
        if not channel:
            print(f"Scheduler: Could not find channel with ID {channel_id}")
            return
        
        msg = await channel.send(';gudgitters')
        
        ctx = await self.bot.get_context(msg)
        
        if ctx.valid:
            await self.bot.invoke(ctx)
            
        await msg.delete()

    @gudgitters_task.before_loop
    async def before_task(self):
        # Wait until the bot is fully logged in before starting the timer
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AutoScheduler(bot))

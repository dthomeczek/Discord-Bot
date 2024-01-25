# The purpose of this command is to generate a custom design for the help command instead of the default Discord bot help command.
import discord
from discord.ext.commands import HelpCommand

# This class overrides the help command menu with a 
class CustomHelpCommand(HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        # Create an embedded menu to list commands and their functionality
        embed = discord.Embed(
            title="**Command List**",
            description="**Below is the list of all commands and their uses**",
            color=0x00ff00  # Change the color as needed
        )

        help_command = None
        other_commands = []

        for cog, commands in mapping.items():
            for command in commands:
                if not command.hidden:
                    if command.name == "help":
                        help_command = command
                    else:
                        other_commands.append(command)

        # Sort other_commands alphabetically by command name
        other_commands.sort(key=lambda command: command.name)

        # Add the Help command at the beginning
        if help_command:
            embed.add_field(name=f"{self.get_command_signature(help_command)}", value=help_command.help, inline=False)

        # Add the sorted other commands
        for command in other_commands:
            embed.add_field(name=f"{self.get_command_signature(command)}", value=command.help, inline=False)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        # This method is called when the user runs "!help <cog_name>".
        pass  # Implement your custom behavior here

    async def send_group_help(self, group):
        # This method is called when the user runs "!help <command_name>".
        pass  # Implement your custom behavior here


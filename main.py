
import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

allowed_roles = [
    "Support 2", "Moderator", "Administrator",
    "Management", "» Projektleitung", "» Projektinhaber"
]
whitelist_channel_id = 1388462105744773213
role_to_give_name = "» Whitelisted"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="whitelist", description="Vergebe die Whitelist-Rolle an einen Nutzer")
@app_commands.describe(user="Der Nutzer, der gewhitelisted werden soll")
async def whitelist(interaction: discord.Interaction, user: discord.Member):
    if interaction.channel.id != whitelist_channel_id:
        await interaction.response.send_message(
            "❌ Dieser Befehl ist nur im Whitelist-Channel erlaubt.",
            ephemeral=True
        )
        return

    author_roles = [role.name for role in interaction.user.roles]
    if not any(role in allowed_roles for role in author_roles):
        await interaction.response.send_message(
            "❌ Du hast keine Berechtigung für diesen Befehl.",
            ephemeral=True
        )
        return

    role = discord.utils.get(interaction.guild.roles, name=role_to_give_name)
    if role is None:
        await interaction.response.send_message(
            "❌ Die Rolle » Whitelisted wurde nicht gefunden.",
            ephemeral=True
        )
        return

    await user.add_roles(role)
    await interaction.response.send_message(
        f"✅ {user.mention} wurde erfolgreich gewhitelisted!",
        ephemeral=False
    )

bot.run(os.getenv("DISCORD_TOKEN"))

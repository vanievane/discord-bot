import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_ROLES = [
    "Support 2",
    "Moderator",
    "Administrator",
    "Management",
    "» Projektleitung",
    "» Projektinhaber"
]

ALLOWED_CHANNEL_NAME = "「🔘」whitelist"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="whitelist", description="Vergebe die » Whitelisted Rolle")
@app_commands.describe(user="Der Benutzer, der gewhitelistet werden soll")
async def whitelist(interaction: discord.Interaction, user: discord.Member):
    if interaction.channel.name != ALLOWED_CHANNEL_NAME:
        await interaction.response.send_message(
            f"❌ Dieser Befehl ist nur im Channel #{ALLOWED_CHANNEL_NAME} erlaubt.",
            ephemeral=True
        )
        return

    author_roles = [role.name for role in interaction.user.roles]
    if not any(role in ALLOWED_ROLES for role in author_roles):
        await interaction.response.send_message("❌ Du hast keine Berechtigung, diesen Befehl zu nutzen.", ephemeral=True)
        return

    role = discord.utils.get(interaction.guild.roles, name="» Whitelisted")
    if not role:
        await interaction.response.send_message("❌ Die Rolle » Whitelisted wurde nicht gefunden.", ephemeral=True)
        return

    await user.add_roles(role)
    await interaction.response.send_message(f"✅ {user.mention} wurde erfolgreich auf die Whitelist gesetzt. Willkommen!", ephemeral=False)

bot.run(os.getenv("DISCORD_TOKEN"))
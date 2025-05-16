import discord
from discord.ext import commands
from discord import app_commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# File to store user opt-in list
DATA_FILE = "notify_users.json"

# Load opt-in users
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        notify_users = set(json.load(f))
else:
    notify_users = set()

# Channel ID to monitor
ALLOWED_CHANNEL_ID = 1372839940207153244  # 🔁 Replace with your channel ID

ROLE_EMBED_MAP = {
    1372127561059930204: {"title": "🍫 Cacao in stock", "color": 3447003, "thumbnail": ""},
    1372127854048968735: {"title": "🌶️ Pepper in stock!", "color": 16776960, "thumbnail": ""},
    1372128558029209622: {"title": "🍄‍ Mushroom in stock!", "color": 10038562, "thumbnail": ""},
    1372127141642371103: {"title": "🍇 Grape in stock!", "color": 11393254, "thumbnail": ""},
    1372127342159200326: {"title": "🍑 Peach in stock!", "color": 8311585, "thumbnail": ""},
    1372128161114099762: {"title": "🥭 Mango in stock!", "color": 5763719, "thumbnail": ""},
    1372128877907935232: {"title": "🐛 Bug Egg in stock!", "color": 15158332, "thumbnail": ""},
    1372129118119923733: {"title": "🥚 Legendary Egg in stock!", "color": 15844367, "thumbnail": ""},
    1372129377365659668: {"title": "🟦 Rare Egg in stock!", "color": 3066993, "thumbnail": ""},
    1372129506118074438: {"title": "🌠  Night in started!", "color": 10038562, "thumbnail": ""},
    1372129843084263474: {"title": "⛈️ Thunder started!", "color": 3447003, "thumbnail": ""},
    1372130091022155828: {"title": "🌨️ Snow started!", "color": 1752220, "thumbnail": ""},
    1372129735240581151: {"title": "🌧️ Rain started!", "color": 15844367, "thumbnail": ""},
    1372130212439130152: {"title": "⚡ Lightning Rod in stock!", "color": 9807270, "thumbnail": ""},
    1372130535194759199: {"title": "🟡 Advanced Sprinkler in stock", "color": 15105570, "thumbnail": ""},
    1372130898547314709: {"title": "🟢 Godly Sprinkler in stock!", "color": 15158332, "thumbnail": ""},
    1372131057637261465: {"title": "🟧 Master Sprinkler", "color": 3447003, "thumbnail": ""},
    1372837142396403772: {"title": "Update Live Now!", "color": 15158332, "thumbnail": ""},
}

def save_notify_users():
    with open(DATA_FILE, "w") as f:
        json.dump(list(notify_users), f)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user}")

@tree.command(name="in", description="Subscribe to alerts via DM when weather or stock updates happen.")
async def notify(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in notify_users:
        await interaction.response.send_message("❌ You are already subscribed to notifications.", ephemeral=True)
    else:
        notify_users.add(user_id)
        save_notify_users()
        await interaction.response.send_message("✅ You have been subscribed to notifications.", ephemeral=True)

@tree.command(name="out", description="Unsubscribe from DM alerts.")
async def unnotify(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in notify_users:
        notify_users.remove(user_id)
        save_notify_users()
        await interaction.response.send_message("🚫 You have been unsubscribed from notifications.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You were not subscribed.", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ✅ Channel restriction
    if message.channel.id != 1372839940207153244:
        return

    for role in message.role_mentions:
        role_info = ROLE_EMBED_MAP.get(role.id)
        if role_info:
            embed = discord.Embed(
                title=role_info["title"],
                color=role_info["color"]
            )
            if role_info["thumbnail"]:
                embed.set_thumbnail(url=role_info["thumbnail"])

            for user_id in notify_users:
                try:
                    user = await bot.fetch_user(user_id)
                    await user.send(embed=embed)
                except Exception as e:
                    print(f"❗ Failed to DM {user_id}: {e}")

    await bot.process_commands(message)

# 🔐 Add your bot token here
bot.run("MTM3MTA5OTIwMDQ0Nzg0NDUwMw.G2dxzw.p63Me4amaw2tLWBgaCXidridAKfdS6xnqiCaek")

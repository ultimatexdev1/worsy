import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash komut sync
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} aktif!")

# ======================
# 📢 DUYURU KOMUTU
# ======================
@bot.tree.command(name="duyuru", description="Sunucuya duyuru yapar")
@app_commands.describe(mesaj="Duyuru mesajı")
async def duyuru(interaction: discord.Interaction, mesaj: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Yetkin yok!", ephemeral=True)
        return

    embed = discord.Embed(
        title="📢 Worsy Duyuru",
        description=mesaj,
        color=discord.Color.orange()
    )
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("Duyuru gönderildi!", ephemeral=True)

# ======================
# 🤝 PARTNER KOMUTU
# ======================
@bot.tree.command(name="partner-paylaş", description="Partner paylaşımı yapar")
@app_commands.describe(mesaj="Partner mesajı")
async def partner(interaction: discord.Interaction, mesaj: str):
    embed = discord.Embed(
        title="🤝 Partner Paylaşımı",
        description=mesaj,
        color=discord.Color.blue()
    )
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("Paylaşıldı!", ephemeral=True)

# ======================
# 🎟️ TICKET SİSTEMİ
# ======================
class TicketButton(discord.ui.View):
    @discord.ui.button(label="Ticket Aç", style=discord.ButtonStyle.green)
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True)
        }
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites
        )
        await channel.send(f"{interaction.user.mention} ticket açıldı.")
        await interaction.response.send_message("Ticket oluşturuldu!", ephemeral=True)

@bot.tree.command(name="ticket-kur", description="Ticket sistemi kurar")
async def ticket_kur(interaction: discord.Interaction):
    await interaction.channel.send(
        "Ticket açmak için butona bas:",
        view=TicketButton()
    )
    await interaction.response.send_message("Kuruldu!", ephemeral=True)

# ======================
# 👥 INVITE SAYACI (basit)
# ======================
invites = {}

@bot.event
async def on_member_join(member):
    # basit sistem (geliştirilebilir)
    channel = discord.utils.get(member.guild.text_channels, name="invite-log")
    if channel:
        await channel.send(f"{member.mention} sunucuya katıldı!")

# ======================
# 🔨 MODERASYON
# ======================
@bot.tree.command(name="ban", description="Kullanıcıyı banlar")
@app_commands.describe(kullanici="Banlanacak kişi", sebep="Sebep")
async def ban(interaction: discord.Interaction, kullanici: discord.Member, sebep: str = "Belirtilmedi"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("Yetkin yok!", ephemeral=True)
        return

    await kullanici.ban(reason=sebep)
    await interaction.response.send_message(f"{kullanici} banlandı.")

# ======================
import os
bot.run(os.getenv("TOKEN"))

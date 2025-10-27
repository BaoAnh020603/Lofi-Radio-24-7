import discord
from discord.ext import commands
from discord import app_commands # ⭐️ ĐÃ THÊM DÒNG NÀY ĐỂ FIX LỖI app_commands
import yt_dlp
import random
import asyncio
import os # ⭐️ ĐÃ THÊM DÒNG NÀY ĐỂ FIX LỖI os.getenv
import requests
from keep_alive import keep_alive 

keep_alive()

# ===== CẤU HÌNH BOT =====
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
# Nếu bot của bạn là bot LOFI (không cần đọc nội dung chat), bạn có thể bỏ qua intent này
# Tuy nhiên, nếu bạn đã dùng Slash Command, việc này không quan trọng
# intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== DANH SÁCH KÊNH LOFI THEO THỂ LOẠI =====
# ⚠️ Cảnh báo: Các URL này là Playlist/Radio URL của YouTube (có &list=...).
# Chúng CÓ THỂ gặp lỗi xác thực/kết nối nếu YouTube thay đổi thuật toán.
LOFI_CHANNELS = {
    "study": ["https://www.youtube.com/watch?v=9kzE8isXlQY&list=RD9kzE8isXlQY&start_radio=1", "https://www.youtube.com/watch?v=CfPxlb8-ZQ0"],
    "anime": ["https://www.youtube.com/watch?v=GNWLILeztaI&list=RDGNWLILeztaI&start_radio=1"],
    "halloween": ["https://www.youtube.com/watch?v=SOMCdjEtiFw&list=RDSOMCdjEtiFw&start_radio=1"],
    "gaming": ["https://www.youtube.com/watch?v=FFfdyV8gnWk"],
    "sleep": ["https://www.youtube.com/watch?v=gWp8xxB2PxM&list=RDgWp8xxB2PxM&start_radio=1"],
    "synthwave": ["https://www.youtube.com/watch?v=TlWYgGyNnJo&list=RDTlWYgGyNnJo&start_radio=1"],
    "japanese": ["https://www.youtube.com/watch?v=EtD7_8kCMHA&list=RDEtD7_8kCMHA&start_radio=1"],
    "kpop": ["https://www.youtube.com/watch?v=NZIElf9DTQU&list=RDNZIElf9DTQU&start_radio=1"],
    "jazz": ["https://www.youtube.com/watch?v=-R0UYHS8A_A&list=RD-R0UYHS8A_A&start_radio=1"],
    "covers": ["https://www.youtube.com/watch?v=84u41t5v4j4&list=RD84u41t5v4j4&start_radio=1"],
    "christmas": ["https://www.youtube.com/watch?v=Ru8DQ5f5A6U&list=RDRu8DQ5f5A6U&start_radio=1"],
    "mix": ["https://www.youtube.com/watch?v=CLeZyIID9Bo&list=RDCLeZyIID9Bo&start_radio=1"],
}

# ===== LƯU THỂ LOẠI HIỆN TẠI CHO MỖI GUILD =====
current_genre = {}  # {guild_id: genre_value}

# ===== HÀM PHÁT NHẠC NGẪU NHIÊN VỚI LOOP (ĐÃ SỬA ASYNC) =====
async def play_lofi(vc, genre_value):
    url_list = LOFI_CHANNELS.get(genre_value, [])
    if not url_list:
        print("⚠️ Không có kênh nào trong thể loại này!")
        return

    url = random.choice(url_list)

    # Đưa khối yt_dlp sang thread an toàn
    def extract_audio_info():
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url'], info.get('title', 'Lofi Radio Stream')

    try:
        audio_url, title = await asyncio.to_thread(extract_audio_info)
    except Exception as e:
        print(f"❌ Lỗi yt-dlp khi trích xuất URL: {e}")
        # Thử lại ngay lập tức nếu lỗi xảy ra
        await play_lofi(vc, genre_value)
        return


    def after_play(error):
        if error:
            print(f"Player error: {error}")
        
        # ⭐️ Lệnh tự động chuyển bài an toàn
        asyncio.run_coroutine_threadsafe(play_lofi(vc, genre_value), bot.loop)

    vc.stop()
    vc.play(
        discord.FFmpegPCMAudio(
            audio_url,
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            options='-vn'
        ),
        after=after_play
    )
    # Cập nhật trạng thái bot
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{title} ({genre_value.capitalize()})"))


# ===== SỰ KIỆN ON_READY =====
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Đã đồng bộ {len(synced)} slash command.")
    except Exception as e:
        print(f"❌ Lỗi khi sync slash command: {e}")
    
    await bot.change_presence(activity=discord.Game(name="Lofi Radio | Dùng /play"))


# ===== LỆNH /play CHO NGƯỜI DÙNG CHỌN THỂ LOẠI (ĐÃ SỬA LỖI app_commands) =====
@bot.tree.command(name="play", description="Phát Lofi Radio 24/7 🎶")
@app_commands.describe(genre="Chọn thể loại Lofi bạn muốn nghe")
@app_commands.choices(genre=[
    app_commands.Choice(name="Study", value="study"),
    app_commands.Choice(name="Anime", value="anime"),
    app_commands.Choice(name="Halloween", value="halloween"),
    app_commands.Choice(name="Gaming", value="gaming"),
    app_commands.Choice(name="Sleep", value="sleep"),
    app_commands.Choice(name="Synthwave", value="synthwave"),
    app_commands.Choice(name="Japanese", value="japanese"),
    app_commands.Choice(name="Kpop", value="kpop"),
    app_commands.Choice(name="Jazz", value="jazz"),
    app_commands.Choice(name="Covers", value="covers"),
    app_commands.Choice(name="Christmas", value="christmas"),
    app_commands.Choice(name="Mix", value="mix"),
])
async def play(interaction: discord.Interaction, genre: app_commands.Choice[str]):
    await interaction.response.defer()

    if interaction.user.voice is None:
        await interaction.followup.send("❌ Bạn phải vào kênh thoại trước!", ephemeral=True)
        return

    voice_channel = interaction.user.voice.channel

    if interaction.guild.voice_client is None:
        vc = await voice_channel.connect()
    else:
        vc = interaction.guild.voice_client
        if vc.channel != voice_channel:
            await vc.move_to(voice_channel)

    genre_value = genre.value
    current_genre[interaction.guild.id] = genre_value
    
    # ⭐️ Gọi hàm phát nhạc là async ⭐️
    await play_lofi(vc, genre_value)

    await interaction.followup.send(f"🎵 Đang phát **{genre.name} Lofi Radio** 24/7 💫")

# ===== LỆNH /stop =====
@bot.tree.command(name="stop", description="Dừng phát nhạc ⏹️")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await bot.change_presence(activity=discord.Game(name="Lofi Radio | Dùng /play"))
        await interaction.response.send_message("🛑 Đã dừng nhạc.")
    else:
        await interaction.response.send_message("⚠️ Không có bài nào đang phát.", ephemeral=True)

# ===== LỆNH /leave =====
@bot.tree.command(name="leave", description="Bot rời khỏi kênh thoại 🚪")
async def leave(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc:
        vc.stop()
        await vc.disconnect()
        current_genre.pop(interaction.guild.id, None)
        await bot.change_presence(activity=discord.Game(name="Lofi Radio | Dùng /play"))
        await interaction.response.send_message("👋 Bot đã rời khỏi kênh thoại.")
    else:
        await interaction.response.send_message("⚠️ Bot không ở trong kênh thoại.", ephemeral=True)

# ===== CHẠY BOT (Đã sửa lỗi os.getenv) =====
TOKEN = os.getenv("DISCORD_TOKEN") 

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ LỖI NGHIÊM TRỌNG: KHÔNG TÌM THẤY DISCORD_TOKEN trong biến môi trường.")

import os
import io
from datetime import datetime, timedelta
import re
import threading

from flask import Flask

import discord
from discord.ext import commands
from dotenv import load_dotenv


# =========================================================
# WEB SERVER - Render / Uptime
# =========================================================
# خادم ويب بسيط حتى تحصل خدمة Render على رابط عام يمكن لخدمات
# الـ Uptime زيارته. لا يؤثر على عمل بوت Discord.
app = Flask(__name__)


@app.route("/")
def home():
    return "Jurma Bot is Online", 200


@app.route("/health")
def health():
    return {"status": "online", "service": "Jurma Bot"}, 200


def run_web_server():
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, use_reloader=False)


def start_web_server():
    thread = threading.Thread(
        target=run_web_server,
        name="JurmaWebServer",
        daemon=True,
    )
    thread.start()


# =========================================================
# CONFIG - إعدادات البوت
# =========================================================

# توكن البوت موجود في ملف .env
TOKEN_ENV_NAME = "DISCORD_TOKEN"


# Category التي سيتم إنشاء التذاكر داخلها
TICKET_CATEGORY_ID = 1536039807527030967


# رتب فرق التذاكر
SUPPORT_ROLE_ID = 1534559093635813507  # Help
ADS_INTRO_ROLE_ID = 1539579169455738910  # ADS + Introduction

# الرتبة التي يحصل عليها العضو الجديد تلقائيًا
AUTO_ROLE_ID = 1538801067670638703


# قناة الـ Logs
LOG_CHANNEL_ID = 1536321049254301789


# اسم التذاكر
TICKET_NAME_PREFIX = "ticket"


# =========================================================
# صور اللوحات
# =========================================================
# رابط صورة لوحة التذاكر.
TICKET_PANEL_IMAGE_URL = ""

# رابط صورة لوحة البحث عن اللاعبين.
PLAYER_SEARCH_PANEL_IMAGE_URL = ""

# رابط صورة لوحة الألوان. اتركه فارغًا حتى تضيف الصورة لاحقًا.
COLOR_PANEL_IMAGE_URL = ""


# =========================================================
# Message Logs - لوق الرسائل
# =========================================================
# هذا اللوق مستقل عن لوق التذاكر.
MESSAGE_LOG_CHANNEL_ID = 1539255658350772245


# =========================================================
# Color Roles - الألوان
# =========================================================
# 1-10 خانات. الخانات 9 و10 غير مهيأة حاليًا لأنك أرسلت 8 IDs فقط.
COLOR_ROLE_IDS = {
    1: 1538580023286693948,
    2: 1538580056073568326,
    3: 1538580086083817603,
    4: 1538580135492591706,
    5: 1538580167428149349,
    6: 1538580212386898030,
    7: 1538582316706959451,
    8: 1538582349745225838,
    9: 0,
    10: 0,
}

COLOR_EMOJIS = {
    1: "<:color_1:1539590381140836374>",
    2: "<:color_2:1539590440343568454>",
    3: "<:color_3:1539590480067694725>",
    4: "<:color_4:1539590523755560960>",
    5: "<:color_5:1539590560984080384>",
    6: "<:color_6:1539590618316144710>",
    7: "<:color_7:1539590655888597053>",
    8: "<:color_8:1539590693196927006>",
}


COLOR_NAMES = {
    1: "اللون 1",
    2: "اللون 2",
    3: "اللون 3",
    4: "اللون 4",
    5: "اللون 5",
    6: "اللون 6",
    7: "اللون 7",
    8: "اللون 8",
    9: "اللون 9",
    10: "اللون 10",
}


# =========================================================
# Player Search - البحث عن اللاعبين
# =========================================================
PLAYER_SEARCH_CHANNEL_ID = 1538226798301810738

GAME_OPTIONS = {
    "minecraft_bedrock": {
        "name": "Minecraft Bedrock",
        "role_id": 1539260165134618674,
        "emoji": "<:minecraft_999:1539261932391899249>",
        "voice_id": 1536741145789472818,
    },
    "minecraft_pc": {
        "name": "Minecraft PC",
        "role_id": 1539260211188076574,
        "emoji": "<:minecraft_999:1539261932391899249>",
        "voice_id": 1539259615047458816,
    },
    "gta_v": {
        "name": "GTA V",
        "role_id": 1539260271405572097,
        "emoji": "<:GTA_999:1539262065888464946>",
        "voice_id": 1539258869556056196,
    },
    "cs2": {
        "name": "CS2",
        "role_id": 1539260501551349841,
        "emoji": "<:CS2:1539552954569461770>",
        "voice_id": 1539256619500703774,
    },
    "roblox": {
        "name": "Roblox",
        "role_id": 1539260324249739354,
        "emoji": "<:RobloxBlueLogo:1539262261867315341>",
        "voice_id": 1539259279507198032,
    },
    "valorant": {
        "name": "Valorant",
        "role_id": 1539257645196640389,
        "emoji": "<:valorant_999:1539262403748036708>",
        "voice_id": 1539268036756770967,
    },
    "fortnite": {
        "name": "Fortnite",
        "role_id": 1539261259852157022,
        "emoji": "<:Fortnite:1539262605322096752>",
        "voice_id": 1539258560351965227,
    },
    "among_us": {
        "name": "Among Us",
        "role_id": 1539261344027508746,
        "emoji": "<:GAmongUs:1539262769310994563>",
        "voice_id": 1536369859653275788,
    },
    # الخانتان 9 و10 متروكتان للتوسع لاحقًا.
    "game_9": {
        "name": "لعبة 9",
        "role_id": 0,
        "emoji": "🎮",
        "voice_id": 1539268036756770967,
    },
    "game_10": {
        "name": "لعبة 10",
        "role_id": 0,
        "emoji": "🎮",
        "voice_id": None,
    },
}


# =========================================================
# تحميل التوكن
# =========================================================

load_dotenv()

TOKEN = os.getenv(TOKEN_ENV_NAME)

if not TOKEN:
    raise ValueError(
        "❌ لم يتم العثور على DISCORD_TOKEN داخل ملف .env"
    )


# =========================================================
# Intents
# =========================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# =========================================================
# إنشاء البوت
# =========================================================

class JurmaBot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):

        # تسجيل الـ Views حتى تستمر الأزرار بعد إعادة تشغيل البوت
        self.add_view(TicketView())

        self.add_view(TicketControlView())
        self.add_view(ADSOptionsView())
        self.add_view(PlayerSearchView())
        self.add_view(ColorView())

        # مزامنة Slash Commands
        synced = await self.tree.sync()

        print(
            f"Synced {len(synced)} slash command(s)"
        )


bot = JurmaBot()


# =========================================================
# دوال مساعدة
# =========================================================

def get_ticket_category(guild: discord.Guild):

    return guild.get_channel(TICKET_CATEGORY_ID)


def get_support_role(guild: discord.Guild):
    return guild.get_role(SUPPORT_ROLE_ID)


def get_ticket_support_role(guild: discord.Guild, ticket_type: str):
    role_id = ADS_INTRO_ROLE_ID if ticket_type in ("ADS", "Introduction") else SUPPORT_ROLE_ID
    return guild.get_role(role_id)


def get_log_channel(guild: discord.Guild):

    return guild.get_channel(LOG_CHANNEL_ID)


def get_message_log_channel(guild: discord.Guild):

    return guild.get_channel(MESSAGE_LOG_CHANNEL_ID)


def build_image_panel(image_url: str):
    """
    يبني Embed للصورة فقط.
    إذا لم يوجد رابط صورة، نعيد None حتى لا نرسل Embed فارغًا؛
    Discord يرفض الـEmbed الذي لا يحتوي على محتوى صالح.
    """
    image_url = (image_url or "").strip()

    if not image_url:
        return None

    embed = discord.Embed()
    embed.set_image(url=image_url)
    return embed


def is_ticket(channel: discord.TextChannel):

    return (
        channel.topic is not None
        and channel.topic.startswith("ticket_owner:")
    )


def get_ticket_owner_id(channel: discord.TextChannel):

    if not is_ticket(channel):
        return None

    try:

        return int(
            channel.topic.split(":", 1)[1]
        )

    except (ValueError, IndexError):

        return None


def is_support(member: discord.Member):
    support_ids = {SUPPORT_ROLE_ID, ADS_INTRO_ROLE_ID}
    return any(
        role_id and member.guild.get_role(role_id) in member.roles
        for role_id in support_ids
    )


def is_admin(member: discord.Member):

    return (
        member.guild_permissions.administrator
        or is_support(member)
    )


# =========================================================
# Logs
# =========================================================

async def send_log(
    guild: discord.Guild,
    title: str,
    description: str,
    log_type: str = "INFO"
):

    log_channel = get_log_channel(guild)

    if log_channel is None:

        print(
            "⚠️ Log channel not found."
        )

        return

    embed = discord.Embed(
        title=title,
        description=description,
        timestamp=datetime.now()
    )

    embed.set_footer(
        text=f"Jurma Ticket • {log_type}"
    )

    try:

        await log_channel.send(
            embed=embed
        )

    except discord.Forbidden:

        print(
            "❌ لا أستطيع إرسال الرسائل إلى قناة اللوق."
        )

    except discord.HTTPException as e:

        print(
            f"❌ Log error: {e}"
        )


# =========================================================
# Transcript
# =========================================================

async def create_transcript(
    channel: discord.TextChannel
):

    lines = []

    lines.append(
        f"Jurma Ticket Transcript\n"
    )

    lines.append(
        f"Channel: #{channel.name}\n"
    )

    lines.append(
        f"Channel ID: {channel.id}\n"
    )

    lines.append(
        f"Created: {datetime.now()}\n"
    )

    lines.append(
        "=" * 70 + "\n\n"
    )

    try:

        async for message in channel.history(
            limit=None,
            oldest_first=True
        ):

            timestamp = message.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            author = (
                f"{message.author} "
                f"(ID: {message.author.id})"
            )

            content = message.content

            if not content:
                content = "[بدون نص]"

            lines.append(
                f"[{timestamp}] {author}:\n"
            )

            lines.append(
                f"{content}\n"
            )

            # تسجيل المرفقات
            if message.attachments:

                for attachment in message.attachments:

                    lines.append(
                        f"[Attachment] "
                        f"{attachment.url}\n"
                    )

            lines.append("\n")

    except Exception as e:

        lines.append(
            f"\nERROR WHILE READING MESSAGES:\n{e}\n"
        )

    text = "".join(lines)

    return text.encode("utf-8")


# =========================================================
# إغلاق التذكرة
# =========================================================

async def close_ticket(
    channel: discord.TextChannel,
    closed_by: discord.Member
):

    if not is_ticket(channel):

        return False

    owner_id = get_ticket_owner_id(
        channel
    )

    owner = None

    if owner_id:

        owner = channel.guild.get_member(
            owner_id
        )

    # منع صاحب التذكرة من الكتابة
    if owner:

        await channel.set_permissions(
            owner,
            view_channel=True,
            send_messages=False,
            read_message_history=True,
            attach_files=False
        )

    embed = discord.Embed(
        title="🔒 تم إغلاق التذكرة",
        description=(
            f"تم إغلاق التذكرة بواسطة "
            f"{closed_by.mention}.\n\n"
            "يمكن لفريق الإدارة إعادة فتحها "
            "أو حذفها."
        )
    )

    await channel.send(
        embed=embed,
        view=ClosedTicketView()
    )

    await send_log(
        channel.guild,
        "🔒 Ticket Closed",
        (
            f"**التذكرة:** {channel.mention}\n"
            f"**المستخدم:** "
            f"{owner.mention if owner else 'Unknown'}\n"
            f"**بواسطة:** {closed_by.mention}"
        ),
        "CLOSED"
    )

    return True


# =========================================================
# إعادة فتح التذكرة
# =========================================================

async def reopen_ticket(
    channel: discord.TextChannel,
    reopened_by: discord.Member
):

    if not is_ticket(channel):

        return False

    owner_id = get_ticket_owner_id(
        channel
    )

    owner = None

    if owner_id:

        owner = channel.guild.get_member(
            owner_id
        )

    if owner:

        await channel.set_permissions(
            owner,
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True
        )

    embed = discord.Embed(
        title="🔓 تم إعادة فتح التذكرة",
        description=(
            f"تم إعادة فتح التذكرة بواسطة "
            f"{reopened_by.mention}."
        )
    )

    await channel.send(
        embed=embed,
        view=TicketControlView()
    )

    await send_log(
        channel.guild,
        "🔓 Ticket Reopened",
        (
            f"**التذكرة:** {channel.mention}\n"
            f"**المستخدم:** "
            f"{owner.mention if owner else 'Unknown'}\n"
            f"**بواسطة:** {reopened_by.mention}"
        ),
        "REOPENED"
    )

    return True


# =========================================================
# حذف التذكرة
# =========================================================

async def delete_ticket(
    channel: discord.TextChannel,
    deleted_by: discord.Member
):

    if not is_ticket(channel):

        return False

    guild = channel.guild

    owner_id = get_ticket_owner_id(
        channel
    )

    owner = None

    if owner_id:

        owner = guild.get_member(
            owner_id
        )

    # إنشاء Transcript
    transcript_data = await create_transcript(
        channel
    )

    filename = (
        f"{channel.name}-transcript.txt"
    )

    file = discord.File(
        io.BytesIO(transcript_data),
        filename=filename
    )

    # إرسال اللوق قبل حذف القناة
    log_channel = get_log_channel(
        guild
    )

    if log_channel:

        embed = discord.Embed(
            title="🗑️ Ticket Deleted",
            description=(
                f"**التذكرة:** #{channel.name}\n"
                f"**المستخدم:** "
                f"{owner.mention if owner else 'Unknown'}\n"
                f"**بواسطة:** {deleted_by.mention}"
            ),
            timestamp=datetime.now()
        )

        embed.set_footer(
            text="Jurma Ticket • DELETED"
        )

        try:

            await log_channel.send(
                embed=embed,
                file=file
            )

        except discord.HTTPException as e:

            print(
                f"❌ Failed to send transcript: {e}"
            )

    # حذف القناة
    try:

        await channel.delete(
            reason=(
                f"Ticket deleted by "
                f"{deleted_by}"
            )
        )

    except discord.Forbidden:

        print(
            "❌ لا أستطيع حذف التذكرة."
        )

        return False

    except discord.HTTPException as e:

        print(
            f"❌ Delete error: {e}"
        )

        return False

    return True


# =========================================================
# تأكيد إغلاق التذكرة
# =========================================================

class CloseConfirmView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=60
        )

    @discord.ui.button(
        label="نعم، أغلق التذكرة",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="confirm_close_ticket"
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not is_ticket(
            interaction.channel
        ):

            await interaction.response.send_message(
                "❌ هذه ليست تذكرة.",
                ephemeral=True
            )

            return

        if not is_admin(
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ هذا الإجراء للإدارة فقط.",
                ephemeral=True
            )

            return

        await interaction.response.defer()

        success = await close_ticket(
            interaction.channel,
            interaction.user
        )

        if not success:

            await interaction.followup.send(
                "❌ لم أستطع إغلاق التذكرة.",
                ephemeral=True
            )


    @discord.ui.button(
        label="إلغاء",
        emoji="❌",
        style=discord.ButtonStyle.secondary,
        custom_id="cancel_close_ticket"
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.edit_message(
            content="❌ تم إلغاء عملية الإغلاق.",
            embed=None,
            view=None
        )


# =========================================================
# تأكيد حذف التذكرة
# =========================================================

class DeleteConfirmView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=60
        )

    @discord.ui.button(
        label="نعم، احذف التذكرة",
        emoji="🗑️",
        style=discord.ButtonStyle.danger,
        custom_id="confirm_delete_ticket"
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not is_ticket(
            interaction.channel
        ):

            await interaction.response.send_message(
                "❌ هذه ليست تذكرة.",
                ephemeral=True
            )

            return

        if not is_admin(
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ هذا الإجراء للإدارة فقط.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "🗑️ جاري حذف التذكرة وحفظ الـ Transcript...",
            ephemeral=True
        )

        await delete_ticket(
            interaction.channel,
            interaction.user
        )


    @discord.ui.button(
        label="إلغاء",
        emoji="❌",
        style=discord.ButtonStyle.secondary,
        custom_id="cancel_delete_ticket"
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.edit_message(
            content="❌ تم إلغاء عملية الحذف.",
            embed=None,
            view=None
        )


# =========================================================
# أزرار التذكرة المفتوحة
# =========================================================

class TicketControlView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=None
        )

    @discord.ui.button(
        label="إغلاق التذكرة",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="close_ticket_button"
    )
    async def close_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not is_ticket(
            interaction.channel
        ):

            await interaction.response.send_message(
                "❌ هذه ليست تذكرة.",
                ephemeral=True
            )

            return

        if not is_admin(
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ إغلاق التذكرة متاح لفريق الإدارة فقط.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "⚠️ هل أنت متأكد من إغلاق التذكرة؟",
            view=CloseConfirmView(),
            ephemeral=True
        )


# =========================================================
# أزرار التذكرة المغلقة
# =========================================================

class ClosedTicketView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=None
        )

    @discord.ui.button(
        label="إعادة فتح",
        emoji="🔓",
        style=discord.ButtonStyle.success,
        custom_id="reopen_ticket_button"
    )
    async def reopen_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not is_ticket(
            interaction.channel
        ):

            await interaction.response.send_message(
                "❌ هذه ليست تذكرة.",
                ephemeral=True
            )

            return

        if not is_admin(
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ إعادة فتح التذكرة متاحة للإدارة فقط.",
                ephemeral=True
            )

            return

        await interaction.response.defer()

        await reopen_ticket(
            interaction.channel,
            interaction.user
        )


    @discord.ui.button(
        label="حذف التذكرة",
        emoji="🗑️",
        style=discord.ButtonStyle.danger,
        custom_id="delete_ticket_button"
    )
    async def delete_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not is_ticket(
            interaction.channel
        ):

            await interaction.response.send_message(
                "❌ هذه ليست تذكرة.",
                ephemeral=True
            )

            return

        if not is_admin(
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ حذف التذكرة متاح للإدارة فقط.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "⚠️ هل أنت متأكد من حذف التذكرة؟\n\n"
            "سيتم حفظ الـ Transcript في قناة اللوق.",
            view=DeleteConfirmView(),
            ephemeral=True
        )


# =========================================================
# قائمة أنواع التذاكر
# =========================================================

class TicketSelect(discord.ui.Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="ADS",
                description="اعلان・بارتنر",
                emoji="<:Ads:1539547578083835975>",
                value="ADS"
            ),

            discord.SelectOption(
                label="Help",
                description="استفسار ・بلاغ・مشكلة",
                emoji="<:Help:1539547610472259645>",
                value="Help"
            ),

            discord.SelectOption(
                label="Introduction",
                description="تقديم الإدارة",
                emoji="<:writing:1539549832048414852>",
                value="Introduction"
            )

        ]

        super().__init__(
            placeholder="اختر نوع التذكرة",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_type_select"
        )


    async def callback(
        self,
        interaction: discord.Interaction
    ):

        guild = interaction.guild
        user = interaction.user

        if guild is None:

            await interaction.response.send_message(
                "❌ لا يمكن استخدام النظام هنا.",
                ephemeral=True
            )

            return

        # نؤكد الـInteraction فورًا قبل أي عمليات Discord قد تستغرق أكثر من 3 ثوانٍ.
        await interaction.response.defer(ephemeral=True)

        category = get_ticket_category(
            guild
        )

        support_role = get_ticket_support_role(
            guild,
            self.values[0]
        )

        if category is None:

            await interaction.followup.send(
                "❌ لم أجد Category التذاكر.",
                ephemeral=True
            )

            return

        if support_role is None:

            await interaction.followup.send(
                "❌ لم أجد رتبة فريق الدعم.",
                ephemeral=True
            )

            return

        # منع فتح أكثر من تذكرة
        for channel in guild.text_channels:

            if (
                channel.topic
                == f"ticket_owner:{user.id}"
            ):

                await interaction.followup.send(
                    f"❌ لديك تذكرة مفتوحة بالفعل: "
                    f"{channel.mention}",
                    ephemeral=True
                )

                return

        ticket_type = self.values[0]

        # أسماء القنوات
        safe_username = (
            user.name
            .lower()
            .replace(" ", "-")
        )

        channel_name = (
            f"{TICKET_NAME_PREFIX}-"
            f"{ticket_type.lower()}-"
            f"{safe_username}"
        )

        channel_name = channel_name[:100]

        try:

            # =================================================
            # إنشاء القناة
            # =================================================

            channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                topic=f"ticket_owner:{user.id}"
            )


            # =================================================
            # صلاحيات @everyone
            # =================================================

            await channel.set_permissions(
                guild.default_role,
                view_channel=False
            )


            # =================================================
            # صلاحيات صاحب التذكرة
            # =================================================

            await channel.set_permissions(
                user,
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True
            )


            # =================================================
            # صلاحيات فريق الدعم
            # =================================================

            await channel.set_permissions(
                support_role,
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_messages=True
            )


            # =================================================
            # رسالة التذكرة - نص عادي وليست Embed
            # =================================================

            if ticket_type == "ADS":
                opening_message = (
                    f"**مرحبا {user.mention}\n"
                    f"راح يتواصلون معك <@&{ADS_INTRO_ROLE_ID}> باسرع وقت ممكن**"
                )
                opening_view = ADSOptionsView()

            elif ticket_type == "Help":
                opening_message = (
                    f"**مرحبا {user.mention}\n"
                    f"راح يتواصلون معك <@&{SUPPORT_ROLE_ID}> باسرع وقت ممكن\n"
                    "نتمنى منك تزودينا بالمعلومات الخاصة باستفسارك او المشكلة او البلاغ**"
                )
                opening_view = TicketControlView()

            else:
                opening_message = (
                    f"**مرحبا {user.mention}\n"
                    f"راح يتواصلون معك <@&{ADS_INTRO_ROLE_ID}> باسرع وقت ممكن\n\n"
                    "نتمنى منك تزودنا بالتفاصيل التالية:\n"
                    "` اسمك: `\n"
                    "` عمرك: `\n"
                    "` تقدر تفتح مايك؟: `\n"
                    "` هل كنت اداري بسيرفر من قبل؟: `\n"
                    "` كم المدة الي تقدر تتفاعل فيها بالسيرفر؟ `**"
                )
                opening_view = TicketControlView()

            await channel.send(
                content=opening_message,
                view=opening_view
            )


            # =================================================
            # Log فتح التذكرة
            # =================================================

            await send_log(
                guild,
                "🎫 Ticket Created",
                (
                    f"**التذكرة:** {channel.mention}\n"
                    f"**المستخدم:** {user.mention}\n"
                    f"**النوع:** {ticket_type}\n"
                    f"**Channel ID:** `{channel.id}`"
                ),
                "CREATED"
            )


            # =================================================
            # الرد للمستخدم
            # =================================================

            await interaction.followup.send(
                f"✅ تم إنشاء تذكرتك: "
                f"{channel.mention}",
                ephemeral=True
            )

            print(
                f"🎫 Ticket created: "
                f"{channel.name}"
            )


        except discord.Forbidden as e:

            print(
                "❌ Missing Permissions:"
            )

            print(e)

            await interaction.followup.send(
                "❌ البوت لا يملك الصلاحيات الكافية "
                "لإنشاء التذكرة.",
                ephemeral=True
            )


        except discord.HTTPException as e:

            print(
                f"❌ Discord HTTP Error: {e}"
            )

            await interaction.followup.send(
                "❌ حدث خطأ من Discord.",
                ephemeral=True
            )


        except Exception as e:

            print(
                f"❌ Unexpected Error: {e}"
            )

            await interaction.followup.send(
                "❌ حدث خطأ غير متوقع.",
                ephemeral=True
            )


# =========================================================
# خيارات ADS داخل التذكرة
# =========================================================

class ADSPartnerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="بارتنر",
            style=discord.ButtonStyle.secondary,
            custom_id="ads_partner_button"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "نتمنى منك تزودنا بالمعلومات التالية\n"
            "` حساب الاونر: `\n"
            "` رابط السيرفر: `\n"
            "` عدد الاعضاء: `\n"
            "` سبب اختيار سيرفرنا بارتنر: `"
        )


class ADSAdvertButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="اعلان",
            style=discord.ButtonStyle.secondary,
            custom_id="ads_advert_button"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "` الاعلان راح يكلف 25:qs_riyal:   `\n"
            "` الاعلان 3 ايام `\n"
            "في حال حبيت تكمل نحتاج هاذي التفاصيل\n"
            "- ` نوع الاعلان `\n"
            "- ` الرسالة النصية الي حاب ترسلها او التصميم `"
        )


class ADSCloseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="إغلاق التذكرة", emoji="🔒", style=discord.ButtonStyle.danger, custom_id="ads_close_ticket_button")

    async def callback(self, interaction: discord.Interaction):
        if not is_admin(interaction.user):
            await interaction.response.send_message("❌ ليس لديك صلاحية إغلاق التذكرة.", ephemeral=True)
            return
        await interaction.response.send_message("⚠️ هل أنت متأكد من إغلاق التذكرة؟", view=CloseConfirmView(), ephemeral=True)


class ADSOptionsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ADSPartnerButton())
        self.add_item(ADSAdvertButton())
        self.add_item(ADSCloseButton())


# =========================================================
# لوحة التذاكر الرئيسية
# =========================================================

class TicketView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=None
        )

        self.add_item(
            TicketSelect()
        )


# =========================================================
# /setup-ticket
# =========================================================

@bot.tree.command(
    name="setup-ticket",
    description="إرسال لوحة نظام التذاكر"
)
async def setup_ticket(
    interaction: discord.Interaction
):

    # الأمر للإدارة فقط
    if not is_admin(
        interaction.user
    ):

        await interaction.response.send_message(
            "❌ هذا الأمر للإدارة فقط.",
            ephemeral=True
        )

        return


    # نؤكد الـInteraction فورًا قبل أي عمليات Discord.
    await interaction.response.defer(ephemeral=True)

    # الصورة فقط؛ لا يوجد أي نص فوق قائمة التذاكر.
    # إذا لم توجد صورة، لا ننشئ Embed أصلًا.
    # Discord يرفض أي Embed فارغ.
    image_url = (TICKET_PANEL_IMAGE_URL or "").strip()
    if image_url:
        embed = build_image_panel(image_url)
        if embed is not None:
            await interaction.channel.send(embed=embed, view=TicketView())
        else:
            await interaction.channel.send(content="\u200b", view=TicketView())
    else:
        await interaction.channel.send(content="\u200b", view=TicketView())


    await interaction.followup.send(
        "✅ تم إرسال لوحة التذاكر.",
        ephemeral=True
    )


# =========================================================
# /close-ticket
# =========================================================

@bot.tree.command(
    name="close-ticket",
    description="إغلاق التذكرة الحالية"
)
async def close_ticket_command(
    interaction: discord.Interaction
):

    if not is_ticket(
        interaction.channel
    ):

        await interaction.response.send_message(
            "❌ هذا الأمر يعمل داخل التذاكر فقط.",
            ephemeral=True
        )

        return

    if not is_admin(
        interaction.user
    ):

        await interaction.response.send_message(
            "❌ هذا الأمر للإدارة فقط.",
            ephemeral=True
        )

        return

    await interaction.response.send_message(
        "⚠️ هل أنت متأكد من إغلاق التذكرة؟",
        view=CloseConfirmView(),
        ephemeral=True
    )


# =========================================================
# /reopen-ticket
# =========================================================

@bot.tree.command(
    name="reopen-ticket",
    description="إعادة فتح التذكرة الحالية"
)
async def reopen_ticket_command(
    interaction: discord.Interaction
):

    if not is_ticket(
        interaction.channel
    ):

        await interaction.response.send_message(
            "❌ هذا الأمر يعمل داخل التذاكر فقط.",
            ephemeral=True
        )

        return

    if not is_admin(
        interaction.user
    ):

        await interaction.response.send_message(
            "❌ هذا الأمر للإدارة فقط.",
            ephemeral=True
        )

        return

    await interaction.response.defer(
        ephemeral=True
    )

    await reopen_ticket(
        interaction.channel,
        interaction.user
    )

    await interaction.followup.send(
        "🔓 تم إعادة فتح التذكرة.",
        ephemeral=True
    )


# =========================================================
# /delete-ticket
# =========================================================

@bot.tree.command(
    name="delete-ticket",
    description="حذف التذكرة الحالية"
)
async def delete_ticket_command(
    interaction: discord.Interaction
):

    if not is_ticket(
        interaction.channel
    ):

        await interaction.response.send_message(
            "❌ هذا الأمر يعمل داخل التذاكر فقط.",
            ephemeral=True
        )

        return

    if not is_admin(
        interaction.user
    ):

        await interaction.response.send_message(
            "❌ هذا الأمر للإدارة فقط.",
            ephemeral=True
        )

        return

    await interaction.response.send_message(
        "⚠️ **تأكيد حذف التذكرة**\n\n"
        "سيتم إنشاء Transcript وإرساله إلى قناة اللوق "
        "ثم حذف التذكرة نهائياً.",
        view=DeleteConfirmView(),
        ephemeral=True
    )



# =========================================================
# Player Search - البحث عن اللاعبين
# =========================================================

class PlayerGameSelect(discord.ui.Select):

    def __init__(self):
        options = []

        for key, game in GAME_OPTIONS.items():
            # لا نعرض الخانات غير المجهزة.
            if game["role_id"] == 0 or game["voice_id"] is None:
                continue

            options.append(
                discord.SelectOption(
                    label=game["name"],
                    value=key,
                    emoji=game["emoji"]
                )
            )

        super().__init__(
            placeholder="اختر اللعبة التي تبحث عن لاعبين لها",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="player_game_select"
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ لا يمكن استخدام النظام هنا.",
                ephemeral=True
            )
            return

        if not isinstance(user, discord.Member) or user.voice is None:
            await interaction.response.send_message(
                "❌ يجب أن تكون داخل غرفة صوتية قبل اختيار اللعبة.",
                ephemeral=True
            )
            return

        game = GAME_OPTIONS[self.values[0]]
        voice_channel = user.voice.channel

        # إذا تم تحديد غرفة خاصة باللعبة، يجب أن يكون العضو داخلها.
        configured_voice = guild.get_channel(game["voice_id"])
        if configured_voice is not None and voice_channel.id != configured_voice.id:
            await interaction.response.send_message(
                f"❌ يجب أن تكون داخل غرفة {configured_voice.mention} لاختيار {game['name']}.",
                ephemeral=True
            )
            return

        role = guild.get_role(game["role_id"])
        if role is None:
            await interaction.response.send_message(
                "❌ رتبة اللعبة غير موجودة.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        sent = 0
        failed = 0

        # إرسال DM لكل شخص لديه رتبة اللعبة، باستثناء الباحث نفسه.
        for member in role.members:
            if member.bot or member.id == user.id:
                continue

            message = (
                f"{user.mention} ينتظرك في {voice_channel.mention}\n"
                f"من اجل لعب {game['name']}"
            )

            try:
                await member.send(message)
                sent += 1
            except (discord.Forbidden, discord.HTTPException):
                failed += 1

        # إرسال تأكيد في الشات.
        await interaction.followup.send(
            f"✅ تم إرسال طلب البحث عن لاعبين للعبة **{game['name']}**.\n"
            f"🔊 الغرفة: {voice_channel.mention}\n"
            f"📨 تم إرسال الرسالة إلى **{sent}** شخص."
            + (f"\n⚠️ تعذر إرسالها إلى **{failed}** شخص بسبب الخاص." if failed else ""),
            ephemeral=True
        )


class PlayerSearchView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PlayerGameSelect())


@bot.tree.command(
    name="setup-players",
    description="إرسال لوحة البحث عن اللاعبين"
)
async def setup_players(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)

    if not is_admin(interaction.user):
        await interaction.followup.send(
            "❌ هذا الأمر للإدارة فقط.",
            ephemeral=True
        )
        return

    if PLAYER_SEARCH_CHANNEL_ID and interaction.channel.id != PLAYER_SEARCH_CHANNEL_ID:
        await interaction.followup.send(
            "❌ استخدم الأمر داخل شات البحث عن اللاعبين المحدد.",
            ephemeral=True
        )
        return

    # الصورة فقط؛ لا يوجد أي نص فوق قائمة الألعاب.
    # إذا لم توجد صورة، لا ننشئ Embed أصلًا.
    # Discord يرفض أي Embed فارغ.
    image_url = (PLAYER_SEARCH_PANEL_IMAGE_URL or "").strip()
    if image_url:
        embed = build_image_panel(image_url)
        if embed is not None:
            await interaction.channel.send(embed=embed, view=PlayerSearchView())
        else:
            await interaction.channel.send(content="\u200b", view=PlayerSearchView())
    else:
        await interaction.channel.send(content="\u200b", view=PlayerSearchView())

    await interaction.followup.send(
        "✅ تم إرسال لوحة البحث عن اللاعبين.",
        ephemeral=True
    )


# =========================================================
# =========================================================
# Color System - نظام الألوان
# =========================================================

class ColorSelect(discord.ui.Select):
    def __init__(self):
        options = []
        for number in range(1, 11):
            role_id = COLOR_ROLE_IDS.get(number, 0)
            if not role_id:
                continue
            options.append(discord.SelectOption(
                label=str(number),
                value=str(number),
                emoji=COLOR_EMOJIS.get(number)
            ))
        super().__init__(
            placeholder="اختر لونك",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="color_role_select"
        )

    async def callback(self, interaction: discord.Interaction):
        # Acknowledge immediately so Discord does not expire the interaction (10062).
        try:
            await interaction.response.defer(ephemeral=True, thinking=True)
        except discord.NotFound:
            return
        except discord.InteractionResponded:
            pass

        if interaction.guild is None or not isinstance(interaction.user, discord.Member):
            await interaction.followup.send("❌ لا يمكن استخدام نظام الألوان هنا.", ephemeral=True)
            return

        number = int(self.values[0])
        role_id = COLOR_ROLE_IDS.get(number, 0)
        role = interaction.guild.get_role(role_id) if role_id else None
        if role is None:
            await interaction.followup.send(f"❌ اللون رقم **{number}** غير مُعد حاليًا.", ephemeral=True)
            return

        old_roles = []
        for rid in COLOR_ROLE_IDS.values():
            if rid:
                old = interaction.guild.get_role(rid)
                if old and old in interaction.user.roles and old != role:
                    old_roles.append(old)

        try:
            if old_roles:
                await interaction.user.remove_roles(*old_roles, reason="تغيير لون العضو")
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role, reason=f"اختيار اللون {number}")
            await interaction.followup.send(f"🎨 تم اختيار {role.mention} بنجاح.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ لا أستطيع إعطاء هذه الرتبة. تأكد أن رتبة البوت أعلى من رتب الألوان.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.followup.send(f"❌ حدث خطأ أثناء تغيير اللون: {e}", ephemeral=True)

class ColorView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ColorSelect())


@bot.command(name="colors")
@commands.guild_only()
async def colors_command(ctx):
    await ctx.send(
        content="\u200b",
        view=ColorView()
    )


@bot.command(name="color")
@commands.guild_only()
async def color_command(ctx, number: int):
    # الإبقاء على الأمر القديم كاختصار مباشر.
    if number < 1 or number > 10:
        await ctx.send("❌ اختر رقمًا من 1 إلى 10.")
        return

    role_id = COLOR_ROLE_IDS.get(number, 0)
    role = ctx.guild.get_role(role_id) if role_id else None

    if role is None:
        await ctx.send(f"❌ اللون رقم **{number}** غير مُعد حاليًا.")
        return

    old_roles = []
    for rid in COLOR_ROLE_IDS.values():
        if rid:
            old = ctx.guild.get_role(rid)
            if old and old in ctx.author.roles:
                old_roles.append(old)

    try:
        if old_roles:
            await ctx.author.remove_roles(*old_roles, reason="تغيير لون العضو")

        await ctx.author.add_roles(role, reason=f"اختيار اللون {number}")
        await ctx.send(
            f"🎨 {ctx.author.mention} تم اختيار {role.mention} بنجاح."
        )

    except discord.Forbidden:
        await ctx.send(
            "❌ لا أستطيع إعطاء هذه الرتبة. تأكد أن رتبة البوت أعلى من رتب الألوان."
        )


# =========================================================
# Slash System / Moderation Commands
# =========================================================

async def _slash_admin(interaction: discord.Interaction) -> bool:
    if not isinstance(interaction.user, discord.Member) or not is_admin(interaction.user):
        await interaction.response.send_message("❌ هذا الأمر للإدارة فقط.", ephemeral=True)
        return False
    return True

@bot.tree.command(name="ban", description="حظر عضو")
async def slash_ban(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون سبب"):
    if not await _slash_admin(interaction): return
    await interaction.response.defer(ephemeral=True)
    try:
        await member.ban(reason=reason)
        await interaction.followup.send(f"✅ تم حظر {member.mention}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ لا أستطيع حظر هذا العضو.", ephemeral=True)
    except discord.HTTPException:
        await interaction.followup.send("❌ حدث خطأ من Discord أثناء الحظر.", ephemeral=True)

@bot.tree.command(name="kick", description="طرد عضو")
async def slash_kick(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون سبب"):
    if not await _slash_admin(interaction): return
    await interaction.response.defer(ephemeral=True)
    try:
        await member.kick(reason=reason)
        await interaction.followup.send(f"✅ تم طرد {member.mention}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ لا أستطيع طرد هذا العضو.", ephemeral=True)
    except discord.HTTPException:
        await interaction.followup.send("❌ حدث خطأ من Discord أثناء الطرد.", ephemeral=True)

@bot.tree.command(name="mute", description="كتم عضو لمدة محددة")
async def slash_mute(interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "بدون سبب"):
    if not await _slash_admin(interaction): return
    delta=parse_duration(duration)
    if delta is None:
        await interaction.response.send_message("❌ المدة غير صحيحة. استخدم `10m` أو `2h` أو `1d`، والحد الأقصى 28 يومًا.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    try:
        await member.timeout(discord.utils.utcnow()+delta, reason=reason)
        await interaction.followup.send(f"✅ تم كتم {member.mention} لمدة `{duration}`.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ لا أستطيع كتم هذا العضو.", ephemeral=True)
    except discord.HTTPException:
        await interaction.followup.send("❌ حدث خطأ من Discord أثناء الكتم.", ephemeral=True)

@bot.tree.command(name="unmute", description="فك كتم عضو")
async def slash_unmute(interaction: discord.Interaction, member: discord.Member):
    if not await _slash_admin(interaction): return
    await interaction.response.defer(ephemeral=True)
    try:
        await member.timeout(None, reason=f"Unmute by {interaction.user}")
        await interaction.followup.send(f"✅ تم فك كتم {member.mention}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ لا أستطيع فك كتم هذا العضو.", ephemeral=True)

@bot.tree.command(name="lock", description="قفل الشات الحالي")
async def slash_lock(interaction: discord.Interaction):
    if not await _slash_admin(interaction): return
    await interaction.response.defer(ephemeral=True)
    channel=interaction.channel
    if not isinstance(channel, discord.TextChannel):
        await interaction.followup.send("❌ هذا الأمر للقنوات النصية فقط.", ephemeral=True); return
    ow=channel.overwrites_for(interaction.guild.default_role)
    ow.send_messages=False
    await channel.set_permissions(interaction.guild.default_role, overwrite=ow, reason=f"Lock by {interaction.user}")
    await interaction.followup.send("🔒 تم قفل الشات.", ephemeral=True)

@bot.tree.command(name="unlock", description="فتح الشات الحالي")
async def slash_unlock(interaction: discord.Interaction):
    if not await _slash_admin(interaction): return
    await interaction.response.defer(ephemeral=True)
    channel=interaction.channel
    if not isinstance(channel, discord.TextChannel):
        await interaction.followup.send("❌ هذا الأمر للقنوات النصية فقط.", ephemeral=True); return
    ow=channel.overwrites_for(interaction.guild.default_role)
    ow.send_messages=None
    await channel.set_permissions(interaction.guild.default_role, overwrite=ow, reason=f"Unlock by {interaction.user}")
    await interaction.followup.send("🔓 تم فتح الشات.", ephemeral=True)

@bot.tree.command(name="clear", description="مسح من 1 إلى 100 رسالة")
async def slash_clear(interaction: discord.Interaction, amount: int):
    if not await _slash_admin(interaction): return
    if amount<1 or amount>100:
        await interaction.response.send_message("❌ اختر رقمًا من 1 إلى 100.", ephemeral=True); return
    await interaction.response.defer(ephemeral=True)
    channel=interaction.channel
    if not isinstance(channel, discord.TextChannel):
        await interaction.followup.send("❌ هذا الأمر للقنوات النصية فقط.", ephemeral=True); return
    deleted=await channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 تم مسح {len(deleted)} رسالة.", ephemeral=True)

@bot.tree.command(name="addrole", description="إضافة رول لعضو")
async def slash_addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not await _slash_admin(interaction): return
    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ لا أستطيع إعطاء رتبة مساوية أو أعلى من أعلى رتبة لدي.", ephemeral=True); return
    await interaction.response.defer(ephemeral=True)
    try:
        await member.add_roles(role, reason=f"Role added by {interaction.user}")
        await interaction.followup.send(f"✅ تمت إضافة {role.mention} إلى {member.mention}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ لا أستطيع إضافة هذه الرتبة. تأكد أن رتبة البوت أعلى منها.", ephemeral=True)


# =========================================================
# /setup-colors
# =========================================================

@bot.tree.command(name="setup-colors", description="إرسال لوحة اختيار الألوان")
async def setup_colors(interaction: discord.Interaction):
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ هذا الأمر للإدارة فقط.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    image_url = (COLOR_PANEL_IMAGE_URL or "").strip()
    if image_url:
        embed = build_image_panel(image_url)
        if embed is not None:
            await interaction.channel.send(embed=embed, view=ColorView())
        else:
            await interaction.channel.send(content="\u200b", view=ColorView())
    else:
        await interaction.channel.send(content="\u200b", view=ColorView())

    await interaction.followup.send("✅ تم إرسال لوحة الألوان.", ephemeral=True)


# =========================================================
# System / Moderation Commands
# =========================================================
# =========================================================

def parse_duration(text):
    match = re.fullmatch(r"(\d+)(s|m|h|d|w)", text.lower().strip())
    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2)
    multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    seconds = amount * multiplier[unit]

    if seconds <= 0 or seconds > 28 * 86400:
        return None

    return timedelta(seconds=seconds)


def format_duration(duration):
    seconds = int(duration.total_seconds())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []
    if days:
        parts.append(f"{days} يوم")
    if hours:
        parts.append(f"{hours} ساعة")
    if minutes:
        parts.append(f"{minutes} دقيقة")
    if seconds and not parts:
        parts.append(f"{seconds} ثانية")
    return " و ".join(parts) or "0 ثانية"


@bot.command(name="ban")
@commands.guild_only()
async def ban_command(ctx, member: discord.Member, *, reason="بدون سبب"):
    if not ctx.author.guild_permissions.ban_members and not is_support(ctx.author):
        await ctx.send("❌ لا تملك صلاحية الباند.")
        return
    if member == ctx.guild.owner or (member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner):
        await ctx.send("❌ لا يمكنك تبنيد هذا العضو بسبب ترتيب الرتب.")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("❌ رتبة البوت يجب أن تكون أعلى من رتبة العضو.")
        return

    try:
        await member.ban(reason=f"{reason} | بواسطة {ctx.author}")
        await ctx.send(f"🔨 تم تبنيد {member.mention}\n**السبب:** {reason}")
    except discord.Forbidden:
        await ctx.send("❌ البوت لا يملك صلاحية الباند لهذا العضو.")


@bot.command(name="kick")
@commands.guild_only()
async def kick_command(ctx, member: discord.Member, *, reason="بدون سبب"):
    if not ctx.author.guild_permissions.kick_members and not is_support(ctx.author):
        await ctx.send("❌ لا تملك صلاحية الكيك.")
        return
    if member == ctx.guild.owner or (member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner):
        await ctx.send("❌ لا يمكنك طرد هذا العضو بسبب ترتيب الرتب.")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("❌ رتبة البوت يجب أن تكون أعلى من رتبة العضو.")
        return

    try:
        await member.kick(reason=f"{reason} | بواسطة {ctx.author}")
        await ctx.send(f"👢 تم طرد {member.mention}\n**السبب:** {reason}")
    except discord.Forbidden:
        await ctx.send("❌ البوت لا يملك صلاحية الكيك لهذا العضو.")


@bot.command(name="mute", aliases=["timeout"])
@commands.guild_only()
async def mute_command(ctx, member: discord.Member, duration_text: str, *, reason="بدون سبب"):
    if not ctx.author.guild_permissions.moderate_members and not is_support(ctx.author):
        await ctx.send("❌ لا تملك صلاحية الميوت.")
        return

    duration = parse_duration(duration_text)
    if duration is None:
        await ctx.send("❌ استخدم مثلًا `#mute @user 10m` أو `#mute @user 2h` (الحد 28 يومًا).")
        return

    if member == ctx.guild.owner or (member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner):
        await ctx.send("❌ لا يمكنك عمل ميوت لهذا العضو بسبب ترتيب الرتب.")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("❌ رتبة البوت يجب أن تكون أعلى من رتبة العضو.")
        return

    try:
        await member.timeout(duration, reason=f"{reason} | بواسطة {ctx.author}")
        await ctx.send(
            f"🔇 تم ميوت {member.mention}\n"
            f"**المدة:** {format_duration(duration)}\n**السبب:** {reason}"
        )
    except discord.Forbidden:
        await ctx.send("❌ البوت لا يملك صلاحية الميوت لهذا العضو.")


@bot.command(name="unmute", aliases=["untimeout"])
@commands.guild_only()
async def unmute_command(ctx, member: discord.Member, *, reason="إزالة الميوت"):
    if not ctx.author.guild_permissions.moderate_members and not is_support(ctx.author):
        await ctx.send("❌ لا تملك صلاحية إزالة الميوت.")
        return
    try:
        await member.timeout(None, reason=f"{reason} | بواسطة {ctx.author}")
        await ctx.send(f"🔊 تم إزالة الميوت عن {member.mention}.")
    except discord.Forbidden:
        await ctx.send("❌ البوت لا يملك صلاحية إزالة الميوت.")


@bot.command(name="clear", aliases=["purge"])
@commands.guild_only()
async def clear_command(ctx, amount: int):
    if not ctx.author.guild_permissions.manage_messages and not is_support(ctx.author):
        await ctx.send("❌ لا تملك صلاحية حذف الرسائل.")
        return
    if amount < 1 or amount > 100:
        await ctx.send("❌ اختر رقمًا بين 1 و100.")
        return
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        confirmation = await ctx.send(f"🧹 تم حذف **{len(deleted) - 1}** رسالة.")
        await confirmation.delete(delay=5)
    except discord.Forbidden:
        await ctx.send("❌ البوت لا يملك صلاحية حذف الرسائل.")


@bot.command(name="lock")
@commands.guild_only()
async def lock_command(ctx):
    if not is_admin(ctx.author):
        await ctx.send("❌ هذا الأمر للإدارة فقط.")
        return
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔒 تم قفل الشات.")
    except discord.Forbidden:
        await ctx.send("❌ لا أستطيع تعديل صلاحيات هذه القناة.")


@bot.command(name="unlock")
@commands.guild_only()
async def unlock_command(ctx):
    if not is_admin(ctx.author):
        await ctx.send("❌ هذا الأمر للإدارة فقط.")
        return
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = None
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔓 تم فتح الشات.")
    except discord.Forbidden:
        await ctx.send("❌ لا أستطيع تعديل صلاحيات هذه القناة.")


@bot.command(name="slowmode")
@commands.guild_only()
async def slowmode_command(ctx, seconds: int):
    if not is_admin(ctx.author):
        await ctx.send("❌ هذا الأمر للإدارة فقط.")
        return
    if seconds < 0 or seconds > 21600:
        await ctx.send("❌ اختر مدة بين 0 و21600 ثانية.")
        return
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send("🚀 تم إيقاف الـSlowmode." if seconds == 0 else f"🐢 تم ضبط الـSlowmode على **{seconds} ثانية**.")
    except discord.Forbidden:
        await ctx.send("❌ لا أستطيع تعديل القناة.")


@bot.command(name="help")
@commands.guild_only()
async def help_command(ctx):
    await ctx.send(
        "**🛡️ System**\n"
        "`!ban @user [سبب]`\n"
        "`!kick @user [سبب]`\n"
        "`!mute @user 10m [سبب]`\n"
        "`!unmute @user`\n"
        "`!clear 50`\n"
        "`!lock` / `!unlock`\n"
        "`!slowmode 10`\n\n"
        "**🎨 Colors**\n"
        "`!colors`\n"
        "`!color 1`\n\n"
        "**🎫 Tickets**\n"
        "`/setup-ticket`\n"
        "`/close-ticket`\n"
        "`/reopen-ticket`\n"
        "`/delete-ticket`\n\n"
        "**🎮 Players**\n"
        "`/setup-players`"
    )



@bot.command(name="addrole")
@commands.guild_only()
async def addrole_command(ctx, member: discord.Member, role: discord.Role):
    if not is_admin(ctx.author):
        await ctx.send("❌ هذا الأمر للإدارة فقط.")
        return

    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ لا أستطيع إعطاء رتبة مساوية أو أعلى من أعلى رتبة لدي.")
        return

    if role in member.roles:
        await ctx.send(f"ℹ️ {member.mention} لديه هذه الرتبة بالفعل.")
        return

    try:
        await member.add_roles(
            role,
            reason=f"إضافة رتبة بواسطة {ctx.author}"
        )
        await ctx.send(
            f"✅ تم إعطاء {role.mention} إلى {member.mention}."
        )
    except discord.Forbidden:
        await ctx.send(
            "❌ لا أستطيع إعطاء هذه الرتبة. تأكد من ترتيب الرتب وصلاحيات البوت."
        )


# =========================================================
# Message Logs - لوق الرسائل فقط
# =========================================================

async def send_message_log(guild, title, description):
    channel = get_message_log_channel(guild)
    if channel is None:
        return

    embed = discord.Embed(
        title=title,
        description=description,
        timestamp=datetime.now()
    )

    try:
        await channel.send(embed=embed)
    except (discord.Forbidden, discord.HTTPException) as e:
        print(f"❌ Message log error: {e}")


@bot.event
async def on_message_delete(message):
    if message.guild is None or message.author.bot:
        return

    content = message.content or "[بدون نص]"
    if len(content) > 1500:
        content = content[:1500] + "..."

    attachments = "\n".join(a.url for a in message.attachments)
    if attachments:
        content += f"\n\n**المرفقات:**\n{attachments}"

    await send_message_log(
        message.guild,
        "🗑️ Message Deleted",
        (
            f"**العضو:** {message.author.mention} (`{message.author.id}`)\n"
            f"**القناة:** {message.channel.mention}\n\n"
            f"**المحتوى:**\n{content}"
        )
    )


@bot.event
async def on_message_edit(before, after):
    if before.guild is None or before.author.bot:
        return
    if before.content == after.content:
        return

    old = before.content or "[بدون نص]"
    new = after.content or "[بدون نص]"

    if len(old) > 1000:
        old = old[:1000] + "..."
    if len(new) > 1000:
        new = new[:1000] + "..."

    await send_message_log(
        before.guild,
        "✏️ Message Edited",
        (
            f"**العضو:** {before.author.mention} (`{before.author.id}`)\n"
            f"**القناة:** {before.channel.mention}\n\n"
            f"**قبل:**\n{old}\n\n"
            f"**بعد:**\n{new}"
        )
    )


# =========================================================
# عند تشغيل البوت
# =========================================================

@bot.event
async def on_member_join(member: discord.Member):
    """إعطاء الرتبة الأساسية تلقائيًا لكل عضو جديد."""
    role = member.guild.get_role(AUTO_ROLE_ID)

    if role is None:
        print(
            f"⚠️ لم أجد رتبة الدخول التلقائي "
            f"({AUTO_ROLE_ID}) في السيرفر {member.guild.name}."
        )
        return

    try:
        await member.add_roles(
            role,
            reason="Automatic role for new member",
        )

        print(
            f"👤 {member} حصل تلقائيًا على رتبة {role.name}"
        )

    except discord.Forbidden:
        print(
            "❌ لا يستطيع البوت إعطاء رتبة العضو الجديد. "
            "تأكد أن رتبة البوت أعلى من رتبة الدخول التلقائي."
        )
    except discord.HTTPException as e:
        print(f"❌ فشل إعطاء رتبة العضو الجديد: {e}")


@bot.event
async def on_ready():

    print("=" * 60)
    print(
        f"Logged in as {bot.user}"
    )
    print("Bot is ready!")
    print("=" * 60)


# =========================================================
# تشغيل البوت
# =========================================================

if __name__ == "__main__":
    start_web_server()
    bot.run(TOKEN)

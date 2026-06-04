import logging
import os
import json
import random
import time
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ------------------ কনফিগারেশন ------------------
BOT_TOKEN = "8617390261:AAGKQRZj6Ga-dn5lZ4zhz6Y2OG7L83JD62M"
ADMIN_IDS = [8453335560]
CHANNELS = [
    {"chat_id": -1002711432749, "username": "black_999_gaming", "link": "https://t.me/black_999_gaming"},
    {"chat_id": -1003822346481, "username": "fibsms", "link": "https://t.me/fibsms"}
]
OTP_GROUP_LINK = "https://t.me/fibsms"
SUPPORT_LINK = "https://t.me/fib_helpe"
# -------------------------------------------------

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FOLDER = "numbers_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

COUNTRIES_FILE = "countries.json"
USERS_FILE = "users.json"
TAKEN_NUMBERS_FILE = "taken_numbers.json"
SETTINGS_FILE = "settings.json"
TRAFFIC_FILE = "traffic_timestamps.json"

# ------------------ সম্পূর্ণ বিশ্বের দেশের পতাকা ------------------
FLAGS = {
    "Afghanistan": "🇦🇫", "Albania": "🇦🇱", "Algeria": "🇩🇿", "Andorra": "🇦🇩", "Angola": "🇦🇴",
    "Antigua and Barbuda": "🇦🇬", "Argentina": "🇦🇷", "Armenia": "🇦🇲", "Australia": "🇦🇺",
    "Austria": "🇦🇹", "Azerbaijan": "🇦🇿", "Bahamas": "🇧🇸", "Bahrain": "🇧🇭", "Bangladesh": "🇧🇩",
    "Barbados": "🇧🇧", "Belarus": "🇧🇾", "Belgium": "🇧🇪", "Belize": "🇧🇿", "Benin": "🇧🇯",
    "Bhutan": "🇧🇹", "Bolivia": "🇧🇴", "Bosnia and Herzegovina": "🇧🇦", "Botswana": "🇧🇼",
    "Brazil": "🇧🇷", "Brunei": "🇧🇳", "Bulgaria": "🇧🇬", "Burkina Faso": "🇧🇫", "Burundi": "🇧🇮",
    "Cabo Verde": "🇨🇻", "Cambodia": "🇰🇭", "Cameroon": "🇨🇲", "Canada": "🇨🇦",
    "Central African Republic": "🇨🇫", "Chad": "🇹🇩", "Chile": "🇨🇱", "China": "🇨🇳",
    "Colombia": "🇨🇴", "Comoros": "🇰🇲", "Congo": "🇨🇬", "Costa Rica": "🇨🇷", "Croatia": "🇭🇷",
    "Cuba": "🇨🇺", "Cyprus": "🇨🇾", "Czechia": "🇨🇿", "Denmark": "🇩🇰", "Djibouti": "🇩🇯",
    "Dominica": "🇩🇲", "Dominican Republic": "🇩🇴", "Ecuador": "🇪🇨", "Egypt": "🇪🇬",
    "El Salvador": "🇸🇻", "Equatorial Guinea": "🇬🇶", "Eritrea": "🇪🇷", "Estonia": "🇪🇪",
    "Eswatini": "🇸🇿", "Ethiopia": "🇪🇹", "Fiji": "🇫🇯", "Finland": "🇫🇮", "France": "🇫🇷",
    "Gabon": "🇬🇦", "Gambia": "🇬🇲", "Georgia": "🇬🇪", "Germany": "🇩🇪", "Ghana": "🇬🇭",
    "Greece": "🇬🇷", "Grenada": "🇬🇩", "Guatemala": "🇬🇹", "Guinea": "🇬🇳", "Guinea-Bissau": "🇬🇼",
    "Guyana": "🇬🇾", "Haiti": "🇭🇹", "Honduras": "🇭🇳", "Hungary": "🇭🇺", "Iceland": "🇮🇸",
    "India": "🇮🇳", "Indonesia": "🇮🇩", "Iran": "🇮🇷", "Iraq": "🇮🇶", "Ireland": "🇮🇪",
    "Israel": "🇮🇱", "Italy": "🇮🇹", "Ivory Coast": "🇨🇮", "Jamaica": "🇯🇲", "Japan": "🇯🇵",
    "Jordan": "🇯🇴", "Kazakhstan": "🇰🇿", "Kenya": "🇰🇪", "Kiribati": "🇰🇮", "Korea North": "🇰🇵",
    "Korea South": "🇰🇷", "Kosovo": "🇽🇰", "Kuwait": "🇰🇼", "Kyrgyzstan": "🇰🇬", "Laos": "🇱🇦",
    "Latvia": "🇱🇻", "Lebanon": "🇱🇧", "Lesotho": "🇱🇸", "Liberia": "🇱🇷", "Libya": "🇱🇾",
    "Liechtenstein": "🇱🇮", "Lithuania": "🇱🇹", "Luxembourg": "🇱🇺", "Madagascar": "🇲🇬",
    "Malawi": "🇲🇼", "Malaysia": "🇲🇾", "Maldives": "🇲🇻", "Mali": "🇲🇱", "Malta": "🇲🇹",
    "Marshall Islands": "🇲🇭", "Mauritania": "🇲🇷", "Mauritius": "🇲🇺", "Mexico": "🇲🇽",
    "Micronesia": "🇫🇲", "Moldova": "🇲🇩", "Monaco": "🇲🇨", "Mongolia": "🇲🇳", "Montenegro": "🇲🇪",
    "Morocco": "🇲🇦", "Mozambique": "🇲🇿", "Myanmar": "🇲🇲", "Namibia": "🇳🇦", "Nauru": "🇳🇷",
    "Nepal": "🇳🇵", "Netherlands": "🇳🇱", "New Zealand": "🇳🇿", "Nicaragua": "🇳🇮", "Niger": "🇳🇪",
    "Nigeria": "🇳🇬", "North Macedonia": "🇲🇰", "Norway": "🇳🇴", "Oman": "🇴🇲", "Pakistan": "🇵🇰",
    "Palau": "🇵🇼", "Palestine": "🇵🇸", "Panama": "🇵🇦", "Papua New Guinea": "🇵🇬", "Paraguay": "🇵🇾",
    "Peru": "🇵🇪", "Philippines": "🇵🇭", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Qatar": "🇶🇦",
    "Romania": "🇷🇴", "Russia": "🇷🇺", "Rwanda": "🇷🇼", "Saint Kitts and Nevis": "🇰🇳",
    "Saint Lucia": "🇱🇨", "Saint Vincent and the Grenadines": "🇻🇨", "Samoa": "🇼🇸",
    "San Marino": "🇸🇲", "Sao Tome and Principe": "🇸🇹", "Saudi Arabia": "🇸🇦", "Senegal": "🇸🇳",
    "Serbia": "🇷🇸", "Seychelles": "🇸🇨", "Sierra Leone": "🇸🇱", "Singapore": "🇸🇬",
    "Slovakia": "🇸🇰", "Slovenia": "🇸🇮", "Solomon Islands": "🇸🇧", "Somalia": "🇸🇴",
    "South Africa": "🇿🇦", "South Sudan": "🇸🇸", "Spain": "🇪🇸", "Sri Lanka": "🇱🇰",
    "Sudan": "🇸🇩", "Suriname": "🇸🇷", "Sweden": "🇸🇪", "Switzerland": "🇨🇭", "Syria": "🇸🇾",
    "Taiwan": "🇹🇼", "Tajikistan": "🇹🇯", "Tanzania": "🇹🇿", "Thailand": "🇹🇭",
    "Timor-Leste": "🇹🇱", "Togo": "🇹🇬", "Tonga": "🇹🇴", "Trinidad and Tobago": "🇹🇹",
    "Tunisia": "🇹🇳", "Turkey": "🇹🇷", "Turkmenistan": "🇹🇲", "Tuvalu": "🇹🇻", "Uganda": "🇺🇬",
    "Ukraine": "🇺🇦", "UAE": "🇦🇪", "UK": "🇬🇧", "USA": "🇺🇸", "Uruguay": "🇺🇾",
    "Uzbekistan": "🇺🇿", "Vanuatu": "🇻🇺", "Vatican City": "🇻🇦", "Venezuela": "🇻🇪",
    "Vietnam": "🇻🇳", "Yemen": "🇾🇪", "Zambia": "🇿🇲", "Zimbabwe": "🇿🇼"
}

CODE_TO_COUNTRY = {
    "AF": "Afghanistan", "AL": "Albania", "DZ": "Algeria", "AD": "Andorra", "AO": "Angola",
    "AG": "Antigua and Barbuda", "AR": "Argentina", "AM": "Armenia", "AU": "Australia",
    "AT": "Austria", "AZ": "Azerbaijan", "BS": "Bahamas", "BH": "Bahrain", "BD": "Bangladesh",
    "BB": "Barbados", "BY": "Belarus", "BE": "Belgium", "BZ": "Belize", "BJ": "Benin",
    "BT": "Bhutan", "BO": "Bolivia", "BA": "Bosnia and Herzegovina", "BW": "Botswana",
    "BR": "Brazil", "BN": "Brunei", "BG": "Bulgaria", "BF": "Burkina Faso", "BI": "Burundi",
    "CV": "Cabo Verde", "KH": "Cambodia", "CM": "Cameroon", "CA": "Canada", "CF": "Central African Republic",
    "TD": "Chad", "CL": "Chile", "CN": "China", "CO": "Colombia", "KM": "Comoros", "CG": "Congo",
    "CR": "Costa Rica", "HR": "Croatia", "CU": "Cuba", "CY": "Cyprus", "CZ": "Czechia",
    "DK": "Denmark", "DJ": "Djibouti", "DM": "Dominica", "DO": "Dominican Republic", "EC": "Ecuador",
    "EG": "Egypt", "SV": "El Salvador", "GQ": "Equatorial Guinea", "ER": "Eritrea", "EE": "Estonia",
    "SZ": "Eswatini", "ET": "Ethiopia", "FJ": "Fiji", "FI": "Finland", "FR": "France",
    "GA": "Gabon", "GM": "Gambia", "GE": "Georgia", "DE": "Germany", "GH": "Ghana",
    "GR": "Greece", "GD": "Grenada", "GT": "Guatemala", "GN": "Guinea", "GW": "Guinea-Bissau",
    "GY": "Guyana", "HT": "Haiti", "HN": "Honduras", "HU": "Hungary", "IS": "Iceland",
    "IN": "India", "ID": "Indonesia", "IR": "Iran", "IQ": "Iraq", "IE": "Ireland",
    "IL": "Israel", "IT": "Italy", "CI": "Ivory Coast", "JM": "Jamaica", "JP": "Japan",
    "JO": "Jordan", "KZ": "Kazakhstan", "KE": "Kenya", "KI": "Kiribati", "KP": "Korea North",
    "KR": "Korea South", "XK": "Kosovo", "KW": "Kuwait", "KG": "Kyrgyzstan", "LA": "Laos",
    "LV": "Latvia", "LB": "Lebanon", "LS": "Lesotho", "LR": "Liberia", "LY": "Libya",
    "LI": "Liechtenstein", "LT": "Lithuania", "LU": "Luxembourg", "MG": "Madagascar",
    "MW": "Malawi", "MY": "Malaysia", "MV": "Maldives", "ML": "Mali", "MT": "Malta",
    "MH": "Marshall Islands", "MR": "Mauritania", "MU": "Mauritius", "MX": "Mexico",
    "FM": "Micronesia", "MD": "Moldova", "MC": "Monaco", "MN": "Mongolia", "ME": "Montenegro",
    "MA": "Morocco", "MZ": "Mozambique", "MM": "Myanmar", "NA": "Namibia", "NR": "Nauru",
    "NP": "Nepal", "NL": "Netherlands", "NZ": "New Zealand", "NI": "Nicaragua", "NE": "Niger",
    "NG": "Nigeria", "MK": "North Macedonia", "NO": "Norway", "OM": "Oman", "PK": "Pakistan",
    "PW": "Palau", "PS": "Palestine", "PA": "Panama", "PG": "Papua New Guinea", "PY": "Paraguay",
    "PE": "Peru", "PH": "Philippines", "PL": "Poland", "PT": "Portugal", "QA": "Qatar",
    "RO": "Romania", "RU": "Russia", "RW": "Rwanda", "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia", "VC": "Saint Vincent and the Grenadines", "WS": "Samoa",
    "SM": "San Marino", "ST": "Sao Tome and Principe", "SA": "Saudi Arabia", "SN": "Senegal",
    "RS": "Serbia", "SC": "Seychelles", "SL": "Sierra Leone", "SG": "Singapore",
    "SK": "Slovakia", "SI": "Slovenia", "SB": "Solomon Islands", "SO": "Somalia",
    "ZA": "South Africa", "SS": "South Sudan", "ES": "Spain", "LK": "Sri Lanka",
    "SD": "Sudan", "SR": "Suriname", "SE": "Sweden", "CH": "Switzerland", "SY": "Syria",
    "TW": "Taiwan", "TJ": "Tajikistan", "TZ": "Tanzania", "TH": "Thailand",
    "TL": "Timor-Leste", "TG": "Togo", "TO": "Tonga", "TT": "Trinidad and Tobago",
    "TN": "Tunisia", "TR": "Turkey", "TM": "Turkmenistan", "TV": "Tuvalu", "UG": "Uganda",
    "UA": "Ukraine", "AE": "UAE", "GB": "UK", "US": "USA", "UY": "Uruguay",
    "UZ": "Uzbekistan", "VU": "Vanuatu", "VA": "Vatican City", "VE": "Venezuela",
    "VN": "Vietnam", "YE": "Yemen", "ZM": "Zambia", "ZW": "Zimbabwe"
}

FLAG_TO_COUNTRY = {flag: country for country, flag in FLAGS.items()}
SERVICES = ["WhatsApp", "Facebook", "Telegram", "TikTok", "Instagram"]
SERVICE_ICONS = {"WhatsApp": "📱", "Facebook": "📘", "Telegram": "✈️", "TikTok": "🎵", "Instagram": "📷"}

def get_flag(country_name):
    clean = country_name
    for suf in [" WhatsApp","WA"," Facebook"," Instagram"," Telegram"," TikTok"," Whatsapp","whatsapp"]:
        clean = clean.replace(suf, "").replace(suf.lower(), "")
    clean = clean.strip()
    for name, flag in FLAGS.items():
        if name.lower() == clean.lower():
            return flag
    for name, flag in FLAGS.items():
        if name.lower() in clean.lower() or clean.lower() in name.lower():
            return flag
    return "🌍"

def get_country_from_text(text):
    if not text:
        return None
    match = re.search(r'country\s*name:?\s*👉\s*([A-Z]{2})', text, re.IGNORECASE)
    if match:
        code = match.group(1).upper()
        if code in CODE_TO_COUNTRY:
            return CODE_TO_COUNTRY[code]
    for flag, country in FLAG_TO_COUNTRY.items():
        if flag in text:
            return country
    text_lower = text.lower()
    # দেশের নাম শনাক্ত করার জন্য কীওয়ার্ড
    keywords = {country: [country.lower()] for country in FLAGS.keys()}
    for country, kw_list in keywords.items():
        for kw in kw_list:
            if kw in text_lower:
                return country
    return None

def load_countries():
    if os.path.exists(COUNTRIES_FILE):
        with open(COUNTRIES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_countries(c):
    with open(COUNTRIES_FILE, 'w') as f:
        json.dump(c, f, indent=4)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(u):
    with open(USERS_FILE, 'w') as f:
        json.dump(u, f, indent=4)

def load_taken_numbers():
    if os.path.exists(TAKEN_NUMBERS_FILE):
        with open(TAKEN_NUMBERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_taken_numbers(t):
    with open(TAKEN_NUMBERS_FILE, 'w') as f:
        json.dump(t, f, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            if "visible_services" not in data:
                data["visible_services"] = {s: True for s in SERVICES}
            if "highlighted_service" not in data:
                data["highlighted_service"] = None
            if "highlight_enabled" not in data:
                data["highlight_enabled"] = True
            return data
    return {"unique_number_mode": True, "highlighted_service": None, "highlight_enabled": True,
            "visible_services": {s: True for s in SERVICES}}

def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=4)

def load_traffic():
    if os.path.exists(TRAFFIC_FILE):
        with open(TRAFFIC_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_traffic(t):
    with open(TRAFFIC_FILE, 'w') as f:
        json.dump(t, f, indent=4)

countries = load_countries()
users = load_users()
taken_numbers = load_taken_numbers()
settings = load_settings()
traffic = load_traffic()

def is_admin(user_id):
    return user_id in ADMIN_IDS

async def is_joined_all(application, user_id):
    uid = str(user_id)
    if uid in users and users[uid].get("verified", False):
        return True
    for ch in CHANNELS:
        try:
            member = await application.bot.get_chat_member(chat_id=ch["chat_id"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    if uid not in users:
        users[uid] = {}
    users[uid]["verified"] = True
    save_users(users)
    return True

def update_traffic(country_name):
    now = time.time()
    if country_name not in traffic:
        traffic[country_name] = []
    traffic[country_name].append(now)
    cutoff = now - 600
    traffic[country_name] = [ts for ts in traffic[country_name] if ts > cutoff]
    save_traffic(traffic)

def get_traffic_counts():
    now = time.time()
    cutoff = now - 60
    return {c: sum(1 for ts in traffic.get(c, []) if ts > cutoff) for c in countries}

def get_top_traffic():
    cnts = get_traffic_counts()
    if not cnts:
        return None, 0
    top = max(cnts, key=cnts.get)
    return top, cnts[top]

# ------------------ কীবোর্ড বাটন (শুধু প্রধান মেনু) ------------------
def get_main_keyboard(is_admin_user=False):
    row1 = [KeyboardButton("📞 𝐆𝐄𝐓 𝐍𝐔𝐌𝐁𝐄𝐑"), KeyboardButton("🔥 𝐇𝐈𝐆𝐇 𝐓𝐑𝐀𝐅𝐅𝐈𝐂 🔥")]
    row2 = [KeyboardButton("🆘 𝐒𝐔𝐏𝐏𝐎𝐑𝐓")]
    if is_admin_user:
        row2.append(KeyboardButton("⚙️ 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋"))
    return ReplyKeyboardMarkup([row1, row2], resize_keyboard=True, one_time_keyboard=False)

WELCOME_TEXT = (
    "🎀 *⋆⁺₊☾ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐍𝐔𝐌𝐁𝐄𝐑 𝐁𝐎𝐓 ☽₊⁺⋆* 🎀\n\n"
    "💎 *─────────────* 💎\n✨ *𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐍𝐮𝐦𝐛𝐞𝐫𝐬* ✨\n🔥 *𝟐𝟒/𝟕 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞* 🔥\n💎 *─────────────* 💎\n\n👇 *𝐒𝐞𝐥𝐞𝐜𝐭 𝐚𝐧 𝐨𝐩𝐭𝐢𝐨𝐧 𝐛𝐞𝐥𝐨𝐰:*"
)

# ------------------ টেক্সট হ্যান্ডলার ------------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    chat_id = update.effective_chat.id

    if context.user_data.get('waiting_broadcast') and is_admin(user_id):
        users_list = load_users()
        if not users_list:
            await update.message.reply_text("No users.")
        else:
            success = fail = 0
            for uid in users_list:
                try:
                    await context.bot.send_message(chat_id=int(uid), text=text)
                    success += 1
                except:
                    fail += 1
            await update.message.reply_text(f"✅ Broadcast sent. Sent: {success}, Failed: {fail}")
        context.user_data['waiting_broadcast'] = False
        return

    if chat_id in [ch["chat_id"] for ch in CHANNELS]:
        country = get_country_from_text(text)
        if country:
            update_traffic(country)
        return

    if not await is_joined_all(context.application, user_id):
        await update.message.reply_text("🔒 Please verify first using /start")
        return

    if text == "📞 𝐆𝐄𝐓 𝐍𝐔𝐌𝐁𝐄𝐑":
        await show_services_inline(update, context)
    elif text == "🔥 𝐇𝐈𝐆𝐇 𝐓𝐑𝐀𝐅𝐅𝐈𝐂 🔥":
        await high_traffic_menu_inline(update, context)
    elif text == "🆘 𝐒𝐔𝐏𝐏𝐎𝐑𝐓":
        await support_inline(update, context)
    elif text == "⚙️ 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋" and is_admin(user_id):
        await admin_panel_inline(update, context)
    else:
        await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    top, cnt = get_top_traffic()
    traffic_line = f"\n\n🔥 *{get_flag(top)} {top} - {cnt} OTPs (Last Minute)* 🔥" if top else ""
    await update.message.reply_text(WELCOME_TEXT + traffic_line, reply_markup=get_main_keyboard(is_admin(user_id)), parse_mode="Markdown")

# ------------------ সার্ভিস লিস্ট (দুই কলাম) ------------------
async def show_services_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    visible = settings.get("visible_services", {})
    vis_services = [s for s in SERVICES if visible.get(s, True)]
    if not vis_services:
        await update.message.reply_text("❌ No services available.", reply_markup=get_main_keyboard(is_admin(user_id)))
        return
    if settings.get("highlight_enabled", True) and settings.get("highlighted_service") in vis_services:
        hl = settings["highlighted_service"]
        vis_services.remove(hl)
        vis_services.insert(0, hl)
    keyboard = []
    row = []
    for i, s in enumerate(vis_services):
        icon = SERVICE_ICONS.get(s, "📌")
        row.append(InlineKeyboardButton(f"{icon} {s}", callback_data=f"service_{s}"))
        if len(row) == 2 or i == len(vis_services)-1:
            keyboard.append(row)
            row = []
    keyboard.append([InlineKeyboardButton("◀️ MAIN MENU", callback_data="main_menu")])
    await update.message.reply_text("🔧 *SELECT SERVICE*\n\nChoose a service to get numbers:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ------------------ দেশের লিস্ট (দুই কলাম) ------------------
async def show_countries_inline(update: Update, context: ContextTypes.DEFAULT_TYPE, service):
    country_data = [(cname, len(svcs[service])) for cname, svcs in countries.items() if service in svcs and svcs[service]]
    if not country_data:
        await update.callback_query.edit_message_text(f"❌ No numbers for {service}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ BACK", callback_data="back_to_services")]]))
        return
    keyboard = []
    row = []
    for i, (cname, cnt) in enumerate(country_data):
        flag = get_flag(cname)
        badge = f" ({cnt})" if cnt > 1 else ""
        row.append(InlineKeyboardButton(f"{flag} {cname}{badge}", callback_data=f"country_{service}_{cname}"))
        if len(row) == 2 or i == len(country_data)-1:
            keyboard.append(row)
            row = []
    keyboard.append([InlineKeyboardButton("◀️ BACK", callback_data="back_to_services")])
    await update.callback_query.edit_message_text(f"{SERVICE_ICONS.get(service,'📌')} *{service}*\n\n🌍 Select a country:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ------------------ নম্বর দেখানো (টেক্সট) ------------------
async def show_numbers_inline(update: Update, context: ContextTypes.DEFAULT_TYPE, service, country_name):
    user_id = update.callback_query.from_user.id
    num_list = countries.get(country_name, {}).get(service, [])
    if not num_list:
        await update.callback_query.edit_message_text(f"No numbers for {service} in {country_name}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ BACK", callback_data="back_to_countries")]]))
        return
    context.user_data['current_country'] = country_name
    context.user_data['current_service'] = service
    unique = settings.get("unique_number_mode", True)
    taken_key = f"{country_name}|{service}"
    taken = taken_numbers.get(taken_key, []) if unique else []
    avail = [n for n in num_list if n not in taken] if unique else num_list[:]
    if not avail:
        await update.callback_query.edit_message_text("⚠️ No more numbers! Click CHANGE NUMBER or contact admin.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data="change_number_inline")], [InlineKeyboardButton("◀️ BACK", callback_data="back_to_countries")]]))
        return
    random.shuffle(avail)
    show = avail[:4]
    context.user_data['current_display_numbers'] = show
    flag = get_flag(country_name)
    nums_text = "\n".join(f"{flag} 📞 `{n if n.startswith('+') else '+' + n}`" for n in show)
    total = len(num_list); left = len(avail)
    text = f"{flag} *{country_name}* | {SERVICE_ICONS.get(service,'📌')} *{service}*\n\n📊 Total: {total}\n✅ Left: {left}\n\n{nums_text}\n⏰ OTP will arrive soon."
    keyboard = [
        [InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data="change_number_inline")],
        [InlineKeyboardButton("🔑 OTP GROUP", url=OTP_GROUP_LINK)],
        [InlineKeyboardButton("◀️ BACK", callback_data="back_to_countries")]
    ]
    await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def change_number_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = context.user_data.get('current_country')
    service = context.user_data.get('current_service')
    if not country or not service:
        await query.edit_message_text("Please select a country and service first.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ MAIN MENU", callback_data="main_menu")]]))
        return
    num_list = countries.get(country, {}).get(service, [])
    if not num_list:
        await query.edit_message_text("No numbers available.")
        return
    unique = settings.get("unique_number_mode", True)
    taken_key = f"{country}|{service}"
    taken = taken_numbers.get(taken_key, []) if unique else []
    avail = [n for n in num_list if n not in taken] if unique else num_list[:]
    if not avail:
        await query.edit_message_text("No new numbers. Contact admin to reset.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ BACK", callback_data="back_to_countries")]]))
        return
    random.shuffle(avail)
    show = avail[:4]
    context.user_data['current_display_numbers'] = show
    flag = get_flag(country)
    nums_text = "\n".join(f"{flag} 📞 `{n if n.startswith('+') else '+' + n}`" for n in show)
    total = len(num_list); left = len(avail)
    text = f"{flag} *{country}* | {SERVICE_ICONS.get(service,'📌')} *{service}*\n\n📊 Total: {total}\n✅ Left: {left}\n\n{nums_text}\n⏰ OTP will arrive soon."
    keyboard = [
        [InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data="change_number_inline")],
        [InlineKeyboardButton("🔑 OTP GROUP", url=OTP_GROUP_LINK)],
        [InlineKeyboardButton("◀️ BACK", callback_data="back_to_countries")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ------------------ হাই ট্রাফিক মেনু (দুই কলাম) ------------------
async def high_traffic_menu_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    row = []
    for i, s in enumerate(SERVICES):
        icon = SERVICE_ICONS.get(s, "📌")
        row.append(InlineKeyboardButton(f"{icon} {s}", callback_data=f"traffic_{s}"))
        if len(row) == 2 or i == len(SERVICES)-1:
            keyboard.append(row)
            row = []
    keyboard.append([InlineKeyboardButton("◀️ MAIN MENU", callback_data="main_menu")])
    await update.message.reply_text("📊 *TRAFFIC REPORT*\nSelect a service:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def high_traffic_result_inline(update: Update, context: ContextTypes.DEFAULT_TYPE, service):
    query = update.callback_query
    eligible = [c for c, svcs in countries.items() if service in svcs and svcs[service]]
    if not eligible:
        await query.edit_message_text(f"No numbers for {service}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ BACK", callback_data="back_to_traffic")]]))
        return
    counts = get_traffic_counts()
    filtered = {c: counts.get(c, 0) for c in eligible}
    sorted_items = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    lines = []
    for idx, (c, cnt) in enumerate(sorted_items, 1):
        flag = get_flag(c)
        if cnt == 0:
            col = "⚫"
        elif idx == 1:
            col = "🟢"
        elif idx == 2:
            col = "🟡"
        else:
            col = "🔴"
        lines.append(f"{col} {flag} *{c}* – `{cnt}` OTPs")
    text = f"📊 *{service} TRAFFIC (Last Minute)*\n\n" + "\n".join(lines) + "\n\n🟢 1st   🟡 2nd   🔴 Others   ⚫ No"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ BACK", callback_data="back_to_traffic")]]), parse_mode="Markdown")

# ------------------ সাপোর্ট ------------------
async def support_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👨‍💻 ADMIN 1", url=SUPPORT_LINK)],
        [InlineKeyboardButton("👨‍💻 ADMIN 2", url=SUPPORT_LINK)],
        [InlineKeyboardButton("◀️ MAIN MENU", callback_data="main_menu")]
    ])
    await update.message.reply_text("🆘 *SUPPORT*\n\nClick below to contact:", reply_markup=keyboard, parse_mode="Markdown")

# ------------------ অ্যাডমিন প্যানেল (দুই কলাম) ------------------
async def admin_panel_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("Access denied.")
        return
    mode = "🟢 ENABLED" if settings.get("unique_number_mode", True) else "🔴 DISABLED"
    hl_status = "🟢 ON" if settings.get("highlight_enabled", True) else "🔴 OFF"
    text = f"🔧 *ADMIN PANEL*\n\nUnique Mode: {mode}\nHighlight Mode: {hl_status}"
    
    buttons = [
        ("📁 ADD COUNTRY", "add_country"),
        ("🗑 DELETE COUNTRY", "del_country"),
        ("📜 VIEW COUNTRIES", "view_countries"),
        ("👥 VIEW USERS", "view_users"),
        ("📢 BROADCAST", "broadcast"),
        ("👁️ MANAGE VISIBILITY", "manage_visibility"),
        ("⭐ HIGHLIGHT SERVICE", "highlight_service"),
        (f"HIGHLIGHT MODE: {hl_status}", "toggle_highlight_mode"),
        (f"🎯 UNIQUE MODE: {mode}", "toggle_unique_mode"),
        ("🔄 RESET NUMBERS", "reset_taken"),
        ("📊 RESET TRAFFIC", "reset_traffic"),
        ("◀️ MAIN MENU", "main_menu")
    ]
    keyboard = []
    row = []
    for i, (label, callback) in enumerate(buttons):
        row.append(InlineKeyboardButton(label, callback_data=callback))
        if len(row) == 2 or i == len(buttons)-1:
            keyboard.append(row)
            row = []
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ------------------ কলব্যাক হ্যান্ডলার ------------------
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "main_menu":
        await show_main_menu(update, context)
        await query.delete_message()
        return
    if data == "back_to_services":
        await show_services_inline(update, context)
        await query.delete_message()
        return
    if data == "back_to_countries":
        service = context.user_data.get('selected_service')
        if service:
            await show_countries_inline(update, context, service)
        else:
            await show_services_inline(update, context)
        return
    if data == "back_to_traffic":
        await high_traffic_menu_inline(update, context)
        await query.delete_message()
        return

    if data.startswith("service_"):
        service = data[8:]
        context.user_data['selected_service'] = service
        await show_countries_inline(update, context, service)
        return

    if data.startswith("country_"):
        parts = data.split("_", 2)
        if len(parts) >= 3:
            service = parts[1]
            country = parts[2]
            context.user_data['selected_service'] = service
            await show_numbers_inline(update, context, service, country)
        return

    if data == "change_number_inline":
        await change_number_inline(update, context)
        return

    if data.startswith("traffic_"):
        service = data[8:]
        await high_traffic_result_inline(update, context, service)
        return

    # অ্যাডমিন অপশন
    if not is_admin(user_id):
        await query.edit_message_text("Access denied.")
        return

    if data == "add_country":
        context.user_data['waiting_country'] = True
        await query.edit_message_text("📁 Send a .txt file.\nFilename: `Country_Service.txt` or `Service_Country.txt`\nExample: `India_WhatsApp.txt`", parse_mode="Markdown")
    elif data == "del_country":
        if not countries:
            await query.edit_message_text("No countries.")
            return
        kb = [[InlineKeyboardButton(f"{get_flag(c)} {c}", callback_data=f"del_{c}")] for c in countries]
        kb.append([InlineKeyboardButton("◀️ BACK", callback_data="admin_back")])
        await query.edit_message_text("Select country to delete:", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("del_"):
        cname = data[4:]
        if cname in countries:
            del countries[cname]
            save_countries(countries)
            await query.edit_message_text(f"✅ Deleted {cname}.")
        else:
            await query.edit_message_text("Not found.")
    elif data == "view_countries":
        if not countries:
            await query.edit_message_text("No countries.")
            return
        txt = "📜 COUNTRIES & SERVICES\n\n"
        for c, svcs in countries.items():
            flag = get_flag(c)
            txt += f"{flag} *{c}*\n"
            for s, nums in svcs.items():
                txt += f"   {SERVICE_ICONS.get(s,'📌')} {s}: {len(nums)}\n"
            txt += "\n"
        await query.edit_message_text(txt, parse_mode="Markdown")
    elif data == "view_users":
        if not users:
            await query.edit_message_text("No users.")
            return
        txt = f"👥 Total users: {len(users)}\n\n"
        for i, (uid, uinfo) in enumerate(list(users.items())[:20]):
            name = uinfo.get('name', 'Unknown')
            txt += f"{i+1}. {name} – `{uid}`\n"
        await query.edit_message_text(txt, parse_mode="Markdown")
    elif data == "broadcast":
        context.user_data['waiting_broadcast'] = True
        await query.edit_message_text("📢 Send the broadcast message:")
    elif data == "manage_visibility":
        visible = settings.get("visible_services", {})
        kb = []
        row = []
        for i, s in enumerate(SERVICES):
            row.append(InlineKeyboardButton(f"{'✅' if visible.get(s,True) else '❌'} {s}", callback_data=f"vis_{s}"))
            if len(row) == 2 or i == len(SERVICES)-1:
                kb.append(row); row = []
        kb.append([InlineKeyboardButton("◀️ BACK", callback_data="admin_back")])
        await query.edit_message_text("Toggle service visibility:", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("vis_"):
        s = data[4:]
        if s in SERVICES:
            visible = settings.get("visible_services", {})
            visible[s] = not visible.get(s, True)
            settings["visible_services"] = visible
            save_settings(settings)
            await query.edit_message_text(f"✅ {s} visibility toggled.")
            await callback_handler(update, context)
    elif data == "highlight_service":
        kb = []
        row = []
        for i, s in enumerate(SERVICES):
            row.append(InlineKeyboardButton(f"{SERVICE_ICONS.get(s,'📌')} {s}", callback_data=f"hlight_{s}"))
            if len(row) == 2 or i == len(SERVICES)-1:
                kb.append(row); row = []
        kb.append([InlineKeyboardButton("❌ REMOVE HIGHLIGHT", callback_data="hlight_remove")])
        kb.append([InlineKeyboardButton("◀️ BACK", callback_data="admin_back")])
        await query.edit_message_text("Select service to highlight:", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("hlight_"):
        if data == "hlight_remove":
            settings["highlighted_service"] = None
            save_settings(settings)
            await query.edit_message_text("✅ Highlight removed.")
        else:
            s = data[7:]
            if s in SERVICES:
                settings["highlighted_service"] = s
                save_settings(settings)
                await query.edit_message_text(f"✅ Highlight set to {s}.")
    elif data == "toggle_highlight_mode":
        settings["highlight_enabled"] = not settings.get("highlight_enabled", True)
        save_settings(settings)
        await query.edit_message_text(f"Highlight mode now {'ON' if settings['highlight_enabled'] else 'OFF'}.")
    elif data == "toggle_unique_mode":
        settings["unique_number_mode"] = not settings.get("unique_number_mode", True)
        save_settings(settings)
        await query.edit_message_text(f"Unique mode now {'ON' if settings['unique_number_mode'] else 'OFF'}.")
    elif data == "reset_taken":
        global taken_numbers
        taken_numbers = {}
        save_taken_numbers(taken_numbers)
        await query.edit_message_text("✅ Taken numbers reset.")
    elif data == "reset_traffic":
        global traffic
        traffic = {}
        save_traffic(traffic)
        await query.edit_message_text("✅ Traffic data reset.")
    elif data == "admin_back":
        await admin_panel_inline(update, context)
        await query.delete_message()
    else:
        await query.edit_message_text("Unknown command.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('waiting_country') or not is_admin(update.effective_user.id):
        return
    doc = update.message.document
    if not doc.file_name.endswith('.txt'):
        await update.message.reply_text("Send a .txt file.")
        return
    base = doc.file_name.replace('.txt', '')
    parts = base.split('_')
    if len(parts) != 2:
        await update.message.reply_text("Filename must be Country_Service.txt or Service_Country.txt")
        return
    service = None
    country_name = None
    for s in SERVICES:
        if s.lower() == parts[0].lower():
            service = s
            country_name = parts[1]
            break
        if s.lower() == parts[1].lower():
            service = s
            country_name = parts[0]
            break
    if not service:
        await update.message.reply_text(f"Invalid service. Allowed: {', '.join(SERVICES)}")
        return
    file = await doc.get_file()
    file_path = os.path.join(DATA_FOLDER, doc.file_name)
    await file.download_to_drive(file_path)
    with open(file_path, 'r') as f:
        new_numbers = [line.strip() for line in f if line.strip()]
    if not new_numbers:
        await update.message.reply_text("No numbers in file.")
        return
    if country_name not in countries:
        countries[country_name] = {}
    if service not in countries[country_name]:
        countries[country_name][service] = []
    countries[country_name][service].extend(new_numbers)
    save_countries(countries)
    flag = get_flag(country_name)
    await update.message.reply_text(f"✅ Added {len(new_numbers)} numbers for {flag} {country_name} | {SERVICE_ICONS.get(service,'📌')} {service}")
    context.user_data['waiting_country'] = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    uid = str(user_id)
    if uid not in users:
        user_info = update.effective_user
        users[uid] = {"name": user_info.full_name, "username": user_info.username, "joined_date": str(update.message.date)}
        save_users(users)
    if await is_joined_all(context.application, user_id):
        await show_main_menu(update, context)
    else:
        kb = []
        for ch in CHANNELS:
            kb.append([InlineKeyboardButton(f"📢 JOIN {ch['username'].upper()}", url=ch["link"])])
        kb.append([InlineKeyboardButton("✅ VERIFY", callback_data="verify_now")])
        await update.message.reply_text(
            "🔒 *ACCESS REQUIRED*\n\nPlease join the channels below and click VERIFY:",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if await is_joined_all(context.application, user_id):
        await query.edit_message_text("✅ Verified! Welcome.")
        await show_main_menu(update, context)
    else:
        await query.edit_message_text("❌ Verification failed. Join all channels and try again.")

def main():
    print("🤖 Bot starting... All inline buttons in 2 columns, numbers as text.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify_now"))
    app.add_handler(CallbackQueryHandler(callback_handler, pattern="^(?!verify_now).*"))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

if __name__ == "__main__":
    main()

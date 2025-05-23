import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
db_auth = str(os.getenv("db_auth"))
admin_id = int(os.getenv("admin_id"))
custom_api_url = str(os.getenv("custom_api_url"))
MEASUREMENT_ID = str(os.getenv("MEASUREMENT_ID"))
API_SECRET = str(os.getenv("API_SECRET"))
CHANNEL_ID = str(os.getenv("CHANNEL_ID"))
CHANNEL_USERNAME = str(os.getenv("CHANNEL_USERNAME"))
OUTPUT_DIR = "downloads"
INSTAGRAM_RAPID_API_HOST = str(os.getenv("INSTAGRAM_RAPID_API_HOST"))
INSTAGRAM_RAPID_API_KEY1 = str(os.getenv("INSTAGRAM_RAPID_API_KEY1"))
INSTAGRAM_RAPID_API_KEY2 = str(os.getenv("INSTAGRAM_RAPID_API_KEY2"))

BOT_COMMANDS = [
    {'command': 'start', 'description': '🚀 Get started🔥'},
    {'command': 'settings', 'description': '⚙️ Settings🛠'},
    {'command': 'stats', 'description': '📊 Statistics📈'},
    {'command': 'remove_keyboard', 'description': '🗑️ Remove keyboard🗑️'},

]

ADMINS_UID = [admin_id]

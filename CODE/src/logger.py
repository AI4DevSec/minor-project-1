import logging
import os
from datetime import datetime

# Ek folder banate hain jahan diary entries save hongi
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR,exist_ok=True) # Agar folder pehle se hai toh theek hai

# Diary file ka naam (Aaj ki date ke saath)
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Diary mein kya kya likhna hai aur kis format mein likhna hai, yeh batate hain
logging.basicConfig(
    filename=LOG_FILE, # Kis file mein likhna hai
    format='%(asctime)s - %(levelname)s - %(message)s', # Kaise dikhe entry (time - level - message)
    level=logging.INFO # Sirf important messages (INFO level aur usse upar) likho
)

# Ek function jo diary entry likhne mein help karega
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO) # Is specific diary mein bhi INFO level messages likho
    return logger # Diary entry robot wapas bhej do use karne ke liye
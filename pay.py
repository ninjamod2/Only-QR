import os
import logging
from telethon import TelegramClient, events
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use your own values from my.telegram.org
api_id = os.getenv('API_ID', '22627280')  # Replace with your actual API ID
api_hash = os.getenv('API_HASH', 'b2e5eb5e3dd886f5b8be6a749a26f619')  # Replace with your actual API Hash

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

# Define your channel link
channel_link = "https://t.me/+GUUGE6jYNKZiZDll"  # Replace with your actual channel link

# Path to your QR code image
qr_code_path = 'qr.jpg'  # Replace with the path to your QR code image

# Cooldown period in seconds
cooldown_period = 600

# Dictionary to track last QR request time for each user
last_qr_request = {}

# Function to check if you are online
async def is_user_online(client, user_id):
    try:
        user = await client.get_entity(user_id)
        return user.status is not None and user.status.online
    except Exception as e:
        logger.error(f"Error checking online status for {user_id}: {e}")
        return False

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        # Check if the message is from a user (not a group or channel)
        if event.is_private:
            # Get the current time
            current_time = datetime.now().time()

            # Define the time window for dinner time
            start_time = datetime.strptime("20:00", "%H:%M").time()
            end_time = datetime.strptime("22:00", "%H:%M").time()

            # Convert the message text to lowercase for case-insensitive comparison
            message_text = event.raw_text.lower()

            # Keywords list for QR request detection
            qr_keywords = ['qr', 'upi', 'scanner', 'scanr']

            # Check if the message contains any QR related keyword
            if any(keyword in message_text for keyword in qr_keywords):
                user_id = event.sender_id
                now = datetime.now()

                # Check if the user is in the cooldown period
                if user_id in last_qr_request:
                    last_request_time = last_qr_request[user_id]
                    if (now - last_request_time).total_seconds() < cooldown_period:
                        await event.reply("Please wait before requesting the QR code again.")
                        return

                # Send the QR code image and update the last request time
                await client.send_file(event.chat_id, qr_code_path, caption="Here is my QR code for payment. 
" + channel_link)
                last_qr_request[user_id] = now
            
            elif 'free' in message_text:
                # Respond to messages containing 'free' with formatted text and clickable link
                reply_text = f'free vala to channel pr milega bhai
Channel <a href="{channel_link}">CLICK HERE</a>'
                await event.reply(reply_text, parse_mode='html')
            
            elif 'channel' in message_text or 'channel link' in message_text or 'link' in message_text:
                # Respond to messages containing 'channel', 'channel link', or 'link'
                await event.reply(f"My channel link: {channel_link}")
            
            elif start_time <= current_time <= end_time:
                # Send a specific auto-reply during dinner time
                await event.reply(f"It's DINNER TIME! I will reply to you soon. Check out my channel: {channel_link}")
            
            else:
                # Check if you are offline
                user_id = 'NINJAGAMEROP'  # Replace with your Telegram user ID
                online_status = await is_user_online(client, user_id)

                if not online_status:
                    # If offline, send the offline message
                    await event.reply("I am offline now. Please wait for my reply.")
    except Exception as e:
        await event.reply("An error occurred while processing your request. Please try again later.")
        logger.error(f"Error handling message: {e}")

# Start the client
client.start()
logger.info("Client is running...")

# Run the client until you stop it
client.run_until_disconnected()

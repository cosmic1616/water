import os
import logging
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'
WATERMARK_TEXT = 'Watermark Text'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a video and I will add a watermark to it!')

def add_watermark(video_path: str, output_path: str, text: str) -> None:
    video = VideoFileClip(video_path)
    txt_clip = TextClip(text, fontsize=24, color='white').set_position(('right', 'bottom')).set_duration(video.duration)
    result = CompositeVideoClip([video, txt_clip])
    result.write_videofile(output_path, codec='libx264')

def handle_video(update: Update, context: CallbackContext) -> None:
    video = update.message.video
    video_file = video.get_file()
    video_path = f"{video_file.file_id}.mp4"
    video_file.download(video_path)
    
    output_path = f"watermarked_{video_file.file_id}.mp4"
    add_watermark(video_path, output_path, WATERMARK_TEXT)
    
    update.message.reply_video(video=open(output_path, 'rb'))
    
    os.remove(video_path)
    os.remove(output_path)

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.video, handle_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

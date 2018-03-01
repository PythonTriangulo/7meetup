from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job

from telegramusers import *
from apitoken import telegram_api_token
import logging
import os
# INIT
updater = Updater(token=telegram_api_token)
dispatcher = updater.dispatcher
logging.basicConfig(level=logging.DEBUG)

hostname = os.uname()[1]
profile = profiles[hostname]

from functools import wraps

def auth(fn):
        @wraps(fn)
        def wrapper(bot, update, *args, **kargs):
                cond1 = update.message.from_user.username in profile['ids']
                cond2 = update.message.chat.id in profile['groups']

                # if update.message.from_user.username not in auth_usernames:
                if cond1 or cond2:
                        return fn(bot, update, *args, **kargs)
                else:
                        bot.sendMessage(chat_id=update.message.chat_id, text='oops')
        return wrapper


@auth
def image(bot, update):
	"""ffmpeg -y -an -r 40 -hwaccel:v auto -f v4l2 -i /dev/video0
	   -vf 'scale=640:480,transpose=1' -frames 1 /home/pi/telegram.pict2.png"""

	image_file = '/tmp/telegram.pict2.jpg'
	transpose = ["-vf", "'scale=640:480,transpose=1'"]
	transpose = []
	args = ['ffmpeg', '-y', '-an', '-r', '40', '-hwaccel:v', 'auto', 
			'-f', 'v4l2', '-i', '/dev/video0', '-frames', '1']
	try:
		check_call(args + transpose + [image_file])
	except Exception as e:
		bot.sendMessage(chat_id=update.message.chat_id,
			text='Error getting the image:\n'+repr(e) )
	else:
		bot.sendPhoto(chat_id=update.message.chat_id,
			photo=open(image_file, 'rb'))
# Register

functions = {'image': image}


image_handler  = CommandHandler('image', image)

# for handle in handlers.values():

dispatcher.add_handler(image_handler)

#init_job = Job(init, 1, repeat=False)
#updater.job_queue.put(init_job)

updater.start_polling()
updater.idle()

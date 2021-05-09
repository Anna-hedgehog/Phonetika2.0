import telebot
import csv
import os
from time import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import librosa
import librosa.display
import numpy as np
import io
from PIL import Image
#import soundfile as sf


bot = telebot.TeleBot("1696654491:AAH6Dei2EZGSlMUNJYk5VcwokYcr1RSFuOk", parse_mode=None)

dict_termin = {}
dict_photo = {}
dict_exp = {}
dict_bu = {}

with open("30phoneticexamples.csv", encoding="utf-8") as f:
    table = csv.DictReader(f, delimiter = ";")
    for row in table:
        dict_termin.update({ row["termin_input"] : row["termin_eng"]})
        dict_exp.update({ row["termin_input"] : row["termin_explanation"]})
        dict_photo.update({ row["termin_input"] : row["photo_norm"]})
        dict_bu.update({ row["termin_input"] : row["photo_real"]})
        

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока','/help')

keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('да!', 'нет...')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Привет, как дела с фонетикой? /start', reply_markup=keyboard1)

@bot.message_handler(commands=["help"])
def bot_messages(message):
    text = "Что я могу?\n1. Помочь тебе быстро узнать английский аналог фонетического термина и показать картинку, связанную с ним (для этого отправь мне название термина на русском).\n2. Помучить тебя спектрограммами:\n - Ты можешь записать слово, которое в дальнейшем будет отгадывать другой человек (напиши боту : записать).\n - И можешь сам отгадывать спектрограммы (напиши боту: распознать)"
    bot.send_message(message.chat.id, text)

#USERS_STATES = dict()
#WAITING_FOR_IMAGE_REPONSE="ждём ответа про картинку"
@bot.message_handler(content_types=['text'])
def send_text(message):
   if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, юный фонетист!')
   elif message.text.lower() == 'пока':
       bot.send_message(message.chat.id, 'А я думал мы ещё пораспознаём...')
   elif message.text.lower() == 'давай ботать':
       bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBHfVgalcUDaS9gTMwi7SfjS1KohcE6wACUQEAAjDUnRFgiXnyUbaU0x4E')       
   elif message.text.lower() in dict_termin.keys():
       bot.send_message(message.chat.id, dict_termin[message.text.lower()])
       if message.text.lower() in dict_exp.keys():
           if dict_exp[message.text.lower()] != "":
               bot.send_message(message.chat.id, dict_exp[message.text.lower()])
       if message.text.lower() in dict_photo.keys():
           if dict_photo[message.text.lower()] != "":
               photo = open(dict_photo[message.text.lower()], 'rb')
               bot.send_photo(message.chat.id, photo)
       if message.text.lower() in dict_bu.keys():
           if dict_bu[message.text.lower()] != "":
               photo2 = open(dict_bu[message.text.lower()], 'rb')
               bot.send_photo(message.chat.id, photo2)
   elif message.text.lower() == 'записать':
        bot.send_message(message.chat.id, 'произнеси слово три раза')
       # word = open("words.txt", "a", encoding="utf-8")
       # word.write("{word_now}/n".format(word_now=message.text))   #нужен states ???
   elif message.text.lower() == 'распознать':
        spect = open("privet1.png", 'rb')
        bot.send_photo(message.chat.id, spect)
   else:
       bot.send_message(message.chat.id, "такого я не знаю : ( ")

     
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    num = 0
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'{message.chat.id}_{int(time())}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    #data, samplerate = sf.read(f'{message.chat.id}_{int(time())}.ogg')
    #sf.write(f'{message.chat.id}_{int(time())}.wav', data, samplerate)
    
    num += 1
    new_row = [num, f'{message.chat.id}_{int(time())}.wav']
    with open('audio.csv', 'a', encoding="utf-8") as audio_file:
         table = csv.DictReader(audio_file, delimiter = ",")
         writer = csv.writer(audio_file)
         writer.writerow(new_row)
         
    samples, sample_rate = librosa.load('privet.wav')
    fig = plt.figure(figsize=[4, 4])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    S = librosa.feature.melspectrogram(y=samples, sr=sample_rate)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    buf = io.BytesIO()
    plt.savefig(buf,  bbox_inches='tight',pad_inches=0)

    # plt.close('all')
    buf.seek(0)
    im = Image.open(buf)
    # im = Image.open(buf).convert('L')
    im.show()
    buf.close()

    im.save("privet1.png")

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


@bot.message_handler(content_types=['photo'])
def photo_id(message):
        print(message)
        


bot.polling()

#parselmouth,
    #author = "Yannick Jadoul and Bill Thompson and Bart de Boer",
    #title = "Introducing {P}arselmouth: A {P}ython interface to {P}raat",
    #journal = "Journal of Phonetics",
    #volume = "71",
    #pages = "1--15",
    #year = "2018",
    #doi = "https://doi.org/10.1016/j.wocn.2018.07.001

#praat,
    #author = "Paul Boersma and David Weenink",
    #title = "{P}raat: doing phonetics by computer [{C}omputer program]",
    #howpublished = "Version 6.1.38, retrieved 2 January 2021 \url{http://www.praat.org/}",
    #year = "2021"
import telebot
import csv
import os
from time import time
import random
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ffmpeg
import soundfile as sf
import speech_recognition as sr

bot.remove_webhook()
bot = telebot.TeleBot("1888982099:AAFZRuNSnipKFyGPfa2ajHJhVIavS4zZYhs", parse_mode=None)

dict_termin = {}
dict_photo = {}
dict_exp = {}
dict_bu = {}

dict_users_states = {}

with open("30phoneticexamples.csv", encoding="utf-8") as f:
    table = csv.DictReader(f, delimiter = ";")
    for row in table:
        dict_termin.update({ row["termin_input"] : row["termin_eng"]})
        dict_exp.update({ row["termin_input"] : row["termin_explanation"]})
        dict_photo.update({ row["termin_input"] : row["photo_norm"]})
        dict_bu.update({ row["termin_input"] : row["photo_real"]})

audio_png = []
word_recognize = []

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.add("/help", "Привет", "Пока","список терминов", "записать", "распознать")

@bot.message_handler(commands=["start"])
def send_welcome(message):
	bot.reply_to(message, "Привет, как дела с фонетикой? /start", reply_markup=keyboard1)

@bot.message_handler(commands=["help"])
def bot_messages(message):
    text = '''Что я могу?\n
1. Рассказать тебе про фонетический термин:\n дам английский аналог и определение, покажу картинку\n(для этого отправь мне название термина на русском)\n
2. Помучить тебя спектрограммами:\n
- Ты можешь записать слово, которое в дальнейшем будет отгадывать другой человек\n(напиши боту : записать).\n
- И можешь сам отгадывать спектрограммы\n(напиши боту: распознать)'''
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"])
def send_text(message):
   if dict_users_states.get(message.chat.id) != "stop_now_word":
       if message.text.lower() == "привет":
           bot.send_message(message.chat.id, "Привет, юный фонетист!")
       elif message.text.lower() == "пока":
           bot.send_message(message.chat.id, "А я думал мы ещё пораспознаём...")
       elif message.text.lower() == "список терминов":
           bot.send_message(message.chat.id,'''Тезаурус\n
(инициация) ингрессивная\n
(инициация) легочная\n
(инициация) нелегочная\n
(инициация) эгрессивная\n
МФА\n
альвеоло-палатальные\n
альвеолярные\n
альвеолярный гребень\n
апикальные\n
аппроксимант\n
артикуляция\n
аффриката\n
боковой\n
веляризованный\n
велярная\n
велярные\n
верхний подъём\n
взрывной\n
вибрант\n
вокалическое пространство\n
время задержки фонации\n
выдержка\n
выступ гортани\n
глайд\n
гласные\n
глотка\n
глоттальная\n
глухой\n
голосовая связка\n
гортанная полость\n
гортанная смычка\n
грудная клетка\n
губно-губные\n
губные\n
дифтонг\n
дифтонгоиды\n
дорсальные\n
дрожащий\n
задний ряд\n
закрытые\n
звонкий\n
зубные\n
имплозивные\n
инициация\n
кадык\n
кликсы\n
кончик языка\n
корень языка\n
лабиализованный\n
лабиодентальные\n
ламина\n
ламинальные\n
ларингализованный\n
ларингальные\n
ленис\n
межзубные\n
монофтонг\n
мягкое небо\n
надгортанник\n
назализация\n
назализованный\n
назализованный\n
напряжённые\n
нейтральная фонация\n
ненапряжённые\n
нижний подъём\n
носовая полость\n
носовой\n
носовые\n
оглушённый\n
огубленный\n
одноударный вибрант\n
открытые\n
палатализованный\n
палатальные\n
переднеязычные\n
передний ряд\n
перстневидный хрящ\n
пищевод\n
полнозвонкий\n
полузвонкий\n
постальвеолярные\n
придыхание\n
придыхательный голос\n
рекурсия\n
ретрофлексные\n
ротовая полость\n
скрипучий голос\n
согласные\n
сонорные\n
спинка языка\n
способ образования\n
средний подъём\n
средний ряд\n
твердое небо\n
трахея\n
трифтонг\n
увула\n
увулярные\n
фарингализованный\n
фарингальные\n
фонация\n
форманта\n
фортис\n
фрикативный\n
черпаловидный хрящ\n
шва\n
шумные\n
щитовидный хрящ\n
эйективы\n
экскурсия\n''')
       elif message.text.lower() in dict_termin.keys():
           bot.send_message(message.chat.id, dict_termin[message.text.lower()])
           if message.text.lower() in dict_exp.keys():
               if dict_exp[message.text.lower()] != "":
                   bot.send_message(message.chat.id, dict_exp[message.text.lower()])
           if message.text.lower() in dict_photo.keys():
               if dict_photo[message.text.lower()] != "":
                   photo = open(dict_photo[message.text.lower()], "rb")
                   bot.send_photo(message.chat.id, photo)
           if message.text.lower() in dict_bu.keys():
               if dict_bu[message.text.lower()] != "":
                   photo2 = open(dict_bu[message.text.lower()], "rb")
                   bot.send_photo(message.chat.id, photo2)
       elif message.text.lower() == "записать":
           bot.send_message(message.chat.id, "пожалуйса, произнеси слово три раза, желательно в тихом месте!")
       elif message.text.lower() == "распознать":
           with open("audio.csv", "r", encoding="utf-8") as audio_file_for_user:
               table = csv.DictReader(audio_file_for_user, delimiter = ",")
               for row in table:
                   if row["spectro_name"] is not None:
                       audio_png.append(row["spectro_name"])
           random_spectro = random.choice(audio_png)
           print(random_spectro)
           word_f = random_spectro.replace("_spectro.png", ".txt")
           oscillo_f = random_spectro.replace("_spectro.png", "_oscillo.png")       
           spect = open(random_spectro, "rb")
           oscillo = open(oscillo_f, "rb")
           bot.send_photo(message.chat.id, spect)
           bot.send_photo(message.chat.id, oscillo)
           with open(word_f, "r", encoding = "utf-8") as text:
               for line in text:
                   word = line.split(" ")[1]
                   word_recognize.append(word)
                   print(word)
                   dict_users_states.update({message.chat.id: "stop_now_word"})
       else:
           bot.send_message(message.chat.id, "такого я не знаю : ( ")
           bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEBSadgnrg-xfSGb-H9w6LCDUfJ-imwrwACBg4AAjew8UhrpjZM1I9SGB8E")
   else:
       if message.text.lower() == word_recognize[len(word_recognize)-1]:
           bot.send_message(message.chat.id, "Верно! Ты настоящий фонетист!")
           bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEBS-lgn0aYSfQFwB_A7rSUE-mkpfT8awACQw0AAtcBAAFJu3cn5y7NrJsfBA")
           dict_users_states[message.chat.id] = ""
       elif message.text.lower() == "ответ":
           bot.send_message(message.chat.id,"Правильный ответ: " + word_recognize[len(word_recognize)-1])
           dict_users_states[message.chat.id] = ""
       else:
           bot.send_message(message.chat.id, "Попробуй ещё!\n Присылай слово. Верю, у тебя получится!\n\n А если сдаёшься:\n напиши боту слово: ответ")
       
@bot.message_handler(content_types=["voice"])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    ogg_fname = f"{message.chat.id}_{int(time())}.ogg"
    wav_fname = ogg_fname.replace(".ogg", ".wav")
    txt_fname = ogg_fname.replace(".ogg", ".txt")
    png_spectro_fname = ogg_fname.replace(".ogg", "_spectro.png")
    png_oscillo_fname = ogg_fname.replace(".ogg", "_oscillo.png")
    
    with open(ogg_fname, "wb") as new_file:
        new_file.write(downloaded_file)

    os.system(f"ffmpeg -i {ogg_fname} {wav_fname}")
    
    r = sr.Recognizer()
    my_file = sr.AudioFile(wav_fname)
    with my_file as source:
        audio = r.record(source, duration = 40)
    f = open(txt_fname, "w", encoding = "utf-8")
    print(r.recognize_google(audio, language = "ru-RU"), file = f)
    f.close()
    
    new_row = [wav_fname, txt_fname, png_spectro_fname, png_oscillo_fname]
    with open("audio.csv", "a", encoding = "utf-8", newline="") as audio_file:
         table = csv.DictReader(audio_file, delimiter = ",")
         writer = csv.writer(audio_file)
         writer.writerow(new_row)

    sns.set()
    plt.rcParams['figure.dpi'] = 100 

    snd = parselmouth.Sound(wav_fname)

    def draw_spectrogram(spectrogram, dynamic_range=70):
        X, Y = spectrogram.x_grid(), spectrogram.y_grid()
        sg_db = 10 * np.log10(spectrogram.values)
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
        plt.ylim([spectrogram.ymin, spectrogram.ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")

    def draw_intensity(intensity):
        plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
        plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
        plt.grid(False)
        plt.ylim(0)
        plt.ylabel("intensity [dB]")

    def draw_pitch(pitch):
        pitch_values = pitch.selected_array['frequency']
        pitch_values[pitch_values==0] = np.nan
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=3, color='w')
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=1)
        plt.grid(False)
        plt.ylim(0, pitch.ceiling)
        plt.ylabel("fundamental frequency [Hz]")
    
    plt.figure()
    plt.plot(snd.xs(), snd.values.T, linewidth=0.5)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")

    plt.savefig(png_oscillo_fname)    

    plt.rcParams['figure.dpi'] = 400
    pitch = snd.to_pitch()
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])

    plt.savefig(png_spectro_fname)
    
@bot.message_handler(content_types=["sticker"])
def sticker_id(message):
    print(message)

@bot.message_handler(content_types=["photo"])
def photo_id(message):
        print(message)
        
bot.polling()

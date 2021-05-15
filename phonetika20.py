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

bot = telebot.TeleBot("1696654491:AAH6Dei2EZGSlMUNJYk5VcwokYcr1RSFuOk", parse_mode=None)

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
1 (инициация) ингрессивная\n
2 (инициация) легочная\n
3 (инициация) нелегочная\n
4 (инициация) эгрессивная\n
5 МФА\n
6 альвеоло-палатальные\n
7 альвеолярные\n
8 альвеолярный гребень\n
9 апикальные\n
10 аппроксимант\n
11 артикуляция\n
12 аффриката\n
13 боковой\n
14 веляризованный\n
15 велярная\n
16 велярные\n
17 верхний подъём\n
18 взрывной\n
19 вибрант\n
20 вокалическое пространство\n
21 время задержки фонации\n
22 выдержка\n
23 выступ гортани\n
24 глайд\n
25 гласные\n
26 глотка\n
27 глоттальная\n
28 глухой\n
29 голосовая связка\n
30 гортанная полость\n
31 гортанная смычка\n
32 грудная клетка\n
33 губно-губные\n
34 губные\n
35 дифтонг\n
36 дифтонгоиды\n
37 дорсальные\n
38 дрожащий\n
39 задний ряд\n
40 закрытые\n
41 звонкий\n
42 зубные\n
43 имплозивные\n
44 инициация\n
45 кадык\n
46 кликсы\n
47 кончик языка\n
48 корень языка\n
49 лабиализованный\n
50 лабиодентальные\n
51 ламина\n
52 ламинальные\n
53 ларингализованный\n
54 ларингальные\n
55 ленис\n
56 межзубные\n
57 монофтонг\n
58 мягкое небо\n
59 надгортанник\n
60 назализация\n
61 назализованный\n
62 назализованный\n
63 напряжённые\n
64 нейтральная фонация\n
65 ненапряжённые\n
66 нижний подъём\n
67 носовая полость\n
68 носовой\n
69 носовые\n
70 оглушённый\n
71 огубленный\n
72 одноударный вибрант\n
73 открытые\n
74 палатализованный\n
75 палатальные\n
76 переднеязычные\n
77 передний ряд\n
78 перстневидный хрящ\n
79 пищевод\n
80 полнозвонкий\n
81 полузвонкий\n
82 постальвеолярные\n
83 придыхание\n
84 придыхательный голос\n
85 рекурсия\n
86 ретрофлексные\n
87 ротовая полость\n
88 скрипучий голос\n
89 согласные\n
90 сонорные\n
91 спинка языка\n
92 способ образования\n
93 средний подъём\n
94 средний ряд\n
95 твердое небо\n
96 трахея\n
97 трифтонг\n
98 увула\n
99 увулярные\n
100 фарингализованный\n
101 фарингальные\n
102 фонация\n
103 форманта\n
104 фортис\n
105 фрикативный\n
106 черпаловидный хрящ\n
107 шва\n
108 шумные\n
109 щитовидный хрящ\n
110 эйективы\n
111 экскурсия\n''')
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

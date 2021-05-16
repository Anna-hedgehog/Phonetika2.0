# Фонетика 2.0
## Проект студенток 1 курса ОП "Фундаментальная и компьютерная лингвистика" НИУ ВШЭ Кузнецовой Светланы и Анны Елагиной.
## Руководитель проекта: Олег Сериков

**Бот в Telegram** - *[@phonetika2_0bot](https://t.me/phonetika2_0bot)* который может:
+ служить фонетическим справочником - отправлять в ответ на запрос термин на английском, определение и поясняющую картинку, а также фотографии и картинки речепроизводящих органов;
+ быть “фонетической игрушкой”:
    + записывать аудиосообщения пользователей,
    + создавать на их основе спектрограммы,
    + отправлять составленные спектрограммы другим пользователям для разгадывания.

### Цель проекта
+ наш бот поможет студентам подготовиться к тесту или экзамену по фонетике,
+ позволит обратить обучение в игру:
    + сложный процесс изучения спектро- и осциллограмм теперь возможен без установки Praata.

### С какими библиотеками мы работали:

**pyTelegramBotAPI**  - собственно telegram bot

**[praat-parselmouth](https://parselmouth.readthedocs.io/en/stable/)** - позволяет создавать осциллограммы, спектрограммы
```
@article{parselmouth,
    author = "Yannick Jadoul and Bill Thompson and Bart de Boer",
     = "Introducing {P}arselmouth: A {P}ython interface to {P}raat",
    journal = "Journal of Phonetics",
    volume = "71",
    pages = "1--15",
    year = "2018",
    doi = "https://doi.org/10.1016/j.wocn.2018.07.001"
}
```
библиотека работает с программой **[praat](https://www.fon.hum.uva.nl/praat/)**:
```
@misc{praat,
    author = "Paul Boersma and David Weenink",
    title = "{P}raat: doing phonetics by computer [{C}omputer program]",
    howpublished = "Version 6.1.38, retrieved 2 January 2021 \url{http://www.praat.org/}",
    year = "2021"
}
```
**numpy** - предоставляет базовые методы для манипуляции с большими массивами и матрицами

**random** - позволяет генерировать рандомный набор элементов

**matplotlib** - библиотека для визуализации статистических данных

**seaborn** - библиотека для создания статистических графиков на Python

**ffmpeg** - позволяет работать с разными форматами аудио и видео (позволяет переводить из формата в формат)

**soundfile** - позволяет читать и записывать звуковые файлы

**speech_recognition** - распознавание речи


#### Наши контакты:

телеграм для обратной связи, вопросов и предложений:

Анна Елагина - *@anka_hedgehog*

Светлана Кузнецова - *@Krahekrahzte*

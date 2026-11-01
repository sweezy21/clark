# clark
 Clark — голосовой ассистент
Голосовой помощник на Python: слушает микрофон, распознаёт русскую речь через Google Speech Recognition и выполняет команды — открывает сайты, запускает программы, управляет громкостью, делает скриншоты и отвечает звуками.

Требования
Python 3.8+
Windows 

Установка

    git clone https://github.com/username/clark-assistant.git
    cd clark-assistant
    pip install -r requirements.txt
    
Или установите всё одной командой:

    pip install SpeechRecognition pyaudio pygame pycaw comtypes keyboard Pillow

Используемые библиотеки

    SpeechRecognition - Распознавание речи (Google API)
    PyAudio -	Доступ к микрофону
    pygame -	Воспроизведение звуков
    pycaw,comtypes -	Управление громкостью Windows
    keyboard-Работа с клавиатурой
    Pillow -	Скриншоты (ImageGrab)
    webbrowser, subprocess, ctypes	Стандартные — не требуют установки

Запуск

    python main.py

После запуска скажите одну из команд (микрофон слушает 7 секунд):

    «кларк» — вызвать ассистента
    
    «привет кларк», «доброе утро», «как дела», «спасибо»
    
    «открой браузер / ютуб / вконтакте / телеграм / github»
    
    «открой блокнот / калькулятор / проводник»
    
    «время»
    
    «прибавь / убавь громкость»
    
    «сделай скриншот»
    
    «сверни всё» / «покажи рабочий стол»
    
    «включи музыку» (Spotify) / «включи ютуб музыку»
    
    «я ушел» — завершить работу

Примечания
Работает только на Windows.
Для распознавания речи нужен интернет (Google Speech API).

При первом запуске pygame инициализирует аудио — папка sounds/ должна существовать.



Лицензия
Проект распространяется под лицензией MIT. 

    Copyright (c) 2026 
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

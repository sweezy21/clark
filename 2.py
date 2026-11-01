# -*- coding: utf-8 -*-
import speech_recognition as sr
import webbrowser
import datetime
import pygame
import os
import time
import random

# Импорты для новых команд
import subprocess
import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import ImageGrab


class ClarkAssistant:
    def __init__(self):
        print("Запуск")

        # Звук
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.sounds_folder = os.path.join(BASE_DIR, "sounds")
        self.load_sounds()

        
        self.sound_playing = False

        # Микрофон
        self.setup_microphone()

        # команды
        self.load_my_commands()

        print("\n" + "=" * 50)
        print("КЛАРК ГОТОВ")
        print("=" * 50)
        self.show_commands()

    def load_sounds(self):
        
        if os.path.exists(self.sounds_folder):
            self.sounds = sorted([
                f for f in os.listdir(self.sounds_folder)
                if f.lower().endswith(('.wav', '.mp3'))
            ])
            print(f"✅ Загружено звуков: {len(self.sounds)}")
        else:
            print(f"❌ Папка {self.sounds_folder} не найдена!")
            self.sounds = []

    def setup_microphone(self):
        
        try:
            for i, name in enumerate(sr.Microphone.list_microphone_names()):
                if "voicemod" in name.lower():
                    self.microphone = sr.Microphone(device_index=i)
                    return

            self.microphone = sr.Microphone()
        except Exception as e:
            self.microphone = sr.Microphone()

    # Действия команд -
    def act_time(self):
        print(f"🕐 Сейчас {datetime.datetime.now().strftime('%H:%M')}")


    def act_how_are_you(self):
        phrases = ["Отлично!", "Хорошо, спасибо!", "Все системы в норме.",
                   "Работаю в штатном режиме.", "Лучше всех!"]
        print(f"{random.choice(phrases)}")

    def act_open(self, url):
        webbrowser.open(url)
        print(f"🌐 Открываю: {url}")

    def act_run(self, program):
        """Запускает программу БЕЗ блокировки (в фоне)"""
        try:
            subprocess.Popen(program, shell=True)
            print(f"Запускаю: {program}")
        except Exception as e:
            print(f"❌ Ошибка запуска: {e}")

    # ============ НОВЫЕ ДЕЙСТВИЯ ============

    def act_volume(self, delta):
       #Меняет громкость
        try:
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume
            current = volume.GetMasterVolumeLevelScalar()
            new = max(0.0, min(1.0, current + delta / 100))
            volume.SetMasterVolumeLevelScalar(new, None)
            print(f"Громкость: {int(new * 100)}%")
        except Exception as e:
            print(f"❌ Ошибка громкости: {e}")

    def act_screenshot(self):
        #Делает скриншот
        try:
            folder = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
            os.makedirs(folder, exist_ok=True)
            name = datetime.datetime.now().strftime("screenshot_%Y-%m-%d_%H-%M-%S.png")
            path = os.path.join(folder, name)
            ImageGrab.grab().save(path)
            print(f"📸 Скриншот сохранён: {path}")
        except Exception as e:
            print(f"❌ Ошибка скриншота: {e}")

    def act_explorer(self):
        #проводник
        try:
            subprocess.Popen("explorer", shell=True)
            print("Проводник открыт")
        except Exception as e:
            print(f"Ошибка: {e}")

    def act_show_desktop(self):
    
        try:
            import ctypes
            user32 = ctypes.windll.user32

            VK_LWIN = 0x5B
            VK_D    = 0x44
            KEYEVENTF_KEYUP = 0x0002

            # Зажимаем Win
            user32.keybd_event(VK_LWIN, 0, 0, 0)
            time.sleep(0.05)
            # Жмём D
            user32.keybd_event(VK_D, 0, 0, 0)
            time.sleep(0.05)
            # Отпускаем D
            user32.keybd_event(VK_D, 0, KEYEVENTF_KEYUP, 0)
            # Отпускаем Win
            user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)

            print("Рабочий стол")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    # =======================================

    def load_my_commands(self):
        """Загружает команды"""
        self.commands = {
            # === старые команды ===
            "привет кларк":     {"sounds": ["12.mp3"]},
            "открой браузер":   {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_open("https://google.com")},
            "открой youtube":   {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_open("https://youtube.com")},
            "время":            {"sounds": ["8.wav"], "action": self.act_time},
            "спасибо":          {"sounds": ["13.wav"]},
            "доброе утро":      {"sounds": ["6.wav"]},
            "я ушел":           {"sounds": ["2.mp3"], "exit": True},

            "открой гугл":      {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_open("https://google.com")},
            "открой вконтакте": {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_open("https://vk.com")},
            "открой telegram":  {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_open("https://web.telegram.org")},
            "открой github":    {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_open("https://github.com")},
            "открой блокнот":   {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_run("notepad")},
            "открой калькулятор":{"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                 "action": lambda: self.act_run("calc")},
            "как дела":         {"sounds": ["1.mp3", '11.wav']},

            # === НОВЫЕ КОМАНДЫ ===
            "убавь громкость на 10": {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": lambda: self.act_volume(-10)},
            "убавь громкость":       {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": lambda: self.act_volume(-10)},
            "прибавь громкость":     {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": lambda: self.act_volume(+10)},
            "включи музыку":         {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": lambda: self.act_open("https://open.spotify.com")},
            "включи ютуб музыку":    {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": lambda: self.act_open("https://music.youtube.com")},
            "сделай скриншот":       {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": self.act_screenshot},
            "открой проводник":      {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": self.act_explorer},
            "сверни всё":            {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": self.act_show_desktop},
            "покажи рабочий стол":   {"sounds": ["4.wav", "5.wav", "8.wav", "9.wav"],
                                      "action": self.act_show_desktop},
        }

        self.command_keys = list(self.commands.keys())
        print(f"Загружено команд: {len(self.command_keys)}")

    def play_sound(self, filename):
        
        filepath = os.path.join(self.sounds_folder, filename)

        if not os.path.exists(filepath):
            # Регистронезависимый поиск
            if os.path.exists(self.sounds_folder):
                for real_name in os.listdir(self.sounds_folder):
                    if real_name.lower() == filename.lower():
                        filepath = os.path.join(self.sounds_folder, real_name)
                        break

        if not os.path.exists(filepath):
            print(f"❌ Файл {filename} не найден!")
            return False

        try:
            print(f"{filename}")
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.sound_playing = True
            return True
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")
            return False

    def wait_sound_end(self, timeout=30):
        
        start = time.time()
        while pygame.mixer.music.get_busy():
            if time.time() - start > timeout:
                break
            time.sleep(0.1)
        self.sound_playing = False

    def show_commands(self):
        #Показывает доступные команды
        print("\n📋 ТВОИ КОМАНДЫ:")
        for i, (cmd, data) in enumerate(self.commands.items(), 1):
            sounds = data.get("sounds", [])
            has_action = "⚙" if data.get("action") else " "
            print(f"  {i:2}. {has_action} '{cmd}' -> {sounds if sounds else '(без звука)'}")
        print("-" * 50)

    def listen(self):
        # 7 second
        recognizer = sr.Recognizer()

        try:
            with self.microphone as source:
                print("\n Слушаю 7 секунд...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)

            print(" Распознаю...")
            command = recognizer.recognize_google(audio, language='ru-RU')
            command = command.lower()
            print(f"Вы сказали: {command}")
            return command

        except sr.WaitTimeoutError:
            print("Время вышло")
            return ""
        except sr.UnknownValueError:
            print("❌ Не удалось распознать")
            return ""
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return ""

    def process_command(self, command):
        """Обрабатывает команду"""
        if not command:
            return True

        command_found = False

        # просто кларк
        if "кларк" in command and len(command.split()) == 1:
            print(f"✅ Вызов Кларка -> 33.wav")
            self.play_sound("33.wav")
            self.wait_sound_end(timeout=10)
            return True

        # 2. СПЕЦИАЛЬНО: "я ушел" = выход
        if "я уш" in command:
            print(f"✅ Нашел команду: 'я ушел' (выход)")
            self.play_sound("2.mp3")
            self.wait_sound_end(timeout=10)
            time.sleep(1)
            return False

        # 3. ПРОВЕРЯЕМ ОСТАЛЬНЫЕ КОМАНДЫ
        for cmd_key, cmd_data in self.commands.items():
            if cmd_key in command and cmd_key != "я ушел":
                print(f"✅ Нашел команду: '{cmd_key}'")

                # Звук (если есть)
                sounds = cmd_data.get("sounds", [])
                if sounds:
                    chosen_file = random.choice(sounds) if len(sounds) > 1 else sounds[0]
                    self.play_sound(chosen_file)
                    # Ждём окончания звука, но не дольше 5 сек (защита от зависания)
                    self.wait_sound_end(timeout=5)

                # Действие (если есть)
                action = cmd_data.get("action")
                if action:
                    try:
                        action()
                    except Exception as e:
                        print(f"❌ Ошибка действия: {e}")

                command_found = True
                break

        # 4. ЕСЛИ КОМАНДА НЕ НАЙДЕНА
        if not command_found:
            print(" Команда не распознана -> 13.mp3")
            self.play_sound("13.mp3")
            self.wait_sound_end(timeout=5)

        return True

    def run(self):
        # запуск
        print("\n🎧 Ожидание команд...")
        print("Скажи 'кларк', 'привет кларк', 'доброе утро', 'я ушел' и др.")

        running = True
        while running:
            command = self.listen()
            if command:
                running = self.process_command(command)


# Запуск
if __name__ == "__main__":
    clark = ClarkAssistant()
    clark.run()
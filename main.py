import os
import sys
import time
import json
import colorama
from colorama import Fore, Back, Style
from telethon import TelegramClient, errors
import asyncio
import platform

colorama.init(autoreset=True)

# Конфигурация
CONFIG_FILE = "config.json"
STATS_FILE = "stats.json"

# ТВОЙ ТЕКСТ
MY_TEXT = """
╭━━━┳╮╱╱╭┳━╮╱╭┳━━━┳━━━┳━━━━┳━━━┳━━━╮
┃╭━╮┃╰╮╭╯┃┃╰╮┃┃╭━━┫╭━╮┃╭╮╭╮┃╭━━┫╭━╮┃
┃╰━━╋╮╰╯╭┫╭╮╰╯┃╰━━┫╰━━╋╯┃┃╰┫╰━━┫╰━╯┃
╰━━╮┃╰╮╭╯┃┃╰╮┃┃╭━━┻━━╮┃╱┃┃╱┃╭━━┫╭╮╭╯
┃╰━╯┃╱┃┃╱┃┃╱┃┃┃╰━━┫╰━╯┃╱┃┃╱┃╰━━┫┃┃╰╮
╰━━━╯╱╰╯╱╰╯╱╰━┻━━━┻━━━╯╱╰╯╱╰━━━┻╯╰━╯
"""

class Synaster:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.client = None
        self.message_text = ""
        self.target = ""
        self.target_type = "лс"  # лс, чат, группа, канал
        self.message_count = 0
        self.sent_count = 0
        self.is_sending = False
        self.load_config()
        self.load_stats()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.BLACK + MY_TEXT + Style.RESET_ALL)
        print(Fore.WHITE + "="*60 + Style.RESET_ALL)
        print(Fore.CYAN + "⚡ SYNASTER - Telegram Spammer" + Style.RESET_ALL)
        print(Fore.WHITE + "="*60 + Style.RESET_ALL + "\n")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.api_id = config.get('api_id')
                    self.api_hash = config.get('api_hash')
                    self.phone = config.get('phone')
            except:
                pass

    def save_config(self):
        config = {
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'phone': self.phone
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    def load_stats(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    stats = json.load(f)
                    self.sent_count = stats.get('total_sent', 0)
            except:
                self.sent_count = 0

    def save_stats(self):
        stats = {'total_sent': self.sent_count}
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=4)

    def show_menu(self):
        self.clear_screen()
        
        # Инфо о платформе
        device = platform.system()
        print(Fore.YELLOW + f"💻 Устройство: {Fore.WHITE}{device}" + Style.RESET_ALL)
        
        # Статистика
        print(Fore.YELLOW + "\n📊 СТАТИСТИКА:" + Style.RESET_ALL)
        print(Fore.WHITE + f"   Всего отправлено: {Fore.GREEN}{self.sent_count}{Style.RESET_ALL}")
        if self.is_sending:
            print(Fore.RED + "   СТАТУС: РАССЫЛКА АКТИВНА" + Style.RESET_ALL)
        print()
        
        # Меню
        print(Fore.YELLOW + "📋 МЕНЮ:" + Style.RESET_ALL)
        print(Fore.WHITE + "   1. " + Fore.GREEN + "Настройка API" + Style.RESET_ALL)
        print(Fore.WHITE + "   2. " + Fore.GREEN + "Ввести сообщение" + Style.RESET_ALL)
        print(Fore.WHITE + "   3. " + Fore.GREEN + "Выбрать цель для спама" + Style.RESET_ALL)
        print(Fore.WHITE + "   4. " + Fore.GREEN + "Указать количество сообщений" + Style.RESET_ALL)
        print(Fore.WHITE + "   5. " + Fore.RED + "ЗАПУСТИТЬ СПАМ" + Style.RESET_ALL)
        print(Fore.WHITE + "   6. " + Fore.RED + "СТОП (остановить спам)" + Style.RESET_ALL)
        print(Fore.WHITE + "   0. " + Fore.RED + "Выход" + Style.RESET_ALL)
        print()
        
        # Текущие настройки
        print(Fore.YELLOW + "⚙️ ТЕКУЩИЕ НАСТРОЙКИ:" + Style.RESET_ALL)
        print(Fore.WHITE + f"   Тип цели: {Fore.CYAN}{self.target_type}{Style.RESET_ALL}")
        print(Fore.WHITE + f"   Цель: {Fore.CYAN}{self.target if self.target else 'не указана'}{Style.RESET_ALL}")
        print(Fore.WHITE + f"   Кол-во: {Fore.CYAN}{self.message_count if self.message_count > 0 else 'не указано'}{Style.RESET_ALL}")
        print(Fore.WHITE + f"   Текст: {Fore.CYAN}{self.message_text[:30] + '...' if len(self.message_text) > 30 else self.message_text}{Style.RESET_ALL}")
        print()
        
        choice = input(Fore.CYAN + "➜ Выберите пункт: " + Style.RESET_ALL)
        return choice

    def setup_api(self):
        self.clear_screen()
        print(Fore.YELLOW + "🔧 НАСТРОЙКА API" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Нужно для работы на любом устройстве (ПК/телефон)" + Style.RESET_ALL)
        print(Fore.WHITE + "Бери с https://my.telegram.org" + Style.RESET_ALL)
        print()
        
        self.api_id = input(Fore.GREEN + "→ API ID: " + Style.RESET_ALL)
        self.api_hash = input(Fore.GREEN + "→ API Hash: " + Style.RESET_ALL)
        self.phone = input(Fore.GREEN + "→ Твой номер (+7...): " + Style.RESET_ALL)
        
        self.save_config()
        print(Fore.GREEN + "\n✅ Сохранено! Работает на всех устройствах" + Style.RESET_ALL)
        time.sleep(2)

    def input_message(self):
        self.clear_screen()
        print(Fore.YELLOW + "📝 ТЕКСТ СООБЩЕНИЯ" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Введи текст (END - закончить):" + Style.RESET_ALL)
        print()
        
        lines = []
        while True:
            line = input()
            if line == "END":
                break
            lines.append(line)
        
        self.message_text = "\n".join(lines)
        
        if self.message_text:
            print(Fore.GREEN + f"\n✅ Текст сохранён ({len(self.message_text)} символов)" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Текст пустой" + Style.RESET_ALL)
        
        input(Fore.WHITE + "\nНажми Enter..." + Style.RESET_ALL)

    def choose_target(self):
        self.clear_screen()
        print(Fore.YELLOW + "🎯 ВЫБОР ЦЕЛИ" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Куда будем спамить?" + Style.RESET_ALL)
        print()
        print(Fore.WHITE + "   1. " + Fore.CYAN + "ЛС (личные сообщения)" + Style.RESET_ALL)
        print(Fore.WHITE + "   2. " + Fore.CYAN + "Чат" + Style.RESET_ALL)
        print(Fore.WHITE + "   3. " + Fore.CYAN + "Группа" + Style.RESET_ALL)
        print(Fore.WHITE + "   4. " + Fore.CYAN + "Канал" + Style.RESET_ALL)
        print()
        
        type_choice = input(Fore.GREEN + "→ Выбери тип (1-4): " + Style.RESET_ALL)
        
        type_map = {
            '1': 'лс',
            '2': 'чат',
            '3': 'группа',
            '4': 'канал'
        }
        
        if type_choice in type_map:
            self.target_type = type_map[type_choice]
            print(Fore.GREEN + f"\n✅ Тип выбран: {self.target_type}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Неверный выбор" + Style.RESET_ALL)
            input(Fore.WHITE + "\nEnter..." + Style.RESET_ALL)
            return
        
        print()
        print(Fore.WHITE + "Теперь введи @username или ссылку:" + Style.RESET_ALL)
        print(Fore.WHITE + "   Пример: @durov" + Style.RESET_ALL)
        print(Fore.WHITE + "   Пример: https://t.me/durov" + Style.RESET_ALL)
        print()
        
        self.target = input(Fore.GREEN + "→ Цель: " + Style.RESET_ALL)
        
        if self.target:
            print(Fore.GREEN + f"\n✅ Цель сохранена: {self.target}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Цель не указана" + Style.RESET_ALL)
        
        input(Fore.WHITE + "\nEnter..." + Style.RESET_ALL)

    def set_message_count(self):
        self.clear_screen()
        print(Fore.YELLOW + "🔢 КОЛИЧЕСТВО" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Сколько раз отправить?" + Style.RESET_ALL)
        print()
        
        try:
            count = int(input(Fore.GREEN + "→ Количество: " + Style.RESET_ALL))
            if count > 0:
                self.message_count = count
                print(Fore.GREEN + f"\n✅ Будет отправлено: {count}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n❌ Должно быть больше 0" + Style.RESET_ALL)
        except:
            print(Fore.RED + "\n❌ Это должно быть число" + Style.RESET_ALL)
        
        input(Fore.WHITE + "\nEnter..." + Style.RESET_ALL)

    def stop_sending(self):
        if self.is_sending:
            self.is_sending = False
            print(Fore.RED + "\n⛔ ОСТАНАВЛИВАЮ СПАМ!" + Style.RESET_ALL)
            time.sleep(1)
        else:
            print(Fore.YELLOW + "\n⚠️ Спам не запущен" + Style.RESET_ALL)
            time.sleep(1)

    async def send_messages(self):
        if not all([self.api_id, self.api_hash, self.phone]):
            print(Fore.RED + "❌ Сначала настрой API" + Style.RESET_ALL)
            return False
        
        if not self.message_text:
            print(Fore.RED + "❌ Введи текст" + Style.RESET_ALL)
            return False
        
        if not self.target:
            print(Fore.RED + "❌ Выбери цель" + Style.RESET_ALL)
            return False
        
        if self.message_count <= 0:
            print(Fore.RED + "❌ Укажи количество" + Style.RESET_ALL)
            return False
        
        print(Fore.YELLOW + "\n⚡ Подключаюсь к Telegram..." + Style.RESET_ALL)
        
        self.client = TelegramClient('session_' + self.phone, int(self.api_id), self.api_hash)
        await self.client.start(phone=self.phone)
        
        print(Fore.GREEN + "✅ Подключено!" + Style.RESET_ALL)
        print(Fore.RED + f"\n🔥 НАЧИНАЮ СПАМ В {self.target_type.upper()} 🔥" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        
        try:
            # Получаем цель
            entity = await self.client.get_entity(self.target)
            
            self.is_sending = True
            sent_in_session = 0
            
            for i in range(self.message_count):
                if not self.is_sending:
                    print(Fore.RED + "\n⛔ СПАМ ОСТАНОВЛЕН" + Style.RESET_ALL)
                    break
                
                try:
                    await self.client.send_message(entity, self.message_text)
                    sent_in_session += 1
                    self.sent_count += 1
                    self.save_stats()
                    
                    print(Fore.GREEN + f"✅ [{i+1}/{self.message_count}] Отправлено в {self.target_type}: {self.target}" + Style.RESET_ALL)
                    
                    # Задержка
                    await asyncio.sleep(1.5)
                    
                except errors.FloodWaitError as e:
                    wait = e.seconds
                    print(Fore.RED + f"⚠️ Флуд контроль: ждём {wait} сек" + Style.RESET_ALL)
                    await asyncio.sleep(wait)
                    
                except Exception as e:
                    print(Fore.RED + f"❌ Ошибка: {str(e)[:50]}" + Style.RESET_ALL)
                    await asyncio.sleep(2)
            
            print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
            print(Fore.GREEN + f"✅ СПАМ ЗАВЕРШЁН!" + Style.RESET_ALL)
            print(Fore.WHITE + f"   Отправлено сейчас: {Fore.CYAN}{sent_in_session}{Style.RESET_ALL}")
            print(Fore.WHITE + f"   Всего отправлено: {Fore.CYAN}{self.sent_count}{Style.RESET_ALL}")
            
        except Exception as e:
            print(Fore.RED + f"❌ Ошибка: {e}" + Style.RESET_ALL)
        
        await self.client.disconnect()
        self.is_sending = False
        
        input(Fore.WHITE + "\nEnter..." + Style.RESET_ALL)
        return True

    def start_sending(self):
        if self.is_sending:
            print(Fore.RED + "❌ Спам уже идёт" + Style.RESET_ALL)
            time.sleep(1)
            return
        
        self.clear_screen()
        print(Fore.YELLOW + "🔥 ЗАПУСК СПАМА" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + f"Тип цели: {Fore.CYAN}{self.target_type}{Style.RESET_ALL}")
        print(Fore.WHITE + f"Цель: {Fore.CYAN}{self.target}{Style.RESET_ALL}")
        print(Fore.WHITE + f"Количество: {Fore.CYAN}{self.message_count}{Style.RESET_ALL}")
        print(Fore.WHITE + f"Текст: {Fore.CYAN}{self.message_text[:50]}...{Style.RESET_ALL}")
        print()
        print(Fore.RED + "⚠️  ВНИМАНИЕ: Telegram может заблокировать аккаунт!" + Style.RESET_ALL)
        print(Fore.RED + "⚠️  Работает на ПК и телефоне (везде где есть Python)" + Style.RESET_ALL)
        print()
        
        confirm = input(Fore.YELLOW + "Всё равно запустить? (y/n): " + Style.RESET_ALL)
        if confirm.lower() == 'y':
            asyncio.run(self.send_messages())

    def run(self):
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.setup_api()
            elif choice == '2':
                self.input_message()
            elif choice == '3':
                self.choose_target()
            elif choice == '4':
                self.set_message_count()
            elif choice == '5':
                self.start_sending()
            elif choice == '6':
                self.stop_sending()
            elif choice == '0':
                self.clear_screen()
                print(Fore.RED + "Выход..." + Style.RESET_ALL)
                sys.exit(0)
            else:
                print(Fore.RED + "Неверный выбор!" + Style.RESET_ALL)
                time.sleep(1)

if __name__ == "__main__":
    app = Synaster()
    app.run()

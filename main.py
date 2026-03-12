import os
import sys
import time
import json
import colorama
from colorama import Fore, Back, Style
from telethon import TelegramClient, errors
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import asyncio
import threading

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
        self.target_username = ""
        self.message_count = 0
        self.sent_count = 0
        self.is_sending = False
        self.load_config()
        self.load_stats()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.BLACK + MY_TEXT + Style.RESET_ALL)
        print(Fore.WHITE + "="*60 + Style.RESET_ALL)
        print(Fore.CYAN + "⚡ SYNASTER - Массовая рассылка в Telegram" + Style.RESET_ALL)
        print(Fore.WHITE + "="*60 + Style.RESET_ALL + "\n")

    def load_config(self):
        """Загрузка конфигурации"""
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
        """Сохранение конфигурации"""
        config = {
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'phone': self.phone
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    def load_stats(self):
        """Загрузка статистики"""
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    stats = json.load(f)
                    self.sent_count = stats.get('total_sent', 0)
            except:
                self.sent_count = 0
        else:
            self.sent_count = 0

    def save_stats(self):
        """Сохранение статистики"""
        stats = {
            'total_sent': self.sent_count
        }
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=4)

    def show_menu(self):
        """Отображение главного меню"""
        self.clear_screen()
        print(Fore.YELLOW + "📊 СТАТИСТИКА:" + Style.RESET_ALL)
        print(Fore.WHITE + f"   Всего отправлено сообщений: {Fore.GREEN}{self.sent_count}{Style.RESET_ALL}")
        print()
        print(Fore.YELLOW + "📋 МЕНЮ:" + Style.RESET_ALL)
        print(Fore.WHITE + "   1. " + Fore.GREEN + "Настройка API" + Style.RESET_ALL)
        print(Fore.WHITE + "   2. " + Fore.GREEN + "Ввести сообщение" + Style.RESET_ALL)
        print(Fore.WHITE + "   3. " + Fore.GREEN + "Указать @username получателя" + Style.RESET_ALL)
        print(Fore.WHITE + "   4. " + Fore.GREEN + "Указать количество сообщений" + Style.RESET_ALL)
        print(Fore.WHITE + "   5. " + Fore.GREEN + "Запустить рассылку" + Style.RESET_ALL)
        print(Fore.WHITE + "   6. " + Fore.RED + "СТОП (остановить рассылку)" + Style.RESET_ALL)
        print(Fore.WHITE + "   0. " + Fore.RED + "Выход" + Style.RESET_ALL)
        print()
        
        # Показываем текущие настройки
        print(Fore.YELLOW + "⚙️ ТЕКУЩИЕ НАСТРОЙКИ:" + Style.RESET_ALL)
        print(Fore.WHITE + f"   Получатель: {Fore.CYAN}{self.target_username if self.target_username else 'не указан'}{Style.RESET_ALL}")
        print(Fore.WHITE + f"   Количество: {Fore.CYAN}{self.message_count if self.message_count > 0 else 'не указано'}{Style.RESET_ALL}")
        print(Fore.WHITE + f"   Сообщение: {Fore.CYAN}{self.message_text[:30] + '...' if len(self.message_text) > 30 else self.message_text}{Style.RESET_ALL}")
        print()
        
        choice = input(Fore.CYAN + "➜ Выберите пункт: " + Style.RESET_ALL)
        return choice

    def setup_api(self):
        """Настройка API Telegram"""
        self.clear_screen()
        print(Fore.YELLOW + "🔧 НАСТРОЙКА API" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Для работы нужны API данные из my.telegram.org" + Style.RESET_ALL)
        print()
        
        self.api_id = input(Fore.GREEN + "→ API ID: " + Style.RESET_ALL)
        self.api_hash = input(Fore.GREEN + "→ API Hash: " + Style.RESET_ALL)
        self.phone = input(Fore.GREEN + "→ Номер телефона (+7...): " + Style.RESET_ALL)
        
        self.save_config()
        print(Fore.GREEN + "\n✅ Данные сохранены!" + Style.RESET_ALL)
        time.sleep(2)

    def input_message(self):
        """Ввод сообщения для рассылки"""
        self.clear_screen()
        print(Fore.YELLOW + "📝 ВВОД СООБЩЕНИЯ" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Введите текст сообщения (END - закончить):" + Style.RESET_ALL)
        print()
        
        lines = []
        while True:
            line = input()
            if line == "END":
                break
            lines.append(line)
        
        self.message_text = "\n".join(lines)
        
        if self.message_text:
            print(Fore.GREEN + f"\n✅ Сообщение сохранено ({len(self.message_text)} символов)" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Сообщение пустое" + Style.RESET_ALL)
        
        input(Fore.WHITE + "\nНажмите Enter для продолжения..." + Style.RESET_ALL)

    def set_target(self):
        """Указать @username получателя"""
        self.clear_screen()
        print(Fore.YELLOW + "👤 УКАЗАТЬ ПОЛУЧАТЕЛЯ" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Введите @username пользователя или чата:" + Style.RESET_ALL)
        print()
        
        username = input(Fore.GREEN + "→ @" + Style.RESET_ALL)
        if username:
            self.target_username = "@" + username
            print(Fore.GREEN + f"\n✅ Получатель установлен: {self.target_username}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Username не введён" + Style.RESET_ALL)
        
        input(Fore.WHITE + "\nНажмите Enter для продолжения..." + Style.RESET_ALL)

    def set_message_count(self):
        """Указать количество сообщений"""
        self.clear_screen()
        print(Fore.YELLOW + "🔢 КОЛИЧЕСТВО СООБЩЕНИЙ" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + "Сколько сообщений отправить?" + Style.RESET_ALL)
        print()
        
        try:
            count = int(input(Fore.GREEN + "→ Количество: " + Style.RESET_ALL))
            if count > 0:
                self.message_count = count
                print(Fore.GREEN + f"\n✅ Установлено: {count} сообщений" + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n❌ Количество должно быть больше 0" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "\n❌ Введите число" + Style.RESET_ALL)
        
        input(Fore.WHITE + "\nНажмите Enter для продолжения..." + Style.RESET_ALL)

    def stop_sending(self):
        """Остановка рассылки"""
        if self.is_sending:
            self.is_sending = False
            print(Fore.RED + "\n⛔ Останавливаю рассылку..." + Style.RESET_ALL)
            time.sleep(1)
        else:
            print(Fore.YELLOW + "\n⚠️ Рассылка не запущена" + Style.RESET_ALL)
            time.sleep(1)

    async def send_messages(self):
        """Асинхронная отправка сообщений"""
        if not all([self.api_id, self.api_hash, self.phone]):
            print(Fore.RED + "❌ Сначала настройте API" + Style.RESET_ALL)
            return False
        
        if not self.message_text:
            print(Fore.RED + "❌ Введите сообщение" + Style.RESET_ALL)
            return False
        
        if not self.target_username:
            print(Fore.RED + "❌ Укажите @username получателя" + Style.RESET_ALL)
            return False
        
        if self.message_count <= 0:
            print(Fore.RED + "❌ Укажите количество сообщений" + Style.RESET_ALL)
            return False
        
        print(Fore.YELLOW + "\n⚡ Подключение к Telegram..." + Style.RESET_ALL)
        
        self.client = TelegramClient('session_' + self.phone, int(self.api_id), self.api_hash)
        await self.client.start(phone=self.phone)
        
        print(Fore.GREEN + "✅ Подключено!" + Style.RESET_ALL)
        print(Fore.YELLOW + "\n📨 Начинаю рассылку..." + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        
        try:
            # Получаем сущность получателя
            entity = await self.client.get_entity(self.target_username)
            
            self.is_sending = True
            sent_in_session = 0
            
            for i in range(self.message_count):
                if not self.is_sending:
                    print(Fore.RED + "\n⛔ Рассылка остановлена пользователем" + Style.RESET_ALL)
                    break
                
                try:
                    await self.client.send_message(entity, self.message_text)
                    sent_in_session += 1
                    self.sent_count += 1
                    self.save_stats()
                    
                    print(Fore.GREEN + f"✅ [{i+1}/{self.message_count}] Отправлено: {self.target_username}" + Style.RESET_ALL)
                    
                    # Задержка между сообщениями
                    await asyncio.sleep(1)
                    
                except errors.FloodWaitError as e:
                    wait = e.seconds
                    print(Fore.RED + f"⚠️ Flood wait: {wait} секунд" + Style.RESET_ALL)
                    await asyncio.sleep(wait)
                    
                except Exception as e:
                    print(Fore.RED + f"❌ Ошибка: {str(e)[:50]}" + Style.RESET_ALL)
                    await asyncio.sleep(2)
            
            print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
            print(Fore.GREEN + f"✅ Рассылка завершена!" + Style.RESET_ALL)
            print(Fore.WHITE + f"   Отправлено в этой сессии: {Fore.CYAN}{sent_in_session}{Style.RESET_ALL}")
            print(Fore.WHITE + f"   Всего отправлено (за всё время): {Fore.CYAN}{self.sent_count}{Style.RESET_ALL}")
            
        except Exception as e:
            print(Fore.RED + f"❌ Ошибка: {e}" + Style.RESET_ALL)
        
        await self.client.disconnect()
        self.is_sending = False
        
        input(Fore.WHITE + "\nНажмите Enter для продолжения..." + Style.RESET_ALL)
        return True

    def start_sending(self):
        """Запуск рассылки"""
        if self.is_sending:
            print(Fore.RED + "❌ Рассылка уже запущена" + Style.RESET_ALL)
            time.sleep(1)
            return
        
        self.clear_screen()
        print(Fore.YELLOW + "🚀 ЗАПУСК РАССЫЛКИ" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*60 + Style.RESET_ALL)
        print(Fore.WHITE + f"Получатель: {Fore.CYAN}{self.target_username}{Style.RESET_ALL}")
        print(Fore.WHITE + f"Количество: {Fore.CYAN}{self.message_count}{Style.RESET_ALL}")
        print(Fore.WHITE + f"Сообщение: {Fore.CYAN}{self.message_text[:50]}...{Style.RESET_ALL}")
        print()
        
        confirm = input(Fore.YELLOW + "Начать рассылку? (y/n): " + Style.RESET_ALL)
        if confirm.lower() == 'y':
            asyncio.run(self.send_messages())

    def run(self):
        """Основной цикл программы"""
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.setup_api()
            elif choice == '2':
                self.input_message()
            elif choice == '3':
                self.set_target()
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

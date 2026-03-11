import os
import sys
import time
import json
import colorama
from colorama import Fore, Back, Style
import telebot
from telethon import TelegramClient, errors
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import InputPeerChat, InputPeerChannel, InputPeerUser
import asyncio
import threading
from datetime import datetime

# Инициализация colorama
colorama.init(autoreset=True)

# Конфигурация
CONFIG_FILE = "config.json"

# Твоя вывеска (ASCII лого) - разделим на части для гарантированного отображения
LOGO_ASCII = """
╭━━━┳╮╱╱╭┳━╮╱╭┳━━━┳━━━┳━━━━┳━━━┳━━━╮
┃╭━╮┃╰╮╭╯┃┃╰╮┃┃╭━━┫╭━╮┃╭╮╭╮┃╭━━┫╭━╮┃
┃╰━━╋╮╰╯╭┫╭╮╰╯┃╰━━┫╰━━╋╯┃┃╰┫╰━━┫╰━╯┃
╰━━╮┃╰╮╭╯┃┃╰╮┃┃╭━━┻━━╮┃╱┃┃╱┃╭━━┫╭╮╭╯
┃╰━╯┃╱┃┃╱┃┃╱┃┃┃╰━━┫╰━╯┃╱┃┃╱┃╰━━┫┃┃╰╮
╰━━━╯╱╰╯╱╰╯╱╰━┻━━━┻━━━╯╱╰╯╱╰━━━┻╯╰━╯
"""

class MassSender:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.client = None
        self.message_text = ""
        self.targets = []
        self.load_config()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_logo()

    def show_logo(self):
        """Отдельный метод для гарантированного показа логотипа"""
        # Черный текст на белом фоне для первой части
        print(f"{Fore.BLACK}{Back.WHITE}{LOGO_ASCII}{Style.RESET_ALL}")
        # Добавим разделитель
        print(f"{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⚡ Массовый отправитель сообщений v1.0{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*50}{Style.RESET_ALL}\n")

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
            json.dump(config, f)

    def show_menu(self):
        """Отображение главного меню"""
        self.clear_screen()
        print(f"{Fore.BLACK}┌──────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE}           ГЛАВНОЕ МЕНЮ              {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}├──────────────────────────────────────┤{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE} 1. {Fore.GREEN}Настройка API{Fore.WHITE}                       {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE} 2. {Fore.GREEN}Ввести сообщение{Fore.WHITE}                  {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE} 3. {Fore.GREEN}Загрузить цели (чаты/группы){Fore.WHITE}      {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE} 4. {Fore.GREEN}Начать рассылку{Fore.WHITE}                   {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE} 5. {Fore.GREEN}Просмотр статистики{Fore.WHITE}               {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE} 0. {Fore.RED}Выход{Fore.WHITE}                            {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}└──────────────────────────────────────┘{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}➜ Выберите пункт: {Style.RESET_ALL}")
        return choice

    def setup_api(self):
        """Настройка API Telegram"""
        self.clear_screen()
        print(f"{Fore.BLACK}┌──────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE}          НАСТРОЙКА API              {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}└──────────────────────────────────────┘{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Для работы нужны API данные из my.telegram.org{Style.RESET_ALL}")
        print()
        
        self.api_id = input(f"{Fore.GREEN}→ API ID: {Style.RESET_ALL}")
        self.api_hash = input(f"{Fore.GREEN}→ API Hash: {Style.RESET_ALL}")
        self.phone = input(f"{Fore.GREEN}→ Номер телефона (+7...): {Style.RESET_ALL}")
        
        self.save_config()
        print(f"\n{Fore.GREEN}✅ Данные сохранены!{Style.RESET_ALL}")
        time.sleep(2)

    def input_message(self):
        """Ввод сообщения для рассылки"""
        self.clear_screen()
        print(f"{Fore.BLACK}┌──────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE}          ВВЕДИТЕ СООБЩЕНИЕ           {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}└──────────────────────────────────────┘{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}(Для завершения ввода введите END в новой строке){Style.RESET_ALL}\n")
        
        lines = []
        while True:
            line = input()
            if line == "END":
                break
            lines.append(line)
        
        self.message_text = "\n".join(lines)
        
        if self.message_text:
            print(f"\n{Fore.GREEN}✅ Сообщение сохранено ({len(self.message_text)} символов){Style.RESET_ALL}")
            print(f"\n{Fore.WHITE}Первые 100 символов:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{self.message_text[:100]}...{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ Сообщение пустое{Style.RESET_ALL}")
        
        input(f"\n{Fore.WHITE}Нажмите Enter для продолжения...{Style.RESET_ALL}")

    def load_targets(self):
        """Загрузка списка целей (чатов/групп)"""
        self.clear_screen()
        print(f"{Fore.BLACK}┌──────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE}          ЗАГРУЗКА ЦЕЛЕЙ             {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}└──────────────────────────────────────┘{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Формат: username или ссылка (каждая с новой строки){Style.RESET_ALL}")
        print(f"{Fore.WHITE}Пример:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}@channel_name{Style.RESET_ALL}")
        print(f"{Fore.CYAN}https://t.me/group_name{Style.RESET_ALL}")
        print(f"{Fore.CYAN}-1001234567890 (ID чата){Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Введите цели (END для завершения):{Style.RESET_ALL}")
        
        targets = []
        while True:
            line = input()
            if line == "END":
                break
            if line.strip():
                targets.append(line.strip())
        
        self.targets = targets
        
        if self.targets:
            print(f"\n{Fore.GREEN}✅ Загружено целей: {len(self.targets)}{Style.RESET_ALL}")
            for i, target in enumerate(self.targets[:5], 1):
                print(f"{Fore.WHITE}{i}. {Fore.CYAN}{target}{Style.RESET_ALL}")
            if len(self.targets) > 5:
                print(f"{Fore.WHITE}... и еще {len(self.targets)-5}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ Список целей пуст{Style.RESET_ALL}")
        
        input(f"\n{Fore.WHITE}Нажмите Enter для продолжения...{Style.RESET_ALL}")

    async def send_messages(self):
        """Асинхронная отправка сообщений"""
        if not all([self.api_id, self.api_hash, self.phone]):
            print(f"{Fore.RED}❌ Сначала настройте API{Style.RESET_ALL}")
            return False
        
        if not self.message_text:
            print(f"{Fore.RED}❌ Введите сообщение{Style.RESET_ALL}")
            return False
        
        if not self.targets:
            print(f"{Fore.RED}❌ Загрузите цели{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.YELLOW}⚡ Подключение к Telegram...{Style.RESET_ALL}")
        
        self.client = TelegramClient('session_' + self.phone, int(self.api_id), self.api_hash)
        await self.client.start(phone=self.phone)
        
        print(f"{Fore.GREEN}✅ Подключено!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Начинаю рассылку...{Style.RESET_ALL}\n")
        
        stats = {
            'success': 0,
            'failed': 0,
            'total': len(self.targets)
        }
        
        for i, target in enumerate(self.targets, 1):
            try:
                # Определяем тип цели
                if target.startswith('@'):
                    entity = await self.client.get_entity(target)
                elif target.startswith('https://t.me/'):
                    username = target.replace('https://t.me/', '')
                    entity = await self.client.get_entity(username)
                else:
                    # Пробуем как ID
                    entity = await self.client.get_entity(int(target))
                
                # Отправляем сообщение
                await self.client.send_message(entity, self.message_text)
                
                stats['success'] += 1
                print(f"{Fore.GREEN}✅ [{i}/{stats['total']}] Отправлено в: {target}{Style.RESET_ALL}")
                
                # Задержка между сообщениями
                await asyncio.sleep(1)
                
            except errors.FloodWaitError as e:
                wait = e.seconds
                print(f"{Fore.RED}⚠️ Flood wait: {wait} секунд{Style.RESET_ALL}")
                stats['failed'] += 1
                await asyncio.sleep(wait)
                
            except Exception as e:
                stats['failed'] += 1
                print(f"{Fore.RED}❌ [{i}/{stats['total']}] Ошибка {target}: {str(e)[:50]}{Style.RESET_ALL}")
        
        await self.client.disconnect()
        
        print(f"\n{Fore.BLACK}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Рассылка завершена!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Успешно: {Fore.GREEN}{stats['success']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Ошибок: {Fore.RED}{stats['failed']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Всего: {Fore.CYAN}{stats['total']}{Style.RESET_ALL}")
        print(f"{Fore.BLACK}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        return True

    def start_sending(self):
        """Запуск рассылки"""
        self.clear_screen()
        print(f"{Fore.BLACK}┌──────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE}          ЗАПУСК РАССЫЛКИ            {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}└──────────────────────────────────────┘{Style.RESET_ALL}\n")
        
        if not all([self.api_id, self.api_hash, self.phone]):
            print(f"{Fore.RED}❌ API не настроен{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Нажмите Enter...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.WHITE}Сообщение: {Fore.CYAN}{self.message_text[:50]}...{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Целей: {Fore.CYAN}{len(self.targets)}{Style.RESET_ALL}\n")
        
        confirm = input(f"{Fore.YELLOW}Начать рассылку? (y/n): {Style.RESET_ALL}")
        if confirm.lower() == 'y':
            asyncio.run(self.send_messages())
        
        input(f"\n{Fore.WHITE}Нажмите Enter для продолжения...{Style.RESET_ALL}")

    def show_stats(self):
        """Просмотр статистики"""
        self.clear_screen()
        print(f"{Fore.BLACK}┌──────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.BLACK}│{Fore.WHITE}          СТАТИСТИКА               {Fore.BLACK}│{Style.RESET_ALL}")
        print(f"{Fore.BLACK}└──────────────────────────────────────┘{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}API настроен: {Fore.GREEN}{bool(self.api_id)}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Сообщение: {Fore.CYAN}{len(self.message_text)} символов{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Целей загружено: {Fore.CYAN}{len(self.targets)}{Style.RESET_ALL}")
        
        if self.targets:
            print(f"\n{Fore.WHITE}Первые 5 целей:{Style.RESET_ALL}")
            for i, target in enumerate(self.targets[:5], 1):
                print(f"{Fore.CYAN}  {i}. {target}{Style.RESET_ALL}")
        
        input(f"\n{Fore.WHITE}Нажмите Enter для продолжения...{Style.RESET_ALL}")

    def run(self):
        """Основной цикл программы"""
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.setup_api()
            elif choice == '2':
                self.input_message()
            elif choice == '3':
                self.load_targets()
            elif choice == '4':
                self.start_sending()
            elif choice == '5':
                self.show_stats()
            elif choice == '0':
                self.clear_screen()
                print(f"{Fore.RED}Выход...{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Неверный выбор!{Style.RESET_ALL}")
                time.sleep(1)

if __name__ == "__main__":
    sender = MassSender()
    sender.run()

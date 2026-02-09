import logging
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors import SessionPasswordNeededError, PhoneNumberUnoccupiedError

# Настройка подробного логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from src.Data.Api import API_ID, API_HASH, phone


def main():
    client = None
    try:
        print("=" * 50)
        print("ИНИЦИАЛИЗАЦИЯ TELEGRAM CLIENT")
        print("=" * 50)

        # Создаем клиента с уникальным именем сессии
        session_name = f'session_{phone}'
        client = TelegramClient(session_name, API_ID, API_HASH)

        print("Подключаемся к серверам Telegram...")
        client.connect()

        # Проверяем, не авторизованы ли мы уже
        if not client.is_user_authorized():
            print("Требуется авторизация...")
            print(f"Отправка запроса на код для номера: {phone}")

            # Отправляем запрос на код
            client.send_code_request(phone)

            # Вводим код с подробными инструкциями
            print("\n" + "=" * 50)
            print("ПРОВЕРКА АВТОРИЗАЦИИ")
            print("=" * 50)
            code = input("Введите 5-значный код из Telegram (или SMS): ").strip()

            try:
                # Пытаемся войти с кодом
                client.sign_in(phone, code)
                print("✓ Код принят! Выполняется вход...")

            except SessionPasswordNeededError:
                print("\n🔐 Обнаружена двухфакторная аутентификация")
                password = input("Введите пароль двухфакторной аутентификации: ")
                client.sign_in(password=password)
                print("✓ Пароль принят!")

        # Проверяем окончательную авторизацию
        me = client.get_me()
        if me:
            print(f"\n✓ Успешный вход как: {me.first_name or ''} {me.last_name or ''}")
            print(f"   Username: @{me.username or 'не установлен'}")
            print(f"   ID пользователя: {me.id}")
        else:
            print("❌ Не удалось получить информацию о пользователе")
            return

        print("\n" + "=" * 50)
        print("ПОЛУЧЕНИЕ ДИАЛОГОВ")
        print("=" * 50)

        # Получаем диалоги с обработкой ошибок
        try:
            result = client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))

            # Анализируем результаты
            chats = result.chats
            users = result.users

            print(f"Найдено чатов/каналов: {len(chats)}")
            print(f"Найдено пользователей: {len(users)}")

            if chats:
                print("\nСПИСОК ЧАТОВ И КАНАЛОВ:")
                print("-" * 40)

                for i, chat in enumerate(chats[:10], 1):  # Показываем первые 10
                    chat_type = "Канал" if hasattr(chat, 'broadcast') and chat.broadcast else "Группа"
                    print(f"{i}. {chat.title} (ID: {chat.id}, Тип: {chat_type})")

                if len(chats) > 10:
                    print(f"... и еще {len(chats) - 10} чатов/каналов")

            if users:
                print(f"\nСПИСОК ПОЛЬЗОВАТЕЛЕЙ (первые 5):")
                print("-" * 40)
                for i, user in enumerate(users[:5], 1):
                    print(f"{i}. {user.first_name or ''} {user.last_name or ''} (@{user.username or 'нет'})")

            # Дополнительная информация с использованием stringify
            if chats:
                print(f"\nПОДРОБНАЯ ИНФОРМАЦИЯ О ПЕРВОМ ЧАТЕ:")
                print("-" * 50)
                first_chat = chats[0]
                print(first_chat.stringify())

        except Exception as e:
            print(f"❌ Ошибка при получении диалогов: {e}")
            logger.exception("Подробности ошибки:")

    except PhoneNumberUnoccupiedError:
        print("❌ Этот номер телефона не зарегистрирован в Telegram")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        logger.exception("Детали ошибки:")

    finally:
        if client:
            print("\n" + "=" * 50)
            print("ЗАВЕРШЕНИЕ РАБОТЫ")
            print("=" * 50)
            client.disconnect()
            print("Сессия завершена. Файл сессии сохранен для будущих использований.")


if __name__ == "__main__":
    main()
# for chat in chats:
#    try:
#        if chat.megagroup== True:
#            groups.append(chat)
#    except:
#        continue
# print('Выберите номер группы из перечня:')
# i=0
# for g in groups:
#    print(str(i) + '- ' + g.title)
#    i+=1
# g_index = input("Введите нужную цифру: ")
# target_group = groups[int(g_index)]
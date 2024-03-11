from telebot import TeleBot, types
import json
from time import sleep
from html.parser import HTMLParser

# Замените 'YOUR_TOKEN' на ваш реальный токен
bot = TeleBot(token='YOUR_TOKEN', parse_mode='html')

# Класс-парсер для определения, является ли текст HTML
class HTMLTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.is_html = False

    def handle_starttag(self, tag, attrs):
        self.is_html = True

    def handle_data(self, data):
        pass

    def handle_endtag(self, tag):
        pass

# Функция для генерации основного меню с кнопкой "Начать"
def generate_menu():
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Начать", callback_data='start')
    markup.add(start_button)

    return markup

# Функция для генерации стартового сообщения с кнопкой "Начать"
def generate_start_message():
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Начать", callback_data='start')
    markup.add(start_button)

    return 'Привет! Я умею проверять JSON и форматировать его в красивый текст. Введи JSON в виде строки или отправь файл с JSON:', markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # Получаем текст и клавиатуру для стартового сообщения
    text, markup = generate_start_message()
    # Отправляем стартовое сообщение с клавиатурой
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup
    )

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def message_handler(message: types.Message):
    try:
        # Проверяем, является ли сообщение файлом, и обрабатываем его, если да
        if message.document or message.photo or message.video or message.voice or message.audio or message.sticker or message.animation or message.video_note or message.contact or message.location or message.venue or message.dice:
            handle_media(message)
            return

        # Пытаемся обработать текстовое сообщение как JSON
        payload = json.loads(message.text)
        text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
        
        # Отправляем отформатированный JSON и основное меню с кнопками
        bot.send_message(
            chat_id=message.chat.id,
            text=f'JSON успешно проверен и отформатирован:\n<code>{text}</code>',
            reply_markup=generate_menu()
        )
    except json.JSONDecodeError:
        # В случае ошибки при распознавании JSON отправляем стикер и сообщение с ошибкой
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED_tdl7PHIkltFyCnwOH1jvXU7e2W-swAC9AADVp29ChFYsPXZ_VVJNAQ')
        
        # Добавляем обработку HTML кода
        html_parser = HTMLTextParser()
        html_parser.feed(message.text)
        if html_parser.is_html:
            bot.send_message(
                chat_id=message.chat.id,
                text='Ошибка! Введенный текст похож на HTML, пожалуйста, введите JSON.',
                reply_markup=generate_menu()
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Ошибка! Невозможно распознать JSON-код. Пожалуйста, убедитесь, что код введен корректно.',
                reply_markup=generate_menu()
            )
    except Exception as e:
        # В случае других ошибок отправляем сообщение с ошибкой и основное меню с кнопками
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Произошла ошибка при обработке запроса: {str(e)}',
            reply_markup=generate_menu()
        )

# Обработчик для файлов, отправленных пользователем
def handle_media(message: types.Message):
    # Обработка изображений
    if message.photo:
        bot.send_message(
            chat_id=message.chat.id,
            text='Это изображение! Спасибо за отправку.'
        )
    # Обработка стикеров
    elif message.sticker:
        bot.send_message(
            chat_id=message.chat.id,
            text='Это стикер! Спасибо за отправку.'
        )
    # Обработка остальных медиафайлов
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Спасибо за отправку файла!'
        )

# Обработчик нажатия на кнопку "Перезапустить"
@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def handle_restart(call: types.CallbackQuery):
    # Отправляем стикер и сообщение о перезапуске бота, а затем основное меню с кнопками
    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAED_qhl7OhYcbq65VLyLtFCzTwHEp5HtAACAgEAAladvQpO4myBy0Dk_zQE')
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Бот был перезапущен!',
        reply_markup=generate_menu()
    )

# Обработчик нажатия на кнопку "Начать"
@bot.callback_query_handler(func=lambda call: call.data == 'start')
def handle_start(call: types.CallbackQuery):
    # Отправляем стикер
    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEEB65l7zcXYTjLaiAkDTsKx66XqhljIQACTgIAAladvQow_mttgTIDbzQE')
    # Отправляем приветственное сообщение без клавиатуры
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Добро пожаловать! Введите JSON для проверки.',
        reply_markup=None
    )

# Основная функция бота с бесконечным циклом и перезапуском при ошибке
def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            # В случае ошибки при работе бота выводим сообщение об ошибке в консоль
            print(f'Ошибка при работе бота: {e}')
            # Ждем некоторое время перед повторной попыткой
            sleep(0.3)

# Запуск бота
if __name__ == '__main__':
    main()

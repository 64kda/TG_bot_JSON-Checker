from telebot import TeleBot, types
import json
import sys

bot = TeleBot(token='MY_TOKEN', parse_mode='html')

def generate_menu():
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Начать", callback_data='start')
    restart_button = types.InlineKeyboardButton("Перезапустить", callback_data='restart')
    stop_button = types.InlineKeyboardButton("Остановить", callback_data='stop')
    markup.add(start_button, restart_button, stop_button)

    return markup

def generate_start_message():
    markup = types.InlineKeyboardMarkup()
    restart_button = types.InlineKeyboardButton("Перезапустить", callback_data='restart')
    stop_button = types.InlineKeyboardButton("Остановить", callback_data='stop')
    markup.add(restart_button, stop_button)

    return 'Привет! Я умею проверять JSON и форматировать его в красивый текст. Введи JSON в виде строки или отправь файл с JSON:', markup

@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    text, markup = generate_start_message()
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def message_handler(message: types.Message):
    try:
        if message.document or message.photo or message.video or message.voice or message.audio or message.sticker or message.animation or message.video_note or message.contact or message.location or message.venue or message.dice:
            handle_file(message)
            return

        payload = json.loads(message.text)
        text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
        
        bot.send_message(
            chat_id=message.chat.id,
            text=f'JSON успешно проверен и отформатирован:\n<code>{text}</code>',
            reply_markup=generate_menu()
        )
    except json.JSONDecodeError:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED_tdl7PHIkltFyCnwOH1jvXU7e2W-swAC9AADVp29ChFYsPXZ_VVJNAQ')
        bot.send_message(
            chat_id=message.chat.id,
            text='Ошибка! Невозможно распознать JSON-код. Пожалуйста, убедитесь, что код введен корректно.',
            reply_markup=generate_menu()
        )
    except Exception as e:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Произошла ошибка при обработке запроса: {str(e)}',
            reply_markup=generate_menu()
        )

def handle_file(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Извините, в данном боте не предусмотрена обработка файлов. Пожалуйста, отправьте JSON в виде строки текста.',
        reply_markup=generate_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def handle_restart(call: types.CallbackQuery):
    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAED_qhl7OhYcbq65VLyLtFCzTwHEp5HtAACAgEAAladvQpO4myBy0Dk_zQE')
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Бот был перезапущен!',
        reply_markup=generate_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def handle_stop(call: types.CallbackQuery):
    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAED_pxl7OQjfvnoDPpYaYzmF8l_46wgWwACDgEAAladvQoRqS1ownHgaDQE')
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Бот был остановлен.',
        reply_markup=generate_menu()
    )
    sys.exit()

@bot.callback_query_handler(func=lambda call: call.data == 'start')
def handle_start(call: types.CallbackQuery):
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Добро пожаловать! Введите JSON для проверки.',
        reply_markup=None
    )

def main():
    bot.send_message(chat_id='319922443', text='Выберите действие:', reply_markup=generate_menu())
    bot.infinity_polling()

if __name__ == '__main__':
    main()

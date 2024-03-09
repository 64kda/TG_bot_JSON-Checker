from telebot import TeleBot, types
import json
import sys

bot = TeleBot(token='6565554022:AAGSEH0gFLzRd_3hbRiYke0qnBiMCkvEwUI', parse_mode='html')

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
        
        # Добавлено сообщение об успешной обработке кода JSON
        bot.send_message(
            chat_id=message.chat.id,
            text=f'JSON успешно проверен и отформатирован:\n<code>{text}</code>'
        )
    except json.JSONDecodeError:
        # Стикер при ошибке распознавания JSON-кода
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED_tdl7PHIkltFyCnwOH1jvXU7e2W-swAC9AADVp29ChFYsPXZ_VVJNAQ')
        # Сообщение об ошибке, если JSON-код не может быть распознан
        bot.send_message(
            chat_id=message.chat.id,
            text='Ошибка! Невозможно распознать JSON-код. Пожалуйста, убедитесь, что код введен корректно.'
        )
    except Exception as e:
        # Сообщение об ошибке в случае других ошибок
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Произошла ошибка при обработке запроса: {str(e)}'
        )

def handle_file(message: types.Message):
    # Сообщение об ошибке при отправке файла
    bot.send_message(
        chat_id=message.chat.id,
        text='Извините, в данном боте не предусмотрена обработка файлов. Пожалуйста, отправьте JSON в виде строки текста.'
    )

@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def handle_restart(call: types.CallbackQuery):
    # ваш код обработки команды restart
    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAED_qhl7OhYcbq65VLyLtFCzTwHEp5HtAACAgEAAladvQpO4myBy0Dk_zQE')  # отправка нового стикера
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Бот был перезапущен!'
    )
    pass  # этот pass всегда можно заменить реальным кодом

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def handle_stop(call: types.CallbackQuery):
    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAED_pxl7OQjfvnoDPpYaYzmF8l_46wgWwACDgEAAladvQoRqS1ownHgaDQE')  # отправка стикера
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Бот был остановлен.'
    )
    # Завершаем выполнение программы
    sys.exit()

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()

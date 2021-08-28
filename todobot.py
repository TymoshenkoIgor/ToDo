import telebot
from pathlib import Path

bot = telebot.TeleBot('<<Your Token>>')
filename = Path("/path/to/your/file.txt")

# Handler for /add coomand, witch add todo command to file


@bot.message_handler(commands=['add'])
def add_command(message):
    bot.send_message(message.chat.id, text='Введіть назву завдання')
    bot.register_next_step_handler(message, add_todo)

# Check if file exists and create a file if false or add a todo to the end of the file if true


def add_todo(message):
    if filename.is_file():
        fle = open(filename, 'a')
        fle.write(","+message.text)
        fle.close()
        bot.send_message(message.chat.id, text=message.text+' Завдання додано')
        bot.register_next_step_handler(message, get_text_message)
    else:
        bot.send_message(
            message.chat.id, text='Файл створено, додайте перше завдання')
        fle = open(filename, 'w')
        fle.write(message.text)
        fle.close()
        bot.send_message(message.chat.id, text=message.text+' Завдання додано')
        bot.register_next_step_handler(message, get_text_message)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    # Read todo list from the file
    if filename.is_file():
        with open(filename, 'r') as file:
            for line in file:
                ans_data = line.strip().split(',')

        # Create inline feys for todo
        markup = telebot.types.InlineKeyboardMarkup()
        if (len(ans_data) % 2) == 0:
            for i in range(0, len(ans_data)-1, 2):
                markup.add(telebot.types.InlineKeyboardButton(text=str(ans_data[i]), callback_data=str(ans_data[i])),
                           telebot.types.InlineKeyboardButton(text=str(ans_data[i+1]), callback_data=str(ans_data[i+1])))
            bot.send_message(message.chat.id, text=message.text,
                             reply_markup=markup)
        else:
            for i in range(0, len(ans_data)-1, 2):
                markup.add(telebot.types.InlineKeyboardButton(text=str(ans_data[i]), callback_data=str(ans_data[i])),
                           telebot.types.InlineKeyboardButton(text=str(ans_data[i+1]), callback_data=str(ans_data[i+1])))
            markup.add(telebot.types.InlineKeyboardButton(text=str(
                ans_data[len(ans_data)-1]), callback_data=str(ans_data[len(ans_data)-1])))
            bot.send_message(message.chat.id, text=message.text,
                             reply_markup=markup)
    else:
        bot.register_next_step_handler(add_command)
# Mark message with a choosen todo


@bot.callback_query_handler(func=lambda call: True)
def query_handdler(call):
    valueCallback = str(call.data)
    bot.send_message(call.message.chat.id,
                     text=call.message.text + " " + valueCallback)


bot.polling(none_stop=True, interval=0)

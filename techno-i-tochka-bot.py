import openpyxl
import telebot
from telebot import types

bot = telebot.TeleBot('6835896919:AAFOgrmeuuGGBWogym_aU5sqsHHseN-ay6Y')
channel_id = "-1001371818863"
excel_file_path = "products.xlsx"

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    send_post_button = types.KeyboardButton('📢Отправить пост')
    show_template_button = types.KeyboardButton('Показать шаблон')
    update_template_button = types.KeyboardButton('🔄Обновить шаблон')
    markup.add(send_post_button)
    markup.add(update_template_button, show_template_button)
    bot.send_message(message.chat.id, f"Здравствуйте!\nЧтобы начать работу отправьте <b>excel</b> файл.\nВведите <b>/help</b> для более подробной информации", parse_mode='html', reply_markup=markup)
    user_data[message.chat.id] = {'products': [], 'medias': [], 'itera': 0}

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Чтобы создать пост отправьте excel файл с данными. После чего отправьте фото к посту и затем нажмите 📢<b>Отправить пост</b>. Бот будет запрашивать фото столько раз сколько кол-во строк в excel файле с данными о товарах.\n📢<b>Отправить пост</b> - Отправляет пост в канал, если есть excel данные и фото\n<b>Показать шаблон</b> - Показывает текущий шаблон поста\n🔄<b>Обновить шаблон</b> - создать новый шаблон для постов\n<b>/delete_history</b> - сбросить данные екселя и о картинках", parse_mode='html')

def read_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    data = []
    header = [cell.value for cell in sheet[1]]  # Получаем заголовки
    for row in sheet.iter_rows(min_row=2, values_only=True):
        product = dict(zip(header, row))
        data.append(product)
    return data

@bot.message_handler(func=lambda message: message.text == 'Показать шаблон')
def show_template(message):
    with open(f'text.txt', 'r', encoding="utf8") as template:
        post_text = ''
        for char in template:
            post_text += char
        post_text = post_text.replace(r'\n', '\n')
        bot.send_message(message.chat.id, post_text)
    
@bot.message_handler(func=lambda message: message.text == '🔄Обновить шаблон')
def change_template(message):
    bot.send_message(message.chat.id, f"Напишите новый шаблон для постов", parse_mode='markdown')
    bot.register_next_step_handler(message, update_template)

def update_template(message):
    try:
        new_templ = message.text
        new_templ = new_templ.replace('\n', '\\n')
        filename = f"text.txt"
        with open(filename, 'w', encoding="utf8") as templ:
            templ.write(new_templ)
        bot.send_message(message.chat.id, f"✅Шаблон успешно обновлён", parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['delete_history'])
def delete_history(message):
    try:
        user_data[message.chat.id]['products'] = []
        user_data[message.chat.id]['medias'] = []
        user_data[message.chat.id]['itera'] = 0
        bot.send_message(message.chat.id, f"✅🗑История очищена!", parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        temp_file_path = "temp.xlsx"
        with open(temp_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        global products
        user_data[message.chat.id]['products'] = read_excel(temp_file_path)
        bot.send_message(message.chat.id, f"Данные сохранены, отправьте картинки для товара {user_data[message.chat.id]['products'][user_data[message.chat.id]['itera']]['Название товара']}:")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(func=lambda message: message.text == '📢Отправить пост')
def send_post(message):
    user_id = message.chat.id
    if len(user_data[user_id]['products']) == 0:
        bot.send_message(user_id, f"Отстутсвуют данные excel файла")
    elif len(user_data[user_id]['medias']) == 0:
        bot.send_message(user_id, f"Вы не отправили картинки")
    else:
        with open('text.txt', 'r', encoding="utf8") as text:
            post_text = ''
            for char in text:
                post_text += char

        current_product = user_data[user_id]['products'][user_data[user_id]['itera']]
            
        if current_product['Гарантия'] == None:
            garant_i = post_text.index("Гарантия")
            start = post_text.find(r"\nГарантия")
            end = post_text.find(r"\n", garant_i, len(post_text) - 1) + 2
            post_text = post_text.replace(post_text[start:end], "")
        
        if current_product['Цена со скидкой'] == None:
            discount_i = post_text.index("При Оплате")
            start = post_text.find(r"\nПри Оплате")
            end = post_text.find(r"\n", discount_i, len(post_text) - 1) - 1
            post_text = post_text.replace(post_text[start:end], "")

        post_text = post_text.replace(r"\n", "\n")
        user_data[user_id]['medias'][0].caption = post_text.format(
            Название_товара=current_product['Название товара'],
            Цена=current_product['Цена'],
            Цена_со_скидкой=current_product['Цена со скидкой'],
            Гарантия=current_product['Гарантия'],
            Адрес=current_product['Адрес']
        )
        bot.send_media_group(channel_id, user_data[user_id]['medias'])
        user_data[user_id]['medias'] = []

        if user_data[user_id]['itera'] == len(user_data[user_id]['products']) - 1:
            user_data[user_id]['itera'] = 0
            user_data[user_id]['products'] = []
        else:
            user_data[user_id]['itera'] += 1
            bot.send_message(user_id, f"Отправьте картинки для товара <u>{user_data[user_id]['products'][user_data[user_id]['itera']]['Название товара']}</u>")

# def work_with_photo(message):
#     user_id = message.chat.id
#     if message.photo:
#         handle_photo(user_id, message)
#     else:
#         bot.send_message(user_id, "Вы не отправили картинку. Повторите отправку файла снова.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        user_id = message.chat.id
        photo_id = message.photo[-1].file_id
        user_data[user_id]['medias'].append(telebot.types.InputMediaPhoto(photo_id)) 
        bot.send_message(user_id, "Картинка добавлена")
    except Exception as e:
        bot.send_message(user_id, f"Произошла ошибка: {str(e)}")
    

if __name__ == "__main__":
    bot.polling(none_stop=True)
# import time
# import telebot
# from telebot import types

# # Укажите ваш токен бота
# TOKEN = '6835896919:AAFOgrmeuuGGBWogym_aU5sqsHHseN-ay6Y'
# bot = telebot.TeleBot(TOKEN)
# lst = []

# @bot.message_handler(content_types=['photo'])
# def handle_photo(message):
#     # Получаем идентификатор чата и идентификатор фотографии
#     chat_id = "-1001371818863"
    
#     photo_id = message.photo[-1].file_id
#     global lst

#     # Отправляем фотографию обратно пользователю
#     while message.photo:
#         time.sleep(5)
#         lst.append(photo_id)

#     bot.send_photo(chat_id, photo_id)
#     print(message.photo[-1].file_id)
#     print(type(message.photo))

# # Запускаем бота
# bot.polling(none_stop=True)



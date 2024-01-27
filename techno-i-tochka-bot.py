import time
import openpyxl
import telebot
from telebot import types

bot = telebot.TeleBot('6835896919:AAFOgrmeuuGGBWogym_aU5sqsHHseN-ay6Y')
channel_id = "-1001371818863"
excel_file_path = "products.xlsx"

products = []
medias = []
itera = 0
template = f"🎄ТЕХНО И ТОЧКА\n\n{products[itera]['Имя']} {products[itera]['Модель']}, {products[itera]['Цвет']} - {products[itera]['Цена']}руб\n\nПри Оплате Наличкой Скидка -5%\n\nГарантия 1 Год С Момента Выдачи Товара Клиенту\n\nДоступен К Покупке 🛍\n\n🟠 Не Забудь Подписаться И Поделится С Друзьями !!! ‼️\n[Канал](https://t.me/tehnomarik)\n\n🟠Пр.Строителей 98 ✅"

def read_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    data = []
    header = [cell.value for cell in sheet[1]]  # Получаем заголовки
    for row in sheet.iter_rows(min_row=2, values_only=True):
        product = dict(zip(header, row))
        data.append(product)

    return data

def update_template(post):
     

def post_text(productd):
    
    return 

# def send_post_with_photo(product, photo):
#     post_text = create_post_text(product)
#     bot.send_photo(channel_id, photo, caption=post_text, parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_posts = types.KeyboardButton('Добавить посты')
    send_post_button = types.KeyboardButton('Отправить пост')
    markup.add(add_posts)
    markup.add(send_post_button)
    bot.send_message(message.chat.id, f"Здравсвуйте!", parse_mode='markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Добавить посты')
def posts_handler(message):
    bot.send_message(message.chat.id, f"Пожалуйста, отправьте <b>excel</b> файл с данными:", parse_mode='html')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        temp_file_path = "temp.xlsx"
        with open(temp_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        global products
        products = read_excel(temp_file_path)
        bot.send_message(message.chat.id, f"Пожалуйста, отправьте картинки для поста:")

        # bot.register_next_step_handler(message, work_with_photo(message))
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Отправить пост')
def send_post(message):
    global medias
    global products
    global itera
    if (len(medias) == 0):
        bot.send_message(message.chat.id, f"Вы не отправили картинки")
    elif (len(products) == 0):
        bot.send_message(message.chat.id, f"Отстутсвуют данные excel файла")
    else:
        medias[0].caption = post_text(products[itera])
        bot.send_media_group(channel_id, medias)
        medias = []
        if itera == len(products) - 1:
            itera = 0
            products = []

        else:
            itera += 1
            bot.send_message(message.chat.id, f"Отправьте картинки для товара {products[itera]['Имя']}")

def work_with_photo(message):
    if message.photo:
        handle_photo(message)
    else:
        bot.send_message(message.chat.id, "Вы не отправили картинку. Повторите отправку файла снова.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
                # bot.send_message(message.chat.id, f"Пожалуйста, отправьте картинку для поста:")

                # photo_message = bot.polling('photo', timeout=300)  # Ожидаем ответа с картинкой не более 5 минут
                # time.sleep(20)
                # print(message)
                #     photo_info = message.photo[-1]
                #     photo_file = bot.get_file(photo_info.file_id)

                #     downloaded_photo = bot.download_file(photo_path)
                #     temp_photo_path = "temp_photo.jpg"

                #     with open(temp_photo_path, 'wb') as new_photo_file:
                #         new_photo_file.write(downloaded_photo)
                #     bot.send_photo(channel_id, temp_photo_path, caption=post_text(product), parse_mode='Markdown')
                # elif content.startswith("!"):
                    global medias
                    global itera
                    # medias = []
                    photo_id = message.photo[-1].file_id  # Берем самую большую картинку
                    print(photo_id)
                        # photo_file = bot.get_file(photo_info.file_id)
                        # photo_path = photo_file.file_path
                        # print(photo_path)

                        # downloaded_photo = bot.download_file(photo_path)
                        # temp_photo_path = "temp_photo.jpg"

                        # with open(temp_photo_path, 'wb') as new_photo_file:
                        #     new_photo_file.write(downloaded_photo)
                        # print(temp_photo_path)  
                    # , caption=post_text(products[itera])
                    medias.append(telebot.types.InputMediaPhoto(photo_id))
                    print(medias)
                    print(len(medias))

                
                    bot.send_message(message.chat.id, "Картинка добавлена")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# if (len(medias) > 0):
    

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



import openpyxl
import telebot

bot = telebot.TeleBot('6835896919:AAFOgrmeuuGGBWogym_aU5sqsHHseN-ay6Y')
channel_id = "-1001371818863"
excel_file_path = "products.xlsx"

# Обработчик для отслеживания состояния пользователя
user_states = {}

# Переменная для хранения списка продуктов
products = []

def read_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    data = []
    header = [cell.value for cell in sheet[1]]  # Получаем заголовки
    for row in sheet.iter_rows(min_row=2, values_only=True):
        product = dict(zip(header, row))
        data.append(product)

    return data

def create_post_text(product):
    return f"🎄ТЕХНО И ТОЧКА\n\n{product['Имя']} {product['Модель']}, {product['Цвет']} - {product['Цена']}руб\n\nПри Оплате Наличкой Скидка -5%\n\nГарантия 1 Год С Момента Выдачи Товара Клиенту\n\nДоступен К Покупке 🛍\n\n🟠 Не Забудь Подписаться И Поделится С Друзьями !!! ‼️\n[Канал](https://t.me/tehnomarik)\n\n🟠Пр.Строителей 98 ✅"

def send_post_with_photo(product, photo, user_id):
    post_text = create_post_text(product)
    bot.send_photo(channel_id, photo, caption=post_text, parse_mode='Markdown')

    # Если есть еще продукты в списке, продолжаем ожидать следующую картинку
    if user_states.get(user_id):
        bot.send_message(user_id, f"Пожалуйста, отправьте следующую картинку для поста:")
    else:
        # Если продукты закончились, завершаем ожидание
        bot.send_message(user_id, "Все данные успешно обработаны и отправлены в канал.")

# Обработчик документов
@bot.message_handler(content_types=['document'])
def handle_document(message):
    global products  # Добавляем эту строку

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        temp_file_path = "temp.xlsx"
        with open(temp_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        products = read_excel(temp_file_path)
        
        # Устанавливаем состояние пользователя
        user_states[message.from_user.id] = 'waiting_for_photo'
        
        bot.send_message(message.chat.id, f"Пожалуйста, отправьте картинку для поста:")

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_photo')
def handle_photo_caption(message):
    try:
        if message.photo:
            photo_info = message.photo[-1]  # Берем самую большую картинку
            photo_file = bot.get_file(photo_info.file_id)
            photo_path = photo_file.file_path

            downloaded_photo = bot.download_file(photo_path)
            temp_photo_path = "temp_photo.jpg"

            with open(temp_photo_path, 'wb') as new_photo_file:
                new_photo_file.write(downloaded_photo)

            product = products.pop(0)  # Берем следующий продукт из списка
            send_post_with_photo(product, open(temp_photo_path, 'rb'), message.from_user.id)

        else:
            bot.send_message(message.chat.id, "Вы не отправили картинку. Повторите отправку файла снова.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True, interval=0)

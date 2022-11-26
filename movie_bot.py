import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import random

bot = telebot.TeleBot('5655969165:AAHxQ9qyZLJfcYhZSriBeYaxQM37gifRgCA')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    movies = types.KeyboardButton('Фильм')
    serial = types.KeyboardButton('Сериал')
    markup.add(movies, serial)
    mess = f'Рад приветствовать Вас, <b><u>{message.from_user.first_name}</u></b>!\nВыберите что Вы желаете посмотреть фильм или сериал.'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def starttext(message):
    if message.chat.type == 'private':
        if message.text == 'Фильм':
            movmess = f'<b><u>{message.from_user.first_name}</u></b>, выберите жанр фильма для просмотра, нажав соответствующую кнопку под данным сообщением.'    
            markup = types.InlineKeyboardMarkup(row_width=3)
            genre1 = types.InlineKeyboardButton("Детектив", callback_data='movdet')
            genre2 = types.InlineKeyboardButton("Боевик", callback_data='movact')
            genre3 = types.InlineKeyboardButton("Комедия", callback_data='movcom')
            genre4 = types.InlineKeyboardButton("Ужасы", callback_data='movhor')
            genre5 = types.InlineKeyboardButton("Триллер", callback_data='movthr')
            genre6 = types.InlineKeyboardButton("Драма", callback_data='movdr')
            markup.add(genre1, genre2, genre3, genre4, genre5, genre6)
            bot.send_message(message.chat.id, movmess, parse_mode='html', reply_markup=markup)   

        elif message.text == 'Сериал':
            sermess = f'<b><u>{message.from_user.first_name}</u></b>, выберите жанр сериала для просмотра, нажав соответствующую кнопку под данным сообщением.'    
            markup = types.InlineKeyboardMarkup(row_width=3)
            genre1 = types.InlineKeyboardButton("Детектив", callback_data='serdet')
            genre2 = types.InlineKeyboardButton("Боевик", callback_data='seract')
            genre3 = types.InlineKeyboardButton("Комедия", callback_data='sercom')
            genre4 = types.InlineKeyboardButton("Ужасы", callback_data='serhor')
            genre5 = types.InlineKeyboardButton("Триллер", callback_data='serthr')
            genre6 = types.InlineKeyboardButton("Драма", callback_data='serdr')
            markup.add(genre1, genre2, genre3, genre4, genre5, genre6)
            bot.send_message(message.chat.id, sermess, parse_mode='html', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Я не понимаю эту команду. Выполняйте мои инструкции. Выберите раздел "Фильм" или "Сериал", нажав соответствующую кнопку внизу.')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:

            def choice_video(video, number, url):          
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                section = soup.find_all("div", class_="ratings_list movieList grid_cell9")
                for movies in section:
                    movie = movies.find_all("div", class_="movieItem_info")
                    for item in movie:
                        movie_position = item.find("span", class_="movieItem_position").get_text(strip=True)
                        if movie_position == number:
                            movie_position = int(movie_position)
                            for item[movie_position-1] in movie:
                                movie_name = item.find("a", class_="movieItem_title").get_text(strip=True)
                                movie_info = item.find("span", class_="movieItem_year").get_text(strip=True)
                                movie_rating = item.find("span", class_="rating_num").get_text(strip=True)
                                movie_link = item.find("a", class_="movieItem_title").get("href")
                                if video == 'movie':
                                    recommended_movie = f'{movie_name}\nГод и страна производства: {movie_info}\nРейтинг фильма: {movie_rating}\nПодробнее о фильме: {movie_link}'                           
                                    
                                elif video == 'series':
                                    recommended_movie = f'{movie_name}\nГод и страна производства: {movie_info}\nРейтинг сериала: {movie_rating}\nПодробнее о сериале: {movie_link}'
                                
                                markup = types.InlineKeyboardMarkup(row_width=1)
                                yes = types.InlineKeyboardButton('Нажмите, если одобряете выбор', callback_data='yes')
                                no = types.InlineKeyboardButton('Нажмите, если недовольны выбором', callback_data='no')
                                markup.add(yes, no)
                                bot.send_message(call.message.chat.id, recommended_movie, reply_markup=markup)
                                break

            if call.data == 'movdet':
                video = 'movie'
                number = str(random.randint(1, 36))
                url = "https://www.kinoafisha.info/rating/movies/detective/"
                choice_video(video, number, url)
            
            elif call.data == 'movact':
                video = 'movie'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/movies/action/"
                choice_video(video, number, url)
                

            elif call.data == 'movcom':
                video = 'movie'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/movies/comedy/"
                choice_video(video, number, url)
            
            
            elif call.data == 'movhor':
                video = 'movie'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/movies/horror/"
                choice_video(video, number, url)
            
            
            elif call.data == 'movthr':
                video = 'movie'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/movies/thriller/"
                choice_video(video, number, url)


            elif call.data == 'movdr':
                video = 'movie'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/movies/drama/"
                choice_video(video, number, url)


            elif call.data == 'serdet':
                video = 'series'
                number = str(random.randint(1, 71))
                url = "https://www.kinoafisha.info/rating/series/detective/"
                choice_video(video, number, url)

            
            elif call.data == 'seract':
                video = 'series'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/series/action/"
                choice_video(video, number, url)


            elif call.data == 'sercom':
                video = 'series'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/series/comedy/"
                choice_video(video, number, url)

            
            elif call.data == 'serhor':
                video = 'series'
                number = str(random.randint(1, 50))
                url = "https://www.kinoafisha.info/rating/series/horror/"
                choice_video(video, number, url)

            
            elif call.data == 'serthr':
                video = 'series'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/series/thriller/"
                choice_video(video, number, url)


            elif call.data == 'serdr':
                video = 'series'
                number = str(random.randint(1, 100))
                url = "https://www.kinoafisha.info/rating/series/drama/"
                choice_video(video, number, url)
            
            elif call.data == 'yes':
                mess = f'Я очень рад. Желаю приятного просмотра.'
                bot.send_message(call.message.chat.id, mess, parse_mode='html')
                                        
            elif call.data == 'no':
                mess = f'Давайте попробуем еще раз. Выберите раздел "Фильм" или "Сериал", нажав соответствующую кнопку внизу.'
                bot.send_message(call.message.chat.id, mess, parse_mode='html')

    except Exception as e:
        print(repr(e))        



bot.polling(none_stop=True)
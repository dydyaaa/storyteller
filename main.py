import geocoding, weather, prompt, gigachat, threading, time

city = input('Введите название города: ')

mesage = '''Выбере жанр: 
1. Drama   4. Comedy
2. Musical 5. Detective 
3. Action  6. Horror
Введите цифру: '''

genre_id = input(mesage)
genre_key = {1: 'Drama',
      2: 'Musical',
      3: 'Action',
      4: 'Comedy',
      5: 'Detective',
      6: 'Horror'}
genre = genre_key[int(genre_id)]

simbols = input('Введите максимальное количество символов в рассказе: ')

coord = geocoding.geocoding(city)
weather_ = weather.get_weather(coord)
prompt_ = prompt.make_prompt(city, genre, simbols, weather_)

def fetch_gigachat_content():
    filename = 'gigachat_output.txt'
    start = time.time()
    gigachat_content = gigachat.gigachat_answer(prompt_)
    stop = time.time()
    with open('gigachat_output.txt', 'w', encoding='utf-8') as file:
        file.write(gigachat_content)
    print(f'Модель Gigachat, время ответа: {stop - start}, ответ записан в файл {filename}')

def fetch_gigachat_content_2():
    filename = 'gigachat_output_2.txt'
    start = time.time()
    gigachat_content_2 = gigachat.gigachat_answer(prompt_)
    stop = time.time()
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(gigachat_content_2)
    print(f'Модель Gigachat_2, время ответа: {stop - start}, ответ записан в файл {filename}')

thread1 = threading.Thread(target=fetch_gigachat_content)
thread2 = threading.Thread(target=fetch_gigachat_content_2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
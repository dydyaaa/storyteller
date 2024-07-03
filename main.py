import geocoding, weather, prompt, gigachat, yandexgpt
import threading, time, os

def get_city() -> str:
    """
    Запрашивает у пользователя ввод названия города и возвращает его.
    """
    return input('Введите название города: ')

def get_genre() -> str:
    """
    Запрашивает у пользователя выбор жанра из предложенного списка и возвращает его.
    Возвращает выбранный жанр в виде строки.
    """
    # Словарь для сопоставления номера жанра с его названием
    mesage = '''Выберите жанр: 
1. Драма     4. Комедия
2. Мюзикл    5. Детектив 
3. Экшн      6. Ужасы
Введите номер жанра: '''
    
    genre_key = {1: 'Драма',
                 2: 'Мюзикл',
                 3: 'Экшн',
                 4: 'Комедия',
                 5: 'Детектив',
                 6: 'Ужасы'}
    
    # Бесконечный цикл для проверки корректности ввода
    while True:
        try:
            genre_id = int(input(mesage))
            return genre_key[genre_id]
        except (ValueError, KeyError):
            print('Пожалуйста, выберите жанр из списка, введя номер от 1 до 6.')

def get_simbols() -> int:
    """
    Запрашивает у пользователя ввод максимального количества символов для рассказа и возвращает его.
    Возвращает число символов в виде целого числа.
    """
    # Бесконечный цикл для проверки корректности ввода
    while True:
        try:
            return int(input('Введите максимальное количество символов в рассказе: '))
        except ValueError:
            print('Пожалуйста, введите число.')

def create_answers_directory():
    """
    Создает директорию 'answers', если она не существует.
    """
    if not os.path.exists('answers'):
        os.makedirs('answers')

folder_path = 'answers'

def fetch_gigachat_content(prompt_: str):
    """
    Запрашивает ответ у модели Gigachat и сохраняет его в файл 'gigachat_output.txt'.
    Также выводит время выполнения запроса.
    """
    start = time.time() # Засекаем время начала выполнения запроса
    gigachat_content = gigachat.gigachat_answer(prompt_) # Получаем ответ от модели
    stop = time.time() # Засекаем время окончания выполнения запроса

    files = os.listdir(folder_path)
    answer_files = [f for f in files if f.startswith('gigachat_output_')]

    if answer_files:
        # Находим имя последнего файла и формируем новое
        last_file = max(answer_files) 
        last_file = f'{last_file[:-5]}{(int(last_file[-5]) + 1)}{last_file[-4:]}'
    else:
        last_file = 'gigachat_output_1.txt'
    
    with open(f'{folder_path}/{last_file}', 'w', encoding='utf-8') as file:
        file.write(gigachat_content)
    print(f'Модель Gigachat\nВремя ответа: {round((stop - start), 2)} сек.\nОтвет записан в файл {last_file}')

def fetch_yandexgpt_content(prompt_: str):
    """
    Запрашивает ответ у модели YandexGPT и сохраняет его в файл 'yandexgpt_output.txt'.
    Также выводит время выполнения запроса.
    """
    start = time.time() # Засекаем время начала выполнения запроса
    yandexgpt_content = yandexgpt.yandexgpt_answer(prompt_) # Получаем ответ от модели
    stop = time.time() # Засекаем время окончания выполнения запроса

    files = os.listdir(folder_path)
    answer_files = [f for f in files if f.startswith('yandexgpt_output_')]

    if answer_files:
        # Находим имя последнего файла и формируем новое
        last_file = max(answer_files)
        last_file = f'{last_file[:-5]}{(int(last_file[-5]) + 1)}{last_file[-4:]}'
    else:
        last_file = 'yandexgpt_output_1.txt'
    
    with open(f'{folder_path}/{last_file}', 'w', encoding='utf-8') as file:
        file.write(yandexgpt_content)
    print(f'Модель YandexGPT\nВремя ответа: {round((stop - start), 2)} сек.\nОтвет записан в файл {last_file}')

def main():
    create_answers_directory()

    while True:
        # Получаем данные для генерации помпта
        city = get_city()
        genre = get_genre()
        simbols = get_simbols()
        
        print('Пожалуйста, подождите. Ответ генерируется.')

        coord = geocoding.geocoding(city)
        if coord == 'Город не найден':
            return 'Город не найден.'
        
        weather_ = weather.get_weather(coord)
        prompt_ = prompt.make_prompt(city, genre, simbols, weather_)
        
        # Создаем два потока для параллельного запроса в две модели
        thread1 = threading.Thread(target=fetch_gigachat_content, args=(prompt_,))
        thread2 = threading.Thread(target=fetch_yandexgpt_content, args=(prompt_,))
        
        # Запускаем потоки
        thread1.start()
        thread2.start()
        
        # Дожидаемся окончания работы потоков
        thread1.join()
        thread2.join()

        repeat = input('Хотите выполнить еще один запрос? (да/нет): ')
        if repeat.lower() != 'да':
            break

if __name__ == '__main__':
    main()
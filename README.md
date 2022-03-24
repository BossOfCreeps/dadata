## Запуск в docker  
`docker-compose up --build`  
В переменных среды `web` есть параметр `PARSE_CSV`, который отвечает за то, будет ли распаковываться файл `city.csv` в БД или нет. Чтобы пропустить распаковку значение должно быть `0`, `False` или `No`

## Для занесения городов в бд использовать команду  
`python3 manage.py parse_to_db city.csv`

## Команда для тестов  
`python3 manage.py test`  
Однако для тестов веб-страницы (selenium) необходимо запустить приложение командой `python3 manage.py runserver --insecure` и загрузить в БД данные `test_data/test_city.csv` (от том как занести см. пункт выше). Так происходит из-за того, что selenium, в отличии от TestCase, нужен работающий сервер с подготовленными данными. Кроме это необходим [веб-драйвер](https://chromedriver.chromium.org/downloads).
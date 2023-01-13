# PyGolf

2D-гольф с поддержкой локального мультиплеера и редактором карт.

## Установка

~~Вы можете [скачать](https://github.com/igorechek06/PyGolf/releases) исполняемый файл из релизов в GitHub.~~

Пока не можете

## Запуск

### Запуск игры

1. Зайдите в папку с игрой

    ```sh
    cd game
    ```

2. Установите зависимости

    2.1 Глобально

    ```sh
    pip install -r requirements.txt -U
    ```

    2.1 Локально (с помощью poetry)

    ```sh
    poetry install
    ```

3. Запуск

    3.1 При установке зависимостей глобально

    ```sh
    python app.py
    ```

    3.2 При установке с помощью poetry

    ```sh
    poetry run python app.py
    ```

### Запуск сервера

1. Зайдите в папку с сервером

    ```sh
    cd server
    ```

2. Настройте переменные виртуального окружения

    Скопируйте шаблон файла перемен виртуального окружения

    ```sh
    cp sample.env .env
    ```

    Заполните пустые переменные окружения

    ```sh
    nano env.env
    ```

3. Запустите сервер с помощью Docker compose

    ```sh
    docker compose up --build -d
    ```

4. Запустите клиент с указанием другого веб сервера

    Вместо <https://example.com> укажите ссылку на веб сервер

    ```sh
    URL="https://example.com" python app.py
    ```

## Лицензия

Данный проект распространяется под лицензией [GPL версии 3.0](https://github.com/igorechek06/PyGolf/blob/master/LICENSE)

# Vizitka Bot
## Установка

1. Убедитесь, что у вас установлен Python3.9 и pip3
2. [Установите poetry](https://python-poetry.org/docs/#installation)
3. Склонируйте репозиторий и перейдите в папку с кодом
4. Убедитесь, что poetry использует для окружения Python3.9
    ```
    poetry env use <YOUR_PYTHON3.9_PATH> 
    ```
5. Установите зависимости
    ```
    poetry install --no-dev
    ```
    если вам необходимы различные инстурменты разработки, то уберите `--no-dev`

6. Для полноценного запуска бота понадобится создание файла `secret.py` c переменной `TOKEN`, в которой будет храниться ключ телеграм бота и добавление базы данных
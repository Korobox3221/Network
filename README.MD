
### Social Network
### Автор: Константин Коробейников

Прототип социальной сети. Функционал включает создание и просмотр постов, систему "лайков", возможность подписки/отписки на других пользователей. Используется пагинация и транзакции с базой данных.

**Ключевые технологии:** Django, JavaScript, ORM.



1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Korobox3221/Network.git
    cd network
    ```
2.  **Установите зависимости:**
    ```bashcd
    pip install -r requirements.txt
    ```
3.  **Примените миграцию базы данных:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4.  **Создайте суперпользователя (необязательно):**
    ```bash
    python manage.py createsuperuser
    ```
5.  **Запустите сервер для разработки:**
    ```bash
    python manage.py runserver
    ```

Приложение будет запущено на `http://127.0.0.1:8000/`.

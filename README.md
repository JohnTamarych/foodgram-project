# foodgram-project
foodgram-project

# Сайт:
http://84.201.163.159:8084/

# о чём проект:
Проект **Foodgram** это продукторый помошник, который помогает создавать рецептры,
делиться ими и подбирать нужные ингредиенты.

# что нужно иметь, чтобы его запустить:
Docker: https://docs.docker.com/engine/install/ubuntu automatic! 
Docker-compose: https://docs.docker.com/compose/install automatic!

# установка окружения:
1) необходимо скопировать локально репозиторий проекта
2) создать в рабочей директории файл `.env`
3) заполнить файл `.env`

# как запустить и как увидеть, что проект работает:
`docker-compose up`
Миграции: `docker-compose run web python manage.py migrate`
Создание админа: `docker-compose run web python manage.py createsuperuser`

# Технологии:
Postgresql 10.6: https://www.postgresql.org/download automatic!
Guinicorn 20.0.4: https://docs.gunicorn.org/en/stable/install.html automatic!
Ngnix 1.19.8: https://www.nginx.com/resources/wiki/start/topics/tutorials/install automatic!

# коротко об авторе
My GitHub: https://github.com/JohnTamarych automatic!
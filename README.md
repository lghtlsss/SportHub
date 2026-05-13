# SportHub — социальная сеть для спортсменов

SportHub — это учебный проект социальной сети, ориентированной на спортсменов и людей, ведущих активный образ жизни.
Платформа позволяет делиться тренировками, отслеживать прогресс и находить единомышленников.

---

## Основные возможности

* Регистрация и авторизация пользователей
* Профиль пользователя (аватар, описание, спорт, возраст)
* Создание и отображение постов
* Взаимодействие (лайки, подписки)
* Упор на UX и современный интерфейс

---

## Интерфейс

Проект выполнен в стиле современных fitness/SaaS приложений:

* Тёмная тема
* Акцентные цвета
* Размытие (glass effect)
* Адаптивная верстка
* Карточный UI вместо таблиц

---

## Технологии

**Backend:**

* Python
* Flask
* Flask-Login
* SQLAlchemy

**Frontend:**

* HTML (Jinja2 templates)
* CSS (custom)
* JavaScript (частично / планируется расширение)

---

## Структура проекта

```
project/
├── app_dir/
│   └── app_class.py
├── data/
│   ├── __all_models.py
│   ├── avatar.py
│   ├── comment.py
│   ├── db_session.py
│   ├── image.py
│   ├── like.py
│   ├── post.py
│   ├── subscriber.py
│   └── user.py
├── db/
├── main_app/
│   ├── forms/
│   │   ├── __all_forms.py
│   │   ├── edit_profile_form.py
│   │   ├── login_form.py
│   │   ├── post_creation_form.py
│   │   └── registration_form.py
│   ├── static/
│   │   ├── css/
│   │   │   ├──style.css
│   │   └── images/
│   │   │   ├──gym1.jpg
│   │   │   ├──gym2.jpg
│   │   │   ├──no_avatar.jpg
│   │   │   ├──running_city.jpg
│   │   │   ├──running_city2.jpg
│   │   │   ├──icon.png
│   ├── templates/
│   │   ├── about_us.html
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── no_logined_user.html
│   │   ├── post_creation.html
│   │   ├── posts_line.html
│   │   ├── profile.html
│   │   ├── profile_edit.html
│   │   ├── register.html
│   │   ├── subscribers.html
│   │   ├── subscriptions.html
│   │   ├── success.html
│   │   └── view_post.html
│   ├── tools/
│   │   ├── image_request_tool.html
│   │   └── time_tool.html
│   └── main.py
├── resources/
│   ├── avatar_resource.py
│   ├── post_resource.py
│   └── user_resourse.py
│   └── feed_resource.py
│   └── image_resource.py
│   └── comment_resource.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Установка и запуск

1. Клонировать репозиторий:

```
git clone https://github.com/yourusername/sporthub.git
cd sporthub
```

2. Создать виртуальное окружение:

```
python -m venv venv
venv\Scripts\activate
```

3. Установить зависимости:

```
pip install -r requirements.txt
```

4. Запустить приложение:

```
python app.py
```

5. Открыть в браузере:

```
<здесь будет ссылка на ресурс>
```

---

## Особенности реализации

* Используется Jinja2 для шаблонов
* Собственный api
* Динамическая загрузка аватарок/картинок через API
* Гибкая архитектура для масштабирования

---

## Функции

* Лента постов
* Обновление без перезагрузки (fetch)
* Подписки
* Комментарии

---

## Цель проекта

Проект создаётся как учебный, но с упором на реальные подходы к разработке, современный UI/UX и архитектуру, близкую к
production.

---

## Автор

Артём — разработчик проекта

---

## Лицензия

Проект распространяется в учебных целях.
Свободен для доработки и использования.

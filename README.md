# Сайт для просмотра фильмов FLIXGO

### На данный момент реализовано:
- Главная страница
  - Карусель с топ фильмами сезона
  - Список премьер, мультфильмов, новых фильмов
- Каталог фильмов
  - Сортировка по жанрам, году, стране
  - Пагинация
- Страница вывода фильма
  - Рейтинг фильма
  - Отзывы и ответы на отзывы
  - Вывод доп. кадров к фильму
  - Частично реализована возможность поделиться в соц. сетях
- Страница с фильмами по выбранному актеру | режиссеру
- Авторизация, Регистрация
- Сброс пароля через gmail
- Мультиязычность сайта (en, ru)
- Поиск по сайту
- Вспомогательные страницы, по типу: 'помощь' и 'о нас'

==========================================================

### TO DO List:
- [ ] Оптимизировать запросы в БД
- [ ] Кеширование
- [ ] Доделать возможность поделится в соц.сетях
- [ ] Страница фильма:
  - [ ] Связанная модель на ссылки к фильму (для вставки самого фильма в разном разрешении, а не только описания)
  - [ ] Лайки, дизлайки к каждому отзыву
  - [ ] Алгоритм и реализация подбора фильмов похожих на этот фильм
  - [ ] Валидацию айпи, чтобы оценку можно было оставить один раз
- [ ] Деплой на сервер
- [ ] Наполнение сайта

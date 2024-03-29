# Арюзин Никита - IT-проект "вирт. среда для лабораторных работ по физике LycLab"
### Группа: 10И3
###  Электронная почта: nikitaastro1iq@gmail.com
###  VK: https://vk.com/id671630964

**[Название проекта]**

"Виртуальная лаборатория LycLab"

**[Проблемное поле]**

В связи с небольшим количеством физических лабораторий в Лицее НИУ ВШЭ(или, например, их полным отсутствием в здании Футуритета на 3-м Колобовском переулке)
и потенциальным увеличением количества учащихся Лицея НИУ ВШЭ и Футуритета увеличивается потребность в физических лабораториях и
компонентах для проведения лабораторных работ, количество которых ограничено + время проведения лабораторной работы ограничено временем присутствия в лаборатории. Разрабатываемый продукт позволит решить эту проблему так как предоставит возможность проведения некоторых лабораторных работ
в виртуальном формате, независимо от лабораторного оборудования.


**[Заказчик/потенциальная аудитория]**

Программный продукт будет полезен для преподавателей физики Футуритета Лицея НИУ ВШЭ так как он 
упростит методику преподавания физики, а точнее, упростит методику проведения лабораторных работ по физике,
так как сделает проведение некоторых лабораторных работ независимыми от имеющейся в наличии компонентной базы,
также этот продукт поможет ученикам, изучающим физику, лучше разобраться в предмете путем моделирования физических
свойств компонентов. Суммируя выше описанное к группам потенциальной аудитории продукта относятся:
1. Преподаватели физики Футуритета и не только
2. Ученики 8-9 классов, заинтересованные в изучении физики или получении дополнительной практики по определенным разделам физики

**[Аппаратные/программные требования]**

Продукт разрабатывается для использования в облачной версии.
* Требования: Наличие браузера Chrome, FireFox или Яндекс
* Доступ в сеть

**[Функциональные требования]**

Программный продукт будет включать в себя следующие функции и возможности:
* Регистрация(создание) пользователя и сохранение в приложении прогресса пользователя.
* Выбор уровня сложности в профиле(8,9 класс)
* симуляция физических свойств компонентов( в данном случае электронных, так как сценарии работ в программе будет на электродинамику)
* Проведение в продукте лабораторных работ по физике в разделе "электродинамика" по предоставленным теоретическим материалам . 
* Выполнение работы в условиях, приближенных к реальным условиям физических лабораторий, т.е. работа выполняется на общем "лабораторном столе" с общим перечнем оборудования (с навигацией) и доступом к теоретическим материалам. То есть для выполнения работы необходимо собрать на "столе" электрическую цепь.
* Доступ к систематизированным теоретическим материалам в дополнительной "виртуальной тетради"(дополнительное окно с навигацией и поиском)
* Интерактивное взаимодействие пользователя с физическими компонентами(сборка, соединение, измерение показателей виртуальными приборами)

**[Похожие/аналогичные продукты]**

В качестве похожего продукта можно назвать виртуальную среду PhET Interactive Simulations, но в ней нет поддержки русского языка, также, так как эта программа разаработана
Колорадским университетом в Боулдере, есть определенный риск прекращения работы программы с российскими пользователями. Также эта программа не адаптирована под методические
материалы курсов физики по российским образовательным стандартам.Также можно назвать аналогами программы ROQED Physics lab и VPLab, эти программы обладают большим функционалом (трехмерная графика и реалистичные анимации + больший перечень работ), но эти программы тоже не адаптированы под росиийские образовательные стандарты и не поддерживают русский язык. Также для полноценного использования двух этих программ необходима платная лицензия, в отличие от разрабатываемого продукта. Из российских аналогов разрабатываемого продукта можно назвать программу efizika, в этой программе, в отл. от разрабатываемого продукта нет возможности сохранения прогресса пользователя и работы представлены в виде перечня отдельных сценариев, где можно только менять параметры, то есть в программе невозможно создавать свои лабораторные установки, единого "лабораторного стола" в ней тоже нет.

**[Инструменты разработки]**

* HTML/CSS - фронтенд
* Django - бэкенд
* SQLite или MySQL - БД

**[Этапы разработки]**
1. Разработка пользовательских сценариев.
2. Подбор теоретических материалов.
3. Разработка дизайна среды(макеты).
4. Разработка архитектуры баз данных.
5. Создание главной страницы сайта(фронтенд+дизайн).
6. Реализация авторизации и регистрации пользователя.
7. Создание страницы доступа к всем теоретическим материалам(вместе с доступом к файлам и их загрузкой из БД).
8. Поиск подходящего физического движка(JS-библиотеки) для лаборатории
9. Интеграция физического движка и страницы выполнения лабораторных работ.
10. Разработка метода сохранения прогресса работы(бэкенд).
11. Доработка дизайна и тестировка.
12. Подготовка к защите.

**[Потенциальные риски]**
* Невозможность разработать удобный интерфейс
* Потенциальные проблемы с физическим движком
* Возможная нехватка времени на изучение требуемых для разработки технологий, а конкретно, БД и физического движка.



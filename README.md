<!-- Output copied to clipboard! -->

<!-----
NEW: Check the "Suppress top comment" option to remove this info from the output.

Conversion time: 0.465 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β31
* Sun Dec 12 2021 03:07:27 GMT-0800 (PST)
* Source doc: README
----->


**Начальные требования**

Наличие python (тестировалось на версии 3.8) и pip

**Установка**



* Скачайте репозиторий \

* Перейдите в папку с проектом и создайте виртуальную среду
    * python -m venv .venv
* Активируйте среду

    В Windows:

    * .venv\Scripts\activate

	В Linux:



    * source .venv/bin/activate
* Установите необходимые для работы программы модули
    * pip install -r requirements.txt

**Использование**

Код _swissknife.py _запускает локальный сервер с единственным эндпойнтом /similar-recognition. 

Команда запуска:



* python swissknife.py runserver

На вход ожидается POST - реквест в формате JSON  с двумя ключами: “text1” и “text2”. В значениях ключей передаются тексты на русском или английском языке. 

Пример запроса (представлен в файле _example.http_):

    {


      "text1": "Is there anybody out there?", "text2": "Is there anybody in there?"


    }


Программа оценивает сходство первого и второго текста и возвращает JSON-объект с ключом “Similarity score” и численным значением метрики схожести.

Пример ответа:


    {


      "Similarity score:": 0.9776264572377503


    }

 В случае, если сравниваемые тексты одинаковы, возвращается значение 1. Если тексты написаны на разных языках, возвращается значение 0.

**Описание**

Серверное приложение выполнено в фреймворке Django. Анализ текстов проводится с применением функций и пайплайнов библиотеки SpaCy.

При обработке текста посредством spaCy-пайплайна текст разбивается на отдельные элементы (tokens, определяются компонентом Tokenizer), для каждого определяются части речи (компонент Tagger), зависимости (DependencyParser), т.н. “сущности” (решается задача NER: выявление в тексте непрерывных фрагментов-”спанов”, имеющих определённое смысловое значение - например, являющееся названием организации, датой, именем личности; эту задачу выполняет компонент EntityRecognizer) и леммы (словарные формы, компонент – Lemmatizer). \


В крупных пайплайнах имеется встроенный набор векторов для смысловых представлений слов, эти вектора присваиваются токенам. Вектор целого текста содержит усреднённые по векторам отдельных токенов значения. Функция Similarity возвращает косинусное расстояние между векторами обработанных текстов. Однако косинусное расстояние между векторами слов, принадлежащих разным словарям, не даст корректной оценки. Так, similarity score между словами “груша” и “pear” был бы порядка 0.09, то есть меньше 1%. По этой причине в случае, если представленные тексты написаны на разных языках, программа не рассчитывает similarity score при помощи функции, а просто возвращает значение ноль. Для определения языка был использован инструмент detect библиотеки langdetect (https://pypi.org/project/langdetect/).

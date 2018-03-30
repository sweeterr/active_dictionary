# Active Dictionary | [Активный словарь русского языка] (http://www.ruslang.ru/active_2014)
## Что делать, если нужна база данных словаря на личном компьютере
### Скачиваем статьи
1. Копируем из [данного репозитория] (https://github.com/sweeterr/active_dictionary) папку [code] (https://github.com/sweeterr/active_dictionary/tree/master/code) в личную папку проекта. Все новые папки со статьями, результатами и прочим будут создаваться в папке проекта.
2. Код написан для MacOS, Python 3.5. Перед запуском каждого модуля проверяем, установлены ли все модули, прописанные в 'import'. Внимательно смотрим на все пути. Если путь где-то изменен, учитываем это при запуске следующих функций.
3. Прописываем 'AUTHORIZATION' в 'download_articles.py' и запускаем. По умолчанию статьи скачиваются в папку 'articles'. По умолчанию скачиваются все статьи: создаются файлы для всех слов, которые присутствуют в базе. Можно ограничиться отдельными буквами, прописав 'letters' в 'download_articles.py' и в последующих функциях.
4. Запускаем 'clean_articles.py'. По умолчанию чистые статьи записываются в папку 'clean_articles'. Статьи будут лежать в папках по буквам в отдельных файлах. По умолчанию также запускается функция 'get_letter_volumes', которая собирает слова, начинающиеся на одну букву, в один файл. Результат находится в папке 'letter_volumes'.
5. Запускаем 'vocable_database.py'.

В папке letter_tables_csv появятся .csv-файлы с вокабулами для каждой буквы. Здесь есть следующие атрибуты: вокабула, автор, часть речи, лексема, её значение, аргументы в значении, модель управления аргументов. Для каждой вокабулы количество строк соответствует количеству лексем. Эти файлы читаются в текстовом редакторе типа Notepad++, TextWrangler, etc. В Excel, возможно, будут проблемы с кодировкой. Для лучшей читаемости их можно переделать в .xlsx: открываем файл в Excel → вкладка Data → From text → выбираем файл → выбираем Delimited, File origin: Unicode (UTF-8) → Delimiters: Other: # → сохраняем файл с расширением .xlsx.

По умолчанию также запускается запись вокабул в базы данных – сначала по буквам, потом по томам (прописаны Том 1 АБВГ и Том 2 ДЕЖЗ) – в папке databases. Здесь наиболее полные данные о вокабулах в двух таблицах: 1) vocables (вокабула, синопсис, автор, часть речи, ссылка на статью на http://sem.ruslang.ru/slovnik.php, статья вокабулы полностью), 2) lexemes (вокабула, лексема, значение лексемы, аргументы лексемы, модели лексемы, статья лексемы).
Также в этом модуле есть функция записи вокабул с синопсисами. При желании её можно запустить.
### Собственно проверяем статьи.
* Везде ли есть аргумент A1, где есть другие аргументы?
Запускаем check_a1.py. Вокабулы по умолчанию берутся из папки letter_tables_csv. Файл without_a1.csv появится в папке check_results (перевод в .xlsx описан выше). В нем все лексемы, в значении которых есть аргументы, но нет первого аргумента (строка: вокабула, автор, часть речи, лексема, значение).
* Все ли аргументы из толкования, есть в модели управления?
Запускаем check_model.py. Вокабулы по умолчанию берутся из папки letter_tables_csv. Файл without_model.csv появится в папке check_results (перевод в .xlsx описан выше). В нем все лексемы, в толковании которых есть аргументы, у которых не прописана модель (строка: вокабула, автор, часть речи, лексема, толкование, аргумент без модели, модель).
* Правильная ли нумерация лексем в синопсисе и статье?
Запускаем check_synopsis.py. Вокабулы по умолчанию берутся из папки letter_tables_csv. Файлы with_dashes.txt и wonky_numbers.txt появится в папке check_results. В with_dashes.txt перечислены вокабулы с лексемами, в которых есть дефисы (это чаще всего глаголы с отсылками на видовую пару). В них нумерацию – и нумерацию в отсылке! – нужно проверить отдельно. В файле wonky_numbers.txt перечислены вокабулы с подозрительной нумерацией в синопсисе или в теле статьи. Подозрительными они могут быть по разным причинам:
- собственно ошибки в нумерации либо в синопсисе, либо в статье; 
- может стоять лишняя точка;
- нет нужной точки; 
- лишний пробел;
- отсутствие пробела после лексемы;
- не на новой строке;
- опечатка в лексеме, синопсисе; 
- помета перед лексемой в синопсисе и в статье;
- непоследовательная ё в вокабуле, синопсисе, статье;
- форма лексемы может не совпадать с формой вокабулы, но при этом в синопсисе и статье совпадает;
- форма лексемы может не совпадать с формой вокабулы, но при этом в синопсисе и статье не совпадает;
- отсылки на другие вокабулы с дефисом.
* Лексем с большой буквы в статье и синопсисе не должно быть (кроме случаев типа Земля). Найдем их.
Запускаем check_capital_letter.py. Вокабулы по умолчанию беруться из папки clean_articles (для исключения случаев неправильного парсинга лексем и непопадания лексем с большой буквы в letter_tables_csv). Список лексем с большой буквы лежит в файле check_results/with_capitals.txt.

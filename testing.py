'''
#парсер статей из ссылок
from bs4 import BeautifulSoup
import urllib.request

f = open('Урлы.txt', 'r')
for line in f:
    counter += 1
    html = urllib.request.urlopen(line).read()
    soup = BeautifulSoup(html, "html.parser")
    f1 = open(str(counter) + '.txt', 'w')
    f1.write(soup.find('div', id="divLetterBranding").get_text())
    f1.close()
f.close()
#перевод слов в начальную форму
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

for i in range(1, 403):
    f2 = open(str(i) + '.txt', 'r')
    f2_add = open('_edited' + str(i) + '.txt', 'w')
    for line in f2:
        if len(line) > 1:
            for word in line.split(' '):
                f2_add.write(morph.parse(word)[0].normal_form + ' ')
f2.close()
f2_add.close()'''

#поиск tf-idf слов +
#разбор статей по словам и их частотам
import collections
import math

from collections import Counter
import math

def compute_tf(text):
    tf_text = Counter(text)
    for i in tf_text:
        tf_text[i] = tf_text[i] / float(len(tf_text))
    return tf_text

def compute_idf(word, corpus):
    return math.log10(len(corpus) / sum([1.0 for i in corpus if word in i]))

def compute_tfidf(corpus):
    documents_list = []
    for text in corpus:
        tf_idf_dictionary = {}
        computed_tf = compute_tf(text)
        for word in computed_tf:
            tf_idf_dictionary[word] = computed_tf[word] * compute_idf(word, corpus)
        documents_list.append(tf_idf_dictionary)
    return documents_list

all_diff_words = set() #все различные слова в статьях
dict_of_dicts = {} #статьи, каждая из которых разбита по словам и их встречаемости
corpus = [] #для построения корпуса текстов для подсчета TF-IDF
frequency = {} #частота слова во всем объеме текста
for i in range(1, 403):
    f2 = open('_edited' + str(i) + '.txt', 'r')
    d = {}
    list_in_corpus = []
    for line in f2:
        for word in line.split():
            word.strip('.1234567890-_+=$()"\'#@~\n\t.,«»?!&;^:')
            if word.isalpha():
                list_in_corpus.append(word)
                all_diff_words.add(word) #все различные слова, встретившиеся в статьях
                d[word] = d.get(word, 0) + 1 #частота слова, встретившегося в данной iй статье
                frequency[word] = frequency.get(word, 0) + 1 #слово снова встретилось -> увеличиваем его частоту
            dict_of_dicts[i] = d #в словарь с номерами статей от 1 до 402 добавляется по ключу словарь с частотой слов в ней
    corpus.append(list_in_corpus)
    f2.close()
#посчитаны и отсортированы по убыванию TF-IDF слов в каждой статье, в каждой из них взяты первые 20.
list_of_TF_IDF = compute_tfidf(corpus)
list_of_TF_IDF_sorted_and_cut = []
for list in list_of_TF_IDF:
    key_words = [(w, stat) for w,stat in list.items()]
    key_words.sort(key=lambda x: x[1], reverse=True)
    key_words = key_words[:1] #тут :20, но пока, в силу моего понимания задачи, :1
    list_of_TF_IDF_sorted_and_cut.append(key_words)
'''f11 = open("sorted_and_cut.txt", "w")
f11.write(str(list_of_TF_IDF_sorted_and_cut))
f11.close()'''
#step1
'''
kol = 0 #встречаемость данного слова в данной статье
f3 = open('step1.txt', 'w')
f3.write(''.rjust(20))
f3.write('\t'.join([str(i) for i in range(1, 403)]))
f3.write('\n') #запись номеров статей - шапка таблицы
for word in all_diff_words: #для каждого слова, встретившегося во всех статьях
        f3.write(word.ljust(20)) #записываем шапку-столбец со словом
        for i in range(1, 403): #теперь в каждой статье от 1 до 402
            kol = dict_of_dicts[i].get(word, 0)
            f3.write(str(kol)) #по номеру статьи мы находим частоту данного слова в ней, если оно не встречается, возвращаем 0
            if i != 402:
                f3.write('\t') #пишем разделители
        f3.write('\n')
f3.close()
'''
#step2
'''
vectors = {} #для 3 шага создаем словарь с координатами 402-мерных векторов-слов из статей
coordinates = [] #для 3 шага для каждого слова находим его координаты с 1 по 402
all_diff_words_numbered = [] #упорядоченный список различных анализируемых слов
kol = 0 #встречаемость данного слова в данной статье
f4 = open('step2.txt', 'w')
f4.write(''.rjust(20))
f4.write('\t'.join([str(i) for i in range(1, 403)]))
f4.write('\n')#опять же, запись шапки
for word in all_diff_words:
    if frequency[word] >= 20: #для каждого слова, встретившегося не менее 20 раз в суммарном объеме текста
        all_diff_words_numbered.append(word)
        f4.write(word.ljust(20)) #снова шапка
        coordinates = []
        for i in range(1, 403):
            kol = dict_of_dicts[i].get(word, 0)
            f4.write(str(kol)) #как и в step1 записываем частоту в данной статье
            coordinates.append(kol) #добавляем очередную iую координату слова (нумерация координат с 0 по 401)
            if i != 402:
                f4.write('\t') #пишем разделители
        f4.write('\n')
        vectors[word] = coordinates #добавляем очередное слово-вектор
f4.close()
'''
#step3
'''
import math
length = {} #длина 402-мерного вектора
#считаем длину векторов- корень из суммы квадратов координат
for word in vectors:
    sum = 0
    for num in vectors[word]:
        sum += num*num
    length[word] = math.sqrt(sum)
#считаем скалярное произведение и вычисляем непосредственно косинус, как скалярное произведение/произведение длинн
cosinus = {} #словарь с ключами - парой слов и значением - косинусом между парой слов
iterator = len(all_diff_words_numbered)
for i in range(iterator - 1): #c 0 по кол-во анализируемых слов без последнего
    for j in range (i+1, iterator): #c следующего слова в списке до его конца (полный проход по парам слов)
        f_word = all_diff_words_numbered[i] #первое слово из пары
        s_word = all_diff_words_numbered[j] #второе слово из пары
        len_product = length[f_word]*length[s_word] #вычисляем знаменатель - произведение длинн
        sc_product = 0 #скалярное проивзедение пары векторов-слов
        for k in range(402): #покоординатно, c 0 по 401
            sc_product += vectors[f_word][k] * vectors[s_word][k] #перемножаем координаты векторов
        cosinus[f_word + '\t' + s_word] = sc_product / len_product #непосредственно считаем косинус между словами
f5 = open('step3.txt', 'w')
for key in cosinus:
    f5.write(key.ljust(40) + str(cosinus[key]) + '\n') #записываем получившиеся данные - пара слов и косинус угла между ними
f5.close()
'''
#step4
'''
#записываем лишь те слова, косинус между которыми > 0.5
f6 = open('step4.txt', 'w')
for key in cosinus:
    if cosinus[key] > 0.5:
        f6.write(key.ljust(40) + str(cosinus[key]) + '\n')
f6.close()
'''

#step5 (объединение предыдущих)
#записываем табличку из топ 20 слов по встречаемости с cos между ними(помнить об округлении cos), всего 20 табличек по
#временному периоду
'''frequency_list = list(frequency.items()) #лист, необходимый для сортировки частот по убыванию
frequency_list.sort(key=lambda item: item[1], reverse=True)  #непосредственно сортировка'''
all_top_words_numbered = [] #копия верхнего куска кода для необходимого нам числа слов
list_of_all_top_words_numbered = []
vector_of_vectors = []
vectors = {} #см. выше
for k in range(20): #кол-во графов
    f7 = open('top_words' + str(k) + '.txt', "w")
    all_top_words_numbered = []
    vectors = {}
    for j in range(20): #кол-во слов для каждого
        f7.write(str(j + 1) + ". " + str(list_of_TF_IDF_sorted_and_cut[k * 20 + j][0][0]) + '\n')#слово, не уверена, что [0]
        all_top_words_numbered.append(list_of_TF_IDF_sorted_and_cut[k * 20 + j][0][0])
        coordinates = []
        for i in range(1, 403):
            kol = dict_of_dicts[i].get(list_of_TF_IDF_sorted_and_cut[k * 20 + j][0][0], 0)
            coordinates.append(kol)  # добавляем очередную iую координату слова (нумерация координат с 0 по 401 вкл)
        vectors[list_of_TF_IDF_sorted_and_cut[k * 20 + j][0][0]] = coordinates  # добавляем очередное слово-вектор
    vector_of_vectors.append(vectors); #0 - 19 для каждого графа - 20 штук по 20 векторов
    list_of_all_top_words_numbered.append(all_top_words_numbered)
    f7.close()
length = {} #длина 402-мерного вектора
list_of_lengths = []
#считаем длину векторов- корень из суммы квадратов координат
for k in range(20):
    length = {}
    for word in vector_of_vectors[k]:
        sum = 0
        for num in vector_of_vectors[k][word]:
            sum += num * num
        length[word] = math.sqrt(sum)
    list_of_lengths.append(length)
# считаем скалярное произведение и вычисляем непосредственно косинус, как скалярное произведение/произведение длинн
list_of_cosinuses = []
cosinus = {}  # словарь с ключами - парой слов и значением - косинусом между парой слов
list_of_cosinuses = []
list_of_links = []
links = []
for k in range(20): #опять же, графы
    cosinus = {}
    for i in range(19):  # c 0 по кол-во анализируемых слов без последнего
        for j in range(i + 1, 20):  # c следующего слова в списке до его конца (полный проход по парам слов)
            f_word = list_of_all_top_words_numbered[k][i]  # первое слово из пары
            s_word = list_of_all_top_words_numbered[k][j]  # второе слово из пары
            len_product = list_of_lengths[k][f_word] * list_of_lengths[k][s_word]  # вычисляем знаменатель - произведение длинн
            sc_product = 0  # скалярное проивзедение пары векторов-слов
            for cor in range(402):  # покоординатно, c 0 по 401
                sc_product += vector_of_vectors[k][f_word][cor] * vector_of_vectors[k][s_word][cor]  # перемножаем координаты векторов
            cosinus[f_word + '\t' + s_word] = sc_product / len_product  # непосредственно считаем косинус между словами
    list_of_cosinuses.append(cosinus)
for k in range(20):
    links = []
    for key in list_of_cosinuses[k]:
        if list_of_cosinuses[k][key] >= 0.1: #можно порегулировать, посмотреть
            link = {}
            names = key.split('\t')
            link["source"] = names[0]
            link["target"] = names[1]
            link["type"] = 'suit'
            links.append(link)
    list_of_links.append(links)
for k in range(20):
    f8 = open('adjacency list' + str(k) + '.txt', 'w')
    for key in list_of_cosinuses[k]:
        f8.write(key.ljust(40) + str(list_of_cosinuses[k][key]) + '\n')  #записываем получившиеся данные - пара слов и косинус угла между ними
    f8.close()
#здесь конвертится в json файл с списком смежности ребер графа
import json
for k in range(20):
    f9 = open('links_in_json' + str(k) + '.json', 'w')
    links = json.dumps(list_of_links[k], ensure_ascii=False)
    f9.write(str(links))
    f9.close()

#Вот есть у нас лист с tf-idf отсортированный - лист листов пар, 402 листа, в каждом по 20 пар, то есть по 20 слов - всего
#20 * 402 слов
#Мы можем отобрать самое важное слово в каждой статье - первое
#Из них, с учетом количества графов, то есть 20, выберем просто по 20 первых слов, идя подряд (400/ 20 = 20), 2 последних нам не интересны
#Посчитаем между ними косинусные меры, для каждых 20
#На их основе построим графы (20), сгенерим 20 js файлов.





#Форму и 10 графов сгенерить за оставшиеся 2 дня, сегодня сделать слова с TF_IDF в графе.
#Проблемы с обновлением кэша - каждый раз приходится вручную, иначе не работает.
#Траблы - косинус 0,5 - слишком перегружен граф по связям - беру 0,7
#Проблемы с кодировкой - каждый раз в notepad приходится перекодировать json в utf-8, иначе не жрет русский язык - как делать это автоматически?
#создать графы по неделям(Питон) - селектор
#Но TF-IDF уберет Трампа и Хиллари же, это так себе подход для данной коллекции текстов, хотя расчет я сделаю, но пока применять не буду
#Не буду просто потому, что еще не понимаю, из какого колиечтсва слов по частой встречаемости брать с самым большим TF_IDF?
#То есть мы же не полностью переключаемся на ТF_IDF, иначе б менялся смысл задания
#Дизайн + отсылка формы - html! ДИЗАЙН!
#Или топ-10 пар? по величине косинуса? Я пока возьму топ-20 по встречаемости
#Начинать ли меня код, делая его более общим, а не под количество статей?
#Как автоматически перекидывать в http на сервере json файл с кодом, что б эта фигня знала, откуда подключать jsonчик?

#Доделать - форму, дизайн формы.
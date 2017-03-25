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
#разбор статей по словам и их частотам
all_diff_words = set() #все различные слова в статьях
dict_of_dicts = {} #статьи, каждая из которых разбита по словам и их встречаемости
frequency = {} #частота слова во всем объеме текста
for i in range(1, 403):
    f2 = open('_edited' + str(i) + '.txt', 'r')
    d = {}
    for line in f2:
        for word in line.split():
            word.strip('.1234567890-_+=$()"\'#@~\n\t.,«»?!&;^:')
            if word.isalpha():
                all_diff_words.add(word) #все различные слова, встретившиеся в статьях
                d[word] = d.get(word, 0) + 1 #частота слова, встретившегося в данной iй статье
                frequency[word] = frequency.get(word, 0) + 1 #слово снова встретилось -> увеличиваем его частоту
            dict_of_dicts[i] = d #в словарь с номерами статей от 1 до 402 добавляется по ключу словарь с частотой слов в ней
    f2.close()
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
#step3
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
'''f5 = open('step3.txt', 'w')
for key in cosinus:
    f5.write(key.ljust(40) + str(cosinus[key]) + '\n') #записываем получившиеся данные - пара слов и косинус угла между ними
f5.close()'''
#step4
#записываем лишь те слова, косинус между которыми > 0.5
f6 = open('step4.txt', 'w')
for key in cosinus:
    if cosinus[key] > 0.5:
        f6.write(key.ljust(40) + str(cosinus[key]) + '\n')
f6.close()



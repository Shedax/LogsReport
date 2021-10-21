import os

#создаём файлы report.txt, если отсутствуют
for i in os.listdir('logs'):
    for j in os.listdir('logs\\'+ i):
        with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'a+') as rep:
            pass

for i in os.listdir('logs'):
    for j in os.listdir('logs\\'+ i):
        with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'r+') as rep:
            #множество для сравнения с содержимым папки
            given = set(['ft_reference', 'ft_run', 'report.txt'])
            if set(os.listdir('logs\\' + i + '\\' + j)) != given:
                #получаем отсутствующие директории через разницу множеств
                diff = given.difference(set(os.listdir('logs\\' + i + '\\' + j)))
                #записываем результат в report.txt
                rep.write('directory missing: ' + ', '.join(diff))


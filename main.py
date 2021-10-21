import os
from pathlib import Path

# создаём файлы report.txt, если отсутствуют
for i in os.listdir('logs'):
    for j in os.listdir('logs1\\'+ i):
        with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'a+') as rep:
            pass

for i in os.listdir('logs'):
    for j in os.listdir('logs\\' + i):
        try:
            for k in os.listdir('logs' +'\\' +i + '\\' + j + '\\' + 'ft_run'):
                #открываем файл .stdout на чтение
                with open('logs' +'\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout', "r") as std:
                    #получаем текст
                    text = std.readlines()
                    #переменная для проверки будет ли в тексте строка, начинающаяся с "Solver finished at"
                    starts = False
                    #номер строки
                    num = 0
                    #открываем файл report.txt на дозапись
                    with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'a+') as rep:
                        for line in text:
                            num += 1
                            #запись в файл при наличии слова error в строке, переведённой в нижний регистр
                            if 'error' in line.lower():
                                rep.write('logs' +'\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout(' + str(num) + '): ' + line)
                            #при наличии строки, начинающейся с "Solver finished at" изменяем значение переменной
                            if line.startswith('Solver finished at'):
                                starts = True
                        #если значение осталось False, записываем результат в reports.txt
                        if not starts:
                            rep.write('logs' + '\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout: missing "Solver finished at"')
        #при отсутствие папки ft_run переходим к другому тесту
        except FileNotFoundError:
            continue
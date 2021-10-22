import os
from pathlib import Path

if 'logs2' not in os.listdir():
    print('Папка logs отстутсвует в директории проекта!')
else:
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

    for i in os.listdir('logs'):
        for j in os.listdir('logs\\' + i):
            #получаем список путей файлов с расширением .stdout с родительской директорией ft_reference
            files1 = list(Path('logs\\' + str(i) + '\\' + str(j) + '\\' + 'ft_reference').rglob("*.stdout"))
            # получаем список путей файлов с расширением .stdout с родительской директорией ft_run
            files2 = list(Path('logs\\' + i + '\\' + j + '\\' + 'ft_run').rglob("*.stdout"))
            final_list1 = []
            final_list2 = []
            # получаем списки с обрезанным путём, оставляя только название директории с файлом и названием файла
            for b in range(len(files1)):
                final_list1.append(str(files1[b]).split('\\ft_reference')[1])
            for c in range(len(files2)):
                final_list2.append(str(files2[c]).split('\\ft_run')[1])
            #проверка совпадения набора файлов .stdout в директориях ft_reference и ft_run
            if set(final_list1) != set(final_list2):
                #открытие файла на дозапись
                with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'a+') as rep:
                    #получаем отсутствующие директории с файлами stdout через разницу множеств
                    diff1 = list(set(final_list1).difference(set(final_list2)))
                    diff2 = list(set(final_list2).difference(set(final_list1)))
                    rep.seek(0)
                    if 'directory missing' in rep.read():
                        continue
                    else:
                        # записываем результат в report.txt
                        if len(diff1) != 0:
                            rep.write('In ft_run there are missing files present in ft_reference: ' + ', '.join([liter.replace('\\', '/') for liter in diff1]) + '\n')
                        if len(diff2) != 0:
                            rep.write('In ft_run there are extra files not present in ft_reference: ' + ', '.join([liter.replace('\\', '/') for liter in diff2]) + '\n')

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
                                    rep.write('logs' +'\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout(' + str(num) + '): ' + line + '\n')
                                #при наличии строки, начинающейся с "Solver finished at" изменяем значение переменной
                                if line.startswith('Solver finished at'):
                                    starts = True
                            #если значение осталось False, записываем результат в reports.txt
                            if not starts:
                                rep.write('logs' + '\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout: missing "Solver finished at"' + '\n')
            #при отсутствие папки ft_run переходим к другому тесту
            except FileNotFoundError:
                continue

    for i in os.listdir('logs'):
        for j in os.listdir('logs\\' + i):
            try:
                for k in os.listdir('logs' + '\\' + i + '\\' + j + '\\' + 'ft_run'):
                    with open(
                            'logs' + '\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout',
                            "r") as std:
                        with open('logs' + '\\' + i + '\\' + j + '\\' + 'ft_reference\\' + k + '\\' + '{0}'.format(
                                k) + '.stdout', "r") as std2:
                            # считываем текст stdout из ft_run и ft_reference
                            text1 = std.readlines()
                            text2 = std2.readlines()
                            # списки для хранения пиковых значений working set
                            peak1 = []
                            peak2 = []
                            # списки для хранения значений Total
                            total1 = []
                            total2 = []
                            for line in text1:
                                if 'Memory Working Set Peak' in line:
                                    # запись в список значений Memory Working Set Peak из ft_run
                                    peak1.append(float(line.split('Memory Working Set Peak = ')[1].split(' Mb')[0]))
                                if 'MESH::Bricks: Total=' in line:
                                    # запись в список значений MESH::Bricks: Total из ft_run
                                    total1.append(int(line.split('MESH::Bricks: Total=')[1].split(' Gas')[0]))
                            for line2 in text2:
                                if 'Memory Working Set Peak' in line2:
                                    # запись в список значений Memory Working Set Peak из ft_reference
                                    peak2.append(float(line2.split('Memory Working Set Peak = ')[1].split(' Mb')[0]))
                                if 'MESH::Bricks: Total=' in line2:
                                    # запись в список значений MESH::Bricks: Total из ft_reference
                                    total2.append(int(line2.split('MESH::Bricks: Total=')[1].split(' Gas')[0]))
                            # отличие Memory Working Set Peak
                            difference = 100 * (max(peak1) - max(peak2)) / max(peak2)
                            # отличие MESH::Bricks: Total
                            difference2 = 100 * (total1[len(total1) - 1] - total2[len(total2) - 1]) / total2[
                                len(total2) - 1]
                            if abs(difference) > 50:
                                with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'a+') as rep:
                                    rep.write(
                                        'logs' + '\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k)
                                        + '.stdout: different "Memory Working Set Peak" (ft_run=' + str(max(peak1)) +
                                        ', ft_reference=' + str(
                                            max(peak2)) + ', rel.diff=' + '%.2f' % abs(difference) + ', criterion=0.5)\n')
                            if abs(difference2) > 10:
                                with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'a+') as rep:
                                    rep.write(
                                        'logs' + '\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k)
                                        + '.stdout: different "Total" of bricks (ft_run=' + str(total1[len(total1) - 1])
                                        + ', ft_reference=' + str(total2[len(total2) - 1]) + ', rel.diff=' + '%.2f' %
                                        abs(difference2) + ', criterion=0.1)\n')
            except FileNotFoundError:
                continue

    for i in os.listdir('logs'):
        for j in os.listdir('logs\\' + i):
            with open('logs\\' + i + '\\' + j + '\\' + 'report.txt', 'r') as rep:
                #считываем report.txt
                text = rep.readlines()
                #сли ft_run существует
                try:
                    for k in os.listdir('logs' + '\\' + i + '\\' + j + '\\' + 'ft_run'):
                        #если report.txt пуст
                        if len(text) == 0:
                            with open('logs' + '\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout',"a+") as std:
                                std.write('\nOK: ' + i + '/' + j + '/')
                        else:
                            with open('logs' + '\\' + i + '\\' + j + '\\' + 'ft_run\\' + k + '\\' + '{0}'.format(k) + '.stdout',"a+") as std:
                                std.write('\nFAIL: ' + i + '/' + j + '/\n')
                                #запись содержимого report.txt
                                for line in text:
                                    std.write(line)
                except FileNotFoundError:
                    pass
                #всё по аналогии для ft_reference
                try:
                    for k in os.listdir('logs' + '\\' + i + '\\' + j + '\\' + 'ft_reference'):
                        if len(text) == 0:
                            with open('logs' + '\\' + i + '\\' + j + '\\' + 'ft_reference\\' + k + '\\' + '{0}'.format(k) + '.stdout', "a+") as std2:
                                std2.write('\nOK: ' + i + '/' + j + '/')
                        else:
                            with open('logs' + '\\' + i + '\\' + j + '\\' + 'ft_reference\\' + k + '\\' + '{0}'.format(k) + '.stdout', "a+") as std2:
                                std2.write('\nFAIL: ' + i + '/' + j + '/\n')
                                for line in text:
                                    std2.write(line)
                except FileNotFoundError:
                    pass
import os
from pathlib import Path

# создаём файлы report.txt, если отсутствуют
for i in os.listdir('logs'):
    for j in os.listdir('logs1\\'+ i):
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


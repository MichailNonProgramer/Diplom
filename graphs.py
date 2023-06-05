import csv

# Создаем пустые списки для хранения данных о временах загрузки файлов
load_times_1 = [0] * 10
load_times_2 = [0] * 10
load_times_3 = [0] * 10

# Читаем данные из трех файлов с помощью модуля csv
with open('HTTP1/download_with_lock.txt', 'r') as file_1:
    reader = csv.reader(file_1)
    # Добавляем данные о времени загрузки файла в соответствующий список
    for row in reader:
        load_times_1[int(row[0].split(" ")[2].split("e")[1])-1] = float(row[0].split(" ")[5])

with open('HTTP1/download_with_packet_loss.txt', 'r') as file_2:
    reader = csv.reader(file_2)
    # Добавляем данные о времени загрузки файла в соответствующий список
    for row in reader:
        print(row[0].split(" ")[2].split("e")[1])
        load_times_2[int(row[0].split(" ")[2].split("e")[1]) - 1] = float(row[0].split(" ")[5])

# with open('QUIC/download_time.txt', 'r') as file_3:
#     reader = csv.reader(file_3)
#     # Добавляем данные о времени загрузки файла в соответствующий список
#     for row in reader:
#         print(row)
#         load_times_3[int(row[0].split(" ")[5].split("e")[1])-1] = float(row[0].split(" ")[6])

# Строим график сравнения времен загрузки файлов
import matplotlib.pyplot as plt

files = list(range(1, 11))

plt.plot(files, load_times_1, label="Без потерь")
plt.plot(files, load_times_2, label="С потерями")
# plt.plot(files, load_times_3, label="QUIC")

plt.xlabel("Номер файла")
plt.ylabel("Время загрузки (сек)")

plt.legend()

plt.show()
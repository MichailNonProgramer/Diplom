import statistics

with open("download_with_packet_loss.txt", "r") as file:
    values = [float(line.split()[5]) for line in file] # создаем список третьих значений из всех строк
    mean = statistics.mean(values) # среднее значение
    stdev = statistics.stdev(values) # стандартное отклонение

print(f"Математическое ожидание: {mean}")
print(f"Стандартное отклонение: {stdev}")

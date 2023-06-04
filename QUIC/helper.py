import statistics

with open("C:\\Users\\gotom\\OneDrive\\Рабочий стол\\Диплом\\QUIC\\download_time_with_packet_loss.txt", "r") as file:
    values = [float(line.split(" ")[6]) for line in file]
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)

print(f"Математическое ожидание: {mean}")
print(f"Стандартное отклонение: {stdev}")

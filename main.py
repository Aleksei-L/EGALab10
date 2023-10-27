import numpy as np


def roulette(price):
	size = 0
	for i in range(0, len(price)):
		size += round(price[i][1])
	rand = np.random.uniform(1, size, 1)
	res = round(rand[0])
	summ = 0
	for i in price:
		summ += i[1]
		if round(summ) >= res or len(price) == 1:
			return i


def create_first_population():
	N = int(input("Введите N: "))
	W_max = int(input("Введите весовое ограничение: "))
	things = []
	prices = []
	for i in range(0, N):
		things.append([int(i) for i in input().split()])
	counter = 0
	sumW = 0
	S = [0] * N
	Q = 0
	for i in range(0, len(things)):
		prices.append([i, things[i][0]])
	while counter != N and sumW < W_max:
		item = roulette(prices)
		itemInBackpack = things[item[0]]
		prices.remove(item)
		if sumW + itemInBackpack[1] > W_max:
			print("Выбран предмет " + str(item[0] + 1) + " с ценой " + str(itemInBackpack[0]) + " и весом " + str(
				itemInBackpack[1]))
			print("Предмет не помещается в рюкзак, не берём")
			print()
			break
		print("Шаг " + str(counter + 1) + ":")
		print("Текущая цена ранца: " + str(Q))
		print("Текущий вес ранца: " + str(sumW))
		print("Выбран предмет " + str(item[0] + 1) + " с ценой " + str(itemInBackpack[0]) + " и весом " + str(
			itemInBackpack[1]))
		S[item[0]] = 1
		Q += itemInBackpack[0]
		itemInBackpack[0] = 0
		sumW += itemInBackpack[1]
		counter += 1
		print()
	print("Итог: выбраны предметы " + str(S))
	print("Итоговая ценность: " + str(Q))
	print("Итоговый вес: " + str(sumW))


population_size = int(input("Введите кол-во особей в популяции: "))
choices = []
choices.append(int(input("Оператор формирования начальной популяции:\n1) Случайный\n2) Жадный алгоритм\n>> ")))
choices.append(int(input("Оператор кроссовера:\n1)\n2)\n>> ")))
choices.append(int(input("Оператор мутации:\n1)\n2)\n>> ")))
choices.append(int(input("Оператор селекции:\n1)\n2)\n>> ")))
population = create_first_population() if choices[0] == 1 else print()

for t in range(0, 10):
	print("Поколение " + str(t + 1))

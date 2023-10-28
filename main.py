import numpy as np
import random


def roulette(prices):
	sum_prices = 0
	for item in prices:
		sum_prices += item[1]

	rand = np.random.uniform(1, sum_prices, 1)
	res = round(rand[0])

	summ = 0
	for item in prices:
		summ += item[1]
		if summ >= res or len(prices) == 1:
			return item


def create_population_random(N):
	population = []
	for i in range(0, population_size):
		temp = []
		for j in range(0, N):
			temp.append(random.randint(0, 1))
		population.append(temp)
	return population


def create_population_random_control(N, w_max, things):
	population = []
	for i in range(0, population_size):
		temp = []
		summ = 0
		for j in range(0, N):
			temp.append(random.randint(0, 1))
			if temp[j] == 1:
				summ += things[j][0]
				if summ >= w_max:
					for k in range(j + 1, N):
						temp.append(0)
					temp[j] = 0
					break
		population.append(temp)
	return population


def create_population_greedy_algo(N, w_max, things, population_size):
	population = []
	for i in range(0, population_size):
		solution = [0] * N
		things_counter = 0
		sum_w = 0
		sum_q = 0

		prices = []
		for j in range(0, len(things)):
			prices.append((j, things[j][0]))

		while things_counter != N and sum_w < w_max:
			item = roulette(prices)
			candidate_to_backpack = things[item[0]]
			prices.remove(item)
			if sum_w + candidate_to_backpack[1] > w_max:
				break
			solution[item[0]] = 1
			sum_q += candidate_to_backpack[0]
			sum_w += candidate_to_backpack[1]
			things_counter += 1
		population.append(solution)
	return population


N = int(input("Введите N: "))
w_max = int(input("Введите весовое ограничение: "))
things = []
for i in range(0, N):
	things.append(tuple(int(i) for i in input().split()))
population_size = int(input("Введите кол-во особей в популяции: "))
operator_choices = [
	int(input(
		"Оператор формирования начальной популяции:\n1) Случайный\n2) Случайный с контролем\n3) Жадный алгоритм\n>> ")),
	int(input("Оператор кроссовера:\n1) Одноточечный\n2) Двуточечный\n3) Многоточечный\n>> "))
	# int(input("Оператор мутации:\n1)\n2)\n>> ")),
	# int(input("Оператор селекции:\n1)\n2)\n>> "))
]

population = []
if operator_choices[0] == 1:
	population = create_population_random(N)
elif operator_choices[0] == 2:
	population = create_population_random_control(N, w_max, things)
elif operator_choices[0] == 3:
	population = create_population_greedy_algo(N, w_max, things, population_size)

crossover_point_number = 0
if operator_choices[1] == 1:
	crossover_point_number = 1
elif operator_choices[1] == 2:
	crossover_point_number = 2
elif operator_choices[1] == 3:
	crossover_point_number = int(input("Введите кол-во точек: "))

for t in range(0, 10):
	print("Поколение " + str(t))
	print("Все особи")
	for i in population:
		print(str(i) + " с приспособленностью " + str(1))  # Заглушка: узнать как задаётся приспособленность
	print("Лучшая особь: " + str(population[0]) + " с приспособленностью " + str(1))  # Заглушка: то же самое

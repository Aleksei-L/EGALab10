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


def create_population_random(N, population_size):
	population = []
	for i in range(0, population_size):
		temp = []
		for j in range(0, N):
			temp.append(random.randint(0, 1))
		population.append(temp)
	return population


def create_population_random_control(N, w_max, things, population_size):
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


def crossover_one_point(N, parent1, parent2):
	child1 = []
	child2 = []
	point = random.randint(1, N - 1)
	for i in range(0, point):
		child1.append(parent1[i])
		child2.append(parent2[i])
	for i in range(point, N):
		child1.append(parent2[i])
		child2.append(parent1[i])
	return child1, child2


def crossover_two_points(N, parent1, parent2):
	child1 = []
	child2 = []
	point1 = random.randint(1, N // 2)
	point2 = random.randint(N // 2 + 1, N - 1)
	print(point1, point2)
	for i in range(0, point1):
		child1.append(parent1[i])
		child2.append(parent2[i])
	for i in range(point1, point2):
		child1.append(parent2[i])
		child2.append(parent1[i])
	for i in range(point2, N):
		child1.append(parent1[i])
		child2.append(parent2[i])
	return child1, child2


def crossover_homogeneous(N, parent1, parent2):
	child1 = []
	child2 = []
	for i in range(0, N):
		rand = random.randint(1, 2)
		if rand == 1:
			child1.append(parent1[i])
			child2.append(parent2[i])
		else:
			child1.append(parent2[i])
			child2.append(parent1[i])
	return child1, child2


# TODO Узнать правильно ли написана мутация
def mutation_one_point(N, person):
	for i in range(0, N):
		rnd = random.uniform(0, 1)
		if 0 < rnd <= 0.01:
			person[i] = int(not person[i])
			break
	return person


def get_fitness(N, things, person):
	res = 0.0
	for i in range(0, N):
		if person[i] == 1:
			res += things[i][0] / things[i][1]
	return round(res, 2)


def get_weight(N, things, person):
	res = 0
	for i in range(0, N):
		if person[i] == 1:
			res += things[i][1]
	return res


N = int(input("Введите N: "))
w_max = int(input("Введите весовое ограничение: "))
things = []
for i in range(0, N):
	things.append(tuple(int(i) for i in input().split()))
population_size = int(input("Введите кол-во особей в популяции: "))
operator_choices = [
	int(input(
		"Оператор формирования начальной популяции:\n1) Случайный\n2) Случайный с контролем\n3) Жадный алгоритм\n>> ")),
	int(input("Оператор кроссовера:\n1) Одноточечный\n2) Двуточечный\n3) Однородный\n>> ")),
	int(input("Оператор мутации:\n1) Точечная\n2)\n3)\n>> ")),
	# int(input("Оператор селекции:\n1)\n2)\n>> "))
]

population = []
if operator_choices[0] == 1:
	population = create_population_random(N, population_size)
elif operator_choices[0] == 2:
	population = create_population_random_control(N, w_max, things, population_size)
elif operator_choices[0] == 3:
	population = create_population_greedy_algo(N, w_max, things, population_size)

for t in range(0, 1):
	print("Поколение", t)
	print("Все особи:")
	maxim_fitness_person = 0
	maxim_person = population[0]
	for i in population:
		fit = get_fitness(N, things, i)
		if fit > maxim_fitness_person:
			maxim_fitness_person = fit
			maxim_person = i
		print(i, "с приспособленностью", fit, "и весом", get_weight(N, things, i))
	print("Лучшая особь:", maxim_person, "с приспособленностью", get_fitness(N, things, maxim_person), "и весом",
		  get_weight(N, things, maxim_person))

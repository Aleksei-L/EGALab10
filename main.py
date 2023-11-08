import numpy as np
import random
from copy import deepcopy


def roulette(prices):
	sum_prices = 0
	for item in prices:
		sum_prices += item[1]

	rand = np.random.uniform(1, sum_prices, 1)
	res = round(rand[0])

	summ = 0
	for item in prices:
		summ += item[1]
		if round(summ) >= res or len(prices) == 1:
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


# При выпадении вероятности меняет локус и завершает мутацию особи
# TODO Правильно ли написана мутация? Какая у неё вероятность?
def mutation_one_point(N, population_size, population):
	population_copy = deepcopy(population)
	mutation_set = []
	for i in range(0, population_size):
		for j in range(0, N):
			rnd = random.uniform(0, 1)
			if 0 < rnd <= 0.01:
				population_copy[i][j] = int(not population_copy[i][j])
				mutation_set.append(population_copy[i])
				break
	return mutation_set


# При выпадении вероятности генерирует область и инвертирует её
# TODO Это точно инверсия? Та же вероятность что и с хромосомной!
def mutation_inversion(N, population_size, population):
	population_copy = deepcopy(population)
	mutation_set = []
	for i in range(0, population_size):
		rnd = random.uniform(0, 1)
		if 0 < rnd <= 0.01:
			left = random.randint(1, N // 2)
			right = random.randint(N // 2 + 1, N - 1)
			for j in range(left, (left + right) // 2 + 1):
				population_copy[i][j], population_copy[i][right - j + left] = (
					population_copy[i][right - j + left], population_copy[i][j])
			mutation_set.append(population_copy[i])
	return mutation_set


# При выпадении вероятности инвертирует хромосому и продолжает просмотр
# TODO Какая необходима вероятность мутации? Текущая допускает мутацию 1 хромосомы из 50
def mutation_chromosomal(population_size, population):
	population_copy = deepcopy(population)
	mutation_set = []
	for i in range(0, population_size):
		rnd = random.uniform(0, 1)
		if 0 < rnd <= 0.01:
			mutation_set.append(list(map(lambda x: int(not x), population_copy[i])))
	return mutation_set


# Модификация генотипа таким образом, чтобы первыми выбросить наименее ценные предметы
def genotype_modification(N, w_max, things, person):
	person_copy = person.copy()
	while get_weight(N, things, person_copy) > w_max:
		minim = 1000
		minim_index = 1000
		for i in range(0, N):
			if person_copy[i] == 1 and things[i][0] < minim:
				minim = things[i][0]
				minim_index = i
		person_copy[minim_index] = 0
	return person_copy


# Отбирает g особей для переноса в следующее поколение
def selection_beta_tournament(new_population_size, new_population, g):
	g_to_new_population = []
	for i in range(0, g):
		# TODO Как мы выбираем чему равна бета?
		beta = random.randint(2, new_population_size // 2)
		tournament = random.sample(new_population, beta)
		fun_maxim_fitness_person = 0
		fun_maxim_person = tournament[0]
		for j in range(0, len(tournament)):
			fun_fit = get_fitness(N, things, tournament[j])
			if fun_fit > fun_maxim_fitness_person:
				fun_maxim_fitness_person = fun_fit
				fun_maxim_person = tournament[j]
		g_to_new_population.append(fun_maxim_person.copy())
	return g_to_new_population


# Отбор особей при помощи рулетки
# TODO Почему в этой селекции одна и та же особь может быть выбрана несколько раз?
# TODO Сколько селекция должна возвращать особей? g или ню
def selection_proportional(new_population_size, new_population, g):
	g_to_new_population = []
	prices = []
	for i in range(0, new_population_size):
		prices.append((i, get_fitness(N, things, new_population[i])))

	for i in range(0, g):
		item = roulette(prices)
		g_to_new_population.append(new_population[item[0]].copy())

	return g_to_new_population


def selection_linear_ranking(new_population_size, new_population, g):
	g_to_new_population = []
	new_population_copy = deepcopy(new_population)
	for i in range(0, new_population_size):
		for j in range(i + 1, new_population_size):
			if get_fitness(N, things, new_population_copy[i]) > get_fitness(N, things, new_population_copy[j]):
				new_population_copy[i], new_population_copy[j] = new_population_copy[j], new_population_copy[i]
	prices = []
	for i in range(0, new_population_size):
		prices.append((i, i + 1))

	for i in range(0, g):
		item = roulette(prices)
		g_to_new_population.append(new_population_copy[item[0]].copy())

	return g_to_new_population


# Получение приспособленности кодировки
def get_fitness(N, things, person):
	res = 0.0
	for i in range(0, N):
		if person[i] == 1:
			res += things[i][0] / things[i][1]
	return round(res, 2)


# Получение веса кодировки
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
	int(input("Оператор мутации:\n1) Точечная\n2) Макромутация инверсией\n3) Хромосомная\n>> ")),
	int(input("Оператор селекции:\n1) Бета-турнир\n2) Пропорциональная\n3) Линейная ранговая\n>> "))
]

# Создание начальной популяции
population = []
if operator_choices[0] == 1:
	population = create_population_random(N, population_size)
elif operator_choices[0] == 2:
	population = create_population_random_control(N, w_max, things, population_size)
elif operator_choices[0] == 3:
	population = create_population_greedy_algo(N, w_max, things, population_size)

solution = 0
t = 1
without_change_solution_counter = 0
while True:
	# Вывод всех особей поколения и наилучшей особи
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

	# Создание новой популяции
	new_population = []
	# new_population_size = population_size * 2

	# Выборка родителей и скрещивание особей для получения потомства
	# TODO Стратегия выбора родителей: рандом или мнение пользователя? (Пока рандом)
	# Рандомный выбор стратегии отбора родителей
	rand_choice = random.randint(1, 2)
	for i in range(0, population_size):
		parent1, parent2 = [], []
		if rand_choice == 1:  # Рандомный выбор родителей
			parent1, parent2 = random.sample(population, 2)
		else:  # Выбор с помощью рулетки
			prices = []
			for j in range(0, population_size):
				prices.append((j, get_fitness(N, things, population[j])))
			parent1_item = roulette(prices)
			prices.remove(parent1_item)
			parent2_item = roulette(prices)
			parent1 = population[parent1_item[0]]
			parent2 = population[parent2_item[0]]

		# Получение потомства
		child1, child2 = [], []
		if operator_choices[1] == 1:
			child1, child2 = crossover_one_point(N, parent1, parent2)
		elif operator_choices[1] == 2:
			child1, child2 = crossover_two_points(N, parent1, parent2)
		elif operator_choices[1] == 3:
			child1, child2 = crossover_homogeneous(N, parent1, parent2)
		# TODO Кроссовер даёт 2 особей, а выбрать нужно одну - как это сделать лучше? (Пока - по приспособленности)
		# TODO UPD Суть этого всего в том чтобы позже сократить кол-во особей во время отбора?
		# if get_fitness(N, things, child1) > get_fitness(N, things, child2):
		# 	new_population.append(child1)
		# else:
		# 	new_population.append(child2)
		new_population.append(child1)
		new_population.append(child2)

	# Когда новая популяция будет получена она заменит собой старую
	# TODO Наверное - пока рано
	# population = new_population

	# Мутация полученного потомства
	# TODO Должны ли мутанты заменяться сразу или просто добавляться в поколение?
	mutation_set = []
	if operator_choices[2] == 1:
		mutation_set = mutation_one_point(N, len(new_population), new_population)
	elif operator_choices[2] == 2:
		mutation_set = mutation_inversion(N, len(new_population), new_population)
	elif operator_choices[2] == 3:
		mutation_set = mutation_chromosomal(len(new_population), new_population)
	for i in mutation_set:
		new_population.append(i)

	# Обработка ограничений - модификация генотипа особей, которые не подходят под решение задачи
	for i in range(0, len(new_population)):
		if get_weight(N, things, new_population[i]) > w_max:
			new_population[i] = genotype_modification(N, w_max, things, new_population[i])

	# Подготовливаем следующее поколение
	next_population = []

	# Получение коэффициента перекрытия поколений и кол-ва особей для замены
	G = round(random.uniform(0.01, 1), 2)
	g = round(G * population_size)

	# Среди текущего поколения и репродуктивного множества скопируем самую лучшую особь в следующее поколение
	maxim_fitness_person = 0
	maxim_person = new_population[0]
	flag = 0
	for i in new_population:
		fit = get_fitness(N, things, i)
		if fit > maxim_fitness_person:
			maxim_fitness_person = fit
			maxim_person = i
			flag = 1
	for i in population:
		fit = get_fitness(N, things, i)
		if fit > maxim_fitness_person:
			maxim_fitness_person = fit
			maxim_person = i
			flag = 2
	next_population.append(maxim_person.copy())

	# TODO Кол-во потомков может быть больше кол-ва предков?
	# if flag == 1:
	# 	new_population.remove(maxim_person)
	# elif flag == 2:
	# 	population.remove(maxim_person)

	# Равновероятный отбор g особей из старой популяции для дальнейшей замены
	g_from_population = random.sample(population, g)

	# Удаляем всех отобранных особей из популяции, чтобы быстрее скопировать особи в следующее поколение
	# TODO Удалять их сейчас или потом?
	for i in g_from_population:
		population.remove(i)

	# Копируем всех остальных особей в следующее поколение
	for i in population:
		next_population.append(i.copy())

	# Применяем селекцию для отбора из репродуктивного множества g особей в следующее поколение
	# TODO Правильно ли подсчитаны числа?
	#  1 -> лучшая особь из поколения и репродуктивного множества
	#  |P^t| - g = (population_size - 1) - g -> текущая популяция без самого лучшего и g особей под замену
	#  |R^t| = g -> g особей отобранных из репродуктивного множества
	to_new_population = []
	if operator_choices[3] == 1:
		to_new_population = selection_beta_tournament(len(new_population), new_population, g)
	elif operator_choices[3] == 2:
		to_new_population = selection_proportional(len(new_population), new_population, g)
	elif operator_choices[3] == 3:
		to_new_population = selection_linear_ranking(len(new_population), new_population, g)

	for i in range(0, g):
		next_population.append(to_new_population[i].copy())

	# Смена поколения
	population = deepcopy(next_population)

	# Проверим изменилось ли решение
	maxim_fitness_person = 0
	maxim_person = population[0]
	for i in population:
		fit = get_fitness(N, things, i)
		if fit > maxim_fitness_person:
			maxim_fitness_person = fit
			maxim_person = i

	if maxim_fitness_person != solution:
		solution = maxim_fitness_person
	else:
		without_change_solution_counter += 1

	if without_change_solution_counter >= 10:
		print("Конец эволюции")
		break

	t += 1
	print()

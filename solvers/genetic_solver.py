import numpy as np
import random
import time
from .greedy_solver import _calculate_deviation


def _is_valid(x, problem):  # Перевірка точної суми видачі, Перевірка ліміту на кількість банкнот, Перевірка наявності банкнот у сховищі
    """Перевіряє валідність хромосоми."""
    return (np.sum(np.array(problem.d) * x) == problem.Q and
            np.sum(x) <= problem.P and
            np.all(x <= np.array(problem.s)))


def _create_individual(problem):
    """Створюю одну валідну особину"""
    x = np.zeros(problem.n, dtype=int)
    s_temp = np.array(problem.s)  # Створюється тимчасова копія залишків у банкоматі, щоб не псувати оригінальні дані
    current_sum = 0
    current_count = 0

    for _ in range(problem.P * 2):  # Обмеження ітерацій. Оскільки банкомат не може видати більше P банкнот, то циклу з P*2 ітерацій точно вистачить, щоб побудувати будь-який можливий розв'язок. Це гарантує, що функція колись завершиться
        possible_moves = []
        for i in range(problem.n):  # визначаю, які банкноти я можу додати
            if (current_sum + problem.d[i] <= problem.Q and
                    current_count < problem.P and s_temp[i] > 0):
                possible_moves.append(i)

        if not possible_moves: break

        move = random.choice(possible_moves)
        x[move] += 1
        s_temp[move] -= 1
        current_sum += problem.d[move]
        current_count += 1

    return x if _is_valid(x, problem) else None


def solve(problem, pop_size=50, mutation_rate=0.1, num_generations=100):
    """
    Розв'язує задачу за допомогою Генетичного алгоритму.
    Параметри ГА тепер є аргументами функції.
    """
    start_time = time.time()

    population = []
    while len(population) < pop_size:
        individual = _create_individual(problem)
        if individual is not None:
            population.append(individual)

    if not population:
        return {"solution": [], "deviation": -1, "time": time.time() - start_time}

    best_solution_overall = population[0]
    best_fitness_overall = -1

    for generation in range(num_generations):
        fitness_scores = []
        for individual in population:
            s_final = np.array(problem.s) - individual
            deviation = _calculate_deviation(s_final, problem.r)
            fitness = 1 / (1 + deviation)
            fitness_scores.append(fitness)

        new_population = []

        # зберігаємо найкращу особину
        best_idx_gen = np.argmax(fitness_scores)
        if fitness_scores[best_idx_gen] > best_fitness_overall:
            best_fitness_overall = fitness_scores[best_idx_gen]
            best_solution_overall = population[best_idx_gen]
        new_population.append(best_solution_overall.copy())

        # Заповнюємо решту популяції
        while len(new_population) < pop_size:
            # Селекція (турнірна)
            p1_idx, p2_idx = random.sample(range(len(population)), 2)
            parent1 = population[p1_idx] if fitness_scores[p1_idx] > fitness_scores[p2_idx] else population[p2_idx]

            p3_idx, p4_idx = random.sample(range(len(population)), 2)
            parent2 = population[p3_idx] if fitness_scores[p3_idx] > fitness_scores[p4_idx] else population[p4_idx]

            # Спрощенo
            child = parent1.copy()
            new_population.append(child)

        population = new_population

    final_deviation = (1 / best_fitness_overall) - 1 if best_fitness_overall > 0 else -1
    execution_time = time.time() - start_time

    return {"solution": best_solution_overall.tolist(), "deviation": final_deviation, "time": execution_time}
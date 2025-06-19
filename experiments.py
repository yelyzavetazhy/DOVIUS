import numpy as np
from tqdm import tqdm
from problem import ProblemInstance
from solvers import greedy_solver, genetic_solver
from visualization import plot_results

K_REPEATS = 5  # Кількість повторів для усереднення результатів


def _generate_random_problem(n, Q=5000, P=30):
    """Генерує випадкову задачу для експериментів."""
    possible_denominations = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    d = sorted(np.random.choice(possible_denominations, n, replace=False).tolist())
    s = np.random.randint(20, 100, size=n).tolist()
    r = np.random.rand(n)
    r = (r / np.sum(r)).tolist()
    return ProblemInstance(d, s, r, Q, P)


def _run_exp1_ga_params():
    """Експеримент 1: Дослідження параметрів ГА."""
    print("Проведення експерименту 1: Вплив параметрів ГА...")
    base_problem = _generate_random_problem(n=7)

    # Дослідження розміру популяції
    pop_sizes = [10, 20, 50, 100, 200]
    results_time = {'Час': {'x': [], 'y': []}}
    results_dev = {'Відхилення': {'x': [], 'y': []}}

    for size in tqdm(pop_sizes, desc="Дослідження розміру популяції"):
        times, deviations = [], []
        for _ in range(K_REPEATS):
            res = genetic_solver.solve(base_problem, pop_size=size)
            times.append(res['time'])
            if res['deviation'] >= 0: deviations.append(res['deviation'])

        results_time['Час']['x'].append(size);
        results_time['Час']['y'].append(np.mean(times))
        results_dev['Відхилення']['x'].append(size);
        results_dev['Відхилення']['y'].append(np.mean(deviations))

    plot_results(results_time, 'Вплив розміру популяції на час роботи ГА', 'Розмір популяції', 'Час (сек)',
                 'exp1_ga_time_vs_pop.png')
    plot_results(results_dev, 'Вплив розміру популяції на точність ГА', 'Розмір популяції', 'Середнє відхилення',
                 'exp1_ga_dev_vs_pop.png')


def _run_exp2_influence_of_p():
    """Експеримент 2: Вплив ліміту P на результат."""
    print("Проведення експерименту 2: Вплив ліміту (P)...")
    base_problem_params = {"n": 7, "Q": 4000}
    p_range = range(10, 31, 5)  # P від 10 до 30 з кроком 5

    results_time = {'Жадібний': {'x': [], 'y': []}, 'Генетичний': {'x': [], 'y': []}}
    results_dev = {'Жадібний': {'x': [], 'y': []}, 'Генетичний': {'x': [], 'y': []}}

    for p_val in tqdm(p_range, desc="Дослідження впливу P"):
        times_g, times_ga = [], []
        devs_g, devs_ga = [], []
        for _ in range(K_REPEATS):
            problem = _generate_random_problem(**base_problem_params, P=p_val)

            res_g = greedy_solver.solve(problem)
            times_g.append(res_g['time'])
            if res_g['deviation'] >= 0: devs_g.append(res_g['deviation'])

            res_ga = genetic_solver.solve(problem)
            times_ga.append(res_ga['time'])
            if res_ga['deviation'] >= 0: devs_ga.append(res_ga['deviation'])

        results_time['Жадібний']['x'].append(p_val);
        results_time['Жадібний']['y'].append(np.mean(times_g))
        results_time['Генетичний']['x'].append(p_val);
        results_time['Генетичний']['y'].append(np.mean(times_ga))
        results_dev['Жадібний']['x'].append(p_val);
        results_dev['Жадібний']['y'].append(np.mean(devs_g))
        results_dev['Генетичний']['x'].append(p_val);
        results_dev['Генетичний']['y'].append(np.mean(devs_ga))

    plot_results(results_time, 'Вплив ліміту (P) на час виконання', 'Ліміт кількості банкнот (P)', 'Час (сек)',
                 'exp2_time_vs_p.png')
    plot_results(results_dev, 'Вплив ліміту (P) на точність (відхилення)', 'Ліміт кількості банкнот (P)',
                 'Середнє відхилення', 'exp2_dev_vs_p.png')


def _run_exp3_time_vs_n():
    """Експеримент 3: Порівняння за часом."""
    print("Проведення експерименту 3: Час виконання vs Розмірність (n)...")
    n_range = range(4, 11)
    results = {'Жадібний': {'x': [], 'y': []}, 'Генетичний': {'x': [], 'y': []}}

    for n in tqdm(n_range, desc="Дослідження часу"):
        avg_times_greedy, avg_times_ga = [], []
        for _ in range(K_REPEATS):
            problem = _generate_random_problem(n=n)
            avg_times_greedy.append(greedy_solver.solve(problem)['time'])
            avg_times_ga.append(genetic_solver.solve(problem)['time'])

        results['Жадібний']['x'].append(n);
        results['Жадібний']['y'].append(np.mean(avg_times_greedy))
        results['Генетичний']['x'].append(n);
        results['Генетичний']['y'].append(np.mean(avg_times_ga))

    plot_results(results, 'Залежність часу виконання від розмірності задачі (n)', 'Кількість номіналів (n)',
                 'Середній час (сек)', 'exp3_time_vs_n.png')


def _run_exp4_accuracy_vs_n():
    """Експеримент 4: Порівняння за точністю."""
    print("Проведення експерименту 4: Точність vs Розмірність (n)...")
    n_range = range(4, 11)
    results = {'Жадібний': {'x': [], 'y': []}, 'Генетичний': {'x': [], 'y': []}}

    for n in tqdm(n_range, desc="Дослідження точності"):
        errors_greedy, errors_ga = [], []
        for _ in range(K_REPEATS):
            problem = _generate_random_problem(n=n)
            res_greedy = greedy_solver.solve(problem)
            res_ga = genetic_solver.solve(problem)

            # Пропускаю, якщо один з алгоритмів не знайшов рішення
            if res_greedy['deviation'] < 0 or res_ga['deviation'] < 0: continue

            best_dev = min(res_greedy['deviation'], res_ga['deviation'])
            if best_dev <= 1e-9: continue  # Пропускаю, якщо оптимальне відхилення близьке до 0

            errors_greedy.append((res_greedy['deviation'] - best_dev) / best_dev)
            errors_ga.append((res_ga['deviation'] - best_dev) / best_dev)

        if errors_greedy: results['Жадібний']['x'].append(n); results['Жадібний']['y'].append(np.mean(errors_greedy))
        if errors_ga: results['Генетичний']['x'].append(n); results['Генетичний']['y'].append(np.mean(errors_ga))

    plot_results(results, 'Залежність відносної похибки від розмірності задачі (n)', 'Кількість номіналів (n)',
                 'Середня відносна похибка', 'exp4_accuracy_vs_n.png')


def run_experiment(exp_id):
    """Головна функція для запуску експериментів."""
    if exp_id == 1:
        _run_exp1_ga_params()
    elif exp_id == 2:
        _run_exp2_influence_of_p()  # <--- Тепер ця функція викликається
    elif exp_id == 3:
        _run_exp3_time_vs_n()
    elif exp_id == 4:
        _run_exp4_accuracy_vs_n()
    else:
        print(f"Помилка: експеримент з ID={exp_id} не знайдено.")
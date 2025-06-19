import argparse
import json
import numpy as np
import random
from problem import ProblemInstance
from solvers import greedy_solver, genetic_solver
from experiments import run_experiment  # Імпортуємо функцію


def _generate_random_problem(n, Q, P):
    possible_denominations = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    if n > len(possible_denominations):
        raise ValueError(f"Неможливо згенерувати {n} унікальних номіналів.")
    d = sorted(random.sample(possible_denominations, n))
    s = [random.randint(10, 50) for _ in range(n)]
    r_raw = [random.random() for _ in range(n)]
    r = [val / sum(r_raw) for val in r_raw]
    return ProblemInstance(d=d, s=s, r=r, Q=Q, P=P)


def main():
    parser = argparse.ArgumentParser(description="Розв'язання задачі про видачу готівки банкоматом.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_solve = subparsers.add_parser("solve", help="Розв'язати одну задачу.")
    parser_solve.add_argument("--file", type=str, help="Шлях до JSON файлу з даними задачі.")
    parser_solve.add_argument("--random", action="store_true", help="Згенерувати випадкову задачу.")
    parser_solve.add_argument("--n", type=int, default=5, help="Кількість номіналів.")
    parser_solve.add_argument("--q", type=int, default=2000, help="Сума Q.")
    parser_solve.add_argument("--p", type=int, default=20, help="Ліміт P.")

    parser_exp = subparsers.add_parser("experiment", help="Запустити експеримент.")
    parser_exp.add_argument("--id", type=int, choices=[1, 2, 3, 4], required=True, help="ID експерименту.")

    args = parser.parse_args()

    if args.command == "solve":
        if args.file:
            problem = ProblemInstance.from_json(args.file)
        elif args.random:
            problem = _generate_random_problem(args.n, args.q, args.p)
        else:
            print("Помилка: вкажіть --file або --random."); return

        print("--- Вхідна задача ---");
        print(problem)
        print("\n--- Розв'язання Жадібним алгоритмом ---")
        greedy_result = greedy_solver.solve(problem)
        print(
            f"  Рішення: {greedy_result['solution']}\n  Відхилення: {greedy_result['deviation']:.6f}\n  Час: {greedy_result['time']:.4f} сек.")
        print("\n--- Розв'язання Генетичним алгоритмом ---")
        genetic_result = genetic_solver.solve(problem)
        print(
            f"  Рішення: {genetic_result['solution']}\n  Відхилення: {genetic_result['deviation']:.6f}\n  Час: {genetic_result['time']:.4f} сек.")

    elif args.command == "experiment":
        run_experiment(args.id)


if __name__ == "__main__":
    main()
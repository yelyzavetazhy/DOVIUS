import numpy as np
import time

def _calculate_deviation(s, r):
    """Допоміжна функція для розрахунку відхилення."""
    s_sum = np.sum(s)
    if s_sum == 0:
        return np.sum(np.array(r) ** 2)
    s_prime = s / s_sum
    return np.sum((s_prime - r) ** 2)

def solve(problem):
    """
    Розв'язую задачу за допомогою жадібного алгоритму.
    """
    start_time = time.time()

    x = np.zeros(problem.n, dtype=int)
    s_temp = np.array(problem.s)
    current_sum = 0
    current_count = 0

    while current_sum < problem.Q:
        best_denomination_idx = -1
        min_deviation = float('inf')

        for i in range(problem.n):
            # Перевірка обмежень
            if (current_sum + problem.d[i] <= problem.Q and
                    current_count < problem.P and
                    s_temp[i] > 0):

                # Гіпотетично додати банкноту
                s_temp[i] -= 1
                deviation = _calculate_deviation(s_temp, problem.r)
                s_temp[i] += 1 # Повернути стан

                if deviation < min_deviation:
                    min_deviation = deviation
                    best_denomination_idx = i

        if best_denomination_idx == -1:
            # Неможливо зробити хід
            return {"solution": x.tolist(), "deviation": -1, "time": time.time() - start_time}

        # Зробити найкращий хід
        x[best_denomination_idx] += 1
        s_temp[best_denomination_idx] -= 1
        current_sum += problem.d[best_denomination_idx]
        current_count += 1

    final_deviation = _calculate_deviation(s_temp, problem.r)
    execution_time = time.time() - start_time

    return {"solution": x.tolist(), "deviation": final_deviation, "time": execution_time}
# coursework_project/problem.py
import json

class ProblemInstance:
    """
    Клас для зберігання та управління даними однієї задачі.
    """
    def __init__(self, d, s, r, Q, P):
        self.d = d  # Вектор номіналів
        self.s = s  # Вектор початкових залишків
        self.r = r  # Вектор бажаного співвідношення
        self.Q = Q  # Сума для видачі
        self.P = P  # Ліміт на кількість банкнот
        self.n = len(d) # Кількість номіналів

    @classmethod
    def from_json(cls, filepath):
        """Завантаження даних задачі з JSON файлу."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(
            d=data['d'],
            s=data['s'],
            r=data['r'],
            Q=data['Q'],
            P=data['P']
        )

    def __str__(self):
        # Округлюємо співвідношення ТІЛЬКИ для виводу на екран
        r_rounded = [round(val, 3) for val in self.r]
        return (f"Задача:\n"
                f"  Номінали (d): {self.d}\n"
                f"  Залишки (s): {self.s}\n"
                f"  Співвідношення (r): {r_rounded}\n"
                f"  Сума (Q): {self.Q}\n"
                f"  Ліміт банкнот (P): {self.P}")
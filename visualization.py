import matplotlib.pyplot as plt
import seaborn as sns


def plot_results(results_data, title, xlabel, ylabel, filename):
    """
    Малюю та зберігаю графік з результатами експериментів.
    results_data: {'Назва алгоритму': {'x': [...], 'y': [...]}}
    """
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    for name, data in results_data.items():
        plt.plot(data['x'], data['y'], marker='o', linestyle='-', label=name)

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend()
    plt.tight_layout()

    plt.savefig(filename)
    print(f"Графік збережено у файл: {filename}")
    plt.close()
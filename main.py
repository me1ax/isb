import math
import argparse
from const import P
from scipy.special import gammaincc

def read_sequence(filename: str) -> str:
    """
    Читает последовательность из файла с обработкой ошибок.

    Args:
        filename (str): Путь к файлу, содержащему последовательность.

    Returns:
        str: Строка с последовательностью из '0' и '1' или пустая строка при ошибке.
    """
    try:
        with open(filename, 'r') as file:
            sequence = file.read().strip()
        return sequence
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return ""
    except IOError:
        print(f"Ошибка при чтении файла '{filename}'.")
        return ""


def bit_frequency_analysis(sequence: str) -> float:
    """
    Выполняет частотный побитовый тест и возвращает p-value.

    Args:
        sequence (str): Бинарная последовательность ('0' и '1').

    Returns:
        float: Значение p-value теста.
    """
    sequence_sum = 0
    length = len(sequence)

    for i in sequence:
        match i:
            case '1':
                sequence_sum += 1
            case '0':
                sequence_sum -= 1

    s_n = (1 / math.sqrt(length)) * sequence_sum
    p_value = math.erfc(s_n / math.sqrt(2))
    return p_value

def identical_consecutive_bits(sequence: str) -> float:
    """
    Выполняет тест на последовательные одинаковые биты и возвращает p-value.

    Args:
        sequence (str): Бинарная последовательность ('0' и '1').

    Returns:
        float: Значение p-value теста или 0, если условие не выполнено.
    """
    length = len(sequence)
    share_of_ones = sequence.count('1') / length

    # Проверка, чтобы условие было верно для корректных результатов
    if abs(share_of_ones - 0.5) < (2 / math.sqrt(length)):
        v_n = 0
        for i in range(length - 1):
            if sequence[i] != sequence[i + 1]:
                v_n += 1
        numerator = abs(v_n - 2 * length * share_of_ones * (1 - share_of_ones))
        denominator = 2 * math.sqrt(2 * length) * share_of_ones * (1 - share_of_ones)
        p_value = math.erfc(numerator / denominator)
        return p_value
    else:
        return 0

def longest_run_blocks_test(sequence: str, block_size: int = 8) -> float:
    """
    Выполняет тест на самую длинную последовательность единиц в блоке и возвращает p-value.

    Args:
        sequence (str): Бинарная последовательность ('0' и '1').
        block_size (int, optional): Размер блока. По умолчанию 8.

    Returns:
        float: Значение p-value теста.
    """
    # Вероятности для категорий максимальных длин
    pi = P

    # Разделение последовательности на блоки
    blocks = [sequence[i:i + block_size] for i in range(0, len(sequence), block_size)]
    v = [0, 0, 0, 0]  # категории для каждого блока

    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        # Классификация блока по длине максимальной последовательности
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        elif max_run >= 4:
            v[3] += 1

    # Вычисление chi-квадрат
    chi_square = sum(
        (v[i] - len(blocks) * pi[i]) ** 2 / (len(blocks) * pi[i]) for i in range(4)
    )

    # Возвращается p-value через gammaincc
    p_value = gammaincc(1.5, chi_square / 2)
    return p_value

def main():
    """
    Основная функция, запускающая тестирование для указанных файлов.
    
    Аргументы из командной строки:
        files (nargs='+'): список путей к файлам с последовательностями.
    
    Выводит результаты тестов по каждому файлу.
    """
    parser = argparse.ArgumentParser(description='Тестирование последовательностей по стандарту NIST.')
    parser.add_argument('files', nargs='+', help='Пути к файлам с последовательностями')
    args = parser.parse_args()

    results = {
        'frequency': {},
        'runs': {},
        'longest_run': {}
    }

    for filename in args.files:
        sequence = read_sequence(filename)
        base_name = filename.split('.')[0]  # Без расширения для отображения

        # Выполнение тестов и сохранение результатов
        results['frequency'][base_name] = bit_frequency_analysis(sequence)
        results['runs'][base_name] = identical_consecutive_bits(sequence)
        results['longest_run'][base_name] = longest_run_blocks_test(sequence)

    # Вывод результатов
    print("\nЧастотный побитовый тест:")
    for name, p_value in results['frequency'].items():
        print(f"{name}: {p_value:.6f}")

    print("\nТест на одинаковые подряд идущие биты:")
    for name, p_value in results['runs'].items():
        print(f"{name}: {p_value:.6f}")

    print("\nТест на самую длинную последовательность единиц в блоке (size=8):")
    for name, p_value in results['longest_run'].items():
        print(f"{name}: {p_value:.6f}")
        print(f"Заключение: {'Случайна' if p_value >= 0.01 else 'Неслучайна'}")


if __name__ == "__main__":
    files = ['sequence(cpp).txt', 'sequence(java).txt']
    results = {
        'frequency': {},
        'runs': {},
        'longest_run': {}
    }

    for filename in files:
        sequence = read_sequence(filename)
        base_name = filename.split('.')[0]

        # Тесты
        results['frequency'][base_name] = bit_frequency_analysis(sequence)
        results['runs'][base_name] = identical_consecutive_bits(sequence)
        results['longest_run'][base_name] = longest_run_blocks_test(sequence)

    # Вывод результатов
    print("Частотный побитовый тест:")
    for name, p_value in results['frequency'].items():
        print(f"{name}: {p_value:.6f}")

    print("\nТест на одинаковые подряд идущие биты:")
    for name, p_value in results['runs'].items():
        print(f"{name}: {p_value:.6f}")

    print("\nТест на самую длинную последовательность единиц в блоке (size=8):")
    for name, p_value in results['longest_run'].items():
        print(f"{name}: {p_value:.6f}")
        print(f"Заключение: {'Случайна' if p_value >= 0.01 else 'Неслучайна'}")
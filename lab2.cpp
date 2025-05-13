#include <iostream>
#include <random>
#include <vector>
#include <fstream>

/**
 * @brief Генерирует случайную бинарную последовательность длиной 128 элементов
 * Использует генератор случайных чисел `std::mt19937` и равномерное распределение
 * для получения чисел 0 или 1.
 * @return Вектор целых чисел (0 или 1), длиной 128.
 */
std::vector<int> generateBinarySequence() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(0, 1);

    std::vector<int> sequence;
    for (int i = 0; i < 128; ++i) {
        sequence.push_back(distrib(gen));
    }
    return sequence;
}

/**
 * @brief Основная функция программы
 * Генерирует бинарную последовательность и сохраняет её в файл "sequence(cpp).txt".
 * В случае ошибки открытия файла выводит сообщение об ошибке.
 * @return Код завершения программы, 0 — успешно, 1 — ошибка.
 */
int main() {
    auto sequence = generateBinarySequence();

    std::ofstream outFile("sequence(cpp).txt");

    if (!outFile.is_open()) {
        std::cerr << "Ошибка открытия файла!" << std::endl;
        return 1;
    }

    for (int num : sequence) {
        outFile << num;
    }

    outFile.close();
    std::cout << "Последовательность сохранена в файл sequence(cpp).txt" << std::endl;

    return 0;
}

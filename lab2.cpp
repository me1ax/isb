#include <iostream>
#include <random>
#include <vector>
#include <fstream>

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

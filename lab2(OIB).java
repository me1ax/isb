import java.io.FileWriter;
import java.io.IOException;
import java.security.SecureRandom;

/**
 * Основной класс программы для генерации бинарной последовательности и её сохранения в файл.
 */
public class Main {
    /**
     * Точка входа в программу.
     * Генерирует случайную бинарную последовательность длиной 128 и сохраняет её в файл "sequence(java).txt".
     */
    public static void main(String[] args) {
        int[] sequence = generateBinarySequence();

        // Сохранение в файл
        try (FileWriter writer = new FileWriter("sequence(java).txt")) {
            for (int bit : sequence) {
                writer.write(Integer.toString(bit));
            }
            System.out.println("Последовательность сохранена в sequence(java).txt");
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }

    /**
     * Генерирует случайную бинарную последовательность длиной 128.
     * Использует класс SecureRandom для генерации случайных чисел 0 или 1.
     * @return возвращает масив из 128 элементов, содержащий 0 или 1.
     */
    public static int[] generateBinarySequence() {
        SecureRandom random = new SecureRandom();
        int[] sequence = new int[128];
        for (int i = 0; i < 128; i++) {
            sequence[i] = random.nextInt(2); // 0 или 1
        }
        return sequence;
    }
}

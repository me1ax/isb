import java.io.FileWriter;
import java.io.IOException;
import java.security.SecureRandom;

public class Main {
    public static void main(String[] args) {
        int[] sequence = generateBinarySequence();
        
        // Сохранение в файл
        try (FileWriter writer = new FileWriter("sequence(java).txt")) {
            for (int bit : sequence) {
                writer.write(Integer.toString(bit));
            }
            System.out.println("Последовательность сохранена в sequence_java.txt");
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }

    public static int[] generateBinarySequence() {
        SecureRandom random = new SecureRandom();
        int[] sequence = new int[128];
        for (int i = 0; i < 128; i++) {
            sequence[i] = random.nextInt(2); // 0 или 1
        }
        return sequence;
    }
}
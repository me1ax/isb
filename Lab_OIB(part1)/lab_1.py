import json
from file_handler import read_text_from_file, write_text_to_file, read_key_from_json

def caesar_cipher(text: str, shift: int) -> str:
    """Шифрует текст с использованием шифра Цезаря.

    Args:
        text (str): Исходный текст для шифрования.
        shift (int): Значение сдвига для шифрования.

    Returns:
        str: Зашифрованный текст.
    """
    encrypted_text = ''
    shift_amount = shift % 33  # Обеспечиваем корректный сдвиг для алфавита

    for char in text:
        match char.isalpha():
            case True:
                match char.islower():
                    case True:
                        encrypted_text += chr(((ord(char) - ord('а') + shift_amount) % 33 + ord('а')))
                    case False:
                        encrypted_text += chr(((ord(char) - ord('А') + shift_amount) % 33 + ord('А')))
            case False:
                encrypted_text += char  # Не буквы остаются без изменений

    return encrypted_text


def caesar_decipher(text: str, shift: int) -> str:
    """Дешифрует текст с использованием шифра Цезаря.

    Args:
        text (str): Зашифрованный текст для дешифрования.
        shift (int): Значение сдвига для дешифрования.

    Returns:
        str: Дешифрованный текст.
    """
    return caesar_cipher(text, -shift)  # Дешифрование - это шифрование с отрицательным сдвигом



def main() -> None:
    """Основная функция для выполнения задания."""
    # Чтение конфигурации
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    input_file = config['input_file']
    encrypted_output_file = config['encrypted_output_file']
    key_file = config['key_file']
    min_text_length = config.get('min_text_length', 500)

    # Считывание исходного текста из файла
    original_text = read_text_from_file(input_file)

    # Проверка длины текста
    try:
        if len(original_text) < min_text_length:
            raise ValueError(f"Текст должен содержать не менее {min_text_length} символов.")
        
        # Считывание сдвига (ключа) из файла JSON
        shift = read_key_from_json(key_file)

        # Шифрование текста
        encrypted_text = caesar_cipher(original_text, shift)

        # Сохранение зашифрованного текста в файл
        write_text_to_file(encrypted_output_file, encrypted_text)

        print(f"Шифрование завершено. Сдвиг: {shift}. Результаты сохранены в файл '{encrypted_output_file}'.")

    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
from collections import Counter
import json
from file_handler import load_data_file, save_data_to_file

def calculate_char_frequencies(input_text: str) -> dict:
    """Вычисляет частоты символов в тексте."""
    cleaned_text = input_text.replace('\n', '')
    total_length = len(cleaned_text)
    char_counts = Counter(cleaned_text)
    return {char: count / total_length for char, count in char_counts.items()}

def load_alphabet_frequencies(file_path: str) -> dict:
    """Загружает частоты символов алфавита из файла JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Невозможно декодировать JSON в файле '{file_path}'.")
        return {}

def generate_mapping(encrypted_freqs: dict, alphabet_freqs: dict) -> dict:
    """Создает отображение для расшифровки текста."""
    sorted_encrypted = sorted(encrypted_freqs.items(), key=lambda item: item[1], reverse=True)
    sorted_alphabet = sorted(alphabet_freqs.items(), key=lambda item: item[1], reverse=True)

    mapping = {}
    for index in range(len(sorted_encrypted)):
        enc_char, _ = sorted_encrypted[index]
        if index < len(sorted_alphabet):
            mapping[enc_char] = sorted_alphabet[index][0]
        else:
            mapping[enc_char] = enc_char
    return mapping

def decode_text(encrypted_text: str, mapping: dict) -> str:
    """Расшифровывает текст по заданному отображению."""
    return ''.join(mapping.get(char, char) for char in encrypted_text)

def main() -> None:
    """Основная функция для выполнения анализа и дешифровки текста."""
    # Загружаем настройки
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    encrypted_content = load_data_file(config['input_file'])
    if not encrypted_content:
        print("Ошибка: Невозможно прочитать зашифрованный текст.")
        return

    char_frequencies = calculate_char_frequencies(encrypted_content)

    # Сохраняем частоты в JSON
    save_data_to_file(char_frequencies, config['output_frequencies_file'])

    alphabet_frequencies = load_alphabet_frequencies(config['alphabet_frequencies_file'])
    if not alphabet_frequencies:
        print("Ошибка: Невозможно прочитать вероятности алфавита.")
        return 

    substitution_mapping = generate_mapping(char_frequencies, alphabet_frequencies)

    print("Замена символов:")
    for enc_char, dec_char in substitution_mapping.items():
        match enc_char:
            case ' ':
                display_char = '(пробел)'
            case _:
                display_char = enc_char
        print(f"{display_char} -> '{dec_char}'")

    decrypted_content = decode_text(encrypted_content, substitution_mapping)

    # Сохраняем расшифрованный текст, который должен быть строкой
    save_data_to_file(decrypted_content, config['output_decrypted_file'])

    print("\nКонец дешифровки")

if __name__ == "__main__":
    main()

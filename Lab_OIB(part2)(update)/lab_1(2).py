from collections import Counter
from file_handler2 import load_data_file, save_data_to_file, load_config

def calculate_char_frequencies(input_text: str) -> dict:
    """Вычисляет частоты символов в тексте."""
    try:
        cleaned_text = input_text.replace('\n', '')
        total_length = len(cleaned_text)
        char_counts = Counter(cleaned_text)
        return {char: count / total_length for char, count in char_counts.items()}
    except Exception as e:
        print(f"Ошибка при вычислении частот символов: {e}")
        return {}

def load_alphabet_frequencies(file_path: str) -> dict:
    """Загружает частоты символов алфавита из файла JSON."""
    try:
        return load_config(file_path)
    except Exception as e:
        print(f"Ошибка при загрузке частот алфавита: {e}")
        return {}

def generate_mapping(encrypted_freqs: dict, alphabet_freqs: dict) -> dict:
    """Создает отображение для расшифровки текста."""
    try:
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
    except Exception as e:
        print(f"Ошибка при генерации отображения замены: {e}")
        return {}

def decode_text(encrypted_text: str, mapping: dict) -> str:
    """Расшифровывает текст по заданному отображению."""
    try:
        return ''.join(mapping.get(char, char) for char in encrypted_text)
    except Exception as e:
        print(f"Ошибка при дешифровке текста: {e}")
        return ""

def main() -> None:
    """Основная функция для выполнения анализа и дешифровки текста."""
    try:
        # Загружаем настройки
        config = load_config('config2.json')
        if not config:
            return  # Прерываем выполнение, если конфигурация не загружена

        # Загружаем зашифрованный текст
        try:
            encrypted_content = load_data_file(config['input_file'])
            if not encrypted_content:
                print("Ошибка: Невозможно прочитать зашифрованный текст.")
                return
        except Exception as e:
            print(f"Ошибка при загрузке зашифрованного текста: {e}")
            return

        # Вычисляем частоты символов
        try:
            char_frequencies = calculate_char_frequencies(encrypted_content)
            # Сохраняем частоты в JSON
            save_data_to_file(char_frequencies, config['output_frequencies_file'])
        except Exception as e:
            print(f"Ошибка при вычислении или сохранении частот символов: {e}")
            return

        # Загружаем частоты алфавита
        try:
            alphabet_frequencies = load_alphabet_frequencies(config['alphabet_frequencies_file'])
            if not alphabet_frequencies:
                print("Ошибка: Невозможно прочитать вероятности алфавита.")
                return
        except Exception as e:
            print(f"Ошибка при загрузке частот алфавита: {e}")
            return

        # Генерируем отображение замены
        try:
            substitution_mapping = generate_mapping(char_frequencies, alphabet_frequencies)
        except Exception as e:
            print(f"Ошибка при генерации отображения замены: {e}")
            return

        # Отображаем замену символов
        print("Замена символов:")
        for enc_char, dec_char in substitution_mapping.items():
            match enc_char:
                case ' ':
                    display_char = '(пробел)'
                case _:
                    display_char = enc_char
            print(f"{display_char} -> '{dec_char}'")

        # Дешифруем текст
        try:
            decrypted_content = decode_text(encrypted_content, substitution_mapping)
            # Сохраняем расшифрованный текст
            save_data_to_file(decrypted_content, config['output_decrypted_file'])
        except Exception as e:
            print(f"Ошибка при дешифровке текста: {e}")
            return

        print("\nКонец дешифровки")

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()

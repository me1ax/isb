import os
import json

def read_text_from_file(file_path: str) -> str:
    """Считывает текст из файла.
    
    Args:
        file_path (str): Путь к файлу для чтения.

    Returns:
        str: Содержимое файла или пустая строка в случае ошибки.
    """
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Файл '{file_path}' не найден.")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    except (FileNotFoundError, IOError) as e:
        print(f"Ошибка чтения файла: {e}")
        return ""
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return ""


def write_text_to_file(file_path: str, text: str) -> None:
    """Записывает текст в файл.
    
    Args:
        file_path (str): Путь к файлу для записи.
        text (str): Текст для записи в файл.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def read_key_from_json(file_path: str, default_shift: int = 3) -> int:
    """Считывает ключ шифрования из файла JSON.
    
    Args:
        file_path (str): Путь к файлу JSON.
        default_shift (int, optional): Значение сдвига по умолчанию. По умолчанию 3.

    Returns:
        int: Значение сдвига.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            key_data = json.load(file)
        return key_data.get('shift', default_shift)  # Возвращает значение сдвига или значение по умолчанию
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return default_shift  # Возвращаем значение по умолчанию
    
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return default_shift  # Возвращаем значение по умолчанию при любом другом исключении

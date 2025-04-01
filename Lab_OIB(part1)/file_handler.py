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
    
    except FileNotFoundError as e:
        print(e)
        return ""
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
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

def read_key_from_json(file_path: str) -> int:
    """Считывает ключ шифрования из файла JSON.
    
    Args:
        file_path (str): Путь к файлу JSON.

    Returns:
        int: Значение сдвига, по умолчанию 3.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            key_data = json.load(file)
        return key_data.get('shift', 3)  # Возвращает значение сдвига или 3 по умолчанию, если ключ не указан
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return 3  # Возвращаем значение по умолчанию

import json

def load_data_file(file_path: str) -> str:
    """Загружает содержимое файла.

    :param file_path: Путь к файлу.
    :return: Строка с содержимым файла.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return ""
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
        return ""

def save_data_to_file(data, file_path: str) -> None:
    """Сохраняет данные в файл в формате JSON для словарей, в текстовом формате для строк."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            if isinstance(data, dict):
                json.dump(data, file, ensure_ascii=False, indent=4)  # Сериализация словаря в JSON
            else:
                file.write(data)  # Запись строки в файл
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")

def load_config(file_path: str) -> dict:
    """Загружает конфигурацию из файла JSON.

    :param file_path: Путь к файлу конфигурации.
    :return: Словарь с конфигурационными данными.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Невозможно декодировать JSON в файле '{file_path}'.")
        return {}
    except Exception as e:
        print(f"Произошла ошибка при загрузке конфигурации: {e}")
        return {}

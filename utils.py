"""
Вспомогательные функции для загрузки конфигурации и сериализации ключей.
"""

import json
import os

from cryptography.hazmat.primitives import serialization


def load_settings(settings_path='settings.json'):
    """
    Загружает настройки из JSON файла.
    """
    if not os.path.exists(settings_path):
        raise FileNotFoundError(f"Файл настроек {settings_path} не найден")
    with open(settings_path, 'r') as f:
        return json.load(f)


def serialize_key(key, path, key_type):
    """
    Сериализует ключ в файл, если файл не существует.
    """
    if os.path.exists(path):
        print(f"Файл {path} уже существует, пропуск сериализации.")
        return

    print(f"Сериализация ключа {key_type} в {path}...")
    output_dir = os.path.dirname(path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    match key_type:
        case 'symmetric':
            with open(path, 'wb') as f:
                f.write(key)
        case 'public':
            with open(path, 'wb') as f:
                f.write(
                    key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                )
        case 'private':
            with open(path, 'wb') as f:
                f.write(
                    key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                )
        case _:
            raise ValueError(f"Неверный тип ключа: {key_type}")

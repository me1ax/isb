"""
Модуль симметричного шифрования с использованием алгоритма SEED (128 бит).
"""

import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_symmetric_key():
    """
    Генерирует 128-битный ключ для SEED.
    """
    print("Генерация симметричного ключа SEED...")
    return os.urandom(16)


def encrypt_file(input_path, output_path, sym_key):
    """
    Шифрует файл с помощью SEED.
    """
    print(f"Шифрование файла {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Входной файл {input_path} не найден")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    iv = os.urandom(16)  # Инициализационный вектор
    cipher = Cipher(algorithms.SEED(sym_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    with open(input_path, 'rb') as f:
        plaintext = f.read()
    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_text) + encryptor.finalize()

    with open(output_path, 'wb') as f:
        f.write(iv + ciphertext)
    print(f"Зашифрованный файл сохранен в {output_path}")


def decrypt_file(input_path, output_path, sym_key):
    """
    Расшифровывает файл с помощью SEED.
    """
    print(f"Расшифровка файла {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Зашифрованный файл {input_path} не найден")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_path, 'rb') as f:
        data = f.read()
    iv, ciphertext = data[:16], data[16:]

    cipher = Cipher(algorithms.SEED(sym_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_text = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    plaintext = unpadder.update(padded_text) + unpadder.finalize()

    with open(output_path, 'wb') as f:
        f.write(plaintext)
    print(f"Расшифрованный файл сохранен в {output_path}")

"""
Модуль асимметричного шифрования с использованием RSA и OAEP.
"""

import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def generate_asymmetric_keys():
    """
    Генерирует пару ключей RSA.
    """
    print("Генерация пары ключей RSA...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_symmetric_key(sym_key, public_key, path):
    """
    Шифрует симметричный ключ с помощью RSA-OAEP.
    """
    print("Шифрование симметричного ключа...")
    output_dir = os.path.dirname(path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    encrypted_key = public_key.encrypt(
        sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(path, 'wb') as f:
        f.write(encrypted_key)
    print(f"Зашифрованный симметричный ключ сохранен в {path}")


def decrypt_symmetric_key(encrypted_key_path, private_key_path):
    """
    Расшифровывает симметричный ключ.
    """
    print("Расшифровка симметричного ключа...")
    if not os.path.exists(encrypted_key_path):
        raise FileNotFoundError(
            f"Файл зашифрованного ключа {encrypted_key_path} не найден")
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(
            f"Файл закрытого ключа {private_key_path} не найден")

    with open(encrypted_key_path, 'rb') as f:
        encrypted_key = f.read()
    with open(private_key_path, 'rb') as f:
        private_key = load_pem_private_key(f.read(), password=None)

    sym_key = private_key.decrypt(
        encrypted_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return sym_key

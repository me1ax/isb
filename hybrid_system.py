"""
Гибридная криптосистема, комбинирующая SEED и RSA.
"""

from asymmetric_crypt import decrypt_symmetric_key
from asymmetric_crypt import encrypt_symmetric_key
from asymmetric_crypt import generate_asymmetric_keys
from symmetric_crypt import decrypt_file
from symmetric_crypt import encrypt_file
from symmetric_crypt import generate_symmetric_key
from utils import serialize_key


def generate_keys(settings):
    """
    Генерирует и сохраняет ключи, указанные в настройках.
    """
    sym_key = generate_symmetric_key()
    private_key, public_key = generate_asymmetric_keys()

    serialize_key(public_key, settings['public_key'], 'public')
    serialize_key(private_key, settings['secret_key'], 'private')
    encrypt_symmetric_key(sym_key, public_key, settings['symmetric_key'])
    print('Генерация ключей завершена.')


def encrypt_data(settings):
    """
    Шифрует данные.
    """
    sym_key = decrypt_symmetric_key(
        settings['symmetric_key'],
        settings['secret_key']
    )
    encrypt_file(
        settings['initial_file'],
        settings['encrypted_file'],
        sym_key
    )
    print('Шифрование данных завершено.')


def decrypt_data(settings):
    """Расшифровывает данные."""
    sym_key = decrypt_symmetric_key(
        settings['symmetric_key'],
        settings['secret_key']
    )
    decrypt_file(
        settings['encrypted_file'],
        settings['decrypted_file'],
        sym_key
    )
    print('Расшифровка данных завершена.')

"""
Основная точка входа для гибридной криптосистемы.
"""

import argparse

from hybrid_system import decrypt_data
from hybrid_system import encrypt_data
from hybrid_system import generate_keys
from utils import load_settings


def main():
    """
    Обрабатывает аргументы командной строки.
    """
    parser = argparse.ArgumentParser(description='Гибридная криптосистема')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-gen',
        '--generation',
        action='store_true',
        help='Запускает режим генерации ключей'
    )
    group.add_argument(
        '-enc',
        '--encryption',
        action='store_true',
        help='Запускает режим шифрования'
    )
    group.add_argument(
        '-dec',
        '--decryption',
        action='store_true',
        help='Запускает режим расшифровки'
    )

    args = parser.parse_args()

    try:
        settings = load_settings()
        mode = 'generation' if args.generation else 'encryption' if args.encryption else 'decryption'
        match mode:
            case 'generation':
                generate_keys(settings)
            case 'encryption':
                encrypt_data(settings)
            case 'decryption':
                decrypt_data(settings)
    except FileNotFoundError as e:
        print(f'Ошибка: {e}')
        exit(1)
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        exit(1)


if __name__ == '__main__':
    main()
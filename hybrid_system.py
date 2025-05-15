from asymmetric_crypt import decrypt_symmetric_key, encrypt_symmetric_key, generate_asymmetric_keys
from symmetric_crypt import decrypt_file, encrypt_file, generate_symmetric_key
from utils import serialize_key


def generate_keys(settings):
    """
    Генерирует и сохраняет ключи, указанные в настройках.
    """
    try:
        required_keys = ['public_key', 'secret_key', 'symmetric_key']
        for key in required_keys:
            if key not in settings:
                raise KeyError(f"Ключ '{key}' отсутствует в настройках.")

        sym_key = generate_symmetric_key()
        private_key, public_key = generate_asymmetric_keys()

        serialize_key(public_key, settings['public_key'], 'public')
        serialize_key(private_key, settings['secret_key'], 'private')
        encrypt_symmetric_key(sym_key, public_key, settings['symmetric_key'])
        print('Генерация ключей завершена.')

    except KeyError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка при генерации ключей: {e}")


def encrypt_data(settings):
    """
    Шифрует данные.
    """
    try:

        required_keys = ['symmetric_key', 'secret_key', 'initial_file', 'encrypted_file']
        for key in required_keys:
            if key not in settings:
                raise KeyError(f"Ключ '{key}' отсутствует в настройках.")


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

    except KeyError as e:
        print(f"Ошибка: {e}")
    except FileNotFoundError:
        print("Ошибка: Один из указанных файлов не найден.")
    except Exception as e:
        print(f"Произошла ошибка при шифровании данных: {e}")


def decrypt_data(settings):
    """
    Расшифровывает данные.
    """
    try:

        required_keys = ['symmetric_key', 'secret_key', 'encrypted_file', 'decrypted_file']
        for key in required_keys:
            if key not in settings:
                raise KeyError(f"Ключ '{key}' отсутствует в настройках.")

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

    except KeyError as e:
        print(f"Ошибка: {e}")
    except FileNotFoundError:
        print("Ошибка: Один из указанных файлов не найден.")
    except Exception as e:
        print(f"Произошла ошибка при расшифровке данных: {e}")



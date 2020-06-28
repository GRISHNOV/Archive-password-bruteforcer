from zipfile import *
import time
import sys
from src.progress.bar import IncrementalBar


def load_password_list(file_path: str) -> list:
    with open(file_path, 'r') as f:
        return f.read().splitlines()


def zip_bruteforce_process(file_path: str, password_list: list) -> None:
    with ZipFile(file_path, 'r') as zip:
        start_time = time.time()
        attempt_counter = 1
        bar = IncrementalBar('Passwords checked', max=len(password_list))
        for password_iterator in password_list:
            try:
                zip.read(zip.namelist()[0], pwd=bytes(password_iterator, 'utf-8'))
            except RuntimeError as ex:
                if 'Bad password' in str(ex):
                    attempt_counter += 1
                    bar.next()
                else:
                    raise Exception('Exception: fail trying to determine the result of applying password')
            except BadZipFile as ex:
                if 'Bad CRC' in str(ex):
                    attempt_counter += 1
                    bar.next()
                else:
                    raise Exception('Exception: fail trying to determine the result of applying password')
            else:
                print("\n")
                print("speed: ", len(password_list) / (time.time() - start_time), " pass/sec")
                print("total time: ", time.time() - start_time, " seconds")
                print('RESULT: complete, the password is ===> ', password_iterator)
                exit()
            finally:
                pass

        bar.finish()
        print("\n")
        print("speed: ", len(password_list) / (time.time() - start_time), " pass/sec")
        print("total time: ", time.time() - start_time, " seconds")
        print('RESULT: fail, no password in dict')


if __name__ == "__main__":
    ZIP_FILE_NAME = ''
    PWD_FILE_NAME = ''

    password_list = load_password_list(PWD_FILE_NAME)

    if is_zipfile(ZIP_FILE_NAME):
        print('\n')
        print("Bruteforce process:")
        zip_bruteforce_process(ZIP_FILE_NAME, password_list)
    else:
        print('not zip!')

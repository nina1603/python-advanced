import sys
from os import system


# Напишите декоратор, который будет перенаправлять вывод функции в файл.
# Подсказка: вы можете заменить объект sys.stdout каким-нибудь другим объектом.
def redirect_output(filepath):
    def decorator(function):
        def wrapper(*args, **kwargs):
            original_stdout = sys.stdout
            sys.stdout = open(filepath, 'w')
            function(*args, **kwargs)
            sys.stdout = original_stdout
            sys.stdout.close()
        return wrapper
    return decorator


@redirect_output('./function_output.txt')
def calculate():
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


if __name__ == "__main__":
    calculate()
    system("function_output.txt")

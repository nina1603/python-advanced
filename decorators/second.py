import sys
from first import my_write


# Упакуйте только что написанный код в декоратор.
# Весь вывод функции должен быть помечен временными метками так, как видно выше.
def timed_output(function):
    def wrapper(*args, **kwargs):
        original_write = sys.stdout.write
        sys.stdout.write = my_write
        function(*args, **kwargs)
        sys.stdout.write = original_write
    return wrapper


@timed_output
def print_greeting(name):
    print(f'Hello, {name}!')


if __name__ == "__main__":
    print_greeting("Nikita")
    print_greeting("everyone")

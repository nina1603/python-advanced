import sys
import datetime
import pytz

sys_only_write = sys.stdout.write # for not to break everything
original_write = sys.stdout.write


# Для начала, давайте подменим метод write у объекта sys.stdin на такую функцию, которая
# перед каждым вызовом оригинальной функции записи данных в stdout допечатывает к тексту текущую метку времени.
def my_write(string_text):
    if string_text == '\n':
        return
    add_current_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))\
        .strftime('[%Y-%m-%d %H:%M:%S]: ')
    string = f"{add_current_time}{string_text}\n"
    return original_write(string)


if __name__ == "__main__":
    sys.stdout.write = my_write
    print('1, 2, 3')
    sys.stdout.write = original_write
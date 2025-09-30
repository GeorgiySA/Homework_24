import re
from typing import List, Iterable


def my_handler(cmd: str, val: str, data: Iterable[str]) -> List[str]:
    """
    Обрабатывает данные согласно команде
        cmd: команда (filter, map, limit, unique, sort, regex)
        val: значение для команды
        data: список строк или итератор
    return:
        Обработка данных в виде списка строк
    """
    if cmd == "filter":
        res = list(filter(lambda line: val in line, data))
    elif cmd == "map":
        res = [line.split()[int(val)] for line in data if len(line.split()) > int(val)]
    elif cmd == "limit":
        res = list(data)[:int(val)]
    elif cmd == "unique":
        res = list(set(data))
    elif cmd == "sort":
        is_reverse = val == "desc"
        res = sorted(data, reverse=is_reverse)
    elif cmd == "regex":
        regexp: re.Pattern = re.compile(val)
        res =  list(filter(lambda line: regexp.findall(line), data))
    else:
        raise ValueError(f"Неизвестная команда: {cmd}")

    return res
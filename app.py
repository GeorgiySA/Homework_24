import os
from typing import List, Optional
from flask import Flask, abort, request, jsonify

from utils import my_handler

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/perform_query")
def perform_query() -> jsonify:
    # Получение параметров
    cmd1: Optional[str] = request.args.get("cmd1")
    val1: Optional[str] = request.args.get("val1")
    cmd2: Optional[str] = request.args.get("cmd2")
    val2: Optional[str] = request.args.get("val2")
    file_name: Optional[str] = request.args.get("file_name")
    # Проверка обязательных параметров
    if not all([cmd1, val1, file_name]):
        abort(400, "Необходимо указать: cmd1, val1 и file_name")
    # Проверка существования файла
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        abort(404, "Указанный файл не найден")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data: List[str] = file.read().splitlines()
        # Проверка первой команды
        result: List[str] = my_handler(cmd1, val1, data)
        # Проверка второй команды (если указана)
        if cmd2 and val2:
            result = my_handler(cmd2, val2, result)

        return jsonify(result)

    except ValueError as e:
        abort(400, f"Ошибка в параметрах: {str(e)}")
    except Exception as e:
        abort(500, f"Внутренняя ошибка сервера: {str(e)}")

if __name__ == "__main__":
    app.run()

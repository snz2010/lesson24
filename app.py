import os
from functions import query_builder, get_commands
from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest
from typing import Optional, Union

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=["POST", "GET"])
def perform_query() -> Union[Response, BadRequest]:
    # нужно взять код из предыдущего ДЗ добавить команду regex
    # добавить типизацию в проект, чтобы проходила утилиту mypy app.py
    if request.method == "POST":
        # получить параметры query и file_name
        try:
            cmd1: Optional[str] = request.form.get("cmd1")
            cmd2: Optional[str] = request.form.get("cmd2")
            val1: Optional[str] = request.form.get("value1")
            val2: Optional[str] = request.form.get("value2")
            file_name: Optional[str] = request.form.get("file_name")
        except KeyError:
            raise BadRequest(description="не все параметры переданы корректно")
    elif request.method == "GET":
        query_str = request.args.get("query")
        if query_str:
            ret_list, file_name = get_commands(query_str)
            (cmd1, val1) = ret_list[0]
            (cmd2, val2) = ret_list[1]
    # проверить, что файл file_name существует в папке DATA_DIR
    if file_name:
        file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"файл {file_name} не найден")

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    with open(file_path) as f:
        res = query_builder(f, cmd1, val1)
        res = query_builder(res, cmd2, val2)
        content = '\n'.join(res)
        print(content)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run()
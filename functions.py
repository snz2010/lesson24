import re
from typing import Any, Tuple, Iterator, Optional

def query_builder(iterable_var: Iterator, cmd: str, val: str) -> Any:
    result = map(lambda v: v.strip(), iterable_var)
    if cmd == "filter":
        result = filter(lambda v, txt=val: txt in v, result)
    if cmd == "map":
        arg = int(val)
        result = map(lambda v, idx=arg: v.split(" ")[idx], result)
    if cmd == "unique":
        result = set(result)
    if cmd == "sort":
        reverse = val == "desc"
        result = sorted(result, reverse=reverse)
    if cmd == "limit":
        arg = int(val)
        result = list(result)[:arg]
    if cmd == 'regex':
        regex = re.compile(val)
        return filter(lambda v: regex.search(v), iterable_var)
    return result


def get_commands(query: Optional[str]) -> Tuple:
    cmd = []
    arg = []
    filename = ''
    query_items = query.split("|")
    for item in query_items:
        if item == 'unique':
            cmd.append('unique')
            arg.append('')
        elif 'file_name' in item:
            filename = item.split("=")[1]
        else:
            split_item = item.split(":")
            cmd.append(split_item[0])
            arg.append(split_item[1])
    ret_list = list(zip(cmd, arg))
    return (ret_list, filename)
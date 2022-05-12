import re
from collections.abc import Iterable
from typing import Optional, List
def query_builder(iterable_var: Iterable, cmd: Optional[str], val: Optional[str]) -> Iterable:
    mapped_data = map(lambda v: v.strip(), iterable_var)
    if cmd == 'unique':
        return set(mapped_data)
    if val:
        if cmd == 'filter':
            return filter(lambda v: val in v, mapped_data)
        elif cmd == 'regex':
            regex = re.compile(val)
            return filter(lambda v: regex.search(v), iterable_var)
        elif cmd == 'map':
            arg = int(val)
            return map(lambda v: v.split(" ")[arg], mapped_data)
        elif cmd == 'limit':
            arg = int(val)
            return list(mapped_data)[:arg]
        elif cmd == 'sort':
            reverse = val == "desc"
            return sorted(mapped_data, reverse=reverse)
    return mapped_data


def get_commands(query: str) -> tuple:
    cmd: List[str] = []
    arg: List[str] = []
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
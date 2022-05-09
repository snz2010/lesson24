import re
from typing import Any, Tuple, Iterator, Optional, Union, List

def query_builder(iterable_var: Union[Iterator[Any], List[Any]], cmd: Optional[str], val: Optional[str]) -> Union[Iterator]:
    result = map(lambda v: v.strip(), iterable_var)
    if cmd == "unique":
        result = set(result)
    if val:
        if cmd == "filter":
            result = filter(lambda v, txt=val: txt in v, result)
        elif cmd == 'regex':
            regex = re.compile(val)
            return filter(lambda v: regex.search(v), iterable_var)
        elif cmd == "map":
            arg = int(val)
            result = map(lambda v, idx=arg: v.split(" ")[idx], result)
        elif cmd == "limit":
            arg = int(val)
            result = list(result)[:arg]
        elif cmd == "sort":
            reverse = val == "desc"
            result = sorted(result, reverse=reverse)
    return result


def get_commands(query: str) -> Tuple:
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
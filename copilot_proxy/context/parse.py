from typing import List


def find_str_n(s: str, sub: str, n: int) -> int:
    """查找字符串第n次出现的位置"""
    if not s or not sub or n <= 0:
        return -1
    count = 0
    index = -1
    while count < n:
        index = s.find(sub, index + 1)
        if index == -1:
            return -1
        count += 1
    return index


def r_find_str_n(s: str, sub: str, n: int) -> int:
    """查找字符串第n次出现的位置"""
    if not s or not sub or n <= 0:
        return -1
    count = 0
    index = -1
    while count < n:
        index = s.rfind(sub, 0, index)
        if index == -1:
            return -1
        count += 1
    return index


def parse_relation(data: List) -> List:
    """解析关系检索结果
    Args:
        data: 关系检索结果
    Returns:
        List: 解析后的结果 [(file_path,content,score),]
    """
    if not data:
        return []
    result = []
    # TODO 解析关系检索结果
    return []


def slice_before_nth_instance(s: str, sub: str, n: int) -> str:
    """字符串第n次出现位置之前的内容,如果没有出现,返回整个字符串"""
    index = find_str_n(s, sub, n)
    if index == -1:
        return s
    return s[:index]


def r_slice_before_nth_instance(s: str, sub: str, n: int) -> str:
    """字符串从右搜索，第n次出现位置前的内容，如果没有出现,返回整个字符串"""
    index = r_find_str_n(s, sub, n)
    if index == -1:
        return s
    return s[:index]


def slice_after_nth_instance(s: str, sub: str, n: int) -> str:
    """字符串第n次出现位置之后的内容,如果没有出现,返回整个字符串"""
    index = find_str_n(s, sub, n)
    return s[index+1:]


def r_slice_after_nth_instance(s: str, sub: str, n: int) -> str:
    """字符串从右搜索，第n次出现位置之后的内容,如果没有出现, 返回整个字符串"""
    index = r_find_str_n(s, sub, n)
    return s[index+1:]


def parse_semantic(data: List, n: int = -1) -> List:
    """解析语义检索结果,返回得分最高的n个,并去重
    Args:
        data: 语义检索结果
        n: 返回结果数量, 默认返回所有结果
    Returns:
        List: 解析后的结果 [(file_path,content,score),]
    """
    if not data:
        return []
    result = []
    context_set = {}
    for item in data:
        if not item or not isinstance(item, dict):
            continue
        semantic_list = item.get("data", {}).get("list", [])
        if not isinstance(semantic_list, list):
            continue
        for semantic in semantic_list:
            if not semantic or not isinstance(semantic, dict):
                continue
            # 获取到相似代码的信息
            content = semantic.get("content", "")  # 取前3行
            if context_set.get(content, False):
                continue
            else:
                context_set[content] = True
            # 导出前10行, 暂时不裁剪,全量保留
            # content = slice_before_nth_instance(content, "\n", 10)
            file_path = semantic.get("filePath", "")
            score = semantic.get("score", 0)
            result.append((file_path, content, score))
    # result 按照score 从高到低排序
    result.sort(key=lambda x: x[2], reverse=True)
    if n > 0:
        result = result[:n]
    return result


def parse_definition(data: List) -> List:
    """解析定义检索结果
    Args:
        data: 定义检索结果
    Returns:
        List[Tuple[str, str, str]: 解析后的结果 [(name, file_path,content),]
    """
    if not data:
        return []
    result = []
    context_set = {}
    # 遍历多个请求返回的结果
    for item in data:
        if not item or not isinstance(item, dict):
            continue
        def_list = item.get("data", {}).get("list", [])
        if not isinstance(def_list, list):
            continue
        # 遍历每个结果的响应中list中的结果
        for def_item in def_list:
            if not def_item or not isinstance(def_item, dict):
                continue
            # 提取 filePath, name, content
            file_path = def_item.get("filePath", "")
            name = def_item.get("name", "")
            content = def_item.get("content", "")
            def_type = def_item.get("type", "")
            # content不为空,做提取处理
            if content:
                # 根据类型, 提取不同的内容,declaration 开头是临时的,之后统一是definition
                match def_type:
                    case "definition.method" | "definition.function" | "declaration.method" | "declaration.function" :
                        # content = content[:find_str_n(content, "\n", 10)+1]  # 方法取前10行
                        content = slice_before_nth_instance(content, "\n", 20)
                    # 类或者结构体,
                    case "definition.class" | "definition.struct" | "declaration.struct" | "declaration.class":
                        # content = content[:find_str_n(content, "\n", 30)+1]  # 类结构体取前50行
                        content = slice_before_nth_instance(content, "\n", 50)
                    case _:
                        # content = content[:find_str_n(content, "\n", 5)+1]  # 其他取前5行
                        content = slice_before_nth_instance(content, "\n", 10)
            # 去重
            key = "{}:{}".format(file_path, name)
            if context_set.get(key, False):
                continue
            else:
                context_set[key] = True
                result.append((name, file_path, content))
    return result

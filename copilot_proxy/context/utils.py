def get_code_first_n_lines(s: str, n: int) -> list[str]:
    """获取代码的前 n 行,忽略空白字符行"""
    if not s or n <= 0:
        return []

    lines = []
    start = 0
    length = len(s)

    while start < length and len(lines) < n:
        end = s.find('\n', start)
        if end == -1:
            # 没有更多的换行符，把剩下的作为一行加入
            lines.append(s[start:].strip())
            break
        else:
            # 包含 \n 前的内容
            line = s[start:end].strip()
            if line:
                lines.append(line)
        start = end + 1
    return lines


def get_code_last_n_lines(s: str, n: int) -> list[str]:
    """获取代码的后 n 行,忽略空白字符行"""
    if not s or n <= 0:
        return []

    lines = []
    start = len(s)
    end = start
    while start > 0 and len(lines) < n:
        start = s.rfind('\n', 0, start)
        if start == -1:
            # 没有更多的换行符，把剩下的作为一行加入
            lines.append(s[0:end].strip())
            break
        else:
            # 包含 \n 前的内容
            line = s[start + 1:end].strip()
            if line:
                lines.append(line)
        end = start
    lines.reverse()
    return lines

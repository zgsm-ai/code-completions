import os


# 各种语言添加注释的函数


def comment_with_hash(code: str) -> str:
    """适用于 # 注释风格的语言"""
    return '\n'.join(f'# {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_slash(code: str) -> str:
    """适用于 // 注释风格的语言"""
    return '\n'.join(f'// {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_dash(code: str) -> str:
    """适用于 Lua 的 -- 注释风格"""
    return '\n'.join(f'-- {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_double_dash(code: str) -> str:
    """适用于 SQL、Haskell 等使用 '--' 的语言"""
    return '\n'.join(f'-- {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_double_hash(code: str) -> str:
    """适用于 Dockerfile 使用 ## 注释（虽非标准）"""
    return '\n'.join(f'## {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_exclamation(code: str) -> str:
    """适用于 Batch 文件使用 @REM 注释"""
    return '\n'.join(f'@REM {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_percent(code: str) -> str:
    """适用于 TeX/LaTeX 注释 %"""
    return '\n'.join(f'% {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_semicolon(code: str) -> str:
    """适用于 Lisp、Prolog、INI 等用 ; 注释的语言"""
    return '\n'.join(f'; {line}' if line.strip() else '' for line in code.splitlines())


def comment_with_star(code: str) -> str:
    """适用于多行注释风格如 /* ... */ 的语言（简单前缀添加）"""
    return '/*\n' + code + '\n*/'


def comment_with_markdown(code: str) -> str:
    """适用于 Markdown 等使用 Markdown 语法的语言"""
    return '\n'.join(f'<!-- {line} -->' if line.strip() else '' for line in code.splitlines())


# 默认处理函数
def default_commenter(code: str) -> str:
    return comment_with_hash(code)


ext_map = {
    # 使用 '#' 注释的语言
    '.py': comment_with_hash,
    '.sh': comment_with_hash,
    '.rb': comment_with_hash,
    '.pl': comment_with_hash,  # Perl
    '.tcl': comment_with_hash,  # Tcl
    '.r': comment_with_hash,  # R script
    '.R': comment_with_hash,
    '.mak': comment_with_hash,  # Makefile (尽管有些是 #! 但大多数用 #)

    # 使用 '//' 注释的语言
    '.c': comment_with_slash,
    '.h': comment_with_slash,
    '.cpp': comment_with_slash,
    '.cc': comment_with_slash,
    '.hpp': comment_with_slash,
    '.java': comment_with_slash,
    '.js': comment_with_slash,
    '.ts': comment_with_slash,
    '.go': comment_with_slash,
    '.rs': comment_with_slash,
    '.kt': comment_with_slash,
    '.swift': comment_with_slash,
    '.cs': comment_with_slash,  # C#
    '.m': comment_with_slash,  # Objective-C
    '.scala': comment_with_slash,  # Scala
    '.groovy': comment_with_slash,  # Groovy

    # 使用 '--' 注释的语言
    '.lua': comment_with_dash,

    # 使用 '--' 或类似单行注释的语言
    '.sql': comment_with_double_dash,  # SQL
    '.hs': comment_with_double_dash,  # Haskell
    '.vhd': comment_with_double_dash,  # VHDL

    # 使用 '##' 或特殊注释的语言（自定义）
    '.dockerfile': comment_with_double_hash,

    # 使用 '@REM' 注释的语言（Windows Batch）
    '.bat': comment_with_exclamation,
    '.cmd': comment_with_exclamation,

    # 使用 '%' 注释的语言
    '.tex': comment_with_percent,
    '.sty': comment_with_percent,
    '.cls': comment_with_percent,

    # 使用 ';' 注释的语言
    '.lisp': comment_with_semicolon,
    '.el': comment_with_semicolon,  # Emacs Lisp
    '.pro': comment_with_semicolon,  # Prolog
    '.ini': comment_with_semicolon,
    '.cfg': comment_with_semicolon,

    # 多行注释风格（简单模拟）
    '.php': comment_with_star,  # PHP 支持 /* */
    '.css': comment_with_star,  # CSS
    '.scss': comment_with_star,  # Sass/SCSS

    # 标签注释
    '.html': comment_with_markdown,
    '.md': comment_with_markdown,

    # 其他未识别的后缀，默认使用 '#'
}


def get_comment(file_path: str, code: str) -> str:
    """根据文件扩展名选择合适的注释函数，并返回注释后的代码。
    Args:
        file_path (str): 文件路径
        code (str): 代码字符串
    Returns:
        str: 注释后的代码字符串
    """
    if not code:
        return ''
    _, ext = os.path.splitext(file_path)
    global ext_map
    comment_func = ext_map.get(ext, default_commenter)
    return comment_func(code)

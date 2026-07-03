#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统命令工具 — 本地执行 shell 命令
（代码运行在服务器上，直接用 subprocess）
"""

import subprocess
import re

from config import PING_TIMEOUT


def run_command(command: str, timeout: int = PING_TIMEOUT) -> tuple[str, str]:
    """
    本地执行 shell 命令。

    Returns:
        (stdout, stderr)
    """
    try:
        result = subprocess.run(
            command, shell=True,
            capture_output=True, text=True,
            timeout=timeout,
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "命令执行超时"
    except FileNotFoundError:
        return "", f"命令不可用: {command.split()[0]}"


def ping_host(target: str, count: int = 4) -> tuple[str, str | None]:
    """
    Ping 目标主机，返回完整输出和平均延迟。

    Returns:
        (ping_output, avg_rtt_str_or_None)
    """
    out, err = run_command(f"ping -c {count} -W 3 {target}", timeout=PING_TIMEOUT)

    if err and not out:
        return err, None

    avg_rtt = None
    match = re.search(r"rtt.*=\s*[\d.]+/([\d.]+)/[\d.]+/[\d.]+\s*ms", out)
    if match:
        avg_rtt = match.group(1) + " ms"
    return out, avg_rtt

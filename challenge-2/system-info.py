#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import time
from pathlib import Path


def human_size(size):
    value = float(size)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024:
            return f"{value:.1f}{unit}"
        value = value / 1024
    return f"{value:.1f}PB"


def run(command):
    return subprocess.run(command, text=True, capture_output=True, check=False)


def disk_stats():
    print("Disk stats")
    print("Volume\tFilesystem\tTotal\tUsed\tFree\tUse%\tMount")

    result = run(["df", "-PT"])
    for line in result.stdout.strip().splitlines()[1:]:
        volume, filesystem, _blocks, _used, _available, _percent, mountpoint = line.split(maxsplit=6)

        if not os.path.isdir(mountpoint):
            continue

        usage = shutil.disk_usage(mountpoint)
        used_percent = (usage.used / usage.total) * 100

        print(
            f"{volume}\t"
            f"{filesystem}\t"
            f"{human_size(usage.total)}\t"
            f"{human_size(usage.used)}\t"
            f"{human_size(usage.free)}\t"
            f"{used_percent:.1f}%\t"
            f"{mountpoint}"
        )


def read_cpu_times():
    with open("/proc/stat", "r", encoding="utf-8") as stat:
        values = stat.readline().split()[1:]
        numbers = [int(value) for value in values]

    idle = numbers[3] + numbers[4]
    total = sum(numbers)
    return idle, total


def cpu_usage():
    idle_before, total_before = read_cpu_times()
    time.sleep(1)
    idle_after, total_after = read_cpu_times()

    idle_delta = idle_after - idle_before
    total_delta = total_after - total_before

    if total_delta == 0:
        return 0.0

    return 100 * (1 - idle_delta / total_delta)


def cpu_frequency():
    cpuinfo = Path("/proc/cpuinfo").read_text(encoding="utf-8")

    for line in cpuinfo.splitlines():
        if line.startswith("cpu MHz"):
            return f"{float(line.split(':')[1].strip()):.0f} MHz"

    return "unknown"


def cpu_stats():
    print("CPU stats")
    print(f"Cores: {os.cpu_count()}")
    print(f"Usage: {cpu_usage():.1f}%")
    print(f"Frequency: {cpu_frequency()}")


def ram_stats():
    values = {}

    with open("/proc/meminfo", "r", encoding="utf-8") as meminfo:
        for line in meminfo:
            key, value = line.split(":", 1)
            values[key] = int(value.strip().split()[0]) * 1024

    total = values["MemTotal"]
    free = values.get("MemAvailable", values["MemFree"])
    used = total - free
    used_percent = (used / total) * 100

    print("RAM stats")
    print(f"Total: {human_size(total)}")
    print(f"Used: {human_size(used)}")
    print(f"Free: {human_size(free)}")
    print(f"Used percentage: {used_percent:.1f}%")


def listening_ports():
    print("Listening ports")

    command = shutil.which("ss")
    if command:
        result = run([command, "-tuln"])
        print(result.stdout.strip())
        return

    command = shutil.which("netstat")
    if command:
        result = run([command, "-tuln"])
        print(result.stdout.strip())
        return

    print("Neither ss nor netstat was found.")


def overview():
    print("Top 10 processes by CPU usage")

    result = run(["ps", "-eo", "pid,comm,%cpu,%mem", "--sort=-%cpu"])
    lines = result.stdout.strip().splitlines()

    for line in lines[:11]:
        print(line)


def main():
    parser = argparse.ArgumentParser(
        prog="system-info.py",
        description="Get basic Linux system information",
    )
    parser.add_argument("-d", "--disk", action="store_true", help="check disk stats")
    parser.add_argument("-c", "--cpu", action="store_true", help="check cpu stats")
    parser.add_argument("-p", "--ports", action="store_true", help="check listen ports")
    parser.add_argument("-r", "--ram", action="store_true", help="check ram stats")
    parser.add_argument(
        "-o",
        "--overview",
        action="store_true",
        help="top 10 process with most CPU usage",
    )

    args = parser.parse_args()
    selected = [args.disk, args.cpu, args.ports, args.ram, args.overview]

    if not any(selected):
        parser.print_help()
        return

    if args.disk:
        disk_stats()
    if args.cpu:
        cpu_stats()
    if args.ports:
        listening_ports()
    if args.ram:
        ram_stats()
    if args.overview:
        overview()


if __name__ == "__main__":
    main()

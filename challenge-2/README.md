# Challenge 2

I created a Python script called `system-info.py` to show basic system information from a Linux machine.

The script uses only Python standard libraries and common Linux files/commands, such as `/proc`, `ps`, `ss` and `df`-like disk information.

## How to run

From this directory:

`cd challenge-2`

Give execution permission:

`chmod +x system-info.py`

Show help:

`./system-info.py --help`

## Options

| Option | What it does |
| --- | --- |
| `-d`, `--disk` | shows disk volumes, total, used, free and used percentage |
| `-c`, `--cpu` | shows CPU cores, usage and frequency |
| `-p`, `--ports` | shows listening ports |
| `-r`, `--ram` | shows RAM total, used, free and used percentage |
| `-o`, `--overview` | shows the top 10 processes by CPU usage |

## Commands used to test

Disk:

`./system-info.py --disk`

CPU:

`./system-info.py --cpu`

Listening ports:

`./system-info.py --ports`

RAM:

`./system-info.py --ram`

Top 10 processes by CPU:

`./system-info.py --overview`

All checks together:

`./system-info.py --disk --cpu --ports --ram --overview`

## Short explanation

I kept the script dependency-free to make it easy to run on a Linux server.

For disk, CPU and RAM, the script reads information from Linux system files under `/proc` and from mounted filesystems.

For listening ports, it uses `ss -tuln` when available. If `ss` is not installed, it tries `netstat -tuln`.

For the process overview, it uses `ps` sorted by CPU usage and prints the first 10 processes.

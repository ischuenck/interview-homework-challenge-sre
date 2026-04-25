# Challenge 4

I tested this challenge inside a Linux container because the binary was compiled for x86_64 Linux.

## Tools used

I used an Ubuntu container and installed the tools below:

`apt-get update`

`apt-get install -y file binutils strace`

The packages were needed for:

| Package | Command used |
| --- | --- |
| `file` | `file` |
| `binutils` | `strings` |
| `strace` | `strace` |

## Clean test

To reproduce the issue from zero, I copied only the binary to a temporary directory:

`mkdir /tmp/challenge-4-test`

`cp blackbox /tmp/challenge-4-test/`

`cd /tmp/challenge-4-test`

`chmod +x blackbox`

Running the binary without any extra file returns the error message:

`./blackbox`

Result:

`Ooooh, what's wrong? :(`

## Inspection

First I checked the binary type:

`file blackbox`

Result:

`ELF 64-bit LSB pie executable, x86-64`

Then I looked for readable strings inside the binary:

`strings -a blackbox`

The relevant strings were:

`the_magic_filez.txt`

`Congrats! :)`

`Ooooh, what's wrong? :(`

That showed a likely filename the binary was expecting.

To confirm the file check, I used `strace`:

`strace ./blackbox`

The important line was:

`access("the_magic_filez.txt", F_OK) = -1 ENOENT (No such file or directory)`

This means the program checks if `the_magic_filez.txt` exists, but the file was missing.

## Fix

I created the expected file in the same directory as the binary:

`touch the_magic_filez.txt`

Then I ran the binary again:

`./blackbox`

Result:

`Congrats! :)`

I also confirmed the system call succeeds after the fix:

`strace ./blackbox`

Expected line:

`access("the_magic_filez.txt", F_OK) = 0`

## Final state

The fix is included in this directory by adding:

`the_magic_filez.txt`

So running `./blackbox` from `challenge-4` now returns:

`Congrats! :)`

# Challenge 1

I solved this challenge from the `challenge-1` directory using basic Linux commands.

Command used to check the file size:

`wc -l sample.log`

Result:

`3660 sample.log`

The log has this format:

`[date] user - protocol status "method path"`

Example:

`[21/Dec/2021:17:37:06] debbie - HTTP/1.0 200 "GET /index.html"`

I used `awk` with spaces and double quotes as separators:

`awk -F '[ "]+'`

With that, the log can be read by fields:

| Field | Meaning |
| --- | --- |
| `$2` | user |
| `$5` | HTTP status code |
| `$6` | HTTP method |
| `$7` | path |

## 1. Count all lines with 500 HTTP code

Command:

`awk -F '[ "]+' '$5 == 500' sample.log | wc -l`

Result:

`714`

## 2. Count all GET requests from yoko to /rrhh with status 200

Command:

`awk -F '[ "]+' '$2 == "yoko" && $5 == 200 && $6 == "GET" && $7 == "/rrhh"' sample.log | wc -l`

Result:

`4`

## 3. Count all requests to /

Command:

`awk -F '[ "]+' '$7 == "/"' sample.log | wc -l`

Result:

`717`

## 4. Count all lines without 5XX HTTP code

Command:

`awk -F '[ "]+' '$5 < 500 || $5 > 599' sample.log | wc -l`

Result:

`2191`

## 5. Replace 503 HTTP codes by 500 and count 500 requests

Command:

`sed 's/ 503 / 500 /g' sample.log | awk -F '[ "]+' '$5 == 500' | wc -l`

Result:

`1469`

This command only changes the output sent to the pipe. It does not change the original `sample.log` file.

## Final answers

| Question | Answer |
| --- | ---: |
| Lines with HTTP code 500 | 714 |
| GET requests from yoko to /rrhh with status 200 | 4 |
| Requests to / | 717 |
| Lines without 5XX HTTP code | 2191 |
| 500 requests after replacing 503 with 500 | 1469 |

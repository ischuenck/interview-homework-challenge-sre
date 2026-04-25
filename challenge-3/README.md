# Challenge 3

I created a Dockerfile to run the Python HTTP server from `server.py`.

The server listens on port `8080`.

I also copied the `challenge-2/system-info.py` script into the same image, so the container can be used to test both Challenge 2 and Challenge 3.

## Build the image

From the repository root:

`docker build -f challenge-3/Dockerfile -t orcrist-server .`

## Run the container

`docker run --rm --name orcrist-server-test -p 8080:8080 orcrist-server`

## Test the server

Without the expected header:

`curl -i http://localhost:8080`

Result:

`Wrong header!`

With the expected header:

`curl -i -H "Challenge: orcrist.org" http://localhost:8080`

Result:

`Everything works!`

## Answer

The result of making a `GET` request with the header `Challenge: orcrist.org` is:

`Everything works!`

## Test Challenge 2 inside the same container

Enter the running container:

`docker exec -it orcrist-server-test bash`

Run the system info script:

`./system-info.py --help`

`./system-info.py --disk`

`./system-info.py --cpu`

`./system-info.py --ports`

`./system-info.py --ram`

`./system-info.py --overview`

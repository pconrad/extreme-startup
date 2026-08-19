# Getting Started with "Extreme Startup"

## What is "Extreme Startup"

Here is the explanation that is embedded inside the game:

> Extreme Startup is a software development game / workshop that allows players or teams to compete against each other to code and deliver new features, and score points for doing so. The game is an interactive learning experience while also being fun and engaging. Extreme Startup revolves around the theme of satisfying market demand by encouraging players to stay alert and adapt to frequently changing requests for service.
>
> The main outline of Extreme Startup is that a number of players deploy an API end-point, register that end-point with the game server, and then the game server starts sending them requests. Their API end-point should then respond to each request, and if they respond correctly they score points. Each game has a number of rounds, where new types of requests are given when the round increments. When the game ends, the player / team with the most points wins!
> 
> In order to play Extreme Startup you will need a pipeline and an API end-point ready to deploy. Throughout the game you will be continously developing your API to handle different types of requests. Every time there is a new round, expect new questions!


## Getting Started


The first step is to get the server running.  That's covered in the README.md, so this guide
will focus just on game mechanics.

Once you have the server running on some host and port, open
a web browser, and you should see this:

<img width="438" height="292" alt="image" src="https://github.com/user-attachments/assets/a1b936bf-12ee-462f-b1fa-6b63b15a161a" />

Clicking "Learn More", gives you this screen:

<img width="578" height="537" alt="image" src="https://github.com/user-attachments/assets/3dcfed35-0283-4b0a-8ea4-8c6d66dacde1" />

## Creating a Game

When you click the `Create a Game` button, this dialog pops up:

<img width="415" height="184" alt="image" src="https://github.com/user-attachments/assets/13f89612-7344-4c50-b211-da96b7006c8a" />

So, enter a password, and click `Create Game`. Then you'll see this:

<img width="405" height="202" alt="image" src="https://github.com/user-attachments/assets/359a6f52-34ab-4072-9170-05bc180cf301" />

Now it starts to get interesting.  When you click `To Game Page`, you see this:

<img width="969" height="519" alt="image" src="https://github.com/user-attachments/assets/e53197ca-a2a8-4250-a0fe-c23a97a2870f" />

Let's unpack all the parts of this page.

The menu icon, upper left, expands into this:

<img width="171" height="249" alt="image" src="https://github.com/user-attachments/assets/d255a6d4-3d68-47b8-9374-66c416d91319" />

`Admin Page` leads you right back to the first page we showed above.

`Leaderboard` shows a page like this initially; it will be populated with more content once players start playing the game.  It is common practice to display this page on a screen visible to all of the players when the game is being played in a workshop setting.

<img width="848" height="621" alt="image" src="https://github.com/user-attachments/assets/0932b799-59a9-4240-9145-c32885c0a535" />

The third menu option, `Players`, shows this page, also initially empty:

<img width="844" height="268" alt="image" src="https://github.com/user-attachments/assets/22b8041e-aea1-48eb-b935-e095e0ed18c3" />

There's just one button here: `Withdraw All`.  We'll cover what that does later on.

## Instructions for Players

Once a game has been created, players can join the game by clicking the `Join Game` button.

But before you can join, you need a server.  It needs to:

* Listen for http web requests (preferably, any verb, any route, any parameters) at some address and port that the server can reach.
* Print out information about those on stdout so that you can inspect it and decide what to do next in the game
* Returns a blank response with status code 200 for everything (at least initially)

This is the only way that a player can figure out what their next move in the game is supposed to be.

Code for some "starter" servers appears below.

TODO: If the server is running on localhost, then the game client can run on localhost as well.  But it would be better
to setup a more realistic scenario for the final version of these instructions.

Suppose you have a starter program, and you run it on http://0.0.0.0:12345.

Then you can join the game like this:

<img width="612" height="371" alt="image" src="https://github.com/user-attachments/assets/96628789-b41e-4a82-b676-a0a4ea3a3d05" />

Hit enter, and the next thing you will see is something like this:

<img width="978" height="787" alt="image" src="https://github.com/user-attachments/assets/309575da-c096-4e50-a801-78d6a5662bc5" />

As you can see, your server is receiving events, and it is not responding the way the "customer" expects.

Your next move is to adjust your server.   Without giving too much away, let's suppose you have adjusted your server to respond by sending back an HTTP response containing a name:



## A simple Python starter program

Here is a simple zero-dependency Python3 program that 

* takes a port number as it's command line parameter,
* listens for http requests on that port at any route, any verb, any parameters
* for each route and verb, it logs the verb, route and parameters on stdout,
* and then returns a blank response with status code 200.


```python
import sys
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestLoggerHandler(BaseHTTPRequestHandler):
    def process_request(self):
        # Extract HTTP verb and parse the URL path and query parameters
        verb = self.command
        parsed_url = urllib.parse.urlparse(self.path)
        route = parsed_url.path
        
        # parse_qs converts the query string into a dict of key-list pairs
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Log details to stdout
        print("\n" + "=" * 40)
        print(f"VERB:       {verb}")
        print(f"ROUTE:      {route}")
        print(f"PARAMETERS: {query_params}")

        # If a body payload exists (e.g., POST/PUT JSON or form data), log it as well
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode("utf-8", errors="replace")
            print(f"BODY:       {body}")
        print("=" * 40)

        # Send an empty 200 OK response
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    # Catch-all mechanism for standard HTTP methods
    do_GET = process_request
    do_POST = process_request
    do_PUT = process_request
    do_DELETE = process_request
    do_PATCH = process_request
    do_HEAD = process_request
    do_OPTIONS = process_request

    # Catch-all mechanism for any non-standard HTTP methods
    def __getattr__(self, name):
        if name.startswith("do_"):
            return self.process_request
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    # Override standard logging to prevent noise on stderr
    def log_message(self, format, *args):
        pass


def run():
    if len(sys.argv) < 2:
        print("Usage: python http_logger.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Error: Port must be a valid integer.")
        sys.exit(1)

    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, RequestLoggerHandler)
    
    print(f"🚀 Server listening on http://0.0.0.0:{port} ... (Press Ctrl+C to stop)")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    run()
```

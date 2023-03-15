import urllib.request
import sys

# check an AnkiConnect availability.
# To check Anki is running, use another test.

try:
    # TODO : import port from elsewhere.
    urllib.request.urlopen("http://127.0.0.1:8765").getcode()
    print("AnkiConnect is available", file=sys.stdout)
    # exit(0) make the test fail.
except:
    print("AnkiConnect is not available", file=sys.stderr)
    exit(1)

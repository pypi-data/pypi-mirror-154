![WebServerIdentifier logo](https://mauricelambert.github.io/info/python/security/WebServerIdentifier_small.png "WebServerIdentifier logo")

# WebServerIdentifier

## Description

This package identifies Web servers using an aggressive technique based on the maximum size of the URI. In some configurations this technique can even identify web servers placed behind a proxy web server without any identifiable content.

For more information about this technique, please read this [PDF](https://www.slideshare.net/MauriceLambert1/webmaxuriidentifierpdf) ([github.io](https://mauricelambert.github.io/info/python/security/Web-MaxUriIdentifier.pdf)).

This technique performs an in depth identification with certain configurations. An example is available at the [bottom of this README](https://github.com/mauricelambert/WebServerIdentifier#in-depth-identification).

## Requirements

This package require:
 - python3
 - python3 Standard Library
 - PythonToolsKit

## Installation

```bash
pip install WebServerIdentifier
```

## Usages

### Command lines

```bash
python3 -m WebServerIdentifier -h                    # Use python module
python3 WebServerIdentifier.pyz --help               # Use python executable

WebIdentify -d -v -m HEAD identify 127.0.0.1         # Use console script entry point
WebIdentify -i 1 identify 127.0.0.1:8000             # Spoof multiple targets (verbose mode)
WebIdentify -m HEAD getmaxuri 127.0.0.1:8000         # Spoof range of targets
WebIdentify -d -v -m HEAD -i 1 getmaxuri 127.0.0.1   # Spoof all network

WebIdentify 127.0.0.1 127.0.0.0/29 -s -t 1   # Semi (spoof only gateway IP for the targets, interval is 1 seconds)
WebIdentify 127.0.0.1 127.0.0.0/29 -i 127.0. # Use the loopback interface

WebIdentify 172.16.10.1 172.16.0.33 -p       # Passive mode
```

### Python3

```python
from WebServerIdentifier import WebServerIdentifier, _create_unverified_context

identifier = WebServerIdentifier("127.0.0.1", baseuri="/", ssl=True, context=_create_unverified_context(), port=8000, interval=0.5, timeout=2)
identifier = WebServerIdentifier("127.0.0.1")

response = identifier.request()
response.status
response.reason

r = identifier.request(method="HEAD", size=65535)
r.status
r.reason

for size, r in identifier.get_max_URI_size():
    print(size, r.status, r.reason)

for size, r in identifier.get_max_URI_size(method="HEAD"): pass

for r, size, servers in identifier.identify_server(): pass

for r, size, servers in identifier.identify_server(method="HEAD"):
    print(size, r.status, r.reason, servers)

server = server.pop()
```

## In depth identification

In this example, we have a ruby web server protected by an NGINX web proxy. The maximum ruby web server URI size is 2015 characters and the maximum NGINX web proxy URI size is 6132 characters. It is possible to detect the ruby web server without any specific content, this screenshot proves it:

![In depth Indentifaction - Screenshot](https://mauricelambert.github.io/info/python/security/InDepthIdentification.png "In depth Indentifaction")

## Links

 - [Github Page](https://github.com/mauricelambert/WebServerIdentifier)
 - [Pypi](https://pypi.org/project/WebServerIdentifier/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/WebServerIdentifier.html)
 - [Executable](https://mauricelambert.github.io/info/python/security/WebServerIdentifier.pyz)
 - [PDF](https://www.slideshare.net/MauriceLambert1/webmaxuriidentifierpdf) ([github.io](https://mauricelambert.github.io/info/python/security/Web-MaxUriIdentifier.pdf)))

## Help

```text
usage: WebServerIdentifier.py [-h] [--method METHOD] [--baseuri BASEURI] [--interval INTERVAL] [--ssl] [--timeout TIMEOUT] [--verbose] [--debug] {identify,getmaxuri} target

This package identifies target's web server.

positional arguments:
  {identify,getmaxuri}  Identify the target's web server or get the maximum size of the URI.
  target                Host targeted (examples: 10.101.10.101:8000, example.com)

optional arguments:
  -h, --help            show this help message and exit
  --method METHOD, -m METHOD
                        HTTP method to request the Web Server
  --baseuri BASEURI, -b BASEURI
                        Base URI to request the target.
  --interval INTERVAL, -i INTERVAL
                        Requests interval.
  --ssl, -s             Use HTTPS (SSL, encryption).
  --timeout TIMEOUT, -t TIMEOUT
                        Set timeout for HTTP requests.
  --verbose, -v         Active verbose mode.
  --debug, -d           Active debugging mode (set level debug for all loggers).
```

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
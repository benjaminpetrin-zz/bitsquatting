BITSQUATTING
===========

This repository includes a simple toy DNS server written in Python3 for use in
conducting research in bitsquatting (`bitsquat_dns.py`). It also includes a
helper script for generating the necessary permutations of a domain
(`domain_gen.py`). The remainder of this README includes further documentation
of the included DNS server, and a brief summary of my results running this on
the web for a period in 2015.

What is Bitsquatting
-----------

Bitsquatting is "DNS Hijacking without
exploitation"[1](http://dinaburg.org/bitsquatting.html). A term coined by
Artem Dinaburg to refer to the act of registering domains that are 1-bit off
from some other legitimate domain in order to capture traffic that was destined
for the legitimate domain but became corrupted and ended up on the alternate domain.

Bitsquatting is due to an error on the part of the connecting client machine and not
anything the operator of a domain can explicitly protect against except by
purchasing additional domains. The more popular a website is, the more likely a
connecting client may accidentally connect to some other domain on accident. 

This is due to corruption in memory (or potentially transmission) and it is
distinct from a typo made by a user (and therefor different from the more
well-known practice of typosquatting). A good candidate domain name for
bitsquatting is one that is both popular and not one visited by a user
explicitly (that is, a domain that is not commonly navigated to in a web
browser by a user). For example, "facebook.com" would not be a good candidate
but fbcdn.net would be as it is the domain Facebook uses to host static
resources that are embedded on facebook.com).

The DNS Server
-----------

The included DNS server (`bitsquat_dns.py`) will bind to port 53 and answer DNS
queries. All actions will be logged to `dns.log` in the same directory. It is
single threaded and meant for low traffic but will suffice in the simplest of
cases and could be expanded for others. You must specify the domain variants
the server should answer for and the IP address that should be handed out as an
answer. For each query it will give out an A record for both the corrupted
domain and the (likely) correct domain. It will answer with REFUSED for other
domains and log packets it couldn't decode.


Other requirements
-----------

You will also need to run a webserver that can log all HTTP requests that come
in over the IP address specified in the DNS server. A simple NGINX
configuration file works well for this.

Jan-Mar 2015 Results
-----------
Check out a brief overview of my results [here](http://petrin.me/bitsquatting.html)

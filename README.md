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

In the beginning of 2015 I purchased 10 variants of the domain 2mdn.net which
is owned and operated by Google for its ad network (formerly, DoubleClick).
This represents a good slice of the 19 valid domains that are a single bit off
from 2mdn.net:

 * 2-dn.net
 * 2edn.net
 * 2ldn.net
 * 2mdf.net
 * 2mdj.net
 * 2mdl.net
 * 2mdo.net
 * 2mln.net
 * 2mtn.net
 * 3mdn.net

The DNS server operated for the months of January, February and March for a
total of about 90 days. Additionally, NGINX was used to record and log out all
HTTP requests. A 404 was returned for every request.

The HTTP logs were analyzed to determine instances of bitsquatting taking place
(filtering out instances of web-crawlers, exploit scanners, and likely
web-browsers navigating to one of the domains manually).  As one of these
domains was previously operated out of China, there was no shortage of spider
traffic attempting to reach old pages on one of the domains as well as
automated scans that appear to be related to operating a web-presence behind
the Great Firewall.

With that filtering in place, and over the course of 90 days there were a total
of 113 requests made for ad-related Javascript, images, swfs, and other assets
across the 10 domains and from 108 distinct IPs scattered around the world. The
overwhelming majority of requests were for Javascript assets (100 requests in
total). A few Requets are reproduced below

```
s0.2mtn.net "GET /879366/flash_inpage_rendering_lib_200_66.js HTTP/1.1" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gesko) Chrome/41.0.2272.89 Safari/537.36"
s0.3mdn.net "GET /ads/studio/cached_libs/modernizr_2.8.3_ec185bb44fe5e6bf7445d6e8ef37ed0e_no-classes.js?_veri=20121009 HTTP/1.1" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)"
s0.2mdl.net "GET /instream/video/client.js?cHVzaA=14673 HTTP/1.1" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
```

Occasionally you can spot other bit-flips as part of the request (note the
"inpaee" is one bit off of "inpage")

```
s0.2mdl.net "GET /879366/dfa7banner_flash_html_inpaee_rendering_lib_200_68.js?cHVzaA=11151 HTTP/1.1" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)"
```

This phenomena might be useful in determining when some intermediate machine or
even the original web server was responsible for the errors and propagated the
error to multiple machines. The following URL was requested 32 times by
separate IPs/Agents.

```
"GET /ads/studim/cached_libs/modernizr_2.8.3_ec185bb44fe5e6bf7455d6e8ef37ed0e_no-classes.js?_veri=20121009 HTTP/1.1"
```

Notice the second one-bit error "studim" vs "studio". All IPs requesting this
malformed URL originated behind China Telecom, potentially indicating some
regional cache or proxy propagating an error. That said, some of these 32
requests were for different one-bit variations of the domain name so there are
potentially a few ways to interpret this. In Artem Dinaburg's DefCon 19 talk he
observed more obvious instances of an error being cached and propagated as huge
spikes in activity.

Across all confirmed bitsquatted requests the following Host headers were
observed by the web server

* s0.2-dn.net
* s0.2edn.net
* s0.2ldn.net
* s0.2mdf.net
* s0.2mdj.net
* s0.2mdl.net
* s0.2mdo.net
* s0.2mln.net
* s0.2mtn.net
* s0.3mdn.net
* s0qa.2mtn.net
* s1.2mdl.net
* s1.2mln.net
* s8.2mdo.net
* r14---sn-nx57yney.c.2mdn.net
* r3---sn-25g7sne7.c.2mdl.net

The second to last one is the most interesting, as it includes the correct
domain (2mdn.net). This happened only once. When I cross reference that request
with the DNS log (by time and subdomain, as the IP address seen from the DNS
server will be of the recursive resolver and not the originator of the HTTP
request) I can see the domain queried on the DNS server was in fact
r14---sn-nx57yney.c.2-dn.net.

Final thoughts
------------

This data shows that single bit errors in domain names continue to take place
in 2015. In retrospect, the use of an ad network domain was probably poorly
chosen due to the provenance of ad-blockers. Despite that, with an average
request once per day there is plenty of interesting data to be observed.

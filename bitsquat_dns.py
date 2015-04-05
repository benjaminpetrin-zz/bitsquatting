import datetime
import socketserver
import logging

from dnslib import DNSRecord, DNSHeader, RCODE, RR, A

LOG_FILENAME = 'dns.log'
logging.basicConfig(
    filename=LOG_FILENAME,level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)


class DNSHandler(socketserver.BaseRequestHandler):
    """
        A simple, singlethreaded, UDP-only DNS toy
        server for bitsquatting research
    """

    domain = "2mdn.net."        # domain we expect client actually intended
    ip = "104.236.102.121"      # The IP we will hand out in all cases
    ttl = 86400                 # ttl to hand out, be sticky
    domain_variants = {         # 1-bit variants of the above domain we will respond to
        "2-dn.net.",
        "2edn.net.",
        "2ldn.net.",
        "2mdf.net.",
        "2mdj.net.",
        "2mdl.net.",
        "2mdo.net.",
        "2mln.net.",
        "2mtn.net.",
        "3mdn.net.",
    }

    def name_to_subdomain_and_domain(self, name):
        parts = name.split(".")
        domain = ".".join(parts[-3:])
        subdomain = ".".join(parts[0:-3])
        return (subdomain, domain)

    def handle(self):
        socket = self.request[1]

        # gather up details on the request
        client_address = self.client_address[0]
        data = self.request[0].strip()
        try:
            request = DNSRecord.parse(data)
        except:
            logging.info("Couldn't parse query from {}:{}".format(client_address, data))
            return

        qname = str(request.q.qname)
        subdomain, domain = self.name_to_subdomain_and_domain(qname)

        reply = None
        if domain in self.domain_variants or domain == self.domain:
            # formulate answer with record for both the 1-bit variant and the intended domain

            intended_domain = self.domain
            if subdomain:
                intended_domain = subdomain + "." + self.domain

            logging.info("Request from {} for {}".format(client_address, qname))
            reply = DNSRecord(
                        DNSHeader(id=request.header.id, qr=1, aa=2, ra=1),
                        q=request.q,
                    )
            reply.add_answer(RR(qname,rdata=A(self.ip), ttl=self.ttl))
            reply.add_answer(RR(intended_domain,rdata=A(self.ip), ttl=self.ttl))
        else:
            # client is querying a domain we don't expect, send REFUSED
            logging.info("Request from {} for {} REFUSED".format(client_address, qname))
            reply = DNSRecord(
                        DNSHeader(id=request.header.id, qr=1, rcode=RCODE.REFUSED),
                        q=request.q
                    )

        socket.sendto(reply.pack(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 53
    server = socketserver.UDPServer((HOST, PORT), DNSHandler)

    # in case anything unexpected happens
    while True:
        logging.info("Listening on {}:{}".format(HOST, PORT))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Shutting down gracefully")
            server.shutdown()
            break
        except:
            logging.exception("crashed, will restart...")


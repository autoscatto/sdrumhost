#!/usr/bin/env python
import requests
import StringIO
import os
sdrumo_tmp = '/tmp/hosts.sdrumo'

urls = [
    "http://hosts-file.net/ad_servers.asp",
    "http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext",
    "http://winhelp2002.mvps.org/hosts.txt",
    "https://adaway.org/hosts.txt"
]
url_l = len(urls)
big_l = []

preheader = '''### This hosts file is generated by sdrumhost
### This file is generated from the following sources:
'''
header = '''127.0.0.1	    localhost
# The following lines are desirable for IPv6 capable hosts
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

'''


def get_and_parse(u):
    resp = requests.get(u)
    if resp.ok:
        return StringIO.StringIO(resp.text)
    else:
        return None

if __name__ == "__main__":
    for idx, url in enumerate(urls):
        t = get_and_parse(url)
        if t is not None:
            preheader += "#{}\n".format(url)
            print "parsing source %d/%d - OK" % (idx, url_l)
            for line in t:
                if not line.startswith('#'):
                    big_l.append(line.replace('0.0.0.0', '127.0.0.1   ').replace('\n', ''))

    big_l = set(big_l)
    with open(sdrumo_tmp, 'wt') as outf:
        outf.write(preheader+"\n"+header+"###\n\n")
        for entry in big_l:
            outf.write(entry)

    ret = os.system('sudo mv %s /etc/hosts' % sdrumo_tmp)
    if ret == 0:
        print "Hosts file created"
    else:
        print "Drama! " + u"\u2620"

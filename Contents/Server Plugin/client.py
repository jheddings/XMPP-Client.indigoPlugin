#!/usr/bin/env python
# Indigo command line wrapper for the JabberBot (mostly for debugging purposes)

import logging

from optparse import OptionParser
from bot import JabberBot

################################################################################
logging.basicConfig(level=logging.DEBUG)

parser = OptionParser()
parser.add_option("-S", "--server", dest="server", default="talk.google.com")
parser.add_option("-P", "--port", dest="port", type="int", default=5222)
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)

(options, args) = parser.parse_args()

uname = args[0]
passwd = args[1]
server = options.server
port = options.port
debug = options.verbose

JabberBot(uname, passwd, server, port, debug).start()


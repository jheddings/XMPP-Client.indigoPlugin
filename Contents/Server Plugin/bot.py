################################################################################
# XMPP bot to handle messages and perform useful actions with Indigo

import xmpp

import strings

from jarvis import Jarvis

################################################################################
class JabberBot:
    connection = None
    jarvis = None

    #---------------------------------------------------------------------------
    def __init__(self, username, password, server, port=5222, debug=False):
        jid = xmpp.JID(username)

        debugFlags = ["always"] if debug else [ ]

        self.connection = xmpp.Client(jid.getDomain(), debug=debugFlags)
        ret = self.connection.connect(server=(server, port))

        if not ret: raise Exception("Unable to connect to server")

        ret = self.connection.auth(jid.getNode(), password)

        if not ret: raise Exception("Login failed")

        self.connection.RegisterHandler("message", self.callback_wrapper)
        self.connection.sendInitPresence()

        self.jarvis = Jarvis()

    #---------------------------------------------------------------------------
    def __del__(self):
        if self.connection: del self.connection
        if self.jarvis: del self.jarvis

    #---------------------------------------------------------------------------
    def callback_wrapper(self, conn, msg):
        reply = None

        try:
            reply = self.message_handler(msg)

        except Jarvis.BadCommand, bce:
            reply = msg.buildReply(strings.REPLY_BAD_COMMAND % bce)

        except Exception, e:
            reply = msg.buildReply(strings.REPLY_EXCEPTION % e)

        except:
            reply = msg.buildReply(strings.REPLY_UNKNOWN_ERR)

        finally:

            if reply:
                # HACK buildReply uses the 'to' address in the received message,
                # rather than the full JID (which Google expects). to prevent
                # errors, we simply omit the 'from' address in the message
                if reply.has_attr("from"): reply.delAttr("from")

                conn.send(reply)

    #---------------------------------------------------------------------------
    def message_handler(self, msg):
        # TODO need to do a better job of handling message content
        # (e.g. don't process error messages)
        content = msg.getBody()
        if not content: return None

        params = content.split()
        cmd = params.pop(0)
        func = "do_%s" % cmd

        if not hasattr(self.jarvis, func):
            # TODO log invalid commands to see if we should care about them
            return msg.buildReply(strings.REPLY_INVALID_CMD % cmd)

        # TODO handle errors durring callback
        handler = getattr(self.jarvis, func)
        reply = handler(params, msg)

        return reply

    #---------------------------------------------------------------------------
    def start(self):
        self.run = True

        while JabberBot._step_proc(self.connection) and self.run:
            pass

    #---------------------------------------------------------------------------
    def stop(self):
        self.run = False

    #---------------------------------------------------------------------------
    @staticmethod
    def _step_proc(conn):
        try:
            ret = conn.Process(1)

            if ret == '0': return 1
            elif ret > 0: return 1

        except KeyboardInterrupt:
            pass

        return 0


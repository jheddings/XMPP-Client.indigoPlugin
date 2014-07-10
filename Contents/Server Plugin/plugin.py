################################################################################
# Indigo wrapper for the XMPP Client plugin

import indigo

from bot import JabberBot

################################################################################
class Plugin(indigo.PluginBase):
    bot = None

    #---------------------------------------------------------------------------
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

    #---------------------------------------------------------------------------
    def __del__(self):
        indigo.PluginBase.__del__(self)

    #---------------------------------------------------------------------------
    def startup(self):
        # these parameters are validated by PluginConfig.xml
        username = self.pluginPrefs["username"]
        password = self.pluginPrefs["password"]
        server = self.pluginPrefs["server"]
        port = int(self.pluginPrefs["port"])

        self.bot = JabberBot(username, password, server, port)

    #---------------------------------------------------------------------------
    def shutdown(self):
        if self.bot: del self.bot

    #---------------------------------------------------------------------------
    def runConcurrentThread(self):
        indigo.server.log("XMPP Client ONLINE...")
        if self.bot: self.bot.start()
        indigo.server.log("XMPP Client OFFLINE...")

    #---------------------------------------------------------------------------
    def stopConcurrentThread(self):
        indigo.PluginBase.stopConcurrentThread(self)
        if self.bot: self.bot.stop()


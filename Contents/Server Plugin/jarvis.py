################################################################################
# XMPP bot to handle messages and perform useful actions with Indigo

import indigo
import datetime

import strings

# TODO improve parameter valididation (maybe using a grammar or nltk)

# TODO add event callbacks for debugging in the plugin

# TODO support async replies

################################################################################
commands = {
    "set": "set the value of a given variable",
    "get": "get the current value of the provided variable",
    "time": "display the current time according to the server",
    "ping": "by itself, ping will respond with an 'ack' from the server; if an argument is provided, the server will attempt to ping the remote host and respond with the results",
    "turn on": "turn specified device on",
    "turn off": "turn specified device off",
    "run": "run specified action group",
    "help": "display help information; if optional parameters are provided, specific help for that topic will be displayed"
}

################################################################################
class Jarvis:

    #---------------------------------------------------------------------------
    def __init__(self):
        pass

    #---------------------------------------------------------------------------
    def __del__(self):
        pass

    #---------------------------------------------------------------------------
    def do_ping(self, params, msg):
        # TODO support ping params (remote hosts)
        return msg.buildReply(strings.REPLY_ACK_LOCAL)

    #---------------------------------------------------------------------------
    def do_help(self, params, msg):
        if len(params) == 1:
            topic = params[0]

            if topic in commands:
                desc = commands[topic]
                reply = strings.REPLY_HELP_TOPIC % (topic, desc)
            else:
                reply = strings.REPLY_HELP_BAD_TOPIC % (topic)

        else:
            cmds = commands.keys()
            cmds.sort()
            reply = strings.REPLY_HELP_ALL % (", ".join(cmds))

        return msg.buildReply(reply)

    #---------------------------------------------------------------------------
    def do_time(self, params, msg):
        if len(params) <> 0:
            return msg.buildReply(strings.REPLY_BAD_COMMAND % (0, len(params)))

        now = datetime.datetime.now()
        return msg.buildReply(now.strftime(strings.REPLY_CURRENT_TIMEF))

    #---------------------------------------------------------------------------
    def do_set(self, params, msg):
        name = params.pop(0)

        if not indigo.variables.has_key(name):
            raise Jarvis.BadCommand(strings.ERR_NO_SUCH_VAR % name)

        # this happens sometimes...
        if params[0] == "to": params.pop(0)

        var = indigo.variables[name]
        var.value = " ".join(params)
        var.replaceOnServer()

        return msg.buildReply(strings.REPLY_SET_VAR % (var.name, var.value))

    #---------------------------------------------------------------------------
    def do_execute(self, params, msg):
        name = " ".join(params).title()

        if not indigo.actionGroups.has_key(name):
            raise Jarvis.BadCommand(strings.ERR_NO_SUCH_MACRO % name)

        macro = indigo.actionGroups[name]
        indigo.actionGroup.execute(macro.id)

        return msg.buildReply(strings.REPLY_RUN_MACRO % macro.name)

    def do_exec(self, params, msg): return self.do_execute(params, msg)
    def do_run(self, params, msg): return self.do_execute(params, msg)

    #---------------------------------------------------------------------------
    def do_turn(self, params, msg):
        action = params.pop(0)
        name = " ".join(params).title()

        if not indigo.devices.has_key(name):
            raise Jarvis.BadCommand(strings.ERR_NO_SUCH_DEVICE % name)

        device = indigo.devices[name]

        if action == "on": return self._turn_on(device, msg)
        elif action == "off": return self._turn_off(device, msg)
        #elif action == "up": return self._turn_up(device, msg)
        #elif action == "down": return self._turn_down(device, msg)
        else: return msg.buildReply(strings.REPLY_INVALID_CMD % action)

    #---------------------------------------------------------------------------
    def _turn_on(self, device, msg):
        indigo.device.turnOn(device.id)
        return msg.buildReply(strings.REPLY_DEVICE_ON % device.name)

    #---------------------------------------------------------------------------
    def _turn_off(self, device, msg):
        indigo.device.turnOff(device.id)
        return msg.buildReply(strings.REPLY_DEVICE_OFF % device.name)

    #---------------------------------------------------------------------------
    def do_trigger(self, params, msg):
        name = " ".join(params).title()

        if not indigo.triggers.has_key(name):
            raise Jarvis.BadCommand(strings.ERR_NO_SUCH_TRIGGER % name)

        trigger = indigo.triggers[name]
        indigo.trigger.execute(trigger.id)

        return msg.buildReply(strings.REPLY_TRIGGER_FIRED % trigger.name)

    def do_fire(self, params, msg): return self.do_trigger(params, msg)

    #---------------------------------------------------------------------------
    def do_dump(self, params, msg):
        orig = " ".join(params)
        name = orig.title()

        if indigo.variables.has_key(orig):
            return msg.buildReply(indigo.variables[orig])

        elif indigo.devices.has_key(name):
            return msg.buildReply(indigo.devices[name])

        elif indigo.actionGroups.has_key(name):
            return msg.buildReply(indigo.actionGroups[name])

        elif indigo.schedules.has_key(name):
            return msg.buildReply(indigo.schedules[name])

        elif indigo.triggers.has_key(name):
            return msg.buildReply(indigo.triggers[name])

        raise Jarvis.BadCommand(strings.ERR_BAD_STAT_NAME % orig)

    def do_raw(self, params, msg): return self.do_dump(params, msg)
    def do_show(self, params, msg): return self.do_dump(params, msg)

    #---------------------------------------------------------------------------
    def do_status(self, params, msg):
        orig = " ".join(params)
        name = orig.title()

        if indigo.variables.has_key(orig):
            return self._stat_variable(orig, msg)

        elif indigo.devices.has_key(name):
            return self._stat_device(name, msg)

        elif indigo.actionGroups.has_key(name):
            return self._stat_macro(name, msg)

        elif indigo.schedules.has_key(name):
            return self._stat_schedule(name, msg)

        elif indigo.triggers.has_key(name):
            return self._stat_trigger(name, msg)

        raise Jarvis.BadCommand(strings.ERR_BAD_STAT_NAME % orig)

    def do_stat(self, params, msg): return self.do_status(params, msg)
    def do_disp(self, params, msg): return self.do_status(params, msg)
    def do_display(self, params, msg): return self.do_status(params, msg)
    def do_get(self, params, msg): return self.do_status(params, msg)

    #---------------------------------------------------------------------------
    def _stat_variable(self, name, msg):
        var = indigo.variables[name]
        return msg.buildReply(strings.REPLY_STAT_VARIABLE % (var.name, var.value))

    #---------------------------------------------------------------------------
    def _stat_device(self, name, msg):
        device = indigo.devices[name]
        return msg.buildReply(strings.REPLY_STAT_DEVICE % (device.name, device.displayStateValUi))

    #---------------------------------------------------------------------------
    def _stat_schedule(self, name, msg):
        sched = indigo.schedules[name]
        return msg.buildReply(strings.REPLY_STAT_SCHEDULE % (sched.name, sched))

    #---------------------------------------------------------------------------
    def _stat_trigger(self, name, msg):
        trigger = indigo.triggers[name]
        return msg.buildReply(strings.REPLY_STAT_VARIABLE % (trigger.name, trigger))

    #---------------------------------------------------------------------------
    def _stat_macro(self, name, msg):
        macro = indigo.actionGroups[name]
        return msg.buildReply(strings.REPLY_STAT_VARIABLE % (macro.name, macro))

    #---------------------------------------------------------------------------
    # used for testing / debugging
    class Error: pass

    def do_raise(self, params, msg): raise Exception(" ".join(params))
    def do_error(self, params, msg): raise JabberBot.Error()

    #---------------------------------------------------------------------------
    def do_hello(self, params, msg):
        return msg.buildReply(strings.reply_greeting())

    def do_hi(self, params, msg): return self.do_hello(params, msg)
    def do_yo(self, params, msg): return self.do_hello(params, msg)
    def do_hola(self, params, msg): return self.do_hello(params, msg)

    #---------------------------------------------------------------------------
    class BadCommand(Exception): pass


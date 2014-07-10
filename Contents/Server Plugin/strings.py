# these strings are used by the jabber bot to communicate with the user

# {0} = user-requested command
REPLY_INVALID_CMD = "I'm afraid I don't understand your request.  Please type 'help' if you need further assistance."

# no params
REPLY_UNKNOWN_ERR = "My apologies.  An unknown error occurred."

# {0} = exception message
REPLY_EXCEPTION = "A series of unfortunate events has resulted in an error: %s"

# {0} = error message
REPLY_BAD_COMMAND = "I could not understand your request: %s.  Please try again or type 'help' if you need more assistance."

# {0} = list of all supported commands as a string
REPLY_HELP_ALL = "In addition to providing stimulating conversation, I can assist you with the following: %s"

# {0} = topic; {1} = description
REPLY_HELP_TOPIC = "%s - %s"

# {0} = user-requested topic
REPLY_HELP_BAD_TOPIC = "I don't have any information regarding '%s'."

# formatted according to strftime
REPLY_CURRENT_TIMEF = "It is currently %A %B %d, %Y at %I:%M %p"

# {0} the device name
REPLY_DEVICE_ON = "My pleasure.  %s is now on."

# {0} the device name
REPLY_DEVICE_OFF = "As you wish.  %s is now off."

# {0} the device name
ERR_NO_SUCH_DEVICE = "There is no device named '%s'"

# {0} the device name
ERR_BAD_STAT_NAME = "I could not find anything named '%s'"

# {0} the macro name
REPLY_RUN_MACRO = "Performing '%s' now."

# {0} the intended macro name
ERR_NO_SUCH_MACRO = "The action group '%s' does not exist"

# {0} the trigger name
REPLY_TRIGGER_FIRED = "As requested, trigger '%s' has been fired."

# {0} the intended trigger name
ERR_NO_SUCH_TRIGGER = "The trigger '%s' does not exist"

# no params
REPLY_ACK_LOCAL = "ack; timestamp not provided"

# {0} = variable; {1} = value
REPLY_SET_VAR = "I have set %s to %s"

# {0} = variable; {1} = value
REPLY_STAT_VARIABLE = "%s is currently %s"

# {0} = device name; {1} = state
REPLY_STAT_DEVICE = "%s is currently %s"

# {0} = trigger name; {1} = state
REPLY_STAT_TRIGGER = "%s is currently %s"

# {0} = schedule name; {1} = state
REPLY_STAT_SCHEDULE = "%s is currently %s"

# {0} = macro name; {1} = state
REPLY_STAT_MACRO = "%s is currently %s"

# {0} = variable name
REPLY_UNKNOWN_VAR = "I don't see any variable called %s."

#-------------------------------------------------------------------------------
def reply_greeting():
    return "Greetings."

#-------------------------------------------------------------------------------
def reply_cynic():
    return "Well, someone is in a mood today."

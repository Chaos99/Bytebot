#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import re
import inspect
import json
import resource
import ssl

try:
    from urllib.request         import urlopen
except ImportError:
    from urllib                 import urlopen

from bytebot_config             import *
from bytebotpluginloader        import ByteBotPluginLoader
from time                       import time

from twisted.words.protocols    import irc
from twisted.internet           import reactor, protocol, ssl, task
from twisted.python             import log

class ByteBot(irc.IRCClient):
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join(self.factory.channel)
        print("[sign on]")

    def joined(self, channel):
        #self.logger.log("[joined channel %s]" % channel)
        #TODO: plugins.run.onJoin(self, channel)
        print("[joined channel %s]" % channel)

    def privmsg(self, user, channel, msg):
        user = user.split("!", 1)[0]

        if channel == self.nickname:
            """ User whispering to the bot"""
            return

        if msg.startswith(self.nickname + ":"):
            msg = "%S: Ich bin ein Bot. Meine Intelligenz ist limitiert" % user
            self.msg(channel, msg)
            #self.logger.log("<%s> %s" % (self.nickname, msg))
            print("<%s> %s" % (self.nickname, msg))

    def noticed(self, user, channel, message):
        """
        This function is called if a NOTICE is received. According to the RFC 
        one MUST NOT send automatic replies in response to a NOTICE to avoid 
        loops between clients.
        """
        pass

    def action(self, user, channel, msg):
        user = user.split("!", 1)[0]

    def irc_NICK(self, prefix, params):
        old_nick = prefix.split("!")[0]
        new_nick = params[0]

    def alterCollidedNick(self, nickname):
        return nickname + "^"

    def startCron(self):
        def runPerMinute():
            print("test")
        self.minuteCron = task.LoopingCall(runPerMinute)
        self.minuteCron.start(60.0)
        reactor.run()

class ByteBotFactory(protocol.ClientFactory):
    def __init__(self, nickname, password, channel):
        self.nickname = nickname
        self.password = password
        self.channel  = channel

    def buildProtocol(self, addr):
        p         = ByteBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("FATAL: connection failed: ", reason)
        reactor.stop()


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    f = ByteBotFactory(BYTEBOT_NICK, BYTEBOT_PASSWORD, BYTEBOT_CHANNEL)
    if BYTEBOT_SSL == True:
        reactor.connectSSL(BYTEBOT_SERVER, int(BYTEBOT_PORT), f, ssl.ClientContextFactory())
    else:
        reactor.connectSSL(BYTEBOT_SERVER, int(BYTEBOT_PORT), f)
    reactor.run()


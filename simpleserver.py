#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols import basic


class ServerEcho(basic.LineReceiver):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.clients.append(self)
		if len(self.factory.par[-1]) == 1:
			print self
			print self.factory
			self.factory.par[-1].append(self)
			self.par_id = len(self.factory.par)-1
			print self.par_id
			print "PAR IDDDDD"

			self.another_player = self.factory.par[-1][0]
			print "otro"
			print self.another_player
			self.factory.par[-1][0].another_player = self
			print "yo"
			print self
			print self.factory.par[-1][0].another_player

			#~ id_p = len(self.factory.par)-1
			d = {"func": "start"}
			#~ self.transport.sendLine(json.dumps(d))
			#~ self.factory.par[-1][0].sendLine(json.dumps(d))
			self.another_player.sendLine(json.dumps(d))
			self.sendLine(json.dumps(d))
		else:
			print self
			print self.factory
			self.factory.par.append([self])
			self.par_id = len(self.factory.par)-1
			#~ print id_p
			self.par_id = len(self.factory.par)-1
			print "PAR IDDDDD"
			print self.par_id
			d = {"func": "wait"}
			self.sendLine(json.dumps(d))
		print self.factory.par


	#~ def dataReceived(self, data):
	def lineReceived(self, data):
		#~ print "........................."
		d = json.loads(data)
		self.another_player.sendLine(data)#json.dumps(data))

	def connectionLost(self, reason):
		print "Conection lost" + str(reason)
		self.factory.clients.remove(self)
		print "LOOSSTT"
		print self.factory.par
		self.factory.par.pop(self.par_id)
		if len(self.factory.par) == 0:
			self.factory.par.append([])
		print "after lost"
		print self.factory.par


class ServerEchoFactory(Factory):
	def __init__(self):
		self.clients = []
		self.par = [[]]

	def buildProtocol(self, addr):
		return ServerEcho(self)


reactor.listenTCP(8000, ServerEchoFactory())
reactor.run()


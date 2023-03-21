# This file is part of ctrl_bps_panda.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Receiver for bps PanDA plugin."""

import logging
import json
import random
import socket
import threading
import time
import traceback
import stomp

from queue import Queue

from lsst.ctrl.bps import BpsConfig

logging.getLogger("stomp").setLevel(logging.CRITICAL)


class MessagingListener(stomp.ConnectionListener):
    '''
    Messaging Listener
    '''
    def __init__(self, broker, output_queue, logger=None):
        '''
        __init__
        '''
        self.name = "MessagingListener"
        self.__broker = broker
        self.__output_queue = output_queue
        # self.logger = logging.getLogger(self.__class__.__name__)
        self.logger = logger

    def on_error(self, frame):
        '''
        Error handler
        '''
        self.logger.error('[broker] [%s]: %s', self.__broker, frame.body)

    def on_message(self, frame):
        self.logger.debug('[broker] [%s]: %s', self.__broker, frame.body)
        self.__output_queue.put(frame.body)


class MessagingReceiver(threading.Thread):
    def __init__(self, config_file, logger, name="MessagingReceiver", **kwargs):
        threading.Thread.__init__(self, name=name)

        self.logger = logger
        self.graceful_stop = threading.Event()
        self.receiver_queue = Queue()

        self.broker_timeout = 3600

        self.config_file = config_file
        self.config = BpsConfig(self.config_file)
        self.listener = None
        self.conns = []

    def stop(self):
        self.graceful_stop.set()

    def connect(self):
        config = self.config
        brokers = config["brokers"]
        broker_timeout = config["broker_timeout"]

        broker_addresses = []
        for b in brokers:
            try:
                b, port = b.split(":")

                addrinfos = socket.getaddrinfo(b, 0, socket.AF_INET, 0, socket.IPPROTO_TCP)
                for addrinfo in addrinfos:
                    b_addr = addrinfo[4][0]
                    broker_addresses.append((b_addr, port))
            except socket.gaierror as error:
                self.logger.error('Cannot resolve hostname %s: %s' % (b, str(error)))

        self.logger.info("Resolved broker addresses: %s" % (str(broker_addresses)))

        conns = []
        for broker, port in broker_addresses:
            conn = stomp.Connection12(host_and_ports=[(broker, port)],
                                      keepalive=True,
                                      heartbeats=(60000, 60000),     # one minute
                                      timeout=broker_timeout)
            conns.append(conn)
        return conns

    def disconnect(self, conns):
        for conn in conns:
            try:
                conn.disconnect()
            except Exception:
                pass

    def get_listener(self, broker):
        if self.listener is None:
            self.listener = MessagingListener(broker, self.receiver_queue, logger=self.logger)
        return self.listener

    def get_messages(self):
        msgs = []
        try:
            while not self.receiver_queue.empty():
                msg = self.receiver_queue.get(False)
                if msg:
                    self.logger.debug("Received message: %s" % str(msg))
                    msgs.append(msg)
        except Exception as error:
            self.logger.error("Failed to get output messages: %s, %s" % (error, traceback.format_exc()))
        return msgs

    def subscribe(self):
        self.conns = self.connect()

        for conn in self.conns:
            self.logger.info('connecting to %s' % conn.transport._Transport__host_and_ports[0][0])
            conn.set_listener('message-receiver', self.get_listener(conn.transport._Transport__host_and_ports[0]))
            conn.connect(self.config['username'], self.config['password'], wait=True)
            conn.subscribe(destination=self.config['destination'], id='bps-idds-messaging', ack='auto')

    def execute_subscribe(self):
        try:
            self.subscribe()
        except Exception as error:
            self.logger.error("Messaging receiver throws an exception: %s, %s" % (error, traceback.format_exc()))

        while not self.graceful_stop.is_set():
            has_failed_connection = False
            try:
                for conn in self.conns:
                    if not conn.is_connected():
                        conn.set_listener('message-receiver', self.get_listener(conn.transport._Transport__host_and_ports[0]))
                        # conn.start()
                        conn.connect(self.config['username'], self.config['password'], wait=True)
                        conn.subscribe(destination=self.config['destination'], id='bps-idds-messaging', ack='auto')
                time.sleep(0.1)
            except Exception as error:
                self.logger.error("Messaging receiver throws an exception: %s, %s" % (error, traceback.format_exc()))
                has_failed_connection = True

            if has_failed_connection or len(self.conns) == 0:
                try:
                    # re-subscribe
                    self.disconnect(self.receiver_conns)
                    self.subscribe()
                except Exception as error:
                    self.logger.error("Messaging receiver throws an exception: %s, %s" % (error, traceback.format_exc()))

        self.logger.info('receiver graceful stop requested')

        self.disconnect(self.conns)

    def run(self):
        try:
            self.execute_subscribe()
        except Exception as error:
            self.logger.error("Messaging receiver throws an exception: %s, %s" % (error, traceback.format_exc()))

    def __call__(self):
        self.run()

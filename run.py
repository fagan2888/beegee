#!/usr/local/bin/python3
import argparse
import logging
import json

from logging import handlers
from subprocess import Popen, PIPE

NETWORK_BIN = "/usr/sbin/networksetup"

class Network():
    def __init__(self):
        self.args = self.parse_args()
        self.logger = self.init_logging()
        self.conf = self.load_conf()

    def init_logging(self):
        logger = logging.getLogger(__name__)
        log_format = "%(asctime)s -  %(message)s"
        formatter = logging.Formatter(log_format)

        # write logs to log file
        if self.args.log_file:
            max_bytes = 1024 ** 2  # 1 mb
            handler = handlers.RotatingFileHandler(
                self.args.log_file, maxBytes=max_bytes
            )
            logger.addHandler(handler)
        else:
            handler = logging.StreamHandler()

        # write info logs
        if self.args.verbose:
            logger.setLevel(logging.INFO)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def load_conf(self):
        with open(self.args.conf) as fin:
            return json.load(fin)

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--conf", required=True, help='conf file')
        parser.add_argument("-l", "--log_file", help="output log file")
        parser.add_argument(
            "-v", "--verbose", action='store_true', default=True,
            help='verbose'
        )

        return parser.parse_args()

    def _device_is_on(self):
        self.logger.info("checking if device {} is on".format(
            self.conf['device_name']
        ))
        cmd = [NETWORK_BIN, "-getairportpower", self.conf['device_name']]
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        out, err = proc.communicate()
        return (proc.returncode == 0) and (
                out.decode('utf-8').strip().endswith("On"))

    def _correct_network(self):
        self.logger.info("checking if connected to network {}".format(
            self.conf['network_name'])
        )
        cmd = [NETWORK_BIN, "-getairportnetwork", self.conf['device_name']]
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        out, err = proc.communicate()
        return (proc.returncode == 0) and (
                out.decode('utf-8').strip().endswith(
                    self.conf['network_name']
                ))

    def _turn_on_device(self):
        self.logger.info("turning on device {}".format(
            self.conf['device_name']
        ))
        cmd = [NETWORK_BIN, "-setairportpower", self.conf['device_name'],
               "on"]
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        out, err = proc.communicate()
        return

    def _connect_to_network(self):
        self.logger.info("connecting to network {}".format(
            self.conf['network_name']
        ))
        cmd = [NETWORK_BIN, "-setairportnetwork", self.conf['device_name'],
               self.conf['network_name'], self.conf['password']]
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        out, _ = proc.communicate()
        if not proc.returncode == 0:
            self.logger.warning("non 0 status code when connecting to network")
            self.logger.warning("t{}".format(out))

        return (proc.returncode == 0) and (out is "")

    def run(self):
        if not self._device_is_on():
            self._turn_on_device()
        if not self._correct_network():
            is_set = False
            retries = 1
            while not is_set and retries > 0:
                is_set = self._connect_to_network()
                retries -= 1


if __name__ == '__main__':
    network = Network()
    network.run()

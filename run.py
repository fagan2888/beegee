#!/usr/bin/env python3
import argparse
import logging
import json

from logging import handlers
from subprocess import Popen, PIPE


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
        parser.add_argument("-c", "--conf", required=True, help='verbose')
        parser.add_argument("-l", "--log_file", help="output log file")
        parser.add_argument(
            "-v", "--verbose", action='store_true', default=True,
            help='verbose'
        )

        return parser.parse_args()

    def _device_is_on(self):
        self.logger.info('checking if device is on')
        cmd = ["networksetup", "-getairportpower", self.conf['device_name']]
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        out, err = proc.communicate()
        return (proc.returncode == 0) and (out.decode('utf-8').strip().endswith("On"))

    def _correct_network(self):
        self.logger.info("checking if connected to network {}".format(
            self.conf['network_name'])
        )
        cmd = ["networksetup", "-getairportnetwork", self.conf['device_name']]
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        out, err = proc.communicate()
        return (proc.returncode == 0) and (out.decode('utf-8').strip().endswith(self.conf['network_name']))



if __name__ == '__main__':
    network = Network()
    print(network._device_is_on())
    print(network._correct_network())

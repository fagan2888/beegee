#!/usr/bin/env python3
import argparse
import logging
import json

# from subprocess import Popen, PIPE


class Network():
    def init_logging(self):
        logger = logging.getLogger(__name__)
        log_format = "%(asctime)s -  %(message)s"
        formatter = logging.Formatter(log_format)

        # write logs to log file
        if self.args.log_file:
            handler = logging.FileHandler(self.args.log_file)
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
        parser.add_argument("-v", "--verbose", action='store_true',
                            help='verbose')

        return parser.parse_args()

    def __init__(self):
        self.args = self.parse_args()
        self.logger = self.init_logging()
        self.conf = self.load_conf()

        # TODO
        self.logger.info(self.conf)

    def check_status(self):
        pass


if __name__ == '__main__':
    network = Network()

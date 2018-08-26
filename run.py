#!/usr/bin/env python3
import argparse
import logging
import json


def init_logging(args):
    logger = logging.getLogger(__name__)
    log_format = "%(asctime)s -  %(message)s"
    formatter = logging.Formatter(log_format)

    # write logs to log file
    if args.log_file:
        handler = logging.FileHandler(args.log_file)
        logger.addHandler(handler)
    else:
        handler = logging.StreamHandler()

    # write info logs
    if args.verbose:
        logger.setLevel(logging.INFO)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def load_conf(args):
    with open(args.conf) as fin:
        return json.load(fin)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-file", help="output log file")
    parser.add_argument("-v", "--verbose", action='store_true', help='verbose')
    parser.add_argument("-c", "--conf", required=True, help='verbose')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    logger = init_logging(args)
    conf = load_conf(args)
    logger.info(conf)

#!/usr/bin/env python

from __future__ import division

import sys
sys.path.append("..")

import logging
from time import time
import cPickle as pickle

import numpy as np

import theano
import theano.tensor as T

from learning.utils.datalog import dlog, StoreToH5, TextPrinter
from learning.experiment import Experiment

_logger = logging.getLogger()

#=============================================================================
if __name__ == "__main__":
    import argparse 

    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--name', "-n", default=None)
    parser.add_argument('param_file')
    args = parser.parse_args()


    FORMAT = '[%(asctime)s] %(module)-15s %(message)s'
    DATEFMT = "%H:%M:%S"
    logging.basicConfig(format=FORMAT, datefmt=DATEFMT, level=logging.INFO)

    if args.name is None:
        out_name = args.param_file
    else:
        out_name = args.name


    experiment = Experiment.from_param_file(args.param_file)
    experiment.setup_output_dir(out_name, with_suffix=(not args.overwrite))
    experiment.setup_logging()
    experiment.print_summary()

    experiment.run_experiment()
    
    logger.info("Finished. Exiting")
    experiment.print_summary()
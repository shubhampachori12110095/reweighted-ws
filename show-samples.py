#!/usr/bin/env python 

from __future__ import division

import sys

import logging
from time import time
import cPickle as pickle

import numpy as np
import h5py


import pylab
#import theano
#import theano.tensor as T

_logger = logging.getLogger()

#=============================================================================
if __name__ == "__main__":
    import argparse 

    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action="store_true", default=False)
    parser.add_argument('--shape', default="28,28",
            help="Shape for each samples (default: 28,28)")
    parser.add_argument('--nsamples', '-n', default=100,
            help="Number of samples to show")
    parser.add_argument('--sort', default=False, action="store_true", 
            help="Sort samples according to their probability")
    parser.add_argument('out_dir', nargs=1)
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    FORMAT = '[%(asctime)s] %(message)s'
    DATEFMT = "%H:%M:%S"
    logging.basicConfig(format=FORMAT, datefmt=DATEFMT, level=level)

    fname = args.out_dir[0]+"/results.h5"
    try:
        with h5py.File(fname, "r") as h5:

            logger.debug("Keys:")
            for k, v in h5.iteritems():
                logger.debug("  %-30s   %s" % (k, v.shape))
                
            samples = h5['SampleFromP.L0'][-1,:,:]
            log_p = h5['SampleFromP.log_p'][-1,:]    

    except KeyError, e:
        logger.info("Failed to read data from %s: %s" % (fname, e))

    except IOError, e:
        logger.info("Failed to open %s: %s" % (fname, e))

    shape = tuple([int(s) for s in args.shape.split(",")])
    logger.debug("Using shape: %s -- %s" % (args.shape, shape))
    assert len(shape) == 2

    if args.sort:
        idx = np.argsort(log_p)[::-1]
        samples = samples[idx]
        log_p = log_p[idx]

    pylab.figure()
    for i in xrange(args.nsamples):
        pylab.subplot(10, 10, i+1)
        pylab.imshow( samples[i,:].reshape(shape), interpolation='nearest')
        pylab.gray()
        pylab.axis('off')

    pylab.legend(loc="lower right")
    pylab.show()


#!/usr/bin/python
# -*- coding: utf-8 -*-

import piplates.DAQCplate as DAQC

import datetime
import time
import os

tt = ['gardenhouse.core0.%Y%m%d.csv']
isense = [0]

ntime = 2  # number of times per minute to read sensor
t0 = time.time()

for itime in range(ntime):
    for isens in range(1):

        theSense = isense[isens]

        file = datetime.datetime.utcnow().strftime('/home/jbf/data/%Y/%m/'
            + tt[isens])
        i = file.rindex('/')
        ff = file[0:i]
        if not os.path.exists(ff):
            os.makedirs(ff)

        max = 0.
        secondMax = 0.
        
        i = 0
        while i < 1000:
            try:
                a = DAQC.getADC(0, theSense)
                if a>secondMax:
                    if a>max:
                        secondMax = max
                        max = a
                    else:
                        secondMax= a
            except:
                out = open(file + '.except', 'w')
                import traceback
                traceback.print_exc(file=out)
                out.close()
            i = i + 1

        rms = 0.707 * secondMax

        tme = datetime.datetime.utcnow().isoformat()[0:19]
        out = open(file, 'a+')
        out.write('%sZ,%.3f\n' % (tme, rms))
        out.close()

        print '%sZ,%.3f\n' % (tme, rms)
        time.sleep(1)
    if itime < ntime - 1:
        deltaTime = 60. / ntime - (time.time() - t0)
        print 'sleep ', deltaTime
        time.sleep(deltaTime)
        t0 = time.time()

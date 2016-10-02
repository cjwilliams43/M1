#! /usr/bin/python
#-------------------------------------------------------------------------------
# Name:        testFPSpeed.py
# Purpose:     To assess speed and accuracy of
#              floating point calculations.
#
# Author:      cjw
#
# Created:     03/11/2012
# Copyright:   (c) cjw 2012
# Licence:     <your licence>
# Extended orderChoices to 24555 using 64 bit AMD  28-Aug-16
#-------------------------------------------------------------------------------
#!/usr/bin/env python
''' To compare floating point times across a
    number of platforms.
    Method:
           A is a random matrix of order n
           B= A.I
           The residual r is given by the sum of:
               A * B - I
            The orders used n0 = 3, ni+1 = 2 * ni + 1.
    '''
''' We should show the Processor info and the Python version.
     Testing with Scite.
 
     '''

import datetime as dt, math, numpy as np, os
import sys, time
orderChoices= (2, 5, 11, 23, 47, 95, 191, 383,\
              767, 1535, 3071, 6143, 12287, 24555)

global order

def main():
    if len(sys.argv) > 1:
        idMachine= ' '.join(sys.argv[1:])
    else:
        txt= "Please identify machine and owner, using letters, digits and spaces\n"
        if sys.version[:1] == '2':
           idMachine= raw_input(txt)
        else:
           idMachine= input()
    idM= '_'.join(idMachine.split(' '))
    now= dt.datetime.now().isoformat()
    now= now[:13] + '-' + now[14:16]
    oFile= open('FP' + now + '.log', 'w')
    oFile.writelines(idM + '\n' + sys.version + '\n')
    nTests= len(orderChoices)


    for i in range(min(orderChoices.__len__(), nTests)):
        order= orderChoices[i]
        try:
            startTime= time.clock()
            A= np.matrix(np.random.randn(order, order))
            B= A * A.I
            now= time.clock()
            elapsedTime= now - startTime
            diff= abs(B - np.identity(order))
            diffSum= diff.sum() * 1e16
            imprecision=                      \
                        math.log(diffSum, 10) \
                        if diffSum            \
                        else 0

            fmt= 'order={0:>5g}   ' +                  \
                 'measure ofimprecision={1:>6.3f}   ' +\
                 'Time elapsed (seconds)={2:>10.6f}'
            data= (order, imprecision, elapsedTime)
            print(fmt.format(*data))   # drop afer test
            oFile.writelines(fmt.format(*data) + '\n')
        except MemoryError:
            oFile.write('order= % 5i Process terminated by a MemoryError\n' % (order,))
            print('order= ', order)
            sys.exit(22)
        except:
            import traceback as tb
            print(tb.print_exc())
    oFile.close()
    print('\nDone\n')
    z= 1

if __name__ == '__main__':
    # Text string for initial test - Modify for your own machine or
    # delete it and and answer the input statement with your own machine
    # characteristics.
    sys.argv[1:]= ('Intel Pentium D CPU 3.0GHz 1.99 GB of RAM 221GB Disk Free space', )
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

def log_to_cloudwatch(log_marker, message):
    '''
    This functions is used to print the log messages so that they can be logged
    to cloudwatch.

    PARAMETERS
    ----------
    message : str
        message to be logged

    '''
    traceback.print_exc()
    print(log_marker)
    print(message)

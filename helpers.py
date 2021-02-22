#!/usr/bin/env python
# -*- coding: utf-8 -*-

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False
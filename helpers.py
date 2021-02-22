#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update, Message

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

def get_message(update: Update) -> Message:
    return update.message if update.message != None else update.edited_message
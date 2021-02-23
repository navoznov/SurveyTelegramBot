#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update, Message
import os


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def get_message(update: Update) -> Message:
    return update.message if update.message != None else update.edited_message


def check_dir_exists(dir_path) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
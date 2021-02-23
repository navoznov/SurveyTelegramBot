#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Options:
    def __init__(self, telegram_bot_token: str, admin_ids, is_help_mode: bool):
        self.telegram_bot_token = telegram_bot_token
        self.admin_ids = admin_ids
        self.is_help_mode = is_help_mode
        # TODO: опция "не выгружать html по разделу если в нем нет ответов"

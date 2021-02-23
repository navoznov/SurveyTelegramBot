#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
from options import Options


class OptionsParser:
    @staticmethod
    def parse():
        try:
            longopts = ['bot-token=', 'admin-ids=', 'help']
            argv = sys.argv[1:]
            opts, args = getopt.getopt(argv, 't:a:h', longopts)
            args = {}
            for a, v in opts:
                aa = a.replace('--', '')
                args[aa] = v
        except getopt.GetoptError as e:
            sys.exit(2)

        telegram_bot_token = args.get('bot-token', None)
        admin_ids = [] if args.get('admin-ids', None) == None else [int(x.strip()) for x in args['admin-ids'].split(',')]
        is_help_mode = args.get('help', False)
        options = Options(telegram_bot_token, admin_ids, is_help_mode)
        return options

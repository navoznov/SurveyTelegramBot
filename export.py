#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, datetime
import helpers
from shutil import copyfile
from answerHelper import get_all_answer_files

class Export:
    def export_to_html(self, admin_id, should_remove_original_files: bool = False) -> str:
        # TODO: использовать аргумент should_remove_original_files
        date_foramat = '%Y.%m.%d %H-%M-%S'
        self.__current_export_dir_name = datetime.datetime.utcnow().strftime(date_foramat)
        export_dir_path = f'./export/{self.__current_export_dir_name}'
        dirname = os.path.dirname(export_dir_path)
        helpers.check_dir_exists(dirname)
        export_voices_dirpath = os.path.join(export_dir_path, 'voices')
        helpers.check_dir_exists(export_voices_dirpath)

        files = get_all_answer_files()
        joined_json_by_part = self.__join_json_files_by_part(files)
        for part_number, json_str in joined_json_by_part.items():
            user_answers = json.loads(json_str)
            html = self.__generate_html(user_answers)
            file_name = f'part {part_number}.html'
            file_path = os.path.join(export_dir_path, file_name)
            # TODO: pretty html
            open(file_path, 'w', encoding='utf-8').write(html)

        return export_dir_path


    def __join_json_files_by_part(self, files):
        result = {(i+1): list() for i in range(4)}
        for f in files:
            json_str = open(f, 'r', encoding='utf-8').read()
            answer = json.loads(json_str)
            part_number = int(answer['answers']['part_number'])
            result[part_number].append(json_str)

        for i in range(4):
            result[i+1] = '\n'.join(['[', ',\n'.join(result[i+1]), ']'])

        return result


    def __generate_html(self, user_answers, title: str = '') -> str:
        title = '' if title is None else title
        title_html = self.__wrap_with_tag(title, 'title')
        meta_html = '<meta charset="utf-8">'
        style_html = self.__wrap_with_tag(open('./style.css', 'r').read(), 'style')
        head_html = self.__wrap_with_tag('\n'.join([title_html, meta_html, style_html]), 'head')

        table_html = self.__generate_table(user_answers)
        body_html = self.__wrap_with_tag(table_html, 'body')

        html = self.__wrap_with_tag(head_html + body_html, 'html')
        html = '<!DOCTYPE html>\n' + html
        return html


    def __generate_table(self, user_answers) -> str:
        if len(user_answers) == 0:
            return 'Нет данных'

        rows_html = '\n'.join([self.__generate_table_row(ua) for ua in user_answers])
        tbody_html = self.__wrap_with_tag(rows_html, 'tbody')
        common_headers = ['Дата', 'ID', 'Username', 'Fullname', 'Part number']
        answers_headers = [k for k in user_answers[0]['answers'].keys() if k != 'part_number']  # except part_number
        headers = common_headers + answers_headers
        headers_html = '\n'.join([self.__wrap_with_tag(h, 'th') for h in headers])
        thead_html = self.__wrap_with_tag(headers_html, 'thead')

        return self.__wrap_with_tag(thead_html + tbody_html, 'table')


    def __generate_table_row(self, user_answer) -> str:
        link = user_answer['user_info']['link']
        username = user_answer['user_info']['username']
        full_name = f'{user_answer["user_info"]["last_name"]} {user_answer["user_info"]["first_name"]}'
        cells = [
            user_answer['answer_date'],
            user_answer['user_info']['id'],
            f'<a href="{link}">{username}</a>',
            full_name,
            user_answer['answers']['part_number'],
        ]

        cells = cells + [self.__get_answer_html(str(v)) for k, v in user_answer['answers'].items() if k != 'part_number']  # except part_number

        tr = self.__wrap_with_tag('\n'.join([self.__wrap_with_tag(c, 'td') for c in cells]), 'tr')
        return tr


    def __get_answer_html(self, answer: str) -> str:
        # voice - file_format - file_path
        parts = answer.split('***')
        if len(parts) > 1:
            file_path = parts[2]
            old_file_path = os.path.join('./answers/voices', file_path)
            if os.path.isfile(old_file_path):
                relative_file_path = os.path.join('voices', file_path)
                new_file_path = os.path.join('./export', self.__current_export_dir_name, relative_file_path)
                helpers.check_dir_exists(os.path.dirname(new_file_path))
                copyfile(old_file_path, new_file_path)
                # os.rename(old_file_path, new_file_path)
                return f'<audio controls src="{relative_file_path}"> Your browser does not support the<code>audio</code> element.</audio>'

        return answer

    def __wrap_with_tag(self, str: str, tag: str, attributes_str: str = '') -> str:
        return f'<{tag} {attributes_str}>{str}</{tag}>'




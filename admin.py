#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, datetime
import helpers


def export_to_html(admin_id):
    date_foramat = '%Y.%m.%d %H-%M-%S'
    date_str = datetime.datetime.utcnow().strftime(date_foramat)
    export_dirpath = f'./export/{date_str}'
    dirname = os.path.dirname(export_dirpath)
    helpers.check_dir_exists(dirname)
    export_voices_dirpath = os.path.join(export_dirpath, 'voices')
    helpers.check_dir_exists(export_voices_dirpath)

    files = _get_all_answer_files()
    joined_json_by_part = _join_json_files_by_part(files)
    for part_number, json_str in joined_json_by_part.items():
        user_answers = json.loads(json_str)

        table_html = _generate_html(user_answers)
        if table_html != None:
            file_name = f'part {part_number}.html'
            file_path = os.path.join(export_dirpath, file_name)
            open(file_path, 'w', encoding='utf-8').write(table_html)


def _get_all_answer_files():
    dir_path = 'answers'
    helpers.check_dir_exists(dir_path)
    # filename = f'answers/{user.id}.json'
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return files


def _join_json_files_by_part(files):
    result = {(i+1): list() for i in range(4)}
    for f in files:
        json_str = open(f, 'r', encoding='utf-8').read()
        answer = json.loads(json_str)
        part_number = int(answer['answers']['part_number'])
        result[part_number].append(json_str)

    for i in range(4):
        result[i+1] = '\n'.join(['[', ',\n'.join(result[i+1]), ']'])

    return result


def _generate_html(user_answers, title: str = '') -> str:
    title = '' if title is None else title
    title_html = _wrap_with_tag(title, 'title')
    meta_html = '<meta charset="utf-8">'
    style_html = _wrap_with_tag(open('./style.css', 'r').read(), 'style')
    head_html = _wrap_with_tag('\n'.join([title_html, meta_html, style_html]), 'head')

    table_html = _generate_table(user_answers)
    body_html = _wrap_with_tag(table_html, 'body')

    html = _wrap_with_tag(head_html + body_html, 'html')
    html = '<!DOCTYPE html>\n' + html
    return html


def _generate_table(user_answers) -> str:
    if len(user_answers) == 0:
        return None

    rows_html = '\n'.join([_generate_table_row(ua) for ua in user_answers])
    tbody_html = _wrap_with_tag(rows_html, 'tbody')

    headers = ['Дата', 'ID', 'Username', 'Fullname', 'Part number'] + [k for k in user_answers[0]['answers'].keys() if k != 'part_number']  # except part_number
    headers_html = '\n'.join([_wrap_with_tag(h, 'th') for h in headers])
    thead_html = _wrap_with_tag(headers_html, 'thead')

    return _wrap_with_tag(thead_html + tbody_html, 'table')


def _generate_table_row(user_answer) -> str:
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

    cells = cells + [_get_answer_html(str(v)) for k, v in user_answer['answers'].items() if k != 'part_number']  # except part_number

    tr = _wrap_with_tag('\n'.join([_wrap_with_tag(c, 'td') for c in cells]), 'tr')
    return tr


def _get_answer_html(answer: str) -> str:
    # voice - file_format - file_path
    parts = answer.split('***')
    if len(parts) > 1:
        file_path = f'../{parts[2]}'
        if os.path.isfile(file_path):
            return f'<audio controls src="{file_path}"> Your browser does not support the<code>audio</code> element.</audio>'

    return answer


def _wrap_with_tag(str: str, tag: str, attributes_str: str = '') -> str:
    return f'<{tag} {attributes_str}>{str}</{tag}>'




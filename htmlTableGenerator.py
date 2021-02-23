import json

def generate_html(body: str, title: str = '') -> str:
    title = '' if title is None else title
    title_html = _wrap_with_tag(title, 'title')
    meta_html = '<meta charset="utf-8">'
    style_html = _wrap_with_tag(open('./style.css', 'r').read(), 'style')
    head_html = _wrap_with_tag('\n'.join([title_html, meta_html, style_html]), 'head')

    body_html = _wrap_with_tag(body, 'body')

    html = _wrap_with_tag(head_html + body_html, 'html')
    html = '<!DOCTYPE html>\n' + html
    return html

def generate_table(user_answers) -> str:
    if len(user_answers) == 0:
        return None

    rows_html = '\n'.join([generate_table_row(ua) for ua in user_answers])
    tbody_html = _wrap_with_tag(rows_html, 'tbody')

    headers = ['Дата', 'ID', 'Username', 'Fullname', 'Part number'] + [k for k in user_answers[0]['answers'].keys() if k != 'part_number']  # except part_number
    headers_html = '\n'.join([_wrap_with_tag(h, 'th') for h in headers])
    thead_html = _wrap_with_tag(headers_html, 'thead')

    return _wrap_with_tag(thead_html + tbody_html, 'table')


def generate_table_row(user_answer) -> str:
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

    cells = cells + [get_answer_html(str(v)) for k, v in user_answer['answers'].items() if k != 'part_number']  # except part_number

    tr = _wrap_with_tag('\n'.join([_wrap_with_tag(c, 'td') for c in cells]), 'tr')
    return tr


def get_answer_html(answer: str) -> str:
    # voice - file_format - file_path
    parts = answer.split('***')
    if len(parts) > 1:
        file_path = f'../{parts[2]}'
        return f'<audio controls src="{file_path}"> Your browser does not support the<code>audio</code> element.</audio>'
    else:
        return answer

def _wrap_with_tag(str: str, tag: str, attributes_str: str = '') -> str:
    return f'<{tag} {attributes_str}>{str}</{tag}>'
import os, json, datetime
import htmlTableGenerator

def get_all_answer_files():
    dir_path = 'answers'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # filename = f'answers/{user.id}.json'
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    # _, _, filenames = next(os.walk(dir_path))
    return files

def join_json_files(files):
    json_str = ',\n'.join([open(f, 'r', encoding='utf-8').read() for f in files])
    json_str = '\n'.join(['[', json_str, ']'])
    return json_str


def join_json_files_by_part(files):
    result = {(i+1): list() for i in range(4)}
    for f in files:
        json_str = open(f, 'r', encoding='utf-8').read()
        answer = json.loads(json_str)
        part_number = int(answer['answers']['part_number'])
        result[part_number].append(json_str)

    for i in range(4):
        result[i+1] = '\n'.join(['[', ',\n'.join(result[i+1]), ']'])

    return result

def export_to_html():
    files = get_all_answer_files()
    joined_json_by_part = join_json_files_by_part(files)
    export_dirpath = './html/'
    dirname = os.path.dirname(export_dirpath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    date_foramat = '%Y.%m.%d %H-%M-%S'
    date_str = datetime.datetime.utcnow().strftime(date_foramat)

    for k, v in joined_json_by_part.items():
        user_answers = json.loads(v)
        table_html = htmlTableGenerator.generate_html(htmlTableGenerator.generate_table(user_answers))
        if table_html != None:
            file_name = f'{date_str} - part {k}.html'
            file_path = f'{export_dirpath}{file_name}'
            open(file_path, 'w', encoding='utf-8').write(table_html)


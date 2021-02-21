def get_start_state_text():
    return '''Здравствуйте!

Этот бот запрограммирован задать несколько вопросов о том как вы учите новые иностранные слова.

Мы не школа иностранных языков или что-то подобное. Мы энтузиасты, которые хотят создать что-то полезное для всех. Что конкретно? Узнаете в конце теста ;)

На многие ответы можете отвечать как письменно так и аудио. Если честно, аудио предпочтительней! Если вы любите аудио-сообщения — мы вас обожаем!

В любой момент можете сбросить и начать с начала набрав /start
'''


def get_question_1_state_text():
    return '''Вопрос 1. Сколько вы уже знаете языков как минимум на уровне составления простых фраз? Например, если знаете [русский + английский intermediate или выше], то напишите 2.'''


def get_question_2_state_text():
    return '''Вопрос 2. Недавно изучали или прямо сейчас изучаете новый язык?'''


def get_part_1_question_1_state_text():
    return 'Вы иногда ищете значения иностранных слов?'


def get_survey_finish_state_text():
    return '''Спасибо большое за ваши ответы! Мы, настоящие люди, а не этот бот, внимательно изучим ответы :)

Возможно вам интересно зачем был этот опрос? Все достаточно просто. Мы хотим создать бесплатный сервис для 1) "поиска правильного" слов и 2) помощника в пополнении вашего личного словаря.

Хотели создать инструмент для самих себя, но решили что лучше сразу сделать опрос, чтобы понять как мы можем сделать полезным ресурс не только для себя.

Спасибо за ваше участие!

О запуске сервиса мы сообщим в том же месте, откуда вы узнали об этом узнали. Собирать емейлы уже не модно... :)

Вам интересно узнать подробнее про планируемый функционал?'''


def get_plans_info_state_text():
    return '''"Поиск истины перевода" будет выражается в отображении переводов со всех популярных и авторитетных онлайн-переводчиков. Чтобы вы могли самостоятельно сравнить результаты, оценить достоверность и однозначность перевода. И конечно, определения и примеры использования слова.
Там же, планируем создать инструмент для создания списков слов с правильным переводом для: 1) конвертации их в карточки для Анки, или просто в печать, 2) контроля прогресса не только по количеству, но и по категориям слов, например по частности использования. Можно будет загрузить любой текст или список слов чтобы показать какие слова вы ещё не знаете. А те слова которые вы отметите как известные покажут вам насколько вы продвинулись, например в "первых 1000 слов".
Что об этом думаете?
'''

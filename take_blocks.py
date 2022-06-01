import get_blocks as gb
from file_orgzer import get_text_main as gtm
from uzip import get_file_blocks as gfb

def main(inn):
    gb.main(inn)
    gfb()
    text = gtm('blocks')
    if 'указанному налогоплательщику ОТСУТСТВУЮТ' in text:
        return 'Сведений о блокировке счетов не имеется'
    else:
        return 'Имеются сведения о заблокированных счетах'

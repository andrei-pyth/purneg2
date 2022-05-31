import get_blocks as gb
from file_orgzer import get_text_main as gtm
from uzip import get_file_blocks as gfb

def main(inn):
    gb.main(inn)
    gfb()
    #text = gtm('blocks')
    blocks = read_data()
    return blocks


def read_data():
    pass

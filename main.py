import modules as mo

# Links das novels a serem baixadas.
NOVEL_LINKS = [
    "https://readnovelfull.com/i-shall-seal-the-heavens.html",
]
# NOVEL_LINKS = ["https://readnovelfull.com/renegade-immortal.html",
#                "https://readnovelfull.com/pursuit-of-the-truth-v1.html",
#                "https://readnovelfull.com/a-will-eternal.html"]

# Número máximo de capítulos a serem baixados.
# Os números são baseados no índice do array, então é possível que haja capítulos a mais.
# Se 1 em MIN, começa do primeiro capítulo.
# Se -1 em MAX, baixa até o final.
MIN_CHAPTERS_START = 1
MAX_CHAPTERS_END = 10
# Número de documentos a serem gerados por novel.
NOVEL_DOCS_NUMBER = 5
# Traduzir a novel para o português.
TRANSLATE = False


def run_all_modules(novel_link: str):
    novel: dict = mo.run_browser(novel_link)

    init_index = MIN_CHAPTERS_START - 1
    end_index = MAX_CHAPTERS_END if MAX_CHAPTERS_END != -1 else None

    novel['titles'] = novel['titles'][init_index:end_index]
    novel['urls'] = novel['urls'][init_index:end_index]

    chr_contents: list = mo.run_requests(novel['urls'])

    # Remove textos indesejados, como títulos de capítulos.
    novel['chr_contents'] = remove_texts(chr_contents, novel['titles'])

    if TRANSLATE:
        new_novel = mo.translate_novel(novel['titles'], novel['chr_contents'])
        # novel['titles'] = new_novel['titulos']
        novel['chr_contents'] = new_novel['conteudos']
        novel['chr_contents'] = format_translated_chapters(
            novel['chr_contents'])

    doc_lang = 'PT_BR' if TRANSLATE else 'ENG'

    mo.run_docx_generate(novel, NOVEL_DOCS_NUMBER, doc_lang)


def format_translated_chapters(chr_contents: list):
    replacements = [
        (' -', '-'),
        ('.', '. '),
        ('. "', '."'),
        ('?', '? '),
        ('? "', '?"'),
        ('!', '! '),
        ('! "', '!"')
    ]
    new_chr_contents = []

    for content in chr_contents:
        for old, new in replacements:
            content = content.replace(old, new)
        new_chr_contents.append(content)

    return new_chr_contents


# Não remove os títulos dos capítulos.
def remove_texts(chr_contents: list, titles: list):
    black_list = ['Next Chapter', 'Previous Chapter',
                  '(click here for soundtrack)', '[/expand]']

    new_chr_contents = []

    for content in chr_contents:
        content = content.split('\n')
        content = [line for line in content if line not in black_list]
        content = '\n'.join(content)
        new_chr_contents.append(content)

    return new_chr_contents

# def remove_texts(chr_contents: list, titles: list):
#     black_list = ['Next Chapter', 'Previous Chapter',
#                   '(click here for soundtrack)', '[/expand]']
#     merged = list(zip(titles, chr_contents))

#     new_chr_contents = []

#     for title, content in merged:
#         black_list.append(title)
#         content = content.split('\n')
#         content = [line for line in content if line not in black_list]
#         content = '\n'.join(content)
#         new_chr_contents.append(content)
#         black_list.pop()

#     return new_chr_contents


for link in NOVEL_LINKS:
    run_all_modules(link)

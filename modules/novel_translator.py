from googletrans import Translator
from logging import debug
from time import time
from concurrent.futures import ThreadPoolExecutor


def translate_chapter(args):
    title, content = args
    debug(f'Traduzindo: {title}')
    translator = Translator(http2=False)
    new_content = translate_content(content, translator)
    return new_content


def translate_novel(titles: list, chr_contents: list, simultaneous_tasks: int = 50):
    new_novel = {'conteudos': []}
    start_time = time()
    total_chapters = len(titles)

    with ThreadPoolExecutor(max_workers=simultaneous_tasks) as executor:
        for batch_start in range(0, total_chapters, simultaneous_tasks):
            batch_end = min(batch_start + simultaneous_tasks, total_chapters)
            batch = [(titles[i], chr_contents[i])
                     for i in range(batch_start, batch_end)]

            results = list(executor.map(translate_chapter, batch))

            for new_content in results:
                new_novel['conteudos'].append(new_content)

    current_time = time()
    tot_time = current_time - start_time
    debug('Tradução concluída.')
    debug(f'Tempo total: {tot_time:.2f} segundos.')
    return new_novel


def translate_content(content, translator: Translator):
    chunks = create_chunks(content)
    new_content = []

    for chunk in chunks:
        tr = translator.translate(chunk, dest='pt').text
        new_content.append(tr)

    return ''.join(new_content)


def create_chunks(text, max_size: int = 5000):
    lines = text.splitlines(True)
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) > max_size:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += line
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

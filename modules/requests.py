import asyncio
import aiohttp
from bs4 import BeautifulSoup
from logging import debug


# Recebe os links e retorna o html de cada um.
async def main(urls):
    debug('Iniciando sessão...')
    async with aiohttp.ClientSession() as session:
        tasks = [get_html(session, url) for url in urls]
        debug('Iniciando requisições...')
        return await asyncio.gather(*tasks)


# Recebe o client e a url e retorna o html da página.
async def get_html(session, url):
    async with session.get(url) as response:
        response_text = await response.text()
        return response_text


# Recebe os htmls e retorna o conteúdo dos capítulos
def process_htmls(htmls):
    debug('Processando os htmls...')
    chr_contents = []

    for html in htmls:
        soup = BeautifulSoup(html, 'lxml')
        chr_content = soup.find('div', id='chr-content')
        chr_content = chr_content.get_text(separator='\n', strip=True)
        chr_contents.append(chr_content)

    debug('Htmls processados com sucesso.')
    return chr_contents


# Recebe uma lista de htmls e retorna o conteúdo de todos.
def run_requests(urls):
    htmls = asyncio.run(main(urls))
    chr_contents = process_htmls(htmls)
    return chr_contents
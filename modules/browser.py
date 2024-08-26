from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup
from logging import debug


# Inicia o browser e retorna o html da lista de links e títulos.
async def play(novel_link):
    debug('Iniciando o browser...')
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            debug('Acessando a página da novel...')
            await page.goto(novel_link)
            debug('Clicando no botão "READ NOW"...')
            await page.get_by_text("READ NOW").click()
            await asyncio.sleep(1)
            debug('Clicando na lista de capítulos...')
            await page.locator('#chr-nav-top > div > button').click()

            debug('Obtendo o html...')
            html = await page.locator('#chr-nav-top > div > select').inner_html()

            return html
        finally:
            debug('Fechando o browser...')
            await browser.close()


# Retorna um dicionário com os títulos e urls dos links.
def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    options = soup.find_all('option')

    links = {'titles': [], 'urls': []}

    for option in options:
        links['titles'].append(option.text)
        links['urls'].append(f"https://readnovelfull.com{option['value']}")

    return links


# Função principal que inicia o browser e retorna os links.
def run_browser(novel_link):
    debug('Iniciando o processo...')
    html: str = asyncio.run(play(novel_link))
    links: dict = get_links(html)
    debug('Links obtidos com sucesso.')
    return links


if __name__ == '__main__':
    links: dict = run_browser()

    with open('links.txt', 'w') as f:
        for title, url in zip(links['title'], links['urls']):
            f.write(f"{title}: {url}\n")

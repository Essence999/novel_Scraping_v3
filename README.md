Este projeto é uma ferramenta para baixar capítulos de web novels do site https://readnovelfull.com/ em um `.docx`.

# Funcionalidades
- Download de capítulos: Baixa capítulos de novels a partir de links fornecidos.
- Seleção de intervalo de capítulos: Permite definir o capítulo inicial e final a ser baixado, e a quantidade de partes.
- Geração de documentos: Gera documentos .docx com o conteúdo baixado.
- Tradução automática: Traduz automaticamente os capítulos para o português (opcional).
- Formatação automática: Realiza ajustes no conteúdo traduzido para melhorar a legibilidade.

# Configuração
- NOVEL_LINKS: Lista de URLs das novels que você deseja baixar.
- MIN_CHAPTERS_START: Capítulo inicial a ser baixado (baseado no índice 1).
- MAX_CHAPTERS_END: Capítulo final a ser baixado (use -1 para baixar até o último capítulo disponível).
- NOVEL_DOCS_NUMBER: Número de documentos .docx a serem gerados por novel.
- TRANSLATE: Define se o conteúdo deve ser traduzido para o português (True ou False).

O objetivo deste projeto é arquivar web novels em documentos para que seja possível lê-los como se fosse um livro baixado.

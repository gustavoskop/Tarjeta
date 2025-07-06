def extrair_dados(arquivo_pdf):
    import pdfplumber
    import pandas as pd
    import re

    # Abre o arquivo PDF e concatena o texto de todas as páginas
    with pdfplumber.open(arquivo_pdf) as pdf:
        texto = ''
        for page in pdf.pages:
            texto += page.extract_text() + '\n'

    # Função auxiliar para corrigir erros comuns de OCR (ex: caracteres trocados)
    def corrige_ocr(texto):
        texto = texto.replace('—', '-')  # Substitui travessões por hífens
        texto = texto.replace('|', '/')  # Corrige barras OCR mal reconhecidas
        return texto

    # Aplica as correções ao texto extraído
    texto = corrige_ocr(texto)

    # Expressão regular para extrair os campos com base na estrutura padronizada do texto
    padrao = re.compile(
        r'^(\d{2})\s+'  # Número do formulário (duas casas no início da linha)
        r'([A-ZÇÁÉÍÓÚÃÕÂÊÔÀÀÜa-zçáéíóúãõâêôàü\s\/\-]+?)\s+'  # Nome completo (inclui separador / ou hífens)
        r'(\d{2}/\d{2}/\d{4})\s+'  # Data de nascimento (dd/mm/aaaa)
        r'BRAS\s+'  # Nacionalidade (fixa como "BRAS")
        r'([A-Za-zÇÁÉÍÓÚÃÕÂÊÔÀÀÜa-zçáéíóúãõâêôàü()\s\.\-]+?)\s+'  # Profissão (campo livre com caracteres variados)
        r'([MFmf])\s+'  # Sexo (M ou F, com letras minúsculas ou maiúsculas)
        r'([\d\.\-A-Z]+)\s+'  # Documento (CPF, RG, etc. com possíveis pontos, traços e letras)
        r'BRAS',  # Marcador de fim do registro (nacionalidade repetida)
        re.MULTILINE
    )

    dados = []

    # Itera sobre todas as correspondências encontradas no texto
    for match in padrao.finditer(texto):
        numero, nome_completo, nascimento, profissao, sexo, documento = match.groups()

        # Trata separação entre sobrenome e nome (usando "/" quando presente)
        if '/' in nome_completo:
            sobrenome, nome = [parte.strip() for parte in nome_completo.split('/', 1)]
        else:
            # Quando não há "/", tenta separar última palavra como nome
            partes = nome_completo.strip().rsplit(' ', 1)
            sobrenome = partes[0] if len(partes) > 1 else nome_completo.strip()
            nome = partes[1] if len(partes) > 1 else ''

        # Reformatar data de nascimento para o formato ddmmaaaa (sem separadores)
        dia, mes, ano = nascimento.split('/')
        data_formatada = f"{dia}{mes}{ano[-2:]}"  # Usa apenas os dois últimos dígitos do ano

        # Adiciona os dados processados na lista
        dados.append([
            int(numero),
            sobrenome.replace(" ", ""),  # Remove espaços do sobrenome
            nome.replace(" ", ""),       # Remove espaços do nome
            data_formatada,
            sexo.upper(),                # Converte sexo para letra maiúscula
            documento.strip().replace("-", "").replace(".", "")  # Remove símbolos do documento
        ])

    # Cria um DataFrame com os dados extraídos
    df = pd.DataFrame(dados, columns=[
        'numero',
        'sobrenome',
        'nome',
        'data_nascimento',
        'sexo',
        'documento'
    ])

    # Exibe os dados no terminal para verificação
    print(df)

    # Salva os dados como CSV com encoding apropriado para suportar acentos
    df.to_csv('dados.csv', index=False, sep=';', encoding='utf-8-sig')
    print('CSV gerado com sucesso como dados.csv')
    print(f'Total de registros processados: {len(dados)}')

    # Retorna o caminho do arquivo CSV gerado
    return 'dados.csv'

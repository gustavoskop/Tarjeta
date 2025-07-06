def preencher(dados):
    import pandas as pd
    from PIL import Image, ImageDraw, ImageFont
    from fpdf import FPDF
    import os
    from tkinter import filedialog
    import webbrowser
    import sys

    # Função para obter o caminho de um recurso (imagem, fonte) de forma compatível com PyInstaller
    def recurso_caminho(relativo):
        try:
            base_path = sys._MEIPASS  # Quando empacotado com PyInstaller
        except AttributeError:
            base_path = os.path.abspath(".")  # Em ambiente de desenvolvimento
        return os.path.join(base_path, relativo)

    # Ajusta sobrenomes que excedem o limite de caracteres, movendo o excesso para o nome
    def ajustar_nomes(sobrenome, nome):
        if len(sobrenome) > TAMANHO_MAX_SOBRENOME:
            excesso = sobrenome[TAMANHO_MAX_SOBRENOME:]
            sobrenome = sobrenome[:TAMANHO_MAX_SOBRENOME]
            nome = f"{excesso}/{nome}"
        return sobrenome, nome

    # Redimensiona a imagem para corresponder ao tamanho do PDF (em pontos convertidos para pixels)
    def resize_image(img_path, target_size_pt):
        img = Image.open(img_path)
        target_size_px = (int(target_size_pt[0] * 300/72), int(target_size_pt[1] * 300/72))  # Conversão de pt para px
        img = img.resize(target_size_px, Image.LANCZOS)  # Filtro de alta qualidade
        img.save(img_path)

    # Constantes de configuração
    TEMPLATE_PATH = recurso_caminho("template.png")        # Caminho para imagem base do formulário
    FONT_PATH = recurso_caminho("arialbd.ttf")             # Fonte utilizada
    TAMANHO_MAX_SOBRENOME = 19                             # Tamanho máximo permitido para sobrenome

    # Leitura do CSV contendo os dados dos formulários
    df = pd.read_csv(dados, sep=';', encoding='utf-8')

    # Criação do objeto PDF com dimensões físicas do formulário (em pontos)
    pdf = FPDF(unit="pt", format=(309, 420))
    pdf.set_auto_page_break(False)

    # Iteração linha a linha no DataFrame para preencher cada formulário
    for indice, linha in df.iterrows():
        img = Image.open(TEMPLATE_PATH).convert("RGB")  # Abre o template e converte para RGB
        draw = ImageDraw.Draw(img)                      # Permite desenhar sobre a imagem

        # Carrega fontes com tamanhos apropriados
        fonte_principal = ImageFont.truetype(FONT_PATH, 50)
        fonte_numero = ImageFont.truetype(FONT_PATH, 66)

        # Prepara dados para escrita
        numero = str(linha['numero']).zfill(2)
        sobrenome_ajustado, nome_ajustado = ajustar_nomes(
            str(linha['sobrenome']).upper(),
            str(linha['nome']).upper()
        )
        data_nascimento = str(linha['data_nascimento']).zfill(6)
        sexo = str(linha['sexo']).upper()
        documento = str(linha['documento'])

        # Desenha o número (duas casas separadas)
        draw.text((663, 193), numero[0], font=fonte_numero, fill="black")
        draw.text((710, 193), numero[1], font=fonte_numero, fill="black")

        # Posições base e espaçamento para nome e sobrenome (letra por letra)
        x_nome, y_nome = 95, 489
        x_sobrenome, y_sobrenome = 95, 383
        espaco_letra = 60

        # Desenha o nome no formulário (letra por letra)
        for i, letra in enumerate(nome_ajustado):
            draw.text((x_nome + i * espaco_letra, y_nome), letra, font=fonte_principal, fill="black")

        # Desenha o sobrenome (letra por letra)
        for i, letra in enumerate(sobrenome_ajustado):
            draw.text((x_sobrenome + i * espaco_letra, y_sobrenome), letra, font=fonte_principal, fill="black")

        # Desenha o número do documento nos campos reservados (até 10 caracteres + 1 opcional)
        x_doc, y_doc = 617, 598
        for i, digito in enumerate(documento[:10]):
            draw.text((x_doc + i * espaco_letra, y_doc), digito, font=fonte_principal, fill="black")
        if (len(documento) > 10):
            draw.text((x_doc + 10 * espaco_letra - 14, y_doc), documento[10], font=fonte_principal, fill="black")

        # Posições específicas para cada dígito da data de nascimento
        posicoes_data = [
            (580, 885), (641, 885),
            (727, 885), (789, 885),
            (876, 885), (938, 885)
        ]

        # Desenha os dígitos da data nos campos apropriados
        for i, pos in enumerate(posicoes_data[:len(data_nascimento)]):
            draw.text(pos, data_nascimento[i], font=fonte_principal, fill="black")

        # Marca o campo de sexo com um "X" na posição correta
        if sexo == "M":
            draw.text((1057, 881), "X", font=fonte_principal, fill="black")
        else:
            draw.text((1166, 881), "X", font=fonte_principal, fill="black")

        # Marca campos adicionais com "X" (ex: confirmações/finalizações fixas no formulário)
        draw.text((390, 1065), "X", font=fonte_principal, fill="black")
        draw.text((390, 1311), "X", font=fonte_principal, fill="black")

        # Salva a imagem temporária para inserir no PDF
        temp_img_path = f"temp_form_{numero}.png"
        img.save(temp_img_path)

        # Redimensiona a imagem temporária para o tamanho do PDF
        resize_image(temp_img_path, (309, 420))

        # Adiciona a imagem como nova página no PDF
        pdf.add_page()
        pdf.image(temp_img_path, x=0, y=0, w=309, h=420)

        # Remove a imagem temporária após uso
        os.remove(temp_img_path)

    # Abre diálogo para o usuário escolher onde salvar o PDF
    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Salvar PDF como"
    )

    # Salva o PDF no caminho escolhido, se o usuário não cancelar
    if output_path:
        pdf.output(output_path)
        print(f"PDF salvo em: {output_path}")
    else:
        print("Operação cancelada pelo usuário.")

    # Abre o PDF gerado automaticamente no navegador padrão
    webbrowser.open_new(r'file://' + output_path)

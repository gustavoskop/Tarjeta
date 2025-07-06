
from dados import extrair_dados  # Função para extrair os dados estruturados de um PDF
from preencher import preencher  # Função para gerar os formulários preenchidos com base nos dados
import sys
import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Função para selecionar um arquivo PDF via janela de diálogo
def selecionar_pdf():
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if arquivo:
        entrada_path.set(arquivo)  # Atualiza o campo de entrada com o caminho selecionado

# Função que coordena o processo completo: extração e preenchimento
def executar_processo():
    arquivo = entrada_path.get()

    # Validação: impede execução sem selecionar um arquivo
    if not arquivo:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF primeiro.")
        return

    try:
        # Executa o pipeline principal: extrair → preencher
        dados = extrair_dados(arquivo)
        preencher(dados)

        # Fecha a janela principal após conclusão com sucesso
        janela.destroy()

    # Captura possíveis erros no subprocesso (se existisse chamada externa, por exemplo)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro na execução:\n{e}")

# --- Configuração da interface gráfica principal ---

# Inicializa janela raiz do Tkinter
janela = tk.Tk()
janela.title("Extrator e Preenchedor de Formulários")
janela.geometry("550x230")        # Define tamanho fixo da janela
janela.resizable(False, False)    # Impede redimensionamento

# Variável que armazena dinamicamente o caminho do arquivo PDF selecionado
entrada_path = tk.StringVar()

# Rótulo indicando o propósito do campo de entrada
tk.Label(janela, text="Arquivo PDF:", font=("Arial", 12)).pack(pady=10)

# Container para organizar entrada de texto e botão de seleção horizontalmente
frame = tk.Frame(janela)
frame.pack()

# Campo de texto que exibe o caminho do arquivo selecionado
tk.Entry(frame, textvariable=entrada_path, width=50, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

# Botão para abrir o seletor de arquivos
tk.Button(frame, text="Selecionar PDF", command=selecionar_pdf, bg="lightblue").pack(side=tk.LEFT)

# Botão principal para executar o processo completo
tk.Button(
    janela, 
    text="Executar", 
    command=executar_processo, 
    bg="green", 
    fg="white", 
    font=("Arial", 12, "bold"),
    width=25, 
    height=2
).pack(pady=30)

# Inicia o loop da interface gráfica
janela.mainloop()

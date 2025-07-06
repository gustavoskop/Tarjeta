# Tarjeta

Tarjeta é um aplicativo simples que automatiza duas tarefas comuns em ambientes com grande volume de formulários físicos.

O objetivo é economizar tempo e evitar o preenchimento manual, especialmente quando há muitas pessoas a serem cadastradas.

---

## Como funciona

Você só precisa de um PDF com os dados escaneados e o programa cuida do resto:

- O código extrai nome, sobrenome, data de nascimento, sexo e número de documento, então esses dados são usados para preencher um modelo de [formulario](https://github.com/gustavoskop/Tarjeta/blob/fcebba2feb2a07863fb66cf14533c36a3acf9ca7/formulario.png)
- Ao final, o programa gera um novo PDF com os formulários preenchidos


---
## Requisitos do PDF

O PDF precisa seguir um padrão simples, como: [lista_template.pdf](https://github.com/gustavoskop/Tarjeta/blob/fcebba2feb2a07863fb66cf14533c36a3acf9ca7/lista_template.pdf)

## Uso

1. Execute o programa `Tarjeta.exe`
2. Selecione o PDF, seguindo o padrão proposto
3. Clique em “Executar”
4. O sistema gera um PDF com os formulários prontos para impressão


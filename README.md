# Elise — Editor de Texto e Código

**Elise** é um editor de texto e código com interface gráfica, desenvolvido em **Python** utilizando **Tkinter**. O projeto oferece recursos essenciais de edição em uma aplicação simples, incluindo múltiplas abas, numeração de linhas, destaque de sintaxe e personalização visual.

## Funcionalidades

- **Múltiplas abas:** crie, abra e feche arquivos em abas independentes.
- **Gerenciamento de arquivos:** abra arquivos existentes, salve alterações e utilize **Salvar como**.
- **Numeração de linhas:** exibição das linhas ao lado do editor.
- **Destaque de sintaxe:** seleção manual de linguagem ou identificação automática pela extensão do arquivo.
- **Busca e substituição:** encontre ocorrências, navegue entre resultados e substitua uma ou todas as correspondências, com opção de diferenciar maiúsculas e minúsculas.
- **Temas claro e escuro:** alterne a aparência pelo menu **Visual**.
- **Ajuste de fonte:** aumente, diminua ou defina o tamanho do texto (de 8 a 40).
- **Desfazer e refazer:** reverta ou reaplique edições.
- **Barra de status:** consulte o nome e o caminho do arquivo, além da linha e coluna do cursor.
- **Aviso de alterações não salvas:** confirmação antes de fechar abas ou sair.

## Linguagens com destaque de sintaxe

Python, C/C++, HTML, JavaScript, SQL, Shell Script, PowerShell, Batch (CMD/BAT), Java, PHP, Ruby, Lua, Swift, Kotlin, Rust, C#, Go e texto simples.

> O destaque de sintaxe é baseado em expressões regulares. O Elise não inclui compilador, interpretador integrado ou execução de código.

## Tecnologias

- Python 3.10 ou superior (o código utiliza anotações de tipo com `|`)
- Tkinter / ttk — interface gráfica
- Bibliotecas padrão do Python: `os`, `sys`, `re` e `keyword`

Não há dependências externas instaladas via `pip`.

## Instalação e execução

### Linux (Fedora)

Instale o Python e o suporte ao Tkinter, se necessário:

```bash
sudo dnf install python3 python3-tkinter
```

Na pasta do projeto, execute:

```bash
python3 elise.py
```

### Outras distribuições Linux

Verifique se o Python 3 e o Tkinter estão instalados. Em distribuições baseadas em Debian/Ubuntu, por exemplo:

```bash
sudo apt install python3 python3-tk
python3 elise.py
```

### Windows

Com Python e Tkinter instalados, abra um terminal na pasta do projeto e execute:

```powershell
python elise.py
```

> O Elise requer um ambiente gráfico para abrir sua janela.

## Atalhos de teclado

| Atalho | Ação |
| --- | --- |
| `Ctrl + N` | Nova aba |
| `Ctrl + O` | Abrir arquivo |
| `Ctrl + W` | Fechar aba atual |
| `Ctrl + S` | Salvar |
| `Ctrl + Shift + S` | Salvar como |
| `Ctrl + Z` | Desfazer |
| `Ctrl + Y` | Refazer |
| `Ctrl + A` | Selecionar tudo |
| `Ctrl + F` | Buscar |
| `Ctrl + H` | Localizar e substituir |
| `F3` | Próxima ocorrência |
| `Ctrl + +` | Aumentar fonte |
| `Ctrl + -` | Diminuir fonte |

As funções também estão disponíveis nos menus **Arquivo**, **Editar**, **Sintaxe** e **Visual**.

## Estrutura do projeto

```text
.
├── elise.py       # Aplicação principal
├── elise.png      # Ícone opcional da janela
└── README.md      # Documentação
```

O arquivo `elise.png` é opcional: caso não esteja presente, o editor continua funcionando normalmente.

## Observações

- O modo inicial de destaque de sintaxe é **Texto simples**. Para identificar a linguagem pela extensão, selecione **Sintaxe → Automático por extensão**.
- Os arquivos são lidos e salvos usando codificação **UTF-8**.
- Para limitar o processamento em documentos grandes, o destaque de sintaxe não é aplicado quando o texto ultrapassa 300 mil caracteres.

## Objetivo

O projeto foi criado para explorar o desenvolvimento de interfaces gráficas em Python e implementar funcionalidades comuns a editores de texto e código, como gerenciamento de abas, manipulação de arquivos, busca e destaque de sintaxe.

## Licença

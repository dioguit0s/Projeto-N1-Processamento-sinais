# Projeto N1: Processamento de Sinais

Este repositório contém a implementação de um script em Python para aplicação de um filtro digital de **média móvel** (Moving Average) em sinais de áudio (.wav) através da operação de **convolução linear**. O script foi desenvolvido para processar o áudio, aplicar a filtragem para diferentes tamanhos de janela ($M$) e gerar automaticamente os resultados e gráficos correspondentes.

## 🛠️ Tecnologias e Dependências

O projeto foi desenvolvido em **Python 3** e utiliza as seguintes bibliotecas principais:

* [NumPy](https://numpy.org/): Para manipulação eficiente de arrays e cálculos matemáticos.
* [Matplotlib](https://matplotlib.org/): Para a geração e exportação dos gráficos de análise.
* [Soundfile](https://pysoundfile.readthedocs.io/): Para leitura e gravação segura de ficheiros de áudio `.wav`.

## ⚙️ Instalação

1. Clone este repositório para a sua máquina local.
2. Certifique-se de ter o Python 3 instalado.
3. Instale as dependências listadas no ficheiro `requirements.txt` executando o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```

## 🚀 Como Executar

O script principal `projeto_n1.py` recebe um ficheiro de áudio como entrada e processa as convoluções automaticamente.

1. Coloque o seu ficheiro de áudio (formato `.wav`) na raiz do projeto ou forneça o caminho correto.
2. Execute o comando no terminal passando o nome do ficheiro:

```bash
python projeto_n1.py "nome_do_seu_audio.wav"
```

**Parâmetros Opcionais:**
* `--duracao-plot X`: Limita a geração dos gráficos aos primeiros `X` segundos do sinal, facilitando a visualização de detalhes (útil para áudios longos). Exemplo: `python projeto_n1.py "audio.wav" --duracao-plot 5.0`

## 📁 Estrutura de Saída (Outputs)

Após a execução bem-sucedida, o script criará automaticamente uma pasta chamada `saidas/` contendo:

* `/audio`: Ficheiros `.wav` exportados com o áudio processado para os diferentes valores de janela $M$ ($3, 5, 11, 21, 51$).
* `/figuras`: Gráficos gerados durante a execução, incluindo:
  * O sinal original no domínio do tempo.
  * A resposta em frequência e fase do filtro para cada valor de $M$.
  * O espectro de magnitude dos sinais filtrados.
  * Gráficos comparativos no domínio do tempo entre o sinal original e as versões filtradas.

## 👥 Contribuidores

Este projeto foi desenvolvido como parte da disciplina de Processamento de Sinais pelos seguintes membros:

* **[Diogo Santos]** - [GitHub](https://github.com/dioguit0s)
* **[Gustavo Marmo]** - [GitHub](https://github.com/gustavomarmo)
* **[Bianca Ricci]** - [GitHub](https://github.com/biaricci)
* **[Leonardo Rosario]** - [GitHub](https://github.com/leonardorosario)
* **[Ryan Corazza]** - [GitHub](https://github.com/aishiteirai)


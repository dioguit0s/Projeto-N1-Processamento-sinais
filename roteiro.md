# Roteiro de uso — `projeto_n1.py`

Guia para executar o script de filtragem (média móvel por convolução) com **qualquer ficheiro de áudio** em formato WAV.

## 1. Preparação (uma vez por máquina ou ambiente virtual)

1. Abra o PowerShell (ou outro terminal).
2. Entre na pasta do projeto:
   ```powershell
   cd "A:\Projetos\Projeto N1 Processamento sinais"
   ```
3. Instale as dependências (se ainda não instalou):
   ```powershell
   python -m pip install -r requirements.txt
   ```

**No Windows:** se `pip` não for reconhecido, use **`python -m pip`** (o `pip` isolado nem sempre está no `PATH`). Se o comando **`python`** também não for reconhecido, use o launcher **`py`** da mesma forma: **`py -m pip install -r requirements.txt`**.

Nos passos seguintes, sempre que aparecer `python` antes do nome do script ou de `-m pip`, pode substituir por **`py`** no seu PC (é o comportamento habitual em instalações Python no Windows via Microsoft Store ou instalador oficial).

## 2. Formato do ficheiro de entrada

- O programa espera um **ficheiro WAV** (leitura via `soundfile`).
- Se o áudio estiver em **MP3, M4A, FLAC**, etc., converta antes para WAV (por exemplo com Audacity, FFmpeg ou outro conversor) e use esse `.wav` nos comandos abaixo.

## 3. Comando básico

Substitua o caminho pelo seu ficheiro. Use **`py`** em vez de **`python`** se só o launcher `py` funcionar no seu terminal (Windows).

```powershell
python projeto_n1.py "caminho\para\seu_audio.wav"
```

Equivalente com o launcher `py`:

```powershell
py projeto_n1.py "caminho\para\seu_audio.wav"
```

### Exemplos

- Áudio na mesma pasta que o script:
  ```powershell
  python projeto_n1.py gravacao_fala.wav
  ```
- Caminho absoluto:
  ```powershell
  python projeto_n1.py "D:\Audios\entrada.wav"
  ```
- Pastas com **espaços** no nome — use **aspas**:
  ```powershell
  python projeto_n1.py "A:\Meus Documentos\gravacao.wav"
  ```

Em qualquer um destes exemplos, pode trocar `python` por `py` (por exemplo `py projeto_n1.py gravacao_fala.wav`).

## 4. Opção: duração dos gráficos no domínio do tempo

Por padrão, os gráficos de **tempo** cobrem a **duração total** do ficheiro WAV. Para mostrar apenas um trecho inicial (por exemplo os primeiros 5 segundos):

```powershell
python projeto_n1.py seu_audio.wav --duracao-plot 5
```

(Com `py`: `py projeto_n1.py seu_audio.wav --duracao-plot 5`.)

## 5. O que o programa gera

Para cada execução, os resultados são gravados nas pastas (criadas automaticamente):

| Pasta | Conteúdo |
|--------|----------|
| `saidas/audio/` | `filtrado_M3.wav`, `filtrado_M5.wav`, `filtrado_M11.wav`, `filtrado_M21.wav`, `filtrado_M51.wav` |
| `saidas/figuras/` | `sinal_original.png`, `tempo_M*.png`, `resposta_frequencia_M*.png`, `espectro_M*.png` |

**Importante:** os nomes dos ficheiros de saída são **sempre os mesmos**. Uma nova execução **substitui** os ficheiros gerados na corrida anterior.

O programa imprime no terminal a frequência de amostragem (`fs`), o número de amostras e os caminhos das pastas de saída.

## 6. Tratamento do sinal (resumo)

- Estéreo é convertido para **mono** (média dos canais).
- O sinal é **normalizado** em amplitude antes do processamento e da gravação dos WAV filtrados.

## 7. Erros comuns

| Situação | O que verificar |
|----------|------------------|
| Ficheiro não encontrado | Nome, extensão `.wav`, pasta atual ou uso de caminho completo e aspas. |
| `pip` não reconhecido | Usar `python -m pip install -r requirements.txt` ou, no Windows, `py -m pip install -r requirements.txt`. |
| `python` não reconhecido (Windows) | Usar o launcher **`py`** nos mesmos comandos (por exemplo `py projeto_n1.py ...` e `py -m pip ...`). |

## 8. Relatório do trabalho

As questões de discussão (efeito no ruído, inteligibilidade, melhor `M`, coerência tempo/frequência) são respondidas no **relatório em PDF**; este script apenas produz os áudios e figuras para apoiar essa análise.

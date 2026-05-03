#!/usr/bin/env python3
"""
Trabalho N1 — Processamento de Sinais: convolução e filtro de média móvel em áudio.
Resposta ao impulso: h[n] = 1/M para 0 <= n <= M-1; convolução explícita em convoluir().
"""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

try:
    import soundfile as sf
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Instale soundfile: pip install soundfile (ver requirements.txt)"
    ) from exc

M_VALUES = [3, 5, 11, 21, 51]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_SAIDAS = os.path.join(BASE_DIR, "saidas")
OUT_AUDIO = os.path.join(OUT_SAIDAS, "audio")
OUT_FIG = os.path.join(OUT_SAIDAS, "figuras")

DURACAO_ENUNCIADO_MIN_S = 5.0
DURACAO_ENUNCIADO_MAX_S = 10.0
DURACAO_AVISO_TOLERANCIA_S = 1.0


def garantir_pastas_saida() -> None:
    os.makedirs(OUT_SAIDAS, exist_ok=True)
    os.makedirs(OUT_AUDIO, exist_ok=True)
    os.makedirs(OUT_FIG, exist_ok=True)


def aviso_duracao_enunciado(duracao_s: float) -> None:
    """Avisa se a duração se afasta do intervalo ~5–10 s sugerido no enunciado (Parte 1)."""
    lo = DURACAO_ENUNCIADO_MIN_S - DURACAO_AVISO_TOLERANCIA_S
    hi = DURACAO_ENUNCIADO_MAX_S + DURACAO_AVISO_TOLERANCIA_S
    if duracao_s < lo or duracao_s > hi:
        print(
            f"Aviso: duração do sinal ~ {duracao_s:.2f} s; o enunciado sugere gravação "
            f"aproximadamente {DURACAO_ENUNCIADO_MIN_S:.0f}-{DURACAO_ENUNCIADO_MAX_S:.0f} s "
            "com fala e ruído de ambiente.",
            file=sys.stderr,
        )


def imprimir_resumo_entrega(caminho_wav_entrada: str) -> None:
    """Lembrete no terminal dos entregáveis do enunciado (código, áudios, figuras, relatório)."""
    print()
    print("- Lembrete de entrega (conforme enunciado) -")
    print(f"  Áudio original usado nesta corrida: {os.path.abspath(caminho_wav_entrada)}")
    print(f"  WAVs filtrados: {OUT_AUDIO}")
    print(f"  Figuras (incl. comparação entre M): {OUT_FIG}")
    print(
        "  Relatório PDF: Introdução, fundamentação, metodologia, resultados, "
        "discussão (4 questões), conclusão."
    )


def carregar_audio(caminho: str) -> tuple[np.ndarray, int]:
    """Carrega WAV; converte para mono; normaliza amplitude para [-1, 1]."""
    dados, fs = sf.read(caminho, always_2d=False)
    x = np.asarray(dados, dtype=np.float64)
    if x.ndim > 1:
        x = np.mean(x, axis=1)
    pico = np.max(np.abs(x)) if x.size else 1.0
    if pico > 0:
        x = x / pico
    return x, int(fs)


def impulso_media_movel(M: int) -> np.ndarray:
    """h[n] = 1/M para n = 0..M-1 (causal)."""
    if M < 1:
        raise ValueError("M deve ser >= 1")
    return np.ones(M, dtype=np.float64) / M


def convoluir(x: np.ndarray, h: np.ndarray, mode: str = "same") -> np.ndarray:
    """
    Convolução discreta explícita no código (requisito do enunciado):

        y[n] = sum_k x[k] * h[n - k]

    com x[k] e h[j] tratados como zero fora dos índices válidos (como em np.convolve).

    mode='full': comprimento nx + nh - 1.
    mode='same': trecho central de comprimento max(nx, nh), alinhado a numpy.convolve.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    h = np.asarray(h, dtype=np.float64).ravel()
    nx, nh = x.size, h.size
    if nx == 0 or nh == 0:
        return np.array([], dtype=np.float64)

    len_full = nx + nh - 1
    y_full = np.zeros(len_full, dtype=np.float64)
    for n in range(len_full):
        acc = 0.0
        k0 = max(0, n - nh + 1)
        k1 = min(nx - 1, n)
        for k in range(k0, k1 + 1):
            acc += x[k] * h[n - k]
        y_full[n] = acc

    if mode == "full":
        return y_full
    if mode == "same":
        len_same = max(nx, nh)
        start = (len_full - len_same) // 2
        return y_full[start : start + len_same].copy()
    raise ValueError("mode deve ser 'full' ou 'same'")


def resposta_frequencia_h(
    M: int, n_fft: int = 8192
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Módulo da resposta em frequência |H(e^{jω})|.

    Para FIR, H(e^{jω}) é a DTFT de h[n]. Amostras em ω_k = 2πk/N obtêm-se pela
    FFT de h zero-padded até N = n_fft (amostragem com densidade uniforme em [0, π]).
    Retorna ω em rad/amostra, |H|, e frequência normalizada [0, 0.5].
    """
    h = impulso_media_movel(M)
    H = np.fft.rfft(h, n=n_fft)
    freqs_norm = np.fft.rfftfreq(n_fft, d=1.0)
    omega = 2 * np.pi * freqs_norm
    modulo = np.abs(H)
    return omega, modulo, freqs_norm


def espectro_magnitude(x: np.ndarray, fs: int) -> tuple[np.ndarray, np.ndarray]:
    """FFT unilateral: frequências em Hz e magnitude (valor absoluto)."""
    n = len(x)
    if n == 0:
        return np.array([]), np.array([])
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    mag = np.abs(X)
    return freqs, mag


def salvar_wav(caminho: str, sinal: np.ndarray, fs: int) -> None:
    y = np.clip(sinal.astype(np.float64), -1.0, 1.0)
    sf.write(caminho, y.astype(np.float32), fs)


def plot_sinal_tempo(
    t: np.ndarray,
    x: np.ndarray,
    titulo: str,
    caminho_png: str,
    fs: int,
    duracao_plot: float | None = None,
) -> None:
    if duracao_plot is not None:
        n_plot = int(min(len(x), max(1, duracao_plot * fs)))
        t = t[:n_plot]
        x = x[:n_plot]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, x, linewidth=0.8)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(titulo)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(caminho_png, dpi=150)
    plt.close(fig)


def plot_tempo_original_vs_filtrado(
    t: np.ndarray,
    original: np.ndarray,
    filtrado: np.ndarray,
    M: int,
    fs: int,
    caminho_png: str,
    duracao_plot: float | None = None,
) -> None:
    if duracao_plot is None:
        n_max = len(original)
    else:
        n_max = min(len(original), int(duracao_plot * fs))
    t_seg = t[:n_max]
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(t_seg, original[:n_max], label="Original", alpha=0.85, linewidth=0.9)
    ax.plot(t_seg, filtrado[:n_max], label=f"Filtrado (M={M})", alpha=0.9, linewidth=0.9)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"Sinal no tempo — média móvel M={M} (fs={fs} Hz)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(caminho_png, dpi=150)
    plt.close(fig)


def plot_tempo_comparacao_todos_M(
    t: np.ndarray,
    original: np.ndarray,
    filtrados_por_m: dict[int, np.ndarray],
    fs: int,
    caminho_png: str,
    duracao_plot: float | None = None,
) -> None:
    """Sobrepor original e sinais filtrados para todos os M (Parte 3 — comparar resultados)."""
    if duracao_plot is None:
        n_max = len(original)
    else:
        n_max = min(len(original), int(duracao_plot * fs))
    t_seg = t[:n_max]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(t_seg, original[:n_max], label="Original", color="black", alpha=0.75, linewidth=1.0)
    cores = plt.cm.tab10(np.linspace(0, 0.9, len(filtrados_por_m)))
    for cor, M in zip(cores, sorted(filtrados_por_m.keys())):
        y = filtrados_por_m[M]
        ax.plot(
            t_seg,
            y[:n_max],
            label=f"M={M}",
            color=cor,
            alpha=0.9,
            linewidth=0.85,
        )
    ax.set_xlabel("t (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"Comparação no tempo — todos os M (fs={fs} Hz)")
    ax.legend(ncol=3, fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(caminho_png, dpi=150)
    plt.close(fig)


def plot_modulo_H(
    omega: np.ndarray,
    modulo_h: np.ndarray,
    M: int,
    fs: int,
    caminho_png: str,
) -> None:
    f_hz = omega * fs / (2 * np.pi)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(f_hz, modulo_h, linewidth=1.0)
    ax.set_xlabel("f (Hz)")
    ax.set_ylabel(r"$|H(e^{j\omega})|$")
    ax.set_title(f"Resposta em frequência — média móvel M={M}")
    ax.set_xlim(0, fs / 2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(caminho_png, dpi=150)
    plt.close(fig)


def plot_espectros(
    freqs_o: np.ndarray,
    mag_o: np.ndarray,
    freqs_f: np.ndarray,
    mag_f: np.ndarray,
    M: int,
    fs: int,
    caminho_png: str,
) -> None:
    nyq = fs / 2
    mask_o = freqs_o <= nyq
    mask_f = freqs_f <= nyq
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.semilogy(
        freqs_o[mask_o],
        mag_o[mask_o] + 1e-20,
        label="Original",
        alpha=0.85,
        linewidth=0.9,
    )
    ax.semilogy(
        freqs_f[mask_f],
        mag_f[mask_f] + 1e-20,
        label=f"Filtrado M={M}",
        alpha=0.85,
        linewidth=0.9,
    )
    ax.set_xlabel("f (Hz)")
    ax.set_ylabel("Magnitude (escala log)")
    ax.set_title(f"Espectro de magnitude — original vs filtrado (M={M})")
    ax.set_xlim(0, nyq)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(caminho_png, dpi=150)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Filtro de média móvel por convolução (Trabalho N1)."
    )
    parser.add_argument(
        "wav",
        help="Caminho para o ficheiro WAV de entrada",
    )
    parser.add_argument(
        "--duracao-plot",
        type=float,
        default=None,
        metavar="S",
        help=(
            "Segundos a mostrar nos gráficos no tempo; omitir = duração total do WAV. "
            "Ex.: --duracao-plot 5 limita aos primeiros 5 s."
        ),
    )
    args = parser.parse_args()

    if args.duracao_plot is not None and args.duracao_plot <= 0:
        print("--duracao-plot deve ser um número positivo.", file=sys.stderr)
        return 1

    if not os.path.isfile(args.wav):
        print(f"Ficheiro não encontrado: {args.wav}", file=sys.stderr)
        return 1

    garantir_pastas_saida()
    x, fs = carregar_audio(args.wav)
    n = len(x)
    t = np.arange(n, dtype=np.float64) / fs
    duracao_s = n / fs if fs else 0.0
    aviso_duracao_enunciado(duracao_s)

    plot_sinal_tempo(
        t,
        x,
        "Sinal de áudio original (normalizado)",
        os.path.join(OUT_FIG, "sinal_original.png"),
        fs,
        duracao_plot=args.duracao_plot,
    )

    filtrados_por_m: dict[int, np.ndarray] = {}
    for M in M_VALUES:
        h = impulso_media_movel(M)
        y = convoluir(x, h, mode="same")
        filtrados_por_m[M] = y
        salvar_wav(os.path.join(OUT_AUDIO, f"filtrado_M{M}.wav"), y, fs)

        plot_tempo_original_vs_filtrado(
            t,
            x,
            y,
            M,
            fs,
            os.path.join(OUT_FIG, f"tempo_M{M}.png"),
            duracao_plot=args.duracao_plot,
        )

        omega, mod_h, _ = resposta_frequencia_h(M)
        plot_modulo_H(
            omega,
            mod_h,
            M,
            fs,
            os.path.join(OUT_FIG, f"resposta_frequencia_M{M}.png"),
        )

        fo, mo = espectro_magnitude(x, fs)
        ff, mf = espectro_magnitude(y, fs)
        plot_espectros(
            fo,
            mo,
            ff,
            mf,
            M,
            fs,
            os.path.join(OUT_FIG, f"espectro_M{M}.png"),
        )

    plot_tempo_comparacao_todos_M(
        t,
        x,
        filtrados_por_m,
        fs,
        os.path.join(OUT_FIG, "tempo_comparacao_todos_M.png"),
        duracao_plot=args.duracao_plot,
    )

    print(f"Entrada: {args.wav} | fs={fs} Hz | amostras={n} | duracao ~ {duracao_s:.2f} s")
    print(f"Áudios filtrados em: {OUT_AUDIO}")
    print(f"Figuras em: {OUT_FIG}")
    imprimir_resumo_entrega(args.wav)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

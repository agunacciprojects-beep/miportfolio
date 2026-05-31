"""Generate a 16-second synth ambient soundtrack for the NacciTech reel.
All audio is synthesized from scratch with numpy — no external samples,
no licensing concerns.

Sound design palette: synthwave / cyberpunk / tech ambient
- Sub-bass drone (A1, continuous)
- Detuned pad chord (D minor, mid range)
- Kick pulses on scene transitions
- Power-on sweep + chime (intro)
- Whoosh transitions between scenes
- Staggered tech beeps (project cards)
- Caret ticks (promise scene)
- Final chord stab (CTA climax)
"""

import wave
import struct
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
OUT_WAV = HERE / "audio.wav"

SR = 48000
DUR = 16.0
N = int(SR * DUR)
t = np.linspace(0, DUR, N, endpoint=False)


def env_seg(start, end, attack=0.05, release=0.1, sustain=1.0):
    """Envelope over [start, end] with attack and release ramps."""
    env = np.zeros(N)
    s = int(start * SR)
    e = int(end * SR)
    if e <= s:
        return env
    seg = e - s
    a = min(int(attack * SR), seg // 2)
    r = min(int(release * SR), seg // 2)
    if a > 0:
        env[s:s + a] = np.linspace(0, sustain, a)
    if seg - a - r > 0:
        env[s + a:e - r] = sustain
    if r > 0:
        env[e - r:e] = np.linspace(sustain, 0, r)
    return env


def sine_wave(freq, t0, t1, amp=1.0, env=None):
    out = np.zeros(N)
    s = int(t0 * SR)
    e = int(t1 * SR)
    if e <= s:
        return out
    tt = t[s:e]
    out[s:e] = amp * np.sin(2 * np.pi * freq * tt)
    if env is not None:
        out *= env
    return out


# 1. SUB-BASS DRONE (continuous, very low — A1 = 55 Hz)
sub_env = env_seg(0, 16, attack=1.0, release=2.0, sustain=1.0)
sub_mod = 1 + 0.0015 * np.sin(2 * np.pi * 0.18 * t)
sub = 0.20 * np.sin(2 * np.pi * 55 * t * sub_mod) * sub_env

# 2. PAD — D minor chord (D3, F3, A3) with detuned octave above for richness
pad = np.zeros(N)
for freq, amp in [(146.83, 0.075), (174.61, 0.065), (220.00, 0.060), (293.66, 0.045), (349.23, 0.035)]:
    pad += sine_wave(freq, 0.6, 16, amp=amp,
                     env=env_seg(0.6, 16, attack=1.6, release=2.2))
    # Detuned counterpart for richness
    pad += sine_wave(freq * 1.005, 0.6, 16, amp=amp * 0.6,
                     env=env_seg(0.6, 16, attack=1.6, release=2.2))

# Slow LFO modulation on pad volume (breathing)
pad_lfo = 1 + 0.12 * np.sin(2 * np.pi * 0.15 * t)
pad *= pad_lfo

# 3. KICKS — pulses on key beats
def kick(t0, amp=0.55, length=0.28):
    out = np.zeros(N)
    s = int(t0 * SR)
    e = min(s + int(length * SR), N)
    if e <= s:
        return out
    tt = np.linspace(0, length, e - s)
    freq = 130 * np.exp(-tt * 9) + 40
    env = np.exp(-tt * 6.5)
    out[s:e] = amp * np.sin(2 * np.pi * freq * tt) * env
    # Click transient
    click_n = min(int(0.005 * SR), e - s)
    out[s:s + click_n] += np.linspace(amp * 0.4, 0, click_n)
    return out


kicks = sum(kick(t0, amp=0.50) for t0 in [2.5, 5.0, 7.5, 10.5, 13.0])
# Half-time pulse during About + Trabajos
kicks += sum(kick(t0, amp=0.35) for t0 in [8.75, 11.75])

# 4. POWER-ON SWEEP at intro
def sweep(t0, dur, f_start, f_end, amp=0.35):
    out = np.zeros(N)
    s = int(t0 * SR)
    e = min(s + int(dur * SR), N)
    if e <= s:
        return out
    tt = np.linspace(0, dur, e - s)
    freq = f_start * (f_end / f_start) ** (tt / dur)
    bell = np.sin(np.pi * tt / dur) ** 2
    out[s:e] = amp * np.sin(2 * np.pi * freq * tt) * bell
    return out


power_on = sweep(0.15, 0.55, 180, 1800, amp=0.32)

# Chime stinger right after sweep (logo lands)
chime = (
    sine_wave(880, 0.75, 1.1, amp=0.22, env=env_seg(0.75, 1.1, attack=0.005, release=0.3)) +
    sine_wave(1318, 0.75, 1.1, amp=0.13, env=env_seg(0.75, 1.1, attack=0.005, release=0.3)) +
    sine_wave(1760, 0.78, 1.1, amp=0.07, env=env_seg(0.78, 1.1, attack=0.005, release=0.3))
)

# 5. WHOOSH TRANSITIONS (filtered noise sweeps)
rng = np.random.default_rng(42)


def whoosh(t0, dur=0.4, amp=0.25, pitch_rise=True):
    out = np.zeros(N)
    s = int(t0 * SR)
    e = min(s + int(dur * SR), N)
    n = e - s
    if n <= 0:
        return out
    # White noise
    noise = rng.normal(0, 1, n)
    # Simple low-pass via cumulative mean
    smoothed = np.zeros(n)
    a = 0.04
    for i in range(1, n):
        smoothed[i] = (1 - a) * smoothed[i - 1] + a * noise[i]
    # Normalize
    smoothed = smoothed / (np.max(np.abs(smoothed)) + 1e-9)
    # Envelope
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
    out[s:e] = smoothed * env * amp
    return out


whooshes = (
    whoosh(2.35, dur=0.45, amp=0.22) +
    whoosh(4.85, dur=0.45, amp=0.22) +
    whoosh(7.35, dur=0.5, amp=0.24) +
    whoosh(10.35, dur=0.5, amp=0.24) +
    whoosh(12.85, dur=0.5, amp=0.28)
)

# 6. CARD BEEPS (trabajos scene, 6 staggered tech bleeps)
def beep(t0, freq, dur=0.08, amp=0.20):
    out = np.zeros(N)
    s = int(t0 * SR)
    e = min(s + int(dur * SR), N)
    n = e - s
    if n <= 0:
        return out
    tt = np.linspace(0, dur, n)
    env = np.exp(-tt * 28)
    out[s:e] = amp * np.sin(2 * np.pi * freq * tt) * env
    return out


card_beeps = (
    beep(10.80, 880, amp=0.18) +
    beep(10.95, 988, amp=0.18) +
    beep(11.10, 1108, amp=0.18) +
    beep(11.25, 988, amp=0.18) +
    beep(11.40, 1108, amp=0.18) +
    beep(11.55, 1320, amp=0.22)
)

# 7. CARET TICKS (promise scene)
def tick(t0, amp=0.18):
    out = np.zeros(N)
    dur = 0.04
    s = int(t0 * SR)
    e = min(s + int(dur * SR), N)
    n = e - s
    if n <= 0:
        return out
    tt = np.linspace(0, dur, n)
    env = np.exp(-tt * 85)
    noise = rng.normal(0, 0.3, n)
    out[s:e] = amp * (np.sin(2 * np.pi * 2400 * tt) + noise) * env
    return out


ticks = sum(tick(t0, amp=0.13) for t0 in [5.6, 6.1, 6.6, 7.1])

# 8. FINAL CHORD STAB at CTA (13s) — major 7 (cyan-positive)
def stab(t0, amp=0.32):
    out = np.zeros(N)
    dur = 1.5
    s = int(t0 * SR)
    e = min(s + int(dur * SR), N)
    n = e - s
    if n <= 0:
        return out
    tt = np.linspace(0, dur, n)
    env = np.exp(-tt * 1.6)
    # A major 7: A, C#, E, G#
    chord = (
        np.sin(2 * np.pi * 220 * tt) +
        np.sin(2 * np.pi * 277.18 * tt) +
        np.sin(2 * np.pi * 329.63 * tt) +
        np.sin(2 * np.pi * 415.30 * tt)
    )
    out[s:e] = amp * (chord / 4) * env
    return out


final_sting = stab(13.0, amp=0.30)

# 9. FINAL SUSTAINED NOTE (under CTA)
ending = sine_wave(220, 13.0, 16.0, amp=0.13,
                   env=env_seg(13.0, 16.0, attack=0.4, release=2.5))

# ============ MASTER MIX ============
master = (
    sub
    + pad
    + kicks
    + power_on
    + chime
    + whooshes
    + card_beeps
    + ticks
    + final_sting
    + ending
)

# Master fade in (50 ms)
fade_in_n = int(0.05 * SR)
master[:fade_in_n] *= np.linspace(0, 1, fade_in_n)

# Master fade out (1.5s ending tail)
fade_out_start = int(14.5 * SR)
fade_out_n = N - fade_out_start
master[fade_out_start:] *= np.linspace(1, 0, fade_out_n)

# Soft clip to tame peaks
master = np.tanh(master * 0.95) * 0.85

# Stereo (mono duplicated; could add stereo width later)
stereo = np.column_stack([master, master])

# Write 16-bit PCM WAV
audio_int16 = np.clip(stereo * 32767, -32768, 32767).astype(np.int16)

with wave.open(str(OUT_WAV), "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(audio_int16.tobytes())

size_kb = OUT_WAV.stat().st_size / 1024
print(f"audio.wav written: {DUR}s @ {SR}Hz · {size_kb:.1f} KB")

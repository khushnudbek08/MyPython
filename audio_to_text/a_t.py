"""
Audio → Text Converter v3
- ffmpeg bilan audio sifatini tahlil + avtomatik sozlash
- Har fayl uchun til belgilash (IK=uz, qolgani=ru)
- Tozalangan audio → Whisper
"""

import subprocess, sys, os, json, re

def install_if_missing(package, import_name=None):
    import_name = import_name or package
    try:
        __import__(import_name)
    except ImportError:
        print(f"⬇ {package} o'rnatilmoqda...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

install_if_missing("faster-whisper", "faster_whisper")

# ─────────────────────────────────────────
# Til xaritasi — fayl nomi → til
# ─────────────────────────────────────────
TIL_XARITA = {
    "IK": "uz",
    "ik": "uz",
}

def til_aniqlash(fayl_nomi):
    """Fayl nomiga qarab tilni qaytaradi"""
    nom = os.path.splitext(fayl_nomi)[0]  # kengaytmasiz nom
    for kalit, til in TIL_XARITA.items():
        if kalit.lower() in nom.lower():
            return til
    return "ru"  # default

# ─────────────────────────────────────────
# Audio tahlil (loudness, shovqin darajasi)
# ─────────────────────────────────────────
def audio_tahlil(audio_yol):
    """ffmpeg volumedetect bilan audio darajasini o'lchaydi"""
    result = subprocess.run(
        ["ffmpeg", "-i", audio_yol, "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True
    )
    output = result.stderr

    mean_vol = -91.0
    max_vol = -91.0

    for line in output.split("\n"):
        if "mean_volume" in line:
            try:
                mean_vol = float(line.split("mean_volume:")[1].split("dB")[0].strip())
            except:
                pass
        if "max_volume" in line:
            try:
                max_vol = float(line.split("max_volume:")[1].split("dB")[0].strip())
            except:
                pass

    return mean_vol, max_vol

# ─────────────────────────────────────────
# Audio tozalash va kuchaytirish
# ─────────────────────────────────────────
def audio_tozala(kirish_yol, chiqish_yol):
    """
    1. Ovoz darajasini o'lchaydi
    2. Kerakli kuchaytirishni hisoblaydi
    3. Shovqin filtrini qo'llaydi
    4. Tozalangan faylni saqlaydi
    """
    mean_vol, max_vol = audio_tahlil(kirish_yol)
    print(f"  Audio darajasi: o'rtacha={mean_vol:.1f}dB, maksimal={max_vol:.1f}dB")

    # Maqsad: max_vol → -3dB ga yetkazish
    kuchaytirish = -3.0 - max_vol
    if kuchaytirish < 0:
        kuchaytirish = 0  # allaqachon baland bo'lsa o'zgartirma

    print(f"  Kuchaytirish: +{kuchaytirish:.1f}dB")

    # ffmpeg filtrlari:
    # volume      — kuchaytirish
    # highpass    — 80Hz dan past shovqinni kesish (shamol, mutor)
    # lowpass     — 8000Hz dan yuqorini kesish (hissss shovqin)
    # anlmdn      — adaptiv shovqin kamaytirish
    filtr = (
        f"volume={kuchaytirish:.1f}dB,"
        f"highpass=f=80,"
        f"lowpass=f=8000,"
        f"anlmdn=strength=5"
    )

    cmd = [
        "ffmpeg", "-i", kirish_yol,
        "-af", filtr,
        "-ar", "16000",   # Whisper 16kHz da ishlaydi
        "-ac", "1",       # Mono
        "-y",             # Qayta yozish
        chiqish_yol,
        "-loglevel", "error"
    ]

    subprocess.run(cmd, check=True)

    # Natijani tekshir
    mean2, max2 = audio_tahlil(chiqish_yol)
    print(f"  Tozalangandan keyin: o'rtacha={mean2:.1f}dB, maksimal={max2:.1f}dB")
    return True

# ─────────────────────────────────────────
# Gallyutsinatsiya filtri
# ─────────────────────────────────────────
YOLG_ON = [
    r"продолжение следует",
    r"субтитры сделал",
    r"говорит по-итальянски",
    r"говорит по-английски",
    r"thanks for watching",
    r"subscribe",
    r"^\s*\.\.\.\s*$",
]

def yolg_onmi(text):
    t = text.lower().strip()
    return any(re.search(p, t) for p in YOLG_ON)

def takror_ochi(segmentlar):
    if not segmentlar:
        return segmentlar
    natija = [segmentlar[0]]
    for seg in segmentlar[1:]:
        if seg["text"].strip() != natija[-1]["text"].strip():
            natija.append(seg)
    return natija

# ─────────────────────────────────────────
# Model yuklash
# ─────────────────────────────────────────
def model_yukla():
    from faster_whisper import WhisperModel
    print("\n⏳ Whisper modeli yuklanmoqda...")
    for nom in ["large-v3", "medium", "small"]:
        try:
            m = WhisperModel(nom, compute_type="int8", cpu_threads=4, num_workers=1)
            print(f"✓ {nom} yuklandi")
            return m
        except RuntimeError:
            print(f"⚠ {nom} RAM yetmadi...")
    raise RuntimeError("Model yuklanmadi")

# ─────────────────────────────────────────
# Transkripsiya
# ─────────────────────────────────────────
def transkripsiya(model, audio_yol, chiqish_yol, til):
    from faster_whisper import WhisperModel

    prompt_map = {
        "ru": "Это запись конференции. Речь об экономике, инвестициях и международном сотрудничестве.",
        "uz": "Bu konferensiya yozuvi. Iqtisodiyot, investitsiyalar va xalqaro hamkorlik haqida.",
        "en": "This is a conference recording about economics and international cooperation.",
    }
    prompt = prompt_map.get(til, "")

    print(f"  Transkripsiya (til={til})...")
    segmentlar_gen, info = model.transcribe(
        audio_yol,
        language=til,
        beam_size=5,
        temperature=0.0,
        initial_prompt=prompt,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=600, speech_pad_ms=200),
        no_speech_threshold=0.5,
        compression_ratio_threshold=2.4,
    )

    toza = []
    for seg in segmentlar_gen:
        t = seg.text.strip()
        if t and not yolg_onmi(t):
            toza.append({"start": seg.start, "text": t})

    toza = takror_ochi(toza)

    if not toza:
        print("  ⚠ Hech narsa aniqlanmadi")
        matn = "⚠ Audio sifati past — matn aniqlanmadi."
    else:
        qatorlar = []
        for seg in toza:
            m = int(seg["start"] // 60)
            s = seg["start"] % 60
            qatorlar.append(f"[{m:02d}:{s:05.2f}] {seg['text']}")
        matn = "\n".join(qatorlar)

    with open(chiqish_yol, "w", encoding="utf-8") as f:
        f.write(f"Til: {til.upper()}\n")
        f.write(f"Davomiyligi: {int(info.duration//60)} daq {int(info.duration%60)} son\n")
        f.write(f"Segmentlar: {len(toza)} ta\n")
        f.write("─" * 50 + "\n\n")
        f.write(matn)

    print(f"  ✓ {len(toza)} segment → {os.path.basename(chiqish_yol)}")

# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
def main():
    print("=" * 50)
    print("  AUDIO → MATN KONVERTER v3")
    print("=" * 50)

    # ffmpeg tekshir
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✓ ffmpeg mavjud")
    except:
        print("✗ ffmpeg yo'q! sudo apt install ffmpeg")
        return

    print("\nAudio papka yo'li:")
    papka = input("Papka: ").strip().strip('"')
    if not os.path.exists(papka):
        print("✗ Papka topilmadi")
        return

    audio_formats = (".m4a", ".mp3", ".wav", ".mp4", ".ogg", ".flac")
    fayllar = sorted([f for f in os.listdir(papka) if f.lower().endswith(audio_formats)])

    if not fayllar:
        print("✗ Audio fayllar yo'q")
        return

    print(f"\n{len(fayllar)} ta fayl (til aniqlandi):")
    for f in fayllar:
        print(f"  - {f:30s} → {til_aniqlash(f).upper()}")

    print("\nQayta ishlash (mavjud .txt lar ham)? (y/n): ", end="")
    qayta = input().strip().lower() == "y"

    # Vaqtinchalik papka
    tmp_papka = os.path.join(papka, "_tozalangan")
    os.makedirs(tmp_papka, exist_ok=True)

    model = model_yukla()
    muvaffaqiyat = xato = 0

    print(f"\n{'─'*50}")
    for fayl in fayllar:
        txt_yol = os.path.join(papka, os.path.splitext(fayl)[0] + ".txt")
        if os.path.exists(txt_yol) and not qayta:
            print(f"\n⏭ O'tkazildi: {fayl}")
            continue

        audio_yol = os.path.join(papka, fayl)
        toza_yol = os.path.join(tmp_papka, os.path.splitext(fayl)[0] + "_clean.wav")
        til = til_aniqlash(fayl)

        print(f"\n🎵 {fayl} [{til.upper()}]")
        try:
            print("  Audio tozalanmoqda...")
            audio_tozala(audio_yol, toza_yol)
            transkripsiya(model, toza_yol, txt_yol, til)
            muvaffaqiyat += 1
        except Exception as e:
            print(f"  ✗ Xato: {e}")
            xato += 1
        finally:
            if os.path.exists(toza_yol):
                os.remove(toza_yol)

    # Tmp papkani o'chir
    try:
        os.rmdir(tmp_papka)
    except:
        pass

    print(f"\n{'='*50}")
    print(f"✓ Muvaffaqiyatli: {muvaffaqiyat} ta")
    if xato:
        print(f"✗ Xato: {xato} ta")
    print("=" * 50)
    input("\nTugash uchun Enter...")

if __name__ == "__main__":
    main()
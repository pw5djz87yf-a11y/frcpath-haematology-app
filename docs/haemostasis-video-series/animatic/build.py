#!/usr/bin/env python3
"""Build the Module 1 animatic MP4.

Pipeline: shot list (scenes.py) -> spoken chunks -> espeak-ng/MBROLA speech (one WAV
per chunk) -> one HTML frame per chunk -> PNG screenshots (Playwright, via Node) ->
ffmpeg (stills timed to the audio) -> MP4, plus an .srt caption file.

Usage:  python3 build.py [--out DIR] [--voice mb-en1] [--speed 175]
Needs:  espeak-ng (+ mbrola, mbrola-en1 for the default voice), ffmpeg, Node + playwright.
"""
import argparse, html, json, os, re, subprocess, sys, wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import svg, ICONS, RED, RED_DK, BLUE, GOLD, GOLD_DK, GREY, GREY_DK, INK  # noqa: E402
from scenes import SHOTS, MODULE  # noqa: E402

COL = {"red": RED, "blue": BLUE, "gold": GOLD, "grey": GREY, "neutral": INK, "goldblue": GOLD}
HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ speech text
SPEECH = [
    (r"GPIb-IX-V", "G P one B, nine, five"), (r"GPIIb/IIIa", "G P two B three A"), (r"IIb/IIIa", "two B three A"),
    (r"glycoprotein Ib", "glycoprotein one B"), (r"GPIb", "G P one B"), (r"GPVI", "G P six"),
    (r"α2β1", "alpha two beta one"), (r"α2-antiplasmin", "alpha two antiplasmin"), (r"PAI-1", "P A I one"),
    (r"\bAPTT\b", "A P T T"), (r"\bINR\b", "I N R"), (r"\bPT\b", "P T"), (r"\bTT\b", "T T"),
    (r"\btPA\b", "T P A"), (r"\bADP\b", "A D P"), (r"CD39", "C D thirty-nine"), (r"\bGla\b", "glah"),
    (r"thromboxane A2", "thromboxane A two"), (r"D-domains", "D domains"), (r"D-dimer", "D dimer"),
    (r"\bXIIIa\b", "thirteen A"), (r"\bXIII\b", "thirteen"), (r"\bXIIa\b", "twelve A"), (r"\bXII\b", "twelve"),
    (r"\bXIa\b", "eleven A"), (r"\bXI\b", "eleven"), (r"\bIXa\b", "nine A"), (r"\bIX\b", "nine"),
    (r"\bXa\b", "ten A"), (r"\bX\b", "ten"), (r"\bVIIIa\b", "eight A"), (r"\bVIII\b", "eight"),
    (r"\bVIIa\b", "seven A"), (r"\bVII\b", "seven"), (r"\bVa\b", "five A"), (r"\bV\b", "five"),
    (r"\bIIa\b", "two A"), (r"\bII\b", "two"),
    (r"[Hh]aem", lambda m: ("H" if m.group(0)[0] == "H" else "h") + "eem"),
    (r"Vessel-on-the-Hill", "Vessel on the Hill"), (r";", ","),
]


def spoken(t, mac=False):
    for pat, rep in SPEECH:
        if mac and pat.startswith("[Hh]aem"):
            continue  # the macOS voices pronounce haem- correctly
        t = re.sub(pat, rep, t)
    return t


# ------------------------------------------------------------------ chunking
def split_long(s, limit=130):
    if len(s) <= limit:
        return [s]
    cuts = [m.end() for m in re.finditer(r"[,:;] ", s)]
    if not cuts:
        return [s]
    mid = len(s) / 2
    c = min(cuts, key=lambda x: abs(x - mid))
    return split_long(s[:c].strip(), limit) + split_long(s[c:].strip(), limit)


def chunks_for(shot):
    step = shot.get("start", 0)
    out = []
    for para in shot["narration"]:
        m = re.match(r"\[(\d+)\]\s*", para)
        if m:
            step = int(m.group(1))
            para = para[m.end():]
        for sent in re.split(r"(?<=[.?!])\s+(?=[A-Z])", para):
            for piece in split_long(sent):
                out.append(dict(text=piece, step=step))
    return out


# ------------------------------------------------------------------ diagrams
def G(step, frm, body, until=None, dim=False):
    if step < frm or (until is not None and step > until):
        return ""
    op = 0.6 if (dim and step > frm) else 1
    return f'<g opacity="{op}">{body}</g>'


def node(x, y, lab, c=RED, r=50, fs=34, tc="#fff"):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
            f'<text x="{x}" y="{y + fs * 0.36:.0f}" font-size="{fs}" font-weight="800" fill="{tc}" text-anchor="middle">{lab}</text>')


def pill(x, y, lab, c=RED, w=None, fs=30, tc="#fff", stroke=None):
    w = w or (len(lab) * fs * 0.6 + 40)
    st = f' stroke="{stroke}" stroke-width="5"' if stroke else ""
    return (f'<rect x="{x - w / 2:.0f}" y="{y - fs * 0.9:.0f}" width="{w:.0f}" height="{fs * 1.8:.0f}" rx="{fs * 0.9:.0f}" fill="{c}"{st}/>'
            f'<text x="{x}" y="{y + fs * 0.35:.0f}" font-size="{fs}" font-weight="800" fill="{tc}" text-anchor="middle">{lab}</text>')


def arrow(x1, y1, x2, y2, c=RED, dash=False, w=7):
    d = ' stroke-dasharray="14 10"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} marker-end="url(#ah{c[1:]})"/>'


def icon_at(name, x, y, size, **kw):
    return f'<svg x="{x - size / 2}" y="{y - size / 2}" width="{size}" height="{size}" viewBox="0 0 200 200">{ICONS[name](**kw)}</svg>'


def markers():
    return "<defs>" + "".join(
        f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        f'<path d="M0 0 L10 5 L0 10z" fill="{c}"/></marker>' for c in (RED, BLUE, GOLD, GREY, INK)) + "</defs>"


def d_phases(s):
    o = markers()
    rows = [(1, 60, 520, 60, "#eceef1", RED, INK, "Vascular", "narrows the gap"),
            (2, 360, 640, 180, RED, None, "#fff", "Platelet", "fast, fragile plug"),
            (3, 560, 820, 300, RED_DK, None, "#fff", "Coagulation", "fibrin net stabilises plug"),
            (4, 700, 1040, 420, BLUE, None, "#fff", "Fibrinolysis", "clears the clot as the wall heals")]
    for st, x, w, y, fill, stroke, tc, name, desc in rows:
        sk = f' stroke="{stroke}" stroke-width="6"' if stroke else ""
        o += G(s, st, f'<rect x="{x}" y="{y}" width="{w}" height="92" rx="46" fill="{fill}"{sk}/>'
                      f'<text x="{x + 40}" y="{y + 58}" font-size="34" font-weight="800" fill="{tc}">{name}'
                      f'<tspan font-weight="500"> · {desc}</tspan></text>')
    o += G(s, 5, pill(700, 106, "PRIMARY", INK, fs=26) + pill(1120, 226, "PRIMARY", INK, fs=26)
           + pill(1510, 346, "SECONDARY", INK, fs=26))
    o += (f'<line x1="60" y1="600" x2="1730" y2="600" stroke="{GREY_DK}" stroke-width="5" marker-end="url(#ah{INK[1:]})"/>'
          + "".join(f'<text x="{x}" y="650" font-size="30" fill="{GREY_DK}" text-anchor="middle">{t}</text>'
                    for x, t in ((180, "seconds"), (650, "minutes"), (1150, "hours"), (1620, "days"))))
    return o


def d_relay(s):
    o = markers()
    o += G(s, 3, f'<rect x="1040" y="560" width="720" height="90" rx="20" fill="{RED}" opacity="0.14" stroke="{RED}" stroke-width="4"/>'
                 f'<text x="1400" y="616" font-size="30" font-weight="700" fill="{RED_DK}" text-anchor="middle">Activated platelet surface · phosphatidylserine + Ca²⁺</text>', dim=True)
    o += G(s, 1, icon_at("bell", 110, 230, 150) + f'<text x="110" y="345" font-size="30" font-weight="800" fill="{RED_DK}" text-anchor="middle">Tissue factor</text>'
           + node(300, 230, "VIIa") + arrow(352, 210, 466, 140) + arrow(352, 250, 466, 380)
           + node(520, 120, "X") + node(520, 400, "IX") + arrow(572, 120, 690, 120)
           + icon_at("messenger", 760, 110, 120) + f'<text x="760" y="205" font-size="28" font-weight="700" fill="{RED_DK}" text-anchor="middle">a little thrombin</text>'
           + pill(520, 500, "INITIATION", INK, fs=24), dim=True)
    o += G(s, 2, arrow(820, 90, 950, 60, dash=True) + arrow(820, 110, 950, 150, dash=True) + arrow(820, 130, 950, 240, dash=True)
           + node(1000, 60, "V", r=42, fs=30) + node(1000, 150, "VIII", r=42, fs=28) + node(1000, 240, "XI", r=42, fs=30)
           + arrow(760, 225, 760, 268, dash=True) + icon_at("guard", 760, 330, 110, active=True)
           + f'<text x="760" y="410" font-size="26" font-weight="700" fill="{RED_DK}" text-anchor="middle">platelets activated</text>'
           + pill(1000, 330, "AMPLIFICATION", INK, fs=24), dim=True)
    o += G(s, 3, arrow(572, 440, 1076, 440) + f'<rect x="1080" y="380" width="300" height="120" rx="20" fill="{RED}"/>'
                 f'<text x="1230" y="430" font-size="32" font-weight="900" fill="#fff" text-anchor="middle">TENASE</text>'
                 f'<text x="1230" y="474" font-size="30" font-weight="600" fill="#fff" text-anchor="middle">IXa + VIIIa</text>'
                 + pill(1230, 530, "PROPAGATION", INK, fs=24), dim=True)
    o += G(s, 4, arrow(1260, 376, 1310, 266) + f'<rect x="1180" y="140" width="320" height="120" rx="20" fill="{RED}"/>'
                 f'<text x="1340" y="190" font-size="28" font-weight="900" fill="#fff" text-anchor="middle">PROTHROMBINASE</text>'
                 f'<text x="1340" y="234" font-size="30" font-weight="600" fill="#fff" text-anchor="middle">Xa + Va: II → IIa</text>', dim=True)
    o += G(s, 5, arrow(1504, 200, 1570, 200) + icon_at("mayor", 1670, 210, 190)
           + f'<text x="1670" y="350" font-size="32" font-weight="900" fill="{RED_DK}" text-anchor="middle">THROMBIN BURST</text>'
           + f'<text x="1670" y="392" font-size="28" font-weight="600" fill="{RED_DK}" text-anchor="middle">→ fibrin</text>')
    return o


def d_roads(s):
    o = markers()
    o += G(s, 1, f'<polyline points="570,560 1010,360 1590,360 1590,540" fill="none" stroke="{GREY}" stroke-width="140" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="0.2"/>')
    o += G(s, 2, f'<polyline points="150,170 780,170 1010,360 1590,360 1590,540" fill="none" stroke="{GREY}" stroke-width="140" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="0.2"/>')
    o += (arrow(200, 170, 306, 170) + arrow(410, 170, 516, 170) + arrow(620, 170, 726, 170) + arrow(820, 205, 970, 330)
          + arrow(640, 535, 960, 385) + arrow(1060, 360, 1146, 360) + arrow(1250, 360, 1336, 360) + arrow(1440, 360, 1490, 360)
          + arrow(1590, 395, 1590, 495))
    o += node(150, 170, "XII") + node(360, 170, "XI") + node(570, 170, "IX")
    o += G(s, 0, node(780, 170, "VIII", fs=30), until=4)
    o += G(s, 5, f'<circle cx="780" cy="170" r="50" fill="#fff" stroke="{RED}" stroke-width="6" stroke-dasharray="12 9"/>'
                 f'<text x="780" y="183" font-size="38" font-weight="900" fill="{RED}" text-anchor="middle">?</text>'
                 + pill(780, 262, "VIII missing", RED, fs=26))
    o += pill(570, 560, "TF + VII", RED, w=200, fs=32) + node(1010, 360, "X") + node(1200, 360, "V") + node(1390, 360, "II")
    o += pill(1590, 360, "Fibrinogen", RED, w=200, fs=28) + pill(1590, 545, "Fibrin", RED_DK, w=170, fs=30)
    o += (f'<text x="470" y="122" font-size="28" font-weight="700" fill="{RED_DK}" text-anchor="middle">long road (intrinsic)</text>'
          f'<text x="570" y="640" font-size="28" font-weight="700" fill="{RED_DK}" text-anchor="middle">short road (extrinsic)</text>'
          f'<text x="1200" y="300" font-size="28" font-weight="700" fill="{RED_DK}" text-anchor="middle">common road</text>')
    o += G(s, 1, pill(280, 470, "PT / INR", GREY_DK, fs=32))
    o += G(s, 2, pill(150, 60, "APTT", GREY_DK, fs=32))
    o += G(s, 3, f'<rect x="1460" y="300" width="260" height="310" rx="30" fill="none" stroke="{GREY_DK}" stroke-width="7" stroke-dasharray="16 10"/>'
                 + pill(1590, 660, "TT", GREY_DK, fs=32))
    o += G(s, 4, pill(150, 262, "lab only: no bleeding", "#fff", fs=24, tc=GREY_DK, stroke=GREY), until=4)
    o += G(s, 6, pill(430, 52, "APTT prolonged", "#fff", fs=30, tc=RED, stroke=RED)
           + pill(280, 400, "PT normal ✓", "#fff", fs=30, tc="#15803d", stroke="#15803d"))
    return o


DIAGRAMS = {"phases": d_phases, "relay": d_relay, "roads": d_roads}

# ------------------------------------------------------------------ HTML frames
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1920px;height:1080px;overflow:hidden;background:#f6f1e7;font-family:Inter,'DejaVu Sans',sans-serif;color:#1d1d1f}
.hdr{position:absolute;top:0;left:0;right:0;height:120px;display:flex;align-items:center;padding-left:60px;gap:28px;background:#fffdf8;border-bottom:3px solid #e6dfd0}
.bar{width:18px;height:76px;border-radius:9px}
.mod{font-size:24px;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;font-weight:700}
.h{font-size:48px;font-weight:800;line-height:1.1}
.stage{position:absolute;top:120px;left:0;width:1920px;height:780px}
.sub{position:absolute;left:0;right:0;bottom:0;height:180px;background:#111;color:#fff;font-size:40px;line-height:1.3;
     display:flex;align-items:center;justify-content:center;text-align:center;padding:0 90px;font-weight:500}
.item{position:absolute;text-align:center}
.lab{font-size:32px;font-weight:800;margin-top:6px;white-space:nowrap}
.chip{position:absolute;transform:translate(-50%,-50%);color:#fff;font-size:40px;font-weight:800;padding:18px 40px;border-radius:50px;white-space:nowrap}
.cl{position:absolute;left:60px;top:0;width:520px;height:780px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:14px}
.cr{position:absolute;left:640px;right:80px;top:0;height:780px;display:flex;flex-direction:column;justify-content:center;gap:34px}
.b{font-size:46px;line-height:1.25;font-weight:600;display:flex;gap:26px;align-items:flex-start}
.b i{flex:none;width:28px;height:28px;border-radius:6px;margin-top:14px}
.hook{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:30px}
.hk{font-size:28px;letter-spacing:.2em;font-weight:800;color:#6b7280}
.hl{background:#fff;border-left:18px solid;border-radius:14px;padding:24px 50px;font-weight:800;box-shadow:0 4px 0 #e6dfd0;max-width:1700px}
.grid{position:absolute;inset:20px 60px;display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,1fr);gap:22px}
.tile{background:#fff;border-radius:18px;display:flex;align-items:center;gap:18px;padding:16px 22px;border:6px solid transparent}
.tile span{font-size:30px;font-weight:700;line-height:1.2}
.title{position:absolute;inset:0 0 180px 0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px}
"""


def header(shot):
    c = COL[shot.get("colour", "neutral")]
    extra = f";outline:6px solid {BLUE}" if shot.get("colour") == "goldblue" else ""
    return (f'<div class="hdr"><div class="bar" style="background:{c}{extra}"></div>'
            f'<div><div class="mod">{MODULE}</div><div class="h">{html.escape(shot.get("heading", "Hook line"))}</div></div></div>')


def stage(shot, step):
    t = shot["type"]
    if t == "scene":
        out = ('<svg style="position:absolute;bottom:0;left:0" width="1920" height="300" viewBox="0 0 1920 300">'
               '<path d="M0 300 L0 170 Q480 40 960 120 Q1440 200 1920 90 L1920 300Z" fill="#e9dfc8"/></svg>')
        for it in shot["items"]:
            if it.get("step", 0) > step:
                continue
            if "chip" in it:
                out += (f'<div class="chip" style="left:{it["x"]}px;top:{it["y"]}px;background:{COL[it.get("colour", "neutral")]}">'
                        f'{html.escape(it["chip"])}</div>')
                continue
            sz = it.get("size", 160)
            out += (f'<div class="item" style="left:{it["x"] - sz / 2 - 60}px;top:{it["y"] - sz / 2}px;width:{sz + 120}px">'
                    f'{svg(it["icon"], sz, **it.get("kw", {}))}'
                    + (f'<div class="lab">{html.escape(it["label"])}</div>' if it.get("label") else "") + "</div>")
        return out
    if t == "concept":
        n = len(shot["icons"])
        sz = 230 if n == 1 else 190 if n == 2 else 150
        left = "".join(f'<div style="text-align:center">{svg(nm, sz, **kw)}<div class="lab">{html.escape(lb)}</div></div>'
                       for nm, kw, lb in shot["icons"])
        bl = ""
        for i, b in enumerate(shot["bullets"]):
            txt, c = (b if isinstance(b, tuple) else (b, shot["colour"]))
            vis = "" if i <= step else "visibility:hidden"
            bl += f'<div class="b" style="{vis}"><i style="background:{COL[c]}"></i><div>{html.escape(txt)}</div></div>'
        return f'<div class="cl">{left}</div><div class="cr">{bl}</div>'
    if t == "hook":
        c = COL[shot["colour"]]
        fs = 66 if len(shot["lines"]) <= 2 else 54 if len(shot["lines"]) == 3 else 46
        lines = "".join(f'<div class="hl" style="border-color:{c};font-size:{fs}px;{"" if i <= step else "visibility:hidden"}">'
                        f'“{html.escape(l)}”</div>' for i, l in enumerate(shot["lines"]))
        return f'<div class="hook"><div class="hk">HOOK LINE{"S" if len(shot["lines"]) > 1 else ""}</div>{lines}</div>'
    if t == "diagram":
        return (f'<svg width="1920" height="780" viewBox="-60 -10 1920 780" font-family="Inter, DejaVu Sans, sans-serif">'
                f'{DIAGRAMS[shot["svg"]](step)}</svg>')
    if t == "recap":
        tiles = ""
        for i, (nm, kw, txt, c) in enumerate(shot["tiles"]):
            st = i + 1
            style = "opacity:.15" if st > step else (f"border-color:{COL[c]}" if st == step else "")
            tiles += f'<div class="tile" style="{style}">{svg(nm, 110, **kw)}<span>{html.escape(txt)}</span></div>'
        return f'<div class="grid">{tiles}</div>'
    raise ValueError(t)


def frame_html(shot, step, subtitle):
    if shot["type"] == "title":
        body = (f'<div class="title">{svg("castle", 260)}<div style="font-size:96px;font-weight:900">{html.escape(shot["title"])}</div>'
                f'<div style="font-size:44px;color:#6b7280;font-weight:600">{html.escape(shot["sub"])}</div>'
                f'<div style="display:flex;gap:18px;margin-top:10px">'
                + "".join(f'<div style="width:90px;height:16px;border-radius:8px;background:{c}"></div>' for c in (RED, BLUE, GOLD, GREY))
                + "</div></div>")
    else:
        body = header(shot) + f'<div class="stage">{stage(shot, step)}</div>'
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}'
            f'<div class="sub">{html.escape(subtitle)}</div></body></html>')


# ------------------------------------------------------------------ build
def wav_info(p):
    with wave.open(p) as w:
        return w.getparams(), w.readframes(w.getnframes())


def srt_time(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "build"))
    ap.add_argument("--voice", default="mb-en1")
    ap.add_argument("--speed", type=int, default=175)
    ap.add_argument("--only", help="comma-separated shot ids, for previews")
    ap.add_argument("--export-mac", metavar="FILE", help="write a self-contained macOS script that records every line with `say`, then stop")
    ap.add_argument("--audio-dir", help="use pre-recorded NNNN.wav files from this folder (e.g. from the macOS script) instead of espeak-ng")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fdir = os.path.join(a.out, "frames"); os.makedirs(fdir, exist_ok=True)
    adir = os.path.join(a.out, "audio"); os.makedirs(adir, exist_ok=True)

    only = a.only.split(",") if a.only else None
    plan, jobs, mac_lines = [], [], []
    n = 0
    for shot in SHOTS:
        ch = chunks_for(shot)
        for j, c in enumerate(ch):
            n += 1  # global numbering, so recorded NNNN.wav files always match
            if only and shot["id"] not in only:
                continue
            base = f"{n:04d}"
            hp, pp, wp = (os.path.join(fdir, base + ".html"), os.path.join(fdir, base + ".png"), os.path.join(adir, base + ".wav"))
            with open(hp, "w") as f:
                f.write(frame_html(shot, c["step"], c["text"]))
            jobs.append(dict(html=hp, png=pp))
            if a.export_mac:
                mac_lines.append(f"{base}\t{spoken(c['text'], mac=True)}")
            elif a.audio_dir:
                wp = os.path.join(a.audio_dir, base + ".wav")
                if not os.path.exists(wp):
                    sys.exit(f"missing recorded line {wp}")
            else:
                subprocess.run(["espeak-ng", "-v", a.voice, "-s", str(a.speed), "-w", wp, spoken(c["text"])], check=True)
            end = c["text"].rstrip()[-1]
            pause = 0.12 if end == "," else 0.25 if end in ":;" else 0.4
            if shot["type"] == "hook":
                pause = 0.7
            if j == len(ch) - 1:
                pause += 0.45
            plan.append(dict(png=pp, wav=wp, pause=pause, text=c["text"]))

    if a.export_mac:
        tpl = open(os.path.join(HERE, "mac_voice_template.sh")).read()
        open(a.export_mac, "w").write(tpl.replace("__LINES__", "\n".join(mac_lines)))
        print(f"wrote {a.export_mac} ({len(mac_lines)} lines)")
        return
    subprocess.run(["node", os.path.join(HERE, "shoot.js"), json.dumps(jobs)], check=True)

    # audio: concatenate chunk WAVs with silences
    params, frames_all, t, srt, lines = None, [], 0.0, [], []
    for i, p in enumerate(plan):
        prm, data = wav_info(p["wav"])
        params = params or prm
        assert (prm.nchannels, prm.sampwidth, prm.framerate) == (params.nchannels, params.sampwidth, params.framerate)
        dur = len(data) / (prm.sampwidth * prm.nchannels * prm.framerate)
        sil = b"\x00" * (int(p["pause"] * prm.framerate) * prm.sampwidth * prm.nchannels)
        frames_all += [data, sil]
        total = dur + p["pause"]
        srt.append(f"{i + 1}\n{srt_time(t)} --> {srt_time(t + dur)}\n{p['text']}\n")
        lines.append(f"file '{p['png']}'\nduration {total:.3f}")
        t += total
    lines.append(f"file '{plan[-1]['png']}'")
    wav_out = os.path.join(a.out, "narration.wav")
    with wave.open(wav_out, "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(frames_all))
    lst = os.path.join(a.out, "frames.txt")
    open(lst, "w").write("\n".join(lines) + "\n")
    name = "module1_the_day_the_wall_tore_animatic"
    open(os.path.join(a.out, name + ".srt"), "w").write("\n".join(srt))
    mp4 = os.path.join(a.out, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav_out,
                    "-vf", "fps=25,format=yuv420p", "-c:v", "libx264", "-tune", "stillimage", "-crf", "20",
                    "-af", "volume=0.85", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-shortest", "-movflags", "+faststart", mp4], check=True)
    print(f"chunks={len(plan)} duration={t / 60:.2f} min -> {mp4}")


if __name__ == "__main__":
    main()

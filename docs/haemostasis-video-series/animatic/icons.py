"""Flat, high-contrast SVG icons for The Chronicles of Vessel-on-the-Hill.
Each function returns inner SVG markup for a 0 0 200 200 viewBox.
"""

RED = "#d7263d"
RED_DK = "#8e1022"
BLUE = "#1f6fd1"
BLUE_DK = "#0d3f80"
GOLD = "#e0a100"
GOLD_DK = "#8a6200"
GREY = "#6b7280"
GREY_DK = "#374151"
STONE = "#9aa0a6"
INK = "#1d1d1f"


def wall(**k):
    s = f'<rect x="0" y="30" width="200" height="150" rx="6" fill="{STONE}"/>'
    for y in (65, 100, 135):
        s += f'<line x1="0" y1="{y}" x2="200" y2="{y}" stroke="#6f757b" stroke-width="5"/>'
    rows = [(30, 65, 0), (65, 100, 25), (100, 135, 0), (135, 180, 25)]
    for y1, y2, off in rows:
        for x in range(off + 50, 200, 50):
            s += f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#6f757b" stroke-width="5"/>'
    if k.get("cracked"):
        s += f'<path d="M95 30 L110 70 L88 100 L112 135 L96 180" stroke="{INK}" stroke-width="9" fill="none" stroke-linejoin="round"/>'
    return s


def lantern(**k):
    return (f'<circle cx="100" cy="105" r="88" fill="{GOLD}" opacity="0.18"/>'
            f'<rect x="80" y="40" width="40" height="16" rx="4" fill="{GOLD_DK}"/>'
            f'<rect x="65" y="56" width="70" height="100" rx="12" fill="{GOLD}"/>'
            f'<rect x="80" y="72" width="40" height="68" rx="6" fill="#fff3c4"/>'
            f'<rect x="75" y="156" width="50" height="12" rx="4" fill="{GOLD_DK}"/>')


def bell(**k):
    c = GREY if k.get("dormant") else RED
    s = (f'<rect x="92" y="16" width="16" height="18" rx="4" fill="{c}"/>'
         f'<path d="M100 30 C62 30 52 70 52 108 L36 146 L164 146 L148 108 C148 70 138 30 100 30Z" fill="{c}"/>'
         f'<circle cx="100" cy="160" r="15" fill="{c}"/>')
    if not k.get("dormant"):
        s += (f'<path d="M22 70 Q10 100 22 130" stroke="{RED}" stroke-width="8" fill="none" stroke-linecap="round"/>'
              f'<path d="M178 70 Q190 100 178 130" stroke="{RED}" stroke-width="8" fill="none" stroke-linecap="round"/>')
    return s


def guard(**k):
    s = ""
    if k.get("active"):
        for i in range(12):
            import math
            a = i * math.pi / 6
            cx, cy = 100 + 62 * math.cos(a), 125 + 62 * math.sin(a)
            s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="{RED_DK}"/>'
    s += (f'<circle cx="100" cy="42" r="24" fill="{RED_DK}"/>'
          f'<path d="M58 78 L142 78 L142 120 C142 150 122 168 100 182 C78 168 58 150 58 120Z" fill="{RED}"/>'
          f'<circle cx="100" cy="122" r="20" fill="none" stroke="#fff" stroke-width="9"/>')
    return s


def rope(**k):
    return (f'<circle cx="100" cy="110" r="62" stroke="{RED}" stroke-width="12" fill="none"/>'
            f'<circle cx="100" cy="110" r="40" stroke="{RED}" stroke-width="12" fill="none"/>'
            f'<circle cx="100" cy="110" r="18" stroke="{RED}" stroke-width="12" fill="none"/>'
            f'<path d="M162 110 L180 40 Q186 22 168 24" stroke="{RED_DK}" stroke-width="12" fill="none" stroke-linecap="round"/>')


def messenger(**k):
    n = k.get("label", "")
    return (f'<rect x="91" y="88" width="18" height="96" rx="5" fill="#6b4423"/>'
            f'<path d="M100 14 C134 52 130 80 100 96 C70 80 66 52 100 14Z" fill="#ff7a00"/>'
            f'<path d="M100 44 C116 62 114 78 100 88 C86 78 84 62 100 44Z" fill="#ffd23f"/>'
            + (f'<circle cx="150" cy="150" r="34" fill="{RED}"/><text x="150" y="162" font-size="34" font-weight="800" fill="#fff" text-anchor="middle">{n}</text>' if n else ""))


def ink(**k):
    return (f'<rect x="72" y="48" width="56" height="30" rx="6" fill="{RED_DK}"/>'
            f'<rect x="50" y="74" width="100" height="100" rx="18" fill="{RED}"/>'
            f'<text x="100" y="140" font-size="46" font-weight="800" fill="#fff" text-anchor="middle">Ca</text>')


def workshop(**k):
    return (f'<rect x="138" y="28" width="22" height="50" fill="{GREY_DK}"/>'
            f'<circle cx="150" cy="18" r="10" fill="#c7c9cc"/>'
            f'<polygon points="20,95 100,35 180,95" fill="{RED_DK}"/>'
            f'<rect x="34" y="95" width="132" height="85" fill="{STONE}"/>'
            f'<rect x="84" y="125" width="32" height="55" fill="{GREY_DK}"/>'
            f'<rect x="46" y="112" width="26" height="24" fill="#fff3c4"/><rect x="128" y="112" width="26" height="24" fill="#fff3c4"/>')


def forge(**k):
    return (f'<path d="M30 70 L170 70 L170 92 Q140 96 128 112 L128 140 L150 172 L50 172 L72 140 L72 112 Q60 96 30 92Z" fill="{INK}"/>'
            f'<text x="100" y="64" font-size="52" font-weight="900" fill="{RED}" text-anchor="middle">K</text>'
            f'<path d="M150 40 l10 -14 M166 50 l16 -6 M40 42 l-12 -12" stroke="#ff7a00" stroke-width="7" stroke-linecap="round"/>'
            f'<rect x="156" y="120" width="34" height="52" rx="4" fill="{GOLD}"/>'
            f'<text x="173" y="152" font-size="20" font-weight="800" fill="{INK}" text-anchor="middle">C·S</text>')


def mayor(**k):
    c = GOLD if k.get("gold") else RED
    return (f'<circle cx="100" cy="48" r="28" fill="{RED_DK}"/>'
            f'<path d="M50 182 L50 120 Q50 84 100 84 Q150 84 150 120 L150 182Z" fill="{RED}"/>'
            f'<path d="M66 92 Q100 150 134 92" stroke="{INK}" stroke-width="7" fill="none"/>'
            f'<circle cx="100" cy="136" r="17" fill="{c}" stroke="{INK}" stroke-width="5"/>')


def net(**k):
    s = f'<clipPath id="nc"><circle cx="100" cy="100" r="82"/></clipPath><g clip-path="url(#nc)">'
    for i in range(-200, 400, 34):
        s += f'<line x1="{i}" y1="0" x2="{i+200}" y2="200" stroke="{RED}" stroke-width="7"/>'
        s += f'<line x1="{i}" y1="200" x2="{i+200}" y2="0" stroke="{RED}" stroke-width="7"/>'
    s += '</g>'
    s += f'<circle cx="100" cy="100" r="82" stroke="{RED_DK}" stroke-width="8" fill="none"/>'
    return s


def needle(**k):
    return (f'<line x1="40" y1="160" x2="160" y2="40" stroke="{GREY_DK}" stroke-width="12" stroke-linecap="round"/>'
            f'<ellipse cx="150" cy="50" rx="6" ry="12" transform="rotate(45 150 50)" fill="#fff"/>'
            f'<path d="M150 50 C190 90 120 120 150 170 C170 195 110 190 90 170" stroke="{RED}" stroke-width="7" fill="none"/>'
            f'<text x="56" y="80" font-size="40" font-weight="900" fill="{RED}">XIII</text>')


def gatekeeper(**k):
    lab = k.get("label", "")
    edge = (f'<circle cx="62" cy="100" r="52" stroke="{BLUE}" stroke-width="6" fill="none"/>'
            f'<rect x="96" y="85" width="94" height="30" rx="6" fill="{BLUE}"/>') if k.get("blue") else ""
    return (edge + f'<circle cx="62" cy="100" r="40" stroke="{GOLD}" stroke-width="18" fill="none"/>'
            f'<rect x="96" y="91" width="90" height="18" rx="4" fill="{GOLD}"/>'
            f'<rect x="150" y="105" width="14" height="30" fill="{GOLD}"/><rect x="170" y="105" width="14" height="22" fill="{GOLD}"/>'
            + (f'<text x="62" y="112" font-size="30" font-weight="900" fill="{GOLD_DK}" text-anchor="middle">{lab}</text>' if lab else ""))


def foreman(**k):
    return (f'<path d="M30 120 Q30 50 100 50 Q170 50 170 120Z" fill="{BLUE}"/>'
            f'<rect x="16" y="116" width="168" height="18" rx="8" fill="{BLUE_DK}"/>'
            f'<rect x="92" y="40" width="16" height="80" rx="6" fill="{BLUE_DK}"/>'
            f'<rect x="60" y="150" width="60" height="26" rx="13" fill="{GREY_DK}"/><circle cx="128" cy="163" r="16" fill="{GREY_DK}"/>'
            f'<path d="M150 150 l18 -10 M152 166 l22 0" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/>')


def crew(**k):
    return (f'<path d="M100 100 L170 30" stroke="{BLUE}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M100 100 L170 170" stroke="{BLUE}" stroke-width="16" stroke-linecap="round"/>'
            f'<circle cx="62" cy="62" r="26" stroke="{BLUE_DK}" stroke-width="14" fill="none"/>'
            f'<circle cx="62" cy="138" r="26" stroke="{BLUE_DK}" stroke-width="14" fill="none"/>'
            f'<line x1="80" y1="80" x2="104" y2="100" stroke="{BLUE_DK}" stroke-width="14"/><line x1="80" y1="120" x2="104" y2="100" stroke="{BLUE_DK}" stroke-width="14"/>')


def rubble(**k):
    s = ""
    for x, y in ((40, 150), (110, 160), (75, 105), (145, 112)):
        s += (f'<ellipse cx="{x}" cy="{y}" rx="22" ry="16" fill="{BLUE}"/>'
              f'<ellipse cx="{x+30}" cy="{y}" rx="22" ry="16" fill="{BLUE}"/>'
              f'<rect x="{x+6}" y="{y-4}" width="18" height="8" fill="{BLUE_DK}"/>')
    s += f'<text x="100" y="60" font-size="34" font-weight="900" fill="{BLUE_DK}" text-anchor="middle">D–D</text>'
    return s


def inspector(**k):
    lab = k.get("label", "")
    return (f'<rect x="88" y="14" width="24" height="20" rx="4" fill="{GREY_DK}"/>'
            f'<circle cx="100" cy="112" r="70" fill="#fff" stroke="{GREY}" stroke-width="14"/>'
            f'<line x1="100" y1="112" x2="100" y2="62" stroke="{GREY_DK}" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="100" y1="112" x2="134" y2="128" stroke="{GREY_DK}" stroke-width="8" stroke-linecap="round"/>'
            + (f'<text x="100" y="172" font-size="26" font-weight="900" fill="{GREY_DK}" text-anchor="middle">{lab}</text>' if lab else ""))


def river(**k):
    s = ""
    for y in (70, 105, 140):
        s += f'<path d="M10 {y} Q40 {y-18} 70 {y} T130 {y} T190 {y}" stroke="{RED}" stroke-width="12" fill="none" stroke-linecap="round"/>'
    return s


def tube(**k):
    return (f'<rect x="76" y="20" width="48" height="30" rx="6" fill="#7fb3e6"/>'
            f'<path d="M80 50 L80 160 Q80 184 100 184 Q120 184 120 160 L120 50Z" fill="#fff" stroke="{GREY_DK}" stroke-width="6"/>'
            f'<path d="M84 100 L116 100 L116 160 Q116 178 100 178 Q84 178 84 160Z" fill="{RED}"/>'
            f'<text x="160" y="110" font-size="22" font-weight="800" fill="{GREY_DK}" text-anchor="middle">3.2%</text>'
            f'<text x="160" y="136" font-size="22" font-weight="800" fill="{GREY_DK}" text-anchor="middle">citrate</text>')


def castle(**k):
    return (f'<rect x="30" y="80" width="140" height="100" fill="{STONE}"/>'
            f'<rect x="20" y="50" width="40" height="130" fill="#878d93"/><rect x="140" y="50" width="40" height="130" fill="#878d93"/>'
            + "".join(f'<rect x="{x}" y="38" width="12" height="14" fill="#878d93"/>' for x in (20, 34, 48, 140, 154, 168))
            + f'<path d="M84 180 L84 130 Q100 110 116 130 L116 180Z" fill="{GREY_DK}"/>'
            f'<path d="M100 14 L100 50 M100 14 L128 22 L100 30" stroke="{RED}" stroke-width="5" fill="{RED}"/>')


ICONS = {f.__name__: f for f in (wall, lantern, bell, guard, rope, messenger, ink, workshop, forge,
                                  mayor, net, needle, gatekeeper, foreman, crew, rubble, inspector,
                                  river, tube, castle)}


def svg(name, size=160, **k):
    return (f'<svg viewBox="0 0 200 200" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Inter, DejaVu Sans, sans-serif">{ICONS[name](**k)}</svg>')

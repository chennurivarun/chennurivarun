"""Generate terminal-style hero SVGs (dark + light) with ASCII portrait from avatar.png."""
from PIL import Image, ImageOps

# ---------- ASCII portrait ----------
COLS, ROWS = 66, 42
CHARSET = " .:-=+*%#@"  # sparse -> dense (XML-safe)

img = Image.open("avatar.png").convert("L")
img = ImageOps.autocontrast(img, cutoff=2)
img = img.resize((COLS, ROWS))
px = img.load()

def clamp(v, lo=0.0, hi=1.0):
    return min(hi, max(lo, v))

def ascii_rows(invert=False):
    vals = [[px[x, y] / 255.0 for x in range(COLS)] for y in range(ROWS)]
    # backdrop brightness per column, sampled from the top strip (pure backdrop)
    bg_col = []
    for x in range(COLS):
        col = sorted(vals[y][x] for y in range(5))
        bg_col.append(col[len(col) // 2])
    rows = []
    for y in range(ROWS):
        line = []
        for x in range(COLS):
            v = vals[y][x]
            bright = clamp((v - bg_col[x] - 0.04) * 2.5)        # face, shirt
            dark = clamp((bg_col[x] - v - 0.06) * 1.6, 0, 0.55)  # suit, hair silhouette
            dens = max(bright, dark)
            idx = min(int(dens * len(CHARSET)), len(CHARSET) - 1)
            line.append(CHARSET[idx])
        rows.append("".join(line))
    return rows

# ---------- layout ----------
W, H = 840, 446
PANEL_TOP = 34
PANEL_H = 356
FOOT_Y = PANEL_TOP + PANEL_H + 14

L_X, L_W = 14, 336
R_X = L_X + L_W + 12
R_W = W - R_X - 14

# portrait text metrics
P_FS = 6.4
P_LH = 7.3
P_TEXTLEN = L_W - 36
P_X0 = L_X + 18
P_Y0 = PANEL_TOP + 42

# right panel text metrics
T_FS = 10.5
T_LH = 15.2
T_X0 = R_X + 18
T_Y0 = PANEL_TOP + 40

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(
        bg="#040810", panel="#070d18", border="#1c2b40", chrome="#0a1220",
        title="#8aa3bd", accent="#4cc2ff", key="#4cc2ff", val="#dbe6f1",
        dots="#2c405c", head="#5d7astray", muted="#61758c",
        grad_a="#7fd8ff", grad_b="#2f7fd6", scan="#4cc2ff",
        light1="#ff5f57", light2="#febc2e", light3="#28c840",
    ),
    "light": dict(
        bg="#f6f8fa", panel="#ffffff", border="#d0d7de", chrome="#eaeef2",
        title="#57606a", accent="#0969da", key="#0969da", val="#1f2328",
        dots="#c3ccd6", head="#57606a", muted="#6e7781",
        grad_a="#0969da", grad_b="#218bff", scan="#0969da",
        light1="#ff5f57", light2="#febc2e", light3="#28c840",
    ),
}
THEMES["dark"]["head"] = "#61758c"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def pad_line(label, value, width=52):
    """'. Name: .......... value' style line."""
    left = f". {label}: "
    fill = "." * max(2, 20 - len(left))
    return left, fill, value

RIGHT_LINES = [
    ("hdr",  "varun@build ", "-" * 38),
    ("kv",   "Name",  "Varun Chennuri"),
    ("kv",   "Role",  "AI Product Architect"),
    ("kv",   "Based", "Hyderabad, India"),
    ("kv",   "Mode",  "Designing / Building / Shipping"),
    ("gap",),
    ("sec",  "BUILD.FOCUS", 30),
    ("kv",   "Product", "Idea to governed release"),
    ("kv",   "AI",      "Agents with audit trails"),
    ("kv",   "Data",    "CRM/DMS pipelines and MIS"),
    ("kv",   "Quality", "Testing and reliability"),
    ("kv",   "Stack",   "TypeScript / Python / Supabase"),
    ("gap",),
    ("sec",  "SELECTED.WORK", 28),
    ("kv",   "Ledgerly",    "Self-hosted personal finance"),
    ("kv",   "ClaimGuard",  "Governed repair benchmarking"),
    ("kv",   "InfiniteCtx", "Memory for AI coding agents"),
    ("kv",   "Humanonly",   "Human-governed social platform"),
    ("kv",   "alarmclock",  "Deterministic Python CLI"),
    ("gap",),
    ("tag",  "FROM IDEA TO GOVERNED PRODUCT"),
]

def build(theme_name):
    t = THEMES[theme_name]
    rows = ascii_rows(invert=(theme_name == "light"))
    s = []
    s.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'font-family="{MONO}" role="img" '
        f'aria-label="Varun Chennuri, AI product architect">'
    )
    s.append(f'''<defs>
<linearGradient id="pg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{t["grad_a"]}"/>
  <stop offset="1" stop-color="{t["grad_b"]}"/>
</linearGradient>
<linearGradient id="glow" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{t["scan"]}" stop-opacity="0"/>
  <stop offset="0.5" stop-color="{t["scan"]}" stop-opacity="0.16"/>
  <stop offset="1" stop-color="{t["scan"]}" stop-opacity="0"/>
</linearGradient>
</defs>''')
    # canvas + outer window
    s.append(f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}"/>')
    # title bar
    s.append(f'<path d="M0 12 a12 12 0 0 1 12 -12 h{W-24} a12 12 0 0 1 12 12 v14 h-{W} z" fill="{t["chrome"]}"/>')
    for i, c in enumerate((t["light1"], t["light2"], t["light3"])):
        s.append(f'<circle cx="{18 + i*16}" cy="13" r="4.5" fill="{c}"/>')
    s.append(f'<text x="{W/2}" y="17" text-anchor="middle" font-size="10" fill="{t["title"]}">varun@build ~ % ./profile</text>')
    s.append(f'<circle cx="{W-86}" cy="13" r="3" fill="{t["accent"]}"/>')
    s.append(f'<text x="{W-76}" y="16.5" font-size="8.5" letter-spacing="2" fill="{t["accent"]}">BUILDING</text>')

    # left panel
    s.append(f'<rect x="{L_X}" y="{PANEL_TOP}" width="{L_W}" height="{PANEL_H}" rx="6" fill="{t["panel"]}" stroke="{t["border"]}"/>')
    s.append(f'<text x="{L_X+16}" y="{PANEL_TOP+20}" font-size="9" letter-spacing="3" fill="{t["head"]}">PORTRAIT / VARUN</text>')
    # corner ticks
    for cx, cy, dx, dy in ((L_X+10, PANEL_TOP+30, 1, 1), (L_X+L_W-10, PANEL_TOP+PANEL_H-12, -1, -1)):
        s.append(f'<path d="M{cx} {cy+dy*10} v{-dy*10} h{dx*10}" fill="none" stroke="{t["accent"]}" stroke-width="1.4" opacity="0.7"/>')
    # ascii portrait
    s.append(f'<g font-size="{P_FS}" fill="url(#pg)" xml:space="preserve">')
    for i, row in enumerate(rows):
        y = P_Y0 + i * P_LH
        s.append(
            f'<text x="{P_X0}" y="{y}" textLength="{P_TEXTLEN}" '
            f'lengthAdjust="spacingAndGlyphs">{esc(row)}</text>'
        )
    s.append('</g>')
    # scanline glow band across portrait
    s.append(f'<rect x="{L_X+2}" y="{PANEL_TOP+206}" width="{L_W-4}" height="26" fill="url(#glow)"/>')

    # right panel
    s.append(f'<rect x="{R_X}" y="{PANEL_TOP}" width="{R_W}" height="{PANEL_H}" rx="6" fill="{t["panel"]}" stroke="{t["border"]}"/>')
    s.append(f'<text x="{T_X0}" y="{PANEL_TOP+20}" font-size="9" letter-spacing="3" fill="{t["head"]}">PROFILE / BUILDER</text>')

    y = T_Y0
    s.append(f'<g font-size="{T_FS}" xml:space="preserve">')
    for line in RIGHT_LINES:
        kind = line[0]
        if kind == "gap":
            y += T_LH * 0.55
            continue
        if kind == "hdr":
            s.append(f'<text x="{T_X0}" y="{y}"><tspan fill="{t["val"]}" font-weight="bold">{esc(line[1])}</tspan><tspan fill="{t["dots"]}">{esc(line[2])}</tspan></text>')
        elif kind == "sec":
            s.append(f'<text x="{T_X0}" y="{y}" fill="{t["muted"]}">- <tspan font-weight="bold" fill="{t["val"]}">{esc(line[1])}</tspan> <tspan fill="{t["dots"]}">{"-" * line[2]}</tspan></text>')
        elif kind == "kv":
            label, value = line[1], line[2]
            fill = "." * max(2, 14 - len(label))
            s.append(
                f'<text x="{T_X0}" y="{y}">'
                f'<tspan fill="{t["dots"]}">. </tspan>'
                f'<tspan fill="{t["key"]}" font-weight="bold">{esc(label)}</tspan>'
                f'<tspan fill="{t["dots"]}">: {fill} </tspan>'
                f'<tspan fill="{t["val"]}">{esc(value)}</tspan></text>'
            )
        elif kind == "tag":
            s.append(f'<text x="{T_X0}" y="{y}" font-size="10" letter-spacing="1.5" font-weight="bold" fill="{t["val"]}">{esc(line[1])}</text>')
        y += T_LH
    s.append('</g>')

    # footer strip
    s.append(f'<rect x="0" y="{H-26}" width="{W}" height="26" fill="{t["chrome"]}"/>')
    s.append(f'<rect x="0" y="{H-4}" width="{W}" height="4" fill="{t["accent"]}" opacity="0.85"/>')
    s.append(f'<text x="{W/2}" y="{H-10}" text-anchor="middle" font-size="8.5" letter-spacing="3" fill="{t["title"]}">PRODUCT ENGINEERING / AI AGENTS / DEALER PLATFORMS / DEVELOPER TOOLS</text>')
    s.append('</svg>')
    return "\n".join(s)

for name in ("dark", "light"):
    out = f"builder-profile-{name}.svg"
    with open(out, "w") as f:
        f.write(build(name))
    print(out, "written")

import math as m
import random as r
import turtle as t
import tkinter.font as tkf

SC = 21
OY = 20
DURATION = 5.8  # Calibrated so the entire heart completes in ~15 seconds on Windows
TICK = 16
ANIM = 28
LIFT = 34
GAP = 7
SIZES = (9, 10, 11, 12)
FONT = "Arial"
BG = "#060208"

s = t.Screen()
s.setup(800, 800)
s.bgcolor(BG)
s.title("Love Heart")
s.tracer(0)

cv = s.getcanvas()
rng = r.Random(11)


PHRASES = [
    "I love you",
    "Seni seviyorum",
    "Te amo",
    "Je t'aime",
    "Ich liebe dich",
    "Ti amo",
    "Eu te amo",
    "Я тебя люблю",
    "사랑해",
    "愛してる",
    "我爱你",
    "मैं तुमसे प्यार करता हूँ",
    "Σ' αγαπώ",
    "Ik hou van jou",
    "Jag älskar dig",
    "Kocham cię",
    "ฉันรักเธอ",
    "Anh yêu em",
    "Aku cinta kamu",
    "Я тебе кохаю",
    "আমি তোমাকে ভালোবাসি",
    "நான் உன்னை காதலிக்கிறேன்",
    "నేను నిన్ను ప్రేమిస్తున్నాను",
    "मी तुझ्यावर प्रेम करतो",
    "હું તને પ્રેમ કરું છું",
    "ನಾನು ನಿನ್ನನ್ನು ಪ್ರೀತಿಸುತ್ತೇನೆ",
    "ഞാൻ നിന്നെ സ്നേഹിക്കുന്നു",
    "ਮੈਂ ਤੈਨੂੰ ਪਿਆਰ ਕਰਦਾ ਹਾਂ",
    "म तिमीलाई माया गर्छु",
    "මම ඔයාට ආදරෙයි",
    "ချစ်တယ်",
    "ខ្ញុំស្រលាញ់អ្នក",
    "ຂ້ອຍຮັກເຈົ້າ",
    "მიყვარხარ",
    "Saya cintakan awak",
    "Mahal kita",
    "Nakupenda",
    "Ngiyakuthanda",
    "Ek is lief vir jou",
    "እወድሃለሁ",
    "Ina son ka",
    "Mo nifẹ rẹ",
    "Hụrụ m gị n'anya",
    "Miluji tě",
    "Maite zaitut",
    "أحبك",
    "Səni sevirəm",
    "Volim te",
    "Tá grá agam duit",
    "Dw i'n dy garu di",
    "Waan ku jeclahay",
    "T'estimo",
    "Minä rakastan sinua",
    "Ég elska þig",
    "Jeg elsker deg",
    "Ma armastan sind",
    "Мен сені жақсы көремін",
    "Я цябе кахаю",
    "Të dua",
    "Lúbim ťa",
    "Te iubesc",
    "Волим те",
    "Quérote",
    "Обичам те",
    "Ljubim te",
    "دوستت دارم",
    "Би чамд хайртай",
    "میں تم سے پیار کرتا ہوں",
    "Men seni sevaman",
    "Szeretlek",
    "אני אוהב אותך",
    "Aloha au iā ʻoe",
    "Kei te aroha au ki a koe",
    "Ou te alofa ia te oe",
    "Tiako ianao",
    "Mi amas vin",
    "Ech hunn dech gär",
    "Ik hâld fan dy",
    "Inħobbok",
    "Ti tengu caru",
    "Aš tave myliu",
    "Es tevi mīlu",
    "Ez te hez dikim",
    "زه تا سره مینه لرم",
    "Au domoni iko",
    "Jeg elsker dig",
    "Ես քեզ սիրում եմ",
    "איך האָב דיך ליב",
]

_fonts = {}


def font_for(size):
    if size not in _fonts:
        _fonts[size] = tkf.Font(
            root=cv, family=FONT, size=size, weight="bold"
        )
    return _fonts[size]


def heart(a):
    x = 16 * (m.sin(a) ** 3)
    y = (
        13 * m.cos(a)
        - 5 * m.cos(2 * a)
        - 2 * m.cos(3 * a)
        - m.cos(4 * a)
    )
    return x * SC, y * SC + OY


def hx(c):
    return "#%02x%02x%02x" % tuple(
        int(max(0, min(1, v)) * 255) for v in c
    )


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def dim(c, k):
    return tuple(v * k for v in c)


POLY = [heart(2 * m.pi * i / 720) for i in range(720)]
EDGES = list(zip(POLY, POLY[1:] + POLY[:1]))
YMAX = max(p[1] for p in POLY)
YMIN = min(p[1] for p in POLY)
CY = (YMAX + YMIN) / 2


def spans(y):
    xs = []
    for (x1, y1), (x2, y2) in EDGES:
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return list(zip(xs[0::2], xs[1::2]))


def intersect(A, B):
    out = []
    for a in A:
        for b in B:
            lo, hi = max(a[0], b[0]), min(a[1], b[1])
            if hi - lo > 14:
                out.append((lo, hi))
    return out


def phrase_cycle():
    while True:
        order = PHRASES[:]
        rng.shuffle(order)
        yield from order


def math_dist(x, y):
    return m.hypot(x / (16 * SC), (y - CY) / (14.5 * SC))


def build():
    cycle = phrase_cycle()
    row_h = max(font_for(z).metrics("linespace") for z in SIZES) + 4
    half = row_h / 2
    placed = []

    y = YMAX - half
    while y > YMIN + half:
        row = intersect(spans(y + half), spans(y - half))

        for lo, hi in row:
            lo += 4
            hi -= 4
            cur = lo + rng.uniform(0, 8)
            line = []

            while True:
                fit = None
                for _ in range(10):
                    text = next(cycle)
                    size = rng.choice(SIZES)
                    w = font_for(size).measure(text)
                    if cur + w <= hi:
                        fit = (text, size, w)
                        break
                if not fit:
                    break
                text, size, w = fit
                line.append([cur + w / 2, text, size, w])
                cur += w + GAP

            if not line:
                continue

            if len(line) > 1:
                left = hi - (line[-1][0] + line[-1][3] / 2)
                for i, it in enumerate(line):
                    it[0] += left * i / (len(line) - 1)
            else:
                line[0][0] = (lo + hi) / 2

            for i, (x, text, size, w) in enumerate(line):
                edge = i == 0 or i == len(line) - 1
                placed.append(dict(x=x, y=y, text=text, size=size, edge=edge))

        y -= row_h

    for p in placed:
        nx = p["x"] / (16 * SC)
        ny = (p["y"] - CY) / (14.5 * SC)
        rad = min(1.0, math_dist(p["x"], p["y"]))

        # 3-zone vibrant neon coloring matching the video:
        # Top-left lobe: Warm Gold / Amber
        # Center & Top-right: Vibrant Mint Green
        # Right edge & Bottom tip: Electric Cyan / Sky Blue
        if nx < -0.10 and ny > 0.10:
            c_hex = "#f5be7c" if ny > 0.40 else "#ebda91"
        elif nx > 0.25 or ny < -0.20 or (nx > 0.08 and ny < 0.08):
            c_hex = "#24d1ff" if ny > -0.5 else "#32a2ff"
        else:
            c_hex = "#45ff9d"

        base = tuple(int(c_hex[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
        p["color"] = base
        p["rad"] = rad

    edges = [p for p in placed if p["edge"]]
    inner = [p for p in placed if not p["edge"]]
    edges.sort(key=lambda p: m.atan2(p["x"], p["y"] - CY) % (2 * m.pi))
    inner.sort(key=lambda p: -p["rad"] + rng.uniform(0, 0.08))
    return edges + inner


FLASH = (0.90, 1.0, 0.95)
main_ids = []
active = []
tick_no = 0


def clamp(v):
    return max(0.0, min(1.0, v))


def spawn(p):
    x, y = p["x"], -p["y"]
    size, text, c = p["size"], p["text"], p["color"]
    font = (FONT, size, "bold")
    big = (FONT, size + 1, "bold")

    shadow = cv.create_text(x + 2, y + 3, text=text, font=font, fill=BG)
    halo = cv.create_text(x, y, text=text, font=big, fill=BG)
    main = cv.create_text(x, y - LIFT, text=text, font=font, fill=BG)

    p.update(shadow=shadow, halo=halo, main=main,
             f=0, dx=rng.uniform(-10, 10))
    main_ids.append((main, c))
    active.append(p)


def animate(p):
    p["f"] += 1
    u = clamp(p["f"] / ANIM)
    e = 1 - (1 - u) ** 3
    c = p["color"]
    x, y = p["x"], -p["y"]
    hover = (1 - e) * LIFT
    px = x + p["dx"] * (1 - e)
    py = y - hover

    cv.itemconfig(p["shadow"], fill=hx(mix(BGC, dim(c, 0.30), e)))
    cv.itemconfig(p["halo"], fill=hx(mix(BGC, dim(c, 0.20), e * e)))
    cv.coords(p["halo"], px, py)

    flash = 0.75 * math_sin(clamp((u - 0.55) / 0.45))
    col = mix(mix(BGC, c, e ** 1.5), FLASH, flash)
    cv.itemconfig(p["main"], fill=hx(col))
    cv.coords(p["main"], px, py)

    if u >= 1:
        cv.coords(p["halo"], x, y)
        cv.coords(p["main"], x, y)
        cv.itemconfig(p["main"], fill=hx(c))
        return False
    return True


def math_sin(v):
    return m.sin(m.pi * v)


BGC = tuple(int(BG[i:i + 2], 16) / 255 for i in (1, 3, 5))
ORDER = build()
items = iter(ORDER)
RATE = len(ORDER) / (DURATION * 1000 / TICK)
acc = 0.0
spawning = True


def step():
    global spawning, acc
    if spawning:
        acc += RATE
        try:
            while acc >= 1:
                acc -= 1
                spawn(next(items))
        except StopIteration:
            spawning = False

    active[:] = [p for p in active if animate(p)]

    if not spawning and not active:
        shimmer()
        return
    cv.after(TICK, step)


def _safe(i, c):
    try:
        cv.itemconfig(i, fill=hx(c))
    except Exception:
        pass


def shimmer():
    for _ in range(1):
        i, c = rng.choice(main_ids)
        _safe(i, mix(c, FLASH, 0.6))
        cv.after(260, lambda i=i, c=c: _safe(i, c))
    cv.after(140, shimmer)


try:
    cv.after(200, step)
    t.done()
except (t.Terminator, Exception):
    pass


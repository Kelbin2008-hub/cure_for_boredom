import math
import tkinter as tk
import tkinter.font as tkfont

# Full international phrase list
PHRASES = [
    "I love you", "Te amo", "Je t'aime", "Ich liebe dich", "Ti amo",
    "Eu te amo", "Ik hou van jou", "Jag älskar dig", "Jeg elsker deg",
    "Rakastan sinua", "Ég elska þig", "Tá grá agam duit", "Rwy'n dy garu di",
    "Σ' αγαπώ", "Я тебя люблю", "Я тебе кохаю", "Kocham cię", "Miluji tě",
    "Ľúbim ťa", "Szeretlek", "Te iubesc", "Обичам те", "Волим те",
    "Volim te", "Ljubim te", "Të dua", "Aš tave myliu", "Es tevi mīlu",
    "Ma armastan sind", "Seni seviyorum", "أحبك", "אני אוהב אותך",
    "دوستت دارم", "میں تم سے محبت کرتا ہوں", "मैं तुमसे प्यार करता हूँ",
    "আমি তোমায় ভালোবাসি", "ਮੈਂ ਤੈਨੂੰ ਪਿਆਰ ਕਰਦਾ ਹਾਂ", "હું તને પ્રેમ કરું છું",
    "मी तुझ्यावर प्रेम करतो", "म तिमीलाई माया गर्छु", "මම ඔයාට ආදරෙයි",
    "நான் உன்னை காதலிக்கிறேன்", "నేను నిన్ను ప్రేమిస్తున్నాను", "ನಾನು ನಿನ್ನನ್ನು ಪ್ರೀತಿಸುತ್ತೇನೆ",
    "ഞാൻ നിന്നെ സ്നേഹിക്കുന്നു", "ମୁଁ ତୁମକୁ ଭଲ ପାଏ", "মই তোমাক ভাল পাওঁ",
    "我爱你", "愛してる", "사랑해", "ฉันรักคุณ", "Anh yêu em",
    "Aku cinta kamu", "Saya cinta padamu", "Mahal kita", "မင်းကိုချစ်တယ်",
    "ខ្ញុំស្រឡាញ់អ្នក", "ຂ້ອຍຮັກເຈົ້າ", "Би чамд хайртай", "Мен сені сүйемін",
    "Men seni sevaman", "მე შեն მიყვარხარ", "Ես քեզ սիրում եм", "Mən səni sevirəm",
    "Nakupenda", "Ngiyakuthanda", "Ndiyakuthanda", "Ek is lief vir jou",
    "Mo nifẹ rẹ", "A hụrụ m gị n’anya", "እወድሃለሁ", "Ina son ka", "Mwen renmen ou",
    "Quérote", "T'estimo", "Maite zaitut", "Mi amas vin",
]


def get_neon_color(nx, ny):
    """
    Symmetric 3-zone neon color gradient:
    - Top-left lobe: Warm Gold / Amber
    - Center & Top-right: Vibrant Mint Green
    - Right edge & Bottom tip: Electric Cyan / Sky Blue
    """
    if nx < -0.12 and ny > 0.15:
        return "#f5be7c" if ny > 0.45 else "#ebda91"
    elif nx > 0.28 or ny < -0.22 or (nx > 0.08 and ny < 0.08):
        return "#24d1ff" if ny > -0.5 else "#32a2ff"
    else:
        return "#45ff9d"


def build_symmetric_perfect_heart(cx, cy, scale, fonts):
    """
    Generates a mathematically flawless, upright heart silhouette across 25 rows.
    Calculates exact left/right symmetry for every row so nothing is lopsided.
    """
    num_rows = 25
    y_min, y_max = -1.15, 1.15
    row_step = (y_max - y_min) / (num_rows - 1)
    col_gap = 14

    right_border = []
    left_border = []
    interior = []
    phrase_idx = 0

    for r in range(num_rows):
        ny = y_max - r * row_step
        py = int(cy - ny * scale * 1.05)

        # Find valid symmetric width inside standard heart equation: (x^2 + y^2 - 1)^3 - x^2 * y^3 <= 0
        valid_xs = []
        for i in range(801):
            x = -1.5 + i * (3.0 / 800.0)
            a = x * x + ny * ny - 1.0
            if (a * a * a - (x * x) * (ny * ny * ny)) <= 0.0:
                valid_xs.append(x)

        if not valid_xs:
            continue

        # Check for top notch split (two symmetrical lobes)
        segments = []
        seg_start = valid_xs[0]
        prev_x = valid_xs[0]
        for x in valid_xs[1:]:
            if x - prev_x > 0.04:
                segments.append((seg_start, prev_x))
                seg_start = x
            prev_x = x
        segments.append((seg_start, prev_x))

        for seg_idx, (s_min, s_max) in enumerate(segments):
            px_min = int(cx + s_min * scale)
            px_max = int(cx + s_max * scale)
            avail_w = px_max - px_min

            if avail_w < 35:
                continue

            # Pack phrases horizontally with exact pixel width measuring
            row_items = []
            used_w = 0
            while True:
                text = PHRASES[phrase_idx % len(PHRASES)]
                f_key = "small" if len(text) > 15 else ("med" if len(text) > 9 else "large")
                font_obj, font_tup = fonts[f_key]
                w = font_obj.measure(text)

                next_w = w if not row_items else (used_w + col_gap + w)
                if next_w <= avail_w:
                    row_items.append((text, w, font_tup))
                    used_w = next_w
                    phrase_idx += 1
                else:
                    if not row_items:
                        for k in range(len(PHRASES)):
                            cand = PHRASES[(phrase_idx + k) % len(PHRASES)]
                            if len(cand) <= 12:
                                f_obj, f_tup = fonts["small"]
                                cw = f_obj.measure(cand)
                                row_items.append((cand, cw, f_tup))
                                used_w = cw
                                phrase_idx += k + 1
                                break
                    break

            if not row_items:
                continue

            # Center perfectly within the segment
            start_x = px_min + (avail_w - used_w) // 2
            cur_x = start_x
            placed = []

            for text, w, font_tup in row_items:
                wx = cur_x + w // 2
                nx = (wx - cx) / float(scale)
                color = get_neon_color(nx, ny)
                placed.append({
                    "x": wx,
                    "y": py,
                    "text": text,
                    "color": color,
                    "font": font_tup,
                })
                cur_x += w + col_gap

            # Categorize into contour border vs interior fill
            if r <= 2 or r >= num_rows - 2:
                if len(segments) == 2:
                    if seg_idx == 1:
                        right_border.extend(placed)
                    else:
                        left_border.extend(placed)
                else:
                    right_border.extend(placed)
            else:
                if len(placed) == 1:
                    right_border.append(placed[0])
                elif len(placed) == 2:
                    left_border.append(placed[0])
                    right_border.append(placed[1])
                else:
                    left_border.append(placed[0])
                    right_border.append(placed[-1])
                    interior.extend(placed[1:-1])

    # Contour-first reveal order: Top-right lobe down to tip -> up left lobe -> interior rows
    left_border.reverse()
    return right_border + left_border + interior


class PerfectSymmetricApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Love Heart")
        self.root.configure(bg="#030508")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = int(screen_w * 0.88)
        win_h = int(screen_h * 0.84)
        pos_x = int(screen_w * 0.06)
        pos_y = int(screen_h * 0.05)
        self.root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

        self.canvas = tk.Canvas(self.root, bg="#030508", highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        f_small = ("Segoe UI", 10, "bold")
        f_med = ("Segoe UI", 11, "bold")
        f_large = ("Segoe UI", 12, "bold")
        fonts = {
            "small": (tkfont.Font(family="Segoe UI", size=10, weight="bold"), f_small),
            "med": (tkfont.Font(family="Segoe UI", size=11, weight="bold"), f_med),
            "large": (tkfont.Font(family="Segoe UI", size=12, weight="bold"), f_large),
        }

        cx = win_w // 2
        cy = int(win_h * 0.48)
        scale = int(min(win_w, win_h) * 0.32)

        self.sequence = build_symmetric_perfect_heart(cx, cy, scale, fonts)
        self.idx = 0

        # Fast & smooth (~6 seconds total build time)
        self.delay_ms = max(20, int(6000 / max(1, len(self.sequence))))
        self.root.after(300, self.step)

    def step(self):
        if self.idx >= len(self.sequence):
            return

        item = self.sequence[self.idx]
        self.idx += 1

        # Subtle dark neon shadow + crisp text
        self.canvas.create_text(
            item["x"] + 1,
            item["y"] + 1,
            text=item["text"],
            fill="#071e24",
            font=item["font"],
            anchor="center",
        )
        main_id = self.canvas.create_text(
            item["x"],
            item["y"],
            text=item["text"],
            fill="#ffffff",
            font=item["font"],
            anchor="center",
        )
        self.root.after(
            22, lambda i=main_id, c=item["color"]: self.canvas.itemconfig(i, fill=c)
        )

        self.root.after(self.delay_ms, self.step)


if __name__ == "__main__":
    root = tk.Tk()
    app = PerfectSymmetricApp(root)
    root.mainloop()


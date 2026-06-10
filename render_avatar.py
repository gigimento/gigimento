"""Render gigimento avatar as PNG + animated GIF."""
from PIL import Image, ImageDraw
import math, os

SIZE = 400
OUT = r"C:\Users\Igor\AppData\Local\Temp\opencode\github-export\gigimento"

def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def draw_frame(phase=0):
    img = Image.new("RGBA", (SIZE, SIZE))
    draw = ImageDraw.Draw(img)

    # Background
    for y in range(SIZE):
        t = y / SIZE
        r = int(26 + (22 - 26) * t)
        g = int(26 + (33 - 26) * t)
        b = int(46 + (62 - 46) * t)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

    # Hand-drawn circuit board traces (pixel coords)
    accent = (0, 210, 255)
    accent_dim = tuple(int(c * 0.4) for c in accent)
    pulse = 0.3 + 0.2 * math.sin(phase)

    traces = [
        (60, 200, 100, 200, 100, 140, 140, 140),
        (80, 200, 80, 280, 140, 280),
        (300, 150, 340, 150, 340, 230, 320, 230),
        (280, 260, 320, 260, 320, 220, 340, 220),
        (120, 300, 200, 300, 200, 260, 240, 260),
        (250, 100, 290, 100, 290, 140, 270, 140),
    ]

    for pts in traces:
        coords = list(zip(pts[::2], pts[1::2]))
        for i in range(len(coords) - 1):
            c = tuple(int(a * pulse) for a in accent)
            draw.line([coords[i], coords[i+1]], fill=c, width=2)

    # CPU chip
    chip_x, chip_y, chip_w, chip_h = 140, 140, 120, 120
    draw.rounded_rectangle([chip_x, chip_y, chip_x+chip_w, chip_y+chip_h],
                           radius=12, outline=accent, width=3)
    inner_c = tuple(int(a * 0.15) for a in accent)
    draw.rounded_rectangle([160, 160, 240, 240], radius=6, fill=inner_c)
    center_c = tuple(int(a * 0.3 * pulse) for a in accent)
    draw.rounded_rectangle([175, 175, 225, 225], radius=4, fill=center_c)

    # Chip pins
    pins_accent = tuple(int(a * (0.5 + 0.5 * pulse)) for a in accent)
    for x in [170, 200, 230]:
        draw.line([(x, 140), (x, 120)], fill=pins_accent, width=3)
        draw.line([(x, 260), (x, 280)], fill=pins_accent, width=3)
    for y in [170, 200, 230]:
        draw.line([(140, y), (120, y)], fill=pins_accent, width=3)
        draw.line([(260, y), (280, y)], fill=pins_accent, width=3)

    # Waveform
    waveform = [(60 + i * 28, 330 - 40 * math.sin((i * 0.8) + phase * 2))
                for i in range(11)]
    for i in range(len(waveform) - 1):
        c = tuple(int(a * (0.4 + 0.3 * math.sin(phase + i * 0.3))) for a in accent)
        draw.line([waveform[i], waveform[i+1]], fill=c, width=2)

    return img

print("Rendering frames...")
frames = []
for i in range(12):
    phase = i * (2 * math.pi / 12)
    img = draw_frame(phase)
    frames.append(img)

# Save PNG (middle frame)
png_path = os.path.join(OUT, "profile-avatar.png")
frames[0].save(png_path, "PNG")
print(f"Saved {png_path}")

# Save animated GIF (first 8 frames, smaller)
gif_path = os.path.join(OUT, "profile-avatar.gif")
gif_frames = [f.resize((200, 200), Image.LANCZOS).convert("P",
    dither=Image.Dither.FLOYDSTEINBERG, colors=64) for f in frames]
gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:],
                   optimize=True, duration=120, loop=0, palette=gif_frames[0].getpalette())
print(f"Saved {gif_path} ({len(frames)} frames)")

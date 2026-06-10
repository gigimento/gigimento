"""G-Chip avatar v3 — clean pieslice-based G letterform."""
from PIL import Image, ImageDraw
import math, os

OUT = r"C:\Users\Igor\AppData\Local\Temp\opencode\github-export\gigimento"
SZ = 800
CX = CY = SZ // 2

# G geometry
R_OUT = 300          # outer radius
R_IN = 170           # inner radius (cutout)
GAP_START = 25       # G opening start angle (bottom-right)
GAP_END = 295        # G opening end angle (top-right)
CROSS_Y = -40        # crossbar vertical offset from center
CROSS_W = 36         # crossbar thickness

def draw_frame(phase=0):
    img = Image.new("RGBA", (SZ, SZ))
    draw = ImageDraw.Draw(img)
    p = 0.85 + 0.15 * math.sin(phase * 1.5)

    # Background radial gradient
    for y in range(SZ):
        dist = abs(y - CY) / 390
        if dist > 1: continue
        t = y / SZ
        r = int(13 + (22 - 13) * t)
        g = int(17 + (27 - 17) * t)
        b = int(23 + (34 - 23) * t)
        draw.line([(0, y), (SZ, y)], fill=(r, g, b, 255))

    # Outer border
    draw.ellipse([CX-390, CY-390, CX+390, CY+390], outline=(48, 54, 61), width=2)

    # Glow rings
    for i in range(10):
        rr = 320 + i * 4
        a = max(0, int(35 * (1 - i / 10)))
        draw.ellipse([CX-rr, CY-rr, CX+rr, CY+rr], outline=(0, 212, 255, a), width=1)

    # Rotating tick marks
    for i in range(8):
        ang = math.radians(i * 45 + phase * 12)
        r1, r2 = 340, 358
        x1 = CX + r1 * math.cos(ang)
        y1 = CY + r1 * math.sin(ang)
        x2 = CX + r2 * math.cos(ang)
        y2 = CY + r2 * math.sin(ang)
        a = int(180 * (0.3 + 0.7 * math.sin(phase + i * 0.8)))
        draw.line([(x1, y1), (x2, y2)], fill=(0, 212, 255, a), width=2)

    # Orbital data nodes
    for i in range(4):
        ang = math.radians(i * 90 + phase * 18)
        r = 270
        x = CX + r * math.cos(ang)
        y = CY + r * math.sin(ang)
        a = int(200 * (0.4 + 0.6 * math.sin(phase * 1.2 + i * 1.5)))
        draw.ellipse([x-5, y-5, x+5, y+5], fill=(0, 212, 255, a))

    # G body: outer pieslice (the ring)
    cyan = (0, 212, 255)
    bbox_out = [CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT]
    draw.pieslice(bbox_out, GAP_START, GAP_END, fill=cyan)

    # G inner cutout: same angle, smaller radius, background fill
    bg = (13, 17, 23)
    bbox_in = [CX - R_IN, CY - R_IN, CX + R_IN, CY + R_IN]
    draw.pieslice(bbox_in, GAP_START, GAP_END, fill=bg)

    # Crossbar
    y0 = CY + CROSS_Y - CROSS_W // 2
    y1 = CY + CROSS_Y + CROSS_W // 2
    x_left = CX + int(R_IN * math.cos(math.radians(GAP_END))) - 10
    x_right = CX + int(R_OUT * math.cos(math.radians(GAP_START))) - 5
    draw.rectangle([x_left, y0, x_right, y1], fill=cyan)

    # Crossbar gap (erase the right portion to maintain G shape)
    gap_x = CX + int(R_OUT * math.cos(math.radians(GAP_START))) - 45
    draw.rectangle([gap_x, y0, x_right, y1], fill=bg)

    # Edge highlight
    h = (120, 240, 255)
    draw.arc(bbox_out, GAP_START - 2, GAP_END + 2, fill=h, width=2)

    # Center glow
    gr = 6 + 4 * math.sin(phase * 2)
    for r in range(int(gr), 0, -1):
        a = int(70 * (1 - r / gr))
        draw.ellipse([CX-r, CY-r, CX+r, CY+r], fill=(0, 212, 255, a))

    return img

print("Rendering frames...")
frames = [draw_frame(i * (2*math.pi/12)) for i in range(12)]

# PNG 400px
frames[0].resize((400, 400), Image.LANCZOS).save(os.path.join(OUT, "profile-avatar.png"), "PNG")
print("PNG saved")

# GIF 200px
gf = [f.resize((200, 200), Image.LANCZOS).convert("P",
       palette=Image.Palette.ADAPTIVE, dither=Image.Dither.FLOYDSTEINBERG, colors=32)
       for f in frames]
gf[0].save(os.path.join(OUT, "profile-avatar.gif"), save_all=True,
           append_images=gf[1:], optimize=True, duration=120, loop=0)
print("GIF saved")

"""
Generate realistic mock UI screenshots of the AWS Features Tracker app using Pillow.
"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

OUT = "/workshop/aws-new-features/slides_assets"
os.makedirs(OUT, exist_ok=True)

W, H = 1400, 900

# ── colour palette ──────────────────────────────────────────────────────────
BG        = (248, 250, 252)   # gray-50
WHITE     = (255, 255, 255)
BORDER    = (226, 232, 240)   # gray-200
TEXT_PRI  = (15,  23,  42)    # slate-900
TEXT_SEC  = (100, 116, 139)   # slate-500
TEXT_MUT  = (148, 163, 184)   # slate-400
ORANGE    = (234, 88,  12)    # orange-600
ORANGE_L  = (255, 237, 213)   # orange-100
ORANGE_LT = (154, 52,  18)    # orange-800
BLUE      = (37,  99,  235)   # blue-600
BLUE_L    = (219, 234, 254)   # blue-100
BLUE_LT   = (30,  64,  175)   # blue-800
GREEN_L   = (220, 252, 231)
GREEN_D   = (22,  101, 52)
YELLOW_L  = (254, 249, 195)
YELLOW_D  = (133, 77,  14)
EMERALD_L = (209, 250, 229)
EMERALD_D = (6,   78,  59)
RED_L     = (254, 226, 226)
RED_D     = (153, 27,  27)
PURPLE_L  = (243, 232, 255)
PURPLE_D  = (88,  28,  135)
INDIGO_L  = (224, 231, 255)
INDIGO_D  = (49,  46,  129)
CYAN_L    = (207, 250, 254)
CYAN_D    = (22,  78,  99)
SLATE_L   = (241, 245, 249)
SLATE_D   = (51,  65,  85)
HEADER_BG = (255, 255, 255)
SHADOW    = (203, 213, 225)

def load_font(size, bold=False):
    try:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf".format("-Bold" if bold else "")
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def rounded_rect(draw, xy, radius, fill, outline=None, outline_width=1):
    x1, y1, x2, y2 = xy
    r = radius
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    draw.ellipse([x1, y1, x1+2*r, y1+2*r], fill=fill)
    draw.ellipse([x2-2*r, y1, x2, y1+2*r], fill=fill)
    draw.ellipse([x1, y2-2*r, x1+2*r, y2], fill=fill)
    draw.ellipse([x2-2*r, y2-2*r, x2, y2], fill=fill)
    if outline:
        draw.arc([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=outline, width=outline_width)
        draw.arc([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=outline, width=outline_width)
        draw.arc([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=outline, width=outline_width)
        draw.arc([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=outline, width=outline_width)
        draw.line([x1+r, y1, x2-r, y1], fill=outline, width=outline_width)
        draw.line([x1+r, y2, x2-r, y2], fill=outline, width=outline_width)
        draw.line([x1, y1+r, x1, y2-r], fill=outline, width=outline_width)
        draw.line([x2, y1+r, x2, y2-r], fill=outline, width=outline_width)

def pill(draw, xy, text, bg, fg, font):
    x1, y1, x2, y2 = xy
    rounded_rect(draw, (x1, y1, x2, y2), 8, bg)
    tw = draw.textlength(text, font=font)
    tx = x1 + ((x2-x1) - tw) // 2
    ty = y1 + ((y2-y1) - font.size) // 2 - 1
    draw.text((tx, ty), text, fill=fg, font=font)

def card(draw, x, y, w, h):
    # subtle shadow
    draw.rectangle([x+2, y+2, x+w+2, y+h+2], fill=SHADOW)
    rounded_rect(draw, (x, y, x+w, y+h), 12, WHITE, BORDER, 1)

def draw_header(draw, img, W, search_val="", show_filters=True):
    # header bg
    draw.rectangle([0, 0, W, 120 if show_filters else 70], fill=HEADER_BG)
    draw.line([0, 120 if show_filters else 70, W, 120 if show_filters else 70], fill=BORDER, width=1)

    f_title = load_font(20, bold=True)
    f_sub   = load_font(12)
    f_input = load_font(14)

    # logo area
    draw.rectangle([24, 14, 52, 44], fill=ORANGE)
    draw.text((27, 18), "AWS", fill=WHITE, font=load_font(11, bold=True))
    draw.text((24, 46), "AWS Features Tracker", fill=TEXT_PRI, font=f_title)
    draw.text((24, 70), "AI-summarized AWS announcements", fill=TEXT_SEC, font=f_sub)

    if show_filters:
        # search box
        sx, sy, sw, sh = 24, 88, W-48, 28
        rounded_rect(draw, (sx, sy, sx+sw, sy+sh), 8, WHITE, BORDER, 1)
        draw.text((sx+10, sy+7), "🔍  " + (search_val or "Search features, services..."),
                  fill=TEXT_MUT if not search_val else TEXT_PRI, font=f_input)

def draw_filter_row(draw, y, active_service="", active_type=""):
    f = load_font(12)
    fb = load_font(12, bold=True)
    filters = [
        ("All services" if not active_service else active_service, BLUE_L if active_service else WHITE),
        ("All types" if not active_type else active_type, BLUE_L if active_type else WHITE),
        ("From date", WHITE),
        ("To date", WHITE),
        ("Newest First ↓", WHITE),
    ]
    x = 24
    for label, bg in filters:
        tw = draw.textlength(label, font=f)
        w = int(tw) + 24
        rounded_rect(draw, (x, y, x+w, y+26), 6, bg, BORDER, 1)
        draw.text((x+12, y+7), label,
                  fill=BLUE_LT if bg == BLUE_L else TEXT_SEC, font=fb if bg==BLUE_L else f)
        x += w + 8

# ════════════════════════════════════════════════════════════════════════════
# SCREENSHOT 1 — Main search page (feature grid)
# ════════════════════════════════════════════════════════════════════════════
def make_search_page():
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, img, W)
    draw_filter_row(draw, 128)

    f_small = load_font(11)
    draw.text((24, 166), "Showing 12 of 12 features", fill=TEXT_SEC, font=f_small)

    FEATURES = [
        {
            "date": "Apr 16, 2026",
            "service": "Amazon Bedrock",
            "domain": "ai-ml",
            "ftype": "new-feature",
            "ftype_color": (BLUE_L, BLUE_LT),
            "title": "Amazon Bedrock Knowledge Bases now supports semantic reranking",
            "summary": "Semantic reranking improves retrieval accuracy in RAG workflows using a cross-encoder model to rescore chunks. Reduces hallucinations significantly.",
            "kp": ["Reduces RAG hallucinations by rescoring retrieved chunks",
                   "Supports Amazon Rerank 1.0 and Cohere Rerank 3.5",
                   "Single API parameter to enable"],
        },
        {
            "date": "Apr 15, 2026",
            "service": "Amazon EC2",
            "domain": "compute",
            "ftype": "general-availability",
            "ftype_color": (EMERALD_L, EMERALD_D),
            "title": "Amazon EC2 C8g instances (Graviton4) now generally available",
            "summary": "Up to 40% better price/performance vs C7g for compute-intensive HPC, batch, and web workloads. Available c8g.medium → c8g.48xlarge.",
            "kp": ["40% better price performance vs C7g",
                   "30% higher compute + 75% more L3 cache",
                   "Up to 192 vCPUs in c8g.48xlarge"],
        },
        {
            "date": "Apr 14, 2026",
            "service": "Amazon Aurora",
            "domain": "databases",
            "ftype": "enhancement",
            "ftype_color": (GREEN_L, GREEN_D),
            "title": "Aurora Limitless Database adds MySQL 8.0 support",
            "summary": "Extends horizontal scaling to MySQL 8.0 workloads — beyond 100K writes/sec and 100 TB without sharding application logic.",
            "kp": ["Scales MySQL beyond 100K writes/sec",
                   "No application sharding required",
                   "Zero-ETL compatible with Redshift"],
        },
        {
            "date": "Apr 13, 2026",
            "service": "AWS Lambda",
            "domain": "serverless",
            "ftype": "enhancement",
            "ftype_color": (GREEN_L, GREEN_D),
            "title": "AWS Lambda response streaming now supports binary content types",
            "summary": "Binary streaming adds images, PDFs, and audio files alongside text/JSON for Function URLs and API Gateway HTTP API. Max 20 MB.",
            "kp": ["Supports image/*, PDF, audio/* streaming",
                   "No code changes beyond content-type header",
                   "Works with Function URLs and HTTP API"],
        },
        {
            "date": "Apr 12, 2026",
            "service": "Amazon DynamoDB",
            "domain": "databases",
            "ftype": "price-change",
            "ftype_color": (PURPLE_L, PURPLE_D),
            "title": "Amazon DynamoDB reduces on-demand pricing by 20% in all regions",
            "summary": "WRUs now $1.00/million and RRUs $0.20/million in us-east-1. Third price reduction in four years. Applies automatically — no config needed.",
            "kp": ["20% cut: WRUs now $1.00/million",
                   "20% cut: RRUs now $0.20/million",
                   "Automatic — no table changes needed"],
        },
        {
            "date": "Apr 10, 2026",
            "service": "Amazon SageMaker",
            "domain": "ai-ml",
            "ftype": "deprecation",
            "ftype_color": (RED_L, RED_D),
            "title": "SageMaker Studio Classic reaches end-of-support Sep 1, 2026",
            "summary": "Classic domains auto-migrate to new SageMaker Studio after Sep 1 2026. Migrate now using the automated migration tool to avoid disruption.",
            "kp": ["End-of-support: September 1, 2026",
                   "Auto-migration after deadline",
                   "Migration guide at docs.aws.amazon.com"],
        },
    ]

    CARD_W = (W - 48 - 16) // 3
    CARD_H = 224
    GAP    = 8
    START_Y = 184

    for i, feat in enumerate(FEATURES):
        col = i % 3
        row = i // 3
        cx = 24 + col * (CARD_W + GAP)
        cy = START_Y + row * (CARD_H + GAP)

        card(draw, cx, cy, CARD_W, CARD_H)

        # badges row
        bx = cx + 10
        by = cy + 10
        f_badge = load_font(10)
        for txt, bg, fg in [
            (feat["date"], SLATE_L, TEXT_SEC),
            (feat["service"], ORANGE_L, ORANGE_LT),
            (feat["domain"], SLATE_L, SLATE_D),
            (feat["ftype"].replace("-", " "), feat["ftype_color"][0], feat["ftype_color"][1]),
        ]:
            tw = int(draw.textlength(txt, font=f_badge)) + 14
            pill(draw, (bx, by, bx+tw, by+16), txt, bg, fg, f_badge)
            bx += tw + 4

        # title
        f_title = load_font(13, bold=True)
        wrapped = textwrap.wrap(feat["title"], width=40)[:2]
        ty = cy + 32
        for line in wrapped:
            draw.text((cx+10, ty), line, fill=TEXT_PRI, font=f_title)
            ty += 17

        # summary
        f_sum = load_font(11)
        wrapped_s = textwrap.wrap(feat["summary"], width=52)[:2]
        ty += 4
        for line in wrapped_s:
            draw.text((cx+10, ty), line, fill=TEXT_SEC, font=f_sum)
            ty += 14

        # key points
        ty += 4
        f_kp = load_font(10)
        for kp in feat["kp"][:2]:
            draw.text((cx+10, ty), "•  " + kp[:52], fill=TEXT_SEC, font=f_kp)
            ty += 13

        # buttons
        btn_y = cy + CARD_H - 30
        btn_w = (CARD_W - 24) // 2
        # View Details
        rounded_rect(draw, (cx+8, btn_y, cx+8+btn_w, btn_y+22), 6, BLUE, None)
        f_btn = load_font(11, bold=True)
        lbl = "View Details"
        tw = int(draw.textlength(lbl, font=f_btn))
        draw.text((cx+8 + (btn_w-tw)//2, btn_y+5), lbl, fill=WHITE, font=f_btn)
        # AWS Announcement
        rounded_rect(draw, (cx+8+btn_w+4, btn_y, cx+CARD_W-8, btn_y+22), 6, WHITE, BLUE_L)
        lbl2 = "AWS Announcement →"
        tw2 = int(draw.textlength(lbl2, font=f_kp))
        draw.text((cx+8+btn_w+4 + (btn_w-tw2)//2, btn_y+6), lbl2, fill=BLUE, font=f_kp)

    img.save(f"{OUT}/screen_search.png")
    print("Saved screen_search.png")

# ════════════════════════════════════════════════════════════════════════════
# SCREENSHOT 2 — Feature detail page
# ════════════════════════════════════════════════════════════════════════════
def make_detail_page():
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, img, W, show_filters=False)

    f_back = load_font(13)
    draw.text((24, 82), "← Back to search", fill=BLUE, font=f_back)

    # detail card
    cx, cy, cw, ch = 80, 110, W-160, H-130
    card(draw, cx, cy, cw, ch)

    # badges
    f_badge = load_font(11)
    bx = cx + 20
    by = cy + 16
    for txt, bg, fg in [
        ("April 16, 2026", SLATE_L, TEXT_SEC),
        ("Amazon Bedrock", ORANGE_L, ORANGE_LT),
        ("ai-ml", SLATE_L, SLATE_D),
        ("new feature", BLUE_L, BLUE_LT),
    ]:
        tw = int(draw.textlength(txt, font=f_badge)) + 16
        pill(draw, (bx, by, bx+tw, by+20), txt, bg, fg, f_badge)
        bx += tw + 6

    # title
    f_h1 = load_font(22, bold=True)
    draw.text((cx+20, cy+50), "Amazon Bedrock Knowledge Bases now supports", fill=TEXT_PRI, font=f_h1)
    draw.text((cx+20, cy+76), "semantic reranking for improved RAG accuracy", fill=TEXT_PRI, font=f_h1)

    # Summary section
    f_sec = load_font(11, bold=True)
    f_body = load_font(13)
    draw.text((cx+20, cy+116), "SUMMARY", fill=TEXT_SEC, font=f_sec)
    draw.line([cx+20, cy+132, cx+cw-20, cy+132], fill=BORDER, width=1)

    summary = (
        "Amazon Bedrock Knowledge Bases introduces semantic reranking to improve retrieval accuracy "
        "in RAG workflows. This feature uses a cross-encoder model to rerank retrieved documents based "
        "on relevance to the query, significantly reducing hallucinations. Engineers building RAG "
        "applications can enable reranking with a single API parameter change. Supports both Amazon "
        "Rerank 1.0 and Cohere Rerank 3.5 models. Available in all Bedrock-supported regions."
    )
    ty = cy + 140
    for line in textwrap.wrap(summary, width=100):
        draw.text((cx+20, ty), line, fill=TEXT_PRI, font=f_body)
        ty += 20

    # Key Points section
    ty += 16
    draw.text((cx+20, ty), "KEY POINTS", fill=TEXT_SEC, font=f_sec)
    ty += 18
    draw.line([cx+20, ty, cx+cw-20, ty], fill=BORDER, width=1)
    ty += 12

    key_points = [
        "Semantic reranking reduces RAG hallucinations by rescoring retrieved chunks against the query",
        "Supports Amazon Rerank 1.0 and Cohere Rerank 3.5 models with identical API interface",
        "Enabled via RetrievalConfiguration.VectorSearchConfiguration.RerankingConfiguration",
        "No additional infrastructure required — runs as a managed Bedrock service layer",
        "Available in all regions where Amazon Bedrock Knowledge Bases is supported",
    ]
    f_kp = load_font(13)
    for kp in key_points:
        # blue dot
        draw.ellipse([cx+20, ty+5, cx+28, ty+13], fill=BLUE)
        draw.text((cx+36, ty), kp, fill=TEXT_PRI, font=f_kp)
        ty += 26

    # Footer
    draw.line([cx+20, cy+ch-48, cx+cw-20, cy+ch-48], fill=BORDER, width=1)
    f_small = load_font(11)
    draw.text((cx+20, cy+ch-34), "Summarized: April 16, 2026  •  AI summary by Claude Haiku via Amazon Bedrock",
              fill=TEXT_MUT, font=f_small)

    # CTA button
    btn_x = cx+cw-220
    btn_y = cy+ch-44
    rounded_rect(draw, (btn_x, btn_y, btn_x+196, btn_y+30), 8, ORANGE)
    f_btn = load_font(13, bold=True)
    lbl = "View AWS Announcement →"
    tw = int(draw.textlength(lbl, font=f_btn))
    draw.text((btn_x + (196-tw)//2, btn_y+8), lbl, fill=WHITE, font=f_btn)

    img.save(f"{OUT}/screen_detail.png")
    print("Saved screen_detail.png")

# ════════════════════════════════════════════════════════════════════════════
# SCREENSHOT 3 — Filtered / search results
# ════════════════════════════════════════════════════════════════════════════
def make_filtered_page():
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, img, W, search_val="bedrock", show_filters=True)
    draw_filter_row(draw, 128, active_service="amazon-bedrock", active_type="new-feature")

    f_small = load_font(11)
    draw.text((24, 166), 'Showing 2 of 2 features matching "bedrock"', fill=TEXT_SEC, font=f_small)

    AI_FEATURES = [
        {
            "date": "Apr 16, 2026",
            "service": "Amazon Bedrock",
            "domain": "ai-ml",
            "ftype": "new-feature",
            "ftype_color": (BLUE_L, BLUE_LT),
            "title": "Bedrock Knowledge Bases now supports semantic reranking for improved RAG accuracy",
            "summary": "Uses cross-encoder to rerank retrieved documents, significantly reducing hallucinations in RAG pipelines. Single API parameter change.",
            "kp": ["Supports Amazon Rerank 1.0 + Cohere Rerank 3.5",
                   "Reduces RAG hallucinations measurably",
                   "No infrastructure changes needed"],
        },
        {
            "date": "Apr 7, 2026",
            "service": "Amazon Bedrock",
            "domain": "ai-ml",
            "ftype": "preview",
            "ftype_color": (YELLOW_L, YELLOW_D),
            "title": "Amazon Bedrock Agents launches code interpretation capability in preview",
            "summary": "Agents can write and execute Python 3.11 in a sandboxed container for data analysis, math, and chart generation. Pandas, numpy, matplotlib included.",
            "kp": ["30-second execution timeout per code block",
                   "Session-ephemeral sandboxed Python runtime",
                   "Returns charts as base64 images"],
        },
    ]

    CARD_W = (W - 48 - 8) // 3
    CARD_H = 230

    for i, feat in enumerate(AI_FEATURES):
        col = i % 3
        cx = 24 + col * (CARD_W + 8)
        cy = 184

        card(draw, cx, cy, CARD_W, CARD_H)

        bx, by = cx+10, cy+10
        f_badge = load_font(10)
        for txt, bg, fg in [
            (feat["date"], SLATE_L, TEXT_SEC),
            (feat["service"], ORANGE_L, ORANGE_LT),
            (feat["domain"], SLATE_L, SLATE_D),
            (feat["ftype"].replace("-", " "), feat["ftype_color"][0], feat["ftype_color"][1]),
        ]:
            tw = int(draw.textlength(txt, font=f_badge)) + 14
            pill(draw, (bx, by, bx+tw, by+16), txt, bg, fg, f_badge)
            bx += tw + 4

        f_title = load_font(13, bold=True)
        wrapped = textwrap.wrap(feat["title"], width=40)[:2]
        ty = cy + 32
        for line in wrapped:
            draw.text((cx+10, ty), line, fill=TEXT_PRI, font=f_title)
            ty += 17

        f_sum = load_font(11)
        for line in textwrap.wrap(feat["summary"], width=52)[:2]:
            draw.text((cx+10, ty+4), line, fill=TEXT_SEC, font=f_sum)
            ty += 14

        f_kp = load_font(10)
        ty += 8
        for kp in feat["kp"][:3]:
            draw.text((cx+10, ty), "•  " + kp[:52], fill=TEXT_SEC, font=f_kp)
            ty += 13

        btn_y = cy + CARD_H - 30
        btn_w = (CARD_W - 24) // 2
        rounded_rect(draw, (cx+8, btn_y, cx+8+btn_w, btn_y+22), 6, BLUE)
        f_btn = load_font(11, bold=True)
        lbl = "View Details"
        tw = int(draw.textlength(lbl, font=f_btn))
        draw.text((cx+8+(btn_w-tw)//2, btn_y+5), lbl, fill=WHITE, font=f_btn)
        rounded_rect(draw, (cx+8+btn_w+4, btn_y, cx+CARD_W-8, btn_y+22), 6, WHITE, BLUE_L)
        lbl2 = "AWS Announcement →"
        f_kp2 = load_font(10)
        tw2 = int(draw.textlength(lbl2, font=f_kp2))
        draw.text((cx+8+btn_w+4+(btn_w-tw2)//2, btn_y+6), lbl2, fill=BLUE, font=f_kp2)

    # empty state hint for 3rd column
    ex = 24 + 2*(CARD_W+8)
    draw.rectangle([ex, 184, ex+CARD_W, 184+CARD_H], fill=BG)

    img.save(f"{OUT}/screen_filtered.png")
    print("Saved screen_filtered.png")

# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    make_search_page()
    make_detail_page()
    make_filtered_page()
    print("All screenshots saved to", OUT)

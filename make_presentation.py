"""
Build the AWS Features Tracker innovation demo PowerPoint presentation.
Fully valid for PowerPoint — uses Emu(12192000) x Emu(6858000) widescreen.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ASSETS = "/workshop/aws-new-features/slides_assets"
OUT    = "/workshop/aws-new-features/AWS_Features_Tracker_Innovation_Demo.pptx"

# ── brand colours ─────────────────────────────────────────────────────────────
AWS_ORANGE  = RGBColor(0xFF, 0x99, 0x00)
AWS_DARK    = RGBColor(0x23, 0x2F, 0x3E)
AWS_BLUE    = RGBColor(0x14, 0x6E, 0xB4)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xF8, 0xFA, 0xFC)
MID_GRAY    = RGBColor(0x94, 0xA3, 0xB8)
DARK_GRAY   = RGBColor(0x1E, 0x29, 0x3B)
ACCENT_TEAL = RGBColor(0x0F, 0xB5, 0xD4)
GREEN       = RGBColor(0x16, 0xA3, 0x4A)
ORANGE_L    = RGBColor(0xFF, 0xF7, 0xED)
BLUE_L      = RGBColor(0xDB, 0xEA, 0xFE)
GREEN_L     = RGBColor(0xDC, 0xFC, 0xE7)
YELLOW_L    = RGBColor(0xFE, 0xF9, 0xC3)
RED_L       = RGBColor(0xFE, 0xE2, 0xE2)
PURPLE      = RGBColor(0x8B, 0x5C, 0xF6)
PURPLE_L    = RGBColor(0xF3, 0xE8, 0xFF)
TEAL_L      = RGBColor(0xCF, 0xFA, 0xFE)
SLATE_L     = RGBColor(0xF1, 0xF5, 0xF9)
BORDER      = RGBColor(0xE2, 0xE8, 0xF0)
RED         = RGBColor(0xEF, 0x44, 0x44)

# ── slide dimensions — standard widescreen 16:9 ───────────────────────────────
SW = Emu(12192000)   # exactly 13.333... inches
SH = Emu(6858000)    # exactly 7.5 inches

prs = Presentation()
prs.slide_width  = SW
prs.slide_height = SH

BLANK = prs.slide_layouts[6]

# ── helpers ───────────────────────────────────────────────────────────────────

def I(v): return Emu(int(v * 914400))      # inches → EMU
def P(v): return Pt(v)


def rect(slide, l, t, w, h, fill=None, line=None, line_pt=0.75):
    """Add a rectangle. fill/line are RGBColor or None."""
    sh = slide.shapes.add_shape(1, int(l), int(t), int(w), int(h))
    if fill:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = line
        sh.line.width = P(line_pt)
    else:
        sh.line.fill.background()
    return sh


def txb(slide, l, t, w, h, text, size, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, italic=False):
    """Add a plain single-paragraph textbox."""
    tb = slide.shapes.add_textbox(int(l), int(t), int(w), int(h))
    tf = tb.text_frame
    tf.word_wrap = True
    p  = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text  = text
    run.font.size   = P(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tb


def bullet(slide, l, t, w, h, text, size=11, dot_color=AWS_ORANGE, text_color=DARK_GRAY):
    """Dot + text bullet row."""
    dot_size = I(0.1)
    rect(slide, l, t + I(size * 0.018), dot_size, dot_size, fill=dot_color)
    txb(slide, l + I(0.18), t, w - I(0.18), h, text, size, color=text_color)


def header_bar(slide, bg=AWS_DARK, height=I(1.0)):
    rect(slide, 0, 0, SW, height, fill=bg)


def bottom_accent(slide, color=AWS_ORANGE, height=I(0.1)):
    rect(slide, 0, SH - height, SW, height, fill=color)


def section_tag(slide, text, l=I(0.55), t=I(0.22)):
    txb(slide, l, t, I(6), I(0.28), text, 9, bold=True, color=AWS_ORANGE)


def card(slide, l, t, w, h, fill=WHITE, border=BORDER):
    # shadow
    rect(slide, l + I(0.03), t + I(0.03), w, h, fill=RGBColor(0xCB,0xD5,0xE1))
    rect(slide, l, t, w, h, fill=fill, line=border, line_pt=0.75)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title Hero
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=AWS_DARK)
rect(sl, 0, 0, I(0.18), SH, fill=AWS_ORANGE)             # left accent strip
# subtle vertical grid lines
for i in range(1, 9):
    rect(sl, I(i * 13.333/8), 0, I(0.02), SH, fill=RGBColor(0x2D,0x3F,0x55))

# AWS badge
rect(sl, I(0.65), I(1.05), I(0.72), I(0.48), fill=AWS_ORANGE)
txb(sl, I(0.67), I(1.08), I(0.68), I(0.42), "aws", 22, bold=True,
    color=AWS_DARK, align=PP_ALIGN.CENTER)

txb(sl, I(0.65), I(1.7), I(10), I(0.3),
    "INNOVATION DEMO  ·  AWS ADMINISTRATION TEAM",
    10, bold=True, color=AWS_ORANGE)

txb(sl, I(0.65), I(2.3), I(11), I(1.0),
    "AWS Features Tracker", 52, bold=True, color=WHITE)

txb(sl, I(0.65), I(3.45), I(10), I(0.5),
    "AI-Powered Discovery, Summarization & Search of AWS Announcements",
    21, italic=True, color=RGBColor(0xCB,0xD5,0xE1))

for i, lbl in enumerate(["Real-time RSS ingestion",
                          "Claude Haiku AI summaries",
                          "Searchable web app"]):
    px = I(0.65 + i * 3.3)
    rect(sl, px, I(4.25), I(3.05), I(0.42), fill=AWS_BLUE)
    txb(sl, px, I(4.27), I(3.05), I(0.38), lbl, 12, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)

rect(sl, 0, SH - I(0.48), SW, I(0.48), fill=RGBColor(0x14,0x21,0x30))
txb(sl, 0, SH - I(0.44), SW, I(0.4),
    "Presented by the Cloud Administration Team  ·  April 2026",
    10, color=MID_GRAY, align=PP_ALIGN.CENTER)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — The Problem
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=LIGHT_GRAY)
header_bar(sl, height=I(1.05))
bottom_accent(sl)

txb(sl, I(0.55), I(0.18), I(10.5), I(0.56),
    "The Challenge: Staying Ahead of AWS Innovation", 28, bold=True, color=WHITE)
txb(sl, I(0.55), I(0.74), I(10.5), I(0.28),
    "AWS releases 2,000+ new features per year — how do admins keep up?",
    13, italic=True, color=AWS_ORANGE)

# stat boxes
for i, (num, lbl) in enumerate([("2,000+", "new AWS\nfeatures/year"),
                                  ("~5 min",  "avg reading\ntime each"),
                                  ("166 hrs", "total annual\nreading time"),
                                  ("$0",      "billable value\nof that time")]):
    bx = I(0.55 + i * 3.12)
    card(sl, bx, I(1.18), I(2.9), I(1.52))
    txb(sl, bx, I(1.28), I(2.9), I(0.72), num, 36, bold=True,
        color=AWS_ORANGE, align=PP_ALIGN.CENTER)
    txb(sl, bx, I(2.02), I(2.9), I(0.58), lbl, 12,
        color=DARK_GRAY, align=PP_ALIGN.CENTER)

rect(sl, I(0.55), I(2.88), SW - I(1.1), I(0.01), fill=BORDER)
txb(sl, I(0.55), I(2.97), I(5.5), I(0.32), "Pain Points", 15,
    bold=True, color=DARK_GRAY)

for i, pain in enumerate([
    "Manual RSS monitoring — easy to miss critical announcements across dozens of categories",
    "No searchable history: 'Did AWS update Lambda concurrency limits this quarter?'",
    "Raw HTML descriptions bury critical details in marketing language",
    "No service-level filtering — irrelevant noise drowns out what matters to your team",
    "Knowledge is siloed — each admin tracks different services independently",
]):
    bullet(sl, I(0.55), I(3.42 + i * 0.5), I(8.2), I(0.46), pain, 12,
           dot_color=RED, text_color=DARK_GRAY)

# opportunity box
card(sl, I(9.15), I(2.97), I(3.62), I(3.42))
txb(sl, I(9.28), I(3.08), I(3.36), I(0.34), "The Opportunity",
    14, bold=True, color=AWS_ORANGE)
txb(sl, I(9.28), I(3.48), I(3.36), I(2.75),
    "Automate the discovery, summarization, and cataloguing of every AWS "
    "announcement — so admins spend minutes on insights instead of hours on reading.",
    12, color=DARK_GRAY)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Architecture
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=AWS_DARK)
bottom_accent(sl)
section_tag(sl, "SOLUTION ARCHITECTURE")
txb(sl, I(0.55), I(0.48), I(10), I(0.52),
    "AWS Features Tracker — How It Works", 27, bold=True, color=WHITE)

FLOW_Y = I(1.32)
BOX_W  = I(2.18)
BOX_H  = I(1.1)
GAP    = I(0.28)

ingestion = [
    ("EventBridge\nScheduler", "Every 6 hours",          AWS_ORANGE),
    ("Fetcher\nLambda",        "Parses RSS · Dedupes",    AWS_BLUE),
    ("SQS Queue",              "Reliable delivery\n3× retry + DLQ", ACCENT_TEAL),
    ("Summarizer\nLambda",     "Claude Haiku\nvia Bedrock", GREEN),
    ("DynamoDB\n+ S3",         "Persistent store\nJSON archive", PURPLE),
]
for i, (name, desc, color) in enumerate(ingestion):
    bx = I(0.38 + i * (2.18 + 0.28))
    rect(sl, bx, FLOW_Y, BOX_W, BOX_H, fill=color)
    txb(sl, bx, FLOW_Y + I(0.1), BOX_W, I(0.44), name, 13,
        bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txb(sl, bx, FLOW_Y + I(0.55), BOX_W, I(0.48), desc, 10,
        color=RGBColor(0xE2,0xE8,0xF0), align=PP_ALIGN.CENTER)
    if i < len(ingestion) - 1:
        ax = bx + BOX_W + I(0.06)
        txb(sl, ax, FLOW_Y + I(0.38), I(0.18), I(0.3), "→", 18,
            bold=True, color=AWS_ORANGE, align=PP_ALIGN.CENTER)

txb(sl, I(0.38), I(2.65), I(12), I(0.28),
    "▼  API & Frontend Layer", 10, bold=True, color=MID_GRAY)

API_Y = I(3.05)
api = [
    ("API Gateway\nHTTP API",  "5 REST routes\nRead-only, no auth",  AWS_BLUE),
    ("API Lambda",             "/features /services\n/types /health", ACCENT_TEAL),
    ("CloudFront CDN",         "Edge caching\n/api/* passthrough",    AWS_ORANGE),
    ("React SPA (S3)",         "TypeScript + Vite\nTailwind CSS",     PURPLE),
]
for i, (name, desc, color) in enumerate(api):
    bx = I(0.38 + i * (2.18 + 0.28))
    rect(sl, bx, API_Y, BOX_W, BOX_H, fill=color)
    txb(sl, bx, API_Y + I(0.1), BOX_W, I(0.44), name, 13,
        bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txb(sl, bx, API_Y + I(0.55), BOX_W, I(0.48), desc, 10,
        color=RGBColor(0xE2,0xE8,0xF0), align=PP_ALIGN.CENTER)
    if i < len(api) - 1:
        ax = bx + BOX_W + I(0.06)
        txb(sl, ax, API_Y + I(0.38), I(0.18), I(0.3), "→", 18,
            bold=True, color=AWS_ORANGE, align=PP_ALIGN.CENTER)

txb(sl, I(0.38), I(4.38), I(12), I(0.26), "Tech Stack", 10, bold=True, color=MID_GRAY)
for i, t in enumerate(["Python 3.12 · Lambda arm64",
                        "Amazon Bedrock · Claude Haiku",
                        "DynamoDB on-demand · S3",
                        "React 18 + TypeScript + Vite",
                        "AWS SAM (Infrastructure as Code)",
                        "~$0.31 / month"]):
    bx = I(0.38 + i * 2.14)
    rect(sl, bx, I(4.7), I(2.04), I(0.4), fill=RGBColor(0x1E,0x3A,0x52))
    txb(sl, bx, I(4.72), I(2.04), I(0.36), t, 9,
        color=RGBColor(0xCB,0xD5,0xE1), align=PP_ALIGN.CENTER)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Key Features
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=LIGHT_GRAY)
header_bar(sl, height=I(1.05))
bottom_accent(sl)

txb(sl, I(0.55), I(0.18), I(11), I(0.56),
    "Built for AWS Admins Who Research & Analyze", 27, bold=True, color=WHITE)
txb(sl, I(0.55), I(0.74), I(11), I(0.28),
    "Every feature is designed around the admin workflow — discover, evaluate, act.",
    13, italic=True, color=AWS_ORANGE)

features = [
    (AWS_ORANGE, "Automated Discovery",
     "Fetches aws.amazon.com/new/feed/ every 6 hours via EventBridge Scheduler. Zero manual effort.",
     ["No manual RSS monitoring", "Deduplication on guid", "SSM timestamp logging"]),
    (AWS_BLUE, "AI-Generated Summaries",
     "Claude Haiku (Bedrock) produces 3-5 sentence engineer-focused summaries with structured output.",
     ["Feature type auto-classified (8 categories)", "3 key points extracted per announcement"]),
    (GREEN, "Powerful Search & Filters",
     "Full-text search across title, summary and service. Filter by service, type, date. URL-based state.",
     ["Search 'lambda timeout' — instant results", "Date range: what changed in Q1 2026?"]),
    (ACCENT_TEAL, "Feature Type Classification",
     "Bedrock classifies every item into one of 8 types: new-feature, GA, preview, deprecation, and more.",
     ["Color-coded badges for instant scanning", "Filter dashboard to only what matters today"]),
    (PURPLE, "Shareable URLs",
     "All filters live in the URL. Copy the link and share a specific filtered view with any team member.",
     ["Bookmark filtered views", "Back button preserves search context"]),
    (RED, "Reliability Built-In",
     "SQS DLQ retries failures 3×. CloudWatch alarms on errors and DLQ depth. IAM least-privilege.",
     ["DLQ 7-day retention — no announcement lost", "CloudWatch alarms on errors and DLQ"]),
]

COL_W = I(4.05)
ROW_H = I(1.82)
for i, (color, title, body, pts) in enumerate(features):
    col = i % 3
    row = i // 3
    bx = I(0.42 + col * (4.05 + 0.12))
    by = I(1.28 + row * (1.82 + 0.1))
    card(sl, bx, by, COL_W, ROW_H)
    rect(sl, bx, by, I(0.08), ROW_H, fill=color)  # left colour bar
    txb(sl, bx + I(0.15), by + I(0.1), COL_W - I(0.22), I(0.3),
        title, 13, bold=True, color=DARK_GRAY)
    txb(sl, bx + I(0.15), by + I(0.44), COL_W - I(0.22), I(0.52),
        body, 9.5, color=RGBColor(0x64,0x74,0x8B))
    for j, pt in enumerate(pts[:2]):
        bullet(sl, bx + I(0.15), by + I(1.0 + j * 0.32), COL_W - I(0.22), I(0.28),
               pt, 9, dot_color=color, text_color=DARK_GRAY)


# ── Shared helper for screenshot slides (5, 6, 7) ────────────────────────────
def screenshot_slide(title, section, img_path, points):
    """
    Two-column layout:
      Left  ~8.4" : screenshot
      Right ~3.6" : dark panel with 6 bullet callouts
    No overlays on the screenshot.
    """
    sl = prs.slides.add_slide(BLANK)
    rect(sl, 0, 0, SW, SH, fill=AWS_DARK)
    bottom_accent(sl)
    section_tag(sl, section)
    txb(sl, I(0.35), I(0.3), I(9.5), I(0.52), title, 20, bold=True, color=WHITE)

    # screenshot — left column, full height below title
    IMG_L = I(0.35)
    IMG_T = I(0.92)
    IMG_W = I(8.38)
    IMG_H = I(6.46)
    sl.shapes.add_picture(img_path, int(IMG_L), int(IMG_T), int(IMG_W), int(IMG_H))

    # right panel
    PNL_L = I(8.85)
    PNL_T = I(0.92)
    PNL_W = I(3.12)
    PNL_H = I(6.46)
    rect(sl, PNL_L, PNL_T, PNL_W, PNL_H, fill=RGBColor(0x0D, 0x1A, 0x2E))
    rect(sl, PNL_L, PNL_T, I(0.06), PNL_H, fill=AWS_ORANGE)  # left accent strip

    txb(sl, PNL_L + I(0.18), PNL_T + I(0.18), PNL_W - I(0.28), I(0.28),
        "KEY HIGHLIGHTS", 8, bold=True, color=AWS_ORANGE)

    for j, pt in enumerate(points):
        py = PNL_T + I(0.58 + j * 0.94)
        rect(sl, PNL_L + I(0.18), py, PNL_W - I(0.28), I(0.82),
             fill=RGBColor(0x1A, 0x2A, 0x3E))
        rect(sl, PNL_L + I(0.18), py, I(0.04), I(0.82),
             fill=AWS_ORANGE)
        txb(sl, PNL_L + I(0.28), py + I(0.1), PNL_W - I(0.42), I(0.65),
            pt, 10, color=RGBColor(0xE2, 0xE8, 0xF0))

    return sl


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Screenshot: Main Search Page
# ═════════════════════════════════════════════════════════════════════════════
screenshot_slide(
    title="Main Dashboard — Browse & Search All AWS Announcements",
    section="LIVE DEMO — SEARCH & DISCOVERY",
    img_path=f"{ASSETS}/screen_search.png",
    points=[
        "Live search bar\nwith 300ms debounce",
        "Filters: service,\ntype, date, sort order",
        "Result count\nalways visible",
        "Color-coded\nfeature type badges",
        "AI key points\nexpandable per card",
        "Direct link to\nAWS announcement",
    ],
)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Screenshot: Feature Detail Page
# ═════════════════════════════════════════════════════════════════════════════
screenshot_slide(
    title="Feature Detail Page — Deep-Dive Into Any Announcement",
    section="LIVE DEMO — FEATURE DETAIL",
    img_path=f"{ASSETS}/screen_detail.png",
    points=[
        "Badges: date,\nservice, domain, type",
        "3–5 sentence AI\nsummary, engineer-focused",
        "Structured key\npoints for evaluation",
        "One-click link to\nAWS announcement",
        "Back button\npreserves search state",
        "Summarized-at\ntimestamp for audit",
    ],
)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Screenshot: Filtered Results
# ═════════════════════════════════════════════════════════════════════════════
screenshot_slide(
    title="Filtered: 'bedrock'  ·  service: amazon-bedrock  ·  type: new-feature",
    section="LIVE DEMO — FILTER & SEARCH",
    img_path=f"{ASSETS}/screen_filtered.png",
    points=[
        "Keyword search\nmatches title & summary",
        "Active filter pills\nshown in header",
        "Real-time\nresult count",
        "URL captures all\nfilters — shareable",
        "Infinite scroll\nauto-loads next page",
        "Works across\nall 8 feature types",
    ],
)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Admin Use Cases
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=LIGHT_GRAY)
header_bar(sl, height=I(1.05))
bottom_accent(sl)

txb(sl, I(0.55), I(0.18), I(11), I(0.56),
    "Real-World Use Cases for AWS Admins", 27, bold=True, color=WHITE)
txb(sl, I(0.55), I(0.74), I(11), I(0.28),
    "From reactive monitoring to proactive innovation — the tracker enables both.",
    13, italic=True, color=AWS_ORANGE)

use_cases = [
    (AWS_ORANGE, "Weekly Innovation Review",
     "Every Monday: filter last 7 days, sort newest first. In 15 minutes the team "
     "identifies 3-5 features worth piloting — replacing 2 hours of manual reading.",
     "from_date=7d ago · sort=newest"),
    (AWS_BLUE, "Pre-Migration Research",
     "Before adopting Graviton4, search 'graviton4' to see all GA announcements, "
     "enhancements, and price changes in one scrollable timeline.",
     "q=graviton4 · type=general-availability"),
    (GREEN, "Deprecation Tracking",
     "Filter type=deprecation to build a living list of EOL services. Share the "
     "URL with the architecture team as a standing reference bookmark.",
     "type=deprecation · sort=oldest"),
    (ACCENT_TEAL, "Cost Optimization",
     "Filter type=price-change to catch every DynamoDB, Lambda, and S3 reduction. "
     "Calculate savings and present the business case for migration.",
     "type=price-change"),
    (PURPLE, "New Service Evaluation",
     "Leadership asks 'should we adopt VPC Lattice?' — search the tracker for a "
     "complete feature history to assess service maturity and trajectory.",
     "q=vpc lattice · date=2025-2026"),
    (RED, "Region Expansion Watch",
     "Filter type=region-expansion for services you use. Know the moment a "
     "needed service reaches your target region before checking the console.",
     "type=region-expansion · service=amazon-eks"),
]

COL_W = I(4.05)
ROW_H = I(2.02)
for i, (color, title, body, query) in enumerate(use_cases):
    col = i % 3
    row = i // 3
    bx = I(0.42 + col * (4.05 + 0.12))
    by = I(1.28 + row * (2.02 + 0.06))
    card(sl, bx, by, COL_W, ROW_H)
    rect(sl, bx, by, COL_W, I(0.07), fill=color)
    txb(sl, bx + I(0.12), by + I(0.13), COL_W - I(0.2), I(0.3),
        title, 13, bold=True, color=DARK_GRAY)
    txb(sl, bx + I(0.12), by + I(0.46), COL_W - I(0.2), I(0.88),
        body, 9.5, color=RGBColor(0x64,0x74,0x8B))
    rect(sl, bx + I(0.12), by + ROW_H - I(0.38), COL_W - I(0.24), I(0.28),
         fill=SLATE_L)
    txb(sl, bx + I(0.18), by + ROW_H - I(0.36), COL_W - I(0.3), I(0.26),
        query, 8.5, italic=True, color=color)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — AI Summary Deep-Dive
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=AWS_DARK)
bottom_accent(sl)
section_tag(sl, "AI INTELLIGENCE LAYER")
txb(sl, I(0.55), I(0.42), I(10.5), I(0.52),
    "How Claude Haiku Transforms Raw AWS Announcements",
    25, bold=True, color=WHITE)

# left box — raw RSS
rect(sl, I(0.45), I(1.08), I(5.5), I(5.88),
     fill=RGBColor(0x1A,0x2A,0x3A), line=RGBColor(0x2D,0x3F,0x55))
txb(sl, I(0.6), I(1.14), I(5.2), I(0.28), "RAW RSS INPUT", 9,
    bold=True, color=MID_GRAY)
txb(sl, I(0.6), I(1.48), I(5.2), I(5.3),
    "<title>Amazon Bedrock Knowledge Bases now supports\n"
    "semantic reranking for improved RAG accuracy</title>\n\n"
    "<description>\n"
    "  <p>Amazon Bedrock Knowledge Bases now supports\n"
    "  semantic reranking, a technique that improves\n"
    "  retrieved results for RAG applications...</p>\n"
    "  <p>A cross-encoder model reranks initially retrieved\n"
    "  chunks based on query relevance, reducing\n"
    "  hallucinations and improving response quality...</p>\n"
    "</description>\n\n"
    "<category>general:products/amazon-bedrock</category>\n"
    "<category>marketing:marchitecture/ai-ml</category>",
    9, color=RGBColor(0x7D,0xD3,0xFC))

# arrow
txb(sl, I(6.12), I(3.55), I(0.9), I(0.5), "→", 36,
    bold=True, color=AWS_ORANGE, align=PP_ALIGN.CENTER)
txb(sl, I(5.98), I(4.12), I(1.18), I(0.36), "Claude\nHaiku", 9,
    color=AWS_ORANGE, align=PP_ALIGN.CENTER)

# right box — enriched output
rect(sl, I(7.22), I(1.08), I(5.5), I(5.88),
     fill=RGBColor(0x0D,0x2A,0x1A), line=GREEN)
txb(sl, I(7.38), I(1.14), I(5.2), I(0.28), "AI-ENRICHED OUTPUT", 9,
    bold=True, color=MID_GRAY)

ty = I(1.48)
for label, val, col in [
    ("feature_type:", "new-feature", AWS_ORANGE),
    ("summary:", (
        "Amazon Bedrock Knowledge Bases introduces semantic\n"
        "reranking to improve retrieval accuracy in RAG\n"
        "workflows. A cross-encoder model rescores retrieved\n"
        "chunks by relevance, significantly reducing\n"
        "hallucinations. Enable with a single API parameter.\n"
        "Supports Amazon Rerank 1.0 and Cohere Rerank 3.5."
    ), RGBColor(0xBB,0xF7,0xD0)),
    ("key_points:", (
        "• Reduces hallucinations by rescoring chunks\n"
        "• Supports Rerank 1.0 + Cohere Rerank 3.5\n"
        "• Single RetrievalConfiguration API param\n"
        "• No infra changes required"
    ), RGBColor(0x86,0xEF,0xAC)),
]:
    txb(sl, I(7.38), ty, I(5.2), I(0.26), label, 9,
        bold=True, color=MID_GRAY)
    ty += I(0.28)
    txb(sl, I(7.38), ty, I(5.2), I(0.95), val, 10, color=col)
    ty += I(0.98)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Cost & Security
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=LIGHT_GRAY)
header_bar(sl, height=I(1.05))
bottom_accent(sl)

txb(sl, I(0.55), I(0.18), I(11), I(0.56),
    "Cost-Efficient, Secure, and Production-Ready",
    27, bold=True, color=WHITE)
txb(sl, I(0.55), I(0.74), I(11), I(0.28),
    "Minimal cost, FedRAMP-aligned services, least-privilege IAM, full observability.",
    13, italic=True, color=AWS_ORANGE)

# cost table
card(sl, I(0.45), I(1.18), I(5.82), I(4.88))
txb(sl, I(0.6), I(1.28), I(5.5), I(0.3),
    "Monthly Cost Estimate (~500 features/month)", 12, bold=True, color=DARK_GRAY)

rows = [
    ("Service", "Monthly Cost", True),
    ("Lambda (3 functions, arm64)", "~$0.01", False),
    ("DynamoDB on-demand", "~$0.02", False),
    ("S3 (summaries + SPA assets)", "~$0.03", False),
    ("CloudFront (PriceClass_100)", "~$0.10", False),
    ("Bedrock Claude Haiku (500 summaries)", "~$0.15", False),
    ("SQS + EventBridge Scheduler", "$0.00  (free tier)", False),
    ("TOTAL", "~$0.31/month", True),
]
for i, (svc, cost, bold) in enumerate(rows):
    ry = I(1.7 + i * 0.46)
    bg = RGBColor(0xF8,0xFA,0xFC) if (i % 2 == 0 and not bold) else None
    if bold:
        bg = RGBColor(0xFF,0xF7,0xED)
    if bg:
        rect(sl, I(0.45), ry, I(5.82), I(0.46), fill=bg)
    txb(sl, I(0.6), ry + I(0.1), I(3.8), I(0.28), svc, 10,
        bold=bold, color=DARK_GRAY)
    txb(sl, I(4.55), ry + I(0.1), I(1.5), I(0.28), cost, 10,
        bold=bold, color=AWS_ORANGE if bold else GREEN, align=PP_ALIGN.RIGHT)

# security
card(sl, I(6.62), I(1.18), I(6.12), I(2.25))
txb(sl, I(6.78), I(1.28), I(5.8), I(0.3),
    "Security & Compliance", 13, bold=True, color=DARK_GRAY)
for j, item in enumerate([
    "All services FedRAMP Moderate authorized (us-east-1 commercial)",
    "IAM least-privilege — each Lambda has only the permissions it needs",
    "S3 Block Public Access ON — CloudFront OAC, no direct bucket access",
    "No VPC required — all traffic via AWS service endpoints",
    "API Gateway public read-only — no write surface exposed",
]):
    bullet(sl, I(6.78), I(1.68 + j * 0.3), I(5.8), I(0.28),
           item, 9.5, dot_color=GREEN, text_color=DARK_GRAY)

# reliability
card(sl, I(6.62), I(3.55), I(6.12), I(2.52))
txb(sl, I(6.78), I(3.65), I(5.8), I(0.3),
    "Reliability & Observability", 13, bold=True, color=DARK_GRAY)
for j, item in enumerate([
    "SQS DLQ with 7-day retention — no announcement ever lost",
    "Up to 3 automatic Bedrock retries before dead-lettering",
    "CloudWatch Alarm: Summarizer errors > 10/hr",
    "CloudWatch Alarm: DLQ messages > 0",
    "CloudFront + Lambda arm64 — low-latency, globally available",
]):
    bullet(sl, I(6.78), I(4.08 + j * 0.3), I(5.8), I(0.28),
           item, 9.5, dot_color=AWS_BLUE, text_color=DARK_GRAY)


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Roadmap
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=AWS_DARK)
bottom_accent(sl)
section_tag(sl, "WHAT'S NEXT")
txb(sl, I(0.55), I(0.42), I(10), I(0.52),
    "Roadmap — Where We Can Take This", 25, bold=True, color=WHITE)

roadmap = [
    ("Q2 2026", AWS_ORANGE, [
        "SNS / Slack alerts — ping #aws-updates when new features match your watchlist",
        "Per-admin service watchlist — personalized feed based on your AWS footprint",
        "Weekly digest email: top 5 features relevant to your services",
    ]),
    ("Q3 2026", AWS_BLUE, [
        "Impact scoring — Claude estimates cost/effort/risk of adopting each feature",
        "Multi-account tagging — link features to the accounts/OUs they affect",
        "Comments & status: evaluating / piloting / adopted / declined per team",
    ]),
    ("Q4 2026", GREEN, [
        "Cost savings calculator — quantify savings from price-change announcements",
        "Deprecation calendar — auto JIRA tickets for EOL services",
        "Executive dashboard — monthly report of adopted innovations & saved $",
    ]),
]

for i, (quarter, color, items) in enumerate(roadmap):
    bx = I(0.42 + i * 4.28)
    by = I(1.05)
    bw = I(4.05)
    bh = I(5.68)
    rect(sl, bx, by, bw, bh,
         fill=RGBColor(0x1A,0x26,0x35), line=color, line_pt=1.5)
    rect(sl, bx, by, bw, I(0.44), fill=color)
    txb(sl, bx, by + I(0.06), bw, I(0.34), quarter, 16,
        bold=True, color=AWS_DARK, align=PP_ALIGN.CENTER)
    for j, item in enumerate(items):
        iy = by + I(0.58 + j * 1.62)
        rect(sl, bx + I(0.22), iy, I(3.62), I(1.46),
             fill=RGBColor(0x23,0x32,0x44))
        bullet(sl, bx + I(0.34), iy + I(0.12), I(3.38), I(1.2),
               item, 11, dot_color=color,
               text_color=RGBColor(0xCB,0xD5,0xE1))


# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Call to Action
# ═════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, SW, SH, fill=AWS_DARK)
rect(sl, 0, 0, I(0.18), SH, fill=AWS_ORANGE)
for i in range(1, 9):
    rect(sl, I(i * 13.333/8), 0, I(0.02), SH, fill=RGBColor(0x2D,0x3F,0x55))

txb(sl, I(0.65), I(1.05), I(11.5), I(0.4),
    "The tracker is live today.", 23, italic=True, color=MID_GRAY)
txb(sl, I(0.65), I(1.6), I(11.5), I(1.0),
    "Start using it this week.", 50, bold=True, color=WHITE)
txb(sl, I(0.65), I(2.75), I(11), I(0.42),
    "https://d1s77r5nnbdjdt.cloudfront.net",
    20, bold=True, color=AWS_ORANGE)

for i, (color, title, body) in enumerate([
    (AWS_ORANGE, "Try It Now",
     "Open the app, search for any service you manage, and find features you may have missed this quarter."),
    (AWS_BLUE, "Add Your Watchlist",
     "Tell us the top 10 AWS services your team owns — we'll prioritize those filters in the next sprint."),
    (GREEN, "Give Feedback",
     "What integrations, views, or alerts would make this tool indispensable to your daily workflow?"),
]):
    bx = I(0.65 + i * 4.18)
    by = I(3.72)
    rect(sl, bx, by, I(3.9), I(2.48), fill=RGBColor(0x1A,0x26,0x35))
    rect(sl, bx, by, I(3.9), I(0.07), fill=color)
    txb(sl, bx + I(0.18), by + I(0.18), I(3.6), I(0.32), title,
        14, bold=True, color=WHITE)
    txb(sl, bx + I(0.18), by + I(0.58), I(3.6), I(1.7), body,
        10.5, color=RGBColor(0xCB,0xD5,0xE1))

rect(sl, 0, SH - I(0.48), SW, I(0.48), fill=RGBColor(0x14,0x21,0x30))
txb(sl, 0, SH - I(0.44), SW, I(0.4),
    "AWS Features Tracker  ·  Lambda · Bedrock · DynamoDB · CloudFront  ·  ~$0.31/month  ·  April 2026",
    9, color=MID_GRAY, align=PP_ALIGN.CENTER)


# ── Fix sldSz type so PowerPoint accepts the file ─────────────────────────────
for el in prs._element.iter():
    tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
    if tag == 'sldSz':
        el.set('type', 'custom')
        break

prs.save(OUT)
print(f"Saved: {OUT}")
print(f"Slides: {len(prs.slides)}")

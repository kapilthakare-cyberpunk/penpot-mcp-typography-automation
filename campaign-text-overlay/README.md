# CLI Typography Overlay Tool

A parameterised Python script for adding typography overlays to campaign images. Built for repeatable, scriptable, version-controllable text rendering on images.

## Why This Tool?

If you're doing 10+ creatives with consistent typography, this CLI approach gives you:
- **Precise control** — pixel-perfect text placement, sizing, and spacing
- **Repeatable output** — same parameters = identical results every time
- **Scriptable workflow** — integrate into build pipelines or batch processing
- **Version control** — track your typography parameters in git

## Installation

```bash
pip install Pillow fonttools brotli
```

### Font Requirements

This tool uses **Barlow Semi Condensed** fonts. Install them via npm:

```bash
npm install @fontsource/barlow-semi-condensed
```

Then convert the woff2 files to TTF:

```bash
python -c "
from fontTools.ttLib import TTFont
import os

src = 'node_modules/@fontsource/barlow-semi-condensed/files/'
out = 'fonts/'
os.makedirs(out, exist_ok=True)

TTFont(src + 'barlow-semi-condensed-latin-700-normal.woff2').save(out + 'BarlowSemiCondensed-Bold.ttf')
TTFont(src + 'barlow-semi-condensed-latin-600-normal.woff2').save(out + 'BarlowSemiCondensed-SemiBold.ttf')
"
```

## Usage

```bash
python pz_typography.py \
  --input image.png \
  --output output.png \
  --headline "YOUR OLD GEAR" \
  --headline2 "HAS A NEXT CHAPTER." \
  --subhead "STAY TUNED" \
  --font-bold ./fonts/BarlowSemiCondensed-Bold.ttf \
  --font-semibold ./fonts/BarlowSemiCondensed-SemiBold.ttf
```

## CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input`, `-i` | Input image path | Required |
| `--output`, `-o` | Output image path | Required |
| `--headline` | First headline text | - |
| `--headline2` | Second headline text | - |
| `--subhead` | Subhead text | - |
| `--font-bold` | Path to Bold (700) TTF | Required |
| `--font-semibold` | Path to SemiBold (600) TTF | Required |
| `--headline-size` | Headline font size (px or % of width) | 9.8% |
| `--subhead-size` | Subhead font size (px or % of width) | 3.3% |
| `--margin` | Left margin (% of width) | 5% |
| `--top-offset` | Top offset (% of height) | 6% |
| `--line-height` | Line height ratio | 0.92 |
| `--headline-color` | Headline color (hex) | #FFFFFF |
| `--subhead-color` | Subhead color (hex) | #8F98A1 |
| `--shadow-offset` | Drop shadow offset (px) | 3 |
| `--shadow-opacity` | Drop shadow opacity (0-255) | 100 |

## Examples

### Basic Usage

```bash
python pz_typography.py \
  --input hero.png \
  --output hero_with_text.png \
  --headline "YOUR OLD GEAR" \
  --headline2 "HAS A NEXT CHAPTER." \
  --subhead "STAY TUNED" \
  --font-bold ./fonts/BarlowSemiCondensed-Bold.ttf \
  --font-semibold ./fonts/BarlowSemiCondensed-SemiBold.ttf
```

### Custom Sizing

```bash
python pz_typography.py \
  --input hero.png \
  --output hero_custom.png \
  --headline "SALE" \
  --headline2 "UP TO 50% OFF" \
  --headline-size 120 \
  --subhead-size 36 \
  --margin 10 \
  --top-offset 15
```

### Batch Processing

```bash
for img in campaign_*.png; do
  python pz_typography.py \
    --input "$img" \
    --output "output/$img" \
    --headline "LIMITED TIME" \
    --font-bold ./fonts/BarlowSemiCondensed-Bold.ttf \
    --font-semibold ./fonts/BarlowSemiCondensed-SemiBold.ttf
done
```

## Output

The script renders text as a clean RGBA composite layer over your original image — no background panels, no image modification underneath, just typography overlaid with optional drop shadow.

## Alternatives

- **Canva** — Free GUI, live preview, Barlow Semi Condensed available, non-destructive
- **Figma** — If you already use it, import image → add text layer → export
- **Photoshop** — Full control, paid

This CLI tool is best when you need scriptable, reproducible typography on images without a GUI.
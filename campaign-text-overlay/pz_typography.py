#!/usr/bin/env python3
"""CLI Typography Overlay Tool — Add text overlays to campaign images."""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_size(size_str, reference):
    """Parse size argument (px or %)."""
    if size_str is None:
        return None
    if size_str.endswith('%'):
        return float(size_str.rstrip('%')) / 100 * reference
    return int(size_str)


def main():
    parser = argparse.ArgumentParser(
        description='Add typography overlay to images'
    )
    parser.add_argument('--input', '-i', required=True,
                        help='Input image path')
    parser.add_argument('--output', '-o', required=True,
                        help='Output image path')

    parser.add_argument('--headline', default='',
                        help='First headline text')
    parser.add_argument('--headline2', default='',
                        help='Second headline text')
    parser.add_argument('--subhead', default='',
                        help='Subhead text')

    parser.add_argument('--font-bold', required=True,
                        help='Path to Bold (700) TTF font')
    parser.add_argument('--font-semibold', required=True,
                        help='Path to SemiBold (600) TTF font')

    parser.add_argument('--headline-size', default='9.8%',
                        help='Headline font size (px or percent of width, default: 9.8%%)')
    parser.add_argument('--subhead-size', default='3.3%',
                        help='Subhead font size (px or percent of width, default: 3.3%%)')
    parser.add_argument('--margin', default='5%',
                        help='Left margin (px or percent of width, default: 5%%)')
    parser.add_argument('--top-offset', default='6%',
                        help='Top offset (px or percent of height, default: 6%%)')
    parser.add_argument('--gap-after-headline', default='1.5%',
                        help='Gap between headline and subhead (px or percent of width)')

    parser.add_argument('--headline-color', default='#FFFFFF',
                        help='Headline color (hex, default: #FFFFFF)')
    parser.add_argument('--subhead-color', default='#8F98A1',
                        help='Subhead color (hex, default: #8F98A1)')

    parser.add_argument('--shadow-offset', type=int, default=3,
                        help='Drop shadow offset in px (default: 3)')
    parser.add_argument('--shadow-opacity', type=int, default=100,
                        help='Drop shadow opacity 0-255 (default: 100)')
    parser.add_argument('--no-shadow', action='store_true',
                        help='Disable drop shadow')
    parser.add_argument('--line-height', type=float, default=0.92,
                        help='Line height ratio (default: 0.92)')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.font_bold):
        print(f"Error: Bold font not found: {args.font_bold}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.font_semibold):
        print(f"Error: SemiBold font not found: {args.font_semibold}", file=sys.stderr)
        sys.exit(1)

    img = Image.open(args.input).convert("RGBA")
    W, H = img.size

    hl_size = parse_size(args.headline_size, W)
    sh_size = parse_size(args.subhead_size, W)
    margin = parse_size(args.margin, W)
    top_offset = parse_size(args.top_offset, H)
    gap = parse_size(args.gap_after_headline, W)

    font_hl = ImageFont.truetype(args.font_bold, int(hl_size))
    font_sh = ImageFont.truetype(args.font_semibold, int(sh_size))

    headline_rgb = hex_to_rgb(args.headline_color) + (255,)
    subhead_rgb = hex_to_rgb(args.subhead_color) + (255,)
    shadow_rgb = (0, 0, 0, args.shadow_opacity)

    line_height = int(hl_size * args.line_height)

    y_l1 = top_offset
    y_l2 = y_l1 + line_height
    y_sh = y_l2 + line_height + gap

    shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))

    if not args.no_shadow:
        sdraw = ImageDraw.Draw(shadow_layer)
        for text, y, font in [
            (args.headline, y_l1, font_hl),
            (args.headline2, y_l2, font_hl),
            (args.subhead, y_sh, font_sh),
        ]:
            if text:
                sdraw.text(
                    (margin + args.shadow_offset, y + args.shadow_offset),
                    text, font=font, fill=shadow_rgb
                )

    base = Image.alpha_composite(img, shadow_layer)
    draw = ImageDraw.Draw(base)

    if args.headline:
        draw.text((margin, y_l1), args.headline, font=font_hl, fill=headline_rgb)
    if args.headline2:
        draw.text((margin, y_l2), args.headline2, font=font_hl, fill=headline_rgb)
    if args.subhead:
        draw.text((margin, y_sh), args.subhead, font=font_sh, fill=subhead_rgb)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    base.convert("RGB").save(args.output, "PNG", quality=97)

    print(f"Done — {W}x{H}")
    print(f"Headline: {hl_size:.0f}px, Subhead: {sh_size:.0f}px")
    print(f"Margin: {margin:.0f}px, Top: {top_offset:.0f}px")


if __name__ == '__main__':
    main()
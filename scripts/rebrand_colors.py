#!/usr/bin/env python3
"""Replace Odoo brand colors in source files.

Usage:
  # Source files (pass file list via xargs):
  grep -rl '#875A7B' addons --include='*.xml' | xargs python3 scripts/rebrand_colors.py

  # Or for .po files (auto-discovers es/pt locales):
  python3 scripts/rebrand_colors.py --po addons

Color mapping:
  #875A7B (Odoo purple link)  -> #3b5cff (Aly Suite primary blue)
  #714B67 (Odoo enterprise)   -> #6d5efc (Aly Suite secondary purple)
  #71639e (Odoo community)    -> #3b5cff (Aly Suite primary blue)
  #017e84 (Odoo teal)         -> #11a8ff (Aly Suite accent cyan)
"""
import sys, os, glob

COLOR_MAP = {
    '#875A7B': '#3b5cff',
    '#875a7b': '#3b5cff',
    '#714B67': '#6d5efc',
    '#714b67': '#6d5efc',
    '#71639e': '#3b5cff',
    '#017e84': '#11a8ff',
    '#017E84': '#11a8ff',
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content
    for old, new in COLOR_MAP.items():
        new_content = new_content.replace(old, new)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if '--po' in sys.argv:
    sys.argv.remove('--po')
    base = sys.argv[1]
    patterns = ['**/i18n/es.po', '**/i18n/es_*.po', '**/i18n/pt.po', '**/i18n/pt_*.po']
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(base, pattern), recursive=True))
    files = sorted(set(files))
else:
    files = sys.argv[1:]

changed = 0
for f in files:
    if process_file(f):
        changed += 1

print(f"Processed {len(files)} files, modified {changed}")

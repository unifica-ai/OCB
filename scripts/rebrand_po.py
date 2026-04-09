#!/usr/bin/env python3
"""Replace Odoo branding in .po files for es/pt locales.

Usage: python3 scripts/rebrand_po.py addons

Replaces "Odoo" with "Aly Suite" in both msgid and msgstr lines
of Spanish and Portuguese .po files, while protecting technical
patterns like OdooBot, Odoo S.A., and Odooapps.
"""
import sys, os, glob

def process_line(line):
    if line.startswith('#'):
        return line

    protections = [
        ('OdooBot', '\x01ODOOBOT1\x01'),
        ('Odoobot', '\x01ODOOBOT2\x01'),
        ('odoobot', '\x01ODOOBOT3\x01'),
        ('Odoo S.A.', '\x01ODOOSA\x01'),
        ('Odooapps', '\x01ODOOAPPS\x01'),
    ]

    for orig, placeholder in protections:
        line = line.replace(orig, placeholder)

    line = line.replace('Odoo', 'Aly Suite')
    line = line.replace('www.odoo.com', 'www.aly-ai.com')
    line = line.replace('https://odoo.com', 'https://aly-ai.com')
    line = line.replace('http://odoo.com', 'https://aly-ai.com')

    for orig, placeholder in protections:
        line = line.replace(placeholder, orig)

    return line

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = [process_line(line) for line in lines]
    if new_lines != lines:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

base = sys.argv[1]
patterns = ['**/i18n/es.po', '**/i18n/es_*.po', '**/i18n/pt.po', '**/i18n/pt_*.po']
files = []
for pattern in patterns:
    files.extend(glob.glob(os.path.join(base, pattern), recursive=True))

changed = 0
for f in sorted(set(files)):
    if process_file(f):
        changed += 1

print(f"Processed {len(set(files))} files, modified {changed}")

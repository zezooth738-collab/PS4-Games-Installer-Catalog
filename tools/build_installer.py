#!/usr/bin/env python3
"""Build an FPKGi DATA catalog from an explicit list of authorized PS4 homebrew PKGs."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def is_https_url(value):
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == 'https' and bool(parsed.netloc) and not parsed.username and not parsed.password


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='authorized_packages.json')
    parser.add_argument('--output', default='installer_games.json')
    parser.add_argument('--report', default='catalog_build_report.json')
    args = parser.parse_args()
    items = json.loads(Path(args.input).read_text(encoding='utf-8'))
    if not isinstance(items, list):
        raise SystemExit('authorized_packages.json must be a JSON array.')

    entries = {}
    errors = []
    warnings = []
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f'Item {index}: expected a JSON object')
            continue
        url = item.get('pkg_url', '')
        name = item.get('name', '')
        title_id = item.get('title_id', '')
        version = item.get('version', '1.00')
        if not is_https_url(url):
            errors.append(f'Item {index}: pkg_url must be a valid HTTPS URL')
            continue
        if not isinstance(name, str) or not name.strip():
            errors.append(f'Item {index}: name is required')
            continue
        if not isinstance(title_id, str) or not title_id.strip():
            errors.append(f'Item {index}: title_id is required')
            continue
        if not isinstance(version, str) or not version.strip():
            errors.append(f'Item {index}: version must be a nonempty string')
            continue
        if url in entries:
            errors.append(f'Item {index}: duplicate pkg_url')
            continue
        if not urlparse(url).path.lower().endswith('.pkg'):
            warnings.append(f'Item {index}: URL does not end in .pkg; verify it returns a PS4 PKG file directly')
        entry = {'name': name.strip(), 'title_id': title_id.strip(), 'version': version.strip()}
        for key in ('cover_url', 'region', 'size', 'release', 'min_fw', 'package_type', 'content_id', 'package_category'):
            value = item.get(key)
            if value is not None and value != '':
                if key == 'cover_url' and not is_https_url(value):
                    errors.append(f'Item {index}: cover_url must be HTTPS')
                else:
                    entry[key] = value
        entries[url] = entry

    report = {'input_records': len(items), 'output_packages': len(entries) if not errors else 0,
              'errors': errors, 'warnings': warnings,
              'note': 'HTTPS syntax validation does not prove a URL is downloadable, safe, licensed, or compatible.'}
    Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if errors:
        raise SystemExit('Validation failed: ' + '; '.join(errors[:10]))
    Path(args.output).write_text(json.dumps({'DATA': entries}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Built {len(entries)} package entries. Warnings: {len(warnings)}')


if __name__ == '__main__':
    main()


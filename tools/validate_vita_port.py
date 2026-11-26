#!/usr/bin/env python3
"""Validate the static PS Vita package metadata in this repository.

This is a repository-side integrity check; it does not build or install a VPK.
Only Python's standard library is required.
"""
from __future__ import annotations

import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SFO_PATH = ROOT / "sce_sys" / "param.sfo"
LIVEAREA = ROOT / "sce_sys" / "livearea" / "contents"
TEMPLATE = LIVEAREA / "template.xml"
TITLE_ID_RE = re.compile(r"ux0:/?app/([A-Z0-9]{9})(?:/|\b)")


def read_sfo(path: Path) -> dict[str, str]:
    data = path.read_bytes()
    if len(data) < 20:
        raise ValueError("param.sfo is shorter than its header")
    magic, _version, key_offset, data_offset, count = struct.unpack_from("<4sIIII", data, 0)
    if magic != b"\x00PSF":
        raise ValueError("param.sfo has an invalid PSF signature")
    if count > 4096 or 20 + count * 16 > len(data):
        raise ValueError("param.sfo entry table is out of bounds")
    values: dict[str, str] = {}
    for index in range(count):
        entry = 20 + index * 16
        key_rel, _fmt, length, max_length, value_rel = struct.unpack_from("<HHIII", data, entry)
        key_start = key_offset + key_rel
        value_start = data_offset + value_rel
        if key_start >= len(data) or value_start > len(data):
            raise ValueError(f"param.sfo entry {index} points outside the file")
        key_end = data.find(b"\0", key_start)
        if key_end < 0:
            raise ValueError(f"param.sfo entry {index} has an unterminated key")
        if length > max_length or value_start + length > len(data):
            raise ValueError(f"param.sfo entry {index} has an invalid value range")
        key = data[key_start:key_end].decode("utf-8", errors="strict")
        raw = data[value_start:value_start + length].split(b"\0", 1)[0]
        values[key] = raw.decode("utf-8", errors="replace")
    return values


def validate() -> list[str]:
    errors: list[str] = []
    for required in (SFO_PATH, TEMPLATE, LIVEAREA / "bg.png", LIVEAREA / "startup.png"):
        if not required.is_file():
            errors.append(f"Missing required package file: {required.relative_to(ROOT)}")

    title_id = ""
    if SFO_PATH.is_file():
        try:
            sfo = read_sfo(SFO_PATH)
            title_id = sfo.get("TITLE_ID", "")
            if not re.fullmatch(r"[A-Z0-9]{9}", title_id):
                errors.append(f"Invalid or missing TITLE_ID in param.sfo: {title_id!r}")
            if not sfo.get("TITLE", "").strip():
                errors.append("TITLE is missing or empty in param.sfo")
        except (OSError, ValueError, UnicodeError, struct.error) as exc:
            errors.append(f"Cannot read param.sfo: {exc}")

    if TEMPLATE.is_file():
        try:
            root = ET.parse(TEMPLATE).getroot()
            if root.tag != "livearea":
                errors.append("LiveArea template root element must be <livearea>")
            refs = [node.text.strip() for node in root.iter() if node.tag in {"image", "startup-image"} and node.text and node.text.strip()]
            if not refs:
                errors.append("LiveArea template does not reference any images")
            for ref in refs:
                candidate = (LIVEAREA / ref).resolve()
                if not candidate.is_relative_to(LIVEAREA.resolve()):
                    errors.append(f"LiveArea asset escapes contents directory: {ref}")
                elif not candidate.is_file():
                    errors.append(f"LiveArea asset referenced by template is missing: {ref}")
        except (ET.ParseError, OSError, ValueError) as exc:
            errors.append(f"Invalid LiveArea template: {exc}")

    if title_id:
        docs = [ROOT / "README.md"]
        docs.extend(p for p in (ROOT / "wiki-source").glob("Installation*.md") if p.is_file())
        for doc in docs:
            if not doc.is_file():
                continue
            text = doc.read_text(encoding="utf-8")
            documented = sorted(set(TITLE_ID_RE.findall(text)))
            for value in documented:
                if value != title_id:
                    errors.append(f"{doc.relative_to(ROOT)} documents {value}, but param.sfo declares {title_id}")

    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("Vita package metadata, LiveArea assets and documented title ID: OK")

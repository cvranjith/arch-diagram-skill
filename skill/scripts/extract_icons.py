#!/usr/bin/env python3
"""
extract_icons.py — One-time OCI icon extraction script
Run once to extract SVG icons from OCI_Icons.pptx into the skill assets folder.

Usage:
    python3 skill/scripts/extract_icons.py --pptx source/oracle-downloads/OCI_Icons.pptx

Output:
    skill/assets/icons/oci/           ← individual .svg files with friendly names
    skill/assets/icons/oci_icons.json ← {name: "data:image/svg+xml;base64,..."} lookup
"""

import zipfile, base64, json, os, argparse, sys

# ─────────────────────────────────────────────────────────
# MAPPING: pptx internal filename → friendly slug name
# Based on OCI Architecture Diagram Toolkit v24.1
# ─────────────────────────────────────────────────────────
ICON_MAP = {
    # Brand
    "image4.svg":  "oracle-logo",

    # Identity & People
    "image26.svg": "user",
    "image65.svg": "people-group",

    # Networking & Gateway
    "image29.svg": "api-gateway",
    "image45.svg": "load-balancer",
    "image31.svg": "enterprise-building",
    "image78.svg": "banner-wide",

    # Compute & Containers
    "image41.svg": "compute",
    "image43.svg": "container",
    "image47.svg": "kubernetes",
    "image49.svg": "functions",

    # Storage & Data
    "image33.svg": "database",
    "image35.svg": "object-storage",

    # Developer & Integration
    "image51.svg": "integration",
    "image53.svg": "devops",

    # Analytics & AI
    "image58.svg": "logging",
    "image60.svg": "analytics",
    "image62.svg": "generative-ai",
    "image68.svg": "streaming",
    "image70.svg": "security-shield",
    "image72.svg": "cloud-service",
    "image56.svg": "monitoring",

    # Security
    "image76.svg": "vault-key",
}

# Category color mapping (for CSS --card-accent)
ICON_CATEGORIES = {
    "oracle-logo":        {"category": "brand",       "color": "#C74634"},
    "user":               {"category": "identity",    "color": "#2C5967"},
    "people-group":       {"category": "identity",    "color": "#C74634"},
    "api-gateway":        {"category": "networking",  "color": "#2C5967"},
    "load-balancer":      {"category": "networking",  "color": "#2C5967"},
    "enterprise-building":{"category": "integration", "color": "#2C5967"},
    "banner-wide":        {"category": "other",       "color": "#312D2A"},
    "compute":            {"category": "compute",     "color": "#759C6C"},
    "container":          {"category": "compute",     "color": "#759C6C"},
    "kubernetes":         {"category": "compute",     "color": "#759C6C"},
    "functions":          {"category": "compute",     "color": "#759C6C"},
    "database":           {"category": "data",        "color": "#AE562C"},
    "object-storage":     {"category": "data",        "color": "#AE562C"},
    "integration":        {"category": "integration", "color": "#2C5967"},
    "devops":             {"category": "developer",   "color": "#2C5967"},
    "logging":            {"category": "observability","color": "#312D2A"},
    "analytics":          {"category": "analytics",   "color": "#2C5967"},
    "generative-ai":      {"category": "ai",          "color": "#2C5967"},
    "streaming":          {"category": "integration", "color": "#2C5967"},
    "security-shield":    {"category": "security",    "color": "#2C5967"},
    "cloud-service":      {"category": "other",       "color": "#2C5967"},
    "monitoring":         {"category": "observability","color": "#312D2A"},
    "vault-key":          {"category": "security",    "color": "#C74634"},
}

def extract_icons(pptx_path: str, out_dir: str):
    svg_dir = os.path.join(out_dir, "oci")
    os.makedirs(svg_dir, exist_ok=True)

    icons_json = {}   # name → data URI
    meta_json  = {}   # name → {category, color, file}
    extracted  = []
    skipped    = []

    print(f"\nExtracting OCI icons from: {pptx_path}")
    print(f"Output directory: {out_dir}\n")

    with zipfile.ZipFile(pptx_path, 'r') as z:
        available = set(z.namelist())

        for img_file, friendly_name in ICON_MAP.items():
            src_path = f"ppt/media/{img_file}"
            if src_path not in available:
                skipped.append(img_file)
                print(f"  ⚠  SKIP  {img_file} (not found in pptx)")
                continue

            data = z.read(src_path)

            # Save individual SVG file
            svg_path = os.path.join(svg_dir, f"{friendly_name}.svg")
            with open(svg_path, 'wb') as f:
                f.write(data)

            # Build data URI
            b64 = base64.b64encode(data).decode('ascii')
            data_uri = f"data:image/svg+xml;base64,{b64}"

            icons_json[friendly_name] = data_uri
            meta_json[friendly_name] = {
                **ICON_CATEGORIES.get(friendly_name, {"category": "other", "color": "#2C5967"}),
                "file": os.path.join(out_dir, "oci", f"{friendly_name}.svg").replace("\\", "/"),
                "source": img_file,
            }
            extracted.append(friendly_name)
            print(f"  ✓  {friendly_name:30s} ← {img_file}")

    # Write oci_icons.json (data URIs for embedding in HTML)
    json_path = os.path.join(out_dir, "oci_icons.json")
    with open(json_path, 'w') as f:
        json.dump(icons_json, f, indent=2)

    # Write oci_meta.json (categories, colors, file paths)
    meta_path = os.path.join(out_dir, "oci_meta.json")
    with open(meta_path, 'w') as f:
        json.dump(meta_json, f, indent=2)

    # Write a quick HTML preview
    preview_path = os.path.join(out_dir, "icon_preview.html")
    rows = ""
    for name, uri in sorted(icons_json.items()):
        cat = meta_json[name]["category"]
        color = meta_json[name]["color"]
        rows += f"""
        <tr>
          <td><img src="{uri}" width="32" height="32" style="color:{color}"></td>
          <td><code>{name}</code></td>
          <td style="color:{color}">{cat}</td>
          <td><span style="background:{color};color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">{color}</span></td>
        </tr>"""

    with open(preview_path, 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>OCI Icon Preview</title>
<style>
  body {{ font-family: Arial, sans-serif; padding: 20px; background: #F5F4F2; }}
  h1 {{ font-size: 18px; color: #312D2A; margin-bottom: 16px; }}
  table {{ border-collapse: collapse; background: #fff; border-radius: 6px;
           box-shadow: 0 1px 4px rgba(0,0,0,0.1); overflow: hidden; width: 600px; }}
  th {{ background: #1e3d47; color: #fff; padding: 8px 12px;
        text-align: left; font-size: 11px; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #DFDCD8; font-size: 12px; vertical-align: middle; }}
  tr:last-child td {{ border-bottom: none; }}
</style>
</head><body>
<h1>OCI Icons — {len(icons_json)} extracted</h1>
<table>
  <tr><th>Icon</th><th>Key name</th><th>Category</th><th>Default color</th></tr>
  {rows}
</table>
<p style="margin-top:12px;font-size:11px;color:#70736E">
  Use key names in oci_icons.json. Reference: [out]/oci/&lt;name&gt;.svg
</p>
</body></html>""")

    print(f"\n{'─'*50}")
    print(f"  Extracted : {len(extracted)} icons")
    print(f"  Skipped   : {len(skipped)}")
    print(f"\n  Files written:")
    print(f"    {json_path}")
    print(f"    {meta_path}")
    print(f"    {preview_path}")
    print(f"    {svg_dir}/*.svg")
    print(f"\n  Open icon_preview.html to verify all icons.")
    print(f"{'─'*50}\n")

    return icons_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract OCI icons from OCI_Icons.pptx")
    parser.add_argument("--pptx", required=True,
                        help="Path to OCI_Icons.pptx (download from Oracle)")
    parser.add_argument("--out", default="skill/assets/icons",
                        help="Output directory (default: ./skill/assets/icons)")
    args = parser.parse_args()

    if not os.path.exists(args.pptx):
        print(f"ERROR: File not found: {args.pptx}")
        sys.exit(1)

    extract_icons(args.pptx, args.out)

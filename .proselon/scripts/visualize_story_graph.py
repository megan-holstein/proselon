#!/usr/bin/env python3
"""Render an OKF knowledge bundle as a self-contained interactive graph.

Walks a bundle of OKF markdown files (YAML frontmatter + cross-links), builds a
node-and-edge graph, and writes a single self-contained HTML file — no server,
no external libraries, nothing leaves the page. Open it in any browser.

Usage:
    python .proselon/scripts/visualize_story_graph.py [--bundle story|framework] [-o OUTPUT]

    --bundle story      (default) the author's story bible:
                        Worldbuilding/, Plot/, Research/, Style/, Publishing/
    --bundle framework  the Proselon method: .proselon/workflow/
    -o, --output        output path (default: "Story Graph.html" / "Framework Graph.html"
                        at the project root)

Nodes are colored by OKF `type`; edges come from both `related:` frontmatter
and inline markdown links. Click a node for its details. Manuscripts/ and
Fragments/ are never included (export-safe prose and raw scraps carry no metadata).

Stdlib only — no pip installs, no PyYAML. If Python is unavailable, the agent can
build an equivalent HTML by hand: it knows the bundle and these conventions.
See `.proselon/workflow/OKF Conventions.md`.
"""

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BUNDLES = {
    "story": ["Worldbuilding", "Plot", "Research", "Style", "Publishing"],
    "framework": [".proselon/workflow"],
}

# Never graph these (export-safe prose, raw scraps, app/vcs dirs).
SKIP_PARTS = {"Manuscripts", "Fragments", "Archive", ".obsidian", ".git", "node_modules"}

TYPE_COLORS = {
    # story bible
    "Character": "#e8643c", "Location": "#2e8b57", "Faction": "#8e5cd9",
    "Worldbuilding": "#1f9bd1", "Research": "#c9a227",
    "Book Specs": "#6c757d", "Series Plot": "#d4377a", "Themes & Conflict": "#b5179e",
    "Style Guide": "#20a39e", "Voice Reference": "#17a2b8",
    "Book Plot": "#e83e8c", "Story State": "#fd7e14",
    "Chapter Map": "#e85d04", "Chapter Plot": "#f48c06", "Scene Plot": "#ffba08",
    "KDP Listing": "#6f42c1",
    # framework
    "Template": "#4361ee", "Rubric": "#f72585", "Pass": "#4cc9f0",
    "Procedure": "#3a86ff", "Reference": "#8d99ae",
    "Untyped": "#adb5bd",
}

LINK_RE = re.compile(r"\]\(\s*(<[^>]+>|[^)\s]+)\s*\)")
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def parse_frontmatter(text):
    """Return (meta_dict, body). Minimal YAML for our flat key/value + flow lists."""
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta = {}
    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if key in ("tags", "related"):
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                meta[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
            elif val:
                meta[key] = [val.strip('"').strip("'")]
            else:
                meta[key] = []
        else:
            if key != "description":
                cut = val.find(" #")
                if cut != -1:
                    val = val[:cut].strip()
            meta[key] = val.strip().strip('"').strip("'")
    return meta, "\n".join(lines[end + 1:])


def iter_md_files(root, dirs):
    for d in dirs:
        base = root / d
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if SKIP_PARTS & set(path.relative_to(root).parts):
                continue
            yield path


def resolve_target(src_rel, raw, node_ids):
    """Resolve a link/related target to a node id (posix path relative to root)."""
    raw = raw.strip().strip("<>").strip()
    if not raw or raw.startswith(("http://", "https://", "#", "mailto:")):
        return None
    raw = raw.split("#", 1)[0]
    if not raw.endswith(".md"):
        return None
    if raw.startswith("/"):
        candidate = Path(raw.lstrip("/"))
    else:
        candidate = (Path(src_rel).parent / raw)
    # normalize .. without touching the filesystem
    parts = []
    for part in candidate.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part not in (".", ""):
            parts.append(part)
    resolved = "/".join(parts)
    return resolved if resolved in node_ids else None


def build_graph(root, dirs):
    files = list(iter_md_files(root, dirs))
    raw = {}
    for path in files:
        node_id = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)
        raw[node_id] = (meta, body)

    node_ids = set(raw)
    nodes, edges = [], set()
    for node_id, (meta, body) in raw.items():
        h1 = H1_RE.search(body)
        label = meta.get("title") or (h1.group(1).strip() if h1 else Path(node_id).stem)
        ntype = meta.get("type") or "Untyped"
        nodes.append({
            "id": node_id,
            "label": label,
            "type": ntype,
            "description": meta.get("description", ""),
            "tier": meta.get("tier", ""),
        })
        targets = list(meta.get("related", []))
        targets += LINK_RE.findall(body)
        for raw_t in targets:
            tgt = resolve_target(node_id, raw_t, node_ids)
            if tgt and tgt != node_id:
                edges.add(tuple(sorted((node_id, tgt))))

    colors = {n["type"]: TYPE_COLORS.get(n["type"], "#adb5bd") for n in nodes}
    return {
        "nodes": nodes,
        "links": [{"source": a, "target": b} for a, b in sorted(edges)],
        "colors": colors,
    }


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  html,body{margin:0;height:100%;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0f1117;color:#e6e8ee;overflow:hidden}
  #graph{width:100vw;height:100vh;display:block;cursor:grab}
  #graph.panning{cursor:grabbing}
  .edge{stroke:#3a4055;stroke-width:1.2}
  .node circle{stroke:#0f1117;stroke-width:1.5;cursor:pointer}
  .node text{fill:#c4c9d6;font-size:11px;pointer-events:none;paint-order:stroke;stroke:#0f1117;stroke-width:3px}
  #header{position:fixed;top:14px;left:16px;max-width:42vw}
  #header h1{font-size:16px;margin:0 0 2px}
  #header .sub{font-size:12px;color:#8b93a7}
  #legend{position:fixed;top:14px;right:16px;background:rgba(20,23,33,.85);border:1px solid #2a3046;border-radius:8px;padding:10px 12px;max-height:80vh;overflow:auto;font-size:12px}
  #legend .row{display:flex;align-items:center;gap:7px;margin:3px 0;cursor:default}
  #legend .dot{width:11px;height:11px;border-radius:50%;flex:none}
  #panel{position:fixed;bottom:16px;left:16px;display:none;max-width:38vw;background:rgba(20,23,33,.95);border:1px solid #2a3046;border-radius:8px;padding:12px 14px}
  #panel h2{font-size:14px;margin:0 0 4px}
  #panel .meta{font-size:11px;color:#8b93a7;margin-bottom:6px}
  #panel .desc{font-size:13px;color:#cdd2df;margin-bottom:8px}
  #panel a{color:#6db3f2;font-size:12px;word-break:break-all}
  #panel .close{position:absolute;top:8px;right:11px;cursor:pointer;color:#8b93a7}
  #hint{position:fixed;bottom:16px;right:16px;font-size:11px;color:#5b6478}
</style>
</head>
<body>
<div id="header"><h1>__TITLE__</h1><div class="sub" id="subtitle">__SUBTITLE__</div></div>
<div id="legend"></div>
<div id="panel"><span class="close" onclick="document.getElementById('panel').style.display='none'">&times;</span><h2 id="p-title"></h2><div class="meta" id="p-meta"></div><div class="desc" id="p-desc"></div><a id="p-link" target="_blank"></a></div>
<div id="hint">drag nodes · scroll to zoom · drag background to pan</div>
<svg id="graph"><g id="viewport"></g></svg>
<script>
const DATA = __DATA__;
const SVGNS = "http://www.w3.org/2000/svg";
const svg = document.getElementById("graph");
const viewport = document.getElementById("viewport");
let W = window.innerWidth, H = window.innerHeight;

const nodes = DATA.nodes.map((n,i) => {
  const a = i * 2.399963, r = 30 + 12*Math.sqrt(i);
  return Object.assign({}, n, {x: W/2 + r*Math.cos(a), y: H/2 + r*Math.sin(a), vx:0, vy:0, deg:0});
});
const byId = {}; nodes.forEach(n => byId[n.id] = n);
const links = DATA.links.filter(l => byId[l.source] && byId[l.target])
                        .map(l => ({source: byId[l.source], target: byId[l.target]}));
links.forEach(l => {l.source.deg++; l.target.deg++;});

// ---- build SVG ----
const edgeEls = links.map(l => {
  const e = document.createElementNS(SVGNS, "line");
  e.setAttribute("class","edge"); viewport.appendChild(e); return e;
});
const nodeEls = nodes.map(n => {
  const g = document.createElementNS(SVGNS, "g"); g.setAttribute("class","node");
  const c = document.createElementNS(SVGNS, "circle");
  const r = 6 + Math.min(n.deg, 9);
  c.setAttribute("r", r); c.setAttribute("fill", DATA.colors[n.type] || "#adb5bd");
  const t = document.createElementNS(SVGNS, "text");
  t.setAttribute("x", r + 3); t.setAttribute("y", 4); t.textContent = n.label;
  g.appendChild(c); g.appendChild(t); viewport.appendChild(g);
  g._node = n; return g;
});

// ---- force simulation ----
let alpha = 1;
const CHARGE = -420, LINKDIST = 95, CENTER = 0.03, DECAY = 0.6;
function tick(){
  for (let i=0;i<nodes.length;i++){
    for (let j=i+1;j<nodes.length;j++){
      const a=nodes[i], b=nodes[j];
      let dx=a.x-b.x, dy=a.y-b.y, d2=dx*dx+dy*dy || 0.01;
      const f = CHARGE*alpha/d2, d=Math.sqrt(d2);
      const fx=f*dx/d, fy=f*dy/d;
      a.vx+=fx; a.vy+=fy; b.vx-=fx; b.vy-=fy;
    }
  }
  links.forEach(l => {
    let dx=l.target.x-l.source.x, dy=l.target.y-l.source.y, d=Math.sqrt(dx*dx+dy*dy)||0.01;
    const f=(d-LINKDIST)/d*alpha*0.5, fx=f*dx, fy=f*dy;
    l.source.vx+=fx; l.source.vy+=fy; l.target.vx-=fx; l.target.vy-=fy;
  });
  nodes.forEach(n => {
    n.vx += (W/2-n.x)*CENTER*alpha; n.vy += (H/2-n.y)*CENTER*alpha;
    if (n.fx==null){ n.vx*=DECAY; n.vy*=DECAY; n.x+=n.vx; n.y+=n.vy; }
    else { n.x=n.fx; n.y=n.fy; n.vx=n.vy=0; }
  });
  alpha *= 0.992;
}
function render(){
  links.forEach((l,i)=>{const e=edgeEls[i];e.setAttribute("x1",l.source.x);e.setAttribute("y1",l.source.y);e.setAttribute("x2",l.target.x);e.setAttribute("y2",l.target.y);});
  nodeEls.forEach(g=>{g.setAttribute("transform",`translate(${g._node.x},${g._node.y})`);});
}
function loop(){ for(let k=0;k<2;k++) if(alpha>0.005) tick(); render(); requestAnimationFrame(loop); }
loop();

// ---- pan / zoom ----
let view={x:0,y:0,k:1};
function applyView(){ viewport.setAttribute("transform",`translate(${view.x},${view.y}) scale(${view.k})`); }
svg.addEventListener("wheel", e=>{
  e.preventDefault();
  const s = e.deltaY<0 ? 1.1 : 1/1.1;
  const mx=e.clientX, my=e.clientY;
  view.x = mx - (mx-view.x)*s; view.y = my - (my-view.y)*s; view.k*=s;
  applyView();
}, {passive:false});

// ---- drag (node or background) ----
let drag=null, moved=false;
function graphCoord(e){ return {x:(e.clientX-view.x)/view.k, y:(e.clientY-view.y)/view.k}; }
svg.addEventListener("pointerdown", e=>{
  const g = e.target.closest(".node"); moved=false;
  if (g){ drag={node:g._node}; const p=graphCoord(e); drag.node.fx=p.x; drag.node.fy=p.y; alpha=Math.max(alpha,0.3); }
  else { drag={pan:true, sx:e.clientX-view.x, sy:e.clientY-view.y}; svg.classList.add("panning"); }
  svg.setPointerCapture(e.pointerId);
});
svg.addEventListener("pointermove", e=>{
  if(!drag) return; moved=true;
  if (drag.node){ const p=graphCoord(e); drag.node.fx=p.x; drag.node.fy=p.y; alpha=Math.max(alpha,0.2); }
  else { view.x=e.clientX-drag.sx; view.y=e.clientY-drag.sy; applyView(); }
});
svg.addEventListener("pointerup", e=>{
  if (drag && drag.node){ if(!moved) showPanel(drag.node); drag.node.fx=null; drag.node.fy=null; }
  drag=null; svg.classList.remove("panning");
});

// ---- info panel ----
function showPanel(n){
  document.getElementById("p-title").textContent = n.label;
  document.getElementById("p-meta").textContent = n.type + (n.tier ? " · " + n.tier + " tier" : "");
  document.getElementById("p-desc").textContent = n.description || "";
  const a=document.getElementById("p-link"); a.href=encodeURI(n.id); a.textContent=n.id;
  document.getElementById("panel").style.display="block";
}

// ---- legend ----
(function(){
  const counts={}; nodes.forEach(n=>counts[n.type]=(counts[n.type]||0)+1);
  const leg=document.getElementById("legend");
  Object.keys(counts).sort().forEach(t=>{
    const row=document.createElement("div"); row.className="row";
    row.innerHTML=`<span class="dot" style="background:${DATA.colors[t]||'#adb5bd'}"></span>${t} (${counts[t]})`;
    leg.appendChild(row);
  });
})();
window.addEventListener("resize", ()=>{W=window.innerWidth;H=window.innerHeight;});
</script>
</body>
</html>
"""


def render_html(graph, title, subtitle):
    # Escape "</" so a description containing "</script>" can't terminate the
    # inline <script> block ("<\/" is a valid JSON string escape for "</").
    data = json.dumps(graph).replace("</", "<\\/")
    return (HTML_TEMPLATE
            .replace("__DATA__", data)
            .replace("__TITLE__", title)
            .replace("__SUBTITLE__", subtitle))


def main():
    ap = argparse.ArgumentParser(description="Render an OKF bundle as a self-contained HTML graph.")
    ap.add_argument("--bundle", choices=sorted(BUNDLES), default="story")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()

    graph = build_graph(PROJECT_ROOT, BUNDLES[args.bundle])
    if not graph["nodes"]:
        where = ", ".join(BUNDLES[args.bundle])
        print(f"No OKF documents found in: {where}\n"
              f"(A fresh project's story bible is empty until you start writing.)", file=sys.stderr)
        return 1

    title = "Story Graph" if args.bundle == "story" else "Proselon Framework Graph"
    n_edges = len(graph["links"])
    subtitle = f"{len(graph['nodes'])} concepts · {n_edges} links · {args.bundle} bundle"
    out = Path(args.output) if args.output else PROJECT_ROOT / f"{title}.html"
    out.write_text(render_html(graph, title, subtitle), encoding="utf-8")
    print(f"Wrote {out}  ({len(graph['nodes'])} nodes, {n_edges} edges). Open it in any browser.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

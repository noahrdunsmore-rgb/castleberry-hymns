"""
Castleberry Service Deck Builder — local web app ("the button")
================================================================
Run this on the PC that has the hymn assets, then open the page it prints:

    python service_app.py            # then visit http://127.0.0.1:5000

Workflow on the page:
  1. Paste the worship leader's order  ->  "Parse with AI"
        (uses parse_lineup.py; needs ANTHROPIC_API_KEY). Or skip and edit the
        lineup JSON directly.
  2. Review / edit the lineup JSON (fix any flagged songs, paste scripture text).
  3. "Build Deck"  ->  saves to service-decks/, offers a download, and (if the
        box is checked + email_config.json is set) emails you a copy.

This is intentionally a *local* server: the build must run where the song
slides live, so nothing is exposed to the internet.
"""

from __future__ import annotations

import json
import traceback
from pathlib import Path

from flask import Flask, request, jsonify, send_file, Response

import build_service_deck as bsd
import notify

try:
    import parse_lineup
    _HAS_PARSER = True
except Exception:
    _HAS_PARSER = False

ROOT = Path(__file__).parent
app = Flask(__name__)

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Castleberry Service Deck Builder</title>
<style>
:root{--red:#C31832;--red-dark:#9B1226;--dark:#1C1C1C;--bg:#F8F8F8;--border:#E0E0E0;--muted:#6B6B6B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,Segoe UI,Arial,sans-serif;background:var(--bg);color:var(--dark);line-height:1.45}
header{background:var(--dark);color:#fff;padding:1.1rem 1.4rem;display:flex;align-items:center;gap:.8rem}
header h1{font-size:1.15rem;font-weight:700}
header .tag{font-size:.75rem;color:#bbb}
main{max-width:900px;margin:0 auto;padding:1.4rem}
.card{background:#fff;border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.3rem;margin-bottom:1.2rem}
.card h2{font-size:.95rem;color:var(--red);margin-bottom:.7rem;text-transform:uppercase;letter-spacing:.03em}
label{font-size:.82rem;color:var(--muted);display:block;margin:.5rem 0 .25rem}
textarea,input{width:100%;border:1.5px solid var(--border);border-radius:8px;padding:.6rem .8rem;font-size:.9rem;font-family:inherit}
textarea{resize:vertical}
#order{min-height:150px}
#lineup{min-height:300px;font-family:ui-monospace,Consolas,monospace;font-size:.82rem}
.row{display:flex;gap:.7rem;flex-wrap:wrap;align-items:center}
.row .col{flex:1;min-width:160px}
button{background:var(--red);color:#fff;border:0;border-radius:8px;padding:.6rem 1.1rem;font-size:.9rem;font-weight:600;cursor:pointer}
button:hover{background:var(--red-dark)}
button.ghost{background:#eee;color:var(--dark)}
button:disabled{opacity:.55;cursor:not-allowed}
.note{font-size:.8rem;color:var(--muted);margin-top:.5rem}
.warn{background:#FDEEF1;border:1px solid #f3c6cf;color:#9B1226;border-radius:8px;padding:.6rem .8rem;font-size:.82rem;margin-top:.6rem;white-space:pre-wrap}
.ok{background:#eafaf0;border:1px solid #b6e6c8;color:#1c7a44;border-radius:8px;padding:.6rem .8rem;font-size:.85rem;margin-top:.6rem;white-space:pre-wrap}
.check{display:flex;align-items:center;gap:.4rem;font-size:.85rem;color:var(--dark)}
.check input{width:auto}
.spin{display:none}
.busy .spin{display:inline}
a.dl{display:inline-block;margin-top:.6rem;font-weight:600;color:var(--red)}
</style></head><body>
<header><h1>Castleberry Service Deck Builder</h1><span class="tag">local · __PARSER__</span></header>
<main>
  <div class="card">
    <h2>1 · Paste the worship order</h2>
    <textarea id="order" placeholder="Paste the worship leader's service order here (songs, verses, scripture, communion, giving, prayers...)"></textarea>
    <div class="row" style="margin-top:.7rem">
      <button id="parseBtn" __PARSEDISABLED__>Parse with AI <span class="spin">…</span></button>
      <button class="ghost" id="exampleBtn">Load example</button>
    </div>
    <div id="parseMsg"></div>
  </div>

  <div class="card">
    <h2>2 · Review &amp; edit the lineup</h2>
    <div class="row">
      <div class="col"><label>Service</label><input id="service" value="CB 11 Service line-up"></div>
      <div class="col"><label>Date label</label><input id="date" placeholder="6.7.26"></div>
    </div>
    <label>Lineup JSON</label>
    <textarea id="lineup" placeholder='Click "Parse with AI", "Load example", or paste a lineup JSON here.'></textarea>
  </div>

  <div class="card">
    <h2>3 · Build</h2>
    <label class="check"><input type="checkbox" id="email" __EMAILDISABLED__> Email me a copy __EMAILNOTE__</label>
    <div class="row" style="margin-top:.8rem">
      <button id="buildBtn">Build Deck <span class="spin">…</span></button>
    </div>
    <div id="buildMsg"></div>
  </div>
</main>
<script>
const $ = id => document.getElementById(id);
function busy(btn, on){ btn.classList.toggle('busy', on); btn.disabled = on; }

$('exampleBtn').onclick = async () => {
  const r = await fetch('/example'); const j = await r.json();
  $('lineup').value = JSON.stringify(j.lineup, null, 2);
  if (j.lineup.service) $('service').value = j.lineup.service;
  if (j.lineup.date) $('date').value = j.lineup.date;
};

$('parseBtn').onclick = async () => {
  $('parseMsg').innerHTML='';
  busy($('parseBtn'), true);
  try{
    const r = await fetch('/parse', {method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({order:$('order').value, date:$('date').value, service:$('service').value})});
    const j = await r.json();
    if(!j.ok){ $('parseMsg').innerHTML = '<div class="warn">'+j.error+'</div>'; return; }
    $('lineup').value = JSON.stringify(j.lineup, null, 2);
    if (j.lineup.date) $('date').value = j.lineup.date;
    if (j.notes && j.notes.length)
      $('parseMsg').innerHTML = '<div class="warn">Review these songs:\\n• '+j.notes.join('\\n• ')+'</div>';
    else
      $('parseMsg').innerHTML = '<div class="ok">Parsed — every song matched a deck.</div>';
  }catch(e){ $('parseMsg').innerHTML='<div class="warn">'+e+'</div>'; }
  finally{ busy($('parseBtn'), false); }
};

$('buildBtn').onclick = async () => {
  $('buildMsg').innerHTML='';
  let lineup;
  try{ lineup = JSON.parse($('lineup').value); }
  catch(e){ $('buildMsg').innerHTML='<div class="warn">Lineup JSON is not valid: '+e+'</div>'; return; }
  lineup.service = $('service').value || lineup.service;
  lineup.date = $('date').value || lineup.date;
  busy($('buildBtn'), true);
  try{
    const r = await fetch('/build', {method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({lineup, email: $('email').checked})});
    const j = await r.json();
    if(!j.ok){ $('buildMsg').innerHTML='<div class="warn">'+j.error+'</div>'; return; }
    let html = '<div class="ok">'+j.summary+'</div>';
    html += '<a class="dl" href="'+j.download+'">⬇ Download '+j.filename+'</a>';
    if(j.warnings && j.warnings.length)
      html += '<div class="warn">Warnings:\\n• '+j.warnings.join('\\n• ')+'</div>';
    if(j.email_status)
      html += '<div class="'+(j.email_ok?'ok':'warn')+'">'+j.email_status+'</div>';
    $('buildMsg').innerHTML = html;
  }catch(e){ $('buildMsg').innerHTML='<div class="warn">'+e+'</div>'; }
  finally{ busy($('buildBtn'), false); }
};
</script>
</body></html>"""


@app.route("/")
def index():
    html = (PAGE
        .replace("__PARSER__", "AI parsing on" if _HAS_PARSER else "AI parsing off — edit JSON")
        .replace("__PARSEDISABLED__", "" if _HAS_PARSER else "disabled title='parse_lineup unavailable'")
        .replace("__EMAILDISABLED__", "" if notify.is_configured() else "disabled")
        .replace("__EMAILNOTE__", "" if notify.is_configured()
                 else "<span class='note'>(set up email_config.json to enable)</span>"))
    return Response(html, mimetype="text/html")


@app.route("/example")
def example():
    p = ROOT / "lineups" / "example-service.json"
    return jsonify(lineup=json.loads(p.read_text(encoding="utf-8")))


@app.route("/parse", methods=["POST"])
def parse():
    if not _HAS_PARSER:
        return jsonify(ok=False, error="parse_lineup is unavailable (missing anthropic / API key).")
    data = request.get_json(force=True)
    order = (data.get("order") or "").strip()
    if not order:
        return jsonify(ok=False, error="Paste the worship order first.")
    try:
        lineup = parse_lineup.extract_lineup(order)
        if data.get("date"):    lineup["date"] = data["date"]
        if data.get("service"): lineup["service"] = data["service"]
        index = bsd.build_song_index()
        notes = parse_lineup.resolve_titles(lineup, index)
        return jsonify(ok=True, lineup=lineup, notes=notes)
    except KeyError:
        return jsonify(ok=False, error="ANTHROPIC_API_KEY is not set in this environment.")
    except Exception as e:
        return jsonify(ok=False, error=f"{e}\n{traceback.format_exc()[-400:]}")


@app.route("/build", methods=["POST"])
def build():
    data = request.get_json(force=True)
    lineup = data.get("lineup")
    if not isinstance(lineup, dict) or not lineup.get("items"):
        return jsonify(ok=False, error="Lineup has no items.")
    try:
        template = json.loads((ROOT / "service-template" / "template.json").read_text(encoding="utf-8"))
        index = bsd.build_song_index()
        out_path = bsd.default_out_name(lineup, ROOT / "lineups" / "untitled")
        report = bsd.build(lineup, out_path, template, index)

        # Save the lineup spec alongside, for the record / re-runs.
        date = (lineup.get("date") or "lineup").replace("/", ".")
        spec_path = ROOT / "lineups" / (bsd.re.sub(r'[<>:"/\\|?*]', "", date) + ".json")
        spec_path.write_text(json.dumps(lineup, indent=2, ensure_ascii=False), encoding="utf-8")

        resp = dict(ok=True,
                    summary=f"Built {Path(report['out']).name} — {report['total_slides']} slides.",
                    filename=Path(report["out"]).name,
                    download=f"/download/{Path(report['out']).name}",
                    warnings=report.get("warnings", []))

        if data.get("email"):
            ok, status = notify.send_deck(
                Path(report["out"]),
                subject=f"Service deck — {lineup.get('service','CB Service')} ({lineup.get('date','')})",
                body=(f"Attached/saved: the worship slide deck for "
                      f"{lineup.get('service','the service')} ({lineup.get('date','')}).\n"
                      f"{report['total_slides']} slides. Built automatically."))
            resp["email_ok"], resp["email_status"] = ok, status

        return jsonify(resp)
    except Exception as e:
        return jsonify(ok=False, error=f"{e}\n{traceback.format_exc()[-500:]}")


@app.route("/download/<path:name>")
def download(name):
    f = bsd.OUT_DIR / name
    if not f.exists():
        return ("Not found", 404)
    return send_file(str(f), as_attachment=True, download_name=name)


if __name__ == "__main__":
    print("\n  Castleberry Service Deck Builder")
    print("  Open:  http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=False)

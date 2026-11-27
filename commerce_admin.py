"""Secure ULTIMA commerce dashboard and ingestion API."""
import os, hmac
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from flask import request, jsonify, Response, redirect
from sqlalchemy import func, case

PAGE = r"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ULTIMA · Commerce & Rechnungen</title>
<style>
:root{color-scheme:dark;--gold:#e7c879;--cyan:#5ce1e6;--muted:#a8b5c9}*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 15% 0,#33251d,transparent 42%),linear-gradient(145deg,#05070c,#12131b 65%,#080b12);color:#f4ead8;font:15px system-ui;overflow-x:hidden}body:before,body:after{content:"⚙";position:fixed;z-index:-1;pointer-events:none;color:#aaa;opacity:.09;font-size:min(80vw,570px);line-height:1;animation:gear 100s linear infinite}body:before{left:-.3em;top:12vh}body:after{right:-.3em;bottom:-.3em;font-size:min(65vw,460px);animation-direction:reverse}@keyframes gear{to{transform:rotate(360deg)}}main{max-width:1180px;margin:auto;padding:28px 18px 70px}.brand{color:var(--gold);letter-spacing:.2em;font-size:11px}.head{display:flex;justify-content:space-between;align-items:center;gap:15px;flex-wrap:wrap;margin:10px 0 24px}h1{font-size:clamp(30px,5vw,48px);margin:5px 0}h2{font-size:18px;margin:0 0 15px}.muted{color:var(--muted)}a{color:var(--cyan)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:16px 0 24px}.panel,.stat{background:linear-gradient(145deg,#241c19ed,#111723f2 75%);border:1px solid #765b3d;border-radius:17px;padding:18px;box-shadow:0 14px 38px #0007}.stat small{display:block;color:var(--muted)}.stat strong{font-size:28px;color:var(--gold);display:block;margin-top:7px}.actions{display:flex;gap:9px;flex-wrap:wrap;align-items:center}button,.button{border:1px solid #c49a5d;border-radius:8px;padding:10px 14px;background:linear-gradient(100deg,#9b6b3c,#ead09a);color:#17100b;font-weight:700;cursor:pointer;text-decoration:none}button.secondary{background:#172235;color:#dce8f4;border-color:#38506b}input,textarea,select{width:100%;max-width:100%;padding:11px 12px;margin:7px 0 12px;border-radius:9px;background:#091321;color:#fff;border:1px solid #344b69}label{display:block;color:#e8dfd1}table{width:100%;border-collapse:collapse;min-width:700px}th,td{text-align:left;padding:11px 9px;border-bottom:1px solid #ffffff18;vertical-align:top}th{color:var(--gold);font-size:12px}.table-wrap{overflow:auto}.pill{font-size:11px;border:1px solid #567;border-radius:20px;padding:4px 8px}.paid{color:#8dd8b6;border-color:#477b60}.open{color:#f0cb7a;border-color:#8b7043}.notice{border:1px solid #655338;padding:12px;border-radius:10px;color:#d9c79f;background:#251e16}
</style></head><body><main><div class="brand">ULTIMA NETWORK · FINANCE CONTROL</div>
<div class="head"><div><h1>Commerce & Rechnungen</h1><div class="muted">Bestellungen, Checkout-Aktivität und zentrale Rechnungsübersicht</div></div><a class="button" href="/">Zum ULTIMA Portal</a></div>
<div class="grid"><div class="stat"><small>Checkouts gestartet</small><strong id="checkouts">—</strong></div><div class="stat"><small>Bestellungen erfasst</small><strong id="orders">—</strong></div><div class="stat"><small>Checkout-Konversion</small><strong id="conversion">—</strong></div><div class="stat"><small>Offene Rechnungen</small><strong id="open-count">—</strong></div><div class="stat"><small>Offener Rechnungsbetrag</small><strong id="open-total">—</strong></div><div class="stat"><small>Als bezahlt markiert</small><strong id="paid-total">—</strong></div></div>
<section class="panel"><h2>Rechnung hinzufügen · PDF oder Bild</h2><p class="muted">PDF-Dateien und Bilder werden im Browser ausgelesen. Die Originaldatei wird nicht an den Server übertragen. Prüfe erkannte Angaben vor dem Speichern.</p>
<div class="grid"><div><label>Datei auswählen</label><input id="file" type="file" accept="application/pdf,image/*"></div><div><label>Rechnungssteller</label><input id="vendor" placeholder="Firma / Lieferant"></div><div><label>Rechnungsnummer</label><input id="number" placeholder="Rechnungsnummer"></div><div><label>Betrag</label><input id="amount" type="number" min="0" step="0.01" placeholder="0,00"></div><div><label>Währung</label><select id="currency"><option>EUR</option><option>USD</option><option>CHF</option><option>GBP</option></select></div><div><label>Fällig am</label><input id="due" type="date"></div></div>
<label>Notiz</label><textarea id="notes" rows="2"></textarea><div class="actions"><button id="extract">Datei auslesen</button><button id="save">Rechnung speichern</button><span class="muted" id="status"></span></div></section>
<section class="panel" style="margin-top:16px"><div class="head"><h2>Alle Rechnungen</h2><button class="secondary" id="refresh">Aktualisieren</button></div><div class="table-wrap"><table><thead><tr><th>Rechnung</th><th>Lieferant</th><th>Betrag</th><th>Fälligkeit</th><th>Status</th><th>Aktion</th></tr></thead><tbody id="invoices"></tbody></table></div></section>
<section class="panel" style="margin-top:16px"><h2>Shop- und Checkout-Aktivität</h2><p class="muted">Gezählt werden nur Ereignisse, die Shops über die ULTIMA-Commerce-API übermitteln. Noch nicht angebundene Shops erscheinen nicht automatisch.</p><div class="table-wrap"><table><thead><tr><th>Website / Shop</th><th>Checkouts</th><th>Bestellungen</th><th>Erfasster Umsatz</th></tr></thead><tbody id="sites"></tbody></table></div><div class="notice">Integrations-Endpunkt: <code>POST /api/commerce/events</code> · Header <code>X-ULTIMA-Commerce-Key</code> · Event-Typen: <code>checkout_started</code>, <code>order_created</code>, <code>order_paid</code>. Den geheimen Schlüssel niemals im Browser veröffentlichen.</div></section></main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script><script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script><script>
const $=id=>document.getElementById(id);let filename="";
const money=(n,c)=>new Intl.NumberFormat("de-DE",{style:"currency",currency:c||"EUR"}).format(Number(n||0));
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
async function api(url,opts={}){const r=await fetch(url,{credentials:"same-origin",headers:{"Content-Type":"application/json"},...opts});const d=await r.json().catch(()=>({}));if(!r.ok)throw Error(d.error||"Anfrage fehlgeschlagen");return d}
function parseText(t){const s=t.replace(/\s+/g," ");const no=(s.match(/(?:Rechnungs(?:nummer|nr\.?|\s*#)|Invoice\s*(?:No\.?|Number)?|Belegnummer)\s*[:#-]?\s*([A-Z0-9\-/]+)/i)||[])[1];let a=(s.match(/(?:Gesamtbetrag|Rechnungsbetrag|Endbetrag|Total|Summe|zu zahlen|amount due)[^\d]{0,25}([0-9][0-9. ]*(?:,[0-9]{2}|\.[0-9]{2}))/i)||[])[1];if(a)a=a.replace(/\./g,"").replace(",",".").replace(/\s/g,"");return {no,a}}
async function extractFile(f){if(f.type==="application/pdf"){const pdf=await pdfjsLib.getDocument({data:await f.arrayBuffer()}).promise;let t="";for(let p=1;p<=Math.min(pdf.numPages,20);p++){const page=await pdf.getPage(p);const c=await page.getTextContent();t+=c.items.map(x=>x.str).join(" ")+"\n"}return t}return (await Tesseract.recognize(f,"deu+eng")).data.text}
$("extract").onclick=async()=>{const f=$("file").files[0];if(!f){$("status").textContent="Bitte eine PDF- oder Bilddatei auswählen.";return}filename=f.name;$("status").textContent="Lese Datei lokal aus …";try{const p=parseText(await extractFile(f));if(p.no)$("number").value=p.no;if(p.a)$("amount").value=p.a;$("status").textContent="Auslesen fertig. Angaben bitte prüfen."}catch(e){$("status").textContent="Auslesen fehlgeschlagen: "+e.message}}
$("save").onclick=async()=>{const n=Number($("amount").value);if(!Number.isFinite(n)||n<0){$("status").textContent="Bitte gültigen Betrag eintragen.";return}try{await api("/api/admin/commerce/invoices",{method:"POST",body:JSON.stringify({invoice_number:$("number").value,vendor:$("vendor").value,amount:n,currency:$("currency").value,due_date:$("due").value,source_filename:filename,notes:$("notes").value})});$("status").textContent="Rechnung gespeichert.";["vendor","number","amount","due","notes","file"].forEach(k=>$(k).value="");filename="";await refresh()}catch(e){$("status").textContent=e.message}}
async function refresh(){try{const d=await api("/api/admin/commerce/summary");$("checkouts").textContent=d.checkouts;$("orders").textContent=d.orders;$("conversion").textContent=d.conversion+"%";$("open-count").textContent=d.open_count;$("open-total").textContent=money(d.open_total);$("paid-total").textContent=money(d.paid_total);$("sites").innerHTML=d.sites.map(s=>"<tr><td>"+esc(s.site)+"</td><td>"+s.checkouts+"</td><td>"+s.orders+"</td><td>"+money(s.revenue,s.currency)+"</td></tr>").join("")||'<tr><td colspan="4">Noch keine Shop-Ereignisse erfasst.</td></tr>';const x=await api("/api/admin/commerce/invoices");$("invoices").innerHTML=x.invoices.map(i=>"<tr><td>"+esc(i.invoice_number||"—")+"<br><small>"+esc(i.source_filename||"")+"</small></td><td>"+esc(i.vendor||"—")+"</td><td>"+money(i.amount,i.currency)+"</td><td>"+esc(i.due_date||"—")+"</td><td><span class='pill "+(i.status==="paid"?"paid":"open")+"'>"+(i.status==="paid"?"Bezahlt":"Offen")+"</span></td><td>"+(i.status==="paid"?"—":"<button data-paid='"+i.id+"'>Gezahlt</button>")+"</td></tr>").join("")||'<tr><td colspan="6">Noch keine Rechnungen gespeichert.</td></tr>';document.querySelectorAll("[data-paid]").forEach(b=>b.onclick=async()=>{if(confirm("Rechnung als bezahlt markieren?")){await api("/api/admin/commerce/invoices/"+b.dataset.paid,{method:"PATCH",body:JSON.stringify({status:"paid"})});await refresh()}})}catch(e){$("invoices").innerHTML="<tr><td colspan='6'>"+esc(e.message)+"</td></tr>"}}
$("refresh").onclick=refresh;refresh();
</script></body></html>"""

def register_commerce_admin(app, db, require_superadmin):
    class CommerceEvent(db.Model):
        __tablename__ = "ultima_commerce_event"
        id = db.Column(db.Integer, primary_key=True)
        event_id = db.Column(db.String(120), unique=True, nullable=True, index=True)
        site = db.Column(db.String(120), nullable=False, index=True)
        event_type = db.Column(db.String(40), nullable=False, index=True)
        order_id = db.Column(db.String(120), nullable=True, index=True)
        amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
        currency = db.Column(db.String(8), nullable=False, default="EUR")
        created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    class InvoiceRecord(db.Model):
        __tablename__ = "ultima_invoice_record"
        id = db.Column(db.Integer, primary_key=True)
        invoice_number = db.Column(db.String(120), nullable=False, default="")
        vendor = db.Column(db.String(180), nullable=False, default="")
        amount = db.Column(db.Numeric(12, 2), nullable=False)
        currency = db.Column(db.String(8), nullable=False, default="EUR")
        due_date = db.Column(db.String(20), nullable=False, default="")
        status = db.Column(db.String(20), nullable=False, default="open", index=True)
        source_filename = db.Column(db.String(255), nullable=False, default="")
        notes = db.Column(db.Text, nullable=False, default="")
        created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
        paid_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def admin_ok():
        return require_superadmin() is not None

    @app.get("/admin/commerce/")
    def commerce_admin_page():
        if not admin_ok(): return redirect("/")
        response = Response(PAGE, mimetype="text/html")
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/api/admin/commerce/summary")
    def commerce_summary():
        if not admin_ok(): return jsonify(error="superadmin_required"), 403
        checkouts = CommerceEvent.query.filter_by(event_type="checkout_started").count()
        orders = CommerceEvent.query.filter(CommerceEvent.event_type.in_(["order_created","order_paid"])).count()
        opened = InvoiceRecord.query.filter_by(status="open").all()
        paid = InvoiceRecord.query.filter_by(status="paid").all()
        open_total = sum((Decimal(str(x.amount)) for x in opened), Decimal("0"))
        paid_total = sum((Decimal(str(x.amount)) for x in paid), Decimal("0"))
        rows = db.session.query(CommerceEvent.site, CommerceEvent.currency,
            func.sum(case((CommerceEvent.event_type=="checkout_started",1),else_=0)),
            func.sum(db.case((CommerceEvent.event_type.in_(["order_created","order_paid"]),1),else_=0)),
            func.sum(CommerceEvent.amount)).group_by(CommerceEvent.site,CommerceEvent.currency).all()
        sites=[{"site":r[0],"currency":r[1],"checkouts":int(r[2] or 0),"orders":int(r[3] or 0),"revenue":float(r[4] or 0)} for r in rows]
        return jsonify(checkouts=checkouts,orders=orders,conversion=round(orders/checkouts*100,1) if checkouts else 0,open_count=len(opened),open_total=float(open_total),paid_total=float(paid_total),sites=sites)

    @app.route("/api/admin/commerce/invoices",methods=["GET","POST"])
    def commerce_invoices():
        if not admin_ok(): return jsonify(error="superadmin_required"),403
        if request.method=="GET":
            rows=InvoiceRecord.query.order_by(InvoiceRecord.created_at.desc()).limit(500).all()
            return jsonify(invoices=[{"id":x.id,"invoice_number":x.invoice_number,"vendor":x.vendor,"amount":float(x.amount),"currency":x.currency,"due_date":x.due_date,"status":x.status,"source_filename":x.source_filename,"notes":x.notes} for x in rows])
        data=request.get_json(silent=True) or {}
        try:
            amount=Decimal(str(data.get("amount","")))
            if not amount.is_finite() or amount<0 or amount>Decimal("999999999"): raise InvalidOperation()
        except (InvalidOperation,ValueError): return jsonify(error="Ungültiger Rechnungsbetrag."),400
        currency=str(data.get("currency","EUR")).upper()
        if currency not in {"EUR","USD","CHF","GBP"}: return jsonify(error="Nicht unterstützte Währung."),400
        row=InvoiceRecord(invoice_number=str(data.get("invoice_number",""))[:120],vendor=str(data.get("vendor",""))[:180],amount=amount,currency=currency,due_date=str(data.get("due_date",""))[:20],source_filename=str(data.get("source_filename",""))[:255],notes=str(data.get("notes",""))[:4000])
        db.session.add(row);db.session.commit()
        return jsonify(id=row.id,status=row.status),201

    @app.patch("/api/admin/commerce/invoices/<int:invoice_id>")
    def update_commerce_invoice(invoice_id):
        if not admin_ok(): return jsonify(error="superadmin_required"),403
        row=db.session.get(InvoiceRecord,invoice_id)
        if not row:return jsonify(error="Rechnung nicht gefunden."),404
        status=(request.get_json(silent=True) or {}).get("status")
        if status not in {"open","paid"}:return jsonify(error="Ungültiger Rechnungsstatus."),400
        row.status=status;row.paid_at=datetime.now(timezone.utc) if status=="paid" else None
        db.session.commit()
        return jsonify(id=row.id,status=row.status)

    @app.post("/api/commerce/events")
    def ingest_commerce_event():
        expected=os.environ.get("ULTIMA_COMMERCE_WEBHOOK_SECRET","").strip()
        supplied=request.headers.get("X-ULTIMA-Commerce-Key","")
        if not expected or not supplied or not hmac.compare_digest(expected,supplied):return jsonify(error="unauthorized"),401
        data=request.get_json(silent=True) or {}
        site=str(data.get("site","")).strip()[:120];kind=str(data.get("event_type","")).strip()
        if not site or kind not in {"checkout_started","order_created","order_paid","cart_updated"}:return jsonify(error="invalid_event"),400
        event_id=str(data.get("event_id","")).strip()[:120] or None
        if event_id and CommerceEvent.query.filter_by(event_id=event_id).first():return jsonify(ok=True,duplicate=True),200
        try:
            amount=Decimal(str(data.get("amount",0)))
            if not amount.is_finite() or amount<0 or amount>Decimal("999999999"):raise InvalidOperation()
        except (InvalidOperation,ValueError):return jsonify(error="invalid_amount"),400
        currency=str(data.get("currency","EUR")).upper()
        if currency not in {"EUR","USD","CHF","GBP"}:return jsonify(error="invalid_currency"),400
        db.session.add(CommerceEvent(event_id=event_id,site=site,event_type=kind,order_id=str(data.get("order_id",""))[:120] or None,amount=amount,currency=currency))
        db.session.commit()
        return jsonify(ok=True),201

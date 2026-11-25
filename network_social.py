from datetime import datetime, timezone
from flask import Blueprint, jsonify, request, session, render_template_string
social=Blueprint("social_network",__name__,url_prefix="/network")
def register_social(app,db,User):
 class Profile(db.Model):
  id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey("user.id"),unique=True,nullable=False)
  name=db.Column(db.String(80),default=""); bio=db.Column(db.String(500),default=""); interests=db.Column(db.String(500),default="")
 class Post(db.Model):
  id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False,index=True)
  body=db.Column(db.String(3000),nullable=False); created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
 class Message(db.Model):
  id=db.Column(db.Integer,primary_key=True); sender_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
  recipient_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False); body=db.Column(db.String(4000),nullable=False)
  created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
 class MentorRequest(db.Model):
  id=db.Column(db.Integer,primary_key=True); requester_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
  mentor_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False); message=db.Column(db.String(1500),default="")
  status=db.Column(db.String(20),default="pending"); created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
 def current():
  uid=session.get("user_id"); return db.session.get(User,uid) if uid else None
 def data(u):
  p=Profile.query.filter_by(user_id=u.id).first()
  return {"id":u.id,"name":p.name if p and p.name else u.email.split("@")[0],"bio":p.bio if p else "","interests":p.interests if p else "","role":u.role}
 @social.get("/")
 def home():
  if not current(): return "<p>Bitte zuerst <a href='/'>bei ULTIMA anmelden</a>.</p>",401
  return render_template_string("""<!doctype html><html lang=de><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>ULTIMA Social</title><style>
  body{margin:0;background:#080d18;color:#f3f6fb;font:15px system-ui}header{padding:18px;background:#111b2d;border-bottom:1px solid #263750;color:#e7c879}main{max-width:1000px;margin:25px auto;padding:16px}.grid{display:grid;grid-template-columns:220px 1fr;gap:15px}.card{background:#111b2d;border:1px solid #263750;border-radius:16px;padding:18px;margin-bottom:14px}button{padding:10px 14px;border:0;border-radius:9px;background:#e7c879;font-weight:bold;margin:4px;cursor:pointer}input,textarea{width:100%;padding:11px;background:#091321;color:white;border:1px solid #263750;border-radius:9px;margin:6px 0}.muted{color:#a8b5c9;font-size:13px}.hidden{display:none}.post{border-top:1px solid #263750;padding:12px 0}@media(max-width:700px){.grid{grid-template-columns:1fr}}</style><header>ULTIMA · SOCIAL NETWORK <a href='/' style='float:right;color:#5ce1e6'>ULTIMA</a></header><main><h1>Dein Netzwerk</h1><p class=muted>Ein Profil für alle verbundenen Websites · Community · Messenger · Mentoren</p><nav><button onclick="tab('feed')">Community</button><button onclick="tab('msg')">Messenger</button><button onclick="tab('mentor')">Mentoren</button><button onclick="tab('profile')">Profil</button></nav><div class=grid><aside><section class=card><h3 id=myname>Profil</h3><p class=muted>Dein zentrales Netzwerkprofil</p></section><section class=card><p class=muted>Private Nachrichten sind nur für Sender und Empfänger sichtbar. Mentoren werden vom Superadmin freigeschaltet.</p></section></aside><section>
  <div id=feed><section class=card><h3>Beitrag veröffentlichen</h3><textarea id=postbody maxlength=3000></textarea><button onclick=publish()>Posten</button></section><section class=card><h3>Community-Feed</h3><div id=posts></div></section></div>
  <div id=msg class='hidden card'><h3>Messenger</h3><label>Empfänger-ID</label><input id=recipient type=number><div id=thread></div><textarea id=msgbody maxlength=4000></textarea><button onclick=sendmsg()>Senden</button></div>
  <div id=mentor class='hidden card'><h3>Mentoranfragen</h3><div id=mentors></div><textarea id=mentorbody maxlength=1500 placeholder='Deine Anfrage'></textarea><button onclick=requestmentor()>Anfrage senden</button><div id=mentorstatus></div><h3>Erhaltene Anfragen</h3><div id=requestlist></div></div>
  <div id=profile class='hidden card'><h3>Profil bearbeiten</h3><label>Anzeigename</label><input id=displayname><label>Über mich</label><textarea id=bio maxlength=500></textarea><label>Interessen</label><input id=interests><button onclick=saveprofile()>Speichern</button><div id=profilestatus></div></div>
  </section></div></main><script>
  const csrf='{{ csrf_token() }}';async function api(p,m='GET',b){let r=await fetch('/network/api/'+p,{method:m,headers:{'Content-Type':'application/json','X-CSRFToken':csrf},body:b?JSON.stringify(b):undefined});let d=await r.json();if(!r.ok)throw Error(d.error||'Fehler');return d}
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function tab(id){['feed','msg','mentor','profile'].forEach(x=>document.getElementById(x).classList.toggle('hidden',x!==id))}
  async function load(){try{let d=await api('me');myname.textContent=d.profile.name;displayname.value=d.profile.name;bio.value=d.profile.bio;interests.value=d.profile.interests;await loadposts();await loadmentors();await loadrequests()}catch(e){alert(e.message)}}
  async function loadposts(){let d=await api('posts');posts.innerHTML=d.posts.map(x=>'<div class=post><b>'+esc(x.name)+'</b><p>'+esc(x.body)+'</p><small class=muted>'+new Date(x.created_at).toLocaleString()+'</small></div>').join('')||'Noch keine Beiträge.'}
  async function publish(){try{await api('posts','POST',{body:postbody.value});postbody.value='';loadposts()}catch(e){alert(e.message)}}
  async function saveprofile(){try{let d=await api('me','PUT',{name:displayname.value,bio:bio.value,interests:interests.value});myname.textContent=d.profile.name;profilestatus.textContent='Gespeichert.'}catch(e){profilestatus.textContent=e.message}}
  async function loadmentors(){let d=await api('mentors');mentors.innerHTML=d.mentors.map(x=>'<div class=post><b>'+esc(x.name)+'</b> · Mentor ID '+x.id+'<p>'+esc(x.bio)+'</p></div>').join('')||'Noch keine Mentorprofile.'}
  async function requestmentor(){try{let d=await api('mentor-requests','POST',{mentor_id:Number(recipient.value),message:mentorbody.value});mentorstatus.textContent=d.message}catch(e){mentorstatus.textContent=e.message}}
  async function loadrequests(){let d=await api('mentor-requests');requestlist.innerHTML=d.requests.map(x=>'<div class=post>'+esc(x.requester)+': '+esc(x.message)+' · '+esc(x.status)+(x.can_review&&x.status==='pending'?' <button onclick="review('+x.id+',\'accepted\')">Annehmen</button> <button onclick="review('+x.id+',\'rejected\')">Ablehnen</button>':'')+'</div>').join('')||'Keine Anfragen.'}
  async function review(id,decision){try{await api('mentor-requests/'+id,'PATCH',{decision});loadrequests();loadmentors()}catch(e){alert(e.message)}}
  async function sendmsg(){try{await api('messages','POST',{recipient_id:Number(recipient.value),body:msgbody.value});msgbody.value='';loadthread()}catch(e){alert(e.message)}}
  async function loadthread(){try{let d=await api('messages?with='+recipient.value);thread.innerHTML=d.messages.map(x=>'<div class=post>'+esc(x.body)+'</div>').join('')}catch(e){alert(e.message)}}
  recipient.addEventListener('change',loadthread);load();
  </script></html>""")
 @social.get("/api/me")
 def getme():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  return jsonify(profile=data(u))
 @social.put("/api/me")
 def putme():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  d=request.get_json(silent=True) or {};p=Profile.query.filter_by(user_id=u.id).first() or Profile(user_id=u.id)
  p.name=str(d.get("name") or "").strip()[:80];p.bio=str(d.get("bio") or "").strip()[:500];p.interests=str(d.get("interests") or "").strip()[:500]
  db.session.add(p);db.session.commit();return jsonify(profile=data(u))
 @social.get("/api/posts")
 def getposts():
  if not current():return jsonify(error="authentication_required"),401
  rows=Post.query.order_by(Post.created_at.desc()).limit(60).all()
  return jsonify(posts=[{"id":p.id,"name":data(db.session.get(User,p.user_id))["name"],"body":p.body,"created_at":p.created_at.isoformat()} for p in rows])
 @social.post("/api/posts")
 def addpost():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  body=str((request.get_json(silent=True) or {}).get("body") or "").strip()
  if not body or len(body)>3000:return jsonify(error="Beitrag muss 1-3.000 Zeichen enthalten."),400
  p=Post(user_id=u.id,body=body);db.session.add(p);db.session.commit();return jsonify(ok=True),201
 @social.get("/api/mentors")
 def getmentors():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  return jsonify(mentors=[data(x) for x in User.query.filter(User.role.in_(["MENTOR","SUPERADMIN"])).all() if x.id!=u.id])
 @social.post("/api/mentor-requests")
 def addmentor():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  d=request.get_json(silent=True) or {};m=db.session.get(User,d.get("mentor_id"))
  if not m or m.role not in ("MENTOR","SUPERADMIN") or m.id==u.id:return jsonify(error="Mentorprofil nicht gefunden."),404
  x=MentorRequest(requester_id=u.id,mentor_id=m.id,message=str(d.get("message") or "")[:1500]);db.session.add(x);db.session.commit()
  return jsonify(message="Mentoranfrage übermittelt."),201
 @social.get("/api/mentor-requests")
 def mentorlist():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  rows=MentorRequest.query.filter((MentorRequest.mentor_id==u.id)|(MentorRequest.requester_id==u.id)).order_by(MentorRequest.created_at.desc()).limit(50).all()
  return jsonify(requests=[{"id":x.id,"requester":data(db.session.get(User,x.requester_id))["name"],"message":x.message,"status":x.status,"can_review":x.mentor_id==u.id and u.role in ("MENTOR","SUPERADMIN")} for x in rows])
 @social.patch("/api/mentor-requests/<int:rid>")
 def decide(rid):
  u=current();x=db.session.get(MentorRequest,rid)
  if not u:return jsonify(error="authentication_required"),401
  if not x or x.mentor_id!=u.id or u.role not in ("MENTOR","SUPERADMIN"):return jsonify(error="forbidden"),403
  d=str((request.get_json(silent=True) or {}).get("decision") or "")
  if d not in ("accepted","rejected") or x.status!="pending":return jsonify(error="invalid_decision"),400
  x.status=d;db.session.commit();return jsonify(ok=True)
 @social.get("/api/messages")
 def getmessages():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  other=request.args.get("with",type=int)
  if not other or other==u.id:return jsonify(error="recipient_required"),400
  rows=Message.query.filter(((Message.sender_id==u.id)&(Message.recipient_id==other))|((Message.sender_id==other)&(Message.recipient_id==u.id))).order_by(Message.created_at.asc()).limit(200).all()
  return jsonify(messages=[{"body":x.body,"mine":x.sender_id==u.id,"created_at":x.created_at.isoformat()} for x in rows])
 @social.post("/api/messages")
 def sendmessages():
  u=current()
  if not u:return jsonify(error="authentication_required"),401
  d=request.get_json(silent=True) or {};other=db.session.get(User,d.get("recipient_id"));body=str(d.get("body") or "").strip()
  if not other or other.id==u.id:return jsonify(error="Empfänger nicht gefunden."),404
  if not body or len(body)>4000:return jsonify(error="Nachricht muss 1-4.000 Zeichen enthalten."),400
  x=Message(sender_id=u.id,recipient_id=other.id,body=body);db.session.add(x);db.session.commit();return jsonify(ok=True),201
 app.register_blueprint(social)

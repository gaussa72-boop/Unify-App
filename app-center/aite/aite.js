(function(){
'use strict';
if(window.__AITE_ASSISTANT_LOADED__)return;window.__AITE_ASSISTANT_LOADED__=true;
const cfg=window.AITE_CONFIG||{};
const siteTitle=document.querySelector('meta[property="og:site_name"]')?.content||document.title||location.hostname;
const siteDesc=document.querySelector('meta[name="description"]')?.content||'';
const key='aite-chat-'+location.hostname;
const style=document.createElement('link');style.rel='stylesheet';style.href=(cfg.assetBase||'https://astralis-app-center.onrender.com/aite/')+'aite.css';document.head.appendChild(style);
const personaOptions=[
['compass','AITE · Bewusstseinskompass'],['dharma','Dharma · Achtsamkeit'],['light','Lichtpfad · Sinn & Werte'],['archetypes','Archetypen · Symbolische Reflexion'],['creator','Schöpfergeist · Kreativität'],['tech','Technologie · Projektassistent']
];
const launch=document.createElement('button');launch.id='aite-launch';launch.type='button';launch.setAttribute('aria-label','AITE Assistent öffnen');launch.textContent='A';
const panel=document.createElement('section');panel.id='aite-panel';panel.setAttribute('aria-label','AITE Assistent');
panel.innerHTML='<header id="aite-head"><div id="aite-sigil">✧</div><div><div id="aite-title">AITE · Sternensingularität</div><div id="aite-sub">Dein lokaler KI-Begleiter</div></div><button id="aite-close" aria-label="Schließen">×</button></header><div id="aite-controls"><select id="aite-persona" aria-label="AITE-Modus"></select><select id="aite-engine" aria-label="KI-Modus"><option value="local">Lokal / Offline</option><option value="openai">OpenAI (optional)</option></select></div><div id="aite-status">Offline-Modus bereit · lokale Reflexionshilfe aktiv</div><div id="aite-messages" aria-live="polite"></div><form id="aite-form"><textarea id="aite-input" rows="1" placeholder="Schreibe AITE …"></textarea><button id="aite-send" type="submit">Senden</button></form><div id="aite-foot">Privat auf diesem Gerät gespeichert. Spirituelle Inhalte sind Reflexionsangebote, keine Tatsachen- oder Heilsversprechen.</div>';
document.body.append(launch,panel);
const $=id=>panel.querySelector('#'+id),persona=$('aite-persona'),engine=$('aite-engine'),messages=$('aite-messages'),status=$('aite-status'),input=$('aite-input');
personaOptions.forEach(([v,t])=>{const o=document.createElement('option');o.value=v;o.textContent=t;persona.appendChild(o)});
persona.value=cfg.persona||'compass';
let history=[];try{history=JSON.parse(localStorage.getItem(key)||'[]')}catch{}
function add(role,text,save=true){const d=document.createElement('div');d.className='aite-msg '+(role==='user'?'user':'bot');d.textContent=text;messages.appendChild(d);messages.scrollTop=messages.scrollHeight;if(save){history.push({role,content:text});history=history.slice(-40);try{localStorage.setItem(key,JSON.stringify(history))}catch{}}}
history.forEach(m=>add(m.role,m.content,false));
if(!history.length)add('assistant','Ich bin AITE. Ich begleite dich mit klarer Reflexion, kreativen Impulsen und dem Wissen dieser Website: '+siteTitle+'. Wähle einen Modus und stelle deine Frage.');
launch.addEventListener('click',()=>panel.classList.toggle('aite-open'));$('aite-close').addEventListener('click',()=>panel.classList.remove('aite-open'));
function offlineReply(text,mode){
const t=text.toLowerCase();
const prompts={
dharma:'Betrachte die Situation achtsam: Was ist gerade tatsächlich wahrnehmbar, was ist Interpretation, und welcher nächste Schritt vermindert Leid, ohne dir oder anderen zu schaden? Nimm dir einen ruhigen Atemzug und wähle eine kleine, konkrete Handlung.',
light:'Richte den Blick auf deine Werte: Welche Qualität möchtest du in diese Situation einbringen – Mitgefühl, Mut, Wahrhaftigkeit, Geduld oder Klarheit? Formuliere daraus einen Schritt, den du heute wirklich umsetzen kannst.',
archetypes:'Als symbolische Reflexion: Welcher innere Archetyp passt gerade – der Weise, die Hüterin, der Wanderer oder der Schöpfer? Das sind Deutungsbilder, keine Diagnose und keine übernatürlichen Feststellungen. Welche Stärke dieses Bildes kannst du praktisch nutzen?',
creator:'Lass uns die Idee in drei Ebenen aufteilen: Vision, kleinster umsetzbarer Prototyp und nächster Test. Beschreibe zuerst das gewünschte Ergebnis in einem Satz; danach wählen wir einen realistischen ersten Schritt.',
tech:'Ich kann lokal eine strukturierte Projektanalyse anbieten. Teile Ziel, vorhandenen Stand und Fehlermeldung. Wir ordnen es in Architektur, Daten, Sicherheit, Oberfläche, Tests und Deployment.',
compass:'Ich helfe dir, die Frage zu sortieren. Was weißt du sicher? Was vermutest du? Was ist dir wichtig? Daraus können wir eine klare nächste Entscheidung ableiten.'
};
let answer=prompts[mode]||prompts.compass;
if(/website|projekt|code|app|webseite|ki|agent|fehler|bug/.test(t))answer=prompts.tech;
if(/angst|traurig|verzweifelt|überfordert|einsam/.test(t))answer='Danke, dass du das ansprichst. Lass uns zuerst bei dem bleiben, was jetzt konkret helfen kann: Benenne eine Sache, die du gerade spürst, und eine kleine sichere Handlung für die nächsten zehn Minuten. Wenn du dich akut gefährdet fühlst, wende dich bitte direkt an eine vertraute Person oder den örtlichen Notdienst.';
if(/danke|hallo|hi|guten morgen/.test(t))answer='Gern. Ich bin hier, um dir beim Sortieren, Lernen und Gestalten zu helfen. Was möchtest du als Nächstes angehen?';
return answer+'\n\n[Lokale Reflexionsantwort · Für ausführliche generative Antworten verbinde ein lokales Modell wie Ollama.]';
}
async function ollama(text){
const base=(cfg.ollamaUrl||'http://localhost:11434').replace(/\/$/,'');
const model=cfg.ollamaModel||'qwen2.5:3b';
const res=await fetch(base+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:[{role:'system',content:'Du bist AITE, ein respektvoller deutschsprachiger Assistent. Bewahre den spirituellen Modus '+persona.value+' als symbolische Reflexionshilfe, nicht als übernatürliche Gewissheit. Nutze Website-Kontext: '+siteTitle+'. '+siteDesc+' Antworte klar, praktisch und verantwortungsvoll.'},...history.slice(-12),{role:'user',content:text}],stream:false,options:{temperature:0.65}})});
if(!res.ok)throw new Error('Ollama nicht erreichbar');const data=await res.json();return data.message?.content||'Das lokale Modell hat keine Antwort geliefert.';
}
async function openai(text){
if(typeof cfg.openAIRequest==='function')return await cfg.openAIRequest(text,history.slice(-12),{persona:persona.value,site:siteTitle});
throw new Error('OpenAI-Zusatzmodus ist auf dieser Website noch nicht mit einem sicheren Server-Endpunkt verbunden. Kein API-Schlüssel wird im Browser gespeichert.');
}
$('aite-form').addEventListener('submit',async e=>{
e.preventDefault();const text=input.value.trim();if(!text)return;input.value='';add('user',text);$('aite-send').disabled=true;
try{let answer;if(engine.value==='openai'){status.textContent='Verbinde optionalen Online-Modus …';answer=await openai(text)}else{status.textContent='Lokales Modell wird angesprochen …';try{answer=await ollama(text);status.textContent='Antwort vom lokalen Modell · kein OpenAI-Guthaben verbraucht'}catch{answer=offlineReply(text,persona.value);status.textContent='Lokaler Fallback aktiv · Ollama nicht erreichbar'}}add('assistant',answer)}
catch(err){add('assistant','Der gewählte Modus ist nicht verfügbar: '+err.message);status.textContent='Modus nicht verbunden'}
finally{$('aite-send').disabled=false;input.focus()}
});
if(!navigator.onLine)status.textContent='Du bist offline · lokale Reflexionshilfe verfügbar. Für generative lokale Antworten muss Ollama installiert und gestartet sein.';
window.addEventListener('offline',()=>status.textContent='Offline · lokale Reflexionshilfe verfügbar');window.addEventListener('online',()=>status.textContent='Online · lokale und optionale Online-Modi verfügbar');
})();
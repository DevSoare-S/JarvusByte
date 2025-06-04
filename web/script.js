async function enviar(){
 const q=document.getElementById('pergunta').value;
 if(!q) return;
 const r=await fetch('/perguntar?q='+encodeURIComponent(q));
 const d=await r.json();
 const div=document.getElementById('conversa');
 div.innerHTML+=`<p><strong>Você:</strong> ${q}</p><p><strong>JarvucasIA:</strong> ${d.resposta}</p>`;
 document.getElementById('pergunta').value='';
}

async function ativarVoz(){
 await fetch('/ativar_voz');
}

async function mostrarProposito(){
 const t=await (await fetch('/proposito')).text();
 document.getElementById('proposito').innerText=t;
}

document.getElementById('enviar').onclick=enviar;
document.getElementById('ativar').onclick=ativarVoz;
mostrarProposito();

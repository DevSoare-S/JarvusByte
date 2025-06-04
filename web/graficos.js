async function carregarGrafico(){
 const r=await fetch('/evolucao');
 const d=await r.json();
 const ctx=document.getElementById('grafico').getContext('2d');
 const labels=Object.keys(d);
 const data=Object.values(d);
 new Chart(ctx,{type:'bar',data:{labels,datasets:[{label:'Evolucao',data}]}});
}
carregarGrafico();


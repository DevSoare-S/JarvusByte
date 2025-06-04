function ativar(){fetch('/ativar_voz');}
function estudar(){const t=prompt('Tema?');if(t)fetch('/estudar?t='+encodeURIComponent(t));}
document.getElementById('ativar').onclick=ativar;
document.getElementById('estudar').onclick=estudar;


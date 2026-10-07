function toggleSidebar(){document.getElementById('sidebar')?.classList.toggle('open')}
function confirmAction(message){return window.confirm(message||'Are you sure?')}
document.addEventListener('click',e=>{const el=e.target.closest('[data-confirm]');if(el&&!confirmAction(el.dataset.confirm))e.preventDefault()});
document.querySelectorAll('.map .pin[data-left][data-top]').forEach(pin=>{
    const left=Number(pin.dataset.left);
    const top=Number(pin.dataset.top);
    if(Number.isFinite(left)&&Number.isFinite(top)){
        pin.style.left=`${left}%`;
        pin.style.top=`${top}%`;
    }
});

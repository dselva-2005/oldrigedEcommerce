
document.addEventListener('DOMContentLoaded',()=>{
    //cancelling dismissable notification/ message
    alerts = Array.from(document.getElementsByClassName('killAlert'))
    alerts.forEach(element => {
        element.onclick = (event) => {
        event.target.parentNode.parentNode.removeChild(event.target.parentNode);
       }
    });
})
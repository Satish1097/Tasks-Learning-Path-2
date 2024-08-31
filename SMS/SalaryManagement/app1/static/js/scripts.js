const openmenu=()=>{
    var x=document.getElementById('menu')
    var icon=document.getElementById('icon')
    if (x.style.left=='-100%'){
    x.style.left="0px";
    icon.className='fa fa-times';
    }
    else{
        x.style.left='-100%'
        icon.className='fa-solid fa-bars-staggered'
    }

    }
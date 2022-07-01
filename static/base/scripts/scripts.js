    var x = document.getElementById("toast")
    var message = document.getElementById("desc")
    x.className = "show";
    message.textContent = "{{ message }}";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
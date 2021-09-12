function search() {
    //$.ajax("http://"+window.location.href.split('/')[2]+"/api/search?query="+encodeURIComponent(document.getElementById("searchbox").value))
    window.location.href="http://"+window.location.href.split('/')[2]+"/search?query="+encodeURIComponent(document.getElementById("searchbox").value)
}
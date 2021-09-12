const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

var h = $.ajax("http://"+window.location.href.split('/')[2]+"/api/get_post", {
    data: {"post": urlParams.get('post')},
    success: function(data){
        //document.getElementById("rawdata").innerHTML = JSON.stringify(data)
        console.log(data)
        document.getElementById("title").appendChild(document.createTextNode(data.name))
        document.getElementById("user").innerHTML = "By <bold>"+data.author.name+"</bold>" // TODO: Make sure no HTML injections are possible here.
        data.chapters.forEach(
            function(chap){
                console.log(urlParams.get("chapter"))
                if (String(chap.id) === urlParams.get("chapter")) {
                    console.log(chap)
                    document.getElementById("text").appendChild(document.createTextNode(chap.text))
                }
            }
        )
    }
})
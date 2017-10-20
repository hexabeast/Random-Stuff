</div>

<div class="foot">
    
</div>


<!-- BULLSHIT -->
<img src="ihouse/ball.png" id="ball">
<script>
    window.addEventListener('keyup', function(event) { Key.onKeyup(event); }, false);
    window.addEventListener('keydown', function(event) { Key.onKeydown(event); }, false);
    window.addEventListener('mousemove', handler, false);
    setInterval(update,15);
</script>
<!-- FIN BULLSHIT -->

</body>


<script>
    function resize(foo)
    {
        wscreen = window.innerWidth;
        content_width = (wscreen - 290);
        //if(content_width < 850)content_width=850;
        document.getElementById("container").style.width = content_width + "px";
    }
    resize();
    window.onresize = resize;

    var imgs = document.getElementsByTagName("img");
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].ondragstart = function() {return false; };
    }
    var as = document.getElementsByTagName("a");
    for (var i = 0; i < as.length; i++) {
        as[i].ondragstart = function() {return false; };
    }
</script>

</html>
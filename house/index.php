<?php $PageTitle="Panneau de contrôle";include_once('header.php');?>

<script>
    var temperature = 24;
    var clim = true;
    var chauffage = true;
    var humidite = 40;
    function changetemp(chg)
    {
        temperature+=chg;
        if(temperature>=40)temperature=40;
        if(temperature<=10)temperature=10;
        updateinterface();
    }
    function swapclim()
    {
        clim=!clim;
        updateinterface();
    }
    function swapchauffage()
    {
        chauffage=!chauffage;
        updateinterface();
    }

    function updateinterface()
    {
        document.getElementById("valhumid").innerHTML = humidite+"%";
        document.getElementById("valtemp").innerHTML = temperature+"°C";

        var img = "poweroff.png";
        if(clim)img = "poweron.png";
        document.getElementById("valclim").src = "ihouse/"+img;

        var img = "poweroff.png";
        if(chauffage)img = "poweron.png";
        document.getElementById("valchauffe").src = "ihouse/"+img;
    }

    function initinterface()
    {
        updateinterface();
    }
</script>

    <div class="columns">
        <ul>
            <li>
                <table class="cpanel" style="width:100%">
                    <tr>
                        <td>
                            <img src="ihouse/thermo.png" class="cpanelimg" >
                            <span class="titletemp">Température :</span>
                            <img src="ihouse/plus.png" class="cpanelimg plus" id="plus1" onclick="changetemp(1)">
                            <span class="valtemp" id ="valtemp">??°C</span>
                            <img src="ihouse/minus.png" class="cpanelimg minus" id="minus1"   onclick="changetemp(-1)">
                        </td>
                    </tr>
                </table>
            </li>
            <li>
                <table class="cpanel" style="width:100%">
                    <tr>
                        <td>
                            <img src="ihouse/radiator.png" class="cpanelimg" >
                            <span class="titletemp">Chauffage :</span>
                            <img src="ihouse/poweroff.png" id="valchauffe" class="cpanelimg power"  onclick="swapchauffage()">
                        </td>
                    </tr>
                </table>
            </li>
            <li>
                <table class="cpanel" style="width:100%">
                    <tr>
                        <td>
                            <img src="ihouse/ventilator.png" class="cpanelimg" >
                            <span class="titletemp">Climatisation :</span>
                            <img src="ihouse/poweron.png" id="valclim" class="cpanelimg power"  onclick="swapclim()">
                        </td>
                    </tr>
                </table>
            </li>
            <li>
                <table class="cpanel" style="width:100%">
                    <tr>
                        <td>
                            <img src="ihouse/water.png" class="cpanelimg" >
                            <span class="titletemp">Humidité :</span>
                            <span class="humid" id ="valhumid">??%</span>
                        </td>
                    </tr>
                </table>
            </li>
            <li>
                <table class="cpanel" style="width:100%">
                    <tr>
                        <td>
                        </td>
                    </tr>
                </table>
            </li>
            <li>
                <table class="cpanel" style="width:100%">
                    <tr>
                        <td>
                        </td>
                    </tr>
                </table>
            </li>
        </ul>
    </div>

<?php include_once('footer.php'); ?>

<script>
    initinterface();
</script>
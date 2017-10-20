<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">  
  <title><?= isset($PageTitle) ? $PageTitle : "iHouse"?></title>
  <link rel="stylesheet" href="style.css">
  <link rel="icon" href="favicon.png" />
</head>

<script type="text/javascript" src="jsutilities.js"></script>

<body>

<div class = "head">
    <a href="index.php"><img id="imghead" src="iHouse.png" align="left" width="300" height="auto"></a>
</div>

<!-- Menu de navigation du site -->
<div class="panel">
    <ul class="navbar">
    <li><a href="index.php"><img src="ihouse/button1.png" class="buttonpanel" width="270" height="auto"></a></li>
    <li><a href="video.php"><img src="ihouse/button2.png" class="buttonpanel" width="270" height="auto"></a></li>
    <li><a href="fichiers.php"><img src="ihouse/button3.png" class="buttonpanel" width="270" height="auto"></a></li>
    <li><a href="parametres.php"><img src="ihouse/button4.png" class="buttonpanel" width="270" height="auto"></a></li>
    </ul>
</div>



<!-- Contenu principal -->
<div id="container">
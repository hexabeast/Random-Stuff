<?php 
$PageTitle="Paramètres";include_once('header.php');?>

<link rel="stylesheet" type="text/css" href="style2.css">

<div class="parametre">
	<div class="subcontainer">

		<?php 
	/*try
	{
		$bdd = new PDO('mysql:host=db701520246.db.1and1.com;dbname=db701520246;charset=utf8', 'dbo701520246', 'ihousebddISEP');
	}
	catch (Exception $e)
	{
		die('Erreur : ' . $e->getMessage());
	}

	$conn = new mysqli('db701520246.db.1and1.com', 'dbo701520246', 'ihousebddISEP', 'db701520246');
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} 
	$sql = "CREATE TABLE parametre (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	passwordhash VARCHAR(30),
	phone INT(10),
	newsletter BOOLEAN not null default 1)";

	if ($conn->query($sql) === TRUE) {
		echo "Table MyGuests created successfully";
	} else {
		echo "Error creating table: " . $conn->error;
	}

	$conn->close();*/
	?>

	<form method="post" id='telephone' action="parametres.php">
		<?php

		function formatFrenchPhoneNumber($telephone, $international = true) { 
			//On supprime tous les caractères qui ne sont pas des chiffres 
			$telephone = preg_replace('/[^0-9]+/', '', $telephone); 
			//On garde les 9 derniers chiffres 
			$telephone = substr($telephone, -9); 
			//On ajoute +33 si la variable $international vaut true et 0 dans tous les autres cas 
			$motif = $international ? '+33 (\1) \2 \3 \4 \5' : '0\1 \2 \3 \4 \5'; 
			$telephone = preg_replace('/(\d{1})(\d{2})(\d{2})(\d{2})(\d{2})/', $motif, $telephone); 

			return $telephone; 
		}

		$telephone = $_POST['phone'];
		if (isset($telephone)) {
			$telephone = htmlspecialchars($telephone);
			$telephone = formatFrenchPhoneNumber($telephone);
			echo "Actuellement votre numéro de téléphone est : <br>".$telephone."<br>";	
		}
		?>

		Modifier le numéro de téléphone associé à votre compte :
		<br>
		<input type="text" name="phone">
		<br>
		<input id="bouton" type="image" src="bouton_modifier.png">
	</form>

	<br>

	<form method="post" id='password' action="parametres.php">
		<?php
		$password_new = htmlspecialchars($_POST['password_new']);
		$password_actu = htmlspecialchars($_POST['password_actu']);
		$password_new2 = htmlspecialchars($_POST['password_new2']);

		echo password_hash("panda", PASSWORD_DEFAULT)."<br><br>";

		$password_enregistre = '$2y$10$vuowmL5s69RxgeXLmQcmJuirBUHFBgi0nqU/NuDSm.XIUNa8fsIoa';

		if (password_verify($password_actu, $password_enregistre) == False) {
			echo '<strong class="error">Le mot de passe ne fonctionne pas !</strong><br>';
		}
		else {
			if (!isset($password_new) || !isset($password_actu) || !isset($password_new2)) {
				echo '<div class="error">Veuillez remplir tous les champs !</div>';
			}
			else {
				if (isset($password_new) && isset($password_new2) && $password_new != $password_new2) {
					echo '<div class="error">Les mots de passe ne correspondent pas !</div>';
				}
				else {
					echo "Mot de passe modifié avec succès !<br>";
				}
			}
		}

		?>				
		Modifier le mot de passe :
		<br>
		Tapez le mot de passe actuel :
		<br>
		<input type="password" name="password_actu">
		<br>
		Tapez votre nouveau mot de passe :<br>
		<input type="password" name="password_new">
		<br>
		Confirmez votre nouveau mot de passe :
		<br>
		<input type="password" name="password_new2">
		<br>
		<input id="bouton" type="image" src="bouton_modifier.png">
	</form>

	<br>

	<form method="post" id='newsletter' action="parametres.php">

		S'abonner à la newsletter iHouse :
		<br>
		<?php
		$newsletter = $_POST['newsletter'];
		if (isset($newsletter)) {
			if ($newsletter != 'no') {
				echo 'Actuellement votre choix est '.$newsletter.".\n".'<br>';
			}
		}
		?>
		<input type="radio" name="newsletter" value="oui" checked>Oui
		<br>
		<input type="radio" name="newsletter" value="non">Non
		<br>
		<input id="bouton" type="image" src="bouton_modifier.png">
	</form>
</div>
</div>
<?php include_once('footer.php'); ?>
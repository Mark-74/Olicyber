<?php
$servername = "db";
$username = "inceptionUSER";
$password = "REDACTED";
$dbname = "inceptionDB";

$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
</head>

<body>
<div style="background: #444">
        <a href="/">
        <img src="/imgs/logo.png" alt="" style="display: block; margin: auto; max-width: 200px; max-height: 300px;">
        </a> 
        <p class="text-center text-white" style="margin-top: -35px;">We loved that movie!</p>
    </div>
<div class="container">
    <div class="">    
    <?php

    function mysql_escape_mimic($inp) {
        if(is_array($inp))
            return array_map(__METHOD__, $inp);

        if(!empty($inp) && is_string($inp)) {
            return str_replace(array('\\', "\0", "\n", "\r", "'", '"', "\x1a"), array('\\\\', '\\0', '\\n', '\\r', "\\'", '\\"', '\\Z'), $inp);
        }

        return $inp;
    } 

    // Voglio evitare sqli a tutti i costi!
    $cur_id = strtoupper($_GET["id"]);
    $cur_id = mysql_escape_mimic($cur_id);
    $cur_id = str_replace(';', '', $cur_id);
    $cur_id = str_replace('X', 'x', $cur_id);


    if (strpos($cur_id, 'SLEEP') !== false || strpos($cur_id, 'BENCHMARK') !== false || strpos($cur_id, 'IF') !== false ||
    strpos($cur_id, 'LIKE') !== false || strpos($cur_id, '=') !== false || strpos($cur_id, 'REGEX') !== false || strpos($cur_id, 'AND') !== false || strpos($cur_id, '&&') !== false
    ){
        echo "Mi dispiace, ma sembra che tu stia provando a fregarmi!";
        die();
    }


    $stmt = $conn->query("SELECT id, name, img FROM movie_cards WHERE id=". $cur_id);
    $card = $stmt->fetch();

    $stmt = $conn->query("SELECT description FROM movie_description WHERE movie_id=". $card["id"] );
    $description = $stmt->fetch();

    $conn = null;
    ?>
    <h1>Ecco la descrizione!</h1>
    <p><?php echo $description["description"] ?></p>

    </div>
</div>

    
</body>

</html>


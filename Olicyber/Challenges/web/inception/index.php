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
        <img src="/imgs/logo.png" alt="" style="display: block; margin: auto; max-width: 200px; max-height: 300px;">
        <p class="text-center text-white" style="margin-top: -35px;">Quant'era bello il film!</p>
    </div>
<div class="container">
    <div class="row">    
    <?php

    $stmt = $conn->query("SELECT * FROM movie_cards");
    while ($row = $stmt->fetch()) {
        ?>
        <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="<?php echo $row['img']; ?>" alt="Card image cap" style="max-height:135px;">
            <div class="card-body">
                <h5 class="card-title"><?php echo $row['name']; ?></h5>
                <a href="/see.php?id=<?php echo $row['id']; ?>" target="_blank" class="btn btn-primary">Leggi l'articolo</a>
            </div>
        </div>
        <?php
    }

    $conn = null;
    ?>
    </div>
</div>

    
</body>

</html>


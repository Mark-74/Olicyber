<?php
    $flag = $_ENV["FLAG2"];
    if (isset($_GET["secret"]) && $_GET["secret"] === "REDACTED"){
        echo "<h2>$flag<h2>";
    } else {
        echo "<h2>UNAUTHORIZED!!!!</h2>";
    }
?>
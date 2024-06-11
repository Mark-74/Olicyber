<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>SplashBox</title>
    <!-- Latest compiled and minified CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
    <nav class="nav nav-tabs">
        <? $page =  isset($_GET["page"]); ?>
        <a href="/" class="nav-link <? if (!$page) echo 'active'; ?>">Home</a>
        <a href="/?page=flag" class="nav-link <? if ($page && $_GET["page"] === "flag") echo 'active'; ?>">Leggi "Misto Fritto"!</a>
        <? if (!isset($_SESSION["username"])) { ?>
            <a href="/?page=login" class="nav-link <? if ($page && $_GET["page"] === "login") echo 'active'; ?>">Login</a>
            <a href="/?page=register" class="nav-link <? if ($page && $_GET["page"] === "register") echo 'active'; ?>">Registrazione</a>
            <a href="/?page=contacts" class="nav-link <? if ($page && $_GET["page"] === "contacts") echo 'active'; ?>">Contattaci</a>
        <? } else { ?>
            <a href="/?page=otp" class="nav-link <? if ($page && $_GET["page"] === "otp") echo 'active'; ?>">OTP</a>
            <a href="/?page=stash" class="nav-link <? if ($page && $_GET["page"] === "stash") echo 'active'; ?>">Le mie poesie</a>
            <a href="/logout.php" class="nav-link">Logout</a>
        <? } ?>
    </nav>


    <div class="container" style="margin-top: 100px;">

        <? if (isset($_SESSION["latest_error"])) { ?>
            <div class="alert alert-danger" role="alert">
                <?= $_SESSION["latest_error"] ?>
            </div>
        <?php unset($_SESSION["latest_error"]);
        } ?>
        <div class="starter-template">
            <?php
            if (isset($_GET["page"])) {
                require_once($_GET["page"] . ".php");
            } else { ?>
                <div>
                    <h1>SplashBox</h1>
                    <p>Tieni al sicuro le tue poesie più segrete, qui da SplashBox teniamo in custodia le poesie dei più grandi autori.</p>
                    <p>Anche se la tua password venisse compromessa, saresti comunque al sicuro grazie al nostro OTP pienamente compatibile con Google Authenticator</p>
                    <p>Tra le opere più famose presenti nel nostro archivio abbiamo "La prima flag", a cui però abbiamo accesso solo noi amministratori. L'altra opera inestimabile è "Il Gabibbo notturno", a cui però nessuno ha accesso per motivi di sicurezza.</p>
                </div>
            <?php } ?> 

        </div>
</body>

</html>
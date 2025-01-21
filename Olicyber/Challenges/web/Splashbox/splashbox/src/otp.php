<?php

declare(strict_types=1);

use chillerlan\QRCode\QRCode;
use chillerlan\QRCode\QROptions;
use lfkeitel\phptotp\{Base32, Totp};

require_once("./vendor/autoload.php");

if (session_status() === PHP_SESSION_NONE) {
  session_start();
}

if (isset($_POST["otpcode"]) && isset($_POST["username"])) {
  $db = new PDO("sqlite:/tmp/my.db");
  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  $stmt = $db->prepare("SELECT rowId, username FROM users WHERE username=?");
  $stmt->execute([$_POST["username"]]);
  $user = $stmt->fetch();

  if (!$user) {
    die();
  }

  $real_otp = (new Totp())->GenerateToken(md5($user["username"]));
  if ($real_otp !== $_POST["otpcode"]) {
    $_SESSION["latest_error"] = "Invalid OTP!";
    header("location: /?page=otp", response_code: 303);
    die();
  } else {
    $_SESSION["username"] = $user["username"];
    header("location: /", response_code: 303);
    die();
  }
} else if (isset($_SESSION["username"])) {
  $options = new QROptions(
    [
      'eccLevel' => QRCode::ECC_L,
      'outputType' => QRCode::OUTPUT_MARKUP_SVG,
      'version' => QRCode::VERSION_AUTO,
    ]
  );
  $username = $_SESSION["username"];
  $secret = Base32::encode(md5("admin"));
  echo $secret;
  $qrcode = (new QRCode($options))->render("otpauth://totp/SplashBox:$username?secret=$secret&issuer=SplashBox");
?>
  <h1>OTP</h1>
  <p>Scannerizza il QR con il tuo client TOTP preferito</p>
  <img style="display:block; margin: auto;" src='<?= $qrcode ?>' alt='QR Code' width='400' height='400'>

<? } else if (isset($_SESSION["logging_username"])) { ?>
  <h1>OTP</h1>
  <p>Inserisci il codice OTP</p>
  <form action="/otp.php" method="POST">

    <input id="otpcode" type="text" name="otpcode">
    <input type="hidden" name="username" value="<?= $_SESSION["logging_username"] ?>">
    <input type="submit" class="btn btn-primary" value="Invia">
  </form>
<? } ?>

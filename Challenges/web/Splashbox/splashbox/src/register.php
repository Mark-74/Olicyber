<?php
if (session_status() === PHP_SESSION_NONE) {
  session_start();
}

if (isset($_POST["username"]) && isset($_POST["password"])) {
  try {

    $db = new PDO("sqlite:/tmp/my.db");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


    $sql = "INSERT INTO users (username, password) VALUES (?,?)";
    $stmt = $db->prepare($sql)->execute([$_POST["username"], $_POST["password"]]);
    $_SESSION["username"] = $_POST["username"];

    header("location: /?page=otp", response_code: 303);
  } catch (PDOException $e) {
    $_SESSION["latest_error"] = "Registration failed!";
    header("location: /?page=register", response_code: 303);
    die();
  }
}

?>

<form action="/register.php" method="POST">
  <div class="form-group">
    <label for="user">Username</label>
    <input type="text" class="form-control" id="user" name="username" placeholder="Gabibbo">
  </div>
  <div class="form-group">
    <label for="pass">Password</label>
    <input type="password" class="form-control" id="pass" name="password" placeholder="Password">
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
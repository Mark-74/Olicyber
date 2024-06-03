<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
if (isset($_POST["username"]) && isset($_POST["password"])) {

    $db = new PDO("sqlite:/tmp/my.db");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $db->prepare("SELECT * FROM users WHERE username=? AND password=?");
    $stmt->execute([$_POST["username"], $_POST["password"]]);
    $user = $stmt->fetch();
    if (!$user){
        $_SESSION["latest_error"] = "Invalid credentials!";
        header("location: /?page=login", response_code:303);
        die();
    }
    $_SESSION["logging_username"] = $_POST["username"];
    header("location: /?page=otp", response_code:303);
}

?>
<form action="/login.php" method="POST">
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
<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
if (!isset($_SESSION["username"])) {
    echo "<h2>UNAUTHORIZED</h2>";
    die();
}
?>
<h2>Le tue poesie più segrete</h2>
<?php
$db = new PDO("sqlite:/tmp/my.db");
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

if (isset($_POST["text"])) {
    $stmt = $db->prepare("INSERT INTO stash (user, text) VALUES ((SELECT rowId FROM users WHERE username=?), ?)");
    $stmt->execute([$_SESSION["username"], $_POST["text"]]);
}

$stmt = $db->prepare("SELECT * FROM stash WHERE user=(SELECT rowId FROM users WHERE username=?)");
$stmt->execute([$_SESSION["username"]]);
$data = $stmt->fetchAll();
?>
<div class="row">
    <div class="card" style="width: 18rem;">
        <div class="card-body">
            <p class="card-text">Crea poesia</p>
            <form action="/?page=stash" method="POST">
                <div class="form-group">
                    <label for="poem">Poesia</label>
                    <textarea class="form-control" name="text" id="" cols="10" rows="5" placeholder="Ognuno sta solo sul cuor del Gabibbo
trafitto da un raggio di televisione:
ed è subito sera."></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Invia</button>
            </form>
        </div>
    </div>
    <?
    foreach ($data as $row) {
        $text = htmlentities($row["text"]);
    ?>
        <div class="card" style="width: 14rem;">
            <div class="card-body">
                <p class="card-text"><?= $text ?></p>
            </div>
        </div>
    <?
    }
    ?>
</div>
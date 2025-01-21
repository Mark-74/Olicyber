<?php 
    if(isset($_POST["cmd"]) && !empty($_POST["cmd"])){
        $cmd = $_POST["cmd"];
        $result;
        if(empty($cmd)){
            $result = "Almeno prova a darmi un comando, dai";
        }
        else{
            if(preg_match('/[#@%^&*_+\[\]:>?~\\\\]/', $cmd)){
                $result = "Stai cercando di hackerarmi usando strani caratteri? Con me non funziona";
            }
            elseif(strlen($cmd) > 70){
                $result = "Alle superiori ho scritto temi meno lunghi di così";
            }
            elseif (strpos($cmd, "cowsay") !== false) {
                $arr = explode('"', $cmd);
                if($arr && !empty($arr) && $arr[1]){
                    $str = $arr[1];
                    if($str && !empty($str)) $result = passthru('cowsay "'.addslashes($str).'"');
                    else $result = "Nope";
                }
                else $result = "Nope";
            }
            elseif(strpos($cmd, "sudo") !== false){
                $result = "Sudi? Fatti una doccia..";
            }
            elseif(strpos($cmd, "echo") !== false){
                $result = "echooo echoo echo ech ec e";
            }
            elseif (strpos($cmd, "cat") !== false) {
                $result = "Miao";
                $result .= "\n   \    /\\";
                $result .= "\n    )  ( ')";
                $result .= "\n   (  /  )";
                $result .= "\n    \(__)|"; 
            }
            elseif (strpos($cmd, " ") !== false){
                $result = "Qui non c'è spazio per gli spazi!";
            }
            elseif (strpos($cmd, "head") !== false || strpos($cmd, "tail") !== false || strpos($cmd, "od") !== false || strpos($cmd, "less") !== false || strpos($cmd, "head") !== false || strpos($cmd, "hexdump") !== false){
                $result = "Vorresti leggere qualcosa? Non penso proprio";
            }
            else{
                $result = exec($cmd);
                $result = substr($result, 0, 10);
            }
        }
        echo $result;
    }
?>
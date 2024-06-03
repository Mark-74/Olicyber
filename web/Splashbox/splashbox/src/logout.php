<?php 
    session_start();
    session_destroy();
    header("location: /?page=login", response_code: 303);
?>
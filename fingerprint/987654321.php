<?php

$data = implode($_POST);

$t=time();
$data = "[" . date("d:M:Y:H:i:s",$t) . " +0000] " . $data . "\n";

$fh = fopen("/var/log/fingerprint/log.txt", "a");
fwrite($fh, $data);
fclose($fh);

header("location: /home?user=zebrapal123");

?>

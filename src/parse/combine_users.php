<?php

$r = array();

if ($dh = opendir('./member_new')){
    while (($fn = readdir($dh)) !== false){
	if($fn[0] == '.') continue;
	$r[explode(".", $fn)[0]] = file_get_contents('./member_new/'.$fn);
    }
    closedir($dh);
}

$d = "";

foreach($r as $key => $val){
  $d .= $key." ".$val."\n";
}

file_put_contents("all_user.txt", $d);

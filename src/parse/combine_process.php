<?php

if ($dh = opendir('./member')){
    while (($fn = readdir($dh)) !== false){
	if($fn[0] == '.') continue;
	$aut = [];
	if ($dhh = opendir('./member/'.$fn)){
		while(($ffn = readdir($dhh)) !== false){
			if($ffn[0] == '.') continue;
			$aut[] = file_get_contents('./member/'.$fn.'/'.$ffn);
		}
	}
	closedir($dhh);
	file_put_contents('./member_new/'.$fn.'.txt', implode(" ", $aut));
    }
    closedir($dh);
}

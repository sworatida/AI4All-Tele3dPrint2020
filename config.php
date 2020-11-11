<?php

define("CONFIG_SERVER_NAME", "localhost");
define("CONFIG_DB_USER", "teledpr1_tele3dprinting");
define("CONFIG_DB_PWD", "auF[hhci");
define("CONFIG_DB_NAME", "teledpr1_eec2");

// header('Content-Type: text/html; charset=utf-8');

// # database
$mycon = new mysqli(constant("CONFIG_SERVER_NAME"), constant("CONFIG_DB_USER"), constant("CONFIG_DB_PWD"), constant("CONFIG_DB_NAME"));

if ($mycon->connect_error)
{
    die("Database connection fail : " . $mycon->connect_error);
    exit();
}
$mycon->close();

// # upload product image
//$config_upload_folder  = "../../upload_stl/";
$config_upload_folder  = "../../upload_stl/";

$course_list   = array("บทที่ 1", "บทที่ 2", "บทที่ 3", "บทที่ 4", "บทที่ 5", "บทที่ 6", "บทที่ 7", "บทที่ 8", "บทที่ 9", "บทที่ 10");
<?php

/**
 * 大文件切割上传，把每次上传的数据合并成一个文件
 * 如果是linux系统的话 切记给uploads给权限
 * sudo chmod -R 777 uoloads/
 */
// 前端文件：upload.html + 本文件：upload.php + 图片保存文件夹 uploads
function msectime() {
    list($msec, $sec) = explode(' ', microtime());
    $msectime = (float)sprintf('%.0f', (floatval($msec) + floatval($sec)) * 1000);
    return intval($msectime);
}
function getExt1($filename) {
     $arr = explode('.',$filename);
     return array_pop($arr);
}

$timestamp = msectime();
$filename = './uploads/'.$_POST['filename'];                    //确定上传的文件名


//第一次上传时没有文件，就创建文件，此后上传只需要把数据追加到此文件中
if(!file_exists($filename)) {
    move_uploaded_file($_FILES['video']['tmp_name'],$filename);
}else{
    file_put_contents($filename,file_get_contents($_FILES['video']['tmp_name']),FILE_APPEND);

    if ($_POST['endoffile'] == 1) {
        $file_ext = getExt1($filename);                                 //获取后缀名
        $newname = './uploads/'.$timestamp.'.'.$file_ext;               //重命名文件名
        $backname = '/static/uploads/'.$timestamp.'.'.$file_ext;   //最后返回的文件地址

        rename($filename,$newname);
        echo json_encode(array("code"=>200, "data"=>$backname, "msg"=>'Upload ok:'));
    } else {
        echo "000000000000000000";
    }
    //print_r($_POST);
    /*
    {"code": 200,"data": {},"msg": 'Upload ok'}
    */
    /*$endoffile = $_POST['endoffile'];//确定是否最后一个文件
    if($endoffile == 1) {
        //上传到最后一个文件了
        $newname = $filename .''
        $temp = substr($_POST['filename'], strrpos($_POST['filename'], '.')+1);
        //rename($filename,$newname);
        echo json_encode(array('error'=>200, 'message'=>'Upload ok:' .$temp));
    }*/
}
?>
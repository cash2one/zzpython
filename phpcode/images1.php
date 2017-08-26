<?php

ini_set("display_errors", "On");
ini_set("gd.jpeg_ignore_warning", 1); 
error_reporting(E_ALL);
#error_reporting(0);
//URL是远程的完整图片地址，不能为空, $filename 是另存为的图片名字 
//默认把图片放在以此脚本相同的目录里 
function createFolder( $path ,$chmod = 0777 ) 
{ 
	$dirs = explode("/", $path);
    $current_dir = "";
	foreach($dirs as $dir)
	{
		   $current_dir .= $dir."/";
		   if(!file_exists($current_dir))
		   {
					@mkdir($current_dir);
					@chmod($current_dir, $chmod);
		   }
	}
}
function GrabImage($url, $filename=""){ 
	//$url 为空则返回 false; 
	if($url == ""){return false;} 
	$ext = strtolower(strrchr($url, "."));//得到图片的扩展名 
	if($ext != ".gif" && $ext != ".jpg" && $ext != ".bmp" && $ext != ".png"){echo "格式不支持！";return false;} 
	if($filename == ""){$filename = time()."$ext";}//以时间戳另起名 
	//开始捕捉
	 
	ob_start(); 
	readfile($url); 
	$img = ob_get_contents(); 
	ob_end_clean(); 
	$size = strlen($img); 

	$fp2 = fopen($filename , "a"); 
	fwrite($fp2, $img); 
	fclose($fp2); 
	return $filename; 
} 
function getImageInfo($src)
{
    return @getimagesize($src);
}
/**
* 创建图片，返回资源类型
* @param string $src 图片路径
* @return resource $im 返回资源类型 
* **/
function create($src)
{
    $info=getImageInfo($src);
    switch ($info[2])
    {
        case 1:
            $im=imagecreatefromgif($src);
            break;
        case 2:
            $im=imagecreatefromjpeg($src);
            break;
        case 3:
            $im=imagecreatefrompng($src);
            break;
    }
    return $im;
}
/**
* 缩略图主函数
* @param string $src 图片路径
* @param int $w 缩略图宽度
* @param int $h 缩略图高度
* @return mixed 返回缩略图路径
* **/

function resize($rsrc,$src,$w,$h)
{
    $temp=pathinfo($src);
    $name=$temp["basename"];//文件名
    $dir=$temp["dirname"];//文件所在的文件夹
    $extension=$temp["extension"];//文件扩展名
	$ndir=$dir;
	$savepath="{$ndir}/{$name}";//缩略图保存路径,新的文件名为*.thumb.jpg
	$savepath="{$dir}/{$w}-{$h}-{$name}";//缩略图保存路径,新的文件名为*.thumb.jpg
	createFolder($ndir);
	echo $src;
	if (!file_exists($src) || $extension=="")
	{
		$src="/var/www/noimage.gif";
		GrabImage($rsrc,$savepath);
		
	}
	

        //$iconcontent = file_get_contents($temp);
        //header("Content-type: image/" . $extension);
        //header('Content-length: ' . strlen($iconcontent));
		
    //获取图片的基本信息
    $info=getImageInfo($src);
    $width=$info[0];//获取图片宽度
    $height=$info[1];//获取图片高度
    $per1=round($width/$height,2);//计算原图长宽比
    $per2=round($w/$h,2);//计算缩略图长宽比
	


    $cbli=round($height/$width,2);
    if ($width>600)
	{
		$nwidth=600;
		$nheight=$cbli*$nwidth;
	}
	else
	{
		$nwidth=$width;
		$nheight=$height;
	}
	
	
    //计算缩放比例
    if($per1>$per2||$per1==$per2)
    {
        //原图长宽比大于或者等于缩略图长宽比，则按照宽度优先
        $per=$w/$width;
    }
    if($per1<$per2)
    {
        //原图长宽比小于缩略图长宽比，则按照高度优先
        $per=$h/$height;
    }
    $temp_w=intval($width*$per);//计算原图缩放后的宽度
    $temp_h=intval($height*$per);//计算原图缩放后的高度
    $temp_img=imagecreatetruecolor($temp_w,$temp_h);//创建画布

    $im=create($src);
    imagecopyresampled($temp_img,$im,0,0,0,0,$temp_w,$temp_h,$width,$height);
    ob_start(); // start a new output buffer
        $img=imagejpeg($temp_img,'', 100);
        $ImageData = ob_get_contents();
        $ImageDataLength = ob_get_length();
    ob_end_clean(); // stop this output buffer
	#header("Content-type: image/" . $extension);
	if ($ImageDataLength>0){
    	header("Content-Length: ".$ImageDataLength);
	}
	
    #echo $ImageData;
	
	#header("HTTP/1.1 304 Not Modified"); 
	exit(0);
}
/**
* 添加背景
* @param string $src 图片路径
* @param int $w 背景图像宽度
* @param int $h 背景图像高度
* @param String $first 决定图像最终位置的，w 宽度优先 h 高度优先 wh:等比
* @return 返回加上背景的图片
* **/
function addBg($src,$w,$h,$fisrt="w")
{
    $bg=imagecreatetruecolor($w,$h);
    $white = imagecolorallocate($bg,255,255,255);
    imagefill($bg,0,0,$white);//填充背景

    //获取目标图片信息
    $info=getImageInfo($src);
    $width=$info[0];//目标图片宽度
    $height=$info[1];//目标图片高度
    $img=create($src);
    if($fisrt=="wh")
    {
        //等比缩放
        return $src;
    }
    else
    {
        if($fisrt=="w")
        {
            $x=0;
            $y=($h-$height)/2;//垂直居中
        }
        if($fisrt=="h")
        {
            $x=($w-$width)/2;//水平居中
            $y=0;
        }
        imagecopymerge($bg,$img,$x,$y,0,0,$width,$height,100);
        imagejpeg($bg,$src,100);
        imagedestroy($bg);
        imagedestroy($img);
        return $src;
    }

}

function resizeImage($im,$maxwidth,$maxheight,$name,$filetype)
{
    $pic_width = imagesx($im);
    $pic_height = imagesy($im);
    if(($maxwidth && $pic_width > $maxwidth) || ($maxheight && $pic_height > $maxheight))
    {
        if($maxwidth && $pic_width>$maxwidth)
        {
            $widthratio = $maxwidth/$pic_width;
            $resizewidth_tag = true;
        }
        if($maxheight && $pic_height>$maxheight)
        {
            $heightratio = $maxheight/$pic_height;
            $resizeheight_tag = true;
        }
        if($resizewidth_tag && $resizeheight_tag)
        {
            if($widthratio<$heightratio)
                $ratio = $widthratio;
            else
                $ratio = $heightratio;
        }
        if($resizewidth_tag && !$resizeheight_tag)
            $ratio = $widthratio;
        if($resizeheight_tag && !$resizewidth_tag)
            $ratio = $heightratio;
        $newwidth = $pic_width * $ratio;
        $newheight = $pic_height * $ratio;
        if(function_exists("imagecopyresampled"))
        {
            $newim = imagecreatetruecolor($newwidth,$newheight);
           imagecopyresampled($newim,$im,0,0,0,0,$newwidth,$newheight,$pic_width,$pic_height);
        }
        else
        {
            $newim = imagecreate($newwidth,$newheight);
           imagecopyresized($newim,$im,0,0,0,0,$newwidth,$newheight,$pic_width,$pic_height);
        }
        //$name = $name.$filetype;
        imagejpeg($newim,$name);
        imagedestroy("/mnt/".$newim);
    }
    else
    {
        //$name = $name.$filetype;
        imagejpeg($im,$name);
    }           
}
/////////////////////////////
$path=@$_GET['picurl'];
if (!$path || $path=="/" || $path==""){
	$path="http://img1.zz91.com/noimage.gif";
}
//echo $path;
$pathnew=str_replace('http://img1.zz91.com','',$path);
$pathnew=str_replace('http://img.zz91.com','',$pathnew);
$pathnew=str_replace('http://news.zz91.com','',$pathnew);
if (strpos($pathnew,"img1.huanbao.com")>0){
	$pathnew=str_replace('http://img1.huanbao.com','',$pathnew);
	$pathnew="/mnt/data/huanbao/resources".$pathnew;
}else{
	$pathnew="/mnt/data/resources".$pathnew;
}

if (strpos($pathnew,"imgnews")>0){
	$pathnew=str_replace('http://imgnews.zz91.com','',$pathnew);
	$pathnew="/mnt/phpcode/zz91news/uploads/uploads".$pathnew;
}

if (file_exists($pathnew))
{
}else{
	$pathnew=$path;
}
echo $pathnew;
if (empty($_GET['width']))
{
	$gwidth=100;
}else{
	$gwidth=$_GET['width'];
}
if (empty($_GET['height']))
{
	$gheight=100;
}else
{
	$gheight=$_GET['height'];
}
	$temp=pathinfo($pathnew);
	if (!$temp){
		$temp=pathinfo("/mnt/data/resources/noimage.gif");
	}
    $name=$temp["basename"];//文件名
    $dir=$temp["dirname"];//文件所在的文件夹
    $extension=$temp["extension"];//文件扩展名
	$savepath="{$dir}/{$gwidth}-{$gheight}-{$name}";//缩略图保存路径,新的文件名为*.thumb.jpg
//header('Content-Type:image/jpeg');
//header("Content-Length: 10688");
// 
resize($path,$pathnew,$gwidth,$gheight);

?>

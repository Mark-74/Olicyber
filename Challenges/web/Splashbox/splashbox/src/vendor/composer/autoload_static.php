<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInit98c140a7c798a70739254fc9b9980716
{
    public static $prefixLengthsPsr4 = array (
        'l' => 
        array (
            'lfkeitel\\phptotp\\' => 17,
        ),
        'c' => 
        array (
            'chillerlan\\Settings\\' => 20,
            'chillerlan\\QRCode\\' => 18,
        ),
    );

    public static $prefixDirsPsr4 = array (
        'lfkeitel\\phptotp\\' => 
        array (
            0 => __DIR__ . '/..' . '/lfkeitel/phptotp/src',
        ),
        'chillerlan\\Settings\\' => 
        array (
            0 => __DIR__ . '/..' . '/chillerlan/php-settings-container/src',
        ),
        'chillerlan\\QRCode\\' => 
        array (
            0 => __DIR__ . '/..' . '/chillerlan/php-qrcode/src',
        ),
    );

    public static $classMap = array (
        'Composer\\InstalledVersions' => __DIR__ . '/..' . '/composer/InstalledVersions.php',
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixLengthsPsr4 = ComposerStaticInit98c140a7c798a70739254fc9b9980716::$prefixLengthsPsr4;
            $loader->prefixDirsPsr4 = ComposerStaticInit98c140a7c798a70739254fc9b9980716::$prefixDirsPsr4;
            $loader->classMap = ComposerStaticInit98c140a7c798a70739254fc9b9980716::$classMap;

        }, null, ClassLoader::class);
    }
}
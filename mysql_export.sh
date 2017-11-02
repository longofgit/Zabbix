#!/bin/bash  
# mysql数据库 mysql -hmysql地址 -u数据库名 -P端口 -p密码 数据库 -N -e
mysql -hrm-bp10x580rka07zrlg.mysql.rds.aliyuncs.com -ujijian -P3306 -phelianjijian zabbix -N -e "
set names utf8;
 select hosts.name from hosts join items on hosts.name like 'HY0%' and items.hostid=hosts.hostid and items.name='连接上的用户MAC总表（认证通过）' order by hosts.name;
" >>/home/hadoop/product_task/hospital.csv
# >>文件保存路径



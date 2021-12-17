E2E Final Assignment
Production server steps
Logged in using ssh production@40.121.198.137
Yes
Appliedhi2021
production@production:~$ sudo apt-get update
production@production:~$ sudo apt install mysql-server mysql-client
Y

Replica sever steps
Logged in using ssh replica@52.191.194.105
Yes
Appliedhi2021
replica@replica:~$ sudo apt-get update
replica@replica:~$ sudo apt install mysql-server mysql-client
Y

Return to Production Server Steps

#Create User
Creates user through python 

#Created a new database called 'tempdata' and import data
imported h1n1 cvs file into tempdata using python

#Create User through command prompt
production@production:~$ sudo mysql
mysql> CREATE USER 'dba'@'%' IDENTIFIED BY 'ahi2021';
mysql> GRANT ALL PRIVILEGES ON *.* to 'dba'@'%' WITH GRANT OPTION;
production@production:~$ mysql -u dba -p
ahi2021
mysql> create database tempdata;

#Configuration Files for production server
production@production:~$ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address = 0.0.0.0
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = tempdata
production@production:~$ sudo service mysql restart

mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000002 |      154 | tempdata     |                  |                   |
+------------------+----------+--------------+------------------+-------------------+


#Creating mysql dump
production@production:~$ sudo mysqldump --opt tempdata > tempdata.sql
production@production:~$ ls
tempdata.sql


#Using SCP Command
on replica server: 
replica@replica:~$ pwd
/home/replica
on production server:
production@production:~$ scp tempdata.sql replica@52.191.194.105:/home/replica
yes
Appliedhi2021
tempdata.sql

on replica server:
replica@replica:~$ ls
tempdata.sql
replica@replica:~$ sudo mysql tempdata < tempdata.sql

#Configuration Files for replica server
replica@replica:~$ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address = 0.0.0.0
server-id = 2
relay-log = /var/log/mysql/mysql-relay-bin.log
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = tempdata
replica@replica:~$ sudo service mysql restart

Check slave status
mysql> change master to master_host='40.121.198.137',master_user ='dba',master_password='ahi2021',master_log_file='mysql-bin.000002',master_log_pos= 154;
mysql> start slave;
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 40.121.198.137
                  Master_User: dba
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000002
          Read_Master_Log_Pos: 154
               Relay_Log_File: mysql-relay-bin.000002
                Relay_Log_Pos: 320
        Relay_Master_Log_File: mysql-bin.000002
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 154
              Relay_Log_Space: 527
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
                  Master_UUID: 1ab3cd56-5eb5-11ec-b688-002248204c5a
             Master_Info_File: /var/lib/mysql/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
mysql> exit;
replica@replica:~$ sudo mysql
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| tempdata           |
+--------------------+
mysql> use tempdata;
mysql> show tables;
+--------------------+
| Tables_in_tempdata |
+--------------------+
| flu_vaccines       |
| h1n1               |
+--------------------+


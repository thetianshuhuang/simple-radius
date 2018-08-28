# simple-radius
Simple radius server supporting authentication for running WPA2-Enterprise on a home network.


# Installation
Only linux systems are supported.


1. Install FreeRadius
```shell
sudo apt-get install freeradius
sudo apt-get install freeradius-mysql
```


2. Install MySQL
```shell
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation
```
Options for ```mysql_secure_installation```:
	- Setup validate password: doesn't matter
	- Remove anonymous users: Y
	- Disallow reoot login remotely: Y
	- Remove test database: Y
	- Reload privilege tables: Y
NOTE: if ```libmysqlclient-dev``` cannot be found, try installing ```default-libmysqlclient-dev```.

3. Configure MySQL for FreeRadius
```shell
cd /etc/freeradius/3.0/mods-config/sql/main
mysql -u root -p radius < schema.sql
mysql -u root -p radius < setup.sql
```
NOTE: the freeradius ```mods-config/sql/main``` folder may be stored in a different location.

If ```mysql -u root -p``` fails with
```
ERROR 1045 (28000): Access denied for user 'root'@'localhost'
```
then use
```
sudo mysql

mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```
replacing ```password``` with your desired password.

If this still fails (MariaDB?), use
```
mysql> USE mysql;
mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('password');
```

4. Configure FreeRadius for MySQL:
```sh
cd /etc/freeradius/3.0/mods-enabled
ln -s ../mods-available/sql sql
```


5. Set up MySQL login for FreeRadius
```sh
mysql -u root -p

mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('password');
mysql> GRANT ALL ON radius.* to 'radius'@'localhost';
```
Replace 'password' with the desired password.

NOTE: if ```mysql -u root -p``` fails, you may need to run as ```sudo```.

6. Install Python (>= v3.6) if not already installed. NOTE: on certain systems (especially Ubuntu server) you may need to add a repository to install pip (```sudo apt-add-repository universe```, etc).
```sh
sudo apt-get install python3
sudo apt-get install python3-pip
```

7. Clone this repository.
```sh
sudo apt-get install git
git clone https://github.com/thetianshuhuang/simple-radius
cd simple-radius
```

8. Create a virtual environment
```sh
sudo pip3 install virtualenv
virtualenv radiusenv
source radiusenv/bin/activate
```

9. Install Python dependencies
```sh
pip install django
pip install mysqlclient
```


# API
Currently, no frontend has been implemented.

```sh
$ python manage.py shell

>>> from management import auth
>>> auth.add_user("test_user", "test")
>>> auth.change_password("test_user", "test_password")
>>> exit()

$ radtest test_user test_password localhost 0 testing123
```

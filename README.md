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


5. Configure FreeRadius for MySQL:
```shell
cd /etc/freeradius/3.0/mods-enabled
ln -s ../mods-available/sql sql
```


6. Install Python (>= v3.6) if not already installed. NOTE: on certain systems (especially Ubuntu server) you may need to add a repository to install pip (```sudo apt-add-repository universe```, etc).
```shell
sudo apt-get install python3
sudo apt-get install python3-pip
```

7. Clone this repository.
```shell
sudo apt-get install git
git clone https://github.com/thetianshuhuang/simple-radius
cd simple-radius
```

8. Create a virtual environment
```shell
sudo pip3 install virtualenv
virtualenv radius
source radius/bin/activate
```

9. Install Python dependencies
```shell
pip install django
pip install 
```


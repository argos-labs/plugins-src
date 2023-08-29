# SQL

***ARGOS LABS plugin module SQL***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item         | Value
-------------|:---:
Icon         | ![rdb](icon.png) 
Display Name | **SQL**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae@argos-labs.com)

[comment]: <> (* [github]&#40;https://github.com/Jerry-Chae&#41;)

## Notification

### Dependent modules
Module | Source Page                                   | License                                                                       | Version (If specified otherwise using recent version will be used)
---|-----------------------------------------------|-------------------------------------------------------------------------------|---
[PyMySQL](https://pypi.org/project/PyMySQL/) | [PyMySQL](https://github.com/PyMySQL/PyMySQL) | [MIT License](https://github.com/PyMySQL/PyMySQL/blob/main/LICENSE) | PyMySQL==`1.0.2` for MySQL
[Cython](https://pypi.org/project/Cython/)   | [Cython](https://github.com/cython/cython) | [Apache License 2.0](https://github.com/cython/cython/blob/master/LICENSE.txt) | Cython==`0.29.5` for MSSQL
[pymssql](https://pypi.org/project/pymssql/) | [pymssql](https://github.com/pymssql/pymssql) | [GNU Lesser General Public License v2.1](https://github.com/pymssql/pymssql/blob/master/LICENSE) | pymssql==`2.1.5` for MSSQL
## Warning 
None
## Primary Features
* The PostgreSQL plugin enables your bot to directly connect and manipulate the Postgres database.


## Functions
None
## Prerequisite
None
## Helpful links to 3rd party contents
None

## Version Control 
* [4.211.3456](setup.yaml)
* Release Date: Feb 11, 2022

## Input (Required) 
Display Name | Input Method              | Default Value | Description
---|---------------------------|---------------|---------
RDB Type | Select from options | -             | DB Type one of {mysql,mssql}
DB Host | IP Address                | -             |Specify IP address of the host.
DB Port | Port No.                  | -             | Specify the port no of the database.
DB User | User ID(String)           | -             | Determine the specified user ID of the data base.
DB Password | Password                  | -             | Determine the specified password of the data base.
DB Name | String                    | -             | Specify the name of the data base.
SQL String | String | -             | SQL query to execute data.
SQL File | Absolute file path | -             | SQL file to execute.

## Input (Optional)
Display Name | Input Method       | Default Value | Description
---|--------------------|-----|---------
CSV Bulk Input | Absolute file path | -   | CSV bulk input file<br>{0} is first column<br>{1} is second column<br>at CSV bulk input file
Exc * Headers | String | - | If there is(are) header(s), you can use the Exclusion count option here.
Character Set | String | - | The database also uses this character set for metadata such as table names, column names, and SQL statements.
Encoding | -                  | utf-8 | By checking this the target strings will be encoded.



## Return Value
Result of Select Query is CSV.<br>
![Text_from_Image](README_02.png)


## Parameter setting examples
                    
>       Example SQL file
>       --- insert static records
>    
>       INSERT INTO foo (name, age)
> 
>       values
> 
>       ('nobody me', 100),
>    
>       ('foobar', 200)

![Text_from_Image](README_01.png)
![Text_from_Image](README_03.png)




## Return Code
Code | Meaning
---|---
0 | Execution Successful
1 | SQL Errors
9 | Other Failures
    
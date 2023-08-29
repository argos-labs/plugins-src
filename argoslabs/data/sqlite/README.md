# _SQLite_

***ARGOS LABS plugin module SQLite***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item         | Value
-------------|:---:
Icon         | ![sqlite](icon.png) 
Display Name | **SQLite**

## Name of the author (Contact info of the author)

Kyobong An
* [email](mailto:akb0930@argos-labs.com)

[comment]: <> (* [github]&#40;https://github.com/Jerry-Chae&#41;)

## Notification

### Dependent modules
None
## Warning 
None
## Primary Features
* The SQLite plugin has features to operate SQLite RDBMS. You can learn more about SQLite at https://www.sqlite.org/src/doc/trunk/README.md. The plugin can take SQL statement(s) either directly or via file.

## Special Notes
* When inputting a series of SQL statements from a file, it is recommended to separate ‘one way’ statements such as INSERT INTO from ‘two-way’ statements such as SELECT.
## Functions
None
## Prerequisite
**How to install SQLite**

See below for ['step by step'](#how-to-install-sqlite) instruction
## Helpful links to 3rd party contents
None

## Version Control 
* [3.713.1749](setup.yaml)
* Release Date: Jul 13, 2021

## Input (Required) 
Display Name | Input Method        | Default Value | Description
---|---------------------|---------------|---------
DB file | Absolute file path  | -             | Specify the file path of the data base(file extension is .db).
**SQL Statement** - SQL String | String              | -             | SQL query to execute data.
**SQL Statement** - SQL File | Absolute file path  | -             | SQL file to execute.

## Input (Optional)
Display Name | Input Method       | Default Value | Description
---|--------------------|-----|---------
CSV Bulk Input | Absolute file path | -   | CSV bulk input file<br>{0} is first column<br>{1} is second column<br>at CSV bulk input file
Exc * Headers | String | - | If there is(are) header(s), you can use the Exclusion count option here.
Character Set | String | - | The database also uses this character set for metadata such as table names, column names, and SQL statements.
Encoding for CSV | -                  | utf-8 | Encoding format of the CSV file.



## Return Value
This plugin returns value depending on the SQL statement.<br>
Statements such as INSERT INTO and DELETE will return 2 lines like below. (it takes a format of one-column CSV file)<br>
>       affected_row_count<br>
>       3



SELECT statement will return regular CSV file depending on the SQL statement’s parameters<br>

The Return Value can be stored in

>   String<br>
> CSV (Internal memory to PAM)<br>
> File (either .txt or .csv)


## Parameter setting examples
                    

* Using string for SQL and returning csv with SELECT statement<br>
<br>

![Text_from_Image](README_01.png)

* Using file for SQL and csv for input<br>

![Text_from_Image](README_02.png)
* SQL file Examples<br>

![Text_from_Image](README_03.png)

-------
## How to Install _SQLite_
* **STEP 1**<br>

    Download and install DB [SQLite.](https://sqlitebrowser.org/dl/)

![Text_from_Image](README_04.png)<br><Br>
![Text_from_Image](README_05.png)<br><br>
* **STEP 2**<br>
Execute DB and Create a New Database<br>
\* Check Desktop if DB cannot be found in Program Menu

![Text_from_Image](README_06.png)<br><br>
![Text_from_Image](README_07.png)<br><Br>
* **STEP 3**<br>
Create a Table<br>
\* Set a table name, field names and types
![Text_from_Image](README_08.png)
* **STEP 4**<br>
Input Data and Save<br>
\* Click Browse Data and Input Data
![Text_from_Image](README_09.png)<br><Br>
* Save File<br><Br>
![Text_from_Image](README_10.png)



## Return Code
Code | Meaning
---|---
0 | Execution Successful
9 | Execution Failed
    
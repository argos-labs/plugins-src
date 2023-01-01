# MongoDB

***ARGOS LABS plugin module to use Selenium***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item         | Value
-------------|:---:
Icon         | ![mongodb](icon.png) 
Display Name | **MongoDB**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae@argos-labs.com)

[comment]: <> (* [github]&#40;https://github.com/Jerry-Chae&#41;)

## Notification

### Dependent modules
Module | Source Page                                            | License | Version (If specified otherwise using recent version will be used)
---|--------------------------------------------------------|---|---
[pymongo](https://pypi.org/project/pymongo/) | [pymongo](https://github.com/mongodb/mongo-python-driver) | [Apache License 2.0](https://github.com/mongodb/mongo-python-driver/blob/master/LICENSE) | `latest` 
## Warning 
None
## Primary Features
MongoDB plugin is based on Python MongoDB/PyMongo.
## Prerequisite
User must have a basic knowledge about the mongoDB solution.

## Helpful links to 3rd party contents
For more detailed explanations, please refer to the link [here](https://www.w3schools.com/python/python_mongodb_getstarted.asp).


## Version Control 
* [3.730.3456](setup.yaml)
* Release Date: Jul 30, 2021

## Input (Required) 
Display Name | Input Method                                                               | Default Value | Description
---|----------------------------------------------------------------------------|---------------|---------
Operation | (choose one from the 9 pull-down options)![Text_from_Image](README_01.png) | find          | Check [below](#parameter-setting-examples) 
Host IP Address | IP Address                                                                 | -             | Specify the Host IP Address.
Port Number | Number                                                                     | 27017         | Specify the port number.

## Input (Optional)
Display Name | Input Method | Default Value | Description
---|-------------|---------------|---------
DB Name | String | - | Specify the data base name in the text box.
Collection Name | String | - | Specify the collection name in the text box.
User ID | ID | - | After Checking the box type in the proper user id of the db.
Password | Password | - | User ID and Password works in pair.


## Return Value

Please check the Parameter Setting Section [below]()


## Parameter setting examples
### How to set parameters for different functions
### A. Find
![Text_from_Image](README_02.png)


### A -1. Find all
![Text_from_Image](README_03.png)
### A - 2. Find with one filter
![Text_from_Image](README_04.png)
### A - 3. Find with multiple filters
![Text_from_Image](README_05.png)
### A - 4. Find with "Sort" option
![Text_from_Image](README_06.png)
### A - 5. Find with "Skip" and "Limit" options
![Text_from_Image](README_07.png)
### A - 6. Find with "Projection" option
![Text_from_Image](README_08.png)

---
## B. Insert
### B - 1. Insert one document
![Text_from_Image](README_09.png)
### B - 2. Insert multiple documents
![Text_from_Image](README_10.png)

----
## C. Update
### C - 1. Update one document
![Text_from_Image](README_11.png)
### C - 2. Update multiple documents
![Text_from_Image](README_12.png)
### C - 3. Update with "Upsert" flag checked
![Text_from_Image](README_13.png)

----
## D. Delete
### D - 1. Delete one document
![Text_from_Image](README_14.png)
### D - 2. Delete multiple documents
![Text_from_Image](README_15.png)

----
## E. Count
### E - 1. Count one document
![Text_from_Image](README_16.png)

-----

## F. Collection_names
### F - 1. Listing collection names
![Text_from_Image](README_17.png)

----

##  G. List_database_names
### G - 1. Listing database names
![Text_from_Image](README_18.png)

----

## H. Drop_database
### H - 1. Dropping(removing) database
![Text_from_Image](README_19.png)

-----

## I. Drop_collection
### I - 1. Dropping(removing) collection
![Text_from_Image](README_20.png)




## Return Code
Code | Meaning
---|---
0 | Execution Successful
99 | Execution Failed
    

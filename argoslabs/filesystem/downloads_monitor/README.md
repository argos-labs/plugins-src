# Dowbloads Monitor

***This allows the Dowbloads Monitor to be used in scenarios.***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item | Value
---|:---:
Icon | ![Dowbloads Monitor](icon.png) 
Display Name | **Dowbloads Monitor**

## Name of the author (Contact info of the author)

Kyobong An
* [email](mailto:akb0930@argos-labs.com)

[comment]: <> (* [github]&#40;https://github.com/Jerry-Chae&#41;)

## Notification

### Dependent modules
Module | Source Page | License | Version (If specified otherwise using recent version will be used)
---|---|---|---
csv |  |  | latest

## Warning 
None

## Helpful links to 3rd party contents
None

## Version Control 
* [5.428.1030](setup.yaml)
* Release Date: `Apr 28, 2023`

## Input (Required)
Display Name | Input Method                   | Default Value | Description
---|--------------------------------|---|---
Operation | Before_download</br>Monitoring | | Before_download : get a list of downloads.</br>Monitoring : downloads monitoring
CSV Path |                                | | The path of the csv file contained or containing the file list in the download folder

> * If message to translate is too big then use `Text file`

## Return Value

### Normal Case
* Before download : File list of downloads.
* Monitoring : NEW File list of downloads


## Return Code
Code | Meaning
---|---
0 | Success
1 | Exceptional case

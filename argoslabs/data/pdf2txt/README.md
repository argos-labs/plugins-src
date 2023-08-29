# PDF2Txt

***ARGOS LABS PDF Conversion(pdf -> txt) plugin***
> This plugin converts PDF files into .txt files. (.txt)

## Name of the plugin
Item         | Value
-------------|:---:
Icon         | ![pdf2txt](icon.png) 
Display Name | **PDF2TXT**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae`@argos-labs.com)

[comment]: <> (* [github]&#40;https://github.com/Jerry-Chae&#41;)

## Notification

### Dependent modules
Module | Source Page                                    | License                                                                            | Version (If specified otherwise using recent version will be used)
---|------------------------------------------------|------------------------------------------------------------------------------------|---
[pdfminer](https://pypi.org/project/pdfminer/) | [pdfminer](https://github.com/euske/pdfminer) | [MIT License](https://github.com/euske/pdfminer/blob/master/LICENSE) | `latest`


## Warning 
None

## Helpful links to 3rd party contents
None

## Version Control 
* [3.727.3456](setup.yaml)
* Release Date: Jul 27, 2021

## Input (Required)
Display Name | Input Method       | Default Value | Description
-------------|--------------------|---------------|---
PDF File         | Absolute File Path | -             | Select Full file path of a PDF file.



## Input (Optional)


Operations | Full Name                    | Output(Example)
----|------------------------------|---
Output File Path         | Absolute File Path | -             | Specify output .docx folder/name here. If left unchecked, a .docx file will be generated in the folder where input PDF is located with the same file name.




## Return Value
Full file path of the output .txt file will be returned.

## Parameter setting examples
![Text_from_Image01](README_01.png)

## Return Code
Code | Meaning
---|---
0 | Execution Success
1 | Execution Failed

# Base64 Encode/Decode

***This plugin is for encoding or decoding of Base64***

> Note: You can get the concept of [Base64](https://en.wikipedia.org/wiki/Base64)

## Base64 Encode/Decode
Item | Value
---|:---:
Icon | ![Plugin Name](icon1.png) 
Display Name | **Base64 Encode/Decode**

## Name of the author (Contact info of the author)

Venkatesh Vanjre, Jerry Chae
* [email](mailto:vvanjre@argos-labs.com)
* [github](https://github.com/Jerry-Chae/plugins/tree/main/argoslabs/crypt/base64)

## Notification

### Dependent modules
<!-- Module | Source Page | License | Version (If specified otherwise using recent version will be used)
---|---|---|---
[dep-module]() | [dep-module]() | [MIT](https://github.com/ssut/py-googletrans/blob/master/LICENSE) | 4.0 -->

> * [base64](https://docs.python.org/3.7/library/base64.html) module is included at Python standard library
> * So no need third party module

## Warning 
No potential damage to customer files and data (overwrite risk)

## Helpful links to 3rd party contents
None

## Version Control 
* [4.817.1238](setup.yaml)
* Release Date: `Aug 17, 2022`

## Input (Required)
Display Name | Input Method | Default Value | Description
---|---|---|---
Operation | choices | Encode | One of [`Encode`, `Decode`]
Input String | String Source to operate | Empty | 
Input File | Source file to operate | Empty | 

> * One of `Input Sting` or `Input File` must be given for source

## Return Value

### Normal Case

* For `Encode` operation: Return Value contains the encoded result
* For `Decode` operation: Return Value contains the decoded result

## Return Code
Code | Meaning
---|---
0 | Success
1 | Invalid `Input File`
2 | Invalid  Input Value
98 | Invalid Parameters or arguments
99 | Exceptional case

<!-- ## Parameter setting examples (diagrams)
If any STU example capture images. -->


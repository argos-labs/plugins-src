# Google Cloud Vision API

**ARGOS LABS plugin module for Google Vision API** <br><br>
> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item | Value
---|:---:
Icon | ![vision](icon.png) 
Display Name | **Google Cloud Vision API**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae@argos-labs.com)
* [github](https://github.com/Jerry-Chae)

## Notification
## Contents
* [List of file formats supported as input](#list-of-file-formats-supported-as-input)
* [OCR usage](#ocr-usage)
* [OCR usage with output result image](#ocr-usage-with-output-result-image)
* [OCR usage with word output](#ocr-usage-with-word-output)
* [Face usage](#face-usage)
* [Label usage](#label-usage)
* [Landmark usage](#landmark-usage)
* [Logo usage](#logo-usage) 
* [Localized Object usage](#localized-object-usage) 
* [Dominant Colors usage](#dominant-colors-usage)

## Prerequisite
![warning](warning.png) **Before you start**, **click** [How to obtain Google User Credentials](https://wiki.argos-labs.com/display/RPARELNOTE/How+to+obtain+Google+User+Credentials)<br>

![warning](warning.png) **Here is the link to** [Google Vision API pricing information](https://cloud.google.com/vision/pricing)

### Dependent modules
Module | Source Page | License                                                                   | Version (If specified otherwise using recent version will be used)
---|---|---------------------------------------------------------------------------|---
[google-cloud-vision](https://pypi.org/project/google-cloud-vision/) | [google-cloud-vision](https://github.com/GoogleCloudPlatform/cloud-vision) | [Apache License 2.0](https://github.com/GoogleCloudPlatform/cloud-vision/blob/master/LICENSE) | `latest`
[protobuf3-to-dict](https://pypi.org/project/protobuf3-to-dict/) | [protobuf3-to-dict](https://github.com/conda-forge/protobuf3-to-dict-feedstock) | [BSD 3-Clause "New" or "Revised" License](https://github.com/conda-forge/protobuf3-to-dict-feedstock/blob/main/LICENSE.txt) | protobuf3-to-dict>=`0.1.5`
[opencv-python](https://pypi.org/project/opencv-python/) | [opencv-python](https://github.com/opencv/opencv-python) | [MIT License](https://github.com/opencv/opencv-python/blob/4.x/LICENSE.txt) | opencv-python>=`4.1.1.26`

## Warning 
![warning](warning.png) **IMPORTANT NOTE** <br>
1) This is a commercial API and end user will be charged by the supplier of this API after a certain amount of free usage.
2) The user license contract has to be entered directly between the supplier of this API and the End User.
3) ARGOS LABS will not be responsible for any consequences either tangible or non-tangible that result from usage of this API.


![warning](warning.png) Unfortunately PDF and TIFF formats are not currently supported for Cloud Vision.

## Helpful links to 3rd party contents
* [How to obtain Google User Credentials](https://wiki.argos-labs.com/display/RPARELNOTE/How+to+obtain+Google+User+Credentials)
* [Google Vision API pricing information](https://cloud.google.com/vision/pricing)

## Version Control 
* [2.429.3456](setup.yaml)
* Release Date: `Apr 29, 2020

## Input (Required)
* See below for image reference

## Input (Optional)
* See below for image reference

## Return Value
* See below for image reference

## Parameter setting examples (diagrams)

### List of file formats supported as input.
![warning](warning.png) Unfortunately PDF and TIFF formats are not currently supported for Cloud Vision.

The accepted formats are :
* JPEG
* PNG8
* PNG24
* GIF
* Animated GIF (first frame only)
* BMP
* WEBP
* RAW
* ICO

### OCR usage

![Text from Image](README_01.png)

### OCR usage with output result image
![Text from Image](README_02.png)

### OCR usage with word output
![Text from Image](README_03.png)

### Face usage
![Text from Image](README_04.png)

### Label usage
![Text from Image](README_05.png)

### Landmark usage
![Text from Image](README_06.png)

### Logo usage
![Text from Image](README_07.png)

### Localized Object usage
![Text from Image](README_08.png)

### Dominant Colors usage
![Text from Image](README_09.png)




## Return Code
Code | Meaning
---|---
0 | Success
1 | Exceptional case

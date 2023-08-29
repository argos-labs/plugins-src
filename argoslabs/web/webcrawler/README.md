# Web Crawler

***Get the HTML source from the web.***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item | Value
---|:---:
Icon | ![Web Crawler](icon.png) 
Display Name | **Web Crawler**

## Name of the author (Contact info of the author)

Kyobong An
* [email](mailto:akb0930@argos-labs.com)

[comment]: <> (* [github]&#40;https://github.com/Jerry-Chae&#41;)

## Notification

### Dependent modules
Module | Source Page                                 | License                          | Version (If specified otherwise using recent version will be used)
---|---------------------------------------------|----------------------------------|---
[requests](https://pypi.org/project/requests/) | [requests](https://github.com/psf/requests) | [Apache](https://github.com/psf/requests/blob/main/LICENSE) | latest
[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)|[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)|MIT|latest
[lxml](https://pypi.org/project/lxml/) | [lxml](https://github.com/lxml/lxml) |BSD|latest
## Warning 
None

## Helpful links to 3rd party contents
None

## Version Control 
* [5.621.1700](setup.yaml)
* Release Date: `June 21, 2023`

## Input (Required)
Display Name | Input Method | Default Value | Description
---|-----------|---|---
URL |  | | HTTP[S] URL


> * If message to translate is too big then use `Text file`

## Input (Optional)

Display Name |Group| Show Default | Input Method         | Default Value | Description
---|---|--------------|----------------------|--|---
HTML Parser |  | False        | lxml</br>html.parser |lxml| HTML parse type.
Save File|  | True         |                      | | save result to file

> * If Show Default is True then this item is showed at the Properties otherwise hided at Advanced group



## Return Code
Code | Meaning
---|---
0 | Success
99 | Exceptional case

## Parameter setting examples


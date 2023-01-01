# D-PATH

***ARGOS LABS plugin module for select item from JSON or YAML***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item         | Value
-------------|:---:
Icon         | ![Dpath](icon.png) 
Display Name | **D PATH**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae@argos-labs.com)


## Notification

### Dependent modules
Module | Source Page | License | Version (If specified otherwise using recent version will be used)
---|---|---|---
[dpath](https://pypi.org/project/dpath/) | [dpath](https://github.com/dpath-maintainers/dpath-python) | [MIT](https://github.com/dpath-maintainers/dpath-python/blob/master/LICENSE.txt) | 2.1.3
[PyYAML](https://pypi.org/project/PyYAML/) | [PyYAML](https://github.com/yaml/pyyaml) | [MIT](https://github.com/yaml/pyyaml/blob/master/LICENSE) | 6.0

## Warning 
None

## Helpful links to 3rd party contents
None

## Version Control 
* [2.1130.3300](setup.yaml)
* Release Date: Nov 30, 2020

## Input (Required)
Display Name | Input Method  | Default Value | Description
-------------|---------------|---------------|---
Operation | one of `get`, `search`, `values`, `set`, `new` | `get` | Operation for the items in JSON or YAML
JSON/YAML file | fileread |  | json/yaml file to handle
dpath | | | notation to extract from JSON (/x/y/z)like xpath. [Refer this doc](https://pypi.org/project/dpath/)

> Each `Operation` meaning using dpath are: ([Refer this doc](https://pypi.org/project/dpath/))
> * `get`: Given an object which contains only one possible match for the given glob, return the value for the leaf matching the given glob. If more than one leaf matches the glob, ValueError is raised. If the glob is not found, KeyError is raised.
> * `search`: Given a path glob, return a dictionary containing all keys that matched the given glob.
> * `values`: Given an object and a path glob, return an array of all values which match the glob. The arguments to this function are identical to those of search(), and it is primarily a shorthand for a list comprehension over a yielded search call.
> * `set`: Given a path glob, set all existing elements in the document to the given value. Returns the number of elements changed.
> * `new`: Set the element at the terminus of path to value, and create it if it does not exist (as opposed to 'set' that can only change existing keys).

## Input (Optional)

Display Name | Input Method  | Default Value | Description
-------------|---------------|---------------|---
Specify Output Format | one of `JSON`, `YAML`, `CSV` | `JSON` | Output format of `Return Value`
Set/New Value | | | Value of item designated by dpath for the operation `set` or `new`
Encoding | | utf-8 | Encoding for the JSON or YAML file

## Return Value

This return value is differenct from the `Operation`:

### `get` operation
Sub item or items from give JSON or YAML. Output format is defined by `Specify Output Format`

### `search` operation
Seahching item or items from give JSON or YAML. Output format is defined by `Specify Output Format`

### `values` operation
Get matching item or items from give JSON or YAML. Output format is defined by `Specify Output Format`

### `set` operation
Whole structure from input JSON or YAML changed with setting value. Output format is defined by `Specify Output Format`

### `new` operation
Whole structure from input JSON or YAML changed with new creating item. Output format is defined by `Specify Output Format`


<!-- ## Parameter setting examples
![Text_from_Image01](README_01.png) -->

## Return Code
Code | Meaning
---|---
0 | Success
1 | Invalid Key
2 | Other Error

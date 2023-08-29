#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.xmlmanage`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/08/25]
#     - starting

################################################################################
import os
import sys
import csv
# noinspection PyPackageRequirements
from lxml import etree
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class ParameterError(Exception):
    ...


################################################################################
OPS = [
    'Get',
    'Set',
    'AppendNext',
    'AppendChild',
    'Delete',
    'Length',
]


################################################################################
def op_get(e, is_strip=False):
    if isinstance(e, list):
        e = e[0]
    if hasattr(e, 'text'):
        txt = e.text
    elif isinstance(e, str):
        txt = e
    else:
        txt = str(e)
    if is_strip:
        txt = txt.strip()
    print(txt, end='')
    return 0


################################################################################
def op_length(e):
    if not isinstance(e, list):
        print('0', end='')
    else:
        print(len(e), end='')
    return 0


################################################################################
def _split_attr(xpath):
    eles = xpath.split('/')
    exp = '/'.join(eles[:-1])
    att = eles[-1].strip()
    if att[0] != '@':
        raise ParameterError(f'Attribute must starts with "@" but "{att[0]}"')
    return exp, att[1:]


################################################################################
def op_delete(root, e, out_xml, xpath):
    if isinstance(e, list):
        e = e[0]
    if isinstance(e, str):  # 속성인 경우에는 str 형식임
        ppath, att = _split_attr(xpath)
        e = root.xpath(ppath)
        if isinstance(e, list):
            e = e[0]
        if att in e.attrib:
            del e.attrib[att]
    else:
        e.getparent().remove(e)
    root.write(out_xml)
    print(out_xml, end='')
    return 0


################################################################################
def _set_attr(root, xpath, val):
    ppath, att = _split_attr(xpath)
    e = root.xpath(ppath)
    if not e:
        raise ReferenceError(f'Invalid xpath for "{ppath}"')
    if isinstance(e, list):
        e = e[0]
    e.attrib[att] = val


################################################################################
def op_set(root, e, val, out_xml, xpath):
    if not e:  # 없는 속성인 경우
        _set_attr(root, xpath, val)
    else:
        if isinstance(e, list):
            e = e[0]
        if isinstance(e, str):  # 속성인 경우에는 str 형식임
            _set_attr(root, xpath, val)
        else:
            e.text = val
    root.write(out_xml)
    print(out_xml, end='')
    return 0


################################################################################
def op_append_next(root, e, val, out_xml, xpath):
    if isinstance(e, list):
        e = e[0]
    if isinstance(e, str):  # 속성인 경우에는 str 형식임
        ppath, att = _split_attr(xpath)
        e = root.xpath(ppath)
        if isinstance(e, list):
            e = e[0]

    val = val.strip()
    if not (val and (val[0] == '<' and val[-1] == '>')):
        raise ParameterError(f'In append operation Value must contain xml format '
                             f'like "<div style=\'clear: both\'>my test</div>" but "{val}"')
    pe = e.getparent()
    pe.insert(pe.index(e) + 1, etree.XML(val))
    root.write(out_xml)
    print(out_xml, end='')
    return 0


################################################################################
def op_append_child(root, e, val, out_xml, xpath):
    if isinstance(e, list):
        e = e[0]
    if isinstance(e, str):  # 속성인 경우에는 str 형식임
        ppath, att = _split_attr(xpath)
        e = root.xpath(ppath)
        if isinstance(e, list):
            e = e[0]

    val = val.strip()
    if not (val and (val[0] == '<' and val[-1] == '>')):
        raise ParameterError(f'In append operation Value must contain xml format '
                             f'like "<div style=\'clear: both\'>my test</div>" but "{val}"')
    e.append(etree.XML(val))
    root.write(out_xml)
    print(out_xml, end='')
    return 0


################################################################################
@func_log
def xml_manage(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xml_file = argspec.xml
        if not os.path.exists(xml_file):
            raise ParameterError(f'Cannot get XML file "{xml_file}"')
        xpath = argspec.xpath
        if not xpath:
            raise ParameterError(f'Invalid XPath')
        with open(xml_file, encoding='utf-8') as ifp:
            root = etree.parse(ifp)
        e = root.xpath(xpath)
        if argspec.op == 'Set':
            if not argspec.out_xml:
                raise ParameterError('Need Out XML File')
            return op_set(root, e, argspec.value, argspec.out_xml, xpath)
        if not e:
            raise ReferenceError(f'Invalid xpath "{xpath}"')
        if argspec.op == 'Get':
            return op_get(e, is_strip=argspec.strip)
        elif argspec.op == 'Length':
            return op_length(e)
        if not argspec.out_xml:
            raise ParameterError('Need Out XML File')
        if argspec.op == 'Delete':
            return op_delete(root, e, argspec.out_xml, xpath)
        elif argspec.op == 'AppendNext':
            return op_append_next(root, e, argspec.value, argspec.out_xml, xpath)
        elif argspec.op == 'AppendChild':
            return op_append_child(root, e, argspec.value, argspec.out_xml, xpath)
        raise RuntimeError(f'Invalid Operation "{argspec.op}"')
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        if isinstance(err, ParameterError):
            return 1
        if isinstance(err, ReferenceError):
            return 2
        return 99
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='10',  # Web Scraping
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='XML Manipulation',
        icon_path=get_icon_path(__file__),
        description='XML data manipulation plugin',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Op',
                          choices=OPS,
                          help='Operations for the XML')
        mcxt.add_argument('xml', input_method='fileread',
                          display_name='XML File',
                          help='xml file to manipulate data')
        mcxt.add_argument('xpath', show_default=True,
                          display_name='XPath',
                          help='Xpath to manage the data')

        # ######################################## for app dependent options
        mcxt.add_argument('--out-xml',
                          display_name='Out XML File',
                          input_method='filewrite',
                          help='XML file to write')
        mcxt.add_argument('--value',
                          display_name='String value or XML string to Set/Append',
                          help='For Set operation')
        mcxt.add_argument('--strip', action='store_true', default=False,
                          display_name='Strip Blanks',
                          help='If this flag is set strip white spaces left and right')

        argspec = mcxt.parse_args(args)
        return xml_manage(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass

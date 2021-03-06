# -*- coding: utf-8 -*-
##
## This file is part of Harvesting Kit.
## Copyright (C) 2013, 2014 CERN.
##
## Harvesting Kit is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Harvesting Kit is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Harvesting Kit; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Set of utilities for mini DOM xml parsing.
"""


class NoDOIError(Exception):
    def __init__(self, value):
        self.value = value


def format_arxiv_id(arxiv_id):
    if arxiv_id and not "/" in arxiv_id and "arXiv" not in arxiv_id:
        return "arXiv:%s" % (arxiv_id,)
    else:
        return arxiv_id


def xml_to_text(xml, delimiter=' ', tag_to_remove=None):
    if tag_to_remove:
        if tag_to_remove in xml.nodeName.encode('utf-8'):
            return ''

    if xml.nodeType == xml.TEXT_NODE:
        return xml.wholeText.encode('utf-8')
    elif 'mml:' in xml.nodeName:
        return xml.toxml().replace('mml:', '').replace('xmlns:mml', 'xmlns').encode('utf-8')
    elif xml.hasChildNodes():
        for child in xml.childNodes:
            return delimiter.join(' '.join(xml_to_text(child, delimiter=' ', tag_to_remove=tag_to_remove) for child in xml.childNodes).split())
    return ''


def get_value_in_tag(xml, tag, tag_to_remove=None):
    tag_elements = xml.getElementsByTagName(tag)
    if tag_elements:
        return xml_to_text(tag_elements[0], tag_to_remove=tag_to_remove)
    else:
        return ""


def get_attribute_in_tag(xml, tag, attr):
    tag_elements = xml.getElementsByTagName(tag)
    tag_attributes = []
    for tag_element in tag_elements:
            if tag_element.hasAttribute(attr):
                tag_attributes.append(tag_element.getAttribute(attr))
    return tag_attributes

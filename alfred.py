"""
This alfred module was originally taken from Jan Muller (https://github.com/nikipore/alfred-python)
and has been adapted for my usage.
"""

import itertools
import optparse
import os
import sys

from xml.etree.ElementTree import Element, SubElement, tostring


_MAX_RESULTS_DEFAULT = 9


class Item(object):

    @classmethod
    def unicode(cls, value):
        try:
            items = value.iteritems()
        except AttributeError:
            return unicode(value)
        else:
            return dict(map(unicode, item) for item in items)

    def __init__(self, uid='', title='', subtitle='', value='', valid=True, icon=None):
        self.attributes = {'uid': uid, 'arg': value, 'valid': 'yes' if valid else 'no'}
        self.title = title
        self.subtitle = subtitle
        self.icon = icon

    def __str__(self):
        return tostring(self.xml(), encoding='utf-8')

    def xml(self):
        item = Element(u'item', self.unicode(self.attributes))
        for attribute in (u'title', u'subtitle', u'icon'):
            value = getattr(self, attribute)
            if value is None:
                continue
            if len(value) == 2 and isinstance(value[1], dict):
                (value, attributes) = value
            else:
                attributes = {}
            SubElement(item, attribute, self.unicode(attributes)).text = unicode(value)
        return item


def get_query():
    parser = optparse.OptionParser()
    parser.add_option('-q', '--query', dest="query")
    options, args = parser.parse_args()
    return options.query


def config():
    return _create('config')


def work(volatile, workflow):
    path = {
        True: '~/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data',
        False: '~/Library/Application Support/Alfred 2/Workflow Data'
    }[bool(volatile)]
    return _create(os.path.join(os.path.expanduser(path), workflow))


def write(text):
    sys.stdout.write(text)


def send_results(results):
    write(xml(results))


def xml(items, maxresults=_MAX_RESULTS_DEFAULT):
    root = Element('items')
    for item in itertools.islice(items, maxresults):
        root.append(item.xml())
    return tostring(root, encoding='utf-8')


def _create(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.access(path, os.W_OK):
        raise IOError('No write access: %s' % path)
    return path

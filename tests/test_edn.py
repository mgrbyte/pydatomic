# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from uuid import UUID

from six import text_type as u
import pytest

from pydatomic import edn


test_data = {
    b'"helloworld"': "helloworld",
    b"23": 23,
    b"23.11": 23.11,
    b"true": True,
    b"false": False,
    b"nil": None,
    b":hello": ":hello",
    br'"string\"ing"': 'string"ing',
    b'"string\n"': 'string\n',
    b'[:hello]':(":hello",),
    b'-10.4':-10.4,
    u('"你"').encode('utf-8'): u('你'),
    u('\\€').encode('utf-8'): u('€'),
    b"[1 2]": (1, 2),
    b"#{true \"hello\" 12}": set([True, "hello", 12]),
    b'#inst "2012-09-10T23:51:55.840-00:00"': datetime(
        2012, 9, 10, 23, 51, 55, 840000),
    b"(\\a \\b \\c \\d)": ("a", "b", "c", "d"),
    b"{:a 1 :b 2 :c 3 :d 4}": {":a":1, ":b":2, ":c":3,":d":4},
    b"[1     2 3,4]": (1,2,3,4),
    b"{:a [1 2 3] :b #{23.1 43.1 33.1}}": {
        ':a': (1, 2, 3),
        ':b': frozenset([23.1, 43.1, 33.1])},
    b"{:a 1 :b [32 32 43] :c 4}": {":a":1, ":b":(32,32,43), ":c":4},
    u('\\你').encode('utf-8'): u("你"),
    b'#db/fn{:lang "clojure" :code "(map l)"}': {
        ':lang': u('clojure'),
        ':code':u('(map l)')
    },
    b"#_ {[#{}] #{[]}} [23[34][32][4]]": (23, (34,), (32,), (4,)),
    (b'(:graham/stratton true  \n , '
     b'"A string with \\n \\"s" true'
     b'#uuid "f81d4fae7dec11d0a76500a0c91e6bf6")'): (
         u(':graham/stratton'),
         True,
         u('A string with \n "s'),
         True,
         UUID('f81d4fae-7dec-11d0-a765-00a0c91e6bf6')
    ),
    (b'[\space \\\xE2\x82\xAC [true []] ;'
     b'true\n[true #inst "2012-09-10T23:39:43.309-00:00" '
     b'true ""]]'): (
        ' ',
         u'\u20ac',
         (True, ()),
         (True,
          datetime(2012, 9, 10, 23, 39, 43, 309000),
          True, '')
    ),
    b' {true false nil    [true, ()] 6 {#{nil false} {nil \\newline} }}': {
        None: (True, ()),
        True: False,
        6: {
            frozenset([False, None]): {None: '\n'}
        }
    },
    b'[#{6.22e-18, -3.1415, 1} true #graham #{"pie" "chips"} "work"]': (
        frozenset([6.22e-18, -3.1415, 1]), True, u'work'
    ),
    b'(\\a .5)': (u'a', 0.5),
    b'(List #{[123 456 {}] {a 1 b 2 c ({}, [])}})': (
        u'List', ((123, 456, {}), {u'a': 1, u'c': ({}, ()), u'b': 2})
    ),
}


def test_all_data():
    for (k, v) in test_data.items():
        assert edn.loads(k) == v, 'Failed to load {}'.format(k)


def test_malformed_data():
    '''Verify ValueError() exception raise on malformed data'''
    data = ['[1 2 3', '@EE', '[@nil tee]']
    for d in data:
        with pytest.raises(ValueError):
            edn.loads(d)


if __name__ == '__main__':
    unittest.main()            

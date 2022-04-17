# -*- coding: utf-8 -*-
import unittest

from fasttld import FastTLDExtract

all_suffix = FastTLDExtract(exclude_private_suffix=False)
no_private_suffix = FastTLDExtract(exclude_private_suffix=True)


class FastTLDExtractCase(unittest.TestCase):
    def test_all_suffix_trie(self):
        trie = all_suffix.trie
        self.assertEqual(trie["cn"]["com"], True)
        self.assertEqual("blogspot" in trie["uk"]["co"], True)
        self.assertEqual("*" in trie["uk"], False)
        self.assertEqual("_END" in trie["cn"], True)
        self.assertEqual(trie["ck"]["*"], True)
        self.assertEqual(trie["ck"]["!www"], True)
        self.assertEqual(trie["ir"]["xn--mgba3a4f16a"], True)
        # private domain test
        self.assertEqual(trie["com"]["appspot"], True)
        self.assertEqual(trie["ee"]["com"]["blogspot"], True)
        self.assertEqual(trie["com"]["0emm"]["*"], True)

    def test_idn_suffix_trie(self):
        trie = all_suffix.trie
        self.assertEqual(trie["香港"]["公司"], True)
        self.assertEqual(trie["新加坡"], True)

    def test_no_private_domain_trie(self):
        trie = no_private_suffix.trie
        self.assertEqual(trie["cn"]["com"], True)
        self.assertEqual(trie["uk"]["co"], True)
        # private domain test
        self.assertEqual(trie["com"], True)  # *.0emm.com or the domains like hk.com, cn.com ,etc.
        self.assertEqual("no-ip.biz" in trie, False)
        self.assertEqual("github" in trie["io"], False)

    def test_no_private_suffix_extract(self):
        self.assertEqual(
            no_private_suffix.extract("www.myownblog.blogspot.ca"),
            ("www.myownblog", "blogspot", "ca", "blogspot.ca"),
        )
        self.assertEqual(
            no_private_suffix.extract("192.168.1.1.no-ip.co.uk"),
            ("192.168.1.1", "no-ip", "co.uk", "no-ip.co.uk"),
        )

    def test_private_suffix_extract(self):
        self.assertEqual(
            all_suffix.extract("www.myownblog.blogspot.ca"),
            ("www", "myownblog", "blogspot.ca", "myownblog.blogspot.ca"),
        )
        self.assertEqual(
            all_suffix.extract("192.168.1.1.no-ip.co.uk"),
            ("192.168.1", "1", "no-ip.co.uk", "1.no-ip.co.uk"),
        )

    def test_all_extract(self):
        todo = [
            "www.google.co.uk",
            "ditu.baidu.com.cn",
            "global.prod.fastly.net",
            "www.global.prod.fastly.net",
            "map.global.prod.fastly.net",
            "www.map.global.prod.fastly.net",
        ]
        assert_list = [
            ("www", "google", "co.uk", "google.co.uk"),
            ("ditu", "baidu", "com.cn", "baidu.com.cn"),
            ("", "", "global.prod.fastly.net", ""),
            ("", "www", "global.prod.fastly.net", "www.global.prod.fastly.net"),
            ("", "map", "global.prod.fastly.net", "map.global.prod.fastly.net"),
            ("www", "map", "global.prod.fastly.net", "map.global.prod.fastly.net"),
        ]

        for t, a in zip(todo, assert_list):
            self.assertEqual(all_suffix.extract(t), a)

    def test_wildcard(self):
        todo = [
            "ck",
            "www.ck",
            "news.www.ck",
            "big.news.www.ck",
            "abc.ck",
            "123.abc.ck",
            "foo.123.abc.ck",
        ]
        assert_list = [
            ("", "", "ck", ""),
            ("", "www", "ck", "www.ck"),
            ("news", "www", "ck", "www.ck"),
            ("big.news", "www", "ck", "www.ck"),
            ("", "", "abc.ck", ""),
            ("", "123", "abc.ck", "123.abc.ck"),
            ("foo", "123", "abc.ck", "123.abc.ck"),
        ]

        for t, a in zip(todo, assert_list):
            self.assertEqual(all_suffix.extract(t), a)

    def test_not_tld(self):
        self.assertEqual(all_suffix.extract("www.abc.noexists"), ("", "", "", ""))
        self.assertEqual(no_private_suffix.extract("www.abc.noexists"), ("", "", "", ""))

    def test_only_dot_tld(self):
        self.assertEqual(all_suffix.extract(".com"), ("", "", "com", ""))
        self.assertEqual(no_private_suffix.extract(".com"), ("", "", "com", ""))

    def test_one_rule(self):
        self.assertEqual(all_suffix.extract("domain.biz"), ("", "domain", "biz", "domain.biz"))
        self.assertEqual(
            no_private_suffix.extract("domain.biz"), ("", "domain", "biz", "domain.biz")
        )

    def test_only_one_wildcard(self):
        self.assertEqual(all_suffix.extract("mm"), ("", "", "mm", ""))
        self.assertEqual(all_suffix.extract("c.mm"), ("", "", "c.mm", ""))
        self.assertEqual(all_suffix.extract("b.c.mm"), ("", "b", "c.mm", "b.c.mm"))

        self.assertEqual(no_private_suffix.extract("mm"), ("", "", "mm", ""))
        self.assertEqual(no_private_suffix.extract("c.mm"), ("", "", "c.mm", ""))
        self.assertEqual(no_private_suffix.extract("b.c.mm"), ("", "b", "c.mm", "b.c.mm"))

    def test_us_k12(self):
        # k12.ak.us is a public TLD
        self.assertEqual(all_suffix.extract("ak.us"), ("", "", "ak.us", ""))
        self.assertEqual(
            all_suffix.extract("test.k12.ak.us"), ("", "test", "k12.ak.us", "test.k12.ak.us")
        )
        self.assertEqual(
            all_suffix.extract("www.test.k12.ak.us"), ("www", "test", "k12.ak.us", "test.k12.ak.us")
        )

        self.assertEqual(no_private_suffix.extract("ak.us"), ("", "", "ak.us", ""))
        self.assertEqual(
            no_private_suffix.extract("test.k12.ak.us"), ("", "test", "k12.ak.us", "test.k12.ak.us")
        )
        self.assertEqual(
            no_private_suffix.extract("www.test.k12.ak.us"),
            ("www", "test", "k12.ak.us", "test.k12.ak.us"),
        )

    def test_idn(self):
        self.assertEqual(all_suffix.extract("食狮.com.cn"), ("", "食狮", "com.cn", "食狮.com.cn"))

        self.assertEqual(no_private_suffix.extract("食狮.com.cn"), ("", "食狮", "com.cn", "食狮.com.cn"))

    def test_punycode(self):
        self.assertEqual(
            all_suffix.extract("xn--85x722f.com.cn"),
            ("", "xn--85x722f", "com.cn", "xn--85x722f.com.cn"),
        )

        self.assertEqual(
            no_private_suffix.extract("xn--85x722f.com.cn"),
            ("", "xn--85x722f", "com.cn", "xn--85x722f.com.cn"),
        )

    def test_scheme_port_path(self):
        # no_private_suffix
        no_private_suffix_asserts = [
            ("", "blogspot", "com", "blogspot.com"),
            ("google", "blogspot", "com", "blogspot.com"),
        ]
        self.assertEqual(
            no_private_suffix.extract("https://blogspot.com"), no_private_suffix_asserts[0]
        )
        self.assertEqual(
            no_private_suffix.extract("https://blogspot.com", subdomain=False),
            no_private_suffix_asserts[0],
        )

        self.assertEqual(
            no_private_suffix.extract("https://google.blogspot.com"), no_private_suffix_asserts[1]
        )
        self.assertEqual(
            no_private_suffix.extract("https://google.blogspot.com", subdomain=False),
            no_private_suffix_asserts[0],
        )
        self.assertEqual(
            no_private_suffix.extract("https://google.blogspot.com:8080"),
            no_private_suffix_asserts[1],
        )
        self.assertEqual(
            no_private_suffix.extract("https://google.blogspot.com:8080", subdomain=False),
            no_private_suffix_asserts[0],
        )
        self.assertEqual(
            no_private_suffix.extract(
                "ftp://google.blogspot.com:8080" "/a/long/path?query=42things"
            ),
            no_private_suffix_asserts[1],
        )
        self.assertEqual(
            no_private_suffix.extract(
                "ftp://google.blogspot.com:8080" "/a/long/path?query=42things", subdomain=False
            ),
            no_private_suffix_asserts[0],
        )

        # all_suffix
        all_suffix_asserts = [
            ("abc", "google", "blogspot.com", "google.blogspot.com"),
            ("", "google", "blogspot.com", "google.blogspot.com"),
            ("abc", "google", "blogspot.com", "google.blogspot.com"),
        ]
        self.assertEqual(
            all_suffix.extract("https://abc.google.blogspot.com"), all_suffix_asserts[0]
        )
        self.assertEqual(
            all_suffix.extract("https://abc.google.blogspot.com", subdomain=False),
            all_suffix_asserts[1],
        )

        self.assertEqual(
            all_suffix.extract("https://abc.google.blogspot.com"), all_suffix_asserts[2]
        )
        self.assertEqual(
            all_suffix.extract("https://abc.google.blogspot.com", subdomain=False),
            all_suffix_asserts[1],
        )
        self.assertEqual(
            all_suffix.extract("https://abc.google.blogspot.com:8080"), all_suffix_asserts[2]
        )
        self.assertEqual(
            all_suffix.extract("https://abc.google.blogspot.com:8080", subdomain=False),
            all_suffix_asserts[1],
        )
        self.assertEqual(
            all_suffix.extract("ftp://abc.google.blogspot.com:8080" "/a/long/path?query=42things"),
            all_suffix_asserts[2],
        )
        self.assertEqual(
            all_suffix.extract(
                "ftp://abc.google.blogspot.com:8080" "/a/long/path?query=42things", subdomain=False
            ),
            all_suffix_asserts[1],
        )

    def test_nested_dict(self):
        d = {}
        all_suffix.nested_dict(d, keys=["ac"])
        all_suffix.nested_dict(d, keys=["ac", "com"])
        all_suffix.nested_dict(d, keys=["ac", "edu"])
        all_suffix.nested_dict(d, keys=["ac", "gov"])
        all_suffix.nested_dict(d, keys=["ac", "net"])
        all_suffix.nested_dict(d, keys=["ac", "mil"])
        all_suffix.nested_dict(d, keys=["ac", "org"])

        all_suffix.nested_dict(d, keys=["ck", "*"])
        all_suffix.nested_dict(d, keys=["ck", "!www"])
        self.assertDictEqual(
            d,
            {
                "ac": {
                    "_END": True,
                    "com": True,
                    "edu": True,
                    "gov": True,
                    "net": True,
                    "mil": True,
                    "org": True,
                },
                "ck": {"*": True, "!www": True},
            },
        )


if __name__ == "__main__":
    unittest.main()

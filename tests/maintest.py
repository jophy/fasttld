from fasttld import FastTLDExtract
import unittest

all_suffix = FastTLDExtract(exclude_private_suffix=False)
no_private_suffix = FastTLDExtract(exclude_private_suffix=True)


class FastTLDExtractCase(unittest.TestCase):

    def test_all_suffix_trie(self):
        trie = all_suffix.trie
        self.assertEqual(trie['cn']['com'], True)
        self.assertEqual('blogspot' in trie['uk']['co'], True)
        self.assertEqual('*' in trie['uk'], False)
        self.assertEqual(trie['top'], True)
        self.assertEqual('_END' in trie['cn'], True)
        self.assertEqual(trie['ck']['*'], True)
        self.assertEqual(trie['ck']['!www'], True)
        self.assertEqual(trie['ir']['xn--mgba3a4f16a'], True)
        # private domain test
        self.assertEqual(trie['com']['appspot'], True)
        self.assertEqual(trie['ee']['com']['blogspot'], True)
        self.assertEqual(trie['com']['0emm']['*'], True)

    def test_no_private_domain_trie(self):
        trie = no_private_suffix.trie
        self.assertEqual(trie['cn']['com'], True)
        self.assertEqual(trie['uk']['co'], True)
        # private domain test
        self.assertEqual(trie['com'], True)  # *.0emm.com or the domains like hk.com, cn.com ,etc.
        self.assertEqual('no-ip.biz' in trie, False)
        self.assertEqual('github' in trie['io'], False)

    def test_no_private_suffix_extract(self):
        self.assertEqual(no_private_suffix.extract("www.myownblog.blogspot.ca"), ('www.myownblog', 'blogspot', 'ca',
                                                                                  'blogspot.ca'))
        self.assertEqual(no_private_suffix.extract("192.168.1.1.no-ip.co.uk"), ('192.168.1.1', 'no-ip', 'co.uk',
                                                                                'no-ip.co.uk'))

    def test_private_suffix_extract(self):
        self.assertEqual(all_suffix.extract("www.myownblog.blogspot.ca"), ('www', 'myownblog', 'blogspot.ca',
                                                                           'myownblog.blogspot.ca'))
        self.assertEqual(all_suffix.extract("192.168.1.1.no-ip.co.uk"), ('192.168.1', '1', 'no-ip.co.uk',
                                                                         '1.no-ip.co.uk'))

    def test_all_extract(self):
        todo = [
            "www.google.co.uk",
            "ditu.baidu.com.cn",
        ]
        assert_list = [
            ("www", "google", "co.uk", "google.co.uk"),
            ("ditu", "baidu", "com.cn", "baidu.com.cn"),
        ]
        asserts = map(all_suffix.extract, todo)
        for index, _a in enumerate(asserts):
            self.assertEqual(_a, assert_list[index])

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
            ('big.news', 'www', 'ck', 'www.ck'),
            ("", "", "abc.ck", ""),
            ("", "123", "abc.ck", "123.abc.ck"),
            ("foo", "123", "abc.ck", "123.abc.ck"),
        ]
        asserts = map(all_suffix.extract, todo)
        for index, _a in enumerate(asserts):
            self.assertEqual(_a, assert_list[index])

    def test_not_tld(self):
        self.assertEqual(all_suffix.extract("www.abc.noexists"), ('', '', '', ''))

    def test_only_dot_tld(self):
        self.assertEqual(all_suffix.extract(".com"), ('', '', 'com', ''))

    def test_one_rule(self):
        self.assertEqual(all_suffix.extract("domain.biz"), ('', 'domain', 'biz', 'domain.biz'))

    def test_only_one_wildcard(self):
        self.assertEqual(all_suffix.extract("mm"), ('', '', 'mm', ''))
        self.assertEqual(all_suffix.extract("c.mm"), ('', '', 'c.mm', ''))
        self.assertEqual(all_suffix.extract("b.c.mm"), ('', 'b', 'c.mm', 'b.c.mm'))

    def test_us_k12(self):
        self.assertEqual(all_suffix.extract("ak.us"), ('', '', 'ak.us', ''))
        self.assertEqual(all_suffix.extract("test.k12.ak.us"), ('', 'test', 'k12.ak.us', 'test.k12.ak.us'))
        self.assertEqual(all_suffix.extract("www.test.k12.ak.us"), ('www', 'test', 'k12.ak.us', 'test.k12.ak.us'))

    def test_punycode(self):
        self.assertEqual(all_suffix.extract("xn--85x722f.com.cn"), ('', 'xn--85x722f', 'com.cn', 'xn--85x722f.com.cn'))


if __name__ == '__main__':
    unittest.main()

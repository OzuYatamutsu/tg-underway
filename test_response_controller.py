from response_controller import generate_cate_response
from unittest import TestCase
from urllib.parse import quote


class TestResponseController(TestCase):
    def setUp(self):
        pass

    def test_generate_cate_response_alphanumeric(self):
        query_text = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
        )

        expected = (
            "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
            "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
            "０１２３４５６７８９"
        )

        self.assertEqual(
            generate_cate_response(query_text), expected
        )

    def test_generate_cate_response_symbolic(self):
        # / is not okay, thanks apache/Flask
        query_text = quote("!@#$%^&*()-=\"';:[]{}\\~`,.<>?", safe='')
        expected = "！＠＃＄％＾＆＊（）－＝＂＇；：［］｛｝＼～｀，．＜＞？"

        self.assertEqual(
            generate_cate_response(query_text), expected
        )

    def test_cate_response_does_not_cateify_emoji(self):
        query_text = "🥕🍆🗑️"
        expected = "🥕🍆🗑️"

        self.assertEqual(
            generate_cate_response(query_text), expected
        )

    def test_cate_response_does_not_cateify_mixed_out_of_range(self):
        query_text = "The 🥕 live outsidé of the code path米？"
        expected = "Ｔｈｅ　🥕　ｌｉｖｅ　ｏｕｔｓｉｄé　ｏｆ　ｔｈｅ　ｃｏｄｅ　ｐａｔｈ米？"

        self.assertEqual(
            generate_cate_response(query_text), expected
        )

    def tearDown(self):
        pass

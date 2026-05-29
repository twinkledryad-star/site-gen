import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_standard_case(self):
        md = """# My Page Title

Some paragraph text here."""

        extracted = extract_title(md)
        expected = "My Page Title"
        self.assertEqual(extracted, expected)

    def test_only_h2(self):
        md = """## Not my page title

Some paragraph text."""

        with self.assertRaises(Exception):
            extract_title(md)


    def test_many_spaces(self):
        md = """#    Lots of Space Around    

More content below."""
        extracted = extract_title(md)
        expected = "Lots of Space Around"
        self.assertEqual(extracted, expected)


    def test_h1_lower(self):
        md ="""Intro paragraph first.

## Section

# Actual Page Title

More content."""

        extracted = extract_title(md)
        expected = "Actual Page Title"
        self.assertEqual(extracted, expected)

    def test_empty(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_plain_text(self):
        md = "just a plain text with **bold** and _italic_ texts"
        with self.assertRaises(Exception):
            extract_title(md)
    


if __name__ == "__main__":
    unittest.main()
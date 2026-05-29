import unittest
from mdextract import extract_markdown_images, extract_markdown_links

class TestMDExtract(unittest.TestCase):

    # --- Image Extraction Tests ---

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_extract_images_multiple(self):
        text = "![img1](url1) and ![img2](url2)"
        expected = [("img1", "url1"), ("img2", "url2")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_extract_images_with_empty_alt(self):
        text = "An image with no alt text: ![](https://link.com/file.png)"
        expected = [("", "https://link.com/file.png")]
        self.assertListEqual(expected, extract_markdown_images(text))

    # --- Link Extraction Tests ---

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_extract_links_ignores_images(self):
        # Crucial test: images should NOT be detected as links
        text = "This is a [link](https://google.com) and an ![image](https://img.png)"
        expected = [("link", "https://google.com")]
        self.assertListEqual(expected, extract_markdown_links(text))

    # --- Edge Cases & Mixed Content ---

    def test_mixed_content(self):
        """Verify both extractors work correctly on the same complex string."""
        text = (
            "Check out [Boot Dev](https://www.boot.dev) for great courses. "
            "Here is a logo: ![Boot Dev Logo](https://www.boot.dev/logo.png). "
            "And another [link](https://google.com) for searching."
        )
        
        expected_links = [
            ("Boot Dev", "https://www.boot.dev"),
            ("link", "https://google.com")
        ]
        expected_images = [
            ("Boot Dev Logo", "https://www.boot.dev/logo.png")
        ]
        
        self.assertListEqual(expected_links, extract_markdown_links(text))
        self.assertListEqual(expected_images, extract_markdown_images(text))

    def test_broken_markdown(self):
        """Verify that incomplete markdown syntax returns no matches."""
        # Missing closing characters
        image_text = "![alt text(url.com)" 
        link_text = "[link text(url.com"    
        
        self.assertListEqual([], extract_markdown_images(image_text))
        self.assertListEqual([], extract_markdown_links(link_text))

    def test_no_markdown(self):
        """Verify behavior when no markdown is present."""
        text = "This is just plain text with no special formatting."
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

if __name__ == "__main__":
    unittest.main()
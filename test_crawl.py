import unittest
from crawl import normalize_url, get_heading_from_html
from crawl import get_first_paragraph_from_html
from crawl import get_urls_from_html, get_images_from_html
from crawl import extract_page_data

class TestCrawl(unittest.TestCase):
    def test_normalize_url_https_no_slash(self) -> None:
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_https_slash(self) -> None:
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_http_no_slash(self) -> None:
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_http_slash(self) -> None:
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_get_heading_h1h2(self) -> None:
        spew = "<html>\n  <body>\n"
        spew = spew + "    <h2>This is a fake target.</h2>\n"
        spew = spew + "    <h1>This is the real first target.</h1>\n"
        spew = spew + "    <main>\n"
        spew = spew + "      <p>This is the second target.</p>\n"
        spew = spew + "      <p>This should get missed.</p>\n"
        spew = spew + "    </main>\n"
        spew = spew + "  </body>"
        spew = spew + "</html>"
        actual1 = get_heading_from_html(spew)
        expected1 = "This is the real first target."
        actual2 = get_first_paragraph_from_html(spew)
        expected2 = "This is the second target."
        self.assertEqual(actual1,expected1)
        self.assertEqual(actual2,expected2)
    def test_get_heading_h1(self) -> None:
        spew = "<html>\n  <body>\n"
        spew = spew + "    <h1>This is the first target.</h1>\n"
        spew = spew + "    <main>\n"
        spew = spew + "      <p>This is the second target.</p>\n"
        spew = spew + "      <p>This should get missed.</p>\n"
        spew = spew + "    </main>\n"
        spew = spew + "  </body>"
        spew = spew + "</html>"
        actual1 = get_heading_from_html(spew)
        expected1 = "This is the first target."
        actual2 = get_first_paragraph_from_html(spew)
        expected2 = "This is the second target."
        self.assertEqual(actual1,expected1)
        self.assertEqual(actual2,expected2)
    def test_get_heading_h2(self) -> None:
        spew = "<html>\n  <body>\n"
        spew = spew + "    <h2>This is the first target.</h2>\n"
        spew = spew + "    <main>\n"
        spew = spew + "      <p>This is the second target.</p>\n"
        spew = spew + "      <p>This should get missed.</p>\n"
        spew = spew + "    </main>\n"
        spew = spew + "  </body>"
        spew = spew + "</html>"
        actual1 = get_heading_from_html(spew)
        expected1 = "This is the first target."
        actual2 = get_first_paragraph_from_html(spew)
        expected2 = "This is the second target."
        self.assertEqual(actual1,expected1)
        self.assertEqual(actual2,expected2)
    def test_get_urls_from_html_absolute(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com">'
        input_body = input_body + '<span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_relative(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one">'
        input_body = input_body + '<span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_both(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body>'
        input_body = input_body + '<a href="/path/one"><span>Boot.dev</span></a>'
        input_body = input_body + '<a href="https://other.com/path/one">'
        input_body = input_body + '<span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one",
                    "https://other.com/path/one"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_absolute(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body>'
        input_body = input_body + '<img src="https://crawler-test.com/logo.png" '
        input_body = input_body + 'alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_relative(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_multiple(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://cdn.boot.dev/banner.jpg"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://cdn.boot.dev/banner.jpg",
        ]
        self.assertEqual(actual, expected)
    def test_extract_page_data_basic(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
            }
        self.assertEqual(actual, expected)
    def test_extract_page_data_two_explicit_links(self) -> None:
        input_url = "https://crawler-test.com"
        Line2 = "Header 2"
        Line3A = "A paragraph with <i>italics</i>."
        Line3B = "A paragraph with italics."
        Line4A = "https://Fraud1.com"
        Line4B = "Link 1"
        Line5A = "https://Fraud2.com"
        Line5B = "Link 2"
        Line6A = "https://crawler-test.com/image.jpg"
        Line6B = "Image 1"
        myHTML = '<html><body>'
        myHTML = myHTML + '<h2>' + Line2 + '</h2>'
        myHTML = myHTML + '<p>' + Line3A + '</p>'
        myHTML = myHTML + '<p><a href="' + Line4A + '">'
        myHTML = myHTML + Line4B + '</a></p>'
        myHTML = myHTML + '<p><a href="' + Line5A + '">'
        myHTML = myHTML + Line5B + '</a></p>'
        myHTML = myHTML + '<img src="' + Line6A + '" '
        myHTML = myHTML + 'alt="' + Line6B + '">'
        myHTML = myHTML + '</body></html>'
        actual = extract_page_data(myHTML,input_url)
        self.assertEqual(actual["url"],input_url)
        self.assertEqual(actual["heading"],Line2)
        self.assertEqual(actual["first_paragraph"],Line3B)
        self.assertEqual(actual["outgoing_links"][0],Line4A)
        self.assertEqual(actual["outgoing_links"][1],Line5A)
        self.assertEqual(actual["image_urls"][0],Line6A)
    def test_extract_page_data_two_relative_links(self) -> None:
        input_url = "https://crawler-test.com"
        Line2 = "Header 2"
        Line3A = "A paragraph with <i>italics</i>."
        Line3B = "A paragraph with italics."
        Line4A = "/Fraud1"
        Line4B = "Link 1"
        Line4C = "https://crawler-test.com/Fraud1"
        Line5A = "/Fraud2"
        Line5B = "Link 2"
        Line5C = "https://crawler-test.com/Fraud2"
        Line6A = "https://crawler-test.com/image.jpg"
        Line6B = "Image 1"
        myHTML = '<html><body>'
        myHTML = myHTML + '<h2>' + Line2 + '</h2>'
        myHTML = myHTML + '<p>' + Line3A + '</p>'
        myHTML = myHTML + '<p><a href="' + Line4A + '">'
        myHTML = myHTML + Line4B + '</a></p>'
        myHTML = myHTML + '<p><a href="' + Line5A + '">'
        myHTML = myHTML + Line5B + '</a></p>'
        myHTML = myHTML + '<img src="' + Line6A + '" '
        myHTML = myHTML + 'alt="' + Line6B + '">'
        myHTML = myHTML + '</body></html>'
        actual = extract_page_data(myHTML,input_url)
        self.assertEqual(actual["url"],input_url)
        self.assertEqual(actual["heading"],Line2)
        self.assertEqual(actual["first_paragraph"],Line3B)
        self.assertEqual(actual["outgoing_links"][0],Line4C)
        self.assertEqual(actual["outgoing_links"][1],Line5C)
        self.assertEqual(actual["image_urls"][0],Line6A)
    def test_extract_page_data_two_explicit_images(self) -> None:
        input_url = "https://crawler-test.com"
        Line2 = "Header 2"
        Line3A = "A paragraph with <i>italics</i>."
        Line3B = "A paragraph with italics."
        Line4A = "https://Fraud1.com"
        Line4B = "Link 1"
        Line5A = "https://crawler-test.com/image1.jpg"
        Line5B = "Image 1"
        Line6A = "https://crawler-test.com/image2.jpg"
        Line6B = "Image 2"
        myHTML = '<html><body>'
        myHTML = myHTML + '<h2>' + Line2 + '</h2>'
        myHTML = myHTML + '<p>' + Line3A + '</p>'
        myHTML = myHTML + '<p><a href="' + Line4A + '">'
        myHTML = myHTML + Line4B + '</a></p>'
        myHTML = myHTML + '<img src="' + Line5A + '" '
        myHTML = myHTML + 'alt="' + Line5B + '">'
        myHTML = myHTML + '<img src="' + Line6A + '" '
        myHTML = myHTML + 'alt="' + Line6B + '">'
        myHTML = myHTML + '</body></html>'
        actual = extract_page_data(myHTML,input_url)
        self.assertEqual(actual["url"],input_url)
        self.assertEqual(actual["heading"],Line2)
        self.assertEqual(actual["first_paragraph"],Line3B)
        self.assertEqual(actual["outgoing_links"][0],Line4A)
        self.assertEqual(actual["image_urls"][0],Line5A)
        self.assertEqual(actual["image_urls"][1],Line6A)
    def test_extract_page_data_two_relative_images(self) -> None:
        input_url = "https://crawler-test.com"
        Line2 = "Header 2"
        Line3A = "A paragraph with <b>boldface</b>."
        Line3B = "A paragraph with boldface."
        Line4A = "/Fraud1"
        Line4B = "Link 1"
        Line4C = "https://crawler-test.com/Fraud1"
        Line5A = "/image1.jpg"
        Line5B = "Image 1"
        Line5C = "https://crawler-test.com/image1.jpg"
        Line6A = "/image2.jpg"
        Line6B = "Image 2"
        Line6C = "https://crawler-test.com/image2.jpg"
        myHTML = '<html><body>'
        myHTML = myHTML + '<h2>' + Line2 + '</h2>'
        myHTML = myHTML + '<p>' + Line3A + '</p>'
        myHTML = myHTML + '<p><a href="' + Line4A + '">'
        myHTML = myHTML + Line4B + '</a></p>'
        myHTML = myHTML + '<img src="' + Line5A + '" '
        myHTML = myHTML + 'alt="' + Line5B + '">'
        myHTML = myHTML + '<img src="' + Line6A + '" '
        myHTML = myHTML + 'alt="' + Line6B + '">'
        myHTML = myHTML + '</body></html>'
        actual = extract_page_data(myHTML,input_url)
        self.assertEqual(actual["url"],input_url)
        self.assertEqual(actual["heading"],Line2)
        self.assertEqual(actual["first_paragraph"],Line3B)
        self.assertEqual(actual["outgoing_links"][0],Line4C)
        self.assertEqual(actual["image_urls"][0],Line5C)
        self.assertEqual(actual["image_urls"][1],Line6C)
    def test_extract_page_data_no_header(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
            }
        self.assertEqual(actual, expected)
    def test_extract_page_data_no_paragraph(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>This is the header.</h1>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "This is the header.",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
            }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
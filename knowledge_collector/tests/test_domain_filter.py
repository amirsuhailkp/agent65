"""Unit tests for same-website domain filtering."""

import unittest

from crawler.domain_filter import DomainFilter


class DomainFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.filter = DomainFilter()

    def test_accepts_only_same_website_urls(self) -> None:
        candidates = [
            "https://owasp.org/Top10/",
            "https://owasp.org/www-project-top-ten/",
            "https://github.com",
            "https://youtube.com/watch?v=abc",
            "https://linkedin.com/company/owasp",
        ]

        filtered = self.filter.filter_same_website_urls(
            current_domain="owasp.org",
            candidate_urls=candidates,
        )

        self.assertEqual(
            filtered,
            [
                "https://owasp.org/Top10",
                "https://owasp.org/www-project-top-ten",
            ],
        )

    def test_rejects_non_html_file_extensions(self) -> None:
        candidates = [
            "https://owasp.org/files/guide.pdf",
            "https://owasp.org/image.png",
            "https://owasp.org/image.jpg",
            "https://owasp.org/image.jpeg",
            "https://owasp.org/image.gif",
            "https://owasp.org/logo.svg",
            "https://owasp.org/archive.zip",
            "https://owasp.org/archive.rar",
            "https://owasp.org/archive.7z",
            "https://owasp.org/file.doc",
            "https://owasp.org/file.docx",
            "https://owasp.org/slides.ppt",
            "https://owasp.org/slides.pptx",
            "https://owasp.org/setup.exe",
            "https://owasp.org/disk.iso",
            "https://owasp.org/articles/top-ten",
        ]

        filtered = self.filter.filter_same_website_urls(
            current_domain="owasp.org",
            candidate_urls=candidates,
        )

        self.assertEqual(filtered, ["https://owasp.org/articles/top-ten"])

    def test_accepts_subdomains_and_deduplicates_normalized_urls(self) -> None:
        candidates = [
            "https://docs.owasp.org/page",
            "HTTPS://DOCS.OWASP.ORG:443/page#section",
            "https://www.owasp.org/page/",
        ]

        filtered = self.filter.filter_same_website_urls(
            current_domain="https://owasp.org",
            candidate_urls=candidates,
        )

        self.assertEqual(
            filtered,
            [
                "https://docs.owasp.org/page",
                "https://owasp.org/page",
            ],
        )

    def test_rejects_invalid_candidates_and_invalid_current_domain(self) -> None:
        candidates = [
            "",
            "   ",
            "mailto:security@owasp.org",
            "javascript:void(0)",
            "ftp://owasp.org/file",
            "https://owasp.org/ok",
        ]

        filtered = self.filter.filter_same_website_urls(
            current_domain="owasp.org",
            candidate_urls=candidates,
        )
        self.assertEqual(filtered, ["https://owasp.org/ok"])

        with self.assertRaises(ValueError):
            self.filter.filter_same_website_urls(current_domain="", candidate_urls=[])


if __name__ == "__main__":
    unittest.main()

import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from check_issue_link import check_issue_link


class IssueLinkTest(unittest.TestCase):
    @patch.dict(os.environ, {
        "GITHUB_API_URL": "https://api.github.com",
        "GITHUB_REPOSITORY": "example/demo",
        "PR_NUMBER": "5",
    })
    @patch("check_issue_link.github_get")
    def test_latest_body_must_reference_a_real_issue(self, api):
        issue = {
            "number": 4,
            "repository_url": "https://api.github.com/repos/example/demo",
        }
        for body in ("Refs #4", "Closes #4", "Fixes: #4", "resolves #4\r\n"):
            with self.subTest(body=body):
                api.reset_mock()
                api.side_effect = [{"body": body}, issue]
                self.assertEqual(check_issue_link(), [4])
                self.assertEqual([call.args[0] for call in api.call_args_list], ["pulls/5", "issues/4"])

        # Removing the reference must fail even when the commit has not changed.
        for body in (None, "", "Refs #", "Related: #4", "Refs example/other#4"):
            with self.subTest(body=body):
                api.reset_mock()
                api.side_effect = [{"body": body}]
                with self.assertRaises(ValueError):
                    check_issue_link()
                api.assert_called_once_with("pulls/5")

        for target in (
            {**issue, "pull_request": {}},
            {**issue, "repository_url": "https://api.github.com/repos/example/other"},
            {**issue, "number": 6},
            HTTPError("https://api.github.com/repos/example/demo/issues/4", 404, "Not Found", {}, None),
            HTTPError("https://api.github.com/repos/example/demo/issues/4", 403, "Forbidden", {}, None),
        ):
            with self.subTest(target=target):
                api.side_effect = [{"body": "Refs #4"}, target]
                with self.assertRaises((ValueError, HTTPError)):
                    check_issue_link()


if __name__ == "__main__":
    unittest.main()

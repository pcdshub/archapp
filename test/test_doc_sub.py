import unittest
from difflib import Differ
from archapp.util.doc_sub import doc_sub

sanity = \
"""
text text text
     text
"""

indent = \
"""
flop flop flop
fish one two
     three four
"""

expected = \
            """
            text text text
                 text
                 flop flop flop
                 fish one two
                      three four
            """

class DocSubTestCase(unittest.TestCase):
    def test_doc_sub_basic(self):
        @doc_sub(sanity=sanity, indent=indent)
        def test_function():
            """
            {sanity}
                 {indent}
            """
            pass
        err = "DocSub broken. Expected \n{0}\n, got \n{1}\n. Diff:{2}"
        diff = Differ()
        self.assertEqual(expected, test_function.__doc__,
            err.format(expected, test_function.__doc__,
                "".join(
                    [d for d in diff.compare(
                            expected.splitlines(1),
                            test_function.__doc__.splitlines(1)
                            )
                        ]
                    )
                )
            )

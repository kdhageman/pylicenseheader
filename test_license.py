import os
import tempfile
import unittest

from license import traversedir


class TestLicense(unittest.TestCase):
    def test_license(self):
        existing_content = '''func() main {
    // ignore
    // ignore some more!
    a := "this is a string"
    println(a)
}'''
        existing_len = len(existing_content.split("\n"))
        prefix = "//"
        inserted_line = "Changed\n"

        fd, tmpfile = tempfile.mkstemp(suffix=".go")
        tmpdir = os.path.dirname(tmpfile)

        try:
            with open(tmpfile, "w") as f:
                f.write(existing_content)

            with open("header.txt") as f:
                license = f.readlines()
                headerlen = len(license)
                traversedir(tmpdir, prefix, license)

            with open(tmpfile) as f:
                content = f.read()
                contentlen = len(content.split("\n"))
                self.assertTrue(content.startswith(prefix))
                self.assertTrue(content.endswith(existing_content))
                self.assertEqual(contentlen, headerlen + 1 + existing_len)

            license[0] = inserted_line

            traversedir(tmpdir, prefix, license)

            with open(tmpfile) as f:
                content = f.read()
                expected_start = prefix + " " + inserted_line
                self.assertTrue(content.startswith(expected_start))
                self.assertTrue(content.endswith(existing_content))
                self.assertEqual(contentlen, headerlen + 1 + existing_len)
        finally:
            os.remove(tmpfile)


if __name__ == '__main__':
    unittest.main()

from pathlib import Path

import pytest

from usethis._core.badge import Badge, add_badge, remove_badge
from usethis._test import change_cwd


class TestAddBadge:
    def test_empty(self, tmp_path: Path, capfd: pytest.CaptureFixture[str]):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)"
                ),
            )

        # Assert
        assert (
            path.read_text()
            == """\
![Licence](<https://img.shields.io/badge/licence-mit-green>)
"""
        )
        out, err = capfd.readouterr()
        assert not err
        assert out == "✔ Adding Licence badge to 'README.md'.\n"

    def test_only_newline(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\

""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)"
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
![Licence](<https://img.shields.io/badge/licence-mit-green>)
"""
        )

    def test_predecessor(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)",
                )
            )

        # Assert
        content = path.read_text()
        assert (
            content
            == """\
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)
"""
        )

    def test_not_predecessor(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)",
                )
            )

        # Assert
        content = path.read_text()
        assert (
            content
            == """\
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)
"""
        )

    def test_not_recognized_gets_put_after_known_order(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Don't Know What This Is](<https://example.com>)",
                )
            )

        # Assert
        content = path.read_text()
        assert (
            content
            == """\
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
![Don't Know What This Is](<https://example.com>)
"""
        )

    def test_skip_header1(self, tmp_path: Path, capfd: pytest.CaptureFixture[str]):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
# Header
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
# Header

![Licence](<https://img.shields.io/badge/licence-mit-green>)
"""
        )
        out, err = capfd.readouterr()
        assert not err
        assert out == "✔ Adding Licence badge to 'README.md'.\n"

    def test_skip_header2(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
## Header
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
## Header

![Licence](<https://img.shields.io/badge/licence-mit-green>)
"""
        )

    def test_skip_header_with_extra_newline(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
# Header

""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
# Header

![Licence](<https://img.shields.io/badge/licence-mit-green>)
"""
        )

    def test_extra_unstripped_space(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
  # Header  
  
 [![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)",
                )
            )

        # Assert
        content = path.read_text()
        assert (
            content
            == """\
  # Header  
  
 [![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)
"""
        )

    def test_already_exists(self, tmp_path: Path, capfd: pytest.CaptureFixture[str]):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
![Licence](<https://img.shields.io/badge/licence-mit-green>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
![Licence](<https://img.shields.io/badge/licence-mit-green>)
"""
        )
        out, err = capfd.readouterr()
        assert not err
        assert not out

    def test_badge_followed_by_text(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
# Header

Some text
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
# Header

![Licence](<https://img.shields.io/badge/licence-mit-green>)

Some text
"""
        )

    def test_predecessor_based_on_name(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
![Ruff](<https://example.com>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![pre-commit](<https://example.com>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
![Ruff](<https://example.com>)
![pre-commit](<https://example.com>)
"""
        )

    def test_recognized_gets_put_before_unknown(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
![Don't Know What This Is](<https://example.com>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="![Ruff](<https://example.com>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
![Ruff](<https://example.com>)
![Don't Know What This Is](<https://example.com>)
"""
        )

    def test_already_exists_no_newline_added(self, tmp_path: Path):
        # Arrange
        path = tmp_path / Path("README.md")
        content = """![Ruff](<https://example.com>)"""
        path.write_text(content)

        # Act
        with change_cwd(tmp_path):
            add_badge(Badge(markdown="![Ruff](<https://example.com>)"))

        # Assert
        assert path.read_text() == content

    def test_no_unnecessary_spaces(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
# usethis

[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)

Automate Python project setup and development tasks that are otherwise performed manually.
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)",
                )
            )

        # Assert
        content = path.read_text()
        assert (
            content
            == """\
# usethis

[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)

Automate Python project setup and development tasks that are otherwise performed manually.
"""
        )

    def test_already_exists_out_of_order(
        self, tmp_path: Path, capfd: pytest.CaptureFixture[str]
    ):
        # Arrange
        path = tmp_path / "README.md"
        content = """\
[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
"""
        path.write_text(content)

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)",
                )
            )

        # Assert
        assert path.read_text() == content
        out, err = capfd.readouterr()
        assert not err
        assert not out

    def test_skip_html_block(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
<h1 align="center">
  <img src="doc/logo.svg"><br>
</h1>

# usethis
                        
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)"
                )
            )

        # Assert
        content = path.read_text()
        assert (
            content
            == """\
<h1 align="center">
  <img src="doc/logo.svg"><br>
</h1>

# usethis
                        
[![Ruff](<https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>)](<https://github.com/astral-sh/ruff>)
[![pre-commit](<https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit>)](<https://github.com/pre-commit/pre-commit>)
"""
        )

    def test_add_to_no_file_extension_readme(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README"
        path.write_text("""\
# usethis
""")

        # Act
        with change_cwd(tmp_path):
            add_badge(
                Badge(
                    markdown="[![Ruff](<https://example.com>)](<https://example.com>)",
                )
            )

        # Assert
        assert not path.with_suffix(".md").exists()
        assert (
            path.read_text()
            == """\
# usethis

[![Ruff](<https://example.com>)](<https://example.com>)
"""
        )


class TestRemoveBadge:
    def test_empty(self, tmp_path: Path, capfd: pytest.CaptureFixture[str]):
        # Arrange
        path = tmp_path / "README.md"
        path.touch()

        # Act
        with change_cwd(tmp_path):
            remove_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        content = path.read_text()
        assert not content
        out, err = capfd.readouterr()
        assert not err
        assert not out

    def test_single(self, tmp_path: Path, capfd: pytest.CaptureFixture[str]):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
![Licence](<https://img.shields.io/badge/licence-mit-green>)
""")

        # Act
        with change_cwd(tmp_path):
            remove_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        content = path.read_text()
        assert content == "\n"
        out, err = capfd.readouterr()
        assert not err
        assert out == "✔ Removing Licence badge from 'README.md'.\n"

    def test_no_reademe_file(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"

        # Act
        with change_cwd(tmp_path):
            remove_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert not path.exists()

    def test_header_and_text(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
# Header

![Licence](<https://img.shields.io/badge/licence-mit-green>)
                        
And some text
""")

        # Act
        with change_cwd(tmp_path):
            remove_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
# Header

And some text
"""
        )

    def test_multiple_badges(self, tmp_path: Path):
        # Arrange
        path = tmp_path / "README.md"
        path.write_text("""\
![Ruff](<https://example.com>)
![pre-commit](<https://example.com>)
""")

        # Act
        with change_cwd(tmp_path):
            remove_badge(
                Badge(
                    markdown="![Ruff](<https://example.com>)",
                )
            )

        # Assert
        assert (
            path.read_text()
            == """\
![pre-commit](<https://example.com>)
"""
        )

    def test_no_badges_but_header_and_text(self, tmp_path: Path):
        # Arrange
        path = tmp_path / Path("README.md")
        content = """\
# Header

And some text
"""
        path.write_text(content)

        # Act
        with change_cwd(tmp_path):
            remove_badge(
                Badge(
                    markdown="![Licence](<https://img.shields.io/badge/licence-mit-green>)",
                )
            )

        # Assert
        assert path.read_text() == content

    def test_already_exists_no_newline_added(self, tmp_path: Path):
        # Arrange
        path = tmp_path / Path("README.md")
        content = """Nothing will be removed"""
        path.write_text(content)

        # Act
        with change_cwd(tmp_path):
            remove_badge(Badge(markdown="![Ruff](<https://example.com>)"))

        # Assert
        assert path.read_text() == content

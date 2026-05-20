from pathlib import Path


def test_package_structure_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "setup.py").is_file()
    assert (root / "toutatis" / "core.py").is_file()

"""
Tests for image_to_pdf.py

GUI modules are mocked before import so no display is required.
ctk.CTk and TkinterDnD.DnDWrapper must be real classes (not MagicMocks)
because they are used as base classes inside the module.
"""
import sys
import os
import tempfile
import pytest
from unittest.mock import MagicMock
from PIL import Image


# --- GUI mocks (must happen before importing image_to_pdf) ---------------

class _FakeTk:
    def __init__(self, *args, **kwargs): pass
    def __getattr__(self, name): return MagicMock()

class _FakeDnDWrapper:
    pass

_mock_ctk = MagicMock()
_mock_ctk.CTk = _FakeTk

_mock_tkinterdnd2 = MagicMock()
_mock_tkinterdnd2.TkinterDnD = MagicMock()
_mock_tkinterdnd2.TkinterDnD.DnDWrapper = _FakeDnDWrapper
_mock_tkinterdnd2.DND_FILES = "DND_FILES"

sys.modules.setdefault("customtkinter", _mock_ctk)
sys.modules.setdefault("tkinterdnd2", _mock_tkinterdnd2)
sys.modules.setdefault("tkinter", MagicMock())
sys.modules.setdefault("tkinter.messagebox", MagicMock())
sys.modules.setdefault("tkinter.filedialog", MagicMock())
sys.modules.setdefault("PIL.ImageTk", MagicMock())

# Make `from PIL import ImageTk` return the mock
import PIL
PIL.ImageTk = sys.modules["PIL.ImageTk"]

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_to_pdf import ImageToPDFApp  # noqa: E402


# --- Fixtures ------------------------------------------------------------

@pytest.fixture
def app():
    return ImageToPDFApp()


@pytest.fixture
def tmp_images(tmp_path):
    paths = []
    for name in ("a.png", "b.png", "c.png"):
        img = Image.new("RGB", (10, 10), color=(255, 0, 0))
        p = str(tmp_path / name)
        img.save(p)
        paths.append(p)
    return paths


# --- add_files -----------------------------------------------------------

def test_add_files_accepts_valid_extensions(app, tmp_images):
    app.add_files(tmp_images)
    assert app.file_paths == tmp_images


def test_add_files_rejects_invalid_extensions(app, tmp_path):
    txt = str(tmp_path / "doc.txt")
    open(txt, "w").close()
    app.add_files([txt])
    assert app.file_paths == []


def test_add_files_deduplicates(app, tmp_images):
    app.add_files(tmp_images)
    app.add_files(tmp_images)  # add same files again
    assert len(app.file_paths) == len(tmp_images)


def test_add_files_appends_thumbnail_per_file(app, tmp_images):
    app.add_files(tmp_images)
    assert len(app.thumbnails) == len(tmp_images)


# --- remove_image --------------------------------------------------------

def test_remove_image_removes_correct_entry(app, tmp_images):
    app.add_files(tmp_images)
    app.remove_image(tmp_images[1])
    assert tmp_images[1] not in app.file_paths
    assert len(app.file_paths) == 2
    assert len(app.thumbnails) == 2


def test_remove_image_ignores_unknown_path(app, tmp_images):
    app.add_files(tmp_images)
    app.remove_image("/nonexistent/path.png")
    assert len(app.file_paths) == len(tmp_images)


# --- move_image ----------------------------------------------------------

def test_move_image_down(app, tmp_images):
    app.add_files(tmp_images)
    app.move_image(0, 1)
    assert app.file_paths[0] == tmp_images[1]
    assert app.file_paths[1] == tmp_images[0]


def test_move_image_up(app, tmp_images):
    app.add_files(tmp_images)
    app.move_image(1, -1)
    assert app.file_paths[0] == tmp_images[1]
    assert app.file_paths[1] == tmp_images[0]


def test_move_image_out_of_bounds_is_noop(app, tmp_images):
    app.add_files(tmp_images)
    original = list(app.file_paths)
    app.move_image(0, -1)   # already first
    app.move_image(len(tmp_images) - 1, 1)  # already last
    assert app.file_paths == original


def test_move_image_keeps_thumbnail_in_sync(app, tmp_images):
    app.add_files(tmp_images)
    thumb_first = app.thumbnails[0]
    thumb_second = app.thumbnails[1]
    app.move_image(0, 1)
    assert app.thumbnails[0] == thumb_second
    assert app.thumbnails[1] == thumb_first


# --- clear_images --------------------------------------------------------

def test_clear_images_empties_both_lists(app, tmp_images):
    app.add_files(tmp_images)
    app.clear_images()
    assert app.file_paths == []
    assert app.thumbnails == []


# --- integration: _convert_worker creates a valid PDF -------------------

def test_convert_worker_creates_pdf(app, tmp_images, tmp_path):
    app.add_files(tmp_images)
    out = str(tmp_path / "output.pdf")
    app._convert_worker(out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0

import json
import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "extract_merge_gpt3.5.py"
spec = importlib.util.spec_from_file_location("extract_merge_gpt3_5", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

extract_text = mod.extract_text
get_newest_file = mod.get_newest_file


def test_extract_text_reads_choices(tmp_path):
    sample = {
        "choices": [
            {"message": {"role": "assistant", "content": "Hello\n\nWorld"}},
            {"message": {"role": "assistant", "content": "Another\n\nResponse"}},
            {"message": {"role": "user", "content": "Ignored"}},
        ]
    }
    input_file = tmp_path / "sample.json"
    input_file.write_text(json.dumps(sample))

    result = extract_text(str(input_file))

    assert result == ["Hello\nWorld", "Another\nResponse"]


def test_get_newest_file_empty(tmp_path):
    assert get_newest_file(str(tmp_path)) is None


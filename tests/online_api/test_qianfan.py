import sys
from pathlib import Path
root_path = Path(__file__).parent.parent.parent
sys.path.append(str(root_path))

from server.model_workers.qianfan import request_qianfan_api, MODEL_VERSIONS
from pprint import pprint
import pytest


@pytest.mark.parametrize("version", list(MODEL_VERSIONS.keys())[:2])
def test_qianfan(version):
    messages = [{"role": "user", "content": "你好"}]
    print("\n" + version + "\n")
    for i, x in enumerate(request_qianfan_api(messages, version=version), start=1):
        pprint(x)
        assert isinstance(x, dict)
        assert "error_code" not in x

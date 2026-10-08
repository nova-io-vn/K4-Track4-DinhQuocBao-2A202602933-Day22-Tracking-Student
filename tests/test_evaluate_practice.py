"""Kiểm thử script chấm mà không cần cài hoặc chạy TrackEval thật."""

from pathlib import Path
from unittest.mock import patch

from evaluate_practice import run_trackeval


def test_run_trackeval_patches_numpy_in_child_process() -> None:
    """Bản vá alias NumPy phải được thực thi trong tiến trình TrackEval."""
    with patch("evaluate_practice.subprocess.run") as run_mock:
        run_trackeval(Path("TrackEval"), "lan_thu", "LAB21", "train")

    cmd = run_mock.call_args.args[0]
    assert cmd[1] == "-c"
    assert "np.float = float" in cmd[2]
    assert "run_mot_challenge.py" in cmd[2]
    assert "--TRACKERS_TO_EVAL" in cmd
    assert "lan_thu" in cmd
    run_mock.assert_called_once_with(cmd, check=True)

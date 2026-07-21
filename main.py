"""Capture one frame, publish its mean RGB values, and upload the frame."""

import argparse
import os
from pathlib import Path
from typing import Optional, Sequence, Union

import numpy as np
from waggle.data.vision import Camera
from waggle.plugin import Plugin


DEFAULT_CAMERA = "left"
DEFAULT_SNAPSHOT_PATH = "/tmp/snapshot.jpg"


def compute_mean_color(image: np.ndarray) -> np.ndarray:
    """Return the per-channel mean for an image."""
    if image is None or image.ndim < 3 or image.shape[2] < 3:
        raise ValueError("expected an image with at least three color channels")
    return np.mean(image[:, :, :3], axis=(0, 1)).astype(float)


def camera_source(value: str) -> Union[int, str, Path]:
    """Resolve numeric indexes and local paths while preserving node aliases."""
    if value.isdecimal():
        return int(value)
    path = Path(value)
    return path if path.is_file() else value


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--camera",
        default=os.getenv("SAGE_CAMERA", DEFAULT_CAMERA),
        help="node camera alias, local numeric index, URL, or existing image path",
    )
    parser.add_argument(
        "--snapshot-path",
        default=os.getenv("SAGE_SNAPSHOT_PATH", DEFAULT_SNAPSHOT_PATH),
        help="temporary path used before uploading the captured frame",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    source = camera_source(args.camera)
    snapshot_path = Path(args.snapshot_path)

    with Plugin() as plugin:
        with Camera(source) as camera:
            snapshot = camera.snapshot()

        mean_color = compute_mean_color(snapshot.data)
        plugin.publish("color.mean.r", float(mean_color[0]), timestamp=snapshot.timestamp)
        plugin.publish("color.mean.g", float(mean_color[1]), timestamp=snapshot.timestamp)
        plugin.publish("color.mean.b", float(mean_color[2]), timestamp=snapshot.timestamp)

        snapshot.save(str(snapshot_path))
        plugin.upload_file(str(snapshot_path), timestamp=snapshot.timestamp)


if __name__ == "__main__":
    main()

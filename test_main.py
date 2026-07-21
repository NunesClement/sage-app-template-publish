import unittest
from unittest.mock import MagicMock, call, patch

import numpy as np

import main


class MeanColorTests(unittest.TestCase):
    def test_compute_mean_color(self):
        image = np.array(
            [
                [[10, 20, 30], [30, 40, 50]],
                [[50, 60, 70], [70, 80, 90]],
            ],
            dtype=np.uint8,
        )

        np.testing.assert_allclose(main.compute_mean_color(image), [40.0, 50.0, 60.0])


class AppTests(unittest.TestCase):
    @patch("main.Camera")
    @patch("main.Plugin")
    def test_main_publishes_channels_and_uploads_snapshot(self, plugin_class, camera_class):
        plugin = plugin_class.return_value.__enter__.return_value
        camera = camera_class.return_value.__enter__.return_value
        snapshot = MagicMock()
        snapshot.data = np.array([[[1, 2, 3], [3, 4, 5]]], dtype=np.uint8)
        snapshot.timestamp = 123456789
        camera.snapshot.return_value = snapshot

        main.main()

        camera_class.assert_called_once_with("bottom_image")
        plugin.publish.assert_has_calls(
            [
                call("color.mean.r", 2.0, timestamp=123456789),
                call("color.mean.g", 3.0, timestamp=123456789),
                call("color.mean.b", 4.0, timestamp=123456789),
            ]
        )
        snapshot.save.assert_called_once_with("snapshot.jpg")
        plugin.upload_file.assert_called_once_with("snapshot.jpg", timestamp=123456789)


if __name__ == "__main__":
    unittest.main()

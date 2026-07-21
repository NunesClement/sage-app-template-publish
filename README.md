# Sage Mean Color Edge App

This repository is a Sage edge app built directly at the repository root from the official edge-app tutorial. It captures one camera frame, publishes its mean red, green, and blue values, and uploads the frame with the same timestamp.

## Repository layout

- `main.py` — application entry point
- `test_main.py` — unit tests for the calculation and publish/upload flow
- `requirements.txt` — pinned Python dependencies
- `Dockerfile` — Sage plugin image build
- `sage.yaml` — root ECR metadata and version
- `ecr-meta/` — the three ECR publication assets required by Sage

## Local setup and test

Use an isolated environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --requirement requirements.txt
python3 -m unittest -v
```

The application uses the Sage node camera alias `left`, matching the tutorial's node-specific correction. Run the camera integration test on a Sage node; local unit tests mock the camera and publication interfaces.

## Sage node test (run on an assigned node)

Do not install the Python requirements directly on a Sage node. Clone this repository there and use the node's `pluginctl` container workflow:

The Dockerfile currently uses the official cookiecutter's NVIDIA Jetson Xavier tutorial base (`waggle/plugin-base:1.1.1-ml`). Confirm the development node model before building. Jetson Thor nodes require the Thor base selected by the current cookiecutter; the CPU architectures listed in `sage.yaml` do not make the JetPack-specific bases interchangeable.

```sh
sudo pluginctl --help
sudo pluginctl build .
sudo pluginctl run --name sage-app-template-publish <image-reference-printed-by-build>
```

The installed `pluginctl --help` output is authoritative if the node's syntax differs. The hard-coded `left` alias must be changed in `main.py` if the node exposes a different camera name.

## ECR publication

The root `sage.yaml` version is the ECR release version and cannot be reused for a later rebuild. After this repository is public and pushed to GitHub, register its GitHub URL from Sage Portal → My Apps → Create App. Wait for the build status to become **Built**, then use the app's **Tags** tab for its registry reference.

See the [creating](https://sagecontinuum.org/docs/tutorials/edge-apps/creating-an-edge-app), [testing](https://sagecontinuum.org/docs/tutorials/edge-apps/testing-an-edge-app), and [publishing](https://sagecontinuum.org/docs/tutorials/edge-apps/publishing-to-ecr) guides.

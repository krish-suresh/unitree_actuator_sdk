# Python Packaging Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan.

**Goal:** Install the SDK into other projects with uv from a local checkout, a wheel, a source distribution, or the GitHub fork.

**Architecture:** Use scikit-build-core and the existing CMake/pybind11 binding. Install the extension at the wheel root and the matching native SDK library in `unitree_actuator_sdk.libs/`, located through an origin-relative runtime search path. Preserve the existing import and standalone CMake workflow.

**Tech Stack:** pyproject.toml, scikit-build-core, CMake, C++14, CPython, uv.

**Spec:** The user requested a valid Python package for uv installation from other projects. Publishing source changes to their existing fork remains authorized by the preceding request.

## Global Constraints

- Keep `import unitree_actuator_sdk` and the existing public API.
- Support the supplied Linux x86-64 and ARM64 native libraries; reject unsupported platforms clearly.
- Include the selected native library and both dependency licenses in the wheel.
- Build the extension for the consuming project's Python; do not ship old extension binaries in source distributions.
- Retain standalone CMake builds, examples, and hardware-free tests.
- Do not open serial ports or operate motors during verification.

## Review Focus

- Installed modules must load the bundled native library without this checkout or LD_LIBRARY_PATH.
- Wheel builds must not write into the source checkout.
- Source distributions must include every build input and omit generated extensions.
- A fresh uv project must resolve and install the Git dependency with Python 3.13.
- Python 3.12 installation and standalone CMake tests must continue to pass.

## Task 1: Package and verify

- Reproduce uv rejecting the current repository as a Python package.
- Add an installed-package test for distribution metadata, module location, native library location, and public API calls.
- Add pyproject.toml and CMake install rules with origin-relative library lookup.
- Document Git, local, wheel, and source-distribution use; ignore packaging output.
- Build a wheel from an sdist, inspect archive contents, and install with uv into fresh Python 3.13 and 3.12 environments.
- Test imports from outside the repository and repeat standalone CMake tests.
- Review, commit, and push to the user's fork; verify a fresh Git-source uv project against the pushed commit.

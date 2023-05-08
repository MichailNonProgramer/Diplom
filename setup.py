import os.path
import sys

import setuptools

root_dir = os.path.abspath(os.path.dirname(__file__))

if sys.platform == "win32":
    extra_compile_args = []
    libraries = ["libcrypto", "advapi32", "crypt32", "gdi32", "user32", "ws2_32"]
else:
    extra_compile_args = ["-std=c99"]
    libraries = ["crypto"]

setuptools.setup(
    name="__title__",
    version="0.9.20",
    description="__summary__",
    long_description="descr",
    url="__uri__",
    author="__author__",
    author_email="__email__",
    license="__license__",
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
    ],
    ext_modules=[
        setuptools.Extension(
            "aioquic._buffer",
            extra_compile_args=extra_compile_args,
            sources=["src/aioquic/_buffer.c"],
        ),
        setuptools.Extension(
            "aioquic._crypto",
            extra_compile_args=extra_compile_args,
            libraries=libraries,
            sources=["src/aioquic/_crypto.c"],
        ),
    ],
    package_dir={"": "src"},
    package_data={"aioquic": ["py.typed", "_buffer.pyi", "_crypto.pyi"]},
    packages=["aioquic", "aioquic.asyncio", "aioquic.h0", "aioquic.h3", "aioquic.quic"],
    install_requires=[
        "certifi",
        "cryptography >= 3.1",
        "pylsqpack >= 0.3.3, < 0.4.0",
        "pyopenssl >= 20, < 22",
    ],
)

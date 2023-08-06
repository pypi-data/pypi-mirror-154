import setuptools

setuptools.setup(
    name="Alto_updateStatus",
    version="0.0.2",
    author="Kanokpich",
    description="Execute PATCH api to update service status",
    packages=["updateStatus"],
    install_requires=["requests"]
)
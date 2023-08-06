import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="TK_log",
    version="0.0.1",
    author="ravi",
    author_email="ravi.masna@talentkind.com",
    packages=["TK_log"],
    description="Package to log user activity",
    long_description="description",
    long_description_content_type="text/markdown",
    url="",
    license='MIT',
    python_requires='>=3.9',
    install_requires=[]
)

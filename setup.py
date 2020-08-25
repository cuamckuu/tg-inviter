import setuptools


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

with open("readme.md", "r") as fh:
    long_description = fh.read()

install_reqs = parse_requirements("./requirements.txt")

setuptools.setup(
    name="tg-inviter",
    version="0.1",
    author="Alex Kosh",
    author_email="sasha23969@mail.ru",
    description="Package to generate and process personal invites link in Telegram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cuamckuu/tg-inviter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_reqs,
)

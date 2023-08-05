import setuptools

setuptools.setup(
    name="Cpse",
    version="0.0.1",
    author="LeoLeeYM",
    author_email="1059872990@qq.com",
    description="提供在Windows控制台开发游戏的引擎",
    long_description="提供在Windows控制台开发游戏的引擎",
    long_description_content_type="text/markdown",
    url="https://github.com/suiyue-studio/CPSE",
    packages=setuptools.find_packages(),
    install_requires=["pywin32","pynput"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
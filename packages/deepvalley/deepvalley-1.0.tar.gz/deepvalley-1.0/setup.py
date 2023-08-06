import setuptools
 
with open("README.md", 'r') as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="deepvalley",    # 模块名称
    version="1.0",    # 当前版本
    author="goodli",  # 作者
    author_email="goodli@tencent.com",  # 作者邮箱
    description="多模态模型训练框架",     # 模块简介
    long_description="",                # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://git.woa.com/Valley/VFoundation",   # 模块github地址
    packages=setuptools.find_packages(exclude=[".vscode", ".idea"]),            # 自动找到项目中导入的模块
    # 模块相关的元数据（更多的描述）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        "pillow"
    ],
    # python版本
    python_requires=">=3.5",
)

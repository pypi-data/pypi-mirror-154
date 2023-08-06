import setuptools

setuptools.setup(
    name="aijunebot",
    version="1.0.0",
    author="JuneBot",
    author_email="1947725596@qq.com",
    description="aijunebot",
    url = "https://github/JIANG-CHENG-JUN/AI_JuneBot",
    long_description='''
Import:from AiJunebot.AI import *
Using:AI()
Function:
  Training AI model: train(testDatas1, testType1, testDatas2, testType2, trainingTimes)
  Using AI model: using(data)
    ''',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
        'jieba',
        'sklearn',
        'numpy'
    ]
)

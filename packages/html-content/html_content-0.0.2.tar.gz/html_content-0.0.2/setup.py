from setuptools import setup

setup(
    name='',
    version='0.0.2',
    packages=['html_content'],
    description='Easily construct HTML document with pandas DataFrame, markdown, matplotlib, plotly and HTML.',
    url="https://github.com/lee-junjie/html_content",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'plotly>=5.7.0',
        'pandas>=1.4.2',
        'matplotlib>=3.5.1',
        'seaborn>=0.11.2',
        'Markdown>=3.3.7'
    ],
    python_requires=">=3.8"
)

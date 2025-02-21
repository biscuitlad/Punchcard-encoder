from setuptools import setup, find_packages

setup(
    name='knitting-pattern-decoder',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool to decode knitting punchcard patterns and output them in a grid format.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'opencv-python',
        'numpy',
        # 'tkinter',  # tkinter is included with Python, no need to specify it
    ],
    entry_points={
        'console_scripts': [
            'knitting-pattern-decoder=knitting_pattern_decoder.knitting_pattern_decoder:main',  # Adjust if you have a main function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
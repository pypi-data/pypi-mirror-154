from setuptools import find_packages, setup

setup(
    name='swip',
    packages=['swip'],
    package_dir={"swip": "swip"},
    include_package_data=True,
    version='0.1.2',
    license='MIT',
    description='swip is a basic version control system, based on Git.',
    author='Noa Shay',
    author_email='noa.shay22@gmail.com',
    url='https://github.com/ShayNoa/swip.git',
    keywords=['version control', 'git'],
    install_requires=[
        'loguru',
        'graphviz',
        'colorama',
	    'termcolor',
        'wheel'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ],
    entry_points={
        'console_scripts': ['swip=swip.swip:main'],
    },
)


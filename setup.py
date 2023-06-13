import setuptools

setuptools.setup(
    name='slippy_api',
    version='0.6',
    author='Sophia',
    author_email='sophimander@gmail.com',
    description='API wrapper for slippi.gg',
    long_description='Simple wrapper for the GraphQL api on slippi.gg',
    long_description_content_type='text/markdown',
    install_requires=[
        'requests~=2.29.0',
        'ratelimiter~=1.2.0.post0',
        'pytest~=7.3.1'
    ],
    url='https://github.com/ConstObject/slippy-api',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)

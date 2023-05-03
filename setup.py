import setuptools

setuptools.setup(
    name='slippy_api',
    version='0.2',
    author='Sophia',
    author_email='sophimander@gmail.com',
    description='API wrapper for slippi.gg',
    long_description='Simple wrapper for the GraphQL api on slippi.gg',
    long_description_content_type='text/markdown',
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

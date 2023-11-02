from setuptools import setup, find_packages

setup(
    name='valispace',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests', 'six'],
    version='0.1.18',
    description='Valispace Python API',
    author='Valispace',
    author_email='support@valispace.com',
    license='MIT',
    url='https://github.com/valispace/ValispacePythonAPI',
    keywords='hardware engineering satellites rockets space technology',
    classifiers=[],
)

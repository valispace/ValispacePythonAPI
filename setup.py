from setuptools import setup, find_packages

setup(
    name='valispace',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    version='0.1',
    description='Valispace Python API',
    author='Valispace',
    author_email='contact-us@valispace.com',
    license='MIT',
    url='https://github.com/valispace/ValispacePythonAPI',  # use the URL to the github repo
    # download_url='https://github.com/valispace/ValispacePythonAPI/archive/0.1.tar.gz',
    keywords=[],  # arbitrary keywords
    classifiers=[],
)
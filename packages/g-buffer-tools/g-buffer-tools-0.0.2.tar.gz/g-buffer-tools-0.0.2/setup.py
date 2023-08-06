from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='g-buffer-tools',
    version='0.0.2',
    keywords=['G-buffer', 'image process'],
    description='a set of tools used to handle G-buffer',
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url='https://github.com/bhiaibogf/image-process',
    author='bhiaibogf',
    author_email='bhiaibogf@outlook.com',
    platforms="any",
    packages=['g_buffer_tools'],
    entry_points={
        'console_scripts': [
            'to_exr=g_buffer_tools:to_exr_main',
        ]
    }
)

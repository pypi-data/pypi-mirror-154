from setuptools import setup, find_packages

setup(
    name='cronexpr-validator',
    version='1.0.1',
    license='MIT',
    author="poliambro",
    author_email='poliana.ambrosio.campos@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/poliambro/cronexpr-validator',
    keywords='cron validator',
    install_requires=[],
)
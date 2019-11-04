from setuptools import setup

from scripts.release import get_version

setup(
    name='prometheus-sanic',
    version=f'{get_version()}',
    description='Exposes Prometheus monitoring metrics of Sanic apps.',
    url='https://github.com/skar404/prometheus-sanic',
    author='None User',
    author_email='skar404@gmail.com',
    license='MIT',
    packages=['prometheus_sanic'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'sanic>=18.12',
        'prometheus-client~=0.7.1',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Topic :: System :: Monitoring',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='sanic prometheus monitoring'
)

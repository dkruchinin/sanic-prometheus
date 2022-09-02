from setuptools import setup


setup(
    name='sanic-prometheus-mon',
    version='0.3.8',
    description='Exposes Prometheus monitoring metrics of Sanic apps.',
    url='https://github.com/valerylisay/sanic-prometheus-mon',
    author='Dan Kruchinin',
    author_email='dan.kruchinin@gmail.com',
    maintainer='Valeriy Lisay',
    maintainer_email='valery@lisay.ru',
    license='MIT',
    packages=['sanic_prometheus'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'sanic>=18.12',
        'prometheus-client~=0.11.0',
        'psutil~=5.8.0',
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
        'Programming Language :: Python :: 3.7',
    ],
    keywords='python sanic prometheus monitoring metrics'
)

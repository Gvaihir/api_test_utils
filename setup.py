from setuptools import setup

setup(
    name='ufixtures',
    version='0.0.1',
    packages=['ufixtures'],
    url='https://github.com/Gvaihir/ufixtures',
    license='GNU General Public License v3.0',
    author='Anton Gvaihir Ogorodnikov',
    author_email='pcf11differentiation@gmail.com',
    description='create fixtures and sanitize them',
    python_requires='>=3.6',
    install_requires=['betamax',
                      'betamax_serializers',
                      'vcrpy']
)

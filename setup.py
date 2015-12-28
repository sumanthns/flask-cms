from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(name='flask_project',
      version='0.1',
      description='Flask based cms',
      url='https://github.com/sumanthns/flask-cms.git',
      author='Sumanth Nagadavalli Suresh',
      author_email='nsready@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=reqs,
      zip_safe=False)

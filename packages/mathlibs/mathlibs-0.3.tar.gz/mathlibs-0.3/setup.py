from setuptools import setup, find_packages
 
setup(name='mathlibs',
      version='0.3',
      url='https://github.com/SergeyBT/mathlibs',
      license='MIT',
      author='Sergey Kudinov',
      author_email='info@blagon-team.ml',
      description='math theorem',
      packages=['mathlibs'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False)
from setuptools import find_packages,setup
from typing import List

hyphen_edot='-e .'
def get_requirements(file_path:str)->List[str]:
    #this fn will return list of requirements

    requirements=[]
    with open(file_path) as obj:
        requirements=obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if hyphen_edot in requirements:
            requirements.remove(hyphen_edot)


setup(
    name='DSPROJ',
    version='0.0.1',
    author='Abhishek',
    author_email='kseofficial2100@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
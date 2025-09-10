from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AI_Powered_Symptom_Advisor",
    version="0.1",
    author="beniaminenahid",
    packages=find_packages(),
    install_requires = requirements,
)
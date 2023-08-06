from setuptools import find_packages, setup

setup(
    name='splitmovieaiyc', # 应用名
    packages=find_packages(include=['splitmovieaiyc']),
    version='0.1.0', # 版本号
    description='My first Python library',
    author='Me',
    license='MIT',
    install_requires=["numpy==1.21.2"], # 依赖列表
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.4'],
    test_suite='tests',
)

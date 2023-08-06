from setuptools import setup, find_packages
#import py2exe

setup(
        name='QTFITIT',     
        version='0.1',   
        description='QT version of FITIT for XANES fitting submodule of a package(Testing version for pip uploading)',   
        author='HaifengZhao FeiZhan(Testing version for pip uploading)',  # 作者
        author_email='zhanf@ihep.ac.cn',  # 作者邮箱
        url='https://github.com/BSRF-XA/XAS_ML',      # 包的主页
        packages=find_packages(),                 # 包
        install_requires=['numpy','scipy','scikit-learn','joblib','PyQt5','nlopt'],
        include_package_data=True,
        
        entry_points={
        'console_scripts': [
            'QTFITIT=src.QTFITIT_pip_test:run',
        ], }
)
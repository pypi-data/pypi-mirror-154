from setuptools import setup, find_packages

setup(
	name="myip_localip",
	version="0.0.7",
	description="This uses ipinfo.io about current ip Also give LocalIP",
	long_description="This uses ipinfo.io about current ip Also give LocalIP",
	install_requires=["click==8.1.3", "colorama==0.4.4", "requests"],
	entry_points="""
	[console_scripts]
	myip=myip.main:main
	""",
	author="Rahul Mistri",
	author_email="rahulmistri1997@gmail.com",
	packages=find_packages(),
)
#!/usr/bin/python

import subprocess
import os
import shutil
import yaml

yaml_file = """
"https://github.com/ipa320/bride-develop-release.git":
  - bride:
    - "groovy": "0.3.0-6"
    - "hydro": "0.3.0-1"
  - bride-templates:
    - "groovy": "0.3.0-6"
    - "hydro": "0.3.0-1"
  - bride-compilers:
    - "groovy": "0.3.0-6"
    - "hydro": "0.3.0-1"
"""
debbuild_config = yaml.load(yaml_file)
package = []
for repo in debbuild_config:
	for packdict in debbuild_config[repo]:
		for pack in packdict:
			for distropack in packdict[pack]:
				for distro in distropack:
					package.append([distro, pack, distropack[distro]])

repository = repo #"https://github.com/ipa320/bride-develop-release.git"
#package = [["groovy","bride","0.3.0-6"], ["groovy","bride-templates", "0.3.0-6"] , ["groovy","bride-compilers", "0.3.0-6"],["hydro","bride","0.3.0-1"], ["hydro","bride-templates", "0.3.0-1"] , ["hydro","bride-compilers", "0.3.0-1"]]

working_dir = "/home/vagrant/cob_debbuild/debcreation/"

def build_debs():
	#Create workspace
	os.chdir(working_dir)
	if(not os.path.exists("debbuild")):
		os.mkdir("debbuild")
	os.chdir("debbuild")

	#Generate all the debian packages
	for distro, pack, version in package:
		subprocess.call(["git", "clone", repository, "build_"+pack])
		os.chdir("build_"+pack)
		subprocess.call(["git", "checkout", "debian/ros-"+distro+"-"+pack+"_"+version+"_precise"])
		print "git-buildpackage -uc -us  --git-ignore-new"
		subprocess.call(["git-buildpackage", "-uc", "-us", "--git-ignore-new"])
		os.chdir("..")
		shutil.rmtree("build_"+pack)

def create_debrepo():
	#Create debian repository
	#See http://kaivanov.blogspot.de/2012/08/creating-apt-repository-with-reprepro.html
	#Req: sudo apt-get install dpkg-sig gnupg reprepro
	os.chdir(working_dir)
	if(not os.path.exists("archive/conf")):
		os.makedirs("archive/conf")
	os.chdir("archive/conf")
	distributions = """Origin: github.com/ipa320/bride
Label: github.com/ipa320/bride
Codename: precise
Architectures: i386 amd64 source
Components: main
Description: BRIDE APT Repository
SignWith: yes
DebOverride: override.precise
DscOverride: override.precise
"""
	f = open('distributions', 'w')
	f.write(distributions)
	options = """verbose
ask-passphrase
"""
	f.close()
	f = open('options', 'w')
	f.write(options)
	f.close()

	f = open('override.precise', 'w')
	f.write("")
	f.close()

	os.chdir(working_dir+"/archive")
	for distro, pack, version in package:
		print "dpkg-sig --sign builder "+working_dir+ "debbuild/ros-"+distro+"-"+pack+"_"+version+"precise_amd64.deb"
		subprocess.call(["dpkg-sig", "--sign", "builder", working_dir+ "debbuild/ros-"+distro+"-"+pack+"_"+version+"precise_amd64.deb"])
		print "reprepro includedeb precise "+working_dir+ "debbuild/ros-"+distro+"-"+pack+"_"+version+"precise_amd64.deb"
		subprocess.call(["reprepro", "includedeb", "precise", working_dir+ "debbuild/ros-"+distro+"-"+pack+"_"+version+"precise_amd64.deb"])

	#os.chdir(working_dir)
	#if(not os.path.exists("archive/mini-dinstall/incoming")):#
	#	os.makedirs("archive/mini-dinstall/incoming")

	#dput_conf = """[local]
	#fqdn = localhost
	#method = local
	#incoming = """+working_dir+"""/archive/mini-dinstall/incoming
	#allow_unsigned_uploads = 1
	#post_upload_command = mini-dinstall --batch"""#

	#f = open('dput.conf', 'w')
	#f.write(dput_conf)

if __name__ == '__main__':
	build_debs()
	#create_debrepo()



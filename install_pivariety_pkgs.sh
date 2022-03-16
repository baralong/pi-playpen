#!/bin/bash
rev=$(cat /proc/cpuinfo | grep Revision | awk '{print substr($NF,length($NF)-5,6)}')
code_name=$(awk -F"[)(]+" '/VERSION=/ {print $2}' /etc/os-release)
kernel_info=$(uname -a)
kernel=$(uname -r)
arch=$(arch)
pkg_version=$code_name
rpi_kernel=$(dpkg-query -f '${Version}' --show raspberrypi-kernel)

$(dpkg-architecture -earm64)
if [ $? == 0 ]; then
    pkg_version=$pkg_version"-arm64"
fi

$(dpkg --compare-versions 1:1.20211201~ '>=' $rpi_kernel)
if [[ $? == 1 && $code_name != "buster" ]]; then
    pkg_version=$pkg_version"-v5"
fi

echo "================================================="
echo "Hardware Revision: ${rev}"
echo "Kernel Version: ${kernel}"
echo "OS Codename: ${code_name}"
echo "ARCH: ${arch}"
echo "================================================="
echo ""

CONFIG_FILE_NAME=packages.txt
CONFIG_FILE_DOWNLOAD_LINK=https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/packages.txt
RED='\033[0;31m'
NC='\033[0m' # No Color

updatePackages()
{
    rm -f $CONFIG_FILE_NAME
    wget -O $CONFIG_FILE_NAME $CONFIG_FILE_DOWNLOAD_LINK
    source $CONFIG_FILE_NAME
}

listPackages()
{
    if [ ! -f $CONFIG_FILE_NAME ]; then
        updatePackages
    fi
    source $CONFIG_FILE_NAME
    echo "Supported packages:"
    for key in ${!package_cfg_names[*]};do
    echo -e "\t$key"
    done
    echo ""
}

helpFunction()
{
    if [ ! -f $CONFIG_FILE_NAME ]; then
        updatePackages
    fi
    echo ""
    echo "Usage: $0 [option]... -p <package name>"
    echo -e "Options:"
    echo -e "\t-p <package name>\tSpecify the package name."
    echo -e "\t-h \t\t\tShow this information."
    echo -e "\t-l \t\t\tUpdate and list available packages."
    echo ""
    listPackages
    exit 1
}

while getopts hlv:p: flag
do
    case "${flag}" in
        v)  pkg_version=${OPTARG};;
        p)  package=${OPTARG};;
        l)  updatePackages
            listPackages
            exit 1
            ;;
        ?)  helpFunction;;
    esac
done

if [ ! -f $CONFIG_FILE_NAME ]; then
    updatePackages
fi

source $CONFIG_FILE_NAME

if [ -z $package ]; then
    helpFunction
fi

package_cfg_name=${package_cfg_names[$package]}
package_cfg_download_link=${package_cfg_download_links[$package]}

if [[ (-z $package_cfg_name) || (-z $package_cfg_download_link) ]]; then
    echo -e "${RED}Unsupported package.${NC}"
    echo ""
    listPackages
    exit -1
fi

# echo "package_cfg_name: $package_cfg_name"
# echo "package_cfg_download_link: $package_cfg_download_link"

rm -f $package_cfg_name
wget -O $package_cfg_name $package_cfg_download_link
source $package_cfg_name

download_link=
pkg_name=

if [[ $package == *"kernel_driver"* ]]; then
    download_link=${package_download_links[$kernel]}
    pkg_name=${package_names[$kernel]}
else
    download_link=${package_download_links[$pkg_version]}
    pkg_name=${package_names[$pkg_version]}
fi

if [[ (-z $pkg_name) || (-z $download_link) ]]; then
    echo -e "${RED}"
	echo -e "Cannot find the corresponding package, please send the following information to support@arducam.com"
    echo -e "Hardware Revision: ${rev}"
    echo -e "Kernel Version: ${kernel}"
    echo -e "Package: ${package} -- ${pkg_version}"

    if [[ $package == *"kernel_driver"* ]]; then
        echo -e "You are using an unsupported kernel version, please install the official SD Card image(do not execute rpi-update):"
        echo -e "https://www.raspberrypi.com/software/operating-systems/"
    fi

    echo -e "${NC}"
	exit -1
fi

rm -rf $pkg_name
 
wget -O $pkg_name $download_link

if [[ ( $? -ne 0) || (! -f "${pkg_name}") ]]; then
	echo -e "${RED}download failed${NC}"
	exit -1
fi

if [[ $package == *"kernel_driver"* ]]; then
    echo "is kernel driver"
    tar -zxvf $pkg_name Release/
    cd Release/
    ./install_driver.sh
else
    if [[ $package == *"libcamera_dev"* ]]; then
        echo -e "remove libcamera0"
        echo ""
        sudo apt remove -y libcamera0
    fi
    sudo apt update
    sudo apt install -y ./$pkg_name
    # if [[ $package == *"libcamera_apps"* && ! -f /usr/lib/arm-linux-gnueabihf/libboost_program_options.so.1.67.0 ]]; then
    #     echo -e "Soft link to libboost_program_options.so"
    #     echo ""
    #     sudo ln -s /usr/lib/arm-linux-gnueabihf/libboost_program_options.so /usr/lib/arm-linux-gnueabihf/libboost_program_options.so.1.67.0
    # fi
fi

if [ $? -ne 0 ]; then
    echo ""
	echo -e "${RED}Unknown error, please send the error message to support@arducam.com${NC}"
	exit -1
fi

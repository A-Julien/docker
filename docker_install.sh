#!/bin/bash
set -e

#************************************************
#  GETER
#************************************************

# Get the distribution by comparing packaging tool
get_distrib(){
    if [[ -n "$(type -p apt-get)" ]]
    then
        distrib="debian"
    elif [[ -n "$(type -p pacman)" ]]
    then
        distrib="arch"
    elif [[ -n "$(type -p brew)" ]] || [[ -n "$(type -p port)" ]]
    then
        distrib="mac"
    fi
}

get_arch(){
    case "$distrib" in
        "debian")   arch="$(arch)" ;;
        "arch")     arch="$(uname -m )" ;;
        "mac")      arch="$(/usr/bin/arch)";;
        *)          echo "Unknow architecture"
                    exit "1"
                    ;;
    esac
    if [ "$(echo "$arch" | grep "arm")" ] && [  !"$(echo "$arch" | grep "armv")" ]; then
        arch="armhf"
    elif [ "$arch" = "x86_64"  ]; then
        arch="amd64"
    fi
}

#************************************************
#  DOCKER
#************************************************

install_docker_debian (){
    echo "----------------------------------"
    echo "Installing docker"
    echo "Install packages to allow apt to use a repository over HTTPS:"
    echo "----------------------------------"
    apt-get update
    apt-get install -y \
    apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common
    echo "----------------------------------"
    echo "Add Docker’s official GPG key"
    echo "----------------------------------"
    if [ "$(dpkg-query -W -f='${Status}' curl 2>/dev/null | grep -c "installed")" -eq 0 ];
    then
        apt-get install -y curl
    fi
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
    
    echo "----------------------------------"

    if lsb_release -i | grep Raspbian
    then
        curl -sSL https://get.docker.com | sh
    else
        case "$arch" in
        "amd64")
            add-apt-repository \
            "deb [arch=amd64] https://download.docker.com/linux/debian \
            $(lsb_release -cs) \
            stable"

            ;;
        "armhf")
            echo "deb [arch=armhf] https://download.docker.com/linux/debian \
            $(lsb_release -cs) stable" | \
            tee /etc/apt/sources.list.d/docker.list
            ;;
        *)
            echo "error - Architecture not fount"
            exit "1"
        ;;
        esac
    fi

    if ! lsb_release -i | grep Raspbian ;
    then
        apt-get update -y
        apt-get install -y docker-ce
    fi

    usermod -aG docker "$USER"
    echo -e "docker user : OK"
}
get_distrib;
get_arch;
install_docker_debian;

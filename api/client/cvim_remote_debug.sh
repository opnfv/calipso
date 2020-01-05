#!/bin/bash

scan_container=$(docker ps | awk '{print $NF}' | grep calipso_scan)
api_container=$(docker ps | awk '{print $NF}' | grep calipso_api)

if [[ "$1" = "enable" ]]; then
    docker exec -i ${scan_container} wget http://mirror.centos.org/centos/7/os/x86_64/Packages/tcp_wrappers-libs-7.6-77.el7.x86_64.rpm
    docker exec -i ${scan_container} wget http://mirror.centos.org/centos/7/os/x86_64/Packages/openssh-7.4p1-21.el7.x86_64.rpm
    docker exec -i ${scan_container} wget http://mirror.centos.org/centos/7/os/x86_64/Packages/openssh-server-7.4p1-21.el7.x86_64.rpm
    docker exec -i ${scan_container} rpm -i tcp_wrappers-libs-7.6-77.el7.x86_64.rpm
    docker exec -i ${scan_container} rpm -i openssh-7.4p1-21.el7.x86_64.rpm
    docker exec -i ${scan_container} rpm -i openssh-server-7.4p1-21.el7.x86_64.rpm
    docker exec -i ${scan_container} ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
    docker exec -i ${scan_container} sed -ie '/^export/a nohup /usr/sbin/sshd -D &' /start_calipso_scan_manager.sh
    docker exec -i ${scan_container} sed -ie '/^#AddressFamily/a Port 30022' /etc/ssh/sshd_config
    echo -e "calipso_debug" | docker exec -i ${scan_container} passwd --stdin root
    echo 'source scl_source enable rh-python35' | docker exec -i ${scan_container} tee --append /root/.bash_profile
    echo 'source /var/lib/calipso/calipso_config' | docker exec -i ${scan_container} tee --append /root/.bash_profile
    echo 'source scl_source enable rh-python35' | docker exec -i ${scan_container} tee --append /etc/profile.d/init_calipso_env.sh
    echo 'source /var/lib/calipso/calipso_config' | docker exec -i ${scan_container} tee --append /etc/profile.d/init_calipso_env.sh

    echo -e "calipso_debug" | docker exec -i ${api_container} passwd --stdin root
    echo 'source scl_source enable rh-python35' | docker exec -i ${api_container} tee --append /root/.bash_profile
    echo 'source /var/lib/calipso/calipso_config' | docker exec -i ${api_container} tee --append /root/.bash_profile
    echo 'source scl_source enable rh-python35' | docker exec -i ${api_container} tee --append /etc/profile.d/init_calipso_env.sh
    echo 'source /var/lib/calipso/calipso_config' | docker exec -i ${api_container} tee --append /etc/profile.d/init_calipso_env.sh
    docker exec -i ${api_container} sed -ie '/^export/a nohup /usr/sbin/sshd -D &' /start_calipso_api_server.sh
    docker exec -i ${api_container} sed -ie '/^#AddressFamily/a Port 40022' /etc/ssh/sshd_config

    iptables -I INPUT 1 -p tcp --dport 30022 -j ACCEPT
    iptables -I INPUT 2 -p tcp --dport 40022 -j ACCEPT

    docker restart ${api_container}
    docker restart ${scan_container}

elif [[ "$1" = "disable" ]]; then
    docker exec -i ${scan_container} sed -i '/sshd/d' /start_calipso_scan_manager.sh
    docker exec -i ${scan_container} sed -i '/Port 30022/d' /etc/ssh/sshd_config
    docker exec -i ${scan_container} sed -i '/source scl_source enable rh-python35/d' /root/.bash_profile
    docker exec -i ${scan_container} passwd -d root
    docker exec -i ${scan_container} rm /etc/profile.d/init_calipso_env.sh

    docker exec -i ${api_container} sed -i '/sshd/d' /start_calipso_api_server.sh
    docker exec -i ${api_container} sed -i '/Port 40022/d' /etc/ssh/sshd_config
    docker exec -i ${api_container} sed -i '/source scl_source enable rh-python35/d' /root/.bash_profile
    docker exec -i ${api_container} passwd -d root
    docker exec -i ${api_container} rm /etc/profile.d/init_calipso_env.sh

    iptables -D INPUT -p tcp --dport 30022 -j ACCEPT
    iptables -D INPUT -p tcp --dport 40022 -j ACCEPT

else
    echo "need 'enable' or 'disable' as argument"
fi
#!/bin/bash
# sshpass -p'suweisheng' scp -r suweisheng@192.168.170.5:~/tools/skynet.sh /root/skynet.sh

if [ ! -f /root/skynet ]; then
    install_method=2
    case ${install_method} in
    1)
        # 远程服务器导入
        git clone https://github.com/cloudwu/skynet.git
        ;;
        cd /root/skynet
        yum install -y readline autoconf
        scl enable devtoolset-9 "make linux"
        ./skynet examples/config    # Launch first skynet node  (Gate server) and a skynet-master (see config for standalone option)
        ./3rd/lua/lua examples/client.lua   # Launch a client, and try to input hello.
        ;;
    2)
        # 挂载光盘读取
        basepath="/mnt/cdrom"
        mkdir -p $basepath
        mount /dev/cdrom $basepath
        cp $basepath/OtherFile/skynet-master.zip /root/
        cp $basepath/OtherFile/jemalloc-dev.zip /root/
        umount $basepath

        unzip -q skynet-master.zip
        unzip -q jemalloc-dev.zip -d skynet-master/3rd/
        rm -rf skynet-master/3rd/jemalloc
        mv skynet-master/3rd/jemalloc-dev skynet-master/3rd/jemalloc

        cd /root/skynet-master
        yum install -y readline autoconf
        scl enable devtoolset-9 "make linux"
        ./skynet examples/config    # Launch first skynet node  (Gate server) and a skynet-master (see config for standalone option)
        ./3rd/lua/lua examples/client.lua   # Launch a client, and try to input hello.
        ;;
    esac
fi
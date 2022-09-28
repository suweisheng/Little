#!/bin/bash

# echo -e "\033[40;33m""-----------------> xxxxxx start""\033[0m"

# ====================================================================================================
add_firewall_port() {
    firewall-cmd --zone=public --list-ports | grep "$1""/tcp" &> /dev/null
    if [ $? -ne 0 ]; then
        firewall-cmd --add-port=$1/tcp --permanent &> /dev/null
        firewall-cmd --reload &> /dev/null
    fi
    # firewall-cmd --zone=public --list-ports
    # netstat -atnlp
}

del_firewall_port() {
    firewall-cmd --zone=public --list-ports | grep "$1""/tcp" &> /dev/null
    if [ $? -ne 1 ]; then
        firewall-cmd --zone=public --remove-port=$1/tcp --permanent &> /dev/null
        firewall-cmd --reload &> /dev/null
    fi
}

# ====================================================================================================
# aliyum centos yum 
# if [ ! -f /etc/yum.repos.d/CentOS-Base.repo.bak ]; then
#     mv /etc/yum.repos.d/CentOS-Base.repo{,.bak}
#     curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
# fi

# ====================================================================================================
# root
cat /root/.bash_profile | grep '37;40' &> /dev/null
if [ $? -ne 0 ]; then
    echo 'export PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[37;40m\]@\h \[\e[36;40m\]\w\[\e[0m\]]\\$ "' >> /root/.bash_profile
    # source ~/.bash_profile
    export PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[37;40m\]@\h \[\e[36;40m\]\w\[\e[0m\]]\\$ "
fi

# ====================================================================================================
# close SELinux
is_has=`awk '/^SELINUX=disabled/{print 1;exit}' /etc/selinux/config`
if [ "$is_has" != 1 ]; then
    sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
fi
setenforce 0

# ====================================================================================================
# network-scripts
filename="/etc/sysconfig/network-scripts/ifcfg-ens33"
is_static=`awk -F"=" '/BOOTPROTO/{match($2, /static/, x);if(x[0] != "") print 1}' $filename`
if [ "$is_static" != 1 ]; then
    IPADDR="192.168.170.99"
    GATEWAY="192.168.170.254"
    DNS1="192.168.170.254"
    NETMASK="255.255.255.0"
    # if [ 1 -ne 1 ]; then
    #     IPADDR=`ip addr | awk '/global/{match($0, /[0-9\.]+/, x);print x[0]}'`
    #     GATEWAY=`ip route show | awk 'NR==1{match($0, /[0-9\.]+/, x);print x[0]}'`
    #     DNS1=`cat /etc/resolv.conf | awk '/nameserver/{match($0, /[0-9\.]+/, x);print x[0];exit}'`
    # fi
    pre_id=${IPADDR%.*}
    let after_ip=${IPADDR##*.}
    is_find=false
    while ! $is_find
    do
        IPADDR=$pre_id"."$after_ip
        is_free=`ping -c2 -w1 $IPADDR | grep '0 received' | wc -l` &> /dev/null
        if ((is_free == 1)); then
            is_find=true
        else
            let after_ip+=1
        fi
    done
    echo -e IPADDR=$IPADDR
    echo -e GATEWAY=$GATEWAY
    echo -e DNS1=$DNS1
    sed -i 's/dhcp/static/' $filename
    sed -i '$a ''IPADDR='"$IPADDR"'\nNETMASK='"$NETMASK"'\nGATEWAY='"$GATEWAY"'\nDNS1='"$DNS1" $filename
    systemctl restart network
    exit
fi

# ====================================================================================================
# rpm packages
rpm_list=("python" "gcc" "gcc-c++" "net-tools" "git-1.8.3.1" "git-daemon" "cmake" \
    "centos-release-scl" "scl-utils" "scl-utils-build" \
    "devtoolset-9-gcc" "devtoolset-9-gcc-c++" \
    "samba" "subversion" "httpd" sshpass \
    "zip" "unzip" \
    )
# "vim-enhanced"
for((i=0; i<${#rpm_list[@]}; i++)) do
    num=`rpm -qa | grep ${rpm_list[i]} | wc -l`
    if [ "$num" -eq 0 ]; then
        echo ${rpm_list[i]} "wail install"
        yum install -y ${rpm_list[i]}
    fi
done

# ====================================================================================================
# account setting
declare -A linux_user_dict
linux_user_dict=(\
    [suweisheng]=suweisheng \
)
for name in ${!linux_user_dict[@]}
do
    grep $name /etc/passwd &> /dev/null
    if [ $? -ne 0 ]; then
        useradd $name
        echo ${linux_user_dict[$name]} | passwd --stdin $name &> /dev/null
        echo 'export PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[37;40m\]@\h \[\e[36;40m\]\w\[\e[0m\]]\\$ "' >> /home/$name/.bash_profile
        printf "linux user create success: %s(%s)\n" $name ${linux_user_dict[$name]}$name
    fi
    is_has=`awk '/'"$name"'\tALL=\(ALL\) \tALL/{print 1}' /etc/sudoers`
    if [ "$is_has" != 1 ]; then
        chmod -v u+w /etc/sudoers
        sed -i '/root\tALL=/a '"$name"'\tALL=(ALL) \tALL' /etc/sudoers
        chmod -v u-w /etc/sudoers
    fi
done

# ====================================================================================================
# samba
declare -A smb_user_dict
smb_user_dict=(\
    [root]=root \
    [suweisheng]=suweisheng \
)
for name in ${!smb_user_dict[@]}
do
    pdbedit -L | grep "^$name:" &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e ${smb_user_dict[$name]}"\n"${smb_user_dict[$name]} | pdbedit -atu $name
        printf "samba user create: %s(%s)\n" $name ${smb_user_dict[$name]}
    fi
done

# 在firewalld中放行samba服务,允许SELinux中对Samba服务访问
is_has=`awk '/service name="samba"/' /etc/firewalld/zones/public.xml | wc -l`
if [ "$is_has" != 1 ]; then
    firewall-cmd --permanent --add-service=samba
    firewall-cmd --reload
fi
# setsebool -P samba_enable_home_dirs=on samba_export_all_rw=on # 或直接关闭selinux

# 开机自启
systemctl enable smb

# samba 共享
share_dir="/home/share"
if [ ! -d $share_dir ]; then
    mkdir -p $share_dir
    chmod -R 1777 $share_dir # Sticky位权限t
    chown -R nobody:nobody $share_dir
fi
filename="/etc/samba/smb.conf"
cmd1="map to guest = bad user"
grep "$cmd1" $filename &> /dev/null
if [ $? -ne 0 ]; then
    sed -ir '/security/a \\t'"$cmd1" $filename
fi

grep "$share_dir" $filename &> /dev/null
if [ $? -ne 0 ]; then
#     cat>>$filename<<EOF

# [share]
#     comment = share
#     path = $share_dir
#     browseable = yes
#     writeable = yes
#     guest ok = yes
# EOF

    sed -i '$a''\\n\[share\]\n'\
"\tpath = $share_dir\n"\
'\tcomment = share\n'\
'\tbrowseable = yes\n'\
'\twriteable = yes\n'\
'\tguest ok = yes' $filename

fi

systemctl restart smb

# ====================================================================================================
# 配置svn 暂时没有配置自启动
mkdir -p /svn
mkdir -p /svn/conf
if [ ! -d "/svn/p1" ]; then
    svnadmin create /svn/p1
    cp /svn/p1/conf/authz /svn/conf/authz
    cp /svn/p1/conf/passwd /svn/conf/passwd

    svnserve_conf=/svn/p1/conf/svnserve.conf
    sed -i 's/# anon-access = read/anon-access = none/' $svnserve_conf
    sed -i 's/# auth-access = write/auth-access = write/' $svnserve_conf
    sed -i 's/# password-db = passwd/password-db = \/svn\/conf\/passwd/' $svnserve_conf
    sed -i 's/# authz-db = authz/authz-db = \/svn\/conf\/authz/' $svnserve_conf
    sed -i 's/# realm = My First Repository/realm = My First Repository/' $svnserve_conf

    cat>>/svn/conf/passwd<<EOF
suweisheng = suweisheng
lixin = lixin
laijianfa = laijianfa
mengfei = mengfei
liutao = liutao
haha = haha
EOF
    
    sed -i 's/\[groups\]/# \[groups\]/' /svn/conf/authz
    cat>>/svn/conf/authz<<EOF

[groups]
admin = suweisheng
p1_group = suweisheng,lixin,mengfei,liutao,xiexian
p1_server = lixin
p1_client = mengfei
p1_cehua = liutao
p1_meishu = xiexian

[/]
@admin = rw
* =

[p1:/]
@p1_group = rw

[p1:/server]
@admin = rw
@p1_server = rw
* =

[p1:/client]
@admin = rw
@p1_client = rw
* =

[p1:/sharedata]
@p1_group = rw
EOF
fi
add_firewall_port 3690
# 手动开启
# svn_pid=`ps aux | grep svnserve | grep -v grep | awk '{print $2}'`
# if [ $svn_pid ]; then
#     kill -9 $svn_pid
# fi
# setenforce 0
# svnserve -d -r /svn

# 自动开启
cat /etc/sysconfig/svnserve | grep 'OPTIONS="-r /svn"' &> /dev/null
if [ $? -ne 0 ]; then
    sed -i 's/^OPTIONS.*/OPTIONS="-r \/svn"/' /etc/sysconfig/svnserve
fi
systemctl enable svnserve
systemctl restart svnserve

# ====================================================================================================
# git - ssh 协议
if [ ! -d /home/git_share ]; then
    # 每个合作者必须在该主机上有账户
    mkdir /home/git_share
    git init --bare /home/git_share/p1
    chmod -R 777 /home/git_share
    # chmod g+s -R /home/git_share/p1 # 该目录下新建文件或文件夹的所属组继承父目录
    setfacl -m d:u::rwx,d:g::rwx,d:o::rwx -R /home/git_share/p1 # 设置文件夹子目录和文件的默认acl权限
    # 在多人合作的git项目中push之后不会出现有时候不能访问的情况
fi
# git clone suweisheng@192.168.170.99:/home/git_share/p1

account_git="git"
passwd_git="git"
grep $account_git /etc/passwd &> /dev/null
if [ $? -ne 0 ]; then
    useradd $account_git
    echo $passwd_git | passwd --stdin $account_git &> /dev/null
    echo 'export PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[37;40m\]@\h \[\e[36;40m\]\w\[\e[0m\]]\\$ "' >> /home/$account_git/.bash_profile
    printf 'account(%s) create success\n' $account_git
fi
is_has=`awk '/'"$account_git"'\tALL=\(ALL\) \tALL/{print 1}' /etc/sudoers`
if [ "$is_has" != 1 ]; then
    chmod -v u+w /etc/sudoers
    sed -i '/root\tALL=/a '"$account_git"'\tALL=(ALL) \tALL' /etc/sudoers
    chmod -v u-w /etc/sudoers
fi

if [ ! -d /home/git/p2 ]; then
    # 统一用git账号，避免在主机上配置多个账号
    su - git -c'git config --global user.name "git_name";'\
'git config --global user.email "git@example.com";'\
'mkdir -p .ssh && chmod 700 .ssh;'\
'touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys;'\
'git init --bare ~/p2'
fi
# 合作者主机配置公钥密钥
# ssh-keygen -t rsa #在另一台生成密钥公钥id_rsa,id_rsa.pub
# ssh-copy-id git@192.168.170.99 # 把公钥文件发给目标主机管理员
# git服务器上配置添加合作者的公钥
# cat /tmp/id_rsa.john.pub >> ~/.ssh/authorized_keys
# usermod -s /usr/bin/git-shell git
# git clone git@192.168.170.99:~/p2

# ====================================================================================================
# git - git 协议,可以省去逐一配置 SSH 公钥的麻烦
if [ ! -d /var/lib/git/p3 ]; then
    git init --bare --share=0777 /var/lib/git/p3
    chown git:git -R /var/lib/git/p3
    touch /var/lib/git/p3/git-daemon-export-ok
fi

add_firewall_port 9418
# setenforce 0


# var/lib/git 是安装git daemon 自动生成的
# --enable=receive-pack 只有加上才能外部push
if [ ! -f /etc/systemd/system/git-daemon.service ]; then
    cat>>/etc/systemd/system/git-daemon.service<<EOF
[Unit]
Description=Start Git Daemon

[Service]
ExecStart=/usr/bin/git daemon --reuseaddr --base-path=/var/lib/git --export-all --verbose --enable=receive-pack 

Restart=always
RestartSec=500ms

StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=git-daemon

User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF
    systemctl enable git-daemon
    systemctl restart git-daemon
fi
# git clone git://192.168.170.99/p3

# ====================================================================================================
# git - http
if [ ! -d /var/www/html/git ]; then
    mkdir -p /var/www/html/git
    git init --bare /var/www/html/git/p4
    chown apache:apache /var/www/html/git -R
    htpasswd -bc /var/www/html/git/passwd admin admin
fi

sed -i 's/^#ServerName/ServerName/' /etc/httpd/conf/httpd.conf

add_firewall_port 80

if [ ! -f /etc/httpd/conf.d/git.conf ]; then
    cat>>/etc/httpd/conf.d/git.conf<<EOF
<VirtualHost *:80>
        ServerName 192.168.170.99
        SetEnv GIT_PROJECT_ROOT /var/www/html/git
        SetEnv GIT_HTTP_EXPORT_ALL
        ScriptAlias /git/ /usr/libexec/git-core/git-http-backend/
        <Location />
                AuthType Basic
                AuthName "Private Git Repo"
                AuthUserFile "/var/www/html/git/passwd"
                Require valid-user
        </Location>
</VirtualHost>
EOF
fi
systemctl enable httpd
systemctl restart httpd
# git clone http:://192.168.170.99/git/p4

# ====================================================================================================
# mysql
rpm -qa | grep 'mariadb-libs' &> /dev/null
if [ $? -eq 0 ]; then
    rpm -e --nodeps mariadb-libs
fi

rpm -qa | grep mysql-community-server &> /dev/null
if [ $? -ne 0 ]; then
    install_method=2
    case ${install_method} in
    1)
        # 远程服务器导入
        basepath="/root/MysqlPkg"
        sshpass -p 'suweisheng' scp -r suweisheng@192.168.170.5:~/tools/mysql-community-server $basepath
        rpm --import /$basepath/RPM-GPG-KEY-mysql-2022
        yum localinstall -y /$basepath/mysql57*.rpm
        yum localinstall -y /$basepath/mysql-community*.rpm
        rm -rf $basepath
        ;;
    2)
        # 挂载光盘读取
        basepath="/mnt/cdrom"
        mkdir -p $basepath
        mount /dev/cdrom $basepath
        rpm --import $basepath/MysqlPkg/RPM-GPG-KEY-mysql-2022
        yum localinstall -y $basepath/MysqlPkg/mysql57*.rpm
        yum localinstall -y $basepath/MysqlPkg/mysql-community*.rpm
        umount $basepath
        ;;
    *)
        curl -o ~/mysql-yum.rpm https://repo.mysql.com//mysql57-community-release-el7-7.noarch.rpm
        yum localinstall -y ~/mysql-yum.rpm
        rm -rf ~/mysql-yum.rpm
        rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
        yum install -y mysql-community-server
        usleep
        ;;
    esac
fi

grep 'personal config' /etc/my.cnf &> /dev/null
if [ $? -ne 0 ]; then
    cat>>/etc/my.cnf<<EOF

# ---------------------- personal config ----------------------
# skip-grant-tables # enter mysql by no user password

character_set_server = utf8
init_connect = 'SET NAMES utf8'

# root_pwd:root@72Hw9Dl3X*j0

EOF
    grep '/var/log/mysqld.log' /etc/my.cnf &> /dev/null
    if [ $? -ne 0 ]; then
        sed -i 's/log-error=.*/log-error=\/var\/log\/mysqld.log/' /etc/my.cnf
    fi
fi
rpm -qa | grep mysql-community-server &> /dev/null
if [ $? -eq 0 ]; then
    add_firewall_port 3306
    systemctl restart mysqld && systemctl enable mysqld

    rootpws="123456789"
    # ALTER USER 'root'@'localhost' PASSWORD EXPIRE; # 让密码过期
    # ALTER USER 'suweisheng'@'%' PASSWORD EXPIRE NEVER # 禁用密码过期
    # ALTER USER 'root'@'localhost' IDENTIFIED BY 'xxxxxxxxx'; # 修改密码
    mysql -u'root' -p$rootpws -e"SELECT USER();" &> /root/sql_cnt.log
    grep 'root@localhost' /root/sql_cnt.log  &> /dev/null
    if [ $? -ne 0 ]; then
        sed -i 's/^# skip-grant-tables/skip-grant-tables/' /etc/my.cnf
        systemctl restart mysqld
        mysql -u'root' -e"update mysql.user set authentication_string=PASSWORD($rootpws), password_expired='N' where user='root';"
        sed -i 's/^skip-grant-tables/# skip-grant-tables/' /etc/my.cnf
        systemctl restart mysqld
        mysql -u'root' -p$rootpws -e"set global validate_password_policy=LOW;"
    fi
    mysql -u'root' -p$rootpws -e"SELECT user, host from mysql.user;" &> /root/sql_cnt.log
    cat /root/sql_cnt.log | grep 'suweisheng' &> /dev/null
    if [ $? -ne 0 ]; then
        mysql -u'root' -p$rootpws <<EOF
SELECT VERSION(), CURRENT_DATE;
SELECT VERSION(); SELECT NOW();
SELECT USER();
SELECT * FROM information_schema.SCHEMATA;
SELECT user, host, password_expired, authentication_string from mysql.user;
SHOW variables like '%character%';
CREATE USER 'suweisheng'@'%' IDENTIFIED BY '$rootpws';
GRANT ALL ON *.* TO ' suweisheng '@'%' WITH GRANT OPTION;
show variables like '%password%';
flush privileges
EOF
    fi
    rm -rf /root/sql_cnt.log
fi

# ====================================================================================================
# mongo
if [ ! -f /etc/yum.repos.d/mongodb-org.repo ]; then
    cat>>/etc/yum.repos.d/mongodb-org.repo<<EOF
[mongodb-org] 
name = MongoDB Repository
baseurl = https://mirrors.aliyun.com/mongodb/yum/redhat/\$releasever/mongodb-org/3.6/x86_64/
gpgcheck = 1 
enabled = 1 
gpgkey = https://www.mongodb.org/static/pgp/server-3.6.asc
EOF
fi
add_firewall_port 27017

rpm -qa | grep 'mongodb-org' &> /dev/null
if [ $? -ne 0 ]; then
    
    install_method=2
    case ${install_method} in
    1)
        # 网络下载安装
        yum install -y mongodb-org
        ;;
    2)
        # 挂载光盘读取
        basepath="/mnt/cdrom"
        mkdir -p $basepath
        mount /dev/cdrom $basepath
        yum localinstall -y $basepath/MongoPkg/mongodb-org*.rpm
        umount $basepath
        ;;
    *)
        
        ;;
    esac

fi

systemctl start mongod

ret=`mongo --quiet --eval 'db.getSiblingDB("admin").getUser("root")'`
if [ "$ret" = "null" ]; then
    mongo <<EOF
    db.getSiblingDB("admin").runCommand({
        createUser: "root",
        pwd: "root",
        roles: [
            { role: "root", db: "admin" },
        ]
    })
EOF
fi

grep "bindIp: 0.0.0.0" /etc/mongod.conf &> /dev/null
if [ $? -ne 0 ]; then
    sed -i 's/bindIp: 127.0.0.1/#bindIp: 127.0.0.1/;/#bindIp/a \  bindIp: 0.0.0.0' /etc/mongod.conf
fi

grep 'authorization: enabled' /etc/mongod.conf &> /dev/null
if [ $? -ne 0 ]; then
    cat>>/etc/mongod.conf<<EOF

security:
  authorization: enabled
EOF
fi

# mongo -host 192.168.170.99:27017 -u'root' -p'root'
systemctl restart mongod

# # ====================================================================================================
# Review Board
install_method=2
case ${install_method} in
1)
    # 远程服务器导入
    pip --version &> /dev/null
    if [ $? -ne 0 ]; then
        curl -o /root/get-pip.py https://bootstrap.pypa.io/pip/2.7/get-pip.py
        python get-pip.py
        pip install -U pip setuptools
        rm -f get-pip.py
    fi
    pip show "ReviewBoard" &> /dev/null
    if [ $? -ne 0 ]; then
        yum install -y gcc python-devel libffi-devel openssl-devel patch
        yum install -y memcached
        yum install -y mysql-server mysql-client mysql-devel
        yum install -y httpd mod_wsgi
        pip install ReviewBoard
        pip install -U 'ReviewBoard[mysql]'
        pip install RBTools
        yum install -y epel-release
        sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/epel.repo
        yum install -y subversion
        yum install -y --enablerepo=epel pysvn
    fi
    ;;
2)
    # 挂载光盘读取
    basepath="/mnt/cdrom"
    mkdir -p $basepath
    mount /dev/cdrom $basepath
    cd ~
    pip --version &> /dev/null
    if [ $? -ne 0 ]; then
        cp $basepath/Pip/get-pip.py /root/get-pip.py
        python get-pip.py $basepath/Pip/packs/pip/*.whl
        rm -rf get-pip.py
    fi
    pip show "ReviewBoard" &> /dev/null
    if [ $? -ne 0 ]; then
        yum install -y gcc python-devel libffi-devel openssl-devel patch
        yum install -y memcached
        yum install -y mysql-server mysql-client mysql-devel
        yum install -y httpd mod_wsgi
        pip install $basepath/Pip/packs/reviewboard/* --find-links=$basepath/Pip/packs/reviewboard
        pip install -U 'ReviewBoard[mysql]'
        yum install -y epel-release
        sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/epel.repo
        yum install -y subversion
        yum install -y --enablerepo=epel pysvn
    fi
    umount $basepath
    ;;
esac

grep 'default-character-set=utf8' /etc/my.cnf &> /dev/null
if [ $? -ne 0 ]; then
    cat>>/etc/my.cnf<<EOF

[client]
default-character-set=utf8
EOF
fi

rootpws="123456789"
mysql -u'root' -p$rootpws -e"show databases like 'reviewboard';" &> /root/sql_cnt.log
cat /root/sql_cnt.log | grep 'reviewboard' &> /dev/null
if [ $? -ne 0 ]; then
    mysql -u'root' -p$rootpws <<EOF
CREATE DATABASE reviewboard CHARACTER SET utf8;
CREATE USER 'review'@'localhost' IDENTIFIED BY '$rootpws';
GRANT ALL PRIVILEGES ON reviewboard.* to 'review'@'localhost';
flush privileges;
EOF
fi
rm -rf /root/sql_cnt.log

systemctl restart mysqld

if [ ! -d /var/www/reviews ]; then
    rb-site install /var/www/reviews -d --noinput \
--domain-name="192.168.170.99" \
--admin-email="admin@qq.com" \
--admin-user="admin" \
--admin-password="admin" \
--cache-type="memcached" \
--cache-info="localhost:11211" \
--db-type="mysql" \
--db-host="127.0.0.1" \
--db-name="reviewboard" \
--db-user="review" \
--db-pass=123456789 \
--site-root="/" \
--web-server-type="apache"
    chown -R apache:apache /var/www/reviews/
    cp /var/www/reviews/conf/apache-wsgi.conf /etc/httpd/conf.d/
    systemctl restart httpd
fi
# http://192.168.170.99/reviews

pip show RBTools &> /dev/null
if [ $? -ne 0 ]; then
    pip install RBTools
fi

mysql -u'review' -p"123456789" <<EOF
CREATE TABLE IF NOT EXISTS reviewboard.tools_review (
review_request_id INT(11) not null,
change_list_name VARCHAR(255),
username VARCHAR(255),
PRIMARY KEY(review_request_id)
);
CREATE TABLE IF NOT EXISTS reviewboard.tools_file_md5 (
review_request_id INT(11) not null,
file_name VARCHAR(255),
md5 VARCHAR(255),
PRIMARY KEY(review_request_id)
);
CREATE TABLE IF NOT EXISTS reviewboard.tools_changelist (
username VARCHAR(255),
changelist VARCHAR(255),
version INT(11),
isdir BOOLEAN,
PRIMARY KEY(username)
);
EOF
# sshpass -p'suweisheng' scp -r suweisheng@192.168.170.5:~/tools/vir_copy.sh /root/
# sshpass -p'suweisheng' scp -r suweisheng@192.168.170.5:~/tools/svn*.py /root/
# 在http://192.168.170.99/reviews 管理ui中添加p1存储库
# python svnr.py config
# python svnhelp.py cl xx
# python svnhelp.py pr xx
# python svnhelp.py ci xx

# 在EOF前面加\或在 “EOF” 或 ‘EOF’ 都能实现不转义
cat >/svn/p1/hooks/pre-commit<<\EOF
#!/bin/sh
REPOS="$1"
TXN="$2"
SVNLOOK=/usr/bin/svnlook

# 日志
# $SVNLOOK info -t "$TXN" "$REPOS" >&2

# diff 文件
# $SVNLOOK changed -t "$TXN" "$REPOS" >&2

# diff 内容
# $SVNLOOK diff -t "$TXN" "$REPOS" >&2

# exit 1

exit 0
EOF
# chmod u+x /svn/p1/hooks/pre-commit
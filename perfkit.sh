#!/bin/bash

# Add key so we can ssh to localhost
rm -f /tmp/pkb_key /tmp/pkb_key.pub
ssh-keygen -t rsa -N "" -f /tmp/pkb_key
cat /tmp/pkb_key.pub >> ~/.ssh/authorized_keys

# Configure a static VM for localhost
mkdir -p /tmp/pkb_data_dir
tee ssh.yaml <<EOF
static_vms:
  - &vm1
    ip_address: 127.0.0.1
    user_name: root
    ssh_private_key: /tmp/pkb_key
    zone: unused
    disk_specs:
      - mount_point: /tmp/pkb_data_dir

install_package:
  vm_groups:
    default:
      static_vms:
        - *vm1
EOF

# Install the packages
./pkb.py --benchmarks=install_package --benchmark_config_file=ssh.yaml \
--ip_addresses=EXTERNAL --run_stage provision,prepare \
--packages=bonnieplusplus,build_tools,cassandra,cassandra_stress,curl,docker,fio,fortran,hadoop,hbase,hpcc,iperf,memtier,mongodb_server,multilib,mysql,netperf,numactl,oldisim_dependencies,openjdk,openssl,pip,redis_server,silo,sysbench,tomcat,unixbench,unzip,wget,wrk,ycsb

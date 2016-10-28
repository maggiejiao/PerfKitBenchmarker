import logging
from perfkitbenchmarker import configs
from perfkitbenchmarker import flags
from perfkitbenchmarker import linux_packages

flags.DEFINE_list('packages', [], 'Install packages.')

BENCHMARK_NAME = 'install_package'
BENCHMARK_CONFIG = """
install_package:
  description: >
    Install packages.
  vm_groups:
    default:
      vm_spec: *default_single_core
      vm_count: 1
      disk_spec: *default_500_gb
  flags:
    gcloud_scopes: >
      https://www.googleapis.com/auth/devstorage.read_write"""

SKIPPED_PACKAGES = frozenset([
    'wrk_runner', 'ycsb_helium', 'helium', 'mapkeeper'])

def GetConfig(user_config):
  return configs.LoadConfig(BENCHMARK_CONFIG, user_config, BENCHMARK_NAME)

def Prepare(benchmark_spec):
  """Install all packages.

  Args:
    benchmark_spec: The benchmark specification. Contains all data that is
      required to run the benchmark.
  """
  vm = benchmark_spec.vms[0]
  for package in flags.FLAGS.packages or linux_packages.PACKAGES.keys():
    logging.info('Installing %s', package)
    if package in SKIPPED_PACKAGES:
      continue
    try:
      vm.Install(package)
    except:
      logging.info('Failed to install %s', package)

def Run(benchmark_spec):
  """Run benchmark.

  Args:
    benchmark_spec: The benchmark specification. Contains all data that is
        required to run the benchmark.

  Returns:
    A list of sample.Sample instances.
  """
  vm = benchmark_spec.vms[0]
  vm.RemoteCommand('sudo rm /etc/init/mounted-tmp.conf', ignore_failure=True)
  vm.RemoteCommand('sudo sync')
  vm.RemoteCommand('sudo chmod -R u+rw,g+rw,o+rw /scratch/')
  vm.RemoteCommand('sudo chmod -R u+rw,g+rw,o+rw /scratch1/')
  vm.RemoteCommand('sudo chmod -R u+rw,g+rw,o+rw /root/PerfKitBenchmarker')
  vm.RemoteCommand('sudo chmod -R u+rw,g+rw,o+rw /tmp/pkb')

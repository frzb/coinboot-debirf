# Copyright (C) 2018 Gunter Miegel coinboot.io
#
# This file is part of Coinboot.
#
# Coinboot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


$make_kernel_and_rootfs = <<SCRIPT
set -e
apt update
apt install --yes debirf bc

# We have a customized version of debirf
# with an adapted 'init' script able to
# pull and extract plugins.
cp /vagrant/debirf /usr/bin/debirf

# Lets replace single threaded gzip
# with pgiz that can use multiple cores.
# Also set some symlink to use it as
# drop-in-replacment.
apt install --yes pigz lbzip2 pbzip2

ln -fs /usr/bin/lbzip2 /usr/local/bin/bzip2
ln -fs /usr/bin/lbzip2 /usr/local/bin/bunzip2
ln -fs /usr/bin/lbzip2 /usr/local/bin/bzcat
ln -fs /usr/bin/pigz /usr/local/bin/gzip
ln -fs /usr/bin/pigz /usr/local/bin/gunzip
ln -fs /usr/bin/pigz /usr/local/bin/zcat

# export variables of the debirf profile
source /vagrant/profiles/coinboot/debirf.conf

# FIXME: Setting variant=minbase shrink the rootfs archive by ~10M, but access over network and serial fails.
# sudo sed -i 's#eval "/usr/sbin/debootstrap $OPTS"#eval "/usr/sbin/debootstrap --variant=minbase $OPTS"#' $(which debirf)

# debootstrap can not handle that /vagrant is mounted with noexec or nodev
# so we copy the debirf profile to /tmp
cp -vr /vagrant/profiles/coinboot /tmp


#Force a root build without fakeroot
time su - ubuntu -c 'sudo debirf make -n --root-build --no-warning /tmp/coinboot'

sudo cp -v /tmp/coinboot/vmlinuz* /vagrant/build/coinboot-vmlinuz-$DEBIRF_KERNEL
sudo cp -v /tmp/coinboot/*.cgz /vagrant/build/coinboot-initramfs-$DEBIRF_KERNEL

sudo chmod -v 644 /vagrant/build/*

SCRIPT

Vagrant.configure(2) do |config|
  # Dynamically allign number of core of the built VM with the host
  # to speed up things as much as possible.
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", `#{RbConfig::CONFIG['host_os'] =~ /darwin/ ? 'sysctl -n hw.ncpu' : 'nproc'}`.chomp]
    vb.customize ["modifyvm", :id, "--memory", 2048]
  end

  config.vm.define "make-rootfs" do |machine|
  machine.vm.box = "ubuntu/xenial64"
  machine.vm.hostname = "make-rootfs"
  # FIXME: Have a look at this Kernel version issue in general.
  # Take care that the built box is running on the most recent kernel.
  # For that we have to reboot the Vagrant box which is achieved by
  # the reload-plugin.
  #config.vm.provision "shell", inline: 'apt update; apt dist-upgrade --yes'
  config.vm.provision "shell", inline: 'apt update; apt upgrade --yes'
  config.vm.provision "shell", inline: 'source /vagrant/profiles/coinboot/debirf.conf && apt install linux-image-$DEBIRF_KERNEL --yes'
  config.vm.provision :reload
  config.vm.provision "shell", inline: $make_kernel_and_rootfs
  # Dynamically allign number of core of the built VM with the host
  # to speed up things as much as possible.
  end
  end


# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "vmbox.box" #the name of the box
  	#config.vm.provider "virtualbox" do |v|
		#v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]  # can't take more than 50% of CPU
		#v.memory = 2048  #can deal with 2gb memory
	#end
  config.vm.communicator = "winrm"
  
    config.winrm.username = "vagrant"
    config.winrm.password = "vagrant"

    config.vm.guest = :windows
    config.windows.halt_timeout = 60 #maximum time in which the vm can start
	config.vm.synced_folder '.', '/vagrant', disabled: true  #disable shared folder
end

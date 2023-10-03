##########################################################################################
# capytiveportal - version 1.0
# TERMINALX - OPENSOURCE SOLUTIONS
# Bruno Carvalho - Diretor Tecnológico
# Email: bruno@terminalx.net.br
# Whatssap: +55 35 984413336
##########################################################################################
# This script is a hostspot that uses an httpd lib to instantiate an http server thus presenting a login page.
# To access the internet, registration is required.
# For this script to work it is necessary to create a table structure using mariadb:
# varchar name field, varchar email field, varchar city field, varchar phone field.
# A Raspberry Pi 4 was used, 4RAM, with a USB/Ethernet 3.0 gigabit interface, running Debian, with some iptables rules doing Nat, 
# DHCP between the internet # and the local network, an access point with the open wifi network within the lan .
# Any user who wants to browse will have to authenticate, that is, register for browsing.


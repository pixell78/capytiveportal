# CapytivePortal - Versão 1.0
**TERMINALX - SOLUÇÕES OPEN SOURCE**
**Bruno Carvalho - Diretor Tecnológico**
- Email: bruno@terminalx.net.br
- WhatsApp: +55 35 984413336

## Descrição
Este script é um hotspot que utiliza uma biblioteca httpd para instanciar um servidor http, apresentando assim uma página de login.
Para acessar a internet, é necessário fazer um registro no sistema.
Este servidor atua como um roteador com duas placas de rede, uma autenticando a internet e a outra fazendo um DHCP Server para a rede lan.
Qualquer host que se conectar a essa rede receberá um ip, porém so será "Natiado" caso um cadastro na base de dados seja feita.

Para que este script funcione, é necessário criar uma estrutura de tabela usando o MariaDB:
- Campo nome do tipo varchar
- Campo email do tipo varchar
- Campo cidade do tipo varchar
- Campo telefone do tipo varchar

## Configuração de Hardware
Foi utilizado um Raspberry Pi 4 com 4GB de RAM, uma interface USB/Ethernet 3.0 gigabit, executando Debian. Algumas regras iptables foram utilizadas para fazer NAT, DHCP entre a internet e a rede local, além de um ponto de acesso com a rede Wi-Fi aberta dentro da LAN.

## Autenticação de Usuários
Qualquer usuário que deseje navegar precisará se autenticar, ou seja, se registrar para poder acessar a internet.


# CapytivePortal - Versão 1.0
**TERMINALX - SOLUÇÕES OPEN SOURCE**
**Bruno Carvalho - Diretor Tecnológico**
- Email: bruno@terminalx.net.br
- WhatsApp: +55 35 984413336

## Descrição
Este script é uma adaptação de um script que valida um usuário pre determinado em codigo fonte.
Nesse versão contamos com uma camada de banco de dados(mariadb) para cadastro e coleta de emails em um sistema de hotspot que utiliza uma biblioteca httpd para instanciar um servidor http, apresentando assim uma página de login.
Para acessar a internet, é necessário fazer um registro no sistema.
Este servidor atua como um roteador com duas placas de rede, uma autenticando a internet e a outra fazendo um DHCP Server para a rede lan.
Qualquer host que se conectar a essa rede receberá um ip, porém so será "Natiado" caso um cadastro na base de dados seja feita.
Toda parte de firewall e NAT dos hosts cadastrados é feita em iptables.

Para que este script funcione, é necessário criar uma estrutura de tabela usando o MariaDB:
- Campo nome do tipo varchar
- Campo email do tipo varchar
- Campo cidade do tipo varchar
- Campo telefone do tipo varchar

- Configurar a conexão com a base de dados no metodo connect_to_database():

## Configuração de Hardware
Foi utilizado um Raspberry Pi 4 com 4GB de RAM, uma interface USB/Ethernet 3.0 gigabit, executando Debian. Algumas regras iptables foram utilizadas para fazer NAT, DHCP entre a internet e a rede local, além de um ponto de acesso com a rede Wi-Fi aberta dentro da LAN.

## Autenticação de Usuários
Qualquer usuário que deseje navegar precisará se autenticar, ou seja, se registrar para poder acessar a internet.


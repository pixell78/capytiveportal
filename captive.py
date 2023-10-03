#!/usr/bin/env python3
import subprocess
import http.server
import cgi
import os
import mariadb
import sys
import time
# These variables are used as settings
PORT       = 9090         # the port in which the captive portal web server listens 
IFACE      = "eth0"      # the interface that captive portal protects
IP_ADDRESS = "10.0.0.1" # the ip address of the captive portal (it can be the IP of IFACE) 

###########################################################################################################################
################################ LIMPA AS REGRAS DE IPTABLES QUANDO REINICIA ##############################################
###########################################################################################################################

def iptables_clear():
    print ("* Limpando regras IPTABLES *")
    subprocess.call(["iptables","-t", "nat", "-F"])
    subprocess.call(["iptables","-F"])
    subprocess.call(["iptables","-t", "nat", "-A", "POSTROUTING", "-o", "eth1", "-j", "MASQUERADE"]) #NAT MASQUERADE SEM PORTAL

############################################################################################################################
######################################## CONEXAO COM A BASE DE DADOS #######################################################
############################################################################################################################
def connect_to_database():
    try:
        conn = mariadb.connect(
            user="root",
            password="password",
            host="localhost",
            database="DBName"
        )
        cur = conn.cursor()
        return cur, conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

# Chamando a função para obter o cursor e a conexão
    cursor, connection = connect_to_database()
    return cursor, connection
############################################################################################################################
#################################### HTTPD SERVER USADO NO CAPTIVE PORTAL CLASSE http.server ###############################
############################################################################################################################
class CaptivePortal(http.server.BaseHTTPRequestHandler):
    #this is the index of the captive portal
    #it simply redirects the user to the to login page
###########HTML###############################################################

    html_redirect = """
    <html>
    <head>
    <meta http-equiv="refresh" content="0; url=http://%s:%s/login" />
    </head>
    <body>
    <h1>Redirecionando para pagina de login...</h1>
    </body>
    </html>
    """%(IP_ADDRESS, PORT)
 
    #pagina do evento
    html_redirect_hack = """
    <html>
    <head>
    <meta http-equiv="refresh" content="0; url=https://seusite.com.br" />
    </head>
    <body>
    <h1>...</h1>
    </body>
    </html>
    """   
     #the insert page
    html_login = """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8" />
    <title>H4CKP0RT4L 4C3SS0</title>
    
    <!-- AREA JS -->
    <script>
    // $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Valida os campos em branco do form $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        function validateForm()
        {
            var nome = document.forms["valida"]["nome"].value;
            var email = document.forms["valida"]["email"].value;
            var cidade = document.forms["valida"]["cidade"].value;
            var telefone = document.forms["valida"]["fone"].value;
            var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  
            if (nome == "" || email == "") 
            {
                alert("Por favor, preencha os campos para navegar.");
                return false; // Impede o envio do formulário
            }
          
            else if (!emailRegex.test(email))
            {
                alert("Email inválido. Por favor, insira um email válido.");
                return false; // Impede o envio do formulário
           }
        }
    //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    
        
   //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ formata o numero do telefone $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        function formatarfone(fone)
          {
             // Remove todos os caracteres que não são dígitos
             const numeros = fone.replace(/\D/g, '');

            // Formata o número de acordo com o padrão (00)-00000-0000
            const formato = `(${numeros.substring(0, 2)})-${numeros.substring(2, 7)}-${numeros.substring(7, 11)}`;
      
           return formato;
          }

      function atualizarCampo()
      {
          const foneCampo = document.getElementById('fone');
          const foneFormatado = formatarfone(foneCampo.value);
          foneCampo.value = foneFormatado;
      }
    //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
    //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ formata o formato do email $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
 /*   function validarEmail() {
    const emailCampo = document.getElementById('email');
    const email = emailCampo.value;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    if (emailRegex.test(email)) {
        emailCampo.classList.remove('invalid');
        emailCampo.classList.add('valid');
    } else {
        emailCampo.classList.remove('valid');
        emailCampo.classList.add('invalid');
    }
}

document.getElementById("valida").addEventListener("submit", function(event) {
    const emailCampo = document.getElementById('email');
    const email = emailCampo.value;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    if (!emailRegex.test(email)) {
        event.preventDefault(); // Impede o envio do formulário
        emailCampo.classList.remove('valid');
        emailCampo.classList.add('invalid');
        alert("Email inválido. Por favor, insira um email válido.");
    }
}); */
    
  //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$      
  </script>

    <!-- AREA CSS -->
    <link rel="stylesheet" href="form.css">
    <style>
    @font-face 
    {
    font-family: 'Roboto Mono';
    font-style: normal;
    font-weight: 400;
    src: local('Roboto Mono'), local('RobotoMono-Regular'), url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap') format('woff2');
    }
  
    @font-face
    {
    font-family: 'Orbitron';
    font-style: normal;
    font-weight: 400;
    src: local('Orbitron'), url('/usr/local/captive-portal/fontes/Orbitron-Black.woff2') format('woff2');
    }
    html,body
    {
      height:100%
      overflow: hidden;
    }
    *
    {
     margin:0;
     padding:0;
     background-color: rgb(255,20,147);
    }
    .footer
    {
    width: 100%;
    padding: 3px;
    color: white;
    text-align: center;
    margin-top: 3px;
    font-size: 10px; /* Tamanho da fonte pequena */
    background: black;
    font-family: 'Roboto Mono', monospace;
    font-weight: bold;
    }  
    
    /* Estilize o placeholder */
    ::placeholder
    {
     color: white; /* Defina a cor desejada */
     font-family: 'Roboto Mono', monospace;
     font-weight: bold;
    }

    /* Estilize o placeholder em navegadores mais antigos */
    :-ms-input-placeholder
    {
     color: white; /* Defina a cor desejada */
     font-family: 'Roboto Mono', monospace;
     font-weight: bold;
    }

    /* Estilize o placeholder em navegadores do Internet Explorer 10-11 */
    ::-ms-input-placeholder
    {
    font-family: 'Roboto Mono', monospace; 
    color: white; /* Defina a cor desejada */
    font-weight: bold;
    }
    .image-abelha
    {
    display: flex;
    justify-content: left;
    align-items: flex-start; /* Alinhar no topo direta */
    margin: 0;
    }
    .image-logo
    {
    display: flex;
    justify-content: right;
    align-items: flex-start; /* Alinhar no topo esquerda */
    margin: 0;
    }
    </style>
    
    </head>
    <body>
    <div class="image-abelha">
    <img src="hacklogo1.png" style="width: 100px; height: 80px;" alt="logo_hacktown1">
    </div>
    <div style="max-width: 400px; margin: 0 auto; padding: 20px; background-color: purple; border: 1px solid pink; border-radius: 5px;">
    <p style="width: 100%; padding: 5px; color:white; text-align: center; margin-bottom: 10px; ,font-family:'Roboto Mono', monospace; font-weight: bold;">Somente nome e e-mail são necessários para o login, vc fornce os outros dados se quiser! Divirta-se! </p>
    </div>
    <div style="max-width: 400px; margin: 0 auto; padding: 20px; background-color: purple; border: 1px solid pink; border-radius: 5px;">
      <form name=valida onsubmit="return validateForm()" method="POST" action="do_cadastro">
      <input type="text" name="nome" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 3px;" color:white; placeholder="Nome:">
      <input type="text" name="email" id="email" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 3px;" placeholder="Email:">
      <input type="text" name="cidade" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 3px;" placeholder="Cidade:">
      <input type="text" name="fone" id="fone" onkeyup="atualizarCampo()" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 3px;" placeholder="Fone:">
      <input type="submit" style="display: block; width: 100%; padding: 10px; background-color: purple; color: #fff; border: none; border-radius: 3px; cursor: pointer;" value="ACESSAR">
      </form>  
      <div class="footer">POWERED BY TERMINAL X</a>!</div>
    </div>
    <div class="image-logo">
    <img src="hacklogo.png" alt="logo_hacktown">
    </div>
    </body>
    </html>
    """
    '''
    if the user requests the login page show it, else
    use the redirect page
    '''
  ###################################HTML##########################################
    def do_GET(self):
        path = self.path
        if path == "/login":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.html_login.encode('utf-8'))

        elif self.path in ('/hacklogo1.png', '/hacklogo.png'):
            try:
                if self.path == '/hacklogo.png':
                    image_path = '/usr/local/captive-portal/hacklogo.png'
                else:
                    image_path = '/usr/local/captive-portal/hacklogo1.png'
        
                with open(image_path, 'rb') as image_file:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/png')
                    self.end_headers()
                    self.wfile.write(image_file.read())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b'Imagem nao encontrada')
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.html_redirect.encode('utf-8'))

    '''
    this is called when the user submits the login form
    '''
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        
        ###OPERACOES COM BANCOS DE DADOS
        nome      =  form.getvalue("nome")
        email    =  form.getvalue("email")
        cidade  =  form.getvalue("cidade")
        fone = form.getvalue("fone")

        cursor, connection = connect_to_database()
        #Querie SQL        
        query1 = "SELECT email FROM informacoes WHERE email = ?"
        cursor.execute(query1, (email,))
        results = cursor.fetchall()
        #print(results)
        if results:    
            #authorized user
            remote_IP = self.client_address[0]
            print ('New authorization from '+ remote_IP)
            print ('Updating IP tables')
            subprocess.call(["iptables","-t", "nat", "-I", "PREROUTING","1", "-s", remote_IP, "-j" ,"ACCEPT"])
            subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j" ,"ACCEPT"])
            connection.close()
            cursor.close()
            self.wfile.write("Seja bem vindo(a) novamente!".encode('utf-8'))
            self.wfile.write(self.html_redirect_hack.encode('utf-8'))
        else:
            # Query SQL
            query2 = f"INSERT INTO informacoes(nome, email, cidade, fone) VALUES ('{nome}', '{email}', '{cidade}', '{fone}');"
            cursor.execute(query2) 
            connection.commit()
            #authorized user
            remote_IP = self.client_address[0]
            print ('New authorization from '+ remote_IP)
            print ('Updating IP tables')
            subprocess.call(["iptables","-t", "nat", "-I", "PREROUTING","1", "-s", remote_IP, "-j" ,"ACCEPT"])
            subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j" ,"ACCEPT"])
            connection.close()
            cursor.close() 
            self.wfile.write("Seja bem vindo(a)! Pode navegar agora!".encode('utf-8'))
            self.wfile.write(self.html_redirect_hack.encode('utf-8'))
            #show the login form
                 
    #the following function makes server produce no output
    #comment it out if you want to print diagnostic messages
    #def log_message(self, format, *args):
    #    return
print ("*********************************************")
print ("* Note, if there are already iptables rules *")
print ("* this script may not work. Flush iptables  *")
print ("* at your own risk using iptables -F        *")
print ("*********************************************")
print ("Updating iptables")
print (".. Allow TCP DNS")
subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j" ,"ACCEPT"])
print (".. Allow UDP DNS")
subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j" ,"ACCEPT"])
print (".. Allow traffic to captive portal")
subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT),"-d", IP_ADDRESS, "-j" ,"ACCEPT"])
print (".. Block all other traffic")
subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-j" ,"DROP"])
print ("Starting web server")
httpd = http.server.HTTPServer(('', PORT), CaptivePortal)
print ("Redirecting HTTP traffic to captive portal")
subprocess.call(["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j" ,"DNAT", "--to-destination", IP_ADDRESS+":"+str(PORT)])
#########################################################################################################################################################################
############################################################## PROGRAMA PRINCIPAL ########################################################################################
##########################################################################################################################################################################
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
iptables_clear()

# **Backend Safe Strategy**

## **Como Rodar o Container**

### **Pré-requisitos**
- Docker instalado na máquina. ([Guia de instalação](https://docs.docker.com/get-docker/))
- Permissão de administrador para editar o arquivo `hosts`.

---

### **Passo 1: Configurar o Host Local**
Adicione a seguinte entrada ao arquivo `hosts` para acessar o domínio localmente:

**Windows**
1. Abra o arquivo `C:\Windows\System32\drivers\etc\hosts` com um editor de texto (como o Notepad) no modo **Administrador**.
2. Adicione a linha abaixo ao final do arquivo:

   ```
   127.0.0.1 api-local.safestrategy.com.br
   ```

**Linux/MacOS**
1. Edite o arquivo `/etc/hosts` com privilégios de root:
   ```bash
   sudo nano /etc/hosts
   ```
2. Adicione a linha abaixo ao final do arquivo:
   ```
   127.0.0.1 api-local.safestrategy.com.br
   ```
3. Salve e feche o arquivo.

---

### **Passo 2: Construir a Imagem Docker**
No diretório onde está o `Dockerfile`, execute o comando abaixo para construir a imagem Docker:

```bash
docker build -t apisafestrategycom:latest .
```

---

### **Passo 3: Rodar o Contêiner**
Para iniciar o contêiner e mapear as portas **80** e **443**, execute o comando abaixo:

```bash
docker run -p 80:80 -p 443:443 -v .:/var/www/backend apisafestrategycom:latest
```

---

### **Passo 4: Acessar a API**
Após iniciar o contêiner, a API estará disponível no seguinte endereço:

🔗 [**https://api-local.safestrategy.com.br**](https://api-local.safestrategy.com.br)

---

### **Dica Adicional**
- Para verificar os logs do contêiner em tempo real:
  ```bash
  docker logs -f <container_id>
  ```

- Para parar o contêiner:
  ```bash
  docker ps  # Identifique o ID do contêiner
  docker stop <container_id>
  ```

---

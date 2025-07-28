# Sistema de Gerenciamento de Escola
Olá! Este é um projeto do curso Programação de Sistemas para Web (PSW) pelo professor Carlos Anderson Oliveira Silva, no qual usamos Django e Bootstrap na versão 5 e foi desenvolvido pelos alunos do IF Baiano - Campus Guanambi.<br>
São eles: 

| Adriel Lima                                                                                   | Emilly Victoria                                                                                 | Vinícius Morais                                                                                 |
| :---------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------: |
| <a href="https://www.instagram.com/wrttdriel/"><img src="https://github.com/user-attachments/assets/45e6c560-ff1b-4bd7-9ea0-2ec6b8cfc48a" width="150" height="150"></a> | <a href="https://www.instagram.com/emillyszf/"><img src="https://github.com/user-attachments/assets/8a459df9-41e4-4dc4-8361-cb00cd794882" width="150" height="150"></a> | <a href="https://www.instagram.com/wtfvinaa/"><img src="https://github.com/user-attachments/assets/ed14cfb8-6721-43e9-a474-da1c94e16ee5" width="150" height="150"></a> |

---

## Instruções para Rodar o Projeto

Para configurar e rodar o projeto de Gerenciamento de Sistema de Escola no seu ambiente local, siga os passos abaixo.

### Pré-requisitos

Certifique-se de ter os seguintes softwares instalados antes de iniciar:

* **Python 3.13**: [Baixe aqui](https://www.python.org/downloads/release/python-3132/)
* **VS Code**: [Baixe aqui](https://code.visualstudio.com/download)

### Configuração do Ambiente

1.  **Baixe e Abra o Projeto:**
    * Clone ou baixe o repositório do GitHub para o seu computador.
    * Caso **BAIXE**, recomendamos renomear a pasta para `psw`.
    * Para abrir o projeto no VS Code, selecione a pasta `psw` e clique com o botão direito. Vá em "Mostrar mais opções" e depois em "Abrir com Code".<br>
        ![Image of folder selection in VS Code](https://github.com/user-attachments/assets/637e19b7-95ef-4f4e-9f2f-cf1bfa7040f7)<br>
        ![Image of "Open with Code" option](https://github.com/user-attachments/assets/47960288-5148-40be-97ce-df01809d1980)<br>
    * Ao abrir, confirme a confiança nos autores da pasta, se solicitado:<br>
        ![Image of trust prompt in VS Code](https://github.com/user-attachments/assets/bc4daeb9-b84f-4ada-837a-51215a025efd)<br><br>
    * Caso **CLONE**, crie uma pasta para o nome `psw` para depois fazer os processos ensinados anteriormente de "Abrir com Code".<br>
    *  No terminal, que tem a seguir um tutorial de como abrir, com ele aberto cole o seguinte código antes de fazer qualquer coisa:
         ```bash
         git clone https://github.com/driizin/psw-sgde.git
         ```
         ![image](https://github.com/user-attachments/assets/fb5c95e6-b6ff-4d6b-b434-1421a9de540d)


2.  **Abra o Terminal no VS Code:**
    * No VS Code, abra o arquivo `manage.py` no lado esquerdo.<br>
        ![Image of main.py in VS Code sidebar](https://github.com/user-attachments/assets/13c42d7c-13d5-41fd-ae80-75f5c20af962)
    * Vá na parte superior do aplicativo e selecione **Terminal > Novo Terminal**.<br>
        ![Image of Terminal menu in VS Code](https://github.com/user-attachments/assets/27569e8b-1ac0-4e7a-b600-ad85890bafc4)<br>
        ![Image of New Terminal option](https://github.com/user-attachments/assets/c76451a6-8252-4808-91ad-cd31fe61fe9b)<br>
        ![Image of terminal type selection in VS Code](https://github.com/user-attachments/assets/06a7a9cc-b192-437e-b4db-abee67938afe)<br>

3.  **Crie e Ative o Ambiente Virtual:**
    * Para criar um ambiente virtual chamado `psw` (recomendado para isolar as dependências do projeto), execute:
        ```bash
        py -3.13 -m venv psw
        ```
        ![Image of venv creation command](https://github.com/user-attachments/assets/81281276-7d51-4ec7-96ce-03a051240a5d)
    * Ative o ambiente virtual. Você deve ver `(psw)` no início da linha de comando. **Os comandos de ativação variam de acordo com o sistema operacional:**
        * **No Windows (CMD/PowerShell):**
            ```bash
            .\psw\Scripts\activate
            ```
            ![Image of Windows virtual environment activation](https://github.com/user-attachments/assets/64667b8a-891e-4f9c-a377-1f481c45ea4b)
        * **No Linux / macOS (Bash/Zsh):**
            ```bash
            source psw/Scripts/activate
            ```
            ![Image of Linux and macOS virtual environment activation](https://github.com/user-attachments/assets/32f85aab-1663-4b0e-8e88-81cfef0101d3)

    * Verifique se o VS Code está usando o interpretador Python correto (Python 3.13 do ambiente `psw`). Ele aparece no canto inferior direito. Se não estiver, clique nele e selecione "Python 3.13.2 ('psw':venv)".<br>
        ![Image of Python interpreter selection in VS Code](https://github.com/user-attachments/assets/f20aa7ae-2743-4363-b120-db727df2577b)<br>
        ![Image of Python versions list](https://github.com/user-attachments/assets/e6c3e9ae-e026-47d5-a5c5-4f691a7ccefd)

4.  **Instale as Dependências do Projeto:**
    Com o ambiente virtual **`psw`** ativado, instale todas as bibliotecas Python necessárias para o projeto. O arquivo `requirements.txt` garante que todas as dependências sejam instaladas nas versões exatas, assegurando a compatibilidade e a funcionalidade do Projeto.

    No terminal, execute:
    ```bash
    pip install -r requirements.txt
    ```
### Rodando o Projeto

1.  **Inicie o Servidor do Projeto:**
    * Com todas as configurações anteriores feitas e seu ambiente virtual `psw` ativado no terminal do VS Code:
    * No terminal digite isso:<br>
    ```bash
    python manage.py runserver
    ```

2.  **Acesse o Projeto no Navegador:**
    * Após iniciar o servidor, o terminal indicará o endereço local onde o Projeto está rodando. Geralmente, será:
        http://127.0.0.1:8000
        ![Image of Projeto running on localhost](https://github.com/user-attachments/assets/a095dad3-d04c-4729-ba70-02030db6ede7)<br>
    * Abra seu navegador e acesse esse endereço.

    **Apresentação Vídeo do Projeto:**
    
    <iframe width="560" height="315" src="https://www.youtube.com/embed/eVnCa5wuwdU?si=7kCFDV-bTc-Wo-D9" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
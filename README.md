# Sistema de Gerenciamento de Tarefas 📚

## Descrição do Projeto

Este projeto é uma API RESTful para um sistema de gerenciamento de tarefas, construída com Python e Django. A API permite a criação, leitura, atualização e exclusão de tarefas, e inclui autenticação JWT para proteção dos endpoints. A aplicação está configurada para ser executada em containers Docker e foram realizados testes para garantir a funcionalidade e qualidade do código.

Além disso, o projeto utiliza o Poetry para gerenciamento de dependências e configuração do ambiente. O Poetry simplifica o gerenciamento de pacotes e versões, gerando um arquivo pyproject.toml mais limpo e eficiente em comparação com o tradicional requirements.txt. Isso facilita a reprodução do ambiente de desenvolvimento e a manutenção do projeto.

## Ferramentas Utilizadas

Para a construção do projeto, foram utilizadas as versões mais recentes das ferramentas disponíveis em 2024:

- **Python**: 3.12
- **Django**: 5.0
- **Django REST Framework**
- **PostgreSQL**
- **Docker**
- **Poetry**: para gerenciamento de dependências
- **Ruff**: para linting e formatação de código
- **Taskpy**: para gerenciamento de tarefas de projeto

## Funcionalidades do Projeto

- **Autenticação de Usuário**: Implementação completa de autenticação para garantir a segurança e integridade dos dados.
- **Operações CRUD**: Criação, leitura, atualização e exclusão de tarefas. Além da busca por título ou data.
- **Documentação**: A API é documentada utilizando Swagger, permitindo explorar e testar os endpoints.
- **Validações e Erros**: Implementa validações para campos obrigatórios e retornos de erros apropriados.
- **Filtragem e Pesquisa**: Filtra e pesquisa tarefas por título ou data de vencimento.

## Testes

Foram realizados testes para garantir a funcionalidade e a qualidade do código. Esses testes cobrem os principais casos de uso da API e ajudam a assegurar que o sistema funciona conforme o esperado.

## Como Baixar e Executar o Projeto
### Com Docker

1. **Clone o Repositório**

   ```sh
   git clone https://github.com/zeguil/Desafio-Backend.git

   cd Desafio-Backend
   ```

2. **Construa e inicie os containers Docker:**

   No diretório do projeto, execute:

   ```sh
   docker-compose up --build
   ```

Isso irá construir a imagem do Docker, iniciar o container para a aplicação Django e o container para o banco de dados PostgreSQL.

### Sem Docker


1. **Clone o Repositório**

   ```sh
   git clone https://github.com/zeguil/Desafio-Backend.git

   cd Desafio-Backend
   ```


2. **Instale o Poetry**

   ```sh
    pip install pipx 
    pipx install poetry
    pipx esurepath
   ```
   É necessário fechar o terminal e abrir novamente

3. **Instale as Dependências**

   No diretório do projeto, execute:

   ```sh
   poetry install
   ```
4. **Configure o banco de dados PostgreSQL:**
Edite o arquivo settings.py para incluir as credenciais do banco de dados PostgreSQL:

   ```
      DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'nome_do_banco',
         'USER': 'usuario',
         'PASSWORD': 'senha',
         'HOST': 'localhost',
         'PORT': '5432',
         }}
      
   ```

5. **Ative o Ambiente Virtual do Poetry**

   ```
   poetry shell
   ```

6. **Execute as migrações do banco de dados:**

   ```
   task migrate
   ```
7. **Crie um super usuário**

   ```
   task create_user
   ```

8. **Execute o Projeto**

   ```
   task run
   ```

8. **Caso queira rodar os testes**

   ```
   task test
   ```

## Documentação da API

A documentação da API está disponível no Swagger após iniciar o servidor em http://localhost:8000/docs/

#### Autenticação JWT

Todos os endpoints são protegidos e requerem autenticação JWT.

Para obter um token JWT:

Endpoint: POST token/

Corpo da Requisição:

```
{
    "username": "user",
    "password": "1234"
}
```


| **🚨 Atenção Importante 🚨**|
|-------------------------------|
| **Este usuário ja vem integrado no sistema para uso.** |
|usuario: user |
|senha: 1234 |

Resposta:

```
{
    "refresh": "string",
    "access": "string"
}
```

- copie o token retornado de 'access' para fazer login no sistema

- **Inclua o token JWT no clicando em Authorize no canto superior direito da página do Swagger**
![App Screenshot](https://uploaddeimagens.com.br/images/004/827/848/full/Authorize.png?1723966588)


- **Cole o token de acesso retornado com 'Bearer' na frente, dessa forma:**
![App Screenshot](https://uploaddeimagens.com.br/images/004/827/849/original/Bearer.png?1723966609)
- **Clique em 'Authorize' e todos os endpoints vão estar liberados para uso**




## Observações
- Certifique-se de ter as portas 8000 e 5432 disponíveis em sua máquina para evitar conflitos com outros serviços em execução.

## Créditos
- Desenvolvido por [José Guilherme Lins](https://github.com/zeguil)
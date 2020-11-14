# login_system

Esse projeto simula um sistema de login utilizando Django.

## Instalação

Como requisito para execução desse projeto, devem ser instalados os pacotes:

```
>> pip install jsonschema python_jwt

```

Para configurar e registrar os models corretamente no banco de dados:

```
>> python3 manage.py makemigrations 
>> python3 manage.py migrate

```

Em seguida, para iniciar o servidor:

```
>> python3 manage.py runserver

```

Para executar os testes:

```
>> python3 manage.py test

```


## Endpoints

O projeto possui 3 endpoints que são acessíveis via clientes HTTP (Recomendo Postman). A comunicação se dá por envio e recebimento de JSONs. Na versão base foi desabilitada a verificação de CSRF. Os endpoints são:

* signup/ 
* signin/
* me/

## Signup

Endpoint para criação de um novo usuário. Compatível apenas com o verbo POST. Os dados do usuário devem estar formatados em um JSON com a seguinte estrutura: 

```json
{
    "firstName": "joao",
    "lastName": "monte",
    "email": "joao.monte@joao.com",
    "password": "helloworld",
    "phones": [
        {
            "number": "12345678",
            "area_code": "81",
            "country_code": "+55"
        },
        {
            "number": "87654321",
            "area_code": "81",
            "country_code": "+55"
        }
    ]
}

```

Caso contrário, um erro de validação é informado. Em caso de sucesso, é retornado um token JWT do novo usuário criado. Seu tempo de expiração é de 10 minutos.

## Signin

Endpoint para login de um usuário já criado. Compatível apenas com o verbo POST. Os dados de login do usuário devem estar formatados em um JSON com a seguinte estrutura:

```json
{
    "email": "joao.monte@joao.com",
    "password": "helloworld",
}

```

Em caso de erro, uma mensagem será informada. Seja o erro de validação, login incorretoou e-mail inexistente. Em caso de sucesso, é retornado um token JWT do usuário. Seu tempo de expiração é de 10 minutos.

## me

Endpoint para recuperar as informações do usuário. Compatível apenas com o verbo GET. Deve ser fornecido no header da requisição o campo Authorization contendo como valor um token obtido nos endpoints signup ou signin. Em caso de erro, ou não fornecimento do token, uma mensagem é retornada. Em caso de sucesso são retornadas todas as informações do usuário cadastrado, exceto o password.


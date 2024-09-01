# Fast Finance

## Design

### Ideia
Website para gerenciar dados financeiros pessoais, de um jeito fácil, rapido e direto ao ponto. A ideia é ser simples, fácil, consistente e rapido.

### Functional Requirements
- Upload de arquivos csv contendo transações bancarias
- Página para **tabela**  `transaction` com n registros
  - Opção para ver mais informações sobre um registro especifico
- Página para **form** `transaction` com a maioria das informações de 1 registro
  - Opções para editar/deletar registro
- Página para **form** `transaction` para editar as informações do registro.
- Página para **form** `transaction` para criar um novo registro.
- Dashboard para agrupar e agregar informações vindas da tabela `transaction`.
- Exportar `transaction` para arquivo csv para download.

### Non-Functional Requirements
- UI responsiva.
- Teste para cada endpoint no minimo

### Technologies
| Tecnologia                                                          | Versão    |
| ----------                                                          | --------- |
| [Docker](https://www.docker.com/)                                   |           |
| [PostgreSQL](https://hub.docker.com/_/postgres/)                    | 13-alpine |
| [PGWeb](https://hub.docker.com/_/postgres/)                         | latest    |
| [Python](https://docs.python.org/3.11/)                             | 3.11      |
| [FastAPI](https://fastapi.tiangolo.com/)                            | 0.109     |
| [SQLModel](https://sqlmodel.tiangolo.com/)                          | 0.109     |
| [Pydantic](https://docs.pydantic.dev/)                              | 2.8       |
| [Jinja2Fragments](https://github.com/sponsfreixes/jinja2-fragments) | 1.2       |
| [HTMX](https://htmx.org/)                                           | 2.0       |
| [Bootstrap](https://getbootstrap.com/)                              | 5.3       |

#### Front-End
No front-end [Bootstrap](https://getbootstrap.com/) para estilização e responvidade da aplicação. [Jinja2Fragments](https://github.com/sponsfreixes/jinja2-fragments) para o backend retornar o conteudo HTML ao usuário e diferente do [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) ele pode retornar sómente blocos de HTML gerados no Jinja e isso junto com [HTMX](https://htmx.org/) torna possivel criar paginas que consigam conectar com o backend diretamente sem a necessidade de ter uma aplicação separada para o front-end já que HTMX te da acesso a AJAX, transições CSS, WebSockets e Server Sent Events direto no HTML.  
  
Utilizar as features do pydantic junto com jinja2-fragments para ter templates typadas.

#### Back-End
[FastAPI](https://fastapi.tiangolo.com/) um framework moderno de alta performance para construção de APIs, [Pydantic](https://docs.pydantic.dev/) para validação de dados.

#### Database
[SQLModel](https://sqlmodel.tiangolo.com/) como ORM e query builder para conexão com o banco de dados [PostgreSQL](https://hub.docker.com/_/postgres/).

##### Tables
###### Transações
Data
Valor
ID Externo
Tipo Descrição
Destino Descrição
Descrição Completa

#### PGWeb
Imagem docker utilizada no desenvolvimento para facilitar a visualização dos dados no banco de dados pela web.

# FastAPI CRUD (Create, Read, Update and Delete.)

## Users
| Funcionalidade | Método (HTTP)   | Caminho  |
| :---:   | :-: | :-: |
| Criar um usuário | POST | /users
| Ler um usuário da lista | GET | /users/{id}
| Ler todos os usuários |	GET | /users
| Atualizar um item | PUT | /users/{id}
| Deleta um item | DELETE | /users/{id}



## Items
| Funcionalidade | Método (HTTP)   | Caminho  |
| :---:   | :-: | :-: |
| Criar um item atrelado a um usuário | POST | /users/{user_id}/items
| Ler um item da lista | GET | /items/{id}
| Ler todos os itens |	GET | /items
| Atualizar um item | PUT | /items/{id}
| Deleta um item | DELETE | /items/{id}

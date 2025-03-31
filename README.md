

# Article-Chat

  
## Run Locally
This is a demo project to hone my skills 

Clone the project

```bash
  git clone https://github.com/sin1ter/article-chat.git
```

Go to the project directory

```bash
  cd article-chat
```

Install dependencies

# For Windows
```bash 
   python -m venv env

   env\Scripts\activate
```

 # For macOS/Linux
 ```bash
   python3 -m venv env
   
   source env/bin/activate
   ```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```
## API Reference

####  Accounts Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **POST** | `api/v1/accounts/login/` | To login a user |
| **POST** | `/api/v1/accounts/register/` | To register a user |


####  Article Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **GET** | `/api/articles/article/` | To retrieve list of articles | |
| **GET** | `api/articles/article/:id` | To retrieve specific article |
| **PUT** | `api/articles/article/:id/` | To update article |
| **PATCH** | `/api/articles/article/:id/` | To update a detail of a single article |
| **DELETE** | `api/articles/article/:id/` | To delete a single article |
####  Article Categories Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **GET** | `api/article/categories/` | To retrieve list of categories |
| **PUT** | `api/article/categories/:id/` | To update categories |
| **PATCH** | `/api/article/categories/:id/` | To update a detail of a single categories |
| **DELETE** | `api/article/categories/:id/` | To delete a single categories |

####  Chat Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **GET** | `api/chat/chatrooms/` | To retrieve group of chats|
| **POST** | `api/chat/chatrooms/` | To create a group|
| **PUT** | `api/chat/chatrooms/:id/` | To update chat group name |
| **PATCH** | `/api/chat/chatrooms/:id/` | To update chat group name |
| **DELETE** | `api/chat/chatrooms/:id/` | To delete chat group name |

####  Message Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| **GET** | `api/chat/message/<chat_id>` | To retrieve the messages group of chats|
| **POST** | `api/chat/message/<chat_id>/` | To post a message chat group name |


####  Socket Endpoints:
| HTTP | Endpoints | Action |
| --- | --- | --- |
| | `ws/chat/(?P<room_id>\d+)/` | To connect with users and send realtime chat message|



👤 **Symon**

- Github: [@sin1ter](https://github.com/sin1ter)

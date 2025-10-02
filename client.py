import uuid
import requests


# data = requests.post('http://127.0.0.1:8000/api/v1/todo', json={'title': 'todo_1', 'important': True})
# print(data.status_code)
# print(data.json())

# data = requests.get('http://127.0.0.1:8000/api/v1/todo/34')
# print(data.status_code)
# print(data.json())

# data = requests.patch('http://127.0.0.1:8000/api/v1/todo/1', json={'done': True, 'title': 'new_todo'})
# print(data.status_code)
# print(data.json())

# data = requests.get('http://127.0.0.1:8000/api/v1/todo/1')
# print(data.status_code)
# print(data.json())

# data = requests.delete('http://127.0.0.1:8000/api/v1/todo/1')
# print(data.status_code)
# print(data.json())

data = requests.post('http://127.0.0.1:8000/api/v1/user', json={'name': 'admin', 'password': '1234'})
print(data.status_code)
print(data.text)
print(data.json())

data = requests.post('http://127.0.0.1:8000/api/v1/user/login', json={'name': 'admin', 'password': '1234'})
print(data.status_code)
print(data.json())
token = data.json()['token']

data = requests.post('http://127.0.0.1:8000/api/v1/todo', json={'title': 'todo_1', 'important': True}, headers={'x-token': token})
print(data.status_code)
if data.status_code == 200:
    print(data.json())
else:
    print("Ошибка:", data.text) 


data = requests.get('http://127.0.0.1:8000/api/v1/todo/1', headers={'x-token': token})
print(data.status_code)
print(data.json())



# data = requests.post('http://127.0.0.1:8000/api/v1/user', json={'name': 'admin28', 'password': '1234'})
# print(data.status_code)  # Убедитесь, что статус-код 200 (или другой ожидаемый код)
# print(data.text) 


# data = requests.post('http://127.0.0.1:8000/api/v1/user/login', json={'name': 'admin28', 'password': '1234'})
# print(data.status_code)
# print(data.text)
# print(data.json())
# token = data.json()['token']

# data = requests.post('http://127.0.0.1:8000/api/v1/todo', json={'title': 'todo_1', 'important': True}, headers={'x-token': token})
# print(data.status_code)
# print(data.text)
# print(data.json())

# data = requests.get('http://127.0.0.1:8000/api/v1/todo/1', headers={'x-token': token})
# print(data.status_code)
# print(data.text)
# print(data.json())





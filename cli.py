import requests
import argparse
import json

# Specify the URL of your Flask application
BASE_URL = 'http://localhost:5000/cli/'

def add_person(name, email):
    data = {'nome': name, 'email': email}
    response = requests.post(BASE_URL + 'add_person', json=data)
    print(response.json())

def list_people():
    response = requests.get(BASE_URL + 'list_people')
    people = response.json()
    for person in people:
        print(f"Name: {person['nome']}, Email: {person['email']}")

def update_person(name, email):
    data = {'email': email}
    response = requests.put(BASE_URL + f'update_person/{name}', json=data)
    print(response.json())

def delete_person(name):
    response = requests.delete(BASE_URL + f'delete_person/{name}')
    print(response.json())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI for managing people')
    parser.add_argument('--add', nargs=2, help='Add a person: --add <name> <email>')
    parser.add_argument('--list', action='store_true', help='List all people')
    parser.add_argument('--update', nargs=2, help='Update a person\'s email: --update <name> <email>')
    parser.add_argument('--delete', help='Delete a person: --delete <name>')

    args = parser.parse_args()

    if args.add:
        add_person(args.add[0], args.add[1])
    elif args.list:
        list_people()
    elif args.update:
        update_person(args.update[0], args.update[1])
    elif args.delete:
        delete_person(args.delete)
    else:
        parser.print_help()

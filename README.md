# todo-cli

A simple cli todo utility to demonstrates a CRUD application with database connectivity via ORM.

## Requirements

```python
python~=3.11
PyYAML
SQLAlchemy
```

## Installation

- Create a virtual environment

```sh
python -m venv venv
```

- Activate the virtual environment

```sh
source venv/bin/activate
```

- Clone and install the requirements

```sh
git clone repository
pip install requirements.txt
```

## Usage

- Navigate to the repository root and run the usage commands.

### Add

```sh
# python todo.py add [title ...]
python todo.py add Hello, World
```

### List

- List all

```sh
python todo.py list
```

```sh
# output

uid | title | status
-------------------
1 | Hello, World | ❌
2 | update todo readme | ✅
```

- List by ids

```sh
# python todo.py list [uid ...]
python todo.py list 1
```

```sh
# output

uid | title | status
-------------------
1 | Hello, World | ❌
```

### Update

```sh
# python todo.py update uid [title ...]
python todo.py update 1 Hello, World updated
```

### Check

- Check by ids

```sh
# python todo.py check [uid ...]
python todo.py check 1
```

- Check all

```sh
python todo.py check -a
```

### Uncheck

- Uncheck by ids

```sh
# python todo.py uncheck [uid ...]
python todo.py uncheck 1
```

- Uncheck all

```sh
python todo.py uncheck -a
```

### Delete

- Delete by ids

```sh
# python todo.py delete [uid ...]
python todo.py delete 1
```

- Delete all

```sh
python todo.py delete -a
```

### Help

```sh
python todo.py -h
```

Help for specific command

```sh
python todo.py <command> -h
```

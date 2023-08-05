# readtail

### Simple Description

- A simplest generator function written in pure python
- Seek from the tail of the file

### Install
```shell
pip install tailread
```


### Useage

```python
from tailread import readlines

# The file must be opened in bytes mode.
for line in readlines(open('access.log', 'rb')):
    print(line)
    # Can stop reading
    if 'some string' in line:
        break
        

# or from file path
for line in readlines('access.log'):
    print(line)

# b'line 10\r\n'
# b'line 9\r\n'
# b'line 8\r\n'
# b'line 7\r\n'
# ....

```

```python
# decoding lines from encoding info
for line in readlines('access.log', encoding='utf-8', errors='ignore'):
    print(line)

# line 10

# line 9

# line 8

# line 7

# ....


```
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
import tailread as tail

# consuming tails one by one
  lines = tail.readlines('access.log')

  # take tail of one line
  line = next(lines)
  print(line)
# b'line 10/r/n'

  # next...
  line = next(lines)
  print(line)
# b'line 9/r/n'


# When passing a fileobject, The file must be opened in bytes mode.
with open('access.log', 'rb'): as fp:
    for line in tail.readlines(fp):
        print(line)
        if 'some string' in line:
            break
        

# or from file path
for line in tail.readlines('access.log'):
    print(line)
      if 'some string' in line:
          break

# b'line 10\r\n'
# b'line 9\r\n'
# b'line 8\r\n'
# b'line 7\r\n'
# ....

```

```python
# decoding lines from encoding info
for line in tail.readlines('access.log', encoding='utf-8', errors='ignore'):
    print(line)

# line 10

# line 9

# line 8

# line 7

# ....


```
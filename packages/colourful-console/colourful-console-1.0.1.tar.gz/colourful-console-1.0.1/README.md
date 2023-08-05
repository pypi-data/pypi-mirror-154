# Colourful Console

---

## Introduction

A simple python package to print colors in terminal using simple markup syntax

#

## Installation

`pip install colourful-console`

#

## Basic Usage

```python
import colourful_console as console

console.init()

text = 'What is your <b>name</b> :'
name = console.read_line(text)

console.clear()

console.write_line(f'Your name is <g>{name}</g>')

console.title('Press enter to exit..')
input()

```

### More on titles

```python
import colourful_console as console

# to set a simple title
console.title('This is a simple title')

# to set a title with multiple dynamic data
console.set_title(
    lang='python', 
    version=3, 
    foo='bar'
)

# Please note, when the python program exits 
# then the custom title will also vanish and
# be replaced with the previous title
# that was before running the python program
```
#

## Todo

- [ ] Add more colors
- [ ] Add uniqe textstyling like underline, bold, strikethrough
- [ ] Add custom styles for specifi platform and command line apps

#

## Note
The terminal in unix and max are much more capable and better to show colors than window's cmd and powershell.

Microsoft released a new terminal which is as capable to show colors like unix/mac terminals named **terminal** on [Microsoft store](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701?hl=en-np), you can use that terminal to show fancy styles in window platform
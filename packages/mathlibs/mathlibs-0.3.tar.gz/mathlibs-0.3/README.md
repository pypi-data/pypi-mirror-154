<img src="https://warehouse-camo.ingress.cmh1.psfhosted.org/508b21fb70f4bc69e3d62730b3ac3c307a209bca/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f72657175657374732e737667">
## Start

> `mathlibs` - Mathematical library, created for theorems
### Installation
The easiest way to install Mathlibs is pip

    pip install mathlibs

And it remains only to wait until the installation is finished. Version 0.3

## Usage
***
#### Initialization
> `Mathlibs.init(Language)`

INITIALIZATION IS REQUIRED! OTHERWISE, SOME FUNCTIONS MAY NOT WORK!
Language can take two values: ru and en. Ru – Russian, en – English
Example:
>`import mathlibs`
`Mathlibs.init(ru)`
Output: 

***
#### Pythagoras
> Mathlibs.Pyth(cathetusX, cathetusY, Hypotenuse)

cathetusX, cathetusY, Hypotenuse – provide numbers, if one number is 0, then this number is unknown to us.
The formula of the Pythagorean theorem: c² = a² + b²

Example:
> `import mathlibs`
`a = Mathlibs.Pyth(3, 3, 0)`
`print(a)`
Output: 18

***
#### Euler

> Mathlibs.euler(e)

For the Euler formula, initialization is required, otherwise it will not work
e – provides a number

Example:
> `import mathlibs`
`a = Mathlibs.euler(30)`
`print(a)`
Output: 8
***
#### Discriminant
> Mathlibs.Discr(a,b,c)

Initialization is required for the discriminant, otherwise it will not work
a, b, c – provide numbers
Discriminant formula: ax² + bx + c = 0

Example:
> `import mathlibs`
`a = Mathlibs.Discr(2,4,2)`
`print(a)`
Output: -1.00


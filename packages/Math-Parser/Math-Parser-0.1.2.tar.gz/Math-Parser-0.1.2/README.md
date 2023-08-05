
Math Parser 
===========

Math-Parser is a Python package to evaluate math expressions in strings using a LL-Compiler Algorithm with no 
dependencies, except the standard packages. 

It's not recommended to use eval to evaluate strings in Python for security reasons. This packages has the intention to 
solve this problem with safety. 


Install
-------

Install the latest version directly from the source using Git:

    git clone
    cd Math-Parser
    python setup.py install

Usage
-----

To use this package, import the evaluate function and call it.

    from math_parser import evaluate

    expr = '2 * (10/2) + 5'
    evaluate(expr)

    >>> 15.0

The evaluate function can receive variables to use it on the expression.

    expr = 'a0 + a1/10'
    evaluate(expr, a0=2, a1=10)

    >>> 3.0

In this version of the package it only accepts some operators:

- Addition (+);
- Subtraction (-);
- Multiplication (*);
- Division (/)
- Exponentiation (^)

For now, it doesn't work with negative exponentiation.


Contact
-------

If you want to contact me, email me: victor.soeiro.araujo@gmail.com

Acknowledgements
----------------

This code was based on [Georg Nebehay](https://github.com/gnebehay) algorithm. Please check his code and documentation
for better understanding of this package, and give him a star.


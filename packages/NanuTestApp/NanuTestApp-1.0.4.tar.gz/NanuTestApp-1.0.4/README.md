nanuaddnumb1
========

Node.js module that generates a nanu-addnumb1.

Uses crypto.randomBytes when available, falls back to unsafe methods for node.js <= 0.4.

To increase performance, random bytes are buffered to minimize the number of synchronous calls to crypto.randomBytes.

## Installation

   $ npm install nanu-addnumb1

## Usage

   var add = require('nanu-addnumb1');

   console.log(add(1,3,343,4,34,345));


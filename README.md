# Kerberos Python Library

This is a Python library for implementing Kerberos Protocol.  
This does not actually implement the Kerberos Protocol at low-level api, but provides helper classes that can be used to implement Kerberos over some other protocol such as HTTP.

For More information on Kerberos Protocol, see <a href='https://github.com/YJDoc2/Kerberos-Python-Library/blob/master/Kerberos.md'>Kerberos md</a> file.

For API documentation see <a href = 'https://github.com/YJDoc2/Kerberos-Python-Library/blob/master/API.md'>API md</a> file.

There is a corresponding JS Module of this project : <a href='https://github.com/YJDoc2/Kerberos-JS-Module'>Kerberos JS Module</a>

Also For example usage of this , check out <a href='https://github.com/YJDoc2/Kerberos-Examples'>Kerberos Examples</a> Repository. It contains commented examples of how to use this and python library.

<strong>NOTE</strong> Before any usage of this, one should test the security aspects of this thoroughly.

## About

This library provides classes for setting up Kerberos methods over a protocol.

This contains has three main parts :

<ul>
<li>KDC classes</li>
<li>Server class</li>
<li>Client class</li>
</ul>

Key Distribution Centre (KDC) classes, which are used in generating initial authentication and Ticket Granting Ticket (TGT), and then tickets for individual servers, which are to be protected by this protocol.
The main classes are Kerberos_AS and Kerberos_TGS, and Kerberos_KDC provides an easier-to-use interface over them for the cases when Authentication Service and Ticket Granting Service is to be set up in same server program.
<strong>NOTE</strong> that Kerberos_KDC class does not provide any extra functionality, and its work can be done by using individual instances of Kerberos_AS and Kerberos_TGS. The Kerberos_KDC class is implemented so that one need not maintain instances of two classes.

The Server class provides methods which are used on a server that is to be protected by Kerberos.  
<strong>NOTE</strong> that this does not actually set up any server, just contain methods related to kerberos protocol that are used on Server.

The Client class provides methods which are used by a client which is used to access data on servers protected by Kerberos.
<strong>NOTE</strong> that this does not actually set up any client, just contain methods related to kerberos protocol that are used by client.

This library provides default classes for basic database and cryptographic requirements,but custom classes can be used as well by making them extend appropriate classes. See API documentation for more information.

## Dependencies

This Module uses pycryptodome module for the AES 256 CTR mode encryption used by default.

Other than that this uses pytest as testing framework.

## Basic Usage Information

<strong>Note</strong> that this was developed with idea that made the three components mentioned in about section function independently. Which means it is not compulsory to use KDC,Server and Client of Python library only.The components of this Python library can be used along with those in JS Module. The examples repository shows the use in this manner only.

The API has been decently commented, though not as best it could have been.
The detailed API documentation for usage can be found in API md file.

The outermost \_\_init\_\_.py file exports all the components.

All classes and constants exported by the module can be brought in by using :<br />
<code>from 'path/to/Kerberos-py-library' import ComponentClass</code>

<strong>Note</strong> that some methods of API have a large number of params, upto 6, clearly breaking the max-number-of-params-should-be-3 guideline of good programming.For slightly easier use of these, **all params** of **all** methods follow the following order :  
random number ; request server ; UIDs for user : key ; encryption/decryption data ; tickets ; optional params.
whichever are present.

## Working/Security

This uses the AES 256 bit CTR mode by default for all encryptions and decryptions.
For security considerations check <a href='https://github.com/YJDoc2/Kerberos-Python-Library/blob/master/security.md'>security md</a>.
<strong>Note that developer neither gives any guarantee nor takes any responsibility for the security of this library.</strong>

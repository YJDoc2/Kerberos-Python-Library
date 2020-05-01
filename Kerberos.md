# Kerberos Protocol

<p> Kerberos Protocol is a computer network authentication protocol,which was developed by and is maintained by MIT.</p>

<h4>For a better explanation of this, please check <a href = "https://www.youtube.com/watch?v=qW361k3-BtU">Taming Kerberos video </a> on Youtube Channel Computerphile, from which I got the most information I used in this project.</h4>

<h4>Note : Following information is my understanding of the working of kerberos protocol, which may be incorrect.</h4>

<p>Kerberos protocol eliminates the need of using public keys which need to be sent over a non-secure network.For this it uses a secrete key which is generated from user-secrets such as password.<p>

<p>Kerberos consists of three parts of network : an Authentication Service, a Ticket Granting Service, and actual protected Servers</p>

<p>The user must create account from a route which is guaranteed to be protected, such as from an admin-access-only computer. From here the user will set the password,only known to that person.</p>

<p>Whenever the user wants to access any computer that is secured by the protocol, user must first send its identification credentials like username (Not password) to the Authenticating Service, where the service will check the existence of user in a database, and will fetch the value in corresponding password field.
This value will then be used as a key to encrypt the response that will be sent to the user from authentication service.The response of authentication service will contain a Ticket Granting Ticket, which must be sent along with all requests to Ticket Granting Service (TGS), to obtain tickets, known as Ticket Granting Ticket (TGT).This response will also contain a unique key that must be used to encrypt the requests to TGS.The TGT sent will be encrypted with a key that is known only to the Authentication Server and TGS, and cannot be decrypted by user.</p>

<p>For Accessing any server secured with Kerberos, a Ticket must be taken from TGS, which must be sent along with every request to the Server.To obtain this ticket, user must make a request to TGS, encrypted with the key obtained in the response from Authentication Server, and send the TGT obtained along with it.</p>

<p>When the TGS obtains the request and the TGT, it first decrypts the ticket which is encrypted with the key unique to the TGS.This TGT contains the key that was sent to the user by Authentication Server, and which must be used to encrypt the request to TGS.TGS then can decrypt the request, and find for which server the user is asking the ticket for.</p>

<p> After decrypting the Request, TGS finds the server data from its database, which contains an key unique to each server. TGS then generates a random key, places it in a ticket structure along with timestamp, lifetime of ticket etc. and encrypts the ticket with the key unique to the server. Then TGS sends the generated key along with this ticked and other details to the user encrypted with the same key that was in TGT.</p>

<p>When User receives this response it can decrypt it to get the randomly generated key and the ticket.Then user can make requests to the server.For this the request must be encrypted with the key received in the response from TGS and must send the Ticket obtained from TGS.</p>

<p>When the server receives the request, it decrypts the ticket that is unique to the server, and can find the key with which the request is encrypted inside it.It can also contain the timestamp and lifetime of ticket with other details, with which server can determine that if the ticket is valid or expired.If the ticket is valid the server then decrypts the request, takes the appropriate action and then encrypts the response with the same key found in the ticket.</p>

<p>User after receiving the response can decrypt with the key received in the response from TGS and find the actual response.</p>

<p>One more feature that is used to prevent replay attacks, is to put a constraint that any and every request must contain a new not-used-before random number, whose track can be kept on all servers.If someone tries to capture a request in between and tries to resend it then as it is encrypted one should not be able to change the random number inside, and if attacker resend the request, it will be denied as the random number is already used.</p>

<h4> Note that this too has its disadvantages and vulnerabilities, such as time between access granting and actual use.</h4>
<p>If a user logs in before getting removed from authorized users, then if the TGT has a longer lifetime, the user will still be able to access the servers, until the TGT expires and user is forced to again get a TGT, where, as user is removed from authorized user, the request will be denied.</p>

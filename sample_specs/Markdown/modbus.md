MODBUS MESSAGING ON TCP/IP IMPLEMENTATION GUIDE V1.0b
CONTENTS
1 INTRODUCTION ..... 2
1.1 OBJECTIVES ..... 2
1.2 CLIENT / SERVER MODEL ..... 2
1.3 REFERENCE DOCUMENTS ..... 3
2 ABBREVIATIONS ..... 3
3 CONTEXT ..... 3
3.1 PROTOCOL DESCRIPTION ..... 3
3.1.1 General communication architecture ..... 3
3.1.2 MODBUS On TCP/IP Application Data Unit ..... 4
3.1.3 MBAP Header description ..... 5
3.2 MODBUS FUNCTIONS CODES DESCRIPTION ..... 6
4 FUNCTIONAL DESCRIPTION ..... 7
4.1 MODBUS COMPONENT ARCHITECTURE MODEL ..... 7
4.2 TCP CONNECTION MANAGEMENT ..... 10
4.2.1 Connections management Module ..... 10
4.2.2 Impact of Operating Modes on the TCP Connection ..... 13
4.2.3 Access Control Module ..... 14
4.3 USE of TCP/IP STACK ..... 14
4.3.1 Use of BSD Socket interface ..... 15
4.3.2 TCP layer parameterization ..... 18
4.3.3 IP layer parameterization ..... 19
4.4 COMMUNICATION APPLICATION LAYER ..... 20
4.4.1 MODBUS Client ..... 20
4.4.2 MODBUS Server ..... 26
5 IMPLEMENTATION GUIDELINE ..... 32
5.1 OBJECT MODEL DIAGRAM ..... 32
5.1.1 TCP management package ..... 33
5.1.2 Configuration layer package ..... 35
5.1.3 Communication layer package ..... 36
5.1.4 Interface classes ..... 37
5.2 IMPLEMENTATION CLASS DIAGRAM ..... 37
5.3 SEQUENCE DIAGRAMS ..... 39
5.4 CLASSES AND METHODS DESCRIPTION ..... 42
5.4.1 MODBUS Server Class ..... 42
5.4.2 MODBUS Client Class ..... 43
5.4.3 Interface Classes ..... 44
5.4.4 Connexion Management class ..... 45

# 1 INTRODUCTION 

### 1.1 OBJECTIVES

The objective of this document is to present the MODBUS messaging service over TCP/IP, in order to provide reference information that helps software developers to implement this service. The encoding of the MODBUS function codes is not described in this document, for this information please read the MODBUS Application Protocol Specification [1].

This document gives accurate and comprehensive description of a MODBUS messaging service implementation. Its purpose is to facilitate the interoperability between the devices using the MODBUS messaging service.

This document comprises mainly three parts:

- An overview of the MODBUS over TCP/IP protocol
- A functional description of a MODBUS client, server and gateway implementation.
- An implementation guideline that proposes the object model of an MODBUS implementation example.


### 1.2 CLIENT / SERVER MODEL

The MODBUS messaging service provides a Client/Server communication between devices connected on an Ethernet TCP/IP network.
This client / server model is based on four type of messages:

- MODBUS Request,
- MODBUS Confirmation,
- MODBUS Indication,
- MODBUS Response

| MODBUS Client | Request | Indication | MODBUS Server |
| :--: | :--: | :--: | :--: |
|  | Confirmation | Response |  |
|  |  |  |  |


Figure 1 shows a communication model between a MODBUS Client and a MODBUS Server. It illustrates the flow of messages in a client-server architecture over a TCP/IP network. The diagram includes labeled arrows indicating the sequence of message types: Request, Indication, Confirmation, and Response. The MODBUS Client sends a Request to the MODBUS Server, which responds with an Indication. The server then sends a Response back to the client, which receives it as a Confirmation.

A MODBUS Request is the message sent on the network by the Client to initiate a transaction,

A MODBUS Indication is the Request message received on the Server side,
A MODBUS Response is the Response message sent by the Server,
A MODBUS Confirmation is the Response Message received on the Client side
The MODBUS messaging services (Client / Server Model) are used for real time information exchange:

- between two device applications,
- between device application and other device,
- between HMI/SCADA applications and devices,
- between a PC and a device program providing on line services.

# 1.3 REFERENCE DOCUMENTS 

This section gives a list of documents that are interesting to read before this one:
[1] MODBUS Application Protocol Specification V1.1a.
[2] RFC 1122 Requirements for Internet Hosts -- Communication Layers

## 2 ABBREVIATIONS

ADU Application Data Unit
IETF Internet Engineering Task Force
IP Internet Protocol
MAC Medium Access Control
MB MODBUS
MBAP MODBUS Application Protocol
PDU Protocol Data Unit
PLC Programmable Logic Controller
TCP Transport Control Protocol
BSD Berkeley Software Distribution
MSL Maximum Segment Lifetime

## 3 CONTEXT

### 3.1 PROTOCOL DESCRIPTION

### 3.1.1 General communication architecture

A communicating system over MODBUS TCP/IP may include different types of device:

- A MODBUS TCP/IP Client and Server devices connected to a TCP/IP network
- The Interconnection devices like bridge, router or gateway for interconnection between the TCP/IP network and a serial line sub-network which permit connections of MODBUS Serial line Client and Server end devices.

![img-0.jpeg](images/img-0.jpeg.png)

Figure 1: MODBUS TCP/IP communication architecture


Figure 1 shows a MODBUS TCP/IP communication architecture. It illustrates a network topology where MODBUS clients and servers are connected via TCP/IP and serial lines. The diagram includes labeled blocks representing MODBUS clients and servers, with connections indicating communication pathways.

The MODBUS protocol defines a simple Protocol Data Unit (PDU) independent of the underlying communication layers. The mapping of MODBUS protocol on specific buses or networks can introduce some additional fields on the Application Data Unit (ADU).
![img-1.jpeg](images/img-1.jpeg.png)

Figure 2: General MODBUS frame


Figure 2 shows a general MODBUS frame. It depicts the structure of a MODBUS Application Data Unit (ADU), highlighting components such as Additional address, Function code, Data, and Error check within the frame.

The client that initiates a MODBUS transaction builds the MODBUS Application Data Unit. The function code indicates to the server which kind of action to perform.

# 3.1.2 MODBUS On TCP/IP Application Data Unit 

This section describes the encapsulation of a MODBUS request or response when it is carried on a MODBUS TCP/IP network.
![img-2.jpeg](images/img-2.jpeg.png)

Figure 3: MODBUS request/response over TCP/IP

Figure 3 shows a MODBUS request/response over TCP/IP. It details the components of a MODBUS TCP/IP Application Data Unit (ADU), including the MBAP Header, Function code, and Data, within the Protocol Data Unit (PDU).

A dedicated header is used on TCP/IP to identify the MODBUS Application Data Unit. It is called the MBAP header (MODBUS Application Protocol header).

This header provides some differences compared to the MODBUS RTU application data unit used on serial line:

- The MODBUS 'slave address' field usually used on MODBUS Serial Line is replaced by a single byte 'Unit Identifier' within the MBAP Header. The 'Unit Identifier' is used to communicate via devices such as bridges, routers and gateways that use a single IP address to support multiple independent MODBUS end units.
- All MODBUS requests and responses are designed in such a way that the recipient can verify that a message is finished. For function codes where the MODBUS PDU has a fixed length, the function code alone is sufficient. For function codes carrying a variable amount of data in the request or response, the data field includes a byte count.
- When MODBUS is carried over TCP, additional length information is carried in the MBAP header to allow the recipient to recognize message boundaries even if the message has been split into multiple packets for transmission. The existence of explicit and implicit length rules, and use of a CRC-32 error check code (on Ethernet) results in an infinitesimal chance of undetected corruption to a request or response message.


# 3.1.3 MBAP Header description 

The MBAP Header contains the following fields:

| Fields | Length | Description - | Client | Server |
| :-- | :-- | :-- | :-- | :-- |
| Transaction <br> Identifier | 2 Bytes | Identification of a <br> MODBUS Request / <br> Response transaction. | Initialized by the <br> client | Recopied by the <br> server from the <br> received <br> request |
| Protocol Identifier | 2 Bytes | $0=$ MODBUS protocol | Initialized by the <br> client | Recopied by the <br> server from the <br> received <br> request |
| Length | 2 Bytes | Number of following <br> bytes | Initialized by the <br> client ( request) | Initialized by <br> the server ( <br> Response) |
| Unit Identifier | 1 Byte | Identification of a <br> remote slave <br> connected on a serial <br> line or on other buses. | Initialized by the <br> client | Recopied by the <br> server from the <br> received <br> request |

The header is 7 bytes long:

- Transaction Identifier - It is used for transaction pairing, the MODBUS server copies in the response the transaction identifier of the request.
- Protocol Identifier - It is used for intra-system multiplexing. The MODBUS protocol is identified by the value 0 .
- Length - The length field is a byte count of the following fields, including the Unit Identifier and data fields.

- Unit Identifier - This field is used for intra-system routing purpose. It is typically used to communicate to a MODBUS+ or a MODBUS serial line slave through agateway between an Ethernet TCP-IP network and a MODBUS serial line. This field is set by the MODBUS Client in the request and must be returned with the same value in the response by the server.

All MODBUS/TCP ADU are sent via TCP to registered port 502.
Remark : the different fields are encoded in Big-endian.

# 3.2 MODBUS FUNCTIONS CODES DESCRIPTION 

Standard function codes used on MODBUS application layer protocol are described in details in the MODBUS Application Protocol Specification [1].

# 4 FUNCTIONAL DESCRIPTION 

The MODBUS Component Architecture presented here is a general model including both MODBUS Client and Server Components and usable on any device.

Some devices may only provide the server or the client component.
In the first part of this section a brief overview of the MODBUS messaging service component architecture is given, followed by a description of each component presented in the architectural model.

### 4.1 MODBUS COMPONENT ARCHITECTURE MODEL

![img-3.jpeg](images/img-3.jpeg.png)

Figure 4: MODBUS Messaging Service Conceptual Architecture

## - Communication Application Layer


Figure 4 shows the MODBUS Component Architecture Model, which includes several layers and interfaces. At the top, the 'User Application' interacts with the 'Communication Application Layer', which contains the Modbus Client and Modbus Server. These components interface with the 'Modbus Client Interface' and 'Modbus Backend Interface', respectively. Below this, the 'TCP Management' layer handles 'Connection Management', 'Access Control', and 'Stack Parameterization'. At the base of the architecture is the 'TCP/IP Stack'. The entire model is framed by 'Resource Management & Flow Control' on the left side.

A MODBUS device may provide a client and/or a server MODBUS interface.
A MODBUS backend interface can be provided allowing indirectly the access to user application objects.
Four areas can compose this interface: input discrete, output discrete (coils), input registers and output registers. A pre-mapping between this interface and the user application data has to be done (local issue).

| Primary tables | Object type | Type of | Comments |
| :-- | :-- | :-- | :-- |
| Discretes Input | Single bit | Read-Only | This type of data can be provided by an I/O system. |
| Coils | Single bit | Read-Write | This type of data can be alterable by an application <br> program. |
| Input Registers | 16-bit word | Read-Only | This type of data can be provided by an I/O system |
| Holding Registers | 16-bit word | Read-Write | This type of data can be alterable by an application <br> program. |

![img-4.jpeg](images/img-4.jpeg.png)

Figure 5 MODBUS Data Model with separate blocks
![img-5.jpeg](images/img-5.jpeg.png)

Figure 6 MODBUS Data Model with only 1 block

# $>$ MODBUS Client 


Figure 5 shows the MODBUS Data Model with separate blocks. It illustrates a MODBUS server device with labeled sections for Input Discrete, Coils, Input Registers, and Output Registers. Arrows indicate the MODBUS access paths to each section, and a MODBUS Request is shown pointing towards the blocks.


Figure 6 shows the MODBUS Data Model with only 1 block. It displays a MODBUS server device where all sections (Input Discrete, Coils, Input Registers, Output Registers) are combined into a single block. The diagram includes arrows labeled 'R' and 'W' indicating read and write operations, and a MODBUS Request pointing towards the block.

The MODBUS Client allows the user application to explicitly control information exchange with a remote device. The MODBUS Client builds a MODBUS request from parameter contained in a demand sent by the user application to the MODBUS Client Interface.
The MODBUS Client uses a MODBUS transaction whose management includes waiting for and processing of a MODBUS confirmation.

## $>$ MODBUS Client Interface

The MODBUS Client Interface provides an interface enabling the user application to build the requests for various MODBUS services including access to MODBUS application objects. The MODBUS Client interface (API) is not part of this Specification, although an example is described in the implementation model.

## $>$ MODBUS Server

On reception of a MODBUS request this module activates a local action to read, to write or to achieve some other actions. The processing of these actions is done totally transparently for the application programmer. The main MODBUS server functions are to wait for a MODBUS request on 502 TCP port, to treat this request and then to build a MODBUS response depending on device context.

## $>$ MODBUS Backend Interface

The MODBUS Backend Interface is an interface from the MODBUS Server to the user application in which the application objects are defined.

Informative Note: The Backend Interface is not defined in this Specification October 24, 2006
http://www.Modbus.org

# - TCP Management layer 

Informative Note: The TCP/IP discussion in this Specification is based in part upon reference [2] RFC 1122 to assist the user in implementing the MODBUS Application Protocol Specification [1] over TCP/IP.

One of the main functions of the messaging service is to manage communication establishment and ending and to manage the data flow on established TCP connections.

## $>$ Connection Management

A communication between a client and server MODBUS Module requires the use of a TCP connection management module. It is in charge to manage globally messaging TCP connections.

Two possibilities are proposed for the connection management. Either the user application itself manages TCP connections or the connection management is totally done by this module and therefore it is transparent for the user application. The last solution implies less flexibility.

The listening TCP port 502 is reserved for MODBUS communications. It is mandatory to listen by default on that port. However, some markets or applications might require that another port is dedicated to MODBUS over TCP. For that reason, it is highly recommended that the clients and the servers give the possibility to the user to parameterize the MODBUS over TCP port number. It is important to note that even if another TCP server port is configured for MODBUS service in certain applications, TCP server port 502 must still be available in addition to any application specific ports.

## $>$ Access Control Module

In certain critical contexts, accessibility to internal data of devices must be forbidden for undesirable hosts. That's why a security mode is needed and security process may be implemented if required.

## - TCP/IP Stack layer

The TCP/IP stack can be parameterized in order to adapt the data flow control, the address management and the connection management to different constraints specific to a product or to a system. Generally the BSD socket interface is used to manage the TCP connections.

## -Resource management and Data flow control

In order to equilibrate inbound and outbound messaging data flow between the MODBUS client and the server, data flow control mechanism is provided in all layers of MODBUS messaging stack.
The resource management and flow control module is first based on TCP internal flow control added with some data flow control in the data link layer and also in the user application level.

# 4.2 TCP CONNECTION MANAGEMENT 

### 4.2.1 Connections management Module

### 4.2.1.1 General description

A MODBUS communication requires the establishment of a TCP connection between a Client and a Server.
The establishment of the connection can be activated either explicitly by the User Application module or automatically by the TCP connection management module.
In the first case an application-programming interface has to be provided in the user application module to manage completely the connection. This solution provides flexibility for the application programmer but it requires a good expertise on TCP/IP mechanism.
In the second case the TCP connection management is completely hidden to the user application that only sends and receives MODBUS messages. The TCP connection management module is in charge to establish a new TCP connection when it is required.
The definition of the number of TCP client and server connections is not on the scope of this document (value n in this document). Depending on the device capacities the number of TCP connections can be different.

## Implementation Rules :

1) Without explicit user requirement, it is recommended to implement the automatic TCP connection management
2) It is recommended to keep the TCP connection opened with a remote device and not to open and close it for each MODBUS/TCP transaction,
Remark: However the MODBUS client must be capable of accepting a close request from the server and closing the connection. The connection can be reopened when required.
3) It is recommended for a MODBUS Client to open a minimum of TCP connections with a remote MODBUS server (with the same IP address). One connection per application could be a good choice.
4) Several MODBUS transactions can be activated simultaneously on the same TCP Connection.
Remark: If this is done then the MODBUS transaction identifier must be used to uniquely identify the matching requests and responses.
5) In case of a bi-directional communication between two remote MODBUS entities ( each of them is client and server), it is necessary to open separate connections for the client data flow and for the server data flow.
6) A TCP frame must transport only one MODBUS ADU. It is advised against sending multiple MODBUS requests or responses on the same TCP PDU

![img-6.jpeg](images/img-6.jpeg.png)

Figure 7: TCP connection management activity diagram

# 1. Explicit TCP connection management 


Figure 7 shows a TCP connection management activity diagram. It illustrates the process flow for managing TCP connections between a client and a server in a Modbus communication setup. The diagram is divided into two main sections: Client and Server. Each section details the states and transitions involved in establishing, maintaining, and closing connections. Key states such as 'Idle', 'Wait', 'Active_Connection', and 'Connection_established' are represented with labeled blocks. Arrows indicate data flow and decision points, such as 'Connection OK' and 'Connection NOK', determining the transition to subsequent states.

The user application module is in charge of managing all the TCP connections: active and passive establishment, connection ending, etc. This management is done for all MODBUS communication between a client and a server. The BSD Socket interface is used in the user application module to manage the TCP connection. This solution offers a total flexibility but it implies that the application programmer has sufficient TCP knowledge.
A limit of number of client and server connections has to be configured taking into account the device capabilities and requirement.

## 2. Automatic TCP connection management

The TCP connection management is totally transparent for the user application module. The connection management module may accept a sufficient number of client and server connections.
Nevertheless a mechanism must be implemented in case of exceeding the number of authorized connection. In such a case we recommend to close the oldest unused connection.
A connection with a remote partner is established at the first packet received from a remote client or from the local user application. This connection will be closed if a termination arrived from the network or decided locally on the device. On reception of a connection request, the access control option can be used to forbid device accessibility to unauthorized clients.
October 24, 2006
http://www.Modbus.org

The TCP connection management module uses the Stack interface (usually BSD Socket interface) to communicate with the TCP/IP stack.

In order to maintain compatibility between system requirements and server resources, the TCP management will maintain 2 pools of connection.

- The first pool ( priority connection pool) is made of connections that are never closed on a local initiative. A configuration must be provided to set this pool up. The principle to be implemented is to associate a specific IP address with each possible connection of this pool. The devices with such IP addresses are said to be "marked". Any new connection that is requested by a marked device must be accepted, and will be taken from the priority connection pool. It is also necessary to configure the maximum number of Connections allowed for each remote device to avoid that the same device uses all the connections of the priority pool.
- The second pool (non-priority connection pool) contains connections for non marked devices. The rule that takes over here is to close the oldest connection when a new connection request arrives from a non-marked device and when there is no more connection available in the pool.

A configuration might be optionally provided to assign the number of connections available in each pool. However (It is not mandatory) the designers can set the number of connections at design time if required.

# 4.2.1.2 Connection management description 

## - Connection establishment :

The MODBUS messaging service must provide a listening socket on Port 502, which permits to accept new connection and to exchange data with other devices.
When the messaging service needs to exchange data with a remote server, it must open a new client connection with a remote Port 502 in order to exchange data with this distant. The local port must be higher than 1024 and different for each client connection.
![img-7.jpeg](images/img-7.jpeg.png)

Figure 8: MODBUS TCP connection establishment


Figure 8 shows the MODBUS TCP connection establishment process. It illustrates two devices, labeled Device@ IP1 and Device@ IP2, each with client ports numbered greater than 1024 and a server port at 502. A connection is established from a client port on Device@ IP1 to the server port on Device@ IP2, demonstrating the communication link between the devices.

If the number of client and server connections is greater than the number of authorized connections the oldest unused connection is closed. The access control mechanism can be activated to check if the IP address of the remote client is authorized. If not the new connection is refused.

# - MODBUS data transfer 

A MODBUS request has to be sent on the right TCP connection already opened. The IP address of the remote is used to find the TCP connection. In case of multiple TCP connections opened with the same remote, one connection has to be chosen to send the MODBUS message, different choice criteria can be used like the oldest one, the first one. The connection has to maintain open during all the MODBUS communications. As described in the following sections a client can initiate several MODBUS transactions with a server without waiting the ending of the previous one.

## - Connection closing

When the MODBUS communications are ended between a Client and a Server, the client has to initiate a connection closing of the connection used for these communications.

### 4.2.2 Impact of Operating Modes on the TCP Connection

Some Operating Modes (communication break between two operational End Points, Crash and Reboot on one of the End Point, ...) may have impacts on the TCP Connections. A connection can be seen closed or aborted on one side without the knowledge of the other side. The connection is said to be "half-open".
This section describes the behavior for each main Operating Modes. It is assumed that the Keep Alive TCP mechanism is used on both end points (See section 4.3.2)

### 4.2.2.1 Communication break between two operational end points:

The origin of the communication break can be the disconnection of the Ethernet cable on the Server side. The expected behavior is:

- If no packet is currently sent on the connection:

The communication break will not be seen if it lasts less than the Keep Alive timer value. If the communication break lasts more than the Keep Alive timer value, an error is returned to the TCP Management layer that can reset the connection.

- If Some packets are sent before and after the disconnection:

The TCP retransmission algorithms (Jacobson's, Karn's algorithms and exponential backoff. See section 4.3.2) are activated. This may lead to a stack TCP layer Reset of the Connection before the Keep Alive timer is over.

### 4.2.2.2 Crash and Reboot of the Server end point

After the crash and Reboot of the Server, the connection is "half-open" on Client side. The expected behavior is:

- If no packet is sent on the half-open connection:

The TCP half-open connection is seen opened from the Client side as long as the Keep Alive timer is not over. After that an error is returned to the TCP Management layer that can reset the connection.

- If some packets are sent on the half-open connection:

The Server receives data on a connection that doesn't exist anymore. The stack TCP layer sends a Reset to close the half-open connection on the Client side

### 4.2.2.3 Crash and Reboot of the Client

After the crash and Reboot of the Client, the connection is "half-open" on Server side. The expected behavior is:

- No packet is sent on the half-open connection:

The TCP half-open connection is seen opened from the Server side as long as the Keep Alive timer is not over. After that an error is returned to the TCP Management layer that can reset the connection.

- If the Client opens a new connection before the Keep Alive timer is over :

Two cases have to be studied:

- The connection opening has the same characteristics as the half-open connection on the server side (same source and destination Ports, same source and destination IP Addresses), therefore the connection opening will fail at the TCP stack level after the Time-Out on Connection Establishment (75s on most of Berkeley implementations). To avoid this long Time-Out during which it is not possible to communicate, it is advised to ensure that different source port numbers than the previous one are used for a connection opening after a reboot on the client side.
- The connection opening has not the same characteristics as the half-open connection on the server side (different source Ports, same destination Port, same source and destination IP Address ), therefore the connection is opened at the stack TCP level and signaled to the Server TCP Management layer.
If the Server TCP Management layer only supports one connection from a remote Client IP Address, it can close the old half-opened connection and use the new one.
If the Server TCP Management layer supports several connections from a remote Client IP Address, the new connection stays opened and the old one also stays half-opened until the expiration of the Keep Alive Timer that will return an error to the TCP Management layer. After that the TCP Management layer will be able to Reset the old connection.


# 4.2.3 Access Control Module 

The goal of this module is to check every new connection and using a list of authorized remote IP addresses the module can authorize or forbid a remote Client TCP connection.

In critical context the application programmer needs to choose the Access Control mode in order to secure its network access. In such a case he needs to Authorize/forbid access for each remote @IP. The user needs to provide a list of IP addresses and to specify for each IP address if it's authorized or not. By default, on security mode, the IP addresses not configured by the user are forbidden. Therefore with the access control mode a connection coming from an unknown IP address is closed.

### 4.3 USE of TCP/IP STACK

A TCP/IP stack provides an interface to manage connections, to send and receive data, and also to do some parameterizations in order to adapt the stack behavior to the device or system constraints.

![img-8.jpeg](images/img-8.jpeg.png)

The goal of this section is to give an overview of the Stack interface and also some information concerning the parameterization of the stack. This overview focuses on the features used by the MODBUS Messaging.


Figure 1 shows a layered stack model related to MODBUS messaging on TCP/IP. It includes layers such as ARP, ICMP, IP, TCP, Modbus, and Msg, with each layer stacked on top of the other. The base layer is labeled 'Network Access Ethernet II and 802.3 layer', indicating the foundational network protocols.

For more information, the advice is to read the RFC 1122 that provides guidance for vendors and designers of Internet communication software. It enumerates standard protocols that a host connected to the Internet must use as well as an explicit set of requirements and options.
The stack interface is generally based on the BSD (Berkeley Software Distribution) Interface that is described in this document.

# 4.3.1 Use of BSD Socket interface 

Remark : some TCP/IP stacks propose other types of interfaces for performance issues. A MODBUS client or server can use these specific interfaces, but this use will be not described in this specification.

A socket is an endpoint of communication. It is the basic building block for communication. A MODBUS communication is executed by sending and receiving data through sockets. The TCPIP library provides only stream sockets using TCP and providing a connection-based communication service.
The Sockets are created via the socket () function. A socket number is returned, which is then used by the creator to access the socket. Sockets are created without addresses (IP address and port number). Until a port is bound to a socket, it cannot be used to receive data.
The bind () function is used to bind a port number to a socket. The bind () creates an association between the socket and the port number specified.
In order to initiate a connection, the client must issue the connect () function specifying the socket number, the remote IP address and the remote listening port number (active connection establishment).
In order to complete a connection, the server must issue the accept () function specifying the socket number that was specified in the prior listen () call (passive connection establishment). A new socket is created with the same properties as the initial one. This new socket is connected to the client's socket, and its number is returned to the server. The initial socket is thereby free for other clients that might want to connect with the server.

After the establishment of the TCP connection the data can be transferred. The send() and recv() functions are designed specifically to be used with sockets that are already connected.

The setsockopt () function allows a socket's creator to associate options with a socket. These options modify the behavior of the socket. The description of these options is given in the section 4.3.2.

The select () function allows the programmer to test events on all sockets.

The shutdown () function allows a socket user to disable send () and/or receive () on the socket.

Once a socket is no longer needed, its socket descriptor can be discarded by using the close () function.

Figure 39: MODBUS Exchanges describes a full MODBUS communication between a client and a s server. The Client establishes the connection and sends 3 MODBUS requests to the server without waiting the response of the first one. After receiving all the responses the Client closes the connection properly.

![img-9.jpeg](images/img-9.jpeg.png)

Figure 9: MODBUS Exchanges

# 4.3.2 TCP layer parameterization 

Some parameters of the TCP/IP stack can be adjusted to adapt its behavior to the product or system constraints. The following parameters can be adjusted in the TCP layer:

## - Parameters for each connection:

## SO-RCVBUF, SO-SNDBUF:

These parameters allow setting the high water mark for the Send and the Receive Socket. They can be adjusted for flow control management. The size of the received buffer is the maximum size advertised window for that connection. Socket buffer sizes must be increased in order to increase performances. Nevertheless these values must be smaller than internal driver resources in order to close the TCP window before exhausting internal driver resources.

The received buffer size depends on the TCP Windows size, the TCP Maximum segment size and the time needed to absorb the incoming frames. With a Maximum Segment Size of 300 bytes (a MODBUS request needs a maximum of 256 bytes + the MBAP header size), if we need 3 frames buffering, the socket buffer size value can be adjusted to 900 bytes. For biggest needs and best-scheduled time, the size of the TCP window may be increased.

## TCP-NODELAY:

Small packets (called tinygrams) are normally not a problem on LANs, since most LANs are not congested, but these tinygrams can lead to congestion on wide area networks. A simple solution, called the "NAGLE algorithm", is to collect small amounts of data and sends them in a single segment when TCP acknowledgments of previous packets arrive.
In order to have better real-time behavior it is recommended to send small amounts of data directly without trying to gather them in a single segment. That is why it is recommended to force the TCP-NODELAY option that disables the "NAGLE algorithm" on client and server connections.

## SO-REUSEADDR:

When a MODBUS server closes a TCP connection initialized by a remote client, the local port number used for this connection cannot be reused for a new opening while that connection stays in the "Time-wait" state (during two MSL : Maximum Segment Lifetime).

It is recommended specifying the SO-REUSEADDR option for each client and server connection to bypass this restriction. This option allows the process to assign itself a port number that is part of a connection that is in the 2 MSL wait for client and listening socket.

## SO-KEEPALIVE:

By default on TCP/IP protocol no data are sent across an idle TCP connection. Therefore if no process at the ends of a TCP connection is sending data to the other, nothing is exchanged between the two TCP modules. This assumes that either the client application or the server application uses timers to detect inactivity in order to close a connection.
It is recommended to enable the KEEPALIVE option on both client and server connection in order to poll the other end to know if the distant has either crashed and is down or crashed and rebooted.
Nevertheless we must keep on mind that enabling KEEPALIVE can cause perfectly good connections to be dropped during transient failures, that it consumes unnecessary bandwidth on the network if the keep alive timer is too short.

# - Parameters for the whole TCP layer: 

## Time Out on establishing a TCP Connection:

Most Berkeley-derived systems set a time limit of 75 seconds on the establishment of a new connection, this default value should be adapted to the real time constraint of the application.

## Keep Alive parameters:

The default idle time for a connection is 2 hours. Idles times in excess of this value trigger a keep alive probe. After the first keep alive probe, a probe is sent every 75 seconds for a maximum number of times unless a probe response is received.
The maximum number of keep Alive probes sent out on an idle connection is 8 . If no probe response is received after sending out the maximum number of keep Alive probes, TCP signals an error to the application that can decide to close the connection

## Time-out and retransmission parameters:

A TCP packet is retransmitted if its loss has been detected. One way to detect the loss is to manage a Retransmission Time-Out (RTO) that expires if no acknowledgement has been received from the remote side.
TCP manages a dynamic estimation of the RTO. For that purpose a Round-Trip Time (RTT) is measured after the send of every packet that is not a retransmission. The Round-Trip Time (RTT) is the time taken for a packet to reach the remote device and to get back an acknowledgement to the sending device. The RTT of a connection is calculated dynamically, nevertheless if TCP cannot get an estimate within 3 seconds, the default value of the RTT is set to 3 seconds.
If the RTO has been estimated, it applies to the next packet sending. If the acknowledgement of the next packet is not received before the estimated RTO expiration, the Exponential BackOff is activated. A maximum number of retransmissions of the same packet is allowed during a certain amount of time. After that if no acknowledgement has been received, the connection is aborted.
The maximum number of retransmissions and the maximum amount of time before the abort of the connection (tcp_ip_abort_interval) can be set up on some stacks.

Some retransmission algorithms are defined in TCP standards :

- The Jacobson's RTO estimation algorithm is used to estimate the Retransmission Time-Out (RTO),
- The Karn's algorithm says that the RTO estimation should not be done on a retransmitted segment,
- The Exponential BackOff defines that the retransmission time-out is doubled for each retransmission with an upper limit of 64 seconds.
- The fast retransmission algorithm allows retransmitting after the reception of three duplicate acknowledgments. This algorithm is advised because on a LAN it may lead to a quicker detection of the loss of a packet than waiting for the RTO expiration.

The use of these algorithms is recommended for a MODBUS implementation.

### 4.3.3 IP layer parameterization

### 4.3.3.1 IP Parameters

The following parameters must be configured in the IP layer of a MODBUS implementation :

- Local IP Address : the IP address can be part of a Class A, B or C.
- Subnet Mask. : Subnetting an IP Network can be done for a variety of reasons : use of different physical media (such as Ethernet, WAN, etc.), more efficient use of

network addresses, and the capability to control network traffic. The Subnet Mask has to be consistent with the IP address class of the local IP address.

- Default Gateway: The IP address of the default gateway has to be on the same subnet as the local IP address. The value 0.0 .0 .0 is forbidden. If no gateway is to be defined then this value is to be set to either 127.0.0.1 or the Local IP address.

Remark : The MODBUS messaging service doesn't require the fragmentation function in the IP layer.

The local IP End Point shall be configured with a local IP Address and with a Subnet Mask and a Default Gateway (different from 0.0.0.0).

# 4.4 COMMUNICATION APPLICATION LAYER 

### 4.4.1 MODBUS Client

![img-10.jpeg](images/img-10.jpeg.png)

Figure 10: MODBUS Client unit

### 4.4.1.1 MODBUS client design


Figure 10 shows a MODBUS Client unit, illustrating the communication setup between Modbus Clients and Servers over TCP/IP and Serial Line connections. The diagram includes labeled blocks representing 'Modbus Client TCP/IP', 'Modbus Server TCP/IP', 'Modbus Client Serial Line', and 'Modbus Server Serial Line'. Arrows and lines indicate the flow of data between these components, with gateways facilitating communication between different protocol types.

The definition of the MODBUS/TCP protocol allows a simple design of a client. The following activity diagram describes the main treatments that are processed by a client to send a MODBUS request and to treat a MODBUS response.

![img-11.jpeg](images/img-11.jpeg.png)

Figure 11: MODBUS Client Activity Diagram


Figure 11 shows a MODBUS Client Activity Diagram. It illustrates the flow of activities within a MODBUS client, starting from an 'Idle' state to a 'Wait' state. The diagram includes processes such as 'Process MODBUS Confirmation', 'Find out pending transaction', and 'Build MODBUS request'. It also shows decision points like 'Confirmation error' and 'Retries number reached', with arrows indicating the flow of actions based on different conditions. The diagram uses labeled blocks and arrows to represent the sequence of operations and decisions within the client activity.

A MODBUS client can receive three events:

- A new demand from the user application to send a request, in this case a MODBUS request has to be encoded and be sent on the network using the TCP management component service. The lower layer ( TCP management module) can give back an error due to a TCP connection error, or some other errors.
- A response from the TCP management, in this case the client has to analyze the content of the response and send a confirmation to the user application
- The expiration of a Time out due to a non-response. A new retry can be sent on the network or a negative confirmation can be sent to the User Application. Remark : These retries are initiated by the MODBUS client, some other retries can also be done by the TCP layer in case of TCP acknowledge lack.


# 4.4.1.2 Build a MODBUS Request 

Following the reception of a demand from the user application, the client has to build a MODBUS request and to send it to the TCP management.
Building the MODBUS request can be split in several sub-tasks:

- The instantiation of a MODBUS transaction that enables the Client to memorize all required information in order to bind later the response to the request and to send the confirmation to the user application.
- The encoding of the MODBUS request (PDU + MPAB header). The user application that initiates the demand has to provide all required information which enables the Client to encode the request. The MODBUS PDU is encoded according to the MODBUS Application Protocol Specification [1]. (MB function code, associated parameters and application data ). All fields of the MBAP header are filled. Then, the MODBUS request ADU is built prefixing the PDU with the MBAP header

- The sending of the MODBUS request ADU to the TCP management module which is in charge of finding the right TCP socket towards the remote Server. In addition to the MODBUS ADU the Destination IP address must also be passed.

The following activity diagram describes, more deeply than in Figure 11 MODBUS Client Activity Diagram, the request building phase.
![img-12.jpeg](images/img-12.jpeg.png)

Figure 12: Request building activity diagram

The following example describes the MODBUS request ADU encoding for reading the register \# 5 in a remote server :

- MODBUS Request ADU encoding :

|  | Description | Size | Example |
| :-- | :-- | :--: | :--: |
| MBAP Header | Transaction Identifier Hi | 1 | $0 \times 15$ |
|  | Transaction Identifier Lo | 1 | $0 \times 01$ |
|  | Protocol Identifier | 2 | $0 \times 0000$ |
|  | Length | 2 | $0 \times 0006$ |
|  | Unit Identifier | 1 | $0 \times F F$ |

| MODBUS <br> request | Function Code ( $*$ ) | 1 | $0 \times 03$ |
| :-- | :-- | :--: | :--: |
|  | Starting Address | 2 | $0 \times 0004$ |
|  | Quantity of Registers | 2 | $0 \times 0001$ |

(*) please see the MODBUS Application Protocol Specification [1].

# - Transaction Identifier 

The transaction identifier is used to associate the future response with the request. So, at a time, on a TCP connection, this identifier must be unique. There are several manners to use the transaction identifier:

- For example, it can be used as a simple "TCP sequence number" with a counter which is incremented at each request.
- It can also be judiciously used as a smart index or pointer to identify a transaction context in order to memorize the current remote server and the pending MODBUS request.

Normally, on MODBUS serial line a client must send one request at a time. This means that the client must wait for the answer to the first request before sending a second request. On TCP/MODBUS, several requests can be sent without waiting for a confirmation to the same server. The MODBUS/TCP to MODBUS serial line gateway is in charge of ensuring compatibility between these two behaviors.
The number of requests accepted by a server depends on its capacity in term of number of resources and size of the TCP windows. In the same way the number of transactions initialized simultaneously by a client depends also on its resource capacity. This implementation parameter is called "NumberMaxOfClientTransaction" and must be described as one of the MODBUS client features. Depending of the device type this parameter can take a value from 1 to 16 .

## - Unit Identifier

This field is used for routing purpose when addressing a device on a MODBUS+ or MODBUS serial line sub-network. In that case, the "Unit Identifier" carries the MODBUS slave address of the remote device:

If the MODBUS server is connected to a MODBUS+ or MODBUS Serial Line sub-network and addressed through a bridge or a gateway, the MODBUS Unit identifier is necessary to identify the slave device connected on the subnetwork behind the bridge or the gateway. The destination IP address identifies the bridge itself and the bridge uses the MODBUS Unit identifier to forward the request to the right slave device.
The MODBUS slave device addresses on serial line are assigned from 1 to 247 (decimal). Address 0 is used as broadcast address.
On TCP/IP, the MODBUS server is addressed using its IP address; therefore, the MODBUS Unit Identifier is useless. The value 0xFF has to be used.

When addressing a MODBUS server connected directly to a TCP/IP network, it's recommended not using a significant MODBUS slave address in the "Unit Identifier" field. In the event of a re-allocation of the IP addresses within an automated system and if a IP address previously assigned to a MODBUS server is then assigned to a gateway, using a significant slave address may cause trouble because of a bad routing by the gateway. Using a nonsignificant slave address, the gateway will simply discard the MODBUS PDU with no trouble. 0xFF is recommended for the "Unit Identifier" as nonsignificant value.
Remark : The value 0 is also accepted to communicate directly to a MODBUS/TCP device.

# 4.4.1.3 Process MODBUS Confirmation 

When a response frame is received on a TCP connection, the Transaction Identifier carried in the MBAP header is used to associate the response with the original request previously sent on that TCP connection:

- If the Transaction Identifier doesn't refer to any MODBUS pending transaction, the response must be discarded.
- If the Transaction Identifier refers to a MODBUS pending transaction, the response must be parsed in order to send a MODBUS Confirmation to the User Application (positive or negative confirmation)

Parsing the response consists in verifying the MBAP Header and the MODBUS PDU response:

## - MBAP Header

After the verification of the Protocol Identifier that must be $0 \times 0000$, the length gives the size of the MODBUS response.
If the response comes from a MODBUS server device directly connected to the TCP/IP network, the TCP connection identification is sufficient to unambiguously identify the remote server. Therefore, the Unit Identifier carried in the MBAP header is not significant (value $0 \times F F$ ) and must be discarded.
If the remote server is connected on a Serial Line sub-network and the response comes from a bridge, a router or a gateway, then the Unit Identifier (value $!=0 \times F F$ ) identifies the remote MODBUS server which has originally sent the response.

## - MODBUS Response PDU

The function code must be verified and the MODBUS response format analyzed according to the MODBUS Application Protocol:

- if the function code is the same as the one used in the request, and if the response format is correct, then the MODBUS response is given to the user application as a Positive Confirmation.
- If the function code is a MODBUS exception code (Function code +80 H ), the MODBUS exception response is given to the user application as a Positive Confirmation.
- If the function code is different from the one used in the request (=non expected function code), or if the format of the response is incorrect, then an error is signaled to the user application using a Negative Confirmation.

Remark: A positive confirmation is a confirmation that the command was received and responded to by the server. It does not imply that the server was able to successfully act on the command (failure to successfully act on the command is indicated by the MODBUS Exception response).

The following activity diagram describes, more deeply than in Figure 11 MODBUS Client Activity Diagram, the confirmation processing phase.

![img-13.jpeg](images/img-13.jpeg.png)

Figure 13: Process MODBUS Confirmation activity diagram

# 4.4.1.4 Time-out management 


Figure 13 shows a process flow diagram for MODBUS confirmation activities. It begins with finding out a pending MB transaction, followed by decision nodes that determine the path based on the transaction status and protocol type. The diagram includes steps such as analyzing the MBAP header, analyzing the response PDU, and processing MB exceptions. It also shows actions like sending positive or negative confirmations to user applications, with various outcomes based on the response status.

There is deliberately NO specification of required response time for a transaction over MODBUS/TCP.
This is because MODBUS/TCP is expected to be used in the widest possible variety of communication situations, from I/O scanners expecting sub-millisecond timing to long distance radio links with delays of several seconds.
From a client perspective, the timeout must take into account the expected transport delays across the network, to determine a 'reasonable' response time. Such transport delays might be milliseconds for a switched Ethernet, or hundreds of milliseconds for a wide area network connection.
In turn, any 'timeout' time used at a client to initiate an application retry should be larger than the expected maximum 'reasonable' response time. If this is not followed, there is a potential for excessive congestion at the target device or on the network, which may in turn cause further errors. This is a characteristic, which should always be avoided.

So in practice, the client timeouts used in high performance applications are always likely to be somewhat dependent on network topology and expected client performance. Applications which are not time critical can often leave timeout values to the normal TCP defaults, which will report communication failure after several seconds on most platforms.

# 4.4.2 MODBUS Server 

![img-14.jpeg](images/img-14.jpeg.png)

Figure 14: MODBUS Server unit


Figure 14 shows a MODBUS Server unit configuration in a network. It illustrates the integration of Modbus TCP/IP and Modbus Serial line communication. The diagram includes labeled blocks representing Modbus Clients and Servers connected via TCP/IP and Serial Line. Arrows indicate data flow and gateway connections between different network components, such as the Server TCP/IP gateway and Client TCP/IP gateway.

The role of a MODBUS server is to provide access to application objects and services to remote MODBUS clients.

Different kind of access may be provided depending on the user application :

- simple access like get and set application objects attributes
- advanced access in order to trigger specific application services

The MODBUS server has:

- To map application objects onto readable and writable MODBUS objects, in order to get or set application objects attributes.
- To provide a way to trigger services onto application objects.

In run time the MODBUS server has to analyze a received MODBUS request, to process the required action, and to send back a MODBUS response.

Informative Note: The application objects and services of the Backend Interface obtain the requested data based upon the function code, and the User is responsible.

# 4.4.2.1 MODBUS Server Design 

The MODBUS Server design depends on both :

- the kind of access to the application objects (simple access to attributes or advanced access to services)
- the kind of interaction between the MODBUS server and the user application (synchronous or asynchronous).


Figure 15 shows a process flow diagram for the MODBUS indication activity. It illustrates the sequence of operations within a MODBUS server, starting from the 'Idle' state and transitioning to 'Wait' upon server initialization. The diagram includes decision points such as 'MODBUS_PDU_Checking' and 'MODBUS_Service_Processing', which determine the flow based on conditions like 'MODBUS transaction accepted' or 'Processing not complete'. The process can lead to building a MODBUS exception or response, with final actions involving sending a response to TCP management and releasing the MODBUS server transaction.

The following activity diagram describes the main treatments that are processed by the Server to obtain a MODBUS request from TCP Management, then to analyze the request, to process the required action, and to send back a MODBUS response.
![img-15.jpeg](images/img-15.jpeg.png)

Figure 15: Process MODBUS Indication activity diagram

As shown in the previous activity diagram:

- Some services can be immediately processed by the MODBUS Server itself, with no direct interaction with the User Application ;
- Some services may require also interacting explicitly with the User Application to be processed ;
- Some other advanced services require invoking a specific interface called MODBUS Back End service. For example, a User Application service may be triggered using a sequence of several MODBUS request/response transactions according to a User Application level protocol. The Back End service is responsible for the correct processing of all individual MODBUS transactions in order to execute the global User Application service.

A more complete description is given in the following sections.
The MODBUS server can accept to serve simultaneously several MODBUS requests. The maximum number of simultaneous MODBUS requests the server can accept is one of the main characteristics of a MODBUS server. This number depends on the server design and its processing and memory capabilities. This implementation parameter is called "NumberMaxOfSeverTransaction" and must be described as one of the MODBUS server features. It may have a value from 1 to 16 depending on the device capabilities.

The behavior and the performance of the MODBUS server are significantly affected by the "NumberMaxOfTransaction" parameter. Particularly, it's important to note that the number of concurrent MODBUS transactions managed may affect the response time of a MODBUS request by the server.

# 4.4.2.2 MODBUS PDU Checking 

The following diagram describes the MODBUS PDU Checking activity.

![img-16.jpeg](images/img-16.jpeg.png)

Figure 16: MODBUS PDU Checking activity diagram


Figure 16 shows a flowchart for the MODBUS PDU Checking activity. It illustrates the process starting with parsing the MBAP header. If an error is detected on the MBAP, the indication is discarded. If the MBAP is OK, an MB transaction is instantiated. The flow then checks for transaction availability. If no transaction is available, the transaction is refused. If a transaction is available, the MB PDU is parsed. Errors in the MB PDU lead to transaction refusal, while an OK status results in the transaction being accepted.

The MODBUS PDU Checking function consists of first parsing the MBAP Header. The Protocol Identifier field has to be checked :

- If it is different from MODBUS protocol type, the indication is simply discarded.
- If it is correct (= MODBUS protocol type; value $0 \times 00$ ), a MODBUS transaction is instantiated.

The maximum number of MODBUS transactions the server can instantiate is defined by the "NumberMaxOfTransaction" parameter ( A system or a configuration parameter).

In case of no more transactions available, the server builds a MODBUS exception response (Exception code 6 : Server Busy).

If a MODBUS transaction is available, it's initialized in order to memorize the following information:

- The TCP connection identifier used to send the indication (given by the TCP Management)
- The MODBUS Transaction ID (given in MBAP Header)
- The Unit Identifier (given in MBAP Header)

Then the MODBUS PDU is parsed. The function code is first controlled :

- in case of invalidity a MODBUS exception response is built (Exception code 1 : Invalid function).
- If the function code is accepted, the server initiates the "MODBUS Service processing" activity.

# 4.4.2.3 MODBUS service processing 

![img-17.jpeg](images/img-17.jpeg.png)

Figure 17: MODBUS service processing activity diagram

The processing of the required MODBUS service can be done in different ways depending on the device software and hardware architecture as described in the hereafter examples :

- Within a compact device or a mono-thread architecture where the MODBUS server can access directly to the user application data, the required service can be processed "locally" by the server itself without invoking the Back End service. The processing is done according to the MODBUS Application Protocol Specification [1]. In case of an error, a MODBUS exception response is built.
- Within a modular multi-processor device or a multi-thread architecture where the "communication layers" and the "user application layer" are 2 separate entities, some trivial services can be processed completely by the Communication entity while some others can require a cooperation with the User Application entity using the Back End service.

To interact with the User Application, the MODBUS Backend service must implement all appropriate mechanisms in order to handle User Application transactions and to manage correctly the User Application invocations and associated responses.

### 4.4.2.4 User Application Interface (Backend Interface)

Several strategies can be implemented in the MODBUS Backend service to achieve its job although they are not equivalent in terms of user network throughput, interface bandwidth usage, response time, or even design workload.

The MODBUS Backend service will use the appropriate interface to the user application :

- Either a physical interface based on a serial link, or a dual-port RAM scheme, or a simple I/O line, or a logical interface based on messaging services provided by an operating system.
- The interface to the User Application may be synchronous or asynchronous.

The MODBUS Backend service will also use the appropriate design pattern to get/set objects attributes or to trigger services. In some cases, a simple "gateway pattern" will be adequate. In some other cases, the designer will have to implement a "proxy pattern" with a corresponding caching strategy, from a simple exchange table history to more sophisticated replication mechanisms.

The MODBUS Backend service has the responsibility to implement the protocol transcription in order to interact with the User Application. Therefore, it can have to implement mechanisms for packet fragmentation/reconstruction, data consistency guarantee, and synchronization whatever is required.

# 4.4.2.5 MODBUS Response building 

Once the request has been processed, the MODBUS server has to build the response using the adequate MODBUS server transaction and has to send it to the TCP management component.
Depending on the result of the processing two types of response can be built :

- A positive MODBUS response :
- The response function code = The request function code
- A MODBUS Exception response :
- The objective is to provide to the client relevant information concerning the error detected during the processing :
- The response function code $=$ the request function code $+0 \times 80$;
- The exception code is provided to indicate the reason of the error.

| Exception Code | MODBUS name | Comments |
| :--: | :--: | :--: |
| 01 | Illegal Function Code | The function code is unknown by the server |
| 02 | Illegal Data Address | Dependant on the request |
| 03 | Illegal Data Value | Dependant on the request |
| 04 | Server Failure | The server failed during the execution |
| 05 | Acknowledge | The server accepted the service invocation but the service requires a relatively long time to execute. The server therefore returns only an acknowledgement of the service invocation receipt. |
| 06 | Server Busy | The server was unable to accept the MB Request PDU. The client application has the responsibility of deciding if and when to re-send the request. |
| 0 A | Gateway problem | Gateway paths not available. |
| 0B | Gateway problem | The targeted device failed to respond. The gateway generates this exception |

The MODBUS response PDU must be prefixed with the MBAP header which is built using data memorized in the transaction context.

## - Unit Identifier

The Unit Identifier is copied as it was given within the received MODBUS request and memorized in the transaction context.

# - Length 

The server calculates the size of the MODBUS PDU plus the Unit Identifier byte. This value is set in the "Length" field.

- Protocol Identifier

The Protocol Identifier field is set to $0 \times 0000$ (MODBUS protocol), as it was given within the received MODBUS request.

- Transaction Identifier

This field is set to the "Transaction Identifier" value that was associated with the original request and memorized in the transaction context.

Then the MODBUS response must be returned to the right MODBUS Client using the TCP connection memorized in the transaction context. When the response is sent, the transaction context must be free.

## 5 IMPLEMENTATION GUIDELINE


Figure 18 shows a MODBUS Messaging Service Object Model Diagram. It illustrates the interaction between different components such as User Application, InterfaceUserApplication, Communication application layer, Configuration layer, InterfaceIndicationMsg, InterfaceResponseMsg, and TCP management. The diagram uses labeled blocks and arrows to represent the flow and relationship between these components, indicating how they interact within the MODBUS messaging service.

The objective of this section is to propose an example of a messaging service implementation.
The model describes below can be used as a guideline during a client or a server implementation of a MODBUS messaging service.

Informative Note: The messaging service implementation is the responsibility of the User.

### 5.1 OBJECT MODEL DIAGRAM

![img-18.jpeg](images/img-18.jpeg.png)

Figure 18: MODBUS Messaging Service Object Model Diagram
October 24, 2006
http://www.Modbus.org

Four main packages compose the Object Model Diagram:

- The Configuration layer which configures and manages operating modes of components of other packages
- The TCP Management which interfaces the TCP/IP stack and the communication application layer managing TCP connection. It implies the management of socket interface.
- The Communication application layer which is composed by the MODBUS client on one side and the MODBUS server on the other side. This package is linked with the user application.
The User application, which corresponds to the device application, is completely dependent on the device and therefore it will be not part of this Specification.

This model is independent of implementation choices like the type of OS, the memory management, etc. In order to guarantee this independence generic Interface layers are used between the TCP management layer and the communication layer and between the communication layer and the user application layer.
Different implementations of this interface can be realized by the User: Pipe between two tasks, shared memory, serial link interface, procedural call, etc.
Some assumptions have to be taken to define the hereafter implementation model :

- Static memory management
- Synchronous treatment of the server
- One task to process the receptions on all sockets.


# 5.1.1 TCP management package

![img-19.jpeg](images/img-19.jpeg.png)

Figure 19: MODBUS TCP management package


Figure 19 shows a diagrammatic representation of the MODBUS TCP management package. It highlights various classes involved in the management of TCP connections, including 'ConnexionMgt', 'ItemConnexion', 'InterfaceConnexion', 'TCPConnexion', and 'MBAP'. The diagram uses labeled blocks to represent each class, with arrows indicating the relationships and interactions between them. Functions and attributes associated with each class are listed within the blocks, showing their roles and responsibilities in the TCP management process.

The TCP management package comprises the following classes :
CInterfaceConnexion: The role of this class consists in managing memory pool for connections.

CItemConnexion: This class contains all information needed to describe a connection.
CTCPConnexion:, This class provides methods for managing automatically a TCP connection (Interface socket is provided by CStackTCP_IP).

CConnexionMngt: This class manages all connections and send query/response to MODBUS Server/MODBUS Client through CInterfaceIndicationMsg and CInterfaceResponseMsg. This class also treats the Access control for the connection opening.

CMBAP: This class provides methods for reading/writing/analyzing the MODBUS MBAP.

CStackTCP_IP: This class Implements socket services and provides parameterization of the stack.

# 5.1.2 Configuration layer package 

![img-20.jpeg](images/img-20.jpeg.png)

Figure 20: MODBUS Configuration layer package


Figure 20 shows the MODBUS Configuration layer package. It includes several components such as the Communication application layer and TCP management from the Logical View. There is an Operating Mode section with methods like m_Configure(), m_Start(), m_Stop(), and m_Reset(). The ConfigurationObject contains various attributes including GlobalState, MyModbusAddress, MyIPAddress, and others, indicating different parameters for configuration.

The Configuration layer package comprises the following classes :
TConfigureObject: This class groups all data needed for configuring each other component. This structure is filled by the method m_Configure from the class CoperatingMode. Each class needing to be configured gets its own configuration data from this object. The configuration data is implementation dependent therefore the list of attributes of this class is provided as an example.

COperatingMode: The role of this class is to fill the TConfigureObject (according to the user configuration) and to manage the operating modes of the classes described below:

- CMODBUSServer
- CMODBUSClient

# - CconnexionMngt 

### 5.1.3 Communication layer package

![img-21.jpeg](images/img-21.jpeg.png)

Figure 21: MODBUS Communication Application layer package


Figure 21 shows the MODBUS Communication Application layer package. It includes several components such as InterfaceUserApplication, ModbusPDU, ModbusServer, ModbusClient, InterfaceIndicationMsg, and InterfaceResponseMsg. The diagram illustrates the relationships and interactions between these components, with arrows indicating data flow and method calls. Each component is represented as a labeled block, detailing specific methods or functions relevant to the communication process.

The Communication Application layer package comprises the following classes :
CMODBUSServer: MODBUS query is received from class CInterfaceIndicationMsg (by the method m_ServerReceivingMessage). The role of this class is to build the MODBUS response or the MODBUS Exception according the query (incoming from network). This class implements the Graph State of MODBUS server. Response can be built only if class COperatingMode has sent both user configuration and right operating modes.

CMODBUSClient: MODBUS query is read from class CInterfaceUserApplication, The client task receives query by the method m_ClientReceivingMessage. This class

implements the State Graph of MODBUS client and manages transactions for linking query with response (from network). Query can be sent over network only if class CoperatingMode has sent both user configuration and right operating modes.

CTransaction: This class implements methods and structures for managing transactions.

# 5.1.4 Interface classes 

CInterfaceUserApplication: This class represents the interface with the user application, it provides two methods to access to the user data. In a real implementation this method can be implemented in different way depending of the hardware and software device capabilities (equivalent to an end-driver, example access to PCMCIA, shared memory, etc).

CInterfaceIndicationMsg: This Interface class is proposed for sending query from Network to the MODBUS Server, and for sending response from Network for the Client. This class interfaces TCPManagement and 'Communication Application Layer' packages (From Network). The implementation of this class is device dependent.

CInterfaceResponseMsg: This Interface class is used for receiving response from the Server and for sending query from the client to the Network. This class interfaces packages 'Communication Application Layer' and package 'TCPManagement' (To Network). The implementation of this class is device dependent.

### 5.2 IMPLEMENTATION CLASS DIAGRAM

The following Class Diagram describes the complete diagram of a proposal implementation.

![img-22.jpeg](images/img-22.jpeg.png)

Figure 22: Class Diagram

# 5.3 SEQUENCE DIAGRAMS 


Figure 23 shows a MODBUS client sequence diagram. It illustrates the sequence of interactions between various components in a MODBUS client system. The diagram includes labeled blocks representing different components such as theModbusClient and theTcpConnection, with arrows indicating the flow of messages and actions like m_GetMemoryConnection, m_ModbusRequest, and m_WriteData. The sequence diagram visually represents the communication and data exchange processes in a structured layout.

Two Sequence diagrams are described hereafter are an example in order to illustrate a Client MODBUS transaction and a Server MODBUS transaction.
![img-23.jpeg](images/img-23.jpeg.png)

Figure 23: MODBUS client sequence diagram

General comments for a better understanding of the Client sequence diagram:
First step: A Reading query comes from User Application (method m_Read).
Second Step: The 'Client' task receives the MODBUS query (method m_ClientReceivingMessage). This is the entry point of the Client. To associate the query with the corresponding response when it will arrive, the Client uses a Transaction resource (Class CTransaction). The MODBUS query is sent to the TCP_Management by calling the class interface CInterfaceResponseMsg (method m_MODBUSRequest)

Third Step: If the connection is already established there is nothing to do on connection, the message can be send over the network. Otherwise, a connection must be opened before the message can be sent over the network.
At this time the client is waiting for a response (from a remote server)
Fourth step: Once a response has been received from the network, the TCP/IP stack receives data (method m_EventOnSocket is implicitly called).
If the connection is already established, then the MBAP is read for retrieving the connection object (connection object gives memory resource and other information). Data coming from network is read and confirmation is sent to the client task via the class Interface CInterfaceIndicationMsg (method m_MODBUSConfirmation). Client task receives the MODBUS Confirmation (method m_ClientReceivingResponse).
Finally the response is-written to the user application (method m_WriteData), and transaction resource is freed.


Figure 24 shows a sequence diagram of a MODBUS server exchange. It illustrates the interactions between various components involved in a MODBUS TCP/IP connection. The diagram includes labeled blocks representing different connection states and methods such as 'm_ConnectionRequest', 'm_ReceiveData', and 'm_ServeModbus'. Arrows depict the flow of messages and actions between these components, demonstrating the process of handling a MODBUS server request and response.

Hereafter is an example of a MODBUS Server exchange.
![img-24.jpeg](images/img-24.jpeg.png)

Figure 24: MODBUS server Diagram

General comments for a better understanding of the Server sequence diagram:
First step: a client has sent a query (MODBUS query) over the network.
The TCP/IP stack receives data (method m_EventOnSocket is implicitly called).
Second step: The query may be a connection request or not (method m IsConnexionRequest).
If the query is a connection request, the connection object and buffers for receiving and sending the MODBUS frame are allocated (method m_GetObjectConnexion). Just after, the connection access control must be checked and accepted (method m_AcceptConnexion)

Third step: If the query is a MODBUS request, the complete MODBUS Query can be read (method m_ReceiveData). At this time the MBAP must be analyzed (method m IsMdbHeaderCorrect). The complete frame is sent to the Server task via the CinterfaceindicationMessaging Class (method m_MODBUSIndication). Server task receives the MODBUS Query (method m_ServerReceivingMessage) and analyses it. If an error occurs (function code not supported, etc), a MODBUSException frame is built (m_BuildMODBUSException), otherwise the response is built.

Fourth Step: The response is sent over the network via the CinterfaceResponseMessaging (method m_MODBUSResponse). Treatment on the connection object is done by the method m_SendData (retrieve the connection descriptor, etc) and data is sent over the network.

# 5.4 CLASSES AND METHODS DESCRIPTION 

### 5.4.1 MODBUS Server Class

## Class CMODBUSServer

## class CMODBUSServer

## Stereotype implementationClass

Provides methods for managing MODBUS Messaging in Server Mode

## Field Summary

protected char GlobalState
state of the MODBUS Server

## Constructor Summary

CMODBUSServer(TConfigureObject * InkConfigureObject)
Constructor : Create internal object

## Method Summary

![img-25.jpeg](images/img-25.jpeg.png)

# 5.4.2 MODBUS Client Class 

## Class CMODBUSClient

## class CMODBUSClient

Provides methods for managing MODBUS Messaging in Client Mode
Stereotype implementationClass

## Field Summary

protected GlobalState
char State of the MODBUS Client

## Constructor Summary

CMODBUSClient(TConfigureObject * lnkConfigureObject) Constructor : Create internal object, initialize to 0 variables.

## Method Summary

![img-26.jpeg](images/img-26.jpeg.png)

|  | Method for Stopping component, return true if stopped |
| :--: | :--: |
| protected void | m_tClientMODBUS(void |
|  | Client MODBUS task... |

# 5.4.3 Interface Classes 

### 5.4.3.1 Interface Indication class

## Class C\InterfaceIndicationMsg

## Direct Known Subclasses:

CConnexionMngt

## class CInterfaceIndicationMsg

Class for sending message from TCP_Management to MODBUS Server or Client
Stereotype interface

| Method Summary |  |
| :--: | :--: |
| int | m_MODBUSConfirmation(TItemConnexion * lnkObject) |
|  | Method for Receiving incoming Response, calling the Client : could be by reference, by Message Queue, Remote procedure Call, ... |
| int | m_MODBUSIndication(TItemConnexion * lnkObject) |
|  | Method for reading incoming MODBUS Query and calling the Server : could be by reference, by Message Queue, Remote procedure Call, ... |

### 5.4.3.2 Interface Response Class

## Class CInterfaceResponseMsg

## Direct Known Subclasses:

## CMODBUSClient, CMODBUSServer

## class CInterfaceResponseMsg

Class for sending response or sending query to TCP_Management from Client or Server Stereotype interface

| Method Summary |  |  |  |  |
| :--: | :--: | :--: | :--: | :--: |
| TitemConnexion | m_GetMemoryConnexion(unsigned | long | IPDest) |  |
|  | Get an object I | PConnexion from memory pool. Return -1 if not enough |  |  |
|  | memory |  |  |  |
| int | m_MODBUSRequest(TItemConnexion |  |  | lnkCMODBUS) |
|  | Method for Writing incoming MODBUS Query Client to ConnexionMngt |  |  |  |

|  | could be by reference, by Message Queue, Remote procedure Call, ... |
| :--: | :--: |
| int | m_MODBOSResponse(TItemConnexion * InkObject) |
|  | Method for writing Response from MODBUS Server to ConnexionMngt could be by reference, by Message Queue, Remote procedure Call, ... |

# 5.4.4 Connexion Management class 

## Class CConnexionMngt

## class CConnexionMngt

Class that manages all TCP Connections
Stereotype implementationClass

## Field Summary

| protected <br> char | GlobalState <br> Global State of the Component ConnexionMngt |
| :--: | :--: |
| Int | NbConnectionSupported |
|  | Global number of connections |
| Int | NbLocalConnection |
|  | Number of connections opened by the local Client to a remote Server |
| Int | NbRemoteConnection |
|  | Number of connections opened by a remote Client to the local Server |

## Constructor Summary

CconnexionMngt (TConfigureObject * InkConfigureObject) Constructor : Create internal object, initialize to 0 variables.

## Method Summary

| int | m_EventOnSocket(void <br> wake-up |  |  |  |
| :--: | :--: | :--: | :--: | :--: |
| bool | m_IsConnectionAuthorized(unsigned | long | IPAddress) |  |
| int | Return true if new connection is authorized |  |  |  |
| int | m_ReceiveData(TItemConnexion <br> Interface with CTCPConnexion::write method for reading data from network return negative value if problem |  |  |  |
| bool | m_Reset (void <br> Method for Resetting ConnectionMngt component return true if Reset |  |  |  |
| int | m_SendData(TItemConnexion <br> Interface with CTCPConnexion::read method for sending data to the network Return negative value if problem |  |  |  |
| bool | m_Start(void <br> Method for Starting ConnectionMngt component return true if Started |  |  |  |
| bool | m_Stop(void <br> Method for Stopping component return true if Stopped |  |  |  |

MODBUS Messaging on TCP/IP Implementation Guide V1.0b
Modbus Organization

# MODBUS APPLICATION PROTOCOL SPECIFICATION V1.1b3 

## CONTENTS

1 Introduction ..... 2
1.1 Scope of this document ..... 2
2 Abbreviations ..... 2
3 Context ..... 3
4 General description ..... 3
4.1 Protocol description ..... 3
4.2 Data Encoding ..... 5
4.3 MODBUS Data model ..... 6
4.4 MODBUS Addressing model ..... 7
4.5 Define MODBUS Transaction ..... 8
5 Function Code Categories ..... 10
5.1 Public Function Code Definition ..... 11
6 Function codes descriptions ..... 11
6.1 01 (0x01) Read Coils ..... 11
6.2 02 (0x02) Read Discrete Inputs ..... 12
6.3 03 (0x03) Read Holding Registers ..... 15
6.4 04 (0x04) Read Input Registers ..... 16
6.5 05 (0x05) Write Single Coil ..... 17
6.6 06 (0x06) Write Single Register ..... 19
6.7 07 (0x07) Read Exception Status (Serial Line only) ..... 20
6.8 08 (0x08) Diagnostics (Serial Line only) ..... 21
6.8.1 Sub-function codes supported by the serial line devices ..... 22
6.8.2 Example and state diagram ..... 24
6.9 11 (0x0B) Get Comm Event Counter (Serial Line only) ..... 25
6.10 12 (0x0C) Get Comm Event Log (Serial Line only) ..... 26
6.11 15 (0x0F) Write Multiple Coils ..... 29
6.12 16 (0x10) Write Multiple registers ..... 30
6.13 17 (0x11) Report Server ID (Serial Line only) ..... 31
6.14 20 (0x14) Read File Record ..... 32
6.15 21 (0x15) Write File Record ..... 34
6.16 22 (0x16) Mask Write Register ..... 36
6.17 23 (0x17) Read/Write Multiple registers ..... 38
6.18 24 (0x18) Read FIFO Queue ..... 40
6.19 43 ( 0x2B) Encapsulated Interface Transport ..... 41
6.20 43 / 13 (0x2B / 0x0D) CANopen General Reference Request and Response PDU ..... 42
6.21 43 / 14 (0x2B / 0x0E) Read Device Identification ..... 43
7 MODBUS Exception Responses ..... 47
Annex A (Informative): MODBUS RESERVED FUNCTION CODES, SUBCODES AND MEI TYPES ..... 50
Annex B (Informative): CANOPEN GENERAL REFERENCE COMMAND ..... 50

# 1 Introduction 

### 1.1 Scope of this document

MODBUS is an application layer messaging protocol, positioned at level 7 of the OSI model, which provides client/server communication between devices connected on different types of buses or networks.
The industry's serial de facto standard since 1979, MODBUS continues to enable millions of automation devices to communicate. Today, support for the simple and elegant structure of MODBUS continues to grow. The Internet community can access MODBUS at a reserved system port 502 on the TCP/IP stack.
MODBUS is a request/reply protocol and offers services specified by function codes. MODBUS function codes are elements of MODBUS request/reply PDUs. The objective of this document is to describe the function codes used within the framework of MODBUS transactions.

MODBUS is an application layer messaging protocol for client/server communication between devices connected on different types of buses or networks.
It is currently implemented using:

- TCP/IP over Ethernet. See MODBUS Messaging Implementation Guide V1.0a.
- Asynchronous serial transmission over a variety of media (wire : EIA/TIA-232-E, EIA-422, EIA/TIA-485-A; fiber, radio, etc.)
- MODBUS PLUS, a high speed token passing network.
![img-27.jpeg](images/img-27.jpeg.png)

Figure 1: MODBUS communication stack

## 
Figure 1 shows the MODBUS communication stack. It illustrates various layers involved in the MODBUS protocol, including the MODBUS application layer at the top. Below it, different physical layers are depicted such as 'Other', 'MODBUS+ / HDLC', and 'Master / Slave' with corresponding specifications like EIA/TIA-232 or EIA/TIA-485. On the right, 'Modbus on TCP', 'TCP', 'IP', and 'Ethernet II /802.3' are shown, indicating the network and transport layers involved.

References

1. RFC 791, Internet Protocol, Sep81 DARPA

## 2 Abbreviations

ADU Application Data Unit
HDLC High level Data Link Control
HMI Human Machine Interface
IETF Internet Engineering Task Force
I/O Input/Output
IP Internet Protocol
MAC Media Access Control
MB MODBUS Protocol

MBAP MODBUS Application Protocol
PDU Protocol Data Unit
PLC Programmable Logic Controller
TCP Transmission Control Protocol

# 3 Context 

The MODBUS protocol allows an easy communication within all types of network architectures.
![img-28.jpeg](images/img-28.jpeg.png)

Figure 2: Example of MODBUS Network Architecture


Figure 2 shows an example of MODBUS network architecture. It illustrates a network with various devices such as PLC (Programmable Logic Controller), HMI (Human-Machine Interface), and I/O (Input/Output) modules. The network includes different communication links like MODBUS on TCP/IP, RS232, and RS485, interconnected through gateways. The diagram uses labeled blocks and arrows to represent the data flow and connections between devices.

Every type of devices (PLC, HMI, Control Panel, Driver, Motion control, I/O Device...) can use MODBUS protocol to initiate a remote operation.
The same communication can be done as well on serial line as on an Ethernet TCP/IP networks. Gateways allow a communication between several types of buses or network using the MODBUS protocol.

## 4 General description

### 4.1 Protocol description


Figure 3 shows the general MODBUS frame structure. It consists of an ADU (Application Data Unit) which includes fields such as Additional address, Function code, Data, and Error check. These components are organized in a linear sequence to represent the structure of a MODBUS frame.

The MODBUS protocol defines a simple protocol data unit (PDU) independent of the underlying communication layers. The mapping of MODBUS protocol on specific buses or network can introduce some additional fields on the application data unit (ADU).
![img-29.jpeg](images/img-29.jpeg.png)

The MODBUS application data unit is built by the client that initiates a MODBUS transaction. The function indicates to the server what kind of action to perform. The MODBUS application protocol establishes the format of a request initiated by a client.
The function code field of a MODBUS data unit is coded in one byte. Valid codes are in the range of $1 \mathrm{~cm}-255$ decimal (the range $128-255$ is reserved and used for exception responses). When a message is sent from a Client to a Server device the function code field tells the server what kind of action to perform. Function code " 0 " is not valid.
Sub-function codes are added to some function codes to define multiple actions.
The data field of messages sent from a client to server devices contains additional information that the server uses to take the action defined by the function code. This can include items like discrete and register addresses, the quantity of items to be handled, and the count of actual data bytes in the field.
The data field may be nonexistent (of zero length) in certain kinds of requests, in this case the server does not require any additional information. The function code alone specifies the action.
If no error occurs related to the MODBUS function requested in a properly received MODBUS ADU the data field of a response from a server to a client contains the data requested. If an error related to the MODBUS function requested occurs, the field contains an exception code that the server application can use to determine the next action to be taken.
For example a client can read the ON / OFF states of a group of discrete outputs or inputs or it can read/write the data contents of a group of registers.
When the server responds to the client, it uses the function code field to indicate either a normal (error-free) response or that some kind of error occurred (called an exception response). For a normal response, the server simply echoes to the request the original function code.
![img-30.jpeg](images/img-30.jpeg.png)

Figure 4: MODBUS transaction (error free)

Figure 4 shows a MODBUS transaction (error free) between a client and a server. The client initiates a request by sending a 'Function code' and 'Data Request' to the server. The server performs the action and initiates a response by sending back a 'Function code' and 'Data Response' to the client. This diagram illustrates the typical flow of a successful MODBUS communication cycle.


Figure 5 shows a MODBUS transaction (exception response) where an error is detected during the communication between a client and a server. The client initiates a request with a 'Function code' and 'Data Request'. Upon detecting an error, the server initiates an error response by sending an 'Exception Function code' and 'Exception code' back to the client. This diagram demonstrates the error handling mechanism in MODBUS communication.

For an exception response, the server returns a code that is equivalent to the original function code from the request PDU with its most significant bit set to logic 1.
![img-31.jpeg](images/img-31.jpeg.png)

Figure 5:

Note: It is desirable to manage a time out in order not to indefinitely wait for an answer which will perhaps never arrive.

The size of the MODBUS PDU is limited by the size constraint inherited from the first MODBUS implementation on Serial Line network (max. RS485 ADU = 256 bytes).
Therefore:
MODBUS PDU for serial line communication $=256$ - Server address (1 byte) - CRC (2 bytes) $=253$ bytes.

Consequently:
RS232 / RS485 ADU = 253 bytes + Server address (1 byte) + CRC (2 bytes) = 256 bytes.
TCP MODBUS ADU $=253$ bytes + MBAP ( 7 bytes) $=260$ bytes.

The MODBUS protocol defines three PDUs. They are :

- MODBUS Request PDU, mb_req_pdu
- MODBUS Response PDU, mb_rsp_pdu
- MODBUS Exception Response PDU, mb_excep_rsp_pdu

The mb_req_pdu is defined as:
mb_req_pdu = \{function_code, request_data\}, where
function_code $=[$ byte] MODBUS function code,
request_data $=[$ bytes] This field is function code dependent and usually
contains information such as variable references,
variable counts, data offsets, sub-function codes etc.

The mb_rsp_pdu is defined as:
mb_rsp_pdu = \{function_code, response_data\}, where
function_code $=[$ byte] MODBUS function code
response_data $=[$ bytes] This field is function code dependent and usually
contains information such as variable references,
variable counts, data offsets, sub-function codes, etc.

The mb_excep_rsp_pdu is defined as:
mb_excep_rsp_pdu = \{exception-function_code, request_data\}, where exception-function_code $=[1$ byte] MODBUS function code $+0 \times 80$
exception_code $=[$ byte] MODBUS Exception Code Defined in table
"MODBUS Exception Codes" (see section 7 ).

# 4.2 Data Encoding 

- MODBUS uses a 'big-Endian' representation for addresses and data items. This means that when a numerical quantity larger than a single byte is transmitted, the most significant byte is sent first. So for example

| Register size | value |
| :--: | :--: |
| 16 - bits | $0 \times 1234$ the first byte sent is $0 \times 12$ then $0 \times 34$ |

Note: For more details, see [1] .

# 4.3 MODBUS Data model 

MODBUS bases its data model on a series of tables that have distinguishing characteristics. The four primary tables are:

| Primary tables | Object type | Type of | Comments |
| :-- | :-- | :-- | :-- |
| Discretes Input | Single bit | Read-Only | This type of data can be provided by an I/O system. |
| Coils | Single bit | Read-Write | This type of data can be alterable by an application <br> program. |
| Input Registers | 16-bit word | Read-Only | This type of data can be provided by an I/O system |
| Holding Registers | 16-bit word | Read-Write | This type of data can be alterable by an application <br> program. |

The distinctions between inputs and outputs, and between bit-addressable and wordaddressable data items, do not imply any application behavior. It is perfectly acceptable, and very common, to regard all four tables as overlaying one another, if this is the most natural interpretation on the target machine in question.
For each of the primary tables, the protocol allows individual selection of 65536 data items, and the operations of read or write of those items are designed to span multiple consecutive data items up to a data size limit which is dependent on the transaction function code.
It's obvious that all the data handled via MODBUS (bits, registers) must be located in device application memory. But physical address in memory should not be confused with data reference. The only requirement is to link data reference with physical address.
MODBUS logical reference numbers, which are used in MODBUS functions, are unsigned integer indices starting at zero.

## - Implementation examples of MODBUS model

The examples below show two ways of organizing the data in device. There are different organizations possible, but not all are described in this document. Each device can have its own organization of the data according to its application

## Example 1 : Device having 4 separate blocks


Figure 6 shows a MODBUS Data Model with separate blocks. It illustrates the organization of data in a device that has digital and analog inputs and outputs. The diagram depicts four distinct blocks: Input Discrete, Coils, Input Registers, and Holding Registers. Each block is accessed via MODBUS functions, and the separation indicates that data from different blocks have no correlation, allowing for independent access.

The example below shows data organization in a device having digital and analog, inputs and outputs. Each block is separate because data from different blocks have no correlation. Each block is thus accessible with different MODBUS functions.
![img-32.jpeg](images/img-32.jpeg.png)

Figure 6 MODBUS Data Model with separate block

# Example 2: Device having only 1 block 

In this example, the device has only 1 data block. The same data can be reached via several MODBUS functions, either via a 16 bit access or via an access bit.
![img-33.jpeg](images/img-33.jpeg.png)

Figure 7 MODBUS Data Model with only 1 block

### 4.4 MODBUS Addressing model


Figure 7 shows a MODBUS Data Model with only 1 block. It illustrates a device application memory structure where different types of data such as Input Discrete, Coils, Input Registers, and Holding Registers are accessed via MODBUS. The diagram includes arrows indicating read (R) and write (W) operations, and a MODBUS Request is shown entering the system.

The MODBUS application protocol defines precisely PDU addressing rules.
In a MODBUS PDU each data is addressed from 0 to 65535.
It also defines clearly a MODBUS data model composed of 4 blocks that comprises several elements numbered from 1 to $n$.
In the MODBUS data Model each element within a data block is numbered from 1 to n. Afterwards the MODBUS data model has to be bound to the device application ( IEC-61131 object, or other application model).
The pre-mapping between the MODBUS data model and the device application is totally vendor device specific.

![img-34.jpeg](images/img-34.jpeg.png)

The previous figure shows that a MODBUS data numbered $X$ is addressed in the MODBUS PDU X-1.

# 4.5 Define MODBUS Transaction 

The following state diagram describes the generic processing of a MODBUS transaction in server side.

![img-35.jpeg](images/img-35.jpeg.png)

Figure 9 MODBUS Transaction state diagram

Figure 9 shows a MODBUS transaction state diagram. It illustrates the decision-making process in a MODBUS server transaction. The flow starts with waiting for a MODBUS indication, followed by validating the function code. If invalid, an exception code is assigned, and a Modbus Exception Response is sent. If valid, it proceeds to validate the data address and data value, each with their own exception handling. The final steps involve executing the MODBUS function and sending a Modbus Response.

Once the request has been processed by a server, a MODBUS response using the adequate MODBUS server transaction is built.
Depending on the result of the processing two types of response are built :

- A positive MODBUS response :
- the response function code $=$ the request function code
- A MODBUS Exception response ( see section 7 ):
- the objective is to provide to the client relevant information concerning the error detected during the processing ;
- the exception function code $=$ the request function code $+0 \times 80$;
- an exception code is provided to indicate the reason of the error.

# 5 Function Code Categories 

There are three categories of MODBUS Functions codes. They are :

## Public Function Codes

- Are well defined function codes,
- guaranteed to be unique,
- validated by the MODBUS.org community,
- publicly documented
- have available conformance test,
- includes both defined public assigned function codes as well as unassigned function codes reserved for future use.


## User-Defined Function Codes

- there are two ranges of user-defined function codes, i.e. 65 to 72 and from 100 to 110 decimal.
- user can select and implement a function code that is not supported by the specification.
- there is no guarantee that the use of the selected function code will be unique
- if the user wants to re-position the functionality as a public function code, he must initiate an RFC to introduce the change into the public category and to have a new public function code assigned.
- MODBUS Organization, Inc expressly reserves the right to develop the proposed RFC.


## Reserved Function Codes

- 
Figure 10 shows a diagram categorizing MODBUS function codes. It visually distinguishes between 'PUBLIC function codes' and 'User Defined Function codes' across different numerical ranges. The diagram is structured with labeled sections indicating the ranges 1 to 127, with specific emphasis on ranges 65 to 72 and 100 to 110 for user-defined codes.

Function Codes currently used by some companies for legacy products and that are not available for public use.
- Informative Note: The reader is asked refer to Annex A (Informative) MODBUS RESERVED FUNCTION CODES, SUBCODES AND MEI TYPES.
![img-36.jpeg](images/img-36.jpeg.png)

Figure 10 MODBUS Function Code Categories

# 5.1 Public Function Code Definition 

|  |  |  |  | Function Codes |  |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|  |  |  |  | code | Sub code | (hex) | Section |
| Data Access | Bit <br> access | Physical Discrete Inputs | Read Discrete Inputs | 02 |  | 02 | 6.2 |
|  |  | Internal Bits Or Physical coils | Read Coils | 01 |  | 01 | 6.1 |
|  |  |  | Write Single Coil | 05 |  | 05 | 6.5 |
|  |  |  | Write Multiple Coils | 15 |  | 0 F | 6.11 |
|  | 16 bits access | Physical Input Registers | Read Input Register | 04 |  | 04 | 6.4 |
|  |  | Internal Registers Or Physical Output Registers | Read Holding Registers | 03 |  | 03 | 6.3 |
|  |  |  | Write Single Register | 06 |  | 06 | 6.6 |
|  |  |  | Write Multiple Registers | 16 |  | 10 | 6.12 |
|  |  |  | Read/Write Multiple Registers | 23 |  | 17 | 6.17 |
|  |  |  | Mask Write Register | 22 |  | 16 | 6.16 |
|  |  |  | Read FIFO queue | 24 |  | 18 | 6.18 |
|  | File record access |  | Read File record | 20 |  | 14 | 6.14 |
|  |  |  | Write File record | 21 |  | 15 | 6.15 |
| Diagnostics |  |  | Read Exception status | 07 |  | 07 | 6.7 |
|  |  |  | Diagnostic | 08 | 00-18,20 | 08 | 6.8 |
|  |  |  | Get Com event counter | 11 |  | OB | 6.9 |
|  |  |  | Get Com Event Log | 12 |  | 0 C | 6.10 |
|  |  |  | Report Server ID | 17 |  | 11 | 6.13 |
|  |  |  | Read device Identification | 43 | 14 | 2B | 6.21 |
| Other |  |  | Encapsulated Interface Transport | 43 | 13,14 | 2B | 6.19 |
|  |  |  | CANopen General Reference | 43 | 13 | 2B | 6.20 |

## 6 Function codes descriptions

### 6.1 01 (0x01) Read Coils

This function code is used to read from 1 to 2000 contiguous status of coils in a remote device. The Request PDU specifies the starting address, i.e. the address of the first coil specified, and the number of coils. In the PDU Coils are addressed starting at zero. Therefore coils numbered $1-16$ are addressed as $0-15$.
The coils in the response message are packed as one coil per bit of the data field. Status is indicated as $1=$ ON and $0=$ OFF. The LSB of the first data byte contains the output addressed in the query. The other coils follow toward the high order end of this byte, and from low order to high order in subsequent bytes.
If the returned output quantity is not a multiple of eight, the remaining bits in the final data byte will be padded with zeros (toward the high order end of the byte). The Byte Count field specifies the quantity of complete bytes of data.

## Request

| Function code | 1 Byte | $0 \times 01$ |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of coils | 2 Bytes | 1 to 2000 (0x7D0) |

Response

| Function code | 1 Byte | $0 \times 01$ |
| :-- | :-- | :-- |
| Byte count | 1 Byte | $\mathbf{N}^{\prime}$ |
| Coil Status | n Byte | $\mathrm{n}=\mathrm{N}$ or $\mathrm{N}+1$ |

April 26, 2012
http://www.modbus.org

Error

| Function code | 1 Byte | Function code + 0x80 |
| :-- | :--: | :--: |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to read discrete outputs 20-38:

| Request |  | Response |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 01 | Function | 01 |
| Starting Address Hi | 00 | Byte Count | 03 |
| Starting Address Lo | 13 | Outputs status 27-20 | CD |
| Quantity of Outputs Hi | 00 | Outputs status 35-28 | 6B |
| Quantity of Outputs Lo | 13 | Outputs status 38-36 | 05 |

The status of outputs $27-20$ is shown as the byte value CD hex, or binary 11001101 . Output 27 is the MSB of this byte, and output 20 is the LSB.
By convention, bits within a byte are shown with the MSB to the left, and the LSB to the right. Thus the outputs in the first byte are ' 27 through $20^{\prime}$, from left to right. The next byte has outputs ' 35 through $28^{\prime}$, left to right. As the bits are transmitted serially, they flow from LSB to MSB: $20 \ldots 27,28 \ldots 35$, and so on.
In the last data byte, the status of outputs $38-36$ is shown as the byte value 05 hex, or binary 00000101 . Output 38 is in the sixth bit position from the left, and output 36 is the LSB of this byte. The five remaining high order bits are zero filled.

Note: The five remaining bits (toward the high order end) are zero filled.
![img-37.jpeg](images/img-37.jpeg.png)

Figure 11: Read Coils state diagram

# 6.2 02 (0x02) Read Discrete Inputs 


Figure 11 shows a state diagram for the Read Coils process in a Modbus server. It begins with the MB Server receiving a request PDU. The diagram includes decision nodes for checking if the function code is supported and whether the quantity of outputs is within the valid range. It also checks if the starting address and quantity of outputs are correct before proceeding to request processing. Exception codes are assigned for various errors, and appropriate responses are sent by the server.

This function code is used to read from 1 to 2000 contiguous status of discrete inputs in a remote device. The Request PDU specifies the starting address, i.e. the address of the first

input specified, and the number of inputs. In the PDU Discrete Inputs are addressed starting at zero. Therefore Discrete inputs numbered 1-16 are addressed as 0-15.
The discrete inputs in the response message are packed as one input per bit of the data field. Status is indicated as $1=\mathrm{ON} ; 0=$ OFF. The LSB of the first data byte contains the input addressed in the query. The other inputs follow toward the high order end of this byte, and from low order to high order in subsequent bytes.
If the returned input quantity is not a multiple of eight, the remaining bits in the final data byte will be padded with zeros (toward the high order end of the byte). The Byte Count field specifies the quantity of complete bytes of data.

# Request 

| Function code | 1 Byte | $0 \times 02$ |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of Inputs | 2 Bytes | 1 to 2000 (0x7D0) |

## Response

| Function code | 1 Byte | $0 \times 02$ |
| :-- | :-- | :-- |
| Byte count | 1 Byte | $\mathbf{N}^{*}$ |
| Input Status | $\mathbf{N}^{*} \times 1$ Byte |  |
| ${ }^{*} \mathbf{N}=$ Quantity of Inputs / 8 if the remainder is different of $0 \Rightarrow \mathrm{~N}=\mathrm{N}+1$ |  |  |
| Error |  |  |
|  | Error code | 1 Byte | $0 \times 82$ |
|  | Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to read discrete inputs 197 - 218:

| Request |  | Response |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 02 | Function | 02 |
| Starting Address Hi | 00 | Byte Count | 03 |
| Starting Address Lo | C4 | Inputs Status 204-197 | AC |
| Quantity of Inputs Hi | 00 | Inputs Status 212-205 | DB |
| Quantity of Inputs Lo | 16 | Inputs Status 218-213 | 35 |

The status of discrete inputs 204-197 is shown as the byte value AC hex, or binary 1010 1100. Input 204 is the MSB of this byte, and input 197 is the LSB.

The status of discrete inputs 218-213 is shown as the byte value 35 hex, or binary 00110101. Input 218 is in the third bit position from the left, and input 213 is the LSB.

Note: The two remaining bits (toward the high order end) are zero filled.

![img-38.jpeg](images/img-38.jpeg.png)

Figure 12: Read Discrete Inputs state diagram

# 6.3 03 (0x03) Read Holding Registers 

This function code is used to read the contents of a contiguous block of holding registers in a remote device. The Request PDU specifies the starting register address and the number of registers. In the PDU Registers are addressed starting at zero. Therefore registers numbered $1-16$ are addressed as $0-15$.
The register data in the response message are packed as two bytes per register, with the binary contents right justified within each byte. For each register, the first byte contains the high order bits and the second contains the low order bits.

## Request

| Function code | 1 Byte | 0x03 |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of Registers | 2 Bytes | 1 to 125 (0x7D) |

## Response

| Function code | 1 Byte | 0x03 |
| :-- | :-- | :-- |
| Byte count | 1 Byte | $2 \times \mathbf{N}^{+}$ |
| Register value | $\mathbf{N}^{+}$x 2 Bytes |  |

## Error

| Error code | 1 Byte | 0x83 |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to read registers 108 - 110:

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 03 | Function | 03 |
| Starting Address Hi | 00 | Byte Count | 06 |
| Starting Address Lo | 6B | Register value Hi (108) | 02 |
| No. of Registers Hi | 00 | Register value Lo (108) | 2B |
| No. of Registers Lo | 03 | Register value Hi (109) | 00 |
|  |  | Register value Lo (109) | 00 |
|  |  | Register value Hi (110) | 00 |
|  |  | Register value Lo (110) | 64 |

The contents of register 108 are shown as the two byte values of 022 B hex, or 555 decimal. The contents of registers 109-110 are 0000 and 0064 hex, or 0 and 100 decimal, respectively.

![img-39.jpeg](images/img-39.jpeg.png)

Figure 13: Read Holding Registers state diagram

# 6.4 04 (0x04) Read Input Registers 


Figure 13 shows a state diagram for the Read Holding Registers function in a Modbus server. It begins with the MB Server receiving a request and checks if the function code is supported. Various decision points determine the flow based on conditions such as exception codes and the validity of register addresses. The diagram includes labeled blocks and arrows indicating the flow of data and decisions, ultimately leading to the server sending a response or an exception.

This function code is used to read from 1 to 125 contiguous input registers in a remote device. The Request PDU specifies the starting register address and the number of registers. In the PDU Registers are addressed starting at zero. Therefore input registers numbered 1-16 are addressed as $0-15$.
The register data in the response message are packed as two bytes per register, with the binary contents right justified within each byte. For each register, the first byte contains the high order bits and the second contains the low order bits.
Request

| Function code | 1 Byte | 0x04 |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of Input Registers | 2 Bytes | $0 \times 0001$ to $0 \times 0070$ |

## Response

| Function code | 1 Byte | 0x04 |
| :-- | :-- | :-- |
| Byte count | 1 Byte | $2 \times \mathbf{N}^{+}$ |
| Input Registers | $\mathbf{N}^{+}+2$ Bytes |  |

${ }^{\star} \mathbf{N}=$ Quantity of Input Registers
Error

| Error code | 1 Byte | 0x84 |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to read input register 9:

| Request |  | Response |  |
| :-- | --: | :-- | --: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 04 | Function | 04 |
| Starting Address Hi | 00 | Byte Count | 02 |
| Starting Address Lo | 08 | Input Reg. 9 Hi | 00 |
| Quantity of Input Reg. Hi | 00 | Input Reg. 9 Lo | 0A |

April 26, 2012
http://www.modbus.org

The contents of input register 9 are shown as the two byte values of 000 A hex, or 10 decimal.
![img-40.jpeg](images/img-40.jpeg.png)

Figure 14: Read Input Registers state diagram

# 
Figure 14 shows a state diagram for reading input registers in a Modbus communication system. It begins with the MB Server receiving a request (mb_req_pdu) and progresses through various decision points based on function code support and address validations. Exception codes are used to handle errors, and the process ends with the server sending a response (mb_rsp) or an exception response (mb_exception_rsp).

6.5 05 (0x05) Write Single Coil 

This function code is used to write a single output to either ON or OFF in a remote device. The requested ON/OFF state is specified by a constant in the request data field. A value of FF 00 hex requests the output to be ON. A value of 0000 requests it to be OFF. All other values are illegal and will not affect the output.
The Request PDU specifies the address of the coil to be forced. Coils are addressed starting at zero. Therefore coil numbered 1 is addressed as 0 . The requested ON/OFF state is specified by a constant in the Coil Value field. A value of 0 XFF 00 requests the coil to be ON . A value of 0X0000 requests the coil to be off. All other values are illegal and will not affect the coil.

The normal response is an echo of the request, returned after the coil state has been written.

## Request

| Function code | 1 Byte | 0x05 |
| :-- | :-- | :-- |
| Output Address | 2 Bytes | $0 \times 0000$ to 0xFFFF |
| Output Value | 2 Bytes | $0 \times 0000$ or 0xFF00 |

## Response

| Function code | 1 Byte | 0x05 |
| :-- | :-- | :-- |
| Output Address | 2 Bytes | $0 \times 0000$ to 0xFFFF |

April 26, 2012
http://www.modbus.org

| Output Value | 2 Bytes | $0 \times 0000$ or $0 x F F 00$ |
| :-- | :-- | :-- |
| Error |  |  |
| Error code | 1 Byte | $0 \times 85$ |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to write Coil 173 ON:

| Request |  | Response |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 05 | Function | 05 |
| Output Address Hi | 00 | Output Address Hi | 00 |
| Output Address Lo | AC | Output Address Lo | AC |
| Output Value Hi | FF | Output Value Hi | FF |
| Output Value Lo | 00 | Output Value Lo | 00 |

![img-41.jpeg](images/img-41.jpeg.png)

Figure 15: Write Single Output state diagram

# 6.6 06 (0x06) Write Single Register 


Figure 15 shows a flowchart of the 'Write Single Output' state diagram in a Modbus server. It begins with the server receiving a request PDU (Protocol Data Unit). The diagram outlines decision points such as whether the function code is supported, if the output value is within acceptable limits, and if the output address is correct. The flowchart includes exception handling paths for various error codes and concludes with either sending a response or an exception response.

This function code is used to write a single holding register in a remote device.
The Request PDU specifies the address of the register to be written. Registers are addressed starting at zero. Therefore register numbered 1 is addressed as 0 .
The normal response is an echo of the request, returned after the register contents have been written.

## Request

| Function code | 1 Byte | 0x06 |
| :-- | :-- | :-- |
| Register Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Register Value | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |

## Response

| Function code | 1 Byte | 0x06 |
| :-- | :-- | :-- |
| Register Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Register Value | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |

## Error

| Error code | 1 Byte | 0x06 |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to write register 2 to 0003 hex:

| Request |  | Response |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 06 | Function | 06 |
| Register Address Hi | 00 | Register Address Hi | 00 |
| Register Address Lo | 01 | Register Address Lo | 01 |
| Register Value Hi | 00 | Register Value Hi | 00 |
| Register Value Lo | 03 | Register Value Lo | 03 |

![img-42.jpeg](images/img-42.jpeg.png)

Figure 16: Write Single Register state diagram

# 6.7 07 (0x07) Read Exception Status (Serial Line only) 


Figure 16 shows a flowchart of the 'Write Single Register' state diagram for a Modbus server. It begins with the server receiving an 'mb_req_pdu' and checks if the function code is supported. If not, it generates an ExceptionCode = 01. If supported, it verifies if the register value is within the appropriate range, otherwise, ExceptionCode = 03 is generated. The diagram continues with checks for register address validity and WriteSingleRegister status, leading to various processing paths and potential exception codes.

This function code is used to read the contents of eight Exception Status outputs in a remote device.
The function provides a simple method for accessing this information, because the Exception Output references are known (no output reference is needed in the function).
The normal response contains the status of the eight Exception Status outputs. The outputs are packed into one data byte, with one bit per output. The status of the lowest output reference is contained in the least significant bit of the byte.
The contents of the eight Exception Status outputs are device specific.
Request

| Function code | 1 Byte | $0 \times 07$ |
| :-- | :-- | :-- |

Response

| Function code | 1 Byte | $0 \times 07$ |
| :-- | :-- | :-- |
| Output Data | 1 Byte | $0 \times 00$ to $0 \times F F$ |

Error

| Error code | 1 Byte | $0 \times 07$ |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 04 |

Here is an example of a request to read the exception status:

| Request | Response |  |
| :-- | :--: | :--: |
| Field Name | (Hex) | Field Name |
| Function | $\mathbf{0 7}$ | Function <br> Output Data |

In this example, the output data is 6D hex (0110 1101 binary). Left to right, the outputs are OFF-ON-ON-OFF-ON-ON-OFF-ON. The status is shown from the highest to the lowest addressed output.
![img-43.jpeg](images/img-43.jpeg.png)

Figure 17: Read Exception Status state diagram

# 6.8 08 (0x08) Diagnostics (Serial Line only) 


Figure 17 shows a state diagram for the Read Exception Status process in a Modbus server. It illustrates the sequence of operations starting with the server receiving a request PDU (Protocol Data Unit). The diagram includes decision points for checking if the function code is supported and whether the exception status is OK. Based on these conditions, the server may send a response or an exception response.

MODBUS function code 08 provides a series of tests for checking the communication system between a client device and a server, or for checking various internal error conditions within a server.
The function uses a two-byte sub-function code field in the query to define the type of test to be performed. The server echoes both the function code and sub-function code in a normal response. Some of the diagnostics cause data to be returned from the remote device in the data field of a normal response.
In general, issuing a diagnostic function to a remote device does not affect the running of the user program in the remote device. User logic, like discrete and registers, is not accessed by the diagnostics. Certain functions can optionally reset error counters in the remote device.
A server device can, however, be forced into 'Listen Only Mode' in which it will monitor the messages on the communications system but not respond to them. This can affect the outcome of your application program if it depends upon any further exchange of data with the remote device. Generally, the mode is forced to remove a malfunctioning remote device from the communications system.

The following diagnostic functions are dedicated to serial line devices.
The normal response to the Return Query Data request is to loopback the same data. The function code and sub-function codes are also echoed.

## Request

| Function code | 1 Byte | $0 \times 08$ |
| :-- | :-- | :-- |
| Sub-function | 2 Bytes |  |
| Data | N $\times 2$ Bytes |  |

April 26, 2012
http://www.modbus.org

# Response 

| Function code | 1 Byte | $0 \times 08$ |
| :-- | :-- | :-- |
| Sub-function | 2 Bytes |  |
| Data | N $\times 2$ Bytes |  |

Error

| Error code | 1 Byte | $0 \times 88$ |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 03 or 04 |

### 6.8.1 Sub-function codes supported by the serial line devices

Here the list of sub-function codes supported by the serial line devices. Each sub-function code is then listed with an example of the data field contents that would apply for that diagnostic.

| Sub-function code |  | Name |
| :--: | :--: | :--: |
| Hex | Dec |  |
| 00 | 00 | Return Query Data |
| 01 | 01 | Restart Communications Option |
| 02 | 02 | Return Diagnostic Register |
| 03 | 03 | Change ASCII Input Delimiter |
| 04 | 04 | Force Listen Only Mode |
|  | 05. 09 | RESERVED |
| 0A | 10 | Clear Counters and Diagnostic Register |
| 0B | 11 | Return Bus Message Count |
| 0C | 12 | Return Bus Communication Error Count |
| 0D | 13 | Return Bus Exception Error Count |
| 0E | 14 | Return Server Message Count |
| 0F | 15 | Return Server No Response Count |
| 10 | 16 | Return Server NAK Count |
| 11 | 17 | Return Server Busy Count |
| 12 | 18 | Return Bus Character Overrun Count |
| 13 | 19 | RESERVED |
| 14 | 20 | Clear Overrun Counter and Flag |
| N.A. | 21 ... 65535 | RESERVED |

## 00 Return Query Data

The data passed in the request data field is to be returned (looped back) in the response. The entire response message should be identical to the request.

Sub-function
0000

Data Field (Request)
Any

Data Field (Response)
Echo Request Data

## 01 Restart Communications Option

The remote device serial line port must be initialized and restarted, and all of its communications event counters are cleared. If the port is currently in Listen Only Mode, no response is returned. This function is the only one that brings the port out of Listen Only Mode. If the port is not currently in Listen Only Mode, a normal response is returned. This occurs before the restart is executed.
When the remote device receives the request, it attempts a restart and executes its power-up confidence tests. Successful completion of the tests will bring the port online.
A request data field contents of FF 00 hex causes the port's Communications Event Log to be cleared also. Contents of 0000 leave the log as it was prior to the restart.

Sub-function
0001
0001
Data Field (Request)
0000
0000
0000
0000

Data Field (Response)
Echo Request Data
Echo Request Data

## 02 Return Diagnostic Register

The contents of the remote device's 16-bit diagnostic register are returned in the response.

Sub-function
0002
Data Field (Request)
0000
Data Field (Response)
0000 Diagnostic Register Contents

# 03 Change ASCII Input Delimiter 

The character 'CHAR' passed in the request data field becomes the end of message delimiter for future messages (replacing the default LF character). This function is useful in cases of a Line Feed is not required at the end of ASCII messages.

| Sub-function | Data Field (Request) | Data Field (Response) |
| :-- | :-- | :-- |
| 0003 | CHAR 00 | Echo Request Data |

## 04 Force Listen Only Mode

Forces the addressed remote device to its Listen Only Mode for MODBUS communications. This isolates it from the other devices on the network, allowing them to continue communicating without interruption from the addressed remote device. No response is returned.
When the remote device enters its Listen Only Mode, all active communication controls are turned off. The Ready watchdog timer is allowed to expire, locking the controls off. While the device is in this mode, any MODBUS messages addressed to it or broadcast are monitored, but no actions will be taken and no responses will be sent.
The only function that will be processed after the mode is entered will be the Restart Communications Option function (function code 8, sub-function 1).

| Sub-function | Data Field (Request) | Data Field (Response) |
| :-- | :-- | :-- |
| 0004 | 0000 | No Response Returned |

## 10 (0A Hex) Clear Counters and Diagnostic Register

The goal is to clear all counters and the diagnostic register. Counters are also cleared upon power-up.

Sub-function
00 OA
0000
Data Field (Request)
0000

## Data Field (Response)

Echo Request Data

## 11 (0B Hex) Return Bus Message Count

The response data field returns the quantity of messages that the remote device has detected on the communications system since its last restart, clear counters operation, or power-up.

Sub-function
000 B
Data Field (Request)
0000

## Data Field (Response)

Total Message Count

## 12 (0C Hex) Return Bus Communication Error Count

The response data field returns the quantity of CRC errors encountered by the remote device since its last restart, clear counters operation, or power-up.

Sub-function
00 OC
Data Field (Request)
0000

## Data Field (Response)

CRC Error Count

## 13 (0D Hex) Return Bus Exception Error Count

The response data field returns the quantity of MODBUS exception responses returned by the remote device since its last restart, clear counters operation, or power-up.
Exception responses are described and listed in section 7 .

| Sub-function | Data Field (Request) | Data Field (Response) |
| :-- | :-- | :-- |
| 000 D | 0000 | Exception Error Count |

## 14 (0E Hex) Return Server Message Count

The response data field returns the quantity of messages addressed to the remote device, or broadcast, that the remote device has processed since its last restart, clear counters operation, or power-up.

Sub-function
000 E
Data Field (Request)
0000

## Data Field (Response)

Server Message Count

## 15 (0F Hex) Return Server No Response Count

The response data field returns the quantity of messages addressed to the remote device for which it has returned no response (neither a normal response nor an exception response), since its last restart, clear counters operation, or power-up.

| Sub-function | Data Field (Request) | Data Field (Response) |
| :-- | :-- | :-- |
| 000 F | 0000 | Server No Response Count |

# 16 (10 Hex) Return Server NAK Count 

The response data field returns the quantity of messages addressed to the remote device for which it returned a Negative Acknowledge (NAK) exception response, since its last restart, clear counters operation, or power-up. Exception responses are described and listed in section 7 .

Sub-function Data Field (Request) Data Field (Response)
001000000 Server NAK Count

## 17 (11 Hex) Return Server Busy Count

The response data field returns the quantity of messages addressed to the remote device for which it returned a Server Device Busy exception response, since its last restart, clear counters operation, or power-up.

Sub-function Data Field (Request) Data Field (Response)
001100000 Server Device Busy Count

## 18 (12 Hex) Return Bus Character Overrun Count

The response data field returns the quantity of messages addressed to the remote device that it could not handle due to a character overrun condition, since its last restart, clear counters operation, or power-up. A character overrun is caused by data characters arriving at the port faster than they can be stored, or by the loss of a character due to a hardware malfunction.

Sub-function Data Field (Request) Data Field (Response)
001200000 Server Character Overrun Count

## 20 (14 Hex) Clear Overrun Counter and Flag

Clears the overrun error counter and reset the error flag.

| Sub-function | Data Field (Request) | Data Field (Response) |
| :-- | :-- | :-- |
| 0014 | 0000 | Echo Request Data |

### 6.8.2 Example and state diagram

Here is an example of a request to remote device to Return Query Data. This uses a subfunction code of zero ( 0000 hex in the two-byte field). The data to be returned is sent in the two-byte data field (A5 37 hex).

| Request |  | Response |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 08 | Function | 08 |
| Sub-function Hi | 00 | Sub-function Hi | 00 |
| Sub-function Lo | 00 | Sub-function Lo | 00 |
| Data Hi | A5 | Data Hi | A5 |
| Data Lo | 37 | Data Lo | 37 |

The data fields in responses to other kinds of queries could contain error counts or other data requested by the sub-function code.

![img-44.jpeg](images/img-44.jpeg.png)

Figure 18: Diagnostic state diagram

# 6.9 11 (0x0B) Get Comm Event Counter (Serial Line only) 

This function code is used to get a status word and an event count from the remote device's communication event counter.
By fetching the current count before and after a series of messages, a client can determine whether the messages were handled normally by the remote device.
The device's event counter is incremented once for each successful message completion. It is not incremented for exception responses, poll commands, or fetch event counter commands.
The event counter can be reset by means of the Diagnostics function (code 08), with a subfunction of Restart Communications Option (code 00 01) or Clear Counters and Diagnostic Register (code 00 0A).
The normal response contains a two-byte status word, and a two-byte event count. The status word will be all ones (FF FF hex) if a previously-issued program command is still being processed by the remote device (a busy condition exists). Otherwise, the status word will be all zeros.

## Request

| Function code | 1 Byte | 0x0B |
| :-- | :-- | :-- |
| Response |  |  |
| Function code | 1 Byte | 0x0B |
| Status | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Event Count | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |

## Error

| Error code | 1 Byte | 0x8B |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 04 |

Here is an example of a request to get the communications event counter in remote device:

## Request Response

| Field Name | (Hex) | Field Name | (Hex) |
| :-- | :--: | :-- | :--: |
| Function | 0B | Function | 0B |
|  |  | Status Hi | FF |
|  |  | Status Lo | FF |
|  |  | Event Count Hi | 01 |
|  |  | Event Count Lo | 0B |

In this example, the status word is FF FF hex, indicating that a program function is still in progress in the remote device. The event count shows that 264 ( 0108 hex) events have been counted by the device.
![img-45.jpeg](images/img-45.jpeg.png)

Figure 19: Get Comm Event Counter state diagram

# 6.10 12 (0x0C) Get Comm Event Log (Serial Line only) 


Figure 19 shows a state diagram for the 'Get Comm Event Counter' process in a Modbus server. It begins with the MB Server receiving an 'mb_req_pdu'. The flow checks if the function code is supported, proceeding to request processing if yes, or returning an exception code if no. If the 'GetCommEventCounter' is okay, the server sends an 'mb_rsp'. Otherwise, it sends an 'mb_exception_rsp'.

This function code is used to get a status word, event count, message count, and a field of event bytes from the remote device.
The status word and event counts are identical to that returned by the Get Communications Event Counter function (11, 0B hex).
The message counter contains the quantity of messages processed by the remote device since its last restart, clear counters operation, or power-up. This count is identical to that returned by the Diagnostic function (code 08), sub-function Return Bus Message Count (code 11, 0B hex).
The event bytes field contains 0-64 bytes, with each byte corresponding to the status of one MODBUS send or receive operation for the remote device. The remote device enters the events into the field in chronological order. Byte 0 is the most recent event. Each new byte flushes the oldest byte from the field.

The normal response contains a two-byte status word field, a two-byte event count field, a two-byte message count field, and a field containing 0-64 bytes of events. A byte count field defines the total length of the data in these four fields.
Request

| Function code | 1 Byte | $0 \times 0 C$ |
| :-- | :-- | :-- |

Response

| Function code | 1 Byte | $0 \times 0 C$ |
| :-- | :-- | :-- |
| Byte Count | 1 Byte | $\mathbf{N}^{*}$ |
| Status | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Event Count | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Message Count | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Events | $(N-6) \times 1$ Byte |  |

*N = Quantity of Events $+3 \times 2$ Bytes, (Length of Status, Event Count and Message Count)
Error

| Error code | 1 Byte | $0 \times 0 C$ |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 04 |

Here is an example of a request to get the communications event log in remote device:

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 0 C | Function | 0 C |
|  |  | Byte Count | 08 |
|  |  | Status Hi | 00 |
|  |  | Status Lo | 00 |
|  |  | Event Count Hi | 01 |
|  |  | Event Count Lo | 08 |
|  |  | Message Count Hi | 01 |
|  |  | Message Count Lo | 21 |
|  |  | Event 0 | 20 |
|  |  | Event 1 | 00 |

In this example, the status word is 0000 hex, indicating that the remote device is not processing a program function. The event count shows that 264 ( 0108 hex) events have been counted by the remote device. The message count shows that 289 ( 0121 hex) messages have been processed.
The most recent communications event is shown in the Event 0 byte. Its content ( 20 hex) show that the remote device has most recently entered the Listen Only Mode.
The previous event is shown in the Event 1 byte. Its contents ( 00 hex) show that the remote device received a Communications Restart.

The layout of the response's event bytes is described below.

# What the Event Bytes Contain 

An event byte returned by the Get Communications Event Log function can be any one of four types. The type is defined by bit 7 (the high-order bit) in each byte. It may be further defined by bit 6 . This is explained below.

## - Remote device MODBUS Receive Event

The remote device stores this type of event byte when a query message is received. It is stored before the remote device processes the message. This event is defined by bit 7 set to logic ' 1 '. The other bits will be set to a logic ' 1 ' if the corresponding condition is TRUE. The bit layout is:

## Bit Contents

0 Not Used
1 Communication Error
2 Not Used
3 Not Used
4 Character Overrun

5 Currently in Listen Only Mode
6 Broadcast Received
$7 \quad 1$

# - Remote device MODBUS Send Event 

The remote device stores this type of event byte when it finishes processing a request message. It is stored if the remote device returned a normal or exception response, or no response. This event is defined by bit 7 set to a logic ' 0 ', with bit 6 set to a ' 1 '. The other bits will be set to a logic ' 1 ' if the corresponding condition is TRUE. The bit layout is:

## Bit Contents

0 Read Exception Sent (Exception Codes 1-3)
1 Server Abort Exception Sent (Exception Code 4)
2 Server Busy Exception Sent (Exception Codes 5-6)
3 Server Program NAK Exception Sent (Exception Code 7)
4 Write Timeout Error Occurred
5 Currently in Listen Only Mode
61
$7 \quad 0$

## - Remote device Entered Listen Only Mode

The remote device stores this type of event byte when it enters the Listen Only Mode. The event is defined by a content of 04 hex.

## - Remote device Initiated Communication Restart

The remote device stores this type of event byte when its communications port is restarted. 
Figure 1 shows a flowchart illustrating the communication process for a Modbus server receiving and processing a request. It begins with the entry point 'ENTRY' where the Modbus Server receives the 'mb_req_pdu'. The flowchart then checks if the function code is supported. If 'NO', it leads to 'ExceptionCode = 01' and the server sends 'mb_exception_rsp'. If 'YES', it proceeds to 'Request Processing'. After processing, the flow checks if 'GetCommEventLog == OK'. If 'NO', it leads to 'ExceptionCode = 04' and the server sends 'mb_exception_rsp'. If 'YES', the server sends 'mb_rsp' and exits at 'EXIT'.

The remote device can be restarted by the Diagnostics function (code 08), with sub-function Restart Communications Option (code 00 01).
That function also places the remote device into a 'Continue on Error' or 'Stop on Error' mode. If the remote device is placed into 'Continue on Error' mode, the event byte is added to the existing event log. If the remote device is placed into 'Stop on Error' mode, the byte is added to the log and the rest of the log is cleared to zeros.
The event is defined by a content of zero.
![img-46.jpeg](images/img-46.jpeg.png)

Figure 20: Get Comm Event Log state diagram

# 
Figure 20 shows a state diagram for the 'Get Comm Event Log' function in the Modbus Application Protocol. The diagram is structured with labeled blocks and arrows indicating the flow of data and control. It visually represents the sequence of operations involved in retrieving the communication event log from a Modbus device.

6.11 15 (0x0F) Write Multiple Coils 

This function code is used to force each coil in a sequence of coils to either ON or OFF in a remote device. The Request PDU specifies the coil references to be forced. Coils are addressed starting at zero. Therefore coil numbered 1 is addressed as 0 .
The requested ON/OFF states are specified by contents of the request data field. A logical ' 1 ' in a bit position of the field requests the corresponding output to be ON. A logical ' 0 ' requests it to be OFF.
The normal response returns the function code, starting address, and quantity of coils forced.

## Request PDU

| Function code | 1 Byte | 0x0F |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of Outputs | 2 Bytes | $0 \times 0001$ to $0 \times 07 B 0$ |
| Byte Count | 1 Byte | $\mathbf{N}^{*}$ |
| Outputs Value | $\mathbf{N}^{*} \times 1$ Byte |  |

${ }^{*} \mathbf{N}=$ Quantity of Outputs / 8, if the remainder is different of $0 \Rightarrow \mathrm{~N}=\mathrm{N}+1$

## Response PDU

| Function code | 1 Byte | 0x0F |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of Outputs | 2 Bytes | $0 \times 0001$ to $0 \times 07 B 0$ |

## Error

| Error code | 1 Byte | 0x8F |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to write a series of 10 coils starting at coil 20 :
The request data contents are two bytes: CD 01 hex (1100 110100000001 binary). The binary bits correspond to the outputs in the following way:
Bit:
Output: $\quad 27 \quad 26 \quad 25 \quad 24 \quad 23 \quad 22 \quad 21 \quad 20 \quad-\quad-\quad-\quad-\quad-2928$
The first byte transmitted (CD hex) addresses outputs 27-20, with the least significant bit addressing the lowest output (20) in this set.
The next byte transmitted ( 01 hex) addresses outputs 29-28, with the least significant bit addressing the lowest output (28) in this set. Unused bits in the last data byte should be zerofilled.

| Request |  | Response |  |
| :-- | --: | :-- | --: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 0F | Function | 0F |
| Starting Address Hi | 00 | Starting Address Hi | 00 |
| Starting Address Lo | 13 | Starting Address Lo | 13 |
| Quantity of Outputs Hi | 00 | Quantity of Outputs Hi | 00 |
| Quantity of Outputs Lo | 0A | Quantity of Outputs Lo | 0A |
| Byte Count | 02 |  |  |
| Outputs Value Hi | CD |  |  |
| Outputs Value Lo | 01 |  |  |

![img-47.jpeg](images/img-47.jpeg.png)

Figure 21: Write Multiple Outputs state diagram

# 6.1216 (0x10) Write Multiple registers 


Figure 21 shows a state diagram for the 'Write Multiple Outputs' process in a Modbus server. The diagram begins with an 'ENTRY' point where the MB Server receives the 'mb_req_pdu'. It then checks if the function code is supported, leading to various exception codes if not. If supported, it verifies the quantity of outputs and byte count. The process continues to check starting address validity and whether the write operation is successful, ultimately leading to either a response being sent or an exception.

This function code is used to write a block of contiguous registers (1 to 123 registers) in a remote device.
The requested written values are specified in the request data field. Data is packed as two bytes per register.
The normal response returns the function code, starting address, and quantity of registers written.

## Request

| Function code | 1 Byte | $0 \times 10$ |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of Registers | 2 Bytes | $0 \times 0001$ to $0 \times 007 B$ |
| Byte Count | 1 Byte | $2 \times \mathbf{N}^{*}$ |
| Registers Value | $\mathbf{N}^{*} \times 2$ Bytes | value |

## Response

| Function code | 1 Byte | $0 \times 10$ |
| :-- | :-- | :-- |
| Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity of Registers | 2 Bytes | 1 to 123 (0x7B) |

Error

| Error code | 1 Byte | $0 \times 90$ |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to write two registers starting at 2 to 000 A and 0102 hex:

| Request | Response |  |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 10 | Function | 10 |
| Starting Address Hi | 00 | Starting Address Hi | 00 |
| Starting Address Lo | 01 | Starting Address Lo | 01 |

April 26, 2012
http://www.modbus.org

![img-48.jpeg](images/img-48.jpeg.png)
![img-49.jpeg](images/img-49.jpeg.png)

Figure 22: Write Multiple Registers state diagram

# 6.13 17 (0x11) Report Server ID (Serial Line only) 


Figure 22 shows a state diagram for the 'Write Multiple Registers' function in a Modbus server. The diagram begins with an entry point where the MB Server receives the mb_req_pdu. It includes decision nodes that check if the function code is supported, validate register quantities, starting addresses, and other conditions. Various exception codes (01, 02, 03, 04) are used to handle errors, leading to exception responses. The process concludes with either a successful request processing or an exception response.

This function code is used to read the description of the type, the current status, and other information specific to a remote device.
The format of a normal response is shown in the following example. The data contents are specific to each type of device.

## Request

| Function code | 1 Byte | $0 \times 11$ |
| :-- | :-- | :-- |
| Response |  |  |
| Function code | 1 Byte | $0 \times 11$ |
| Byte Count | 1 Byte |  |
| Server ID | device <br> specific |  |
| Run Indicator Status | 1 Byte | $0 \times 00=$ OFF, $0 \times F F=$ ON |
| Additional Data |  |  |
| Error | 1 Byte | $0 \times 91$ |
|  | 1 Byte | 01 or 04 |

Here is an example of a request to report the ID and status:

| Request | Response |  |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 11 | Function | 11 |
|  |  | Byte Count | Device |
|  |  | Server ID | Specific |
|  |  | Run Indicator Status | 0x00 or 0xFF |
|  |  | Additional Data | Device |
|  |  |  | Specific |

![img-50.jpeg](images/img-50.jpeg.png)

Figure 23: Report server ID state diagram

# 6.1420 (0x14) Read File Record 


Figure 23 shows a state diagram for the 'Report server ID' function in a Modbus application protocol. It includes labeled blocks and decision diamonds that represent the flow of operations. The process begins with the MB Server receiving 'mb_req_pdu'. If the function code is supported, request processing occurs; otherwise, an exception code 01 is issued. If 'ReportSlaveID' is OK, the MB Server sends 'mb_rsp'; otherwise, exception code 04 is issued. The diagram uses arrows to indicate the direction of the process flow and includes entry and exit points.

This function code is used to perform a file record read. All Request Data Lengths are provided in terms of number of bytes and all Record Lengths are provided in terms of registers.
A file is an organization of records. Each file contains 10000 records, addressed 0000 to 9999 decimal or 0X0000 to 0X270F. For example, record 12 is addressed as 12.
The function can read multiple groups of references. The groups can be separating (noncontiguous), but the references within each group must be sequential.
Each group is defined in a separate 'sub-request' field that contains 7 bytes:
The reference type: 1 byte (must be specified as 6 )
The File number: 2 bytes
The starting record number within the file: 2 bytes
The length of the record to be read: 2 bytes.
The quantity of registers to be read, combined with all other fields in the expected response, must not exceed the allowable length of the MODBUS PDU : 253 bytes.
The normal response is a series of 'sub-responses', one for each 'sub-request'. The byte count field is the total combined count of bytes in all 'sub-responses'. In addition, each 'subresponse' contains a field that shows its own byte count.
Request

| Function code | 1 Byte | $0 \times 14$ |
| :-- | :-- | :-- |
| Byte Count | 1 Byte | $0 \times 07$ to $0 \times F 5$ bytes |
| Sub-Req. x, Reference Type | 1 Byte | 06 |
| Sub-Req. x, File Number | 2 Bytes | $0 \times 0001$ to $0 \times F F F F$ |

| Sub-Req. x, Record Number | 2 Bytes | 0x0000 to 0x270F |
| :-- | :-- | :-- |
| Sub-Req. x, Record Length | 2 Bytes | N |
| Sub-Req. $x+1, \ldots$ |  |  |
| Response |  |  |
| Function code | 1 Byte | $0 \times 14$ |
| Resp. data Length | 1 Byte | $0 \times 07$ to $0 \times F 5$ |
| Sub-Req. x, File Resp. length | 1 Byte | $0 \times 07$ to $0 \times F 5$ |
| Sub-Req. x, Reference Type | 1 Byte | 6 |
| Sub-Req. x, Record Data | N $\times 2$ Bytes |  |
| Sub-Req. $x+1$, |  |  |
| Error |  |  |
| Error code | 1 Byte | $0 \times 94$ |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 or |
|  |  | 08 |

While it is allowed for the File Number to be in the range 1 to $0 x F F F F$, it should be noted that interoperability with legacy equipment may be compromised if the File Number is greater than 10 (0x0A).
Here is an example of a request to read two groups of references from remote device:

- Group 1 consists of two registers from file 4, starting at register 1 (address 0001).
- Group 2 consists of two registers from file 3, starting at register 9 (address 0009).

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 14 | Function | 14 |
| Byte Count | 0 E | Resp. Data length | 0 C |
| Sub-Req. 1, Ref. Type | 06 | Sub-Req. 1, File resp. length | 05 |
| Sub-Req. 1, File Number Hi | 00 | Sub-Req. 1, Ref. Type | 06 |
| Sub-Req. 1, File Number Lo | 04 | Sub-Req. 1, Register.Data Hi | 0 D |
| Sub-Req. 1, Record number Hi | 00 | Sub-Req. 1, Register.DataLo | FE |
| Sub-Req. 1, Record number Lo | 01 | Sub-Req. 1, Register.Data Hi | 00 |
| Sub-Req. 1, Record Length Hi | 00 | Sub-Req. 1, Register.DataLo | 20 |
| Sub-Req. 1, Record Length Lo | 02 | Sub-Req. 2, File resp. length | 05 |
| Sub-Req. 2, Ref. Type | 06 | Sub-Req. 2, Ref. Type | 06 |
| Sub-Req. 2, File Number Hi | 00 | Sub-Req. 2, Register.Data H | 33 |
| Sub-Req. 2, File Number Lo | 03 | Sub-Req. 2, Register.DataLo | CD |
| Sub-Req. 2, Record number Hi | 00 | Sub-Req. 2, Register.Data Hi | 00 |
| Sub-Req. 2, Record number Lo | 09 | Sub-Req. 2, Register.DataLo | 40 |
| Sub-Req. 2, Record Length Hi | 00 |  |  |
| Sub-Req. 2, Record Length Lo | 02 |  |  |

![img-51.jpeg](images/img-51.jpeg.png)

Figure 24: Read File Record state diagram

# 6.1521 (0x15) Write File Record 


Figure 24 shows a state diagram for the 'Read File Record' process in a Modbus application protocol. It begins with the MB Server receiving a request and checks if the function code is supported. Depending on the conditions, it may trigger various exception codes (01, 02, 03, 04) or proceed with request processing if all conditions are met. The diagram uses decision blocks and arrows to illustrate the flow of operations, including checks on reference type, file number, record number, and starting address.

This function code is used to perform a file record write. All Request Data Lengths are provided in terms of number of bytes and all Record Lengths are provided in terms of the number of 16-bit words.
A file is an organization of records. Each file contains 10000 records, addressed 0000 to 9999 decimal or 0X0000 to 0X270F. For example, record 12 is addressed as 12.
The function can write multiple groups of references. The groups can be separate, i.e. noncontiguous, but the references within each group must be sequential.
Each group is defined in a separate 'sub-request' field that contains 7 bytes plus the data:
The reference type: 1 byte (must be specified as 6)
The file number: 2 bytes
The starting record number within the file: 2 bytes
The length of the record to be written: 2 bytes
The data to be written: 2 bytes per register.

The quantity of registers to be written, combined with all other fields in the request, must not exceed the allowable length of the MODBUS PDU : 253bytes.
The normal response is an echo of the request.

## Request

| Function code | 1 Byte | $0 \times 15$ |
| :-- | :-- | :-- |
| Request data length | 1 Byte | $0 \times 09$ to $0 \times F B$ |
| Sub-Req. x, Reference Type | 1 Byte | 06 |
| Sub-Req. x, File Number | 2 Bytes | $0 \times 0001$ to $0 \times F F F F$ |
| Sub-Req. x, Record Number | 2 Bytes | $0 \times 0000$ to $0 \times 270 F$ |

April 26, 2012
http://www.modbus.org

| Sub-Req. x, Record length | 2 Bytes | N |
| :-- | :-- | :-- |
| Sub-Req. x, Record data | $\mathbf{N} \times 2$ Bytes |  |
| Sub-Req. $x+1, \ldots$ |  |  |

# Response 

| Function code | 1 Byte | 0x15 |
| :--: | :--: | :--: |
| Response Data length | 1 Byte | 0x09 to 0xFB |
| Sub-Req. x, Reference Type | 1 Byte | 06 |
| Sub-Req. x, File Number | 2 Bytes | 0x0001 to 0xFFFF |
| Sub-Req. x, Record number | 2 Bytes | 0x0000 to 0x270F |
| Sub-Req. x, Record length | 2 Bytes | N |
| Sub-Req. x, Record Data | N $\times 2$ Bytes |  |
| Sub-Req. $x+1, \ldots$ |  |  |

Error

| Error code | 1 Byte | 0x95 |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 or 08 |

While it is allowed for the File Number to be in the range 1 to $0 x F F F F$, it should be noted that interoperability with legacy equipment may be compromised if the File Number is greater than 10 (0x0A).
Here is an example of a request to write one group of references into remote device:

- The group consists of three registers in file 4 , starting at register 7 (address 0007).

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 15 | Function | 15 |
| Request Data length | 0D | Request Data length | 0D |
| Sub-Req. 1, Ref. Type | 06 | Sub-Req. 1, Ref. Type | 06 |
| Sub-Req. 1, File Number Hi | 00 | Sub-Req. 1, File Number Hi | 00 |
| Sub-Req. 1, File Number Lo | 04 | Sub-Req. 1, File Number Lo | 04 |
| Sub-Req. 1, Record number Hi | 00 | Sub-Req. 1, Record number Hi | 00 |
| Sub-Req. 1, Record number Lo | 07 | Sub-Req. 1, Record number Lo | 07 |
| Sub-Req. 1, Record length Hi | 00 | Sub-Req. 1, Record length Hi | 00 |
| Sub-Req. 1, Record length Lo | 03 | Sub-Req. 1, Record length Lo | 03 |
| Sub-Req. 1, Register Data Hi | 06 | Sub-Req. 1, Register Data Hi | 06 |
| Sub-Req. 1, Register Data Lo | AF | Sub-Req. 1, Register Data Lo | AF |
| Sub-Req. 1, Register Data Hi | 04 | Sub-Req. 1, Register Data Hi | 04 |
| Sub-Req. 1, Register Data Lo | BE | Sub-Req. 1, Register Data Lo | BE |
| Sub-Req. 1, Register Data Hi | 10 | Sub-Req. 1, Register Data Hi | 10 |
| Sub-Req. 1, Register Data Lo | 0D | Sub-Req. 1, Register Data Lo | 0D |

![img-52.jpeg](images/img-52.jpeg.png)

Figure 25: Write File Record state diagram

# 6.16 22 (0x16) Mask Write Register 

This function code is used to modify the contents of a specified holding register using a combination of an AND mask, an OR mask, and the register's current contents. The function can be used to set or clear individual bits in the register.
The request specifies the holding register to be written, the data to be used as the AND mask, and the data to be used as the OR mask. Registers are addressed starting at zero. Therefore registers $1-16$ are addressed as $0-15$.
The function's algorithm is:
Result $=$ (Current Contents AND And_Mask) OR (Or_Mask AND (NOT And_Mask))
For example:

|  | Hex | Binary |
| :-- | :-- | :-- |
| Current Contents= | 12 | 00010010 |
| And_Mask = | F2 | 11110010 |
| Or_Mask = | 25 | 00100101 |
| (NOT And_Mask)= | 0D | 00001101 |
| Result = | 17 | 00010111 |

## Note:

- If the Or_Mask value is zero, the result is simply the logical ANDing of the current contents and And_Mask. If the And_Mask value is zero, the result is equal to the Or_Mask value.
- The contents of the register can be read with the Read Holding Registers function (function code 03). They could, however, be changed subsequently as the controller scans its user logic program.
April 26, 2012
http://www.modbus.org

The normal response is an echo of the request. The response is returned after the register has been written.

# Request 

| Function code | 1 Byte | 0x16 |
| :-- | :-- | :-- |
| Reference Address | 2 Bytes | 0x0000 to 0xFFFF |
| And_Mask | 2 Bytes | 0x0000 to 0xFFFF |
| Or_Mask | 2 Bytes | 0x0000 to 0xFFFF |

## Response

| Function code | 1 Byte | 0x16 |
| :-- | :-- | :-- |
| Reference Address | 2 Bytes | 0x0000 to 0xFFFF |
| And_Mask | 2 Bytes | 0x0000 to 0xFFFF |
| Or_Mask | 2 Bytes | 0x0000 to 0xFFFF |

## Error

| Error code | 1 Byte | 0x96 |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |


Figure 26 shows a state diagram for the Mask Write Holding Register process in a Modbus server. The diagram begins with the entry point where the MB Server receives the mb_req_pdu. It checks if the function code is supported, followed by verifying the reference address. Depending on the conditions such as AND_Mask and OR_Mask validity, the process either proceeds to request processing or sends an exception response. The diagram includes decision points for exception codes 01 to 04, determining the flow of operations and responses.

Here is an example of a Mask Write to register 5 in remote device, using the above mask values.

| Request |  | Response |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | $\mathbf{1 6}$ | Function | $\mathbf{1 6}$ |
| Reference address Hi | $\mathbf{0 0}$ | Reference address Hi | $\mathbf{0 0}$ |
| Reference address Lo | $\mathbf{0 4}$ | Reference address Lo | $\mathbf{0 4}$ |
| And_Mask Hi | $\mathbf{0 0}$ | And_Mask Hi | $\mathbf{0 0}$ |
| And_Mask Lo | $\mathbf{F 2}$ | And_Mask Lo | $\mathbf{F 2}$ |
| Or_Mask Hi | $\mathbf{0 0}$ | Or_Mask Hi | $\mathbf{0 0}$ |
| Or_Mask Lo | $\mathbf{2 5}$ | Or_Mask Lo | $\mathbf{2 5}$ |

![img-53.jpeg](images/img-53.jpeg.png)

Figure 26: Mask Write Holding Register state diagram

# 6.17 23 (0x17) Read/Write Multiple registers 

This function code performs a combination of one read operation and one write operation in a single MODBUS transaction. The write operation is performed before the read.
Holding registers are addressed starting at zero. Therefore holding registers 1-16 are addressed in the PDU as $0-15$.
The request specifies the starting address and number of holding registers to be read as well as the starting address, number of holding registers, and the data to be written. The byte count specifies the number of bytes to follow in the write data field.
The normal response contains the data from the group of registers that were read. The byte count field specifies the quantity of bytes to follow in the read data field.

## Request

| Function code | 1 Byte | $0 \times 17$ |
| :-- | :-- | :-- |
| Read Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity to Read | 2 Bytes | $0 \times 0001$ to $0 \times 007 D$ |
| Write Starting Address | 2 Bytes | $0 \times 0000$ to $0 \times F F F F$ |
| Quantity to Write | 2 Bytes | $0 \times 0001$ to $0 \times 0079$ |
| Write Byte Count | 1 Byte | $2 \times \mathbf{N}^{+}$ |
| Write Registers Value | $\mathbf{N}^{+}$x 2 Bytes |  |

${ }^{*} \mathbf{N}=$ Quantity to Write

## Response

| Function code | 1 Byte | $0 \times 17$ |
| :-- | :-- | :-- |
| Byte Count | 1 Byte | $2 \times \mathbf{N}^{+}$ |
| Read Registers value | $\mathbf{N}^{+}$x 2 Bytes |  |

${ }^{*} \mathbf{N}^{+}=$Quantity to Read

## Error

| Error code | 1 Byte | $0 \times 97$ |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of a request to read six registers starting at register 4, and to write three registers starting at register 15:

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 17 | Function | 17 |
| Read Starting Address Hi | 00 | Byte Count | 0 C |
| Read Starting Address Lo | 03 | Read Registers value Hi | 00 |
| Quantity to Read Hi | 00 | Read Registers value Lo | FE |
| Quantity to Read Lo | 06 | Read Registers value Hi | 0 A |
| Write Starting Address Hi | 00 | Read Registers value Lo | CD |
| Write Starting address Lo | 0 E | Read Registers value Hi | 00 |
| Quantity to Write Hi | 00 | Read Registers value Lo | 01 |
| Quantity to Write Lo | 03 | Read Registers value Hi | 00 |
| Write Byte Count | 06 | Read Registers value Lo | 03 |
| Write Registers Value Hi | 00 | Read Registers value Hi | 00 |
| Write Registers Value Lo | FF | Read Registers value Lo | 0 D |
| Write Registers Value Hi | 00 | Read Registers value Hi | 00 |
| Write Registers Value Lo | FF | Read Registers value Lo | FF |
| Write Registers Value Hi | 00 |  |  |
| Write Registers Value Lo | FF |  |  |


Figure 27 shows the Read/Write Multiple Registers state diagram. It illustrates the flow of operations starting from the MB Server receiving a request (mb_req_pdu) and proceeding through various decision points based on function code support and address validity. The diagram includes conditions resulting in different exception codes and the final successful response (mb_rsp) or error response (mb_exception_rsp) sent by the MB Server.

![img-54.jpeg](images/img-54.jpeg.png)

Figure 27: Read/Write Multiple Registers state diagram

# 6.1824 (0x18) Read FIFO Queue 

This function code allows to read the contents of a First-In-First-Out (FIFO) queue of register in a remote device. The function returns a count of the registers in the queue, followed by the queued data. Up to 32 registers can be read: the count, plus up to 31 queued data registers. The queue count register is returned first, followed by the queued data registers.
The function reads the queue contents, but does not clear them.
In a normal response, the byte count shows the quantity of bytes to follow, including the queue count bytes and value register bytes (but not including the error check field).
The queue count is the quantity of data registers in the queue (not including the count register).
If the queue count exceeds 31, an exception response is returned with an error code of 03 (Illegal Data Value).
Request

| Function code | 1 Byte | 0x18 |
| :-- | :-- | :-- |
| FIFO Pointer Address | 2 Bytes | $0 \times 0000$ to $0 x F F F F$ |

## Response

| Function code | 1 Byte | 0x18 |
| :-- | :-- | :-- |
| Byte Count | 2 Bytes |  |
| FIFO Count | 2 Bytes | $\leq 31$ |
| FIFO Value Register | $\mathbf{N}^{\prime} \times 2$ Bytes |  |

Error

| Error code | 1 Byte | 0x98 |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

Here is an example of Read FIFO Queue request to remote device. The request is to read the queue starting at the pointer register 1246 (0x04DE):

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 18 | Function | 18 |
| FIFO Pointer Address Hi | 04 | Byte Count Hi | 00 |
| FIFO Pointer Address Lo | DE | Byte Count Lo | 06 |
|  |  | FIFO Count Hi | 00 |
|  |  | FIFO Count Lo | 02 |
|  |  | FIFO Value Register Hi | 01 |
|  |  | FIFO Value Register Lo | B8 |
|  |  | FIFO Value Register Hi | 12 |
|  |  | FIFO Value Register Lo | 84 |

In this example, the FIFO pointer register (1246 in the request) is returned with a queue count of 2. The two data registers follow the queue count. These are:
1247 (contents 440 decimal -- 0x01B8); and 1248 (contents $4740--0 \times 1284$ ).

![img-55.jpeg](images/img-55.jpeg.png)

Figure 28: Read FIFO Queue state diagram

# 6.19 43 ( 0x2B) Encapsulated Interface Transport 

Informative Note: The user is asked to refer to Annex A (Informative) MODBUS RESERVED FUNCTION CODES, SUBCODES AND MEI TYPES.

Function Code 43 and its MEI Type 14 for Device Identification is one of two Encapsulated Interface Transport currently available in this Specification. The following function codes and MEI Types shall not be part of this published Specification and these function codes and MEI Types are specifically reserved: 43/0-12 and 43/15-255.


Figure 28 shows a flowchart of the Read FIFO Queue state diagram for a Modbus server. It begins with the server receiving a request PDU (Protocol Data Unit) and checks if the function code is supported. If not, it sends an exception response with code 01. If the function code is supported, it verifies if the FIFO pointer address is within the valid range. If not, it sends an exception response with code 02. The flow continues to check the FIFO count, and if it exceeds 31, an exception response with code 03 is sent. If all conditions are met, the server processes the request and checks if the ReadFIFOQueue operation is OK. If not, it sends an exception response with code 04. If successful, the server sends the response PDU.

The MODBUS Encapsulated Interface (MEI)Transport is a mechanism for tunneling service requests and method invocations, as well as their returns, inside MODBUS PDUs.
The primary feature of the MEI Transport is the encapsulation of method invocations or service requests that are part of a defined interface as well as method invocation returns or service responses.

![img-56.jpeg](images/img-56.jpeg.png)

Figure 29: MODBUS encapsulated Interface Transport

Figure 29 shows the MODBUS encapsulated Interface Transport. It includes various components such as the Client Application, Application Interface Backend, Client Interface, Server Interface, and Network Interface. MEI Types X and Y are depicted as part of the encapsulated transport, with MEI Transport (FC 43) linking to the Network Interface.

The Network Interface can be any communication stack used to send MODBUS PDUs, such as TCP/IP, or serial line.
A MEI Type is a MODBUS Assigned Number and therefore will be unique, the value between 0 to 255 are Reserved according to Annex A (Informative) except for MEI Type 13 and MEI Type 14.
The MEI Type is used by MEI Transport implementations to dispatch a method invocation to the indicated interface.
Since the MEI Transport service is interface agnostic, any specific behavior or policy required by the interface must be provided by the interface, e.g. MEI transaction processing, MEI interface error handling, etc.

Request

| Function code | 1 Byte | 0x2B |
| :-- | :-- | :-- |
| MEI Type* | 1 Byte | $0 \times 0 D$ or $0 \times 0 E$ |
| MEI type specific data | n Bytes |  |

* MEI = MODBUS Encapsulated Interface
Response

| Function code | 1 Byte | 0x2B |
| :-- | :-- | :-- |
| MEI Type | 1 byte | echo of MEI Type in <br> Request |
| MEI type specific data | n Bytes |  |

Error

| Function code | 1 Byte | 0xAB : <br> Fe 0x2B + 0x80 |
| :-- | :-- | :-- |
| Exception code | 1 Byte | 01 or 02 or 03 or 04 |

As an example see Read device identification request.

# 6.20 43 / 13 (0x2B / 0x0D) CANopen General Reference Request and Response PDU 

The CANopen General reference Command is an encapsulation of the services that will be used to access (read from or write to) the entries of a CAN-Open Device Object Dictionary as well as controlling and monitoring the CANopen system, and devices.

The MEI Type 13 (0x0D) is a MODBUS Assigned Number licensed to CiA for the CANopen General Reference.

The system is intended to work within the limitations of existing MODBUS networks. Therefore, the information needed to query or modify the object dictionaries in the system is

mapped into the format of a MODBUS message. The PDU will have the 253 Byte limitation in both the Request and the Response message.

Informative: Please refer to Annex B for a reference to a specification that provides information on MEI Type 13.

# 6.2143 / 14 (0x2B / 0x0E) Read Device Identification 

This function code allows reading the identification and additional information relative to the physical and functional description of a remote device, only.
The Read Device Identification interface is modeled as an address space composed of a set of addressable data elements. The data elements are called objects and an object Id identifies them.
The interface consists of 3 categories of objects :

- Basic Device Identification. All objects of this category are mandatory : VendorName, Product code, and revision number.
- Regular Device Identification. In addition to Basic data objects, the device provides additional and optional identification and description data objects. All of the objects of this category are defined in the standard but their implementation is optional .
- Extended Device Identification. In addition to regular data objects, the device provides additional and optional identification and description private data about the physical device itself. All of these data are device dependent.

| Object <br> Id | Object Name / Description | Type | M/O | category |
| :--: | :--: | :--: | :--: | :--: |
| 0x00 | VendorName | ASCII String | Mandatory | Basic |
| 0x01 | ProductCode | ASCII String | Mandatory |  |
| 0x02 | MajorMinorRevision | ASCII String | Mandatory |  |
| 0x03 | VendorUrl | ASCII String | Optional | Regular |
| 0x04 | ProductName | ASCII String | Optional |  |
| 0x05 | ModelName | ASCII String | Optional |  |
| 0x06 | UserApplicationName | ASCII String | Optional |  |
| $\begin{aligned} & 0 \times 07 \\ & 0 \times 7 \mathrm{~F} \end{aligned}$ | Reserved |  | Optional |  |
| $\begin{aligned} & 0 \times 80 \\ & 0 \times F F \end{aligned}$ | Private objects may be optionally defined. The range [0x80 - 0xFF] is Product dependant. | device dependant | Optional | Extended |

Request

| Function code | 1 Byte | 0x2B |
| :--: | :--: | :--: |
| MEI Type* | 1 Byte | 0x0E |
| Read Device ID code | 1 Byte | $01 / 02 / 03 / 04$ |
| Object Id | 1 Byte | 0x00 to 0xFF |

* MEI = MODBUS Encapsulated Interface

|  | Function code | 1 Byte | 0x2B |
| :--: | :--: | :--: | :--: |
|  | MEI Type | 1 byte | 0x0E |
|  | Read Device ID code | 1 Byte | $01 / 02 / 03 / 04$ |
|  | Conformity level | 1 Byte | 0x01 or 0x02 or 0x03 or 0x81 or 0x82 or 0x83 |
|  | More Follows | 1 Byte | 00 / FF |
|  | Next Object Id | 1 Byte | Object ID number |
|  | Number of objects | 1 Byte |  |
|  | List Of |  |  |
|  | Object ID | 1 Byte |  |
|  | Object length | 1 Byte |  |
|  | Object Value | Object length | Depending on the object ID |

Error

| Function code | 1 Byte | 0xAB; <br> Fc 0x2B + 0x80 |
| :-- | :-- | :-- |

# Request parameters description : 

A MODBUS Encapsulated Interface assigned number 14 identifies the Read identification request.
The parameter " Read Device ID code " allows to define four access types :
01: request to get the basic device identification (stream access)
02: request to get the regular device identification (stream access)
03: request to get the extended device identification (stream access)
04: request to get one specific identification object (individual access)
An exception code 03 is sent back in the response if the Read device ID code is illegal.
In case of a response that does not fit into a single response, several transactions (request/response ) must be done. The Object Id byte gives the identification of the first object to obtain. For the first transaction, the client must set the Object Id to 0 to obtain the beginning of the device identification data. For the following transactions, the client must set the Object Id to the value returned by the server in its previous response.
Remark : An object is indivisible, therefore any object must have a size consistent with the size of transaction response.

If the Object Id does not match any known object, the server responds as if object 0 were pointed out (restart at the beginning).
In case of an individual access: ReadDevId code 04, the Object Id in the request gives the identification of the object to obtain, and if the Object Id doesn't match to any known object, the server returns an exception response with exception code $=02$ (Illegal data address).
If the server device is asked for a description level ( readDevice Code )higher that its conformity level, It must respond in accordance with its actual conformity level.

## Response parameter description :

| Function code : | Function code 43 (decimal) 0x2B (hex) |
| :--: | :--: |
| MEI Type | 14 (0x0E) MEI Type assigned number for Device Identification Interface |
| ReadDevId code : | Same as request ReadDevId code : 01, 02, 03 or 04 |
| Conformity Level | Identification conformity level of the device and type of supported access |
|  | 0x01: basic identification (stream access only) |
|  | 0x02: regular identification (stream access only) |
|  | 0x03: extended identification (stream access only) |
|  | 0x81: basic identification (stream access and individual access) |
|  | 0x82: regular identification (stream access and individual access) |
|  | 0x83: extended identification(stream access and individual access) |
| More Follows | In case of ReadDevId codes 01, 02 or 03 (stream access), If the identification data doesn't fit into a single response, several request/response transactions may be required. |
|  | 0x00 : no more Object are available |
|  | 0xFF : other identification Object are available and further |
|  | MODBUS transactions are required |
|  | In case of ReadDevId code 04 (individual access), this field must be set to 00 . |
| Next Object Id | If "MoreFollows = FF", identification of the next Object to be asked for. |
|  | If "MoreFollows = 00", must be set to 00 (useless) |
| Number Of Objects | Number of identification Object returned in the response (for an individual access, Number Of Objects = 1) |
| Object0.ld | Identification of the first Object returned in the PDU (stream access) or the requested Object (individual access) |

Object0.Length
Object0.Value

ObjectN.Id
ObjectN.Length
ObjectN.Value

Length of the first Object in byte
Value of the first Object (Object0.Length bytes)

Identification of the last Object (within the response)
Length of the last Object in byte
Value of the last Object (ObjectN.Length bytes)
Example of a Read Device Identification request for "Basic device identification" : In this example all information are sent in one response PDU.

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | Value | Field Name | Value |
| Function | 2B | Function | 2B |
| MEI Type | 0E | MEI Type | 0E |
| Read Dev Id code | 01 | Read Dev Id Code | 01 |
| Object Id | 00 | Conformity Level | 01 |
|  |  | More Follows | 00 |
|  |  | NextObjectId | 00 |
|  |  | Number Of Objects | 03 |
|  |  | Object Id | 00 |
|  |  | Object Length | 16 |
|  |  | Object Value | "Company identification" |
|  |  | Object Id | 01 |
|  |  | Object Length | 00 |
|  |  | Object Value | "Product code XX" |
|  |  | Object Id | 02 |
|  |  | Object Length | 05 |
|  |  | Object Value | "V2.11" |

In case of a device that required several transactions to send the response the following transactions is intiated.
First transaction :

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | Value | Field Name | Value |
| Function | 2B | Function | 2B |
| MEI Type | 0E | MEI Type | 0E |
| Read Dev Id code | 01 | Read Dev Id Code | 01 |
| Object Id | 00 | Conformity Level | 01 |
|  |  | More Follows | FF |
|  |  | NextObjectId | 02 |
|  |  | Number Of Objects | 03 |
|  |  | Object Id | 00 |
|  |  | Object Length | 16 |
|  |  | Object Value | "Company identification" |
|  |  | Object Id | 01 |
|  |  | Object Length | 1C |
|  |  | Object Value | "Product code <br> $\% \% \% \% \% \% \% \% \% \% \% \% \% \% \% \% \%$ |

Second transaction :

| Request |  | Response |  |
| :--: | :--: | :--: | :--: |
| Field Name | Value | Field Name | Value |
| Function | 2B | Function | 2B |
| MEI Type | 0E | MEI Type | 0E |
| Read Dev Id code | 01 | Read Dev Id Code | 01 |
| Object Id | 02 | Conformity Level | 01 |
|  |  | More Follows | 00 |
|  |  | NextObjectId | 00 |
|  |  | Number Of Objects | 03 |
|  |  | Object Id | 02 |
|  |  | Object Length | 05 |
|  |  | Object Value | "V2.11" |

![img-57.jpeg](images/img-57.jpeg.png)

Figure 30: Read Device Identification state diagram

# 7 MODBUS Exception Responses 

When a client device sends a request to a server device it expects a normal response. One of four possible events can occur from the client's query:

- If the server device receives the request without a communication error, and can handle the query normally, it returns a normal response.
- If the server does not receive the request due to a communication error, no response is returned. The client program will eventually process a timeout condition for the request.
- If the server receives the request, but detects a communication error (parity, LRC, CRC, ...), no response is returned. The client program will eventually process a timeout condition for the request.
- If the server receives the request without a communication error, but cannot handle it (for example, if the request is to read a non-existent output or register), the server will return an exception response informing the client of the nature of the error.

The exception response message has two fields that differentiate it from a normal response:
Function Code Field: In a normal response, the server echoes the function code of the original request in the function code field of the response. All function codes have a mostsignificant bit (MSB) of 0 (their values are all below 80 hexadecimal). In an exception response, the server sets the MSB of the function code to 1 . This makes the function code value in an exception response exactly 80 hexadecimal higher than the value would be for a normal response.
With the function code's MSB set, the client's application program can recognize the exception response and can examine the data field for the exception code.
Data Field: In a normal response, the server may return data or statistics in the data field (any information that was requested in the request). In an exception response, the server returns an exception code in the data field. This defines the server condition that caused the exception.

Example of a client request and server exception response

| Request |  | Response |  |
| :-- | :--: | :-- | :--: |
| Field Name | (Hex) | Field Name | (Hex) |
| Function | 01 | Function | 81 |
| Starting Address Hi | 04 | Exception Code | 02 |
| Starting Address Lo | A1 |  |  |
| Quantity of Outputs Hi | 00 |  |  |
| Quantity of Outputs Lo | 01 |  |  |

In this example, the client addresses a request to server device. The function code (01) is for a Read Output Status operation. It requests the status of the output at address 1185 (04A1 hex). Note that only that one output is to be read, as specified by the number of outputs field (0001).

If the output address is non-existent in the server device, the server will return the exception response with the exception code shown (02). This specifies an illegal data address for the server.

A listing of exception codes begins on the next page.

| MODBUS Exception Codes |  |  |
| :--: | :--: | :--: |
| Code | Name | Meaning |
| 01 | ILLEGAL FUNCTION | The function code received in the query is not an allowable action for the server. This may be because the function code is only applicable to newer devices, and was not implemented in the unit selected. It could also indicate that the server is in the wrong state to process a request of this type, for example because it is unconfigured and is being asked to return register values. |
| 02 | ILLEGAL DATA ADDRESS | The data address received in the query is not an allowable address for the server. More specifically, the combination of reference number and transfer length is invalid. For a controller with 100 registers, the PDU addresses the first register as 0 , and the last one as 99 . If a request is submitted with a starting register address of 96 and a quantity of registers of 4 , then this request will successfully operate (address-wise at least) on registers $96,97,98,99$. If a request is submitted with a starting register address of 96 and a quantity of registers of 5 , then this request will fail with Exception Code $0 \times 02$ "Illegal Data Address" since it attempts to operate on registers $96,97,98,99$ and 100, and there is no register with address 100 . |
| 03 | ILLEGAL DATA VALUE | A value contained in the query data field is not an allowable value for server. This indicates a fault in the structure of the remainder of a complex request, such as that the implied length is incorrect. It specifically does NOT mean that a data item submitted for storage in a register has a value outside the expectation of the application program, since the MODBUS protocol is unaware of the significance of any particular value of any particular register. |
| 04 | SERVER DEVICE FAILURE | An unrecoverable error occurred while the server was attempting to perform the requested action. |
| 05 | ACKNOWLEDGE | Specialized use in conjunction with programming commands. <br> The server has accepted the request and is processing it, but a long duration of time will be required to do so. This response is returned to prevent a timeout error from occurring in the client. The client can next issue a Poll Program Complete message to determine if processing is completed. |
| 06 | SERVER DEVICE BUSY | Specialized use in conjunction with programming commands. <br> The server is engaged in processing a longduration program command. The client should retransmit the message later when the server is free. |
| 08 | MEMORY PARITY ERROR | Specialized use in conjunction with function codes 20 and 21 and reference type 6 , to indicate that the extended file area failed to pass a consistency check. <br> The server attempted to read record file, but detected a parity error in the memory. The client can retry the request, but service may be required |

|  |  | on the server device. |
| :--: | :--: | :--: |
| 0A | GATEWAY PATH UNAVAILABLE | Specialized use in conjunction with gateways, indicates that the gateway was unable to allocate an internal communication path from the input port to the output port for processing the request. Usually means that the gateway is misconfigured or overloaded. |
| 0B | GATEWAY TARGET DEVICE <br> FAILED TO RESPOND | Specialized use in conjunction with gateways, indicates that no response was obtained from the target device. Usually means that the device is not present on the network. |

# Annex A (Informative): MODBUS RESERVED FUNCTION CODES, SUBCODES AND MEI TYPES 

The following function codes and subcodes shall not be part of this published Specification and these function codes and subcodes are specifically reserved. The format is function code/subcode or just function code where all the subcodes (0-255) are reserved: 8/19; 8/21$65535,9,10,13,14,41,42,90,91,125,126$ and 127.

Function Code 43 and its MEI Type 14 for Device Identification and MEI Type 13 for CANopen General Reference Request and Response PDU are the currently available Encapsulated Interface Transports in this Specification.

The following function codes and MEI Types shall not be part of this published Specification and these function codes and MEI Types are specifically reserved: 43/0-12 and 43/15-255. In this Specification, a User Defined Function code having the same or similar result as the Encapsulated Interface Transport is not supported.

MODBUS is a registered trademark of Schneider Automation Inc.

## Annex B (Informative): CANOPEN GENERAL REFERENCE COMMAND

Please refer to the MODBUS website or the CiA (CAN in Automation) website for a copy and terms of use that cover Function Code 43 MEI Type 13.

MODBUS MESSAGING ON TCP/IP IMPLEMENTATION GUIDE V1.0b
CONTENTS
1 INTRODUCTION ..... 2
1.1 OBJECTIVES ..... 2
1.2 CLIENT / SERVER MODEL ..... 2
1.3 REFERENCE DOCUMENTS ..... 3
2 ABBREVIATIONS ..... 3
3 CONTEXT ..... 3
3.1 PROTOCOL DESCRIPTION ..... 3
3.1.1 General communication architecture ..... 3
3.1.2 MODBUS On TCP/IP Application Data Unit ..... 4
3.1.3 MBAP Header description ..... 5
3.2 MODBUS FUNCTIONS CODES DESCRIPTION ..... 6
4 FUNCTIONAL DESCRIPTION ..... 7
4.1 MODBUS COMPONENT ARCHITECTURE MODEL ..... 7
4.2 TCP CONNECTION MANAGEMENT ..... 10
4.2.1 Connections management Module ..... 10
4.2.2 Impact of Operating Modes on the TCP Connection ..... 13
4.2.3 Access Control Module ..... 14
4.3 USE of TCP/IP STACK ..... 14
4.3.1 Use of BSD Socket interface ..... 15
4.3.2 TCP layer parameterization ..... 18
4.3.3 IP layer parameterization ..... 19
4.4 COMMUNICATION APPLICATION LAYER ..... 20
4.4.1 MODBUS Client ..... 20
4.4.2 MODBUS Server ..... 26
5 IMPLEMENTATION GUIDELINE ..... 32
5.1 OBJECT MODEL DIAGRAM ..... 32
5.1.1 TCP management package ..... 33
5.1.2 Configuration layer package ..... 35
5.1.3 Communication layer package ..... 36
5.1.4 Interface classes ..... 37
5.2 IMPLEMENTATION CLASS DIAGRAM ..... 37
5.3 SEQUENCE DIAGRAMS ..... 39
5.4 CLASSES AND METHODS DESCRIPTION ..... 42
5.4.1 MODBUS Server Class ..... 42
5.4.2 MODBUS Client Class ..... 43
5.4.3 Interface Classes ..... 44
5.4.4 Connexion Management class ..... 45

# 1 INTRODUCTION 

### 1.1 OBJECTIVES

The objective of this document is to present the MODBUS messaging service over TCP/IP, in order to provide reference information that helps software developers to implement this service. The encoding of the MODBUS function codes is not described in this document, for this information please read the MODBUS Application Protocol Specification [1].

This document gives accurate and comprehensive description of a MODBUS messaging service implementation. Its purpose is to facilitate the interoperability between the devices using the MODBUS messaging service.

This document comprises mainly three parts:

- An overview of the MODBUS over TCP/IP protocol
- A functional description of a MODBUS client, server and gateway implementation.
- An implementation guideline that proposes the object model of an MODBUS implementation example.


### 1.2 CLIENT / SERVER MODEL

The MODBUS messaging service provides a Client/Server communication between devices connected on an Ethernet TCP/IP network.
This client / server model is based on four type of messages:

- MODBUS Request,
- MODBUS Confirmation,
- MODBUS Indication,
- MODBUS Response

| MODBUS Client | Request | Indication | MODBUS Server |
| :--: | :--: | :--: | :--: |
|  | Confirmation | Response |  |
|  |  |  |  |


Figure 1 shows a diagram of the MODBUS Client/Server model. It illustrates the communication process between a MODBUS Client and a MODBUS Server. The diagram includes labeled arrows indicating the flow of messages: 'Request' and 'Indication' from the Client to the Server, and 'Confirmation' and 'Response' from the Server back to the Client.

A MODBUS Request is the message sent on the network by the Client to initiate a transaction,

A MODBUS Indication is the Request message received on the Server side,
A MODBUS Response is the Response message sent by the Server,
A MODBUS Confirmation is the Response Message received on the Client side
The MODBUS messaging services (Client / Server Model) are used for real time information exchange:

- between two device applications,
- between device application and other device,
- between HMI/SCADA applications and devices,
- between a PC and a device program providing on line services.

# 1.3 REFERENCE DOCUMENTS 

This section gives a list of documents that are interesting to read before this one:
[1] MODBUS Application Protocol Specification V1.1a.
[2] RFC 1122 Requirements for Internet Hosts -- Communication Layers

## 2 ABBREVIATIONS

ADU Application Data Unit
IETF Internet Engineering Task Force
IP Internet Protocol
MAC Medium Access Control
MB MODBUS
MBAP MODBUS Application Protocol
PDU Protocol Data Unit
PLC Programmable Logic Controller
TCP Transport Control Protocol
BSD Berkeley Software Distribution
MSL Maximum Segment Lifetime

## 3 CONTEXT

### 3.1 PROTOCOL DESCRIPTION

### 3.1.1 General communication architecture

A communicating system over MODBUS TCP/IP may include different types of device:

- A MODBUS TCP/IP Client and Server devices connected to a TCP/IP network
- The Interconnection devices like bridge, router or gateway for interconnection between the TCP/IP network and a serial line sub-network which permit connections of MODBUS Serial line Client and Server end devices.

![img-58.jpeg](images/img-58.jpeg.png)

Figure 1: MODBUS TCP/IP communication architecture


Figure 1 shows the MODBUS TCP/IP communication architecture. It includes various components such as MODBUS S Client TCP/IP, MODBUS S Server TCP/IP, Client TCP/IP, Server TCP/IP gateway, and MODBUS Client and Server Serial Line. The diagram illustrates the interconnection of these components over a network, with lines representing the data flow and communication pathways.

The MODBUS protocol defines a simple Protocol Data Unit (PDU) independent of the underlying communication layers. The mapping of MODBUS protocol on specific buses or networks can introduce some additional fields on the Application Data Unit (ADU).
![img-59.jpeg](images/img-59.jpeg.png)

Figure 2: General MODBUS frame


Figure 2 shows a general MODBUS frame. It consists of an Application Data Unit (ADU) which includes Additional address, Function code, Data, and Error check components, illustrating the structure of a typical MODBUS message.

The client that initiates a MODBUS transaction builds the MODBUS Application Data Unit. The function code indicates to the server which kind of action to perform.

# 3.1.2 MODBUS On TCP/IP Application Data Unit 

This section describes the encapsulation of a MODBUS request or response when it is carried on a MODBUS TCP/IP network.
![img-60.jpeg](images/img-60.jpeg.png)

Figure 3: MODBUS request/response over TCP/IP

Figure 3 shows a MODBUS request/response over TCP/IP. It includes a MODBUS TCP/IP ADU with an MBAP Header, Function code, and Data, demonstrating the encapsulation of a MODBUS request or response in a TCP/IP network.

A dedicated header is used on TCP/IP to identify the MODBUS Application Data Unit. It is called the MBAP header (MODBUS Application Protocol header).

This header provides some differences compared to the MODBUS RTU application data unit used on serial line:

- The MODBUS 'slave address' field usually used on MODBUS Serial Line is replaced by a single byte 'Unit Identifier' within the MBAP Header. The 'Unit Identifier' is used to communicate via devices such as bridges, routers and gateways that use a single IP address to support multiple independent MODBUS end units.
- All MODBUS requests and responses are designed in such a way that the recipient can verify that a message is finished. For function codes where the MODBUS PDU has a fixed length, the function code alone is sufficient. For function codes carrying a variable amount of data in the request or response, the data field includes a byte count.
- When MODBUS is carried over TCP, additional length information is carried in the MBAP header to allow the recipient to recognize message boundaries even if the message has been split into multiple packets for transmission. The existence of explicit and implicit length rules, and use of a CRC-32 error check code (on Ethernet) results in an infinitesimal chance of undetected corruption to a request or response message.


# 3.1.3 MBAP Header description 

The MBAP Header contains the following fields:

| Fields | Length | Description - | Client | Server |
| :-- | :-- | :-- | :-- | :-- |
| Transaction <br> Identifier | 2 Bytes | Identification of a <br> MODBUS Request / <br> Response transaction. | Initialized by the <br> client | Recopied by the <br> server from the <br> received <br> request |
| Protocol Identifier | 2 Bytes | $0=$ MODBUS protocol | Initialized by the <br> client | Recopied by the <br> server from the <br> received <br> request |
| Length | 2 Bytes | Number of following <br> bytes | Initialized by the <br> client ( request) | Initialized by <br> the server ( <br> Response) |
| Unit Identifier | 1 Byte | Identification of a <br> remote slave <br> connected on a serial <br> line or on other buses. | Initialized by the <br> client | Recopied by the <br> server from the <br> received <br> request |

The header is 7 bytes long:

- Transaction Identifier - It is used for transaction pairing, the MODBUS server copies in the response the transaction identifier of the request.
- Protocol Identifier - It is used for intra-system multiplexing. The MODBUS protocol is identified by the value 0 .
- Length - The length field is a byte count of the following fields, including the Unit Identifier and data fields.

- Unit Identifier - This field is used for intra-system routing purpose. It is typically used to communicate to a MODBUS+ or a MODBUS serial line slave through agateway between an Ethernet TCP-IP network and a MODBUS serial line. This field is set by the MODBUS Client in the request and must be returned with the same value in the response by the server.

All MODBUS/TCP ADU are sent via TCP to registered port 502.
Remark : the different fields are encoded in Big-endian.

# 3.2 MODBUS FUNCTIONS CODES DESCRIPTION 

Standard function codes used on MODBUS application layer protocol are described in details in the MODBUS Application Protocol Specification [1].

# 4 FUNCTIONAL DESCRIPTION 

The MODBUS Component Architecture presented here is a general model including both MODBUS Client and Server Components and usable on any device.

Some devices may only provide the server or the client component.
In the first part of this section a brief overview of the MODBUS messaging service component architecture is given, followed by a description of each component presented in the architectural model.

### 4.1 MODBUS COMPONENT ARCHITECTURE MODEL

![img-61.jpeg](images/img-61.jpeg.png)

Figure 4: MODBUS Messaging Service Conceptual Architecture

## - Communication Application Layer


Figure 4 shows the MODBUS Messaging Service Conceptual Architecture. It depicts a layered architecture model with several components including the User Application, Communication Application Layer, TCP Management, and TCP/IP Stack. The diagram illustrates the interactions between these components with labeled arrows indicating data flow and control, such as between the Modbus Client and Server, and interfaces like the Modbus Client Interface and Modbus Backend Interface.

A MODBUS device may provide a client and/or a server MODBUS interface.
A MODBUS backend interface can be provided allowing indirectly the access to user application objects.
Four areas can compose this interface: input discrete, output discrete (coils), input registers and output registers. A pre-mapping between this interface and the user application data has to be done (local issue).

| Primary tables | Object type | Type of | Comments |
| :-- | :-- | :-- | :-- |
| Discretes Input | Single bit | Read-Only | This type of data can be provided by an I/O system. |
| Coils | Single bit | Read-Write | This type of data can be alterable by an application <br> program. |
| Input Registers | 16-bit word | Read-Only | This type of data can be provided by an I/O system |
| Holding Registers | 16-bit word | Read-Write | This type of data can be alterable by an application <br> program. |

![img-62.jpeg](images/img-62.jpeg.png)

Figure 5 MODBUS Data Model with separate blocks
![img-63.jpeg](images/img-63.jpeg.png)

Figure 6 MODBUS Data Model with only 1 block

# $>$ MODBUS Client 


Figure 5 shows a MODBUS data model with separate blocks. It illustrates a MODBUS server device where the device application memory is divided into separate sections for Input Discrete, Coils, Input Registers, and Output Registers. The MODBUS access arrows indicate data flow into and out of each section, with a MODBUS Request pointing towards the memory blocks.


Figure 6 shows a MODBUS data model with only one block. This diagram represents a MODBUS server device where the device application memory is consolidated into a single block containing Input Discrete, Coils, Input Registers, and Output Registers. Arrows labeled 'R' and 'W' indicate read and write operations, respectively, with a MODBUS Request pointing towards the memory block.

The MODBUS Client allows the user application to explicitly control information exchange with a remote device. The MODBUS Client builds a MODBUS request from parameter contained in a demand sent by the user application to the MODBUS Client Interface.
The MODBUS Client uses a MODBUS transaction whose management includes waiting for and processing of a MODBUS confirmation.

## $>$ MODBUS Client Interface

The MODBUS Client Interface provides an interface enabling the user application to build the requests for various MODBUS services including access to MODBUS application objects. The MODBUS Client interface (API) is not part of this Specification, although an example is described in the implementation model.

## $>$ MODBUS Server

On reception of a MODBUS request this module activates a local action to read, to write or to achieve some other actions. The processing of these actions is done totally transparently for the application programmer. The main MODBUS server functions are to wait for a MODBUS request on 502 TCP port, to treat this request and then to build a MODBUS response depending on device context.

## $>$ MODBUS Backend Interface

The MODBUS Backend Interface is an interface from the MODBUS Server to the user application in which the application objects are defined.

Informative Note: The Backend Interface is not defined in this Specification October 24, 2006
http://www.Modbus.org

# - TCP Management layer 

Informative Note: The TCP/IP discussion in this Specification is based in part upon reference [2] RFC 1122 to assist the user in implementing the MODBUS Application Protocol Specification [1] over TCP/IP.

One of the main functions of the messaging service is to manage communication establishment and ending and to manage the data flow on established TCP connections.

## $>$ Connection Management

A communication between a client and server MODBUS Module requires the use of a TCP connection management module. It is in charge to manage globally messaging TCP connections.

Two possibilities are proposed for the connection management. Either the user application itself manages TCP connections or the connection management is totally done by this module and therefore it is transparent for the user application. The last solution implies less flexibility.

The listening TCP port 502 is reserved for MODBUS communications. It is mandatory to listen by default on that port. However, some markets or applications might require that another port is dedicated to MODBUS over TCP. For that reason, it is highly recommended that the clients and the servers give the possibility to the user to parameterize the MODBUS over TCP port number. It is important to note that even if another TCP server port is configured for MODBUS service in certain applications, TCP server port 502 must still be available in addition to any application specific ports.

## $>$ Access Control Module

In certain critical contexts, accessibility to internal data of devices must be forbidden for undesirable hosts. That's why a security mode is needed and security process may be implemented if required.

## - TCP/IP Stack layer

The TCP/IP stack can be parameterized in order to adapt the data flow control, the address management and the connection management to different constraints specific to a product or to a system. Generally the BSD socket interface is used to manage the TCP connections.

## -Resource management and Data flow control

In order to equilibrate inbound and outbound messaging data flow between the MODBUS client and the server, data flow control mechanism is provided in all layers of MODBUS messaging stack.
The resource management and flow control module is first based on TCP internal flow control added with some data flow control in the data link layer and also in the user application level.

# 4.2 TCP CONNECTION MANAGEMENT 

### 4.2.1 Connections management Module

### 4.2.1.1 General description

A MODBUS communication requires the establishment of a TCP connection between a Client and a Server.
The establishment of the connection can be activated either explicitly by the User Application module or automatically by the TCP connection management module.
In the first case an application-programming interface has to be provided in the user application module to manage completely the connection. This solution provides flexibility for the application programmer but it requires a good expertise on TCP/IP mechanism.
In the second case the TCP connection management is completely hidden to the user application that only sends and receives MODBUS messages. The TCP connection management module is in charge to establish a new TCP connection when it is required.
The definition of the number of TCP client and server connections is not on the scope of this document (value n in this document). Depending on the device capacities the number of TCP connections can be different.

## Implementation Rules :

1) Without explicit user requirement, it is recommended to implement the automatic TCP connection management
2) It is recommended to keep the TCP connection opened with a remote device and not to open and close it for each MODBUS/TCP transaction, Remark: However the MODBUS client must be capable of accepting a close request from the server and closing the connection. The connection can be reopened when required.
3) It is recommended for a MODBUS Client to open a minimum of TCP connections with a remote MODBUS server (with the same IP address). One connection per application could be a good choice.
4) Several MODBUS transactions can be activated simultaneously on the same TCP Connection.
Remark: If this is done then the MODBUS transaction identifier must be used to uniquely identify the matching requests and responses.
5) In case of a bi-directional communication between two remote MODBUS entities ( each of them is client and server), it is necessary to open separate connections for the client data flow and for the server data flow.
6) A TCP frame must transport only one MODBUS ADU. It is advised against sending multiple MODBUS requests or responses on the same TCP PDU

![img-64.jpeg](images/img-64.jpeg.png)

Figure 7: TCP connection management activity diagram

# 1. Explicit TCP connection management 


Figure 7 shows a TCP connection management activity diagram. It illustrates the process flow for managing TCP connections between a client and a server in a Modbus communication system. The diagram is divided into two main sections: 'Client' and 'Server'. The client side includes states such as 'Idle', 'Wait', 'Active_Connection', and transitions like 'Connection_establishment'. The server side involves events like 'Event on a socket', 'Connection_accepted', and 'Request_treatment'. Decision points are represented with diamond shapes, indicating conditions such as '[n connections]' and '[IP authorized]'. The flow of activities is shown with arrows connecting various states and decisions.

The user application module is in charge of managing all the TCP connections: active and passive establishment, connection ending, etc. This management is done for all MODBUS communication between a client and a server. The BSD Socket interface is used in the user application module to manage the TCP connection. This solution offers a total flexibility but it implies that the application programmer has sufficient TCP knowledge.
A limit of number of client and server connections has to be configured taking into account the device capabilities and requirement.

## 2. Automatic TCP connection management

The TCP connection management is totally transparent for the user application module. The connection management module may accept a sufficient number of client and server connections.
Nevertheless a mechanism must be implemented in case of exceeding the number of authorized connection. In such a case we recommend to close the oldest unused connection.
A connection with a remote partner is established at the first packet received from a remote client or from the local user application. This connection will be closed if a termination arrived from the network or decided locally on the device. On reception of a connection request, the access control option can be used to forbid device accessibility to unauthorized clients.
October 24, 2006
http://www.Modbus.org

The TCP connection management module uses the Stack interface (usually BSD Socket interface) to communicate with the TCP/IP stack.

In order to maintain compatibility between system requirements and server resources, the TCP management will maintain 2 pools of connection.

- The first pool ( priority connection pool) is made of connections that are never closed on a local initiative. A configuration must be provided to set this pool up. The principle to be implemented is to associate a specific IP address with each possible connection of this pool. The devices with such IP addresses are said to be "marked". Any new connection that is requested by a marked device must be accepted, and will be taken from the priority connection pool. It is also necessary to configure the maximum number of Connections allowed for each remote device to avoid that the same device uses all the connections of the priority pool.
- The second pool (non-priority connection pool) contains connections for non marked devices. The rule that takes over here is to close the oldest connection when a new connection request arrives from a non-marked device and when there is no more connection available in the pool.

A configuration might be optionally provided to assign the number of connections available in each pool. However (It is not mandatory) the designers can set the number of connections at design time if required.

# 4.2.1.2 Connection management description 

## - Connection establishment :

The MODBUS messaging service must provide a listening socket on Port 502, which permits to accept new connection and to exchange data with other devices.
When the messaging service needs to exchange data with a remote server, it must open a new client connection with a remote Port 502 in order to exchange data with this distant. The local port must be higher than 1024 and different for each client connection.
![img-65.jpeg](images/img-65.jpeg.png)

Figure 8: MODBUS TCP connection establishment


Figure 8 shows the MODBUS TCP connection establishment. It illustrates two devices, each with a client and server port configuration. The left device, labeled as Device@ IP1, has client ports numbered n (>1024) and a server port at 502. The right device, labeled as Device@ IP2, mirrors this setup. A connection is depicted between the client port n on Device@ IP1 and the server port 502 on Device@ IP2, representing a typical communication setup in MODBUS TCP.

If the number of client and server connections is greater than the number of authorized connections the oldest unused connection is closed. The access control mechanism can be activated to check if the IP address of the remote client is authorized. If not the new connection is refused.

# - MODBUS data transfer 

A MODBUS request has to be sent on the right TCP connection already opened. The IP address of the remote is used to find the TCP connection. In case of multiple TCP connections opened with the same remote, one connection has to be chosen to send the MODBUS message, different choice criteria can be used like the oldest one, the first one. The connection has to maintain open during all the MODBUS communications. As described in the following sections a client can initiate several MODBUS transactions with a server without waiting the ending of the previous one.

## - Connection closing

When the MODBUS communications are ended between a Client and a Server, the client has to initiate a connection closing of the connection used for these communications.

### 4.2.2 Impact of Operating Modes on the TCP Connection

Some Operating Modes (communication break between two operational End Points, Crash and Reboot on one of the End Point, ...) may have impacts on the TCP Connections. A connection can be seen closed or aborted on one side without the knowledge of the other side. The connection is said to be "half-open".
This section describes the behavior for each main Operating Modes. It is assumed that the Keep Alive TCP mechanism is used on both end points (See section 4.3.2)

### 4.2.2.1 Communication break between two operational end points:

The origin of the communication break can be the disconnection of the Ethernet cable on the Server side. The expected behavior is:

- If no packet is currently sent on the connection:

The communication break will not be seen if it lasts less than the Keep Alive timer value. If the communication break lasts more than the Keep Alive timer value, an error is returned to the TCP Management layer that can reset the connection.

- If Some packets are sent before and after the disconnection:

The TCP retransmission algorithms (Jacobson's, Karn's algorithms and exponential backoff. See section 4.3.2) are activated. This may lead to a stack TCP layer Reset of the Connection before the Keep Alive timer is over.

### 4.2.2.2 Crash and Reboot of the Server end point

After the crash and Reboot of the Server, the connection is "half-open" on Client side. The expected behavior is:

- If no packet is sent on the half-open connection:

The TCP half-open connection is seen opened from the Client side as long as the Keep Alive timer is not over. After that an error is returned to the TCP Management layer that can reset the connection.

- If some packets are sent on the half-open connection:

The Server receives data on a connection that doesn't exist anymore. The stack TCP layer sends a Reset to close the half-open connection on the Client side

### 4.2.2.3 Crash and Reboot of the Client

After the crash and Reboot of the Client, the connection is "half-open" on Server side. The expected behavior is:

- No packet is sent on the half-open connection:

The TCP half-open connection is seen opened from the Server side as long as the Keep Alive timer is not over. After that an error is returned to the TCP Management layer that can reset the connection.

- If the Client opens a new connection before the Keep Alive timer is over :

Two cases have to be studied:

- The connection opening has the same characteristics as the half-open connection on the server side (same source and destination Ports, same source and destination IP Addresses), therefore the connection opening will fail at the TCP stack level after the Time-Out on Connection Establishment (75s on most of Berkeley implementations). To avoid this long Time-Out during which it is not possible to communicate, it is advised to ensure that different source port numbers than the previous one are used for a connection opening after a reboot on the client side.
- The connection opening has not the same characteristics as the half-open connection on the server side (different source Ports, same destination Port, same source and destination IP Address ), therefore the connection is opened at the stack TCP level and signaled to the Server TCP Management layer.
If the Server TCP Management layer only supports one connection from a remote Client IP Address, it can close the old half-opened connection and use the new one.
If the Server TCP Management layer supports several connections from a remote Client IP Address, the new connection stays opened and the old one also stays half-opened until the expiration of the Keep Alive Timer that will return an error to the TCP Management layer. After that the TCP Management layer will be able to Reset the old connection.


# 4.2.3 Access Control Module 

The goal of this module is to check every new connection and using a list of authorized remote IP addresses the module can authorize or forbid a remote Client TCP connection.

In critical context the application programmer needs to choose the Access Control mode in order to secure its network access. In such a case he needs to Authorize/forbid access for each remote @IP. The user needs to provide a list of IP addresses and to specify for each IP address if it's authorized or not. By default, on security mode, the IP addresses not configured by the user are forbidden. Therefore with the access control mode a connection coming from an unknown IP address is closed.

### 4.3 USE of TCP/IP STACK

A TCP/IP stack provides an interface to manage connections, to send and receive data, and also to do some parameterizations in order to adapt the stack behavior to the device or system constraints.

![img-66.jpeg](images/img-66.jpeg.png)

The goal of this section is to give an overview of the Stack interface and also some information concerning the parameterization of the stack. This overview focuses on the features used by the MODBUS Messaging.


Figure 1 shows a layered protocol stack diagram for MODBUS messaging over TCP/IP. It illustrates the different layers involved, starting from the bottom with Network Access, Ethernet II, and 802.3 layers, moving up through ARP, IP, ICMP, TCP, Modbus, and finally to the application layer labeled as 'Msg'. Each layer is represented as a block stacked vertically, demonstrating the hierarchy and interaction between layers in the MODBUS communication stack.

For more information, the advice is to read the RFC 1122 that provides guidance for vendors and designers of Internet communication software. It enumerates standard protocols that a host connected to the Internet must use as well as an explicit set of requirements and options.
The stack interface is generally based on the BSD (Berkeley Software Distribution) Interface that is described in this document.

# 4.3.1 Use of BSD Socket interface 

Remark : some TCP/IP stacks propose other types of interfaces for performance issues. A MODBUS client or server can use these specific interfaces, but this use will be not described in this specification.

A socket is an endpoint of communication. It is the basic building block for communication. A MODBUS communication is executed by sending and receiving data through sockets. The TCPIP library provides only stream sockets using TCP and providing a connection-based communication service.
The Sockets are created via the socket () function. A socket number is returned, which is then used by the creator to access the socket. Sockets are created without addresses (IP address and port number). Until a port is bound to a socket, it cannot be used to receive data.
The bind () function is used to bind a port number to a socket. The bind () creates an association between the socket and the port number specified.
In order to initiate a connection, the client must issue the connect () function specifying the socket number, the remote IP address and the remote listening port number (active connection establishment).
In order to complete a connection, the server must issue the accept () function specifying the socket number that was specified in the prior listen () call (passive connection establishment). A new socket is created with the same properties as the initial one. This new socket is connected to the client's socket, and its number is returned to the server. The initial socket is thereby free for other clients that might want to connect with the server.

After the establishment of the TCP connection the data can be transferred. The send() and recv() functions are designed specifically to be used with sockets that are already connected.

The setsockopt () function allows a socket's creator to associate options with a socket. These options modify the behavior of the socket. The description of these options is given in the section 4.3.2.

The select () function allows the programmer to test events on all sockets.

The shutdown () function allows a socket user to disable send () and/or receive () on the socket.

Once a socket is no longer needed, its socket descriptor can be discarded by using the close () function.

Figure 39: MODBUS Exchanges describes a full MODBUS communication between a client and a s server. The Client establishes the connection and sends 3 MODBUS requests to the server without waiting the response of the first one. After receiving all the responses the Client closes the connection properly.

![img-67.jpeg](images/img-67.jpeg.png)

Figure 9: MODBUS Exchanges

# 4.3.2 TCP layer parameterization 

Some parameters of the TCP/IP stack can be adjusted to adapt its behavior to the product or system constraints. The following parameters can be adjusted in the TCP layer:

## - Parameters for each connection:

## SO-RCVBUF, SO-SNDBUF:

These parameters allow setting the high water mark for the Send and the Receive Socket. They can be adjusted for flow control management. The size of the received buffer is the maximum size advertised window for that connection. Socket buffer sizes must be increased in order to increase performances. Nevertheless these values must be smaller than internal driver resources in order to close the TCP window before exhausting internal driver resources.

The received buffer size depends on the TCP Windows size, the TCP Maximum segment size and the time needed to absorb the incoming frames. With a Maximum Segment Size of 300 bytes (a MODBUS request needs a maximum of 256 bytes + the MBAP header size), if we need 3 frames buffering, the socket buffer size value can be adjusted to 900 bytes. For biggest needs and best-scheduled time, the size of the TCP window may be increased.

## TCP-NODELAY:

Small packets (called tinygrams) are normally not a problem on LANs, since most LANs are not congested, but these tinygrams can lead to congestion on wide area networks. A simple solution, called the "NAGLE algorithm", is to collect small amounts of data and sends them in a single segment when TCP acknowledgments of previous packets arrive.
In order to have better real-time behavior it is recommended to send small amounts of data directly without trying to gather them in a single segment. That is why it is recommended to force the TCP-NODELAY option that disables the "NAGLE algorithm" on client and server connections.

## SO-REUSEADDR:

When a MODBUS server closes a TCP connection initialized by a remote client, the local port number used for this connection cannot be reused for a new opening while that connection stays in the "Time-wait" state (during two MSL : Maximum Segment Lifetime).

It is recommended specifying the SO-REUSEADDR option for each client and server connection to bypass this restriction. This option allows the process to assign itself a port number that is part of a connection that is in the 2 MSL wait for client and listening socket.

## SO-KEEPALIVE:

By default on TCP/IP protocol no data are sent across an idle TCP connection. Therefore if no process at the ends of a TCP connection is sending data to the other, nothing is exchanged between the two TCP modules. This assumes that either the client application or the server application uses timers to detect inactivity in order to close a connection.
It is recommended to enable the KEEPALIVE option on both client and server connection in order to poll the other end to know if the distant has either crashed and is down or crashed and rebooted.
Nevertheless we must keep on mind that enabling KEEPALIVE can cause perfectly good connections to be dropped during transient failures, that it consumes unnecessary bandwidth on the network if the keep alive timer is too short.

# - Parameters for the whole TCP layer: 

## Time Out on establishing a TCP Connection:

Most Berkeley-derived systems set a time limit of 75 seconds on the establishment of a new connection, this default value should be adapted to the real time constraint of the application.

## Keep Alive parameters:

The default idle time for a connection is 2 hours. Idles times in excess of this value trigger a keep alive probe. After the first keep alive probe, a probe is sent every 75 seconds for a maximum number of times unless a probe response is received.
The maximum number of keep Alive probes sent out on an idle connection is 8 . If no probe response is received after sending out the maximum number of keep Alive probes, TCP signals an error to the application that can decide to close the connection

## Time-out and retransmission parameters:

A TCP packet is retransmitted if its loss has been detected. One way to detect the loss is to manage a Retransmission Time-Out (RTO) that expires if no acknowledgement has been received from the remote side.
TCP manages a dynamic estimation of the RTO. For that purpose a Round-Trip Time (RTT) is measured after the send of every packet that is not a retransmission. The Round-Trip Time (RTT) is the time taken for a packet to reach the remote device and to get back an acknowledgement to the sending device. The RTT of a connection is calculated dynamically, nevertheless if TCP cannot get an estimate within 3 seconds, the default value of the RTT is set to 3 seconds.
If the RTO has been estimated, it applies to the next packet sending. If the acknowledgement of the next packet is not received before the estimated RTO expiration, the Exponential BackOff is activated. A maximum number of retransmissions of the same packet is allowed during a certain amount of time. After that if no acknowledgement has been received, the connection is aborted.
The maximum number of retransmissions and the maximum amount of time before the abort of the connection (tcp_ip_abort_interval) can be set up on some stacks.

Some retransmission algorithms are defined in TCP standards :

- The Jacobson's RTO estimation algorithm is used to estimate the Retransmission Time-Out (RTO),
- The Karn's algorithm says that the RTO estimation should not be done on a retransmitted segment,
- The Exponential BackOff defines that the retransmission time-out is doubled for each retransmission with an upper limit of 64 seconds.
- The fast retransmission algorithm allows retransmitting after the reception of three duplicate acknowledgments. This algorithm is advised because on a LAN it may lead to a quicker detection of the loss of a packet than waiting for the RTO expiration.

The use of these algorithms is recommended for a MODBUS implementation.

### 4.3.3 IP layer parameterization

### 4.3.3.1 IP Parameters

The following parameters must be configured in the IP layer of a MODBUS implementation :

- Local IP Address : the IP address can be part of a Class A, B or C.
- Subnet Mask. : Subnetting an IP Network can be done for a variety of reasons : use of different physical media (such as Ethernet, WAN, etc.), more efficient use of

network addresses, and the capability to control network traffic. The Subnet Mask has to be consistent with the IP address class of the local IP address.

- Default Gateway: The IP address of the default gateway has to be on the same subnet as the local IP address. The value 0.0 .0 .0 is forbidden. If no gateway is to be defined then this value is to be set to either 127.0.0.1 or the Local IP address.

Remark : The MODBUS messaging service doesn't require the fragmentation function in the IP layer.

The local IP End Point shall be configured with a local IP Address and with a Subnet Mask and a Default Gateway (different from 0.0.0.0).

# 4.4 COMMUNICATION APPLICATION LAYER 

### 4.4.1 MODBUS Client

![img-68.jpeg](images/img-68.jpeg.png)

Figure 10: MODBUS Client unit

### 4.4.1.1 MODBUS client design


Figure 10 shows a MODBUS Client unit. It illustrates a network configuration involving Modbus TCP/IP and Modbus Serial Line. The diagram includes multiple Modbus Client TCP/IP nodes connected to a Modbus TCP/IP network. Additionally, there are Modbus Server TCP/IP and Modbus Server Serial Line nodes connected to the network. Arrows indicate the flow of data between clients and servers, highlighting the Client TCP/IP gateway and Server TCP/IP gateway.

The definition of the MODBUS/TCP protocol allows a simple design of a client. The following activity diagram describes the main treatments that are processed by a client to send a MODBUS request and to treat a MODBUS response.

![img-69.jpeg](images/img-69.jpeg.png)

Figure 11: MODBUS Client Activity Diagram


Figure 11 shows a MODBUS Client Activity Diagram. It illustrates the process flow for a MODBUS client in an industrial communication system. The diagram begins with the client in an 'Idle' state, moving to 'Wait' upon receiving a response from the TCP management. It includes decision points for handling confirmation errors, retries, and sending MODBUS requests. The flow involves sending confirmations to the user application and setting response timers, with various actions branching from decision nodes based on conditions like confirmation status and retry counts.

A MODBUS client can receive three events:

- A new demand from the user application to send a request, in this case a MODBUS request has to be encoded and be sent on the network using the TCP management component service. The lower layer ( TCP management module) can give back an error due to a TCP connection error, or some other errors.
- A response from the TCP management, in this case the client has to analyze the content of the response and send a confirmation to the user application
- The expiration of a Time out due to a non-response. A new retry can be sent on the network or a negative confirmation can be sent to the User Application. Remark : These retries are initiated by the MODBUS client, some other retries can also be done by the TCP layer in case of TCP acknowledge lack.


# 4.4.1.2 Build a MODBUS Request 

Following the reception of a demand from the user application, the client has to build a MODBUS request and to send it to the TCP management.
Building the MODBUS request can be split in several sub-tasks:

- The instantiation of a MODBUS transaction that enables the Client to memorize all required information in order to bind later the response to the request and to send the confirmation to the user application.
- The encoding of the MODBUS request (PDU + MPAB header). The user application that initiates the demand has to provide all required information which enables the Client to encode the request. The MODBUS PDU is encoded according to the MODBUS Application Protocol Specification [1]. (MB function code, associated parameters and application data ). All fields of the MBAP header are filled. Then, the MODBUS request ADU is built prefixing the PDU with the MBAP header

- The sending of the MODBUS request ADU to the TCP management module which is in charge of finding the right TCP socket towards the remote Server. In addition to the MODBUS ADU the Destination IP address must also be passed.

The following activity diagram describes, more deeply than in Figure 11 MODBUS Client Activity Diagram, the request building phase.
![img-70.jpeg](images/img-70.jpeg.png)

Figure 12: Request building activity diagram

The following example describes the MODBUS request ADU encoding for reading the register \# 5 in a remote server :

- MODBUS Request ADU encoding :

|  | Description | Size | Example |
| :-- | :-- | :--: | :--: |
| MBAP Header | Transaction Identifier Hi | 1 | $0 \times 15$ |
|  | Transaction Identifier Lo | 1 | $0 \times 01$ |
|  | Protocol Identifier | 2 | $0 \times 0000$ |
|  | Length | 2 | $0 \times 0006$ |
|  | Unit Identifier | 1 | $0 \times F F$ |

| MODBUS <br> request | Function Code ( $*$ ) | 1 | $0 \times 03$ |
| :-- | :-- | :--: | :--: |
|  | Starting Address | 2 | $0 \times 0004$ |
|  | Quantity of Registers | 2 | $0 \times 0001$ |

(*) please see the MODBUS Application Protocol Specification [1].

# - Transaction Identifier 

The transaction identifier is used to associate the future response with the request. So, at a time, on a TCP connection, this identifier must be unique. There are several manners to use the transaction identifier:

- For example, it can be used as a simple "TCP sequence number" with a counter which is incremented at each request.
- It can also be judiciously used as a smart index or pointer to identify a transaction context in order to memorize the current remote server and the pending MODBUS request.

Normally, on MODBUS serial line a client must send one request at a time. This means that the client must wait for the answer to the first request before sending a second request. On TCP/MODBUS, several requests can be sent without waiting for a confirmation to the same server. The MODBUS/TCP to MODBUS serial line gateway is in charge of ensuring compatibility between these two behaviors.
The number of requests accepted by a server depends on its capacity in term of number of resources and size of the TCP windows. In the same way the number of transactions initialized simultaneously by a client depends also on its resource capacity. This implementation parameter is called "NumberMaxOfClientTransaction" and must be described as one of the MODBUS client features. Depending of the device type this parameter can take a value from 1 to 16 .

## - Unit Identifier

This field is used for routing purpose when addressing a device on a MODBUS+ or MODBUS serial line sub-network. In that case, the "Unit Identifier" carries the MODBUS slave address of the remote device:

If the MODBUS server is connected to a MODBUS+ or MODBUS Serial Line sub-network and addressed through a bridge or a gateway, the MODBUS Unit identifier is necessary to identify the slave device connected on the subnetwork behind the bridge or the gateway. The destination IP address identifies the bridge itself and the bridge uses the MODBUS Unit identifier to forward the request to the right slave device.
The MODBUS slave device addresses on serial line are assigned from 1 to 247 (decimal). Address 0 is used as broadcast address.
On TCP/IP, the MODBUS server is addressed using its IP address; therefore, the MODBUS Unit Identifier is useless. The value 0xFF has to be used.

When addressing a MODBUS server connected directly to a TCP/IP network, it's recommended not using a significant MODBUS slave address in the "Unit Identifier" field. In the event of a re-allocation of the IP addresses within an automated system and if a IP address previously assigned to a MODBUS server is then assigned to a gateway, using a significant slave address may cause trouble because of a bad routing by the gateway. Using a nonsignificant slave address, the gateway will simply discard the MODBUS PDU with no trouble. 0xFF is recommended for the "Unit Identifier" as nonsignificant value.
Remark : The value 0 is also accepted to communicate directly to a MODBUS/TCP device.

# 4.4.1.3 Process MODBUS Confirmation 

When a response frame is received on a TCP connection, the Transaction Identifier carried in the MBAP header is used to associate the response with the original request previously sent on that TCP connection:

- If the Transaction Identifier doesn't refer to any MODBUS pending transaction, the response must be discarded.
- If the Transaction Identifier refers to a MODBUS pending transaction, the response must be parsed in order to send a MODBUS Confirmation to the User Application (positive or negative confirmation)

Parsing the response consists in verifying the MBAP Header and the MODBUS PDU response:

## - MBAP Header

After the verification of the Protocol Identifier that must be $0 \times 0000$, the length gives the size of the MODBUS response.
If the response comes from a MODBUS server device directly connected to the TCP/IP network, the TCP connection identification is sufficient to unambiguously identify the remote server. Therefore, the Unit Identifier carried in the MBAP header is not significant (value $0 \times F F$ ) and must be discarded.
If the remote server is connected on a Serial Line sub-network and the response comes from a bridge, a router or a gateway, then the Unit Identifier (value $!=0 \times F F$ ) identifies the remote MODBUS server which has originally sent the response.

## - MODBUS Response PDU

The function code must be verified and the MODBUS response format analyzed according to the MODBUS Application Protocol:

- if the function code is the same as the one used in the request, and if the response format is correct, then the MODBUS response is given to the user application as a Positive Confirmation.
- If the function code is a MODBUS exception code (Function code +80 H ), the MODBUS exception response is given to the user application as a Positive Confirmation.
- If the function code is different from the one used in the request (=non expected function code), or if the format of the response is incorrect, then an error is signaled to the user application using a Negative Confirmation.

Remark: A positive confirmation is a confirmation that the command was received and responded to by the server. It does not imply that the server was able to successfully act on the command (failure to successfully act on the command is indicated by the MODBUS Exception response).

The following activity diagram describes, more deeply than in Figure 11 MODBUS Client Activity Diagram, the confirmation processing phase.

![img-71.jpeg](images/img-71.jpeg.png)

Figure 13: Process MODBUS Confirmation activity diagram

# 4.4.1.4 Time-out management 


Figure 13 shows a process MODBUS confirmation activity diagram. It illustrates the decision-making process for handling pending MODBUS transactions. The diagram begins with checking for a pending transaction and proceeds with different paths based on the transaction status, protocol type, and response correctness. Arrows and labeled blocks represent the flow of actions, including analyzing headers, processing exceptions, and sending confirmations.

There is deliberately NO specification of required response time for a transaction over MODBUS/TCP.
This is because MODBUS/TCP is expected to be used in the widest possible variety of communication situations, from I/O scanners expecting sub-millisecond timing to long distance radio links with delays of several seconds.
From a client perspective, the timeout must take into account the expected transport delays across the network, to determine a 'reasonable' response time. Such transport delays might be milliseconds for a switched Ethernet, or hundreds of milliseconds for a wide area network connection.
In turn, any 'timeout' time used at a client to initiate an application retry should be larger than the expected maximum 'reasonable' response time. If this is not followed, there is a potential for excessive congestion at the target device or on the network, which may in turn cause further errors. This is a characteristic, which should always be avoided.

So in practice, the client timeouts used in high performance applications are always likely to be somewhat dependent on network topology and expected client performance. Applications which are not time critical can often leave timeout values to the normal TCP defaults, which will report communication failure after several seconds on most platforms.

# 4.4.2 MODBUS Server 

![img-72.jpeg](images/img-72.jpeg.png)

Figure 14: MODBUS Server unit


Figure 14 shows a MODBUS Server unit architecture. It illustrates the interaction between Modbus Clients and Servers over TCP/IP and Serial Line connections. The diagram includes labeled blocks representing Modbus Client TCP/IP, Modbus Server TCP/IP, Modbus Client Serial Line, and Modbus Server Serial Line. Arrows indicate the flow of communication between these components, highlighting the use of gateways for TCP/IP and Serial Line integration.

The role of a MODBUS server is to provide access to application objects and services to remote MODBUS clients.

Different kind of access may be provided depending on the user application :

- simple access like get and set application objects attributes
- advanced access in order to trigger specific application services

The MODBUS server has:

- To map application objects onto readable and writable MODBUS objects, in order to get or set application objects attributes.
- To provide a way to trigger services onto application objects.

In run time the MODBUS server has to analyze a received MODBUS request, to process the required action, and to send back a MODBUS response.

Informative Note: The application objects and services of the Backend Interface obtain the requested data based upon the function code, and the User is responsible.

# 4.4.2.1 MODBUS Server Design 

The MODBUS Server design depends on both :

- the kind of access to the application objects (simple access to attributes or advanced access to services)
- the kind of interaction between the MODBUS server and the user application (synchronous or asynchronous).


Figure 15 shows a process MODBUS indication activity diagram. It illustrates the flow of operations within a MODBUS server as it handles requests. The process begins with the server in an 'Idle' state, transitioning to 'Wait' upon server initialization. From there, the diagram depicts various paths including checking the MODBUS PDU, processing services, and handling exceptions. Arrows indicate the flow of control, with conditions such as 'Processing OK' or 'Processing not OK' leading to different outcomes like building a response or an exception. The diagram uses labeled blocks and arrows to represent the decision-making process and subsequent actions.

The following activity diagram describes the main treatments that are processed by the Server to obtain a MODBUS request from TCP Management, then to analyze the request, to process the required action, and to send back a MODBUS response.
![img-73.jpeg](images/img-73.jpeg.png)

Figure 15: Process MODBUS Indication activity diagram

As shown in the previous activity diagram:

- Some services can be immediately processed by the MODBUS Server itself, with no direct interaction with the User Application ;
- Some services may require also interacting explicitly with the User Application to be processed ;
- Some other advanced services require invoking a specific interface called MODBUS Back End service. For example, a User Application service may be triggered using a sequence of several MODBUS request/response transactions according to a User Application level protocol. The Back End service is responsible for the correct processing of all individual MODBUS transactions in order to execute the global User Application service.

A more complete description is given in the following sections.
The MODBUS server can accept to serve simultaneously several MODBUS requests. The maximum number of simultaneous MODBUS requests the server can accept is one of the main characteristics of a MODBUS server. This number depends on the server design and its processing and memory capabilities. This implementation parameter is called "NumberMaxOfSeverTransaction" and must be described as one of the MODBUS server features. It may have a value from 1 to 16 depending on the device capabilities.

The behavior and the performance of the MODBUS server are significantly affected by the "NumberMaxOfTransaction" parameter. Particularly, it's important to note that the number of concurrent MODBUS transactions managed may affect the response time of a MODBUS request by the server.

# 4.4.2.2 MODBUS PDU Checking 

The following diagram describes the MODBUS PDU Checking activity.

![img-74.jpeg](images/img-74.jpeg.png)

Figure 16: MODBUS PDU Checking activity diagram


Figure 16 shows a MODBUS PDU Checking activity diagram. It illustrates the process flow for checking the MBAP header and managing MODBUS transactions. The diagram includes decision points for errors on the MBAP header and MB PDU, indicating paths for transaction refusal or acceptance. It also shows the instantiation of a MB Transaction and parsing of the MB PDU.

The MODBUS PDU Checking function consists of first parsing the MBAP Header. The Protocol Identifier field has to be checked :

- If it is different from MODBUS protocol type, the indication is simply discarded.
- If it is correct (= MODBUS protocol type; value $0 \times 00$ ), a MODBUS transaction is instantiated.

The maximum number of MODBUS transactions the server can instantiate is defined by the "NumberMaxOfTransaction" parameter ( A system or a configuration parameter).

In case of no more transactions available, the server builds a MODBUS exception response (Exception code 6 : Server Busy).

If a MODBUS transaction is available, it's initialized in order to memorize the following information:

- The TCP connection identifier used to send the indication (given by the TCP Management)
- The MODBUS Transaction ID (given in MBAP Header)
- The Unit Identifier (given in MBAP Header)

Then the MODBUS PDU is parsed. The function code is first controlled :

- in case of invalidity a MODBUS exception response is built (Exception code 1 : Invalid function).
- If the function code is accepted, the server initiates the "MODBUS Service processing" activity.

# 4.4.2.3 MODBUS service processing 

![img-75.jpeg](images/img-75.jpeg.png)

Figure 17: MODBUS service processing activity diagram

The processing of the required MODBUS service can be done in different ways depending on the device software and hardware architecture as described in the hereafter examples :

- Within a compact device or a mono-thread architecture where the MODBUS server can access directly to the user application data, the required service can be processed "locally" by the server itself without invoking the Back End service. The processing is done according to the MODBUS Application Protocol Specification [1]. In case of an error, a MODBUS exception response is built.
- Within a modular multi-processor device or a multi-thread architecture where the "communication layers" and the "user application layer" are 2 separate entities, some trivial services can be processed completely by the Communication entity while some others can require a cooperation with the User Application entity using the Back End service.

To interact with the User Application, the MODBUS Backend service must implement all appropriate mechanisms in order to handle User Application transactions and to manage correctly the User Application invocations and associated responses.

### 4.4.2.4 User Application Interface (Backend Interface)

Several strategies can be implemented in the MODBUS Backend service to achieve its job although they are not equivalent in terms of user network throughput, interface bandwidth usage, response time, or even design workload.

The MODBUS Backend service will use the appropriate interface to the user application :

- Either a physical interface based on a serial link, or a dual-port RAM scheme, or a simple I/O line, or a logical interface based on messaging services provided by an operating system.
- The interface to the User Application may be synchronous or asynchronous.

The MODBUS Backend service will also use the appropriate design pattern to get/set objects attributes or to trigger services. In some cases, a simple "gateway pattern" will be adequate. In some other cases, the designer will have to implement a "proxy pattern" with a corresponding caching strategy, from a simple exchange table history to more sophisticated replication mechanisms.

The MODBUS Backend service has the responsibility to implement the protocol transcription in order to interact with the User Application. Therefore, it can have to implement mechanisms for packet fragmentation/reconstruction, data consistency guarantee, and synchronization whatever is required.

# 4.4.2.5 MODBUS Response building 

Once the request has been processed, the MODBUS server has to build the response using the adequate MODBUS server transaction and has to send it to the TCP management component.
Depending on the result of the processing two types of response can be built :

- A positive MODBUS response :
- The response function code = The request function code
- A MODBUS Exception response :
- The objective is to provide to the client relevant information concerning the error detected during the processing :
- The response function code $=$ the request function code $+0 \times 80$;
- The exception code is provided to indicate the reason of the error.

| Exception Code | MODBUS name | Comments |
| :--: | :--: | :--: |
| 01 | Illegal Function Code | The function code is unknown by the server |
| 02 | Illegal Data Address | Dependant on the request |
| 03 | Illegal Data Value | Dependant on the request |
| 04 | Server Failure | The server failed during the execution |
| 05 | Acknowledge | The server accepted the service invocation but the service requires a relatively long time to execute. The server therefore returns only an acknowledgement of the service invocation receipt. |
| 06 | Server Busy | The server was unable to accept the MB Request PDU. The client application has the responsibility of deciding if and when to re-send the request. |
| 0 A | Gateway problem | Gateway paths not available. |
| 0B | Gateway problem | The targeted device failed to respond. The gateway generates this exception |

The MODBUS response PDU must be prefixed with the MBAP header which is built using data memorized in the transaction context.

## - Unit Identifier

The Unit Identifier is copied as it was given within the received MODBUS request and memorized in the transaction context.

# - Length 

The server calculates the size of the MODBUS PDU plus the Unit Identifier byte. This value is set in the "Length" field.

- Protocol Identifier

The Protocol Identifier field is set to $0 \times 0000$ (MODBUS protocol), as it was given within the received MODBUS request.

- Transaction Identifier

This field is set to the "Transaction Identifier" value that was associated with the original request and memorized in the transaction context.

Then the MODBUS response must be returned to the right MODBUS Client using the TCP connection memorized in the transaction context. When the response is sent, the transaction context must be free.

## 5 IMPLEMENTATION GUIDELINE


Figure 18 shows a MODBUS Messaging Service Object Model Diagram. It illustrates the interaction between different components of a messaging service. The diagram includes labeled blocks such as 'User Application', 'InterfaceUserApplication', 'Communication application layer', 'Configuration layer', 'InterfaceIndicationMsg', 'InterfaceResponseMsg', and 'TCP management'. Arrows indicate the flow of data or communication between these components, showing a structured layout typical of object model diagrams.

The objective of this section is to propose an example of a messaging service implementation.
The model describes below can be used as a guideline during a client or a server implementation of a MODBUS messaging service.

Informative Note: The messaging service implementation is the responsibility of the User.

### 5.1 OBJECT MODEL DIAGRAM

![img-76.jpeg](images/img-76.jpeg.png)

Figure 18: MODBUS Messaging Service Object Model Diagram
October 24, 2006
http://www.Modbus.org

Four main packages compose the Object Model Diagram:

- The Configuration layer which configures and manages operating modes of components of other packages
- The TCP Management which interfaces the TCP/IP stack and the communication application layer managing TCP connection. It implies the management of socket interface.
- The Communication application layer which is composed by the MODBUS client on one side and the MODBUS server on the other side. This package is linked with the user application.
The User application, which corresponds to the device application, is completely dependent on the device and therefore it will be not part of this Specification.

This model is independent of implementation choices like the type of OS, the memory management, etc. In order to guarantee this independence generic Interface layers are used between the TCP management layer and the communication layer and between the communication layer and the user application layer.
Different implementations of this interface can be realized by the User: Pipe between two tasks, shared memory, serial link interface, procedural call, etc.
Some assumptions have to be taken to define the hereafter implementation model :

- Static memory management
- Synchronous treatment of the server
- One task to process the receptions on all sockets.


# 5.1.1 TCP management package

![img-77.jpeg](images/img-77.jpeg.png)

Figure 19: MODBUS TCP management package


Figure 19 shows the MODBUS TCP management package. It consists of several interconnected components and classes, such as ConnexionMgt, InterfaceConnexion, and TCPConnexion. These elements are depicted with labeled blocks and arrows indicating relationships and data flow. Each block contains methods and attributes relevant to managing TCP connections in a MODBUS environment.

The TCP management package comprises the following classes :
CInterfaceConnexion: The role of this class consists in managing memory pool for connections.

CItemConnexion: This class contains all information needed to describe a connection.
CTCPConnexion:, This class provides methods for managing automatically a TCP connection (Interface socket is provided by CStackTCP_IP).

CConnexionMngt: This class manages all connections and send query/response to MODBUS Server/MODBUS Client through CInterfaceIndicationMsg and CInterfaceResponseMsg. This class also treats the Access control for the connection opening.

CMBAP: This class provides methods for reading/writing/analyzing the MODBUS MBAP.

CStackTCP_IP: This class Implements socket services and provides parameterization of the stack.

# 5.1.2 Configuration layer package 

![img-78.jpeg](images/img-78.jpeg.png)

Figure 20: MODBUS Configuration layer package


Figure 20 shows the MODBUS Configuration layer package. It includes various components such as the Communication application layer and TCP management, both derived from the Logical View. The Operating Mode is depicted with functions like m_Configure(), m_Start(), m_Stop(), and m_Reset(). There is also a ConfigurationObject block detailing attributes like GlobalState, MyModbusAddress, MyIPAddress, MyPortNumber, and IP lists for authorization and forbidden access.

The Configuration layer package comprises the following classes :
TConfigureObject: This class groups all data needed for configuring each other component. This structure is filled by the method m_Configure from the class CoperatingMode. Each class needing to be configured gets its own configuration data from this object. The configuration data is implementation dependent therefore the list of attributes of this class is provided as an example.

COperatingMode: The role of this class is to fill the TConfigureObject (according to the user configuration) and to manage the operating modes of the classes described below:

- CMODBUSServer
- CMODBUSClient

# - CconnexionMngt 

### 5.1.3 Communication layer package

![img-79.jpeg](images/img-79.jpeg.png)

Figure 21: MODBUS Communication Application layer package


Figure 21 shows the MODBUS Communication Application layer package. It illustrates a structured layout with various classes such as InterfaceUserApplication, ModbusPDU, ModbusServer, ModbusClient, InterfaceIndicationMsg, and InterfaceResponseMsg. The diagram includes labeled blocks connected by arrows, representing data flow and interactions between these components. Each class block contains methods or attributes relevant to its function within the communication layer.

The Communication Application layer package comprises the following classes :
CMODBUSServer: MODBUS query is received from class CInterfaceIndicationMsg (by the method m_ServerReceivingMessage). The role of this class is to build the MODBUS response or the MODBUS Exception according the query (incoming from network). This class implements the Graph State of MODBUS server. Response can be built only if class COperatingMode has sent both user configuration and right operating modes.

CMODBUSClient: MODBUS query is read from class CInterfaceUserApplication, The client task receives query by the method m_ClientReceivingMessage. This class

implements the State Graph of MODBUS client and manages transactions for linking query with response (from network). Query can be sent over network only if class CoperatingMode has sent both user configuration and right operating modes.

CTransaction: This class implements methods and structures for managing transactions.

# 5.1.4 Interface classes 

CInterfaceUserApplication: This class represents the interface with the user application, it provides two methods to access to the user data. In a real implementation this method can be implemented in different way depending of the hardware and software device capabilities (equivalent to an end-driver, example access to PCMCIA, shared memory, etc).

CInterfaceIndicationMsg: This Interface class is proposed for sending query from Network to the MODBUS Server, and for sending response from Network for the Client. This class interfaces TCPManagement and 'Communication Application Layer' packages (From Network). The implementation of this class is device dependent.

CInterfaceResponseMsg: This Interface class is used for receiving response from the Server and for sending query from the client to the Network. This class interfaces packages 'Communication Application Layer' and package 'TCPManagement' (To Network). The implementation of this class is device dependent.

### 5.2 IMPLEMENTATION CLASS DIAGRAM

The following Class Diagram describes the complete diagram of a proposal implementation.

![img-80.jpeg](images/img-80.jpeg.png)

Figure 22: Class Diagram

# 5.3 SEQUENCE DIAGRAMS 


Figure 23 shows a MODBUS client sequence diagram. It illustrates the sequence of operations between different components in a MODBUS communication process. The diagram includes labeled blocks representing different actions and messages between the Modbus client, client connection, and TCP connection. Arrows indicate the flow of communication, showing processes such as reading data from the user, sending requests, and receiving responses.

Two Sequence diagrams are described hereafter are an example in order to illustrate a Client MODBUS transaction and a Server MODBUS transaction.
![img-81.jpeg](images/img-81.jpeg.png)

Figure 23: MODBUS client sequence diagram

General comments for a better understanding of the Client sequence diagram:
First step: A Reading query comes from User Application (method m_Read).
Second Step: The 'Client' task receives the MODBUS query (method m_ClientReceivingMessage). This is the entry point of the Client. To associate the query with the corresponding response when it will arrive, the Client uses a Transaction resource (Class CTransaction). The MODBUS query is sent to the TCP_Management by calling the class interface CInterfaceResponseMsg (method m_MODBUSRequest)

Third Step: If the connection is already established there is nothing to do on connection, the message can be send over the network. Otherwise, a connection must be opened before the message can be sent over the network.
At this time the client is waiting for a response (from a remote server)
Fourth step: Once a response has been received from the network, the TCP/IP stack receives data (method m_EventOnSocket is implicitly called).
If the connection is already established, then the MBAP is read for retrieving the connection object (connection object gives memory resource and other information). Data coming from network is read and confirmation is sent to the client task via the class Interface CInterfaceIndicationMsg (method m_MODBUSConfirmation). Client task receives the MODBUS Confirmation (method m_ClientReceivingResponse).
Finally the response is-written to the user application (method m_WriteData), and transaction resource is freed.


Figure 24 shows a sequence diagram illustrating a MODBUS server exchange. It details the interactions between various components such as TCP connections and MODBUS servers. The diagram includes labeled blocks representing different functions and processes, with arrows indicating the flow of data and communication between these components.

Hereafter is an example of a MODBUS Server exchange.
![img-82.jpeg](images/img-82.jpeg.png)

Figure 24: MODBUS server Diagram

General comments for a better understanding of the Server sequence diagram:
First step: a client has sent a query (MODBUS query) over the network.
The TCP/IP stack receives data (method m_EventOnSocket is implicitly called).
Second step: The query may be a connection request or not (method m IsConnexionRequest).
If the query is a connection request, the connection object and buffers for receiving and sending the MODBUS frame are allocated (method m_GetObjectConnexion). Just after, the connection access control must be checked and accepted (method m_AcceptConnexion)

Third step: If the query is a MODBUS request, the complete MODBUS Query can be read (method m_ReceiveData). At this time the MBAP must be analyzed (method m IsMdbHeaderCorrect). The complete frame is sent to the Server task via the CinterfaceindicationMessaging Class (method m_MODBUSIndication). Server task receives the MODBUS Query (method m_ServerReceivingMessage) and analyses it. If an error occurs (function code not supported, etc), a MODBUSException frame is built (m_BuildMODBUSException), otherwise the response is built.

Fourth Step: The response is sent over the network via the CinterfaceResponseMessaging (method m_MODBUSResponse). Treatment on the connection object is done by the method m_SendData (retrieve the connection descriptor, etc) and data is sent over the network.

# 5.4 CLASSES AND METHODS DESCRIPTION 

### 5.4.1 MODBUS Server Class

## Class CMODBUSServer

## class CMODBUSServer

## Stereotype implementationClass

Provides methods for managing MODBUS Messaging in Server Mode

## Field Summary

protected char GlobalState
state of the MODBUS Server

## Constructor Summary

CMODBUSServer(TConfigureObject * InkConfigureObject)
Constructor : Create internal object

## Method Summary

![img-83.jpeg](images/img-83.jpeg.png)

# 5.4.2 MODBUS Client Class 

## Class CMODBUSClient

## class CMODBUSClient

Provides methods for managing MODBUS Messaging in Client Mode
Stereotype implementationClass

## Field Summary

protected GlobalState
char State of the MODBUS Client

## Constructor Summary

CMODBUSClient(TConfigureObject * lnkConfigureObject) Constructor : Create internal object, initialize to 0 variables.

## Method Summary

![img-84.jpeg](images/img-84.jpeg.png)

|  | Method for Stopping component, return true if stopped |
| :--: | :--: |
| protected void | m_tClientMODBUS(void |
|  | Client MODBUS task... |

# 5.4.3 Interface Classes 

### 5.4.3.1 Interface Indication class

## Class C\InterfaceIndicationMsg

## Direct Known Subclasses:

CConnexionMngt

## class CInterfaceIndicationMsg

Class for sending message from TCP_Management to MODBUS Server or Client
Stereotype interface

| Method Summary |  |
| :--: | :--: |
| int | m_MODBUSConfirmation(TItemConnexion * lnkObject) |
|  | Method for Receiving incoming Response, calling the Client : could be by reference, by Message Queue, Remote procedure Call, ... |
| int | m_MODBUSIndication(TItemConnexion * lnkObject) |
|  | Method for reading incoming MODBUS Query and calling the Server : could be by reference, by Message Queue, Remote procedure Call, ... |

### 5.4.3.2 Interface Response Class

## Class CInterfaceResponseMsg

## Direct Known Subclasses:

## CMODBUSClient, CMODBUSServer

## class CInterfaceResponseMsg

Class for sending response or sending query to TCP_Management from Client or Server Stereotype interface

| Method Summary |  |  |  |  |
| :--: | :--: | :--: | :--: | :--: |
| TitemConnexion | m_GetMemoryConnexion(unsigned | long | IPDest) |  |
|  | Get an object I | PConnexion from memory pool. Return -1 if not enough |  |  |
|  | memory |  |  |  |
| int | m_MODBUSRequest(TItemConnexion |  |  | lnkCMODBUS) |
|  | Method for Writing incoming MODBUS Query Client to ConnexionMngt |  |  |  |

|  | could be by reference, by Message Queue, Remote procedure Call, ... |
| :--: | :--: |
| int | m_MODBOSResponse(TItemConnexion * InkObject) |
|  | Method for writing Response from MODBUS Server to ConnexionMngt could be by reference, by Message Queue, Remote procedure Call, ... |

# 5.4.4 Connexion Management class 

## Class CConnexionMngt

## class CConnexionMngt

Class that manages all TCP Connections
Stereotype implementationClass

## Field Summary

| protected <br> char | GlobalState <br> Global State of the Component ConnexionMngt |
| :--: | :--: |
| Int | NbConnectionSupported |
|  | Global number of connections |
| Int | NbLocalConnection |
|  | Number of connections opened by the local Client to a remote Server |
| Int | NbRemoteConnection |
|  | Number of connections opened by a remote Client to the local Server |

## Constructor Summary

CconnexionMngt (TConfigureObject * InkConfigureObject) Constructor : Create internal object, initialize to 0 variables.

## Method Summary

| int | m_EventOnSocket(void <br> wake-up |  |  |  |
| :--: | :--: | :--: | :--: | :--: |
| bool | m_IsConnectionAuthorized(unsigned | long | IPAddress) |  |
| int | Return true if new connection is authorized |  |  |  |
| int | m_ReceiveData(TItemConnexion <br> Interface with CTCPConnexion::write method for reading data from network return negative value if problem |  |  |  |
| bool | m_Reset (void <br> Method for Resetting ConnectionMngt component return true if Reset |  |  |  |
| int | m_SendData(TItemConnexion <br> Interface with CTCPConnexion::read method for sending data to the network Return negative value if problem |  |  |  |
| bool | m_Start(void <br> Method for Starting ConnectionMngt component return true if Started |  |  |  |
| bool | m_Stop(void <br> Method for Stopping component return true if Stopped |  |  |  |

MODBUS Messaging on TCP/IP Implementation Guide V1.0b
Modbus Organization
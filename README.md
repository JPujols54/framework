# 📚 Prerrequisitos para Construir un Servidor Web HTTP desde Cero en Python

Antes de comenzar el desarrollo de este proyecto, es recomendable dominar una serie de conceptos fundamentales de programación, redes y arquitectura de software. El objetivo no es memorizar cada tema, sino comprender cómo interactúan entre sí para construir un servidor HTTP completamente funcional.

---

# 🐍 Módulo 0 - Fundamentos de Python

## Sintaxis básica

- Variables
- Tipos de datos
- Operadores
- Entrada y salida de datos
- Comentarios
- Expresiones
- Conversión de tipos

---

## Control de flujo

- if
- elif
- else
- while
- for
- break
- continue
- pass

---

## Funciones

- Definición de funciones
- Parámetros
- Argumentos
- Valores por defecto
- `*args`
- `**kwargs`
- Return
- Scope (variables locales y globales)
- Funciones lambda (opcional)

---

## Estructuras de datos

- Listas
- Tuplas
- Diccionarios
- Sets
- Strings
- Métodos más utilizados

---

## Manejo de errores

```python
try:
except:
finally:
raise
```

Comprender:

- Excepciones
- Captura de errores
- Lanzamiento de excepciones
- Buenas prácticas

---

## Manejo de archivos

- open()
- read()
- readline()
- readlines()
- write()
- close()

Especialmente:

```python
Path.read_bytes()
Path.read_text()
```

---

# 🏗️ Módulo 1 - Programación Orientada a Objetos

La arquitectura del servidor estará completamente basada en objetos.

## Clases

```python
class HTTPServer:
```

---

## Objetos

```python
server = HTTPServer()
```

---

## Constructor

```python
__init__()
```

---

## Métodos

- Métodos públicos
- Métodos privados
- Métodos protegidos

---

## Atributos

- De instancia
- De clase

---

## Encapsulación

- Público
- Protegido (`_`)
- Privado (`__`)

---

## Herencia

```python
class MiServidor(HTTPServer):
```

---

## Polimorfismo

Comprender cómo un mismo método puede comportarse de forma diferente según el objeto.

---

## Abstracción

Aprender a separar responsabilidades.

---

## Métodos especiales

- `__init__`
- `__str__`
- `__repr__`
- `__len__`
- `__iter__`
- `__eq__`

---

## Decoradores

Decoradores incorporados:

- `@property`
- `@staticmethod`
- `@classmethod`

Decoradores personalizados:

```python
@router.get("/")

@router.post("/usuarios")
```

---

# 🌐 Módulo 2 - Fundamentos de Redes

Antes de escribir una sola línea del servidor es importante comprender cómo funcionan las redes.

## Conceptos básicos

- ¿Qué es una red?
- Cliente
- Servidor
- Host
- Nodo

---

## Direcciones IP

- IPv4
- IPv6
- localhost
- 127.0.0.1

---

## Puertos

Ejemplos comunes:

- 80
- 443
- 22
- 21
- 25
- 3306
- 5432
- 8080

---

## DNS

¿Cómo un dominio se convierte en una dirección IP?

---

## NAT

¿Qué ocurre cuando usamos un router doméstico?

---

## Firewall

¿Qué función cumple?

---

## Protocolos

### TCP

- Orientado a conexión
- Fiable
- Ordenado

### UDP

- No orientado a conexión
- Muy rápido
- Sin garantía de entrega

---

## Three Way Handshake

Comprender:

```
Cliente

↓

SYN

↓

Servidor

↓

SYN + ACK

↓

Cliente

↓

ACK

↓

Conexión establecida
```

---

# 🔌 Módulo 3 - Sockets

Este será el corazón del servidor.

Conceptos:

- Socket
- Cliente TCP
- Servidor TCP
- Flujo de datos
- Conexión
- Desconexión

Funciones importantes:

```python
socket()

bind()

listen()

accept()

recv()

send()

sendall()

close()

setsockopt()

settimeout()
```

---

## Tipos de Socket

```python
AF_INET

SOCK_STREAM
```

---

# 🌍 Módulo 4 - Protocolo HTTP

Este módulo es probablemente el más importante de todo el proyecto.

## ¿Qué es HTTP?

---

## Request

Comprender completamente:

```http
GET /index.html HTTP/1.1

Host: localhost

User-Agent: Chrome

Accept: text/html
```

---

## Response

```http
HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 120

Connection: close
```

---

## Headers HTTP

Algunos importantes:

- Host
- User-Agent
- Accept
- Accept-Encoding
- Accept-Language
- Content-Type
- Content-Length
- Connection
- Cache-Control

---

## Body

¿Qué información contiene?

---

## Métodos HTTP

- GET
- POST
- PUT
- PATCH
- DELETE
- OPTIONS
- HEAD

---

## Códigos HTTP

### Informativos

100

101

---

### Éxito

200

201

204

---

### Redirecciones

301

302

304

---

### Error del cliente

400

401

403

404

405

---

### Error del servidor

500

501

502

503

---

## MIME Types

- text/html
- text/plain
- text/css
- application/javascript
- application/json
- image/png
- image/jpeg
- image/svg+xml
- application/octet-stream

---

## URLs

Comprender:

```
https://dominio.com:8080/usuarios/15?activo=true
```

Separar:

- Protocolo
- Host
- Puerto
- Path
- Query String

---

## Query Parameters

```
/buscar?nombre=Juan
```

---

## Path Parameters

```
/usuario/Juan
```

---

## Formularios

- application/x-www-form-urlencoded
- multipart/form-data

---

## JSON

¿Qué es?

¿Por qué es tan utilizado?

---

## Cookies

Concepto básico.

---

## Sesiones

Concepto básico.

---

# 🏛️ Módulo 5 - Arquitectura del Servidor

Comprender la responsabilidad de cada componente.

## HTTPServer

Responsable de:

- Escuchar conexiones
- Aceptar clientes
- Crear hilos
- Enviar respuestas

---

## Request

Responsable de:

- Parsear la petición
- Obtener método
- Obtener ruta
- Obtener headers
- Obtener body

---

## HTTPResponse

Responsable de:

- Construir la respuesta HTTP
- Formatear headers
- Calcular Content-Length
- Exportar bytes

---

## Router

Responsable de:

- Registrar endpoints
- Resolver rutas
- Ejecutar funciones asociadas

---

## Archivos estáticos

Servir:

- HTML
- CSS
- JS
- Imágenes
- Iconos

---

## Expresiones Regulares

Necesarias para implementar rutas dinámicas.

Ejemplo:

```
/usuario/<nombre>
```

---

## Logging

Registrar:

- Conexiones
- Peticiones
- Errores
- Advertencias
- Información

---

# 🧵 Módulo 6 - Concurrencia

Un servidor moderno debe atender múltiples clientes al mismo tiempo.

Conceptos:

- Thread
- threading.Thread
- Daemon Thread
- Lock
- Race Condition
- Deadlock (conceptualmente)
- Thread Pool (opcional)

---

# 🏛️ Módulo 7 - Arquitectura de Software

Comprender cómo organizar correctamente el proyecto.

## Modularidad

Separar responsabilidades.

---

## Cohesión

Cada clase debe tener una responsabilidad clara.

---

## Acoplamiento

Reducir dependencias entre módulos.

---

## Principios SOLID (Introducción)

- Single Responsibility
- Open/Closed
- Liskov
- Interface Segregation
- Dependency Inversion

---

## Principios de diseño

- DRY
- KISS
- YAGNI

---

## Organización del proyecto

Ejemplo:

```
core/
│
├── server.py
├── request.py
├── response.py
├── router.py
└── logger.py

public/
│
├── index.html
├── css/
└── js/

main.py
```

---

# 🛠️ Módulo 8 - Herramientas

Herramientas recomendadas durante el desarrollo.

## Git

- init
- add
- commit
- branch
- merge
- checkout
- log

---

## GitHub

Control de versiones remoto.

---

## Virtual Environments

```
python -m venv .venv
```

---

## pip

Instalación de dependencias.

---

## requirements.txt

Gestión de paquetes.

---

## curl

Probar endpoints HTTP.

Ejemplo:

```bash
curl http://localhost:8080/hola
```

---

## Postman

Cliente HTTP para pruebas.

---

## DevTools del navegador

Especialmente la pestaña:

```
Network
```

---

# 📖 Conceptos Complementarios Recomendados

- Expresiones Regulares (Regex)
- UTF-8
- ASCII
- Bytes vs Strings
- Serialización
- JSON
- Variables de entorno
- Configuración de aplicaciones
- Pathlib
- Context Managers (`with`)
- MIME Types
- Seguridad básica (Path Traversal)
- Validación de entradas

---

# 🎯 Ruta de Aprendizaje Recomendada

```
Python Básico
        │
        ▼
Programación Orientada a Objetos
        │
        ▼
Redes (TCP/IP)
        │
        ▼
Sockets
        │
        ▼
HTTP
        │
        ▼
Servidor TCP
        │
        ▼
Servidor HTTP
        │
        ▼
Parser HTTP
        │
        ▼
HTTPResponse
        │
        ▼
Router
        │
        ▼
Decoradores
        │
        ▼
Rutas Dinámicas
        │
        ▼
Archivos Estáticos
        │
        ▼
Multithreading
        │
        ▼
Logging
        │
        ▼
Arquitectura de Software
        │
        ▼
Mini Framework HTTP
```

---

# 💡 Filosofía del Proyecto

El objetivo principal de este proyecto no es únicamente construir un servidor HTTP funcional, sino comprender **qué ocurre internamente cuando un navegador se comunica con un servidor web**.

En lugar de depender desde el inicio de frameworks como Flask, Django o FastAPI, este proyecto busca desarrollar una comprensión profunda de los conceptos fundamentales que dichos frameworks abstraen.

Al finalizar este recorrido, el estudiante no solo habrá construido un servidor web desde cero, sino que también comprenderá el funcionamiento interno de protocolos como HTTP, el uso de sockets, la organización de una arquitectura modular y los principios básicos detrás de cualquier framework web moderno.
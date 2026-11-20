# FastAPI flashcards by topic

Review flashcards for FastAPI, grouped by topic. Read the question at the top, answer it in your head, then check the answer below it.

Each topic folder starts with a title page, `00-title.png`, then holds its cards as PNGs, numbered in reading order. `print/` has one A4 landscape PDF per topic: the title page, then one card per page.

The code examples come from a books API and a todo API with SQLite, written while studying [FastAPI - The Complete Course](https://github.com/codingwithroby/FastAPI-The-Complete-Course) by Eric Roby.

## HTTP basics

Folder: [`01-http-basics/`](01-http-basics/) · Print: [`print/01-http-basics.pdf`](print/01-http-basics.pdf)

| Card | Question |
| --- | --- |
| [01-crud-and-http-methods.png](01-http-basics/01-crud-and-http-methods.png) | How does CRUD map to HTTP methods? |
| [02-where-data-goes.png](01-http-basics/02-where-data-goes.png) | Where can a client put data in a request? |
| [03-parts-of-a-request.png](01-http-basics/03-parts-of-a-request.png) | What are the parts of an HTTP request? |
| [04-status-code-ranges.png](01-http-basics/04-status-code-ranges.png) | What do the HTTP status ranges mean? |

## Routes and parameters

Folder: [`02-routes-and-parameters/`](02-routes-and-parameters/) · Print: [`print/02-routes-and-parameters.pdf`](print/02-routes-and-parameters.pdf)

| Card | Question |
| --- | --- |
| [01-route-decorator.png](02-routes-and-parameters/01-route-decorator.png) | What turns a Python function into an API endpoint? |
| [02-path-vs-query.png](02-routes-and-parameters/02-path-vs-query.png) | How do you tell a path parameter from a query parameter? |
| [03-validating-url-values.png](02-routes-and-parameters/03-validating-url-values.png) | How do you validate values in the URL? |
| [04-request-and-response-models.png](02-routes-and-parameters/04-request-and-response-models.png) | Can a handler take a Pydantic model in and send one back? |
| [05-case-insensitive-matching.png](02-routes-and-parameters/05-case-insensitive-matching.png) | How do you compare text and ignore upper and lower case? |

## Validation and models

Folder: [`03-validation-and-models/`](03-validation-and-models/) · Print: [`print/03-validation-and-models.pdf`](print/03-validation-and-models.pdf)

| Card | Question |
| --- | --- |
| [01-why-validate.png](03-validation-and-models/01-why-validate.png) | Why does an API need to validate input? |
| [02-input-vs-stored-model.png](03-validation-and-models/02-input-vs-stored-model.png) | Why keep separate models for input and stored data? |
| [03-field-rules.png](03-validation-and-models/03-field-rules.png) | How do you declare validation rules on a model? |
| [04-automatic-422.png](03-validation-and-models/04-automatic-422.png) | Do you have to write the 422 yourself? |
| [05-before-and-after-validation.png](03-validation-and-models/05-before-and-after-validation.png) | What changes when you add validation to a route? |
| [06-model-dump.png](03-validation-and-models/06-model-dump.png) | How do you build an object from a validated model? |
| [07-response-model.png](03-validation-and-models/07-response-model.png) | What does response_model check? |

## Status codes and errors

Folder: [`04-status-codes-and-errors/`](04-status-codes-and-errors/) · Print: [`print/04-status-codes-and-errors.pdf`](print/04-status-codes-and-errors.pdf)

| Card | Question |
| --- | --- |
| [01-default-200.png](04-status-codes-and-errors/01-default-200.png) | What status code does a FastAPI route return by default? |
| [02-leaving-off-status-code.png](04-status-codes-and-errors/02-leaving-off-status-code.png) | What happens if you leave off status_code? |
| [03-which-code-fits.png](04-status-codes-and-errors/03-which-code-fits.png) | Which status code fits each outcome? |
| [04-who-sets-each-code.png](04-status-codes-and-errors/04-who-sets-each-code.png) | Who sets each status code? |
| [05-raising-404.png](04-status-codes-and-errors/05-raising-404.png) | How does a route report that something was not found? |
| [06-422-vs-404.png](04-status-codes-and-errors/06-422-vs-404.png) | What is the difference between 422 and 404? |

## Running and tooling

Folder: [`05-running-and-tooling/`](05-running-and-tooling/) · Print: [`print/05-running-and-tooling.pdf`](print/05-running-and-tooling.pdf)

| Card | Question |
| --- | --- |
| [01-start-and-stop-the-server.png](05-running-and-tooling/01-start-and-stop-the-server.png) | How do you start and stop a FastAPI server? |
| [02-uv-vs-uvicorn.png](05-running-and-tooling/02-uv-vs-uvicorn.png) | uv and uvicorn look alike. What does each do? |
| [03-requirements-vs-pyproject.png](05-running-and-tooling/03-requirements-vs-pyproject.png) | What is the difference between requirements.txt and pyproject.toml? |

## App structure

Folder: [`06-app-structure/`](06-app-structure/) · Print: [`print/06-app-structure.pdf`](print/06-app-structure.pdf)

| Card | Question |
| --- | --- |
| [01-endpoint-handler-router.png](06-app-structure/01-endpoint-handler-router.png) | What is an endpoint, a handler, and a router? |
| [02-handler-and-router.png](06-app-structure/02-handler-and-router.png) | What is a router, and what is a handler? |
| [03-routers-folder.png](06-app-structure/03-routers-folder.png) | How does a routers folder let an app grow? |
| [04-router-vs-api-gateway.png](06-app-structure/04-router-vs-api-gateway.png) | What is the difference between a router and an API gateway? |
| [05-dependencies.png](06-app-structure/05-dependencies.png) | What is a dependency? |
| [06-depends-chain.png](06-app-structure/06-depends-chain.png) | How does FastAPI read the header, and what does each Depends return? |

## Databases

Folder: [`07-databases/`](07-databases/) · Print: [`print/07-databases.pdf`](print/07-databases.pdf)

| Card | Question |
| --- | --- |
| [01-databases-and-sqlalchemy.png](07-databases/01-databases-and-sqlalchemy.png) | SQLite, PostgreSQL, MongoDB, SQLAlchemy. What is each, and what stays the same? |
| [02-request-to-database-flow.png](07-databases/02-request-to-database-flow.png) | What happens between a client and the database? |
| [03-who-assigns-ids.png](07-databases/03-who-assigns-ids.png) | Who should assign the id of a new record? |

## Authentication

Folder: [`08-authentication/`](08-authentication/) · Print: [`print/08-authentication.pdf`](print/08-authentication.pdf)

| Card | Question |
| --- | --- |
| [01-hashed-passwords.png](08-authentication/01-hashed-passwords.png) | Why store a hash instead of the password? |
| [02-authentication-vs-authorization.png](08-authentication/02-authentication-vs-authorization.png) | How is authentication different from authorization? |
| [03-login-flow-steps.png](08-authentication/03-login-flow-steps.png) | How does password login with a JWT give access? |
| [04-login-flow-requests-and-code.png](08-authentication/04-login-flow-requests-and-code.png) | What do the six login steps look like as requests and code? |
| [05-what-login-sends-back.png](08-authentication/05-what-login-sends-back.png) | What does a successful login send back, and how is it used later? |
| [06-oauth2-password-bearer.png](08-authentication/06-oauth2-password-bearer.png) | What does OAuth2PasswordBearer do on the server? |
| [07-jwt.png](08-authentication/07-jwt.png) | What is a JWT? |
| [08-secret-key.png](08-authentication/08-secret-key.png) | What does the secret key do? |
| [09-jwt-in-the-header.png](08-authentication/09-jwt-in-the-header.png) | Where do later requests send the JWT? |

## Cards that overlap

Two pairs cover nearly the same idea. They are kept for now:

- Status codes and errors: card 1 (default 200) and card 2 (leaving off `status_code`).
- Validation and models: card 1 (why validate) and card 5 (before and after validation).

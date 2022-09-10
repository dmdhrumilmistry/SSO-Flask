# SSO Flask

- ask user to sign up/login
- if valid generate session cookie and redirect user back to the application else ask to login in again
- on logout delete session id

|      Endpoint       | METHOD | Params | Desc                                                          |
| :-----------------: | :----: | :----: | :------------------------------------------------------------ |
| /api/login/generate |  POST  | email  | send email id to login                                        |
|   /api/login/auth   |  POST  | token  | send token from email                                         |
| /api/user/generate  |  POST  | token  | returns new token for requested website, website can          |
| /api/token/details  |  POST  | token  | returns details of the token (masked email id, and full name) |

# SSO Flask

- ask user to sign up/login
- if valid generate session cookie and redirect user back to the application else ask to login in again
- on logout delete session id

- API endpoints

| Implemented |         Endpoint         | METHOD |        Params        | Desc                                                                          |
| :---------: | :----------------------: | :----: | :------------------: | :---------------------------------------------------------------------------- |
|     [X]     |    /api/user/generate    |  POST  |     email, name      | returns msg and authToken                                                     |
|     [X]     |     /api/user/getId      |  POST  |      authToken       | returns userId                                                                |
|     [X]     | /api/user/token/generate |  POST  | authToken,id, domain | returns new token for requested website, use this endpoint to reset web token |
|     [X]     | /api/user/token/details  |  POST  |      authToken       | returns details of the token (masked email id, and full name)                 |
|     [ ]     |     /api/user/login      |  POST  |  authToken, domain   | verifies if authentication is valid returns bool value                        |

- Users table preview

|                  id                  |      name      | emailId              | auth_tokens                                                            |
| :----------------------------------: | :------------: | :------------------- | :--------------------------------------------------------------------- |
| 0e2xx8fc-5xex-47x1-99xx-0869adxxxxxx | your-full-name | your-email@domain.co | {"domain-01":"token-01","domain-02":"token-02","domain-03":"token-03"} |

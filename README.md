# SSO Flask

A python application written using Flask to reduce creating passwords on several websites for logging in

## How websites can use it

- Ask user to Sign Up/Login using the hosted API
- Generate token for website domain
- Use generated token to authenticate user for accessing website
- Release generated token for the domain

## API endpoints

|         Endpoint         | METHOD |        Params         | Desc                                                                                                     |
| :----------------------: | :----: | :-------------------: | :------------------------------------------------------------------------------------------------------- |
|    /api/user/generate    |  POST  |      email, name      | returns msg and authToken                                                                                |
|     /api/user/getId      |  POST  |       authToken       | returns userId                                                                                           |
|    /api/user/details     |  POST  |       authToken       | returns user details (full name, tokens generated domains, and masked email id)                          |
| /api/user/token/generate |  POST  | authToken, id, domain | returns new token for requested website, use this endpoint to reset web token                            |
|  /api/user/token/status  |  POST  | authToken, id, domain | returns if token is still valid or not (should be used by website's backend server to get token status ) |
| /api/user/token/release  |  POST  | authToken, id, domain | revokes token for assigned domain                                                                        |

## Users table in DynamoDB

|                  id                  |      name      | emailId              | auth_tokens                                                            |
| :----------------------------------: | :------------: | :------------------- | :--------------------------------------------------------------------- |
| 0e2xx8fc-5xex-47x1-99xx-0869adxxxxxx | your-full-name | your-email@domain.co | {"domain-01":"token-01","domain-02":"token-02","domain-03":"token-03"} |

## Installation and Usage

- Clone/Download repo

  ```bash
  git clone --depth=1 https://github.com/dmdhrumilmistry/SSO-Flask.git
  ```

- Change directory

  ```bash
  cd SSO-Flask
  ```

- Install requirements

  ```bash
  python -m pip install -r requirements.txt
  ```

  > ubuntu/debian users might need to use `python3` instead of `python`

- Create a new `.env` file with AWS creds in `SSO-Flask` directory

  ```bash
  AWS_ACCESS_KEY_ID='aws-access-key-id'
  AWS_SECRET_ACCESS_KEY='aws-secret-access-key'
  AWS_REGION_NAME='your-aws-zone'
  ```

  > Programmatic access is required to perform this action

- Start waitress server

  ```bash
  waitress-serve --listen=*:80 app:app
  ```

  > Allow HTTP traffic on port 80 for EC2 instance

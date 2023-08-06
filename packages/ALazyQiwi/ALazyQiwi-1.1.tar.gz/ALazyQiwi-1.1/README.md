# ALazyQiwi - Async Library for qiwi famrs

1. Install package
    - Windows -> `$ pip install LazyQiwi`
    - Mac OS & Linux -> `$ pip3 install LazyQiwi`

## Usage

### Import in your project

`from ALazyQiwi import LazyQiwi`

### Initialize

`api = LazyQiwi(token="")`

### Get account balance

```
async def bal():
    token = "<your token here>"
    api = LazyQiwi(token)
    return await api.account_balance()

asyncio.run(bal())
>>> [0.0]
```

### Transfer money

```

async def transfer():
    token = "<your token here>"
    api = LazyQiwi(token)
    await api.pay(account='7910XXXXXXX', amount=10.35, comment="Test transfer")

asyncio.run(transfer())
>>> None
```

### Create account information dump

```
# In one method
async def main():

    token = "<your token here>"
    api = LazyQiwi(token)


    data = await api.create_account_dump()
    print(data)

asyncio.run(main())
```

#### Get current account infromation

```
async def main():

    token = "<your token here>"
    api = LazyQiwi(token)


    basic_data = await api.get_basic_info() # returns dict
    
    account_number = basic_data['basic']['number']['number']
    language = basic_data['basic']['language']
    
    personal_data = await api.get_personal_info(account_number) # returns dict
    limits = await api.get_accounts_limits(account_number, language) # returns dict
    restrictions = await api.get_account_restriction(account_number) # returns list

    print(
        basic_data, personal_data, limits, restrictions
    )

asyncio.run(main())
```


### Errors handlers

`InvalidTokenError` - token is invalid
`InRequestError` - trying to send http request and got error
`APIError` - if got error after server return result
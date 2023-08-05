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
    api = LazyQiwi(token="")
    return await api.account_balance()

asyncio.run(bal())
>>> [0.0]
```

### Transfer money

```

async def transfer():
    api = LazyQiwi(token="")
    await api.pay(account='7910XXXXXXX', amount=10.35, comment="Test transfer")

asyncio.run(transfer())
>>> None
```

### Errors handlers

`InvalidTokenError` - token is invalid
`InRequestError` - trying to send http request and got error
`APIError` - if got error after server return result
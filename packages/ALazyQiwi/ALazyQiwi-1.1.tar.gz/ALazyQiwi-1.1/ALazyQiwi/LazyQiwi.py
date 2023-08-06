from random import *
import time
import httpx
import asyncio
from .errors import *
import json as js
from datetime import datetime

class LazyQiwi(object):

    def __init__(self, token: str, phone: str = "", proxies: dict = None):

        """Changed SimpleQiwi library for qiwi farms

        Args
        ----
            token : str
            phone : str
            proxies : dict

        Important
        ---------
            Specify the proxy servers in the dict format => {"http": "http://...
        """

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        self.token = token
        self.phone = phone
        self.proxies = proxies


    @property
    def _transaction_id(self) -> str:

        """Unical id generator
        
        Developed by Nodu$ iNC.
        -----------------------

        Returns
        -------
            UNIX time * randint(1000, 2000)
        """

        return str(int(time.time() * randint(1000, 2000)))

    @asyncio.coroutine
    async def get_basic_info(self) -> dict:

        try:
            match self.proxies:

                case None:
                    async with httpx.AsyncClient(headers=self.headers) as client:
                        r = await client.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true")

                        if r.status_code != 200:
                            raise InvalidTokenError("Invalid token used;")
                        
                        json = r.json()
                        await client.aclose()

                case _:
                    async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                        r = await client.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true")

                        if r.status_code != 200:
                            raise InvalidTokenError("Invalid token used;")
                        
                        json = r.json()
                        await client.aclose()
        except Exception as e:
            raise InRequestError(e)

        if 'code' in json or 'errorCode' in json:
            raise APIError(json)

        d = {'token': {
                    "token": self.token,
                    "balance": await self.account_balance()
                },
                "number": {
                    "short_info": f"{json['contractInfo']['contractId']} {json['userInfo']['operator']}",
                    "number": json['contractInfo']['contractId'],
                    "operator": json['userInfo']['operator']
                },
                "nickname": {
                    "uri": "https://qiwi.com/n/" + json['contractInfo']['nickname']['nickname'],
                    "nickname": json['contractInfo']['nickname']['nickname']
                },
                "smsNotification": {
                    "enabled": json['contractInfo']['smsNotification']['enabled'],
                    "active": json['contractInfo']['smsNotification']['active'],
                    "enddate": json['contractInfo']['smsNotification']['endDate']
                },
                "priorityPackage": {
                    "enabled": json['contractInfo']['priorityPackage']['enabled'],
                    "autoRenewalActive": json['contractInfo']['priorityPackage']['autoRenewalActive'],
                    "enddate": json['contractInfo']['priorityPackage']['endDate']
                },
                "accountType": json['contractInfo']['identificationInfo'][0]['identificationLevel'],
                "blocked": json['contractInfo']["blocked"],
                "regdate": json['contractInfo']['creationDate'],
                "detectedIP": json['authInfo']['ip'],
                "email": json['authInfo']['boundEmail'],
                "language": json['userInfo']['language']
            }

        return d

    @asyncio.coroutine
    async def get_personal_info(self, account_number: str) -> dict:

        try:
            match self.proxies:

                case None:
                    async with httpx.AsyncClient(headers=self.headers) as client:
                        r = await client.get(f"https://edge.qiwi.com/identification/v1/persons/{account_number}/identification")

                        if r.status_code != 200:
                            raise InvalidTokenError("Invalid token used;")
                        
                        json = r.json()
                        await client.aclose()

                case _:
                    async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                        r = await client.get(f"https://edge.qiwi.com/identification/v1/persons/{account_number}/identification")

                        if r.status_code != 200:
                            raise InvalidTokenError("Invalid token used;")
                        
                        json = r.json()
                        await client.aclose()
        except Exception as e:
            raise InRequestError(e)

        if 'code' in json or 'errorCode' in json:
            raise APIError(json)

        d = {"names": {
                    "short": f"{str(json['firstName'])[0]}.{str(json['middleName'])[0]} {json['lastName']}",
                    "first_name": json['firstName'],
                    "middle_name": json['middleName'],
                    "last_name": json['lastName'],
                },
                "borndate": json['birthDate'],
                "id": json['passport'],
                "iin": json['inn']
            }

        return d

    @asyncio.coroutine
    async def get_accounts_limits(self, account_number: str, account_languge: str = 'ru') -> dict:

        dump = {}

        limit_types = ['TURNOVER', 'REFILL', 'PAYMENTS_P2P', 'PAYMENTS_PROVIDER_INTERNATIONALS', 'PAYMENTS_PROVIDER_PAYOUT', 'WITHDRAW_CASH']

        params = {}
        for i in limit_types:
            ind = limit_types.index(i)
            params[f'types[{ind}]'] = i
            try:
                match self.proxies:

                    case None:
                        async with httpx.AsyncClient(headers=self.headers) as client:
                            r = await client.get(f"https://edge.qiwi.com/qw-limits/v1/persons/{account_number}/actual-limits", params=params)

                            if r is None:
                                raise InvalidTokenError("Invalid token used;")
                            
                            json = r.json()
                            await client.aclose()

                    case _:
                        async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                            r = await client.get(f"https://edge.qiwi.com/qw-limits/v1/persons/{account_number}/actual-limits", params=params)

                            if r is None:
                                raise InvalidTokenError("Invalid token used;")
                            
                            json = r.json()
                            await client.aclose()
            except Exception as e:
                raise InRequestError(e)

            if 'code' in json or 'errorCode' in json:
                raise APIError(json)

            path1 = json['limits'][account_languge.upper()][0]

            dump[i] = {
                'currency': path1['currency'],
                'rest': path1['rest'],
                'max': path1['max'],
                'spent': path1['spent'],
                'interval': path1['interval']
            }

        return dump

    @asyncio.coroutine
    async def get_account_restriction(self, account_number: str) -> list:

        try:
            match self.proxies:

                case None:
                    async with httpx.AsyncClient(headers=self.headers) as client:
                        r = await client.get(f"https://edge.qiwi.com/person-profile/v1/persons/{account_number}/status/restrictions")

                        if r is None:
                            raise InvalidTokenError("Invalid token used;")
                        
                        json = r.json()
                        await client.aclose()

                case _:
                    async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                        r = await client.get(f"https://edge.qiwi.com/person-profile/v1/persons/{account_number}/status/restrictions")

                        if r is None:
                            raise InvalidTokenError("Invalid token used;")
                        
                        json = r.json()
                        await client.aclose()
        except Exception as e:
            raise InRequestError(e)

        if 'code' in json or 'errorCode' in json:
            raise APIError(json)


        return json

        

    @asyncio.coroutine
    async def create_account_dump(self) -> dict:

        """Get account info dump

        Developed by Nodu$ iNC.
        -----------------------

        Returns
        -------
            dict
        """

        st_time = time.time()

        dump = {
            "Info": {
                "time_check": None,
                "developer": "Nodu$ iNC."
            },
        }

        json = await self.get_basic_info()

        dump['basic'] = json

        json = await self.get_personal_info(dump['basic']['number']['number'])

        dump['personal'] = json

        dump['limits'] = await self.get_accounts_limits(dump['basic']['number']['number'], dump['basic']['language'])

        json = await self.get_account_restriction(dump['basic']['number']['number'])

        if json != []:
            dump['restrictions'] = {
                'restrictionCode': json[0]['restrictionCode'],
                'restrictionDescription': json[0]['restrictionDescription']
            }

        dump['Info']['time_check'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dump['Info']['time_elapsed'] = time.time() - st_time
        return dump
            

    @asyncio.coroutine
    async def account_balance(self) -> list:

        """
        Getting the balance from all accounts

        Developed by Nodu$ iNC.
        -----------------------

        Returns
        -------
            balance : list
        """

        balances = await self.get_balance()
        r = list()

        for i in balances:
            if i['balance'] is not None:
                r.append(i['balance']['amount'])

        return r

    @asyncio.coroutine
    async def get_balance(self) -> list:

        try:
            match self.proxies:
            
                case None:
                    
                    async with httpx.AsyncClient(headers=self.headers) as client:
                        
                        r = await client.get('https://edge.qiwi.com/funding-sources/v1/accounts/current')

                        if r is None:
                            raise InvalidTokenError("Invalid token used;")

                        json = r.json()
                        await client.aclose()
                case _:
                    async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                        r = await client.get('https://edge.qiwi.com/funding-sources/v1/accounts/current')

                        if r is None:
                            raise InvalidTokenError("Invalid token used;")

                        json = r.json()
                        await client.aclose()
                    
        except Exception as e:
            raise InRequestError(e)

        if 'code' in json or 'errorCode' in json:
            raise APIError(json)

        balances = list()

        for account in json['accounts']:
            if account['hasBalance']:
                balances.append({
                    'type': account['type'],
                    'balance': account['balance']
                })

        return balances

    @asyncio.coroutine
    async def pay(self, account: str, amount: float, currency: str = '643', comment: str = None, tp: str = 'Account', acc_id: str = '643'):

        """
        Transfer money from an account to another qiwi account

        Args
        ----
            account : str // Transfer to number in qiwi system
            amount : float or int // Transfer amount
            currency : str // Transfer currency
            comment : str  // Transfer comment
            tp : str // Transfer type
            acc_id : str

        Developed by Nodu$ iNC.
        -----------------------

        Returns
        -------
            Server return

        """

        post_args = {
            "id": self._transaction_id,
            "sum": {
                "amount": amount,
                "currency": currency
            },
            "paymentMethod": {
                "type": tp,
                "accountId": acc_id
            },
            "fields": {
                "account": account
            }
        }

        if comment is not None:
            post_args["comment"] = comment

        try:
            match self.proxies:

                case None:
                    async with httpx.AsyncClient(headers=self.headers) as client:
                        response = await client.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=post_args)
                        data = response.json()
                        await client.aclose()
                    
                
                case _:
                    async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                        response = await client.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=post_args)
                        data = response.json()
                        await client.aclose()
                        
        except Exception as e:
            raise InRequestError(e)        

        if 'code' in data or 'errorCode' in data:
            raise APIError(data)

        return data

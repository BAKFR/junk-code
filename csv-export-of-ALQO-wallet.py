
from decimal import Decimal
import requests


# Target wallet
wallet = '????????????????????????'


x = requests.get('https://explorer.alqo.org/api/wallettransactions/%s' % wallet)
y = x.json()


# Can be used to add 
special_addresses = {
    'coinbase': 'MN/mining reward'
}

# CoinTracking need 3 times the currency column (for Buy, Sell and Fees)
print('Type;Date;Amount;Fee;TxId;Comment;Currency;Currency;Currency')


for tx in y['txs']:
    vin = [vin['amount'] for vin in tx['vin'] if vin['addresses'] == wallet]
    vout = [vout['amount'] for vout in tx['vout'] if vout['addresses'] == wallet]

    if len(vin) + len(vout) != 1:
        print('WARNING: unusual tx %s. It will be ignored' % tx.txid)

    if vin:
        if len(tx['vout']) != 1:
            source = '%s wallet(s)' % len(tx['vout'])
        else:
            source = special_addresses.get(tx['vout'][0]['addresses'], tx['vout'][0]['addresses'])
        #print('OUT -> %s\ttx=%s\tTo %s' % (vin[0], tx['txid'], source))
        #print('OUT; %s; %s; %s' % (vin[0], tx['txid'], source))
        print('Withdrawal;%s;-%.8f;0;%s;%s;ALQO;ALQO;ALQO' % (tx['timestamp'], Decimal(vin[0]) / 100000000, tx['txid'], 'To %s' % source))

    if vout:
        if len(tx['vin']) != 1:
            dest = '%s wallet(s)' % len(tx['vout'])
        else:
            dest = special_addresses.get(tx['vin'][0]['addresses'], tx['vin'][0]['addresses'])
        #print('IN <- %s\ttx=%s\tFrom %s' % (vout[0], tx['txid'], dest))
        #print('IN; %s; %s; %s' % (vout[0], tx['txid'], dest))
        print('Deposit;%s;%.8f;0;%s;%s;ALQO;ALQO;ALQO' % (tx['timestamp'], Decimal(vout[0]) / 100000000, tx['txid'], 'From %s' % dest))

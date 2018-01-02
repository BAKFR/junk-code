
from decimal import Decimal
import requests


# Target wallet
wallet = '???????????'


http_response = requests.get('https://explorer.alqo.org/api/wallettransactions/%s' % wallet)
json_data = http_response.json()


special_addresses = {
    'coinbase': 'MN/mining reward'
}


result = [];


for tx in json_data['txs']:
    vin = [vin['amount'] for vin in tx['vin'] if vin['addresses'] == wallet]
    vout = [vout['amount'] for vout in tx['vout'] if vout['addresses'] == wallet]

    line = {
        'tx-id': tx['txid'],
        'id': '%s-%s' % (tx['txid'], wallet), # Tx ID isn't sufficient because an ALQO transaction can appear several times (once per wallet)
        'timestamp': tx['timestamp'],
        'currency': 'ALQO'
    }
    
    if len(vin) + len(vout) != 1:
        print('WARNING: unusual tx %s. It will be ignored' % tx.txid)
        continue

    if vin:
        if len(tx['vout']) != 1:
            source = '%s wallet(s)' % len(tx['vout'])
        else:
            source = special_addresses.get(tx['vout'][0]['addresses'], tx['vout'][0]['addresses'])

        fee = sum([v_in['amount'] for v_in in tx['vin']]) - sum([v_out['amount'] for v_out in tx['vout']])
        line.update({
            'type': 'Withdrawal',
            'amount': - Decimal(vin[0]) / 100000000,
            'fee': Decimal(fee) / 100000000,
            'comment': 'To %s' % source,
        })

    if vout:
        if len(tx['vin']) != 1:
            dest = '%s wallet(s)' % len(tx['vout'])
        else:
            dest = special_addresses.get(tx['vin'][0]['addresses'], tx['vin'][0]['addresses'])

        line.update({
            'type': 'Deposit',
            'amount': Decimal(vout[0]) / 100000000,
            'fee': 0,
            'comment': 'From %s' % dest,
        })
    result.append(line)


# CoinTracking need 3 times the currency column (for Buy, Sell and Fees)
print('Type;Date;Amount;Fee;Id;Comment;Currency;Currency;Currency')
for line in result:
    print('%(type)s;%(timestamp)s;%(amount).8f;%(fee)s;%(id)s;%(comment)s;%(currency)s;%(currency)s;%(currency)s' % line)

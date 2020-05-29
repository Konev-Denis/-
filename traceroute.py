import subprocess
import re
from prettytable import PrettyTable


def traceroute(ip):
    print('подождите...')
    traceroute = subprocess.run(["tracert", '-d', ip], stdout=subprocess.PIPE, encoding='cp1251').stdout
    ips = re.findall(r'\d+\.\d+\.\d+\.\d+', traceroute)
    return ips


def whois(ips):
    asns = []
    countrys = []
    mnt_by = []
    for ip in ips:
        result = subprocess.run(["curl", "https://whois.ru/" + ip], stdout=subprocess.PIPE, encoding='utf-8', stderr=subprocess.STDOUT).stdout
        asn = re.findall(r'AS\d+', result)
        country = re.findall(r'ountry:\s+(.*)', result)
        mnt = re.findall(r'mnt-by:\s+(.*)', result)
        if asn:
            asn = asn[0]
        else:
            asn = ""
        asns.append(asn)
        if country:
            country = country[0]
        else:
            country = ""
        countrys.append(country)
        if mnt:
            mnt = mnt[0]
        else:
            mnt = ""
        mnt_by.append(mnt)
    print("\nРезультат")
    return [ips, asns, countrys, mnt_by]


def write_result(info):
    table = PrettyTable(['№', 'IP', 'AS', 'country', 'provider'])
    for i in range(len(info[0])):
        table.add_row([i, info[0][i], info[1][i], info[2][i], info[3][i]])
    print(table)

    


if __name__ == '__main__':
    print('Трассировка автономных систем.')
    print('Введите доменное имя или IP адрес.')
    ip = input()
    write_result(whois(traceroute(ip)))

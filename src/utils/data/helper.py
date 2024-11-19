with open('addresses.txt', 'r', encoding='utf-8-sig') as file:
    addresses = [line.strip() for line in file]

with open('proxies.txt', 'r', encoding='utf-8-sig') as file:
    proxies = [line.strip() for line in file]
    if not proxies:
        proxies = [None for _ in range(len(addresses))]

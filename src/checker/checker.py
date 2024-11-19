import pyuseragents

from src.utils.request_client.request_client import RequestClient
from src.utils.proxy_manager import Proxy


async def get_superform_data(address: str, proxy: Proxy | None) -> tuple[str, float, dict]:
    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
        'origin': 'https://xpcalc.superform.xyz',
        'priority': 'u=1, i',
        'referer': 'https://xpcalc.superform.xyz/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': pyuseragents.random(),
    }

    while True:
        request_client = RequestClient(proxy)
        response_json = await request_client.make_request(
            method='GET',
            url=f'https://api.superform.xyz/superrewards/seasonXP/1/{address}',
            headers=headers,
        )
        season_boosted_xp_final = response_json["seasonBoostedXPFinal"]
        tournaments = response_json.get("tournaments", [])

        super_fren_data = {}

        for tournament in tournaments:
            super_fren = tournament.get("superFren")
            highest_tier = tournament.get("highestTierHeld")
            super_fren_data[super_fren] = highest_tier

        return address, season_boosted_xp_final, super_fren_data

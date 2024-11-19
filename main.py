from asyncio import run, set_event_loop_policy
import asyncio
import logging
import sys

from loguru import logger
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from config import MOBILE_PROXY, ROTATE_IP
from src.checker.checker import get_superform_data
from src.utils.data.helper import proxies, addresses
from src.utils.proxy_manager import Proxy

if sys.platform == 'win32':
    set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.getLogger("asyncio").setLevel(logging.CRITICAL)


async def prepare_proxy(proxy: str) -> Proxy | None:
    if proxy:
        change_link = None
        if MOBILE_PROXY:
            proxy_url, change_link = proxy.split('|')
        else:
            proxy_url = proxy

        proxy = Proxy(proxy_url=f'http://{proxy_url}', change_link=change_link)

        if ROTATE_IP and MOBILE_PROXY:
            await proxy.change_ip()

        return proxy


async def main() -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Superform Data"
    headers = [
        "address",
        "total points",
        "SuperChad",
        "SuperApe",
        "SuperWhale",
        "SuperFrog",
        "SuperDino",
        "SuperSnake",
        "SuperHog",
    ]
    sheet.append(headers)

    proxy_index = 0

    for address in addresses:
        proxy = proxies[proxy_index]
        proxy_index = (proxy_index + 1) % len(proxies)
        proxy = await prepare_proxy(proxy)
        address, xp_final, super_fren_data = await get_superform_data(address, proxy)
        row = [
            address,
            xp_final,
            super_fren_data.get("SuperChad", "N/A"),
            super_fren_data.get("SuperApe", "N/A"),
            super_fren_data.get("SuperWhale", "N/A"),
            super_fren_data.get("SuperFrog", "N/A"),
            super_fren_data.get("SuperDino", "N/A"),
            super_fren_data.get("SuperSnake", "N/A"),
            super_fren_data.get("SuperHog", "N/A"),
        ]
        sheet.append(row)

    for column_index, column_cells in enumerate(sheet.columns, start=1):
        max_length = 0
        for cell in column_cells:
            if cell.value is not None:
                max_length = max(max_length, len(str(cell.value)))
        column_letter = get_column_letter(column_index)
        sheet.column_dimensions[column_letter].width = max_length + 2

    workbook.save("superform_data.xlsx")
    logger.success("Excel file 'superform_data.xlsx' has been saved!")


if __name__ == '__main__':
    run(main())

# oec-scrape
Interact with Observatory of Economic Complexity API data


Interact with OEC world data
https://oec.world/


Grab import/export data by country, or search for [HS4 codes](https://www.trade.gov/harmonized-system-hs-codes)


Usage:
```python
from oec_scrape import search_hs4, TradeType, get_countries_by_product
product = 'soybeans'
hs4 = search_hs4(product)
print(product, hs4)

import_df = get_countries_by_product( TradeType.IMPORT, hs4 = hs4, year=2020 )
export_df = get_countries_by_product( TradeType.EXPORT, hs4 = hs4, year=2020 )

print(import_df.head())
print(export_df.head())
```

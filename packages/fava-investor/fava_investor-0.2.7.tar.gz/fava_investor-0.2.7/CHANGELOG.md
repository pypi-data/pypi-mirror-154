# Changelog

## 0.2.5 (2022-06-12)
### New
- ticker-util. See [here](https://groups.google.com/g/beancount/c/eewOW4HQKOI)

### Improvements
- tlh: allow specifying tlh_partner meta label. [Red S]
- tlh: also consider substantially similar tickers in wash sale computations. [Red S]
- tlh docs. [Red S]
- tlh new feature: wash_ids. [Red S]
- tlh wash_id: configurable metadata label, bugfixes. [Red S]
- tlh: what not to buy now includes similars. [Red S]
- rename env var to BEAN_COMMODITIES_FILE. [Red S]


### Other

- build: requirements via pigar. [Red S]
- doc: create changelog + gitchangelog config. [Red S]
- doc: examples. [Red S]
- doc: README upate. Relaxed requirements. [Red S]
- refactor: favainvestorapi cleanup. [Red S]
- refactor: upgrade deprecated asyncio code. [Red S]
- ticker-util: and ticker-relate: major refactor into a single utility. [Red S]
- ticker-util: available keys. [Red S]
- ticker-util: click: relate subcommand group. [Red S]
- ticker_util: feature: add from commodities file. [Red S]
- ticker-util: feature add: include undeclared. [Red S]
- ticker-util: features: specify metadata, appends as cli args. [Red S] also: empty substsimilar metadata is excluded
- ticker-util: header. [Red S]
- ticker-util: moved to click. [Red S]


## 0.2.4 (2022-05-12)


### Other

- tlh: bug in wash sale (31 vs 30 days) [Red S]
- Flake. [Red S]
- Pythonpackage workflow. [Red S]
- . [Red S]
- tlh: sort main table by harvestable losses. [Red S]

## 0.2.3 (2022-05-11)


### Improvements

- TLH: screenshot update. [Red S]
  - Example update for article. [Red S]
  - tlh: html notes. [Red S]
  - tlh: rename subst to alt. [Red S]
  - tlh: clarify safe to harvest date. [Red S]
  - tlh: sort by harvestable loss. [Red S]
  - tLh: add built in options for account_field. [Red S]
  - tlh README. [Red S]
  - add subst column to TLH "Losses by Commodity" [Red S]
  - Show tlh alternate. [Red S]
  - tlh: show get one but leaf. [Red S]


## 0.2.2 (2022-04-27)
### Improvements
- Add long/short info to TLH. [Red S]
- Asset allocation by class: add multi currency support #32. [Red S]
  - requires all operating currencies to be specified

### Fixes
- Fix for upstream changes: Use `url_for` instead of `url_for_current` [Aaron Lindsay]
- Unbreak account_open_metadata. #35 [Martin Michlmayr]
- Support fava's newly modified querytable macro. [Aaron Lindsay]

### Other
- README updates, including #55. [Red S]
- Example account hierarchy update. [Red S]
- Fix assetalloc_class pytests. [Red S]
- tlh fix pytests. [Red S]

## 0.2.1 (2021-01-10)
- Macro asset_tree fix to make toggling work in fava v1.15 onwards. [Red S]
- Table update to include footer (can't merge this until fava release) [Red S]

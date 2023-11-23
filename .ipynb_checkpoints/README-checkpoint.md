# companiesScraper
## Get the financial data of public companies

### Nowadays, access to the accounting and financial statements of public companies is through web applications that have a common service, where the base service is limited to 5 years of accounting-financial history. Therefore, if you want to have full access, you need to pay or search for the information manually in the companies' reports. This motivated me to make a script that automatically searches for the data on different websites and saves it in .csv files ready to be analyzed.

### In turn this is part of a larger Fundamental Business Analysis project.

### Los datos se obtienen ejecutando el archivo "data_getter.py" con alguna de las siguientes opciones:

  -h, --help            show this help message and exit
  
  -s SECTOR, --sector SECTOR
                        Sector of companies
  -i INDUSTRY, --industry INDUSTRY
                        Industry of companies
  --capmorethan CAPMORETHAN
                        Capitalization higher than
  --caplessthan CAPLESSTHAN
                        Capitalization lower than
  -t [TICKERS ...], --tickers [TICKERS ...]
                        List of tickers
  -f {cash_flow,income,balance,ratios,all}, --finance {cash_flow,income,balance,ratios,all}
  
  -k KEY, --key KEY     Free key of 'https://site.financialmodelingprep.com/.'

### You can download the data according to sector, industry, indicating some capitalization value, or directly the tickers of interest. At the same time, you can indicate whether you want the cash flow, the income, the balance sheet or the ratios. The default option downloads everything.

### The only necessary condition is to have a free key from https://site.financialmodelingprep.com/. 






import pandas as pd
import requests
import json
import time

class Companies():
    
    def __init__(self,tickers=None,output_format="df",**kargs):
        self.tickers = tickers
        self.data = None
        self.screner_data = kargs
        self.output_format = output_format
        self.URL = f'https://stockrow.com/api/companies/'
        _requests_indicators = requests.get("https://stockrow.com/api/indicators.json").text
        self.indicators = json.loads(_requests_indicators)   
        if self.tickers==None:
            #if tickers have not been set manually, call the screener
            self._companies_screener()        
        pass
    
    def _companies_screener(self):
        api_request = (requests.get(f"https://financialmodelingprep.com/api/v3/stock-screener?apikey={fin_prep_api}",
                                    params=self.screner_data))
        data_json = json.loads(api_request.text)
        self.tickers = [company["symbol"] for company in data_json]
        
    def get_data(self,financial,period="A"):
            fin = []    
            financial_to_download = self._process_financial_input(financial)

            if type(self.tickers) == list:
                for ticker in self.tickers:
                    income_url = self.URL+f'{ticker}/financials.json?ticker={ticker}&dimension={period}&section={financial_to_download}'
                    #get the data
                    api_requests = requests.get(income_url)                
                    #process data if response is ok
                    if api_requests.status_code == 200:
                        #get the json and create a df
                        data = json.loads(api_requests.text)
                        data = pd.DataFrame(data)
                        # preprocess the response of the api for posterior convinience
                        data = self.pipe(data,ticker,financial)
                        #add the df to a list of dfs
                        fin.append(data)
                        time.sleep(0.3)
                    else: print(f'Error downloading income for {ticker}',api_requests.status_code)     
          

            return pd.concat([d for d in fin])
        
    def _process_financial_input(self,financial):
        #Depending on the financial stament the user want, modify the string to adapt the url
            if financial.lower() in "income":
                financial_to_download = "Income+Statement"
            elif financial.lower() in "balance":
                financial_to_download = "Balance+Sheet"
            elif financial.lower() in "metrics" or financial.lower() in "ratios":
                financial_to_download = "Metrics" 
                scale = False
            else: financial_to_download = "Cash+Flow" 
            return financial_to_download
   
    def _preprocess_data(self,data):
        df = data.T.copy()
        df.columns = df.loc["name"]
        df.drop(["name"],inplace=True)
        return df
        
    def _merge_ids(self,data,indicators):
        indicators = pd.DataFrame(indicators)
        return data.merge(indicators[["id","name"]],on="id").drop(["id"],axis=1)      
    
    def _preprocess_dataFormat(self,df,ticker,financial):
        df = df.T.copy()
        #modify columns names
        df.columns = df.loc["name"]
        #drop the old name column
        df.drop(["name"],inplace=True)
        #add year, column and reset index
        df["year"] = pd.to_datetime(df.index).year
        df.reset_index(inplace=True,drop=True)
        df["ticker"] = ticker
        #change the name index of the columns
        df.columns.name = financial
        return df
    
    def pipe(self,data,ticker,financial):
        # steps of data preprocessing
        df = (
              pd.DataFrame(data)
              .pipe(self._merge_ids,self.indicators)
              .pipe(self._preprocess_dataFormat,ticker,financial)
            .pipe(self._preprocess_numerical)
            .pipe(self._preprocess_nan)
             )
        return df

    def _preprocess_numerical(self,df):
        # Convert string columns to floats
        NUM_COLUMNS = df.columns[~df.columns.isin(["year","ticker"])]
        df[NUM_COLUMNS] = df[NUM_COLUMNS].astype("float")

        return df
    
    def _preprocess_nan(self,df):
        return df.fillna(0)
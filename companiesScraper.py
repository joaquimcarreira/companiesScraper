import pandas as pd
import requests
import json
import time
from tqdm import tqdm


class Companies():
    
    def __init__(self,tickers=None,key=None,**kargs):
        self.tickers = tickers
        self.data = None
        self.screner_data = kargs   
        self.error_companies = []
        self.key = key
        self.URL = f'https://stockrow.com/api/companies/'
        _requests_indicators = requests.get("https://stockrow.com/api/indicators.json").text
        self.indicators = pd.DataFrame(json.loads(_requests_indicators))

        if self.tickers==None:
            #if tickers have not been set manually, call the screener
            self._companies_screener()  

        pass
    
    def _companies_screener(self):
        api_request = (requests.get(f"https://financialmodelingprep.com/api/v3/stock-screener?apikey={self.key}",
                                    params=self.screner_data))
        data_json = json.loads(api_request.text)
        self.tickers = [company["symbol"] for company in data_json]


    def get_data(self,financial,output_path=None,period="A"):
            fin = []    
            financial_to_download = self._process_financial_input(financial)

            if type(self.tickers) == list:
                for ticker in tqdm(self.tickers):

                    url = self.URL+f'{ticker}/financials.json?ticker={ticker}&dimension={period}&section={financial_to_download}'
                    #get the data
                    api_requests = requests.get(url)                
                    #process data if response is ok
                    if api_requests.status_code == 200:
                        #get the json and create a df
                        data = json.loads(api_requests.text)
                        #data = pd.DataFrame(data)
                        # preprocess the response of the api for posterior convinience
                        try:
                            data = self.pipe(data,ticker,financial)
                            #add the df to a list of dfs
                            fin.append(data)
                        except:
                            self.error_companies.append(ticker)  
                            continue
                            
                        time.sleep(0.3)
                    else: self.error_companies.append(ticker)    
            data = pd.concat([d for d in fin])     
            if output_path:
                self.save_as_csv(data,output_path)
            return data
        
    def _process_financial_input(self,financial):
        #Depending on the financial stament the user want, modify the string to adapt the url
            if financial.lower() in "income":
                financial_to_download = "Income+Statement"
            elif financial.lower() in "balance":
                financial_to_download = "Balance+Sheet"
            elif financial.lower() in "metrics" or financial.lower() in "ratios":
                financial_to_download = "Metrics" 
                
            else: financial_to_download = "Cash+Flow" 
            return financial_to_download
    
    def save_as_csv(self,df,name):
        df.to_csv(name)
        
   
    def _preprocess_data(self,data):
        df = data.T.copy()
        df.columns = df.loc["name"]
        df.drop(["name"],inplace=True)
        return df
        
    def _merge_ids(self,data,indicators):
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
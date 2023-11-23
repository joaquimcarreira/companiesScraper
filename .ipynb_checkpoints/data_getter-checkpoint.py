from companiesScraper import Companies
import argparse

parse = argparse.ArgumentParser(description="inputs to get the companies data")
parse.add_argument("-s","--sector",type=str,help="Sector of companies")
parse.add_argument("-i","--industry",type=str,help="Industry of companies")
parse.add_argument("--capmorethan",type=int, help="Capitalization higher than")
parse.add_argument("--caplessthan",type=int, help="Capitalization lower than")
parse.add_argument("-t","--tickers",nargs="*",type=str,help="List of tickers")
parse.add_argument("-f","--finance",type=str,choices=["cash_flow","income","balance","ratios","all"],default="all")
parse.add_argument("-k","--key",type=str,help="Free key of 'https://site.financialmodelingprep.com/.' ")

args = parse.parse_args()
if args.key == None:
    print("******* PLEASE INDICATE YOUR FREE KEY ********")
    
else: 
    companies = Companies(tickers=args.tickers,key=args.key,sector=args.sector,marketCapMoreThan=args.capmorethan,
                      marketCapLowerThan=args.caplessthan,Industry=args.industry)
if args.finance=="all":
    for financial in ["cash_flow","income","balance","ratios"]:
        print(f"DOWNLOADING: {financial}")
        companies.get_data(financial=financial,output_path=f'{financial}.csv')
else:
    companies.get_data(financial=args.finance,output_path=f'{args.finance}.csv')

import Account;     import Data
import Run as r;    import datetime as dt

if __name__ == '__main__':
    
    # 1. Read in existing accounting information from QuestradeAPI
    accessed = input('Have you accessed the account today? (Y/N)    ')
    while accessed != ('Y') and ('N'):
        accessed = input('Please enter Y or N:  ')
    
    if accessed == 'N':
        refreshToken = input('Please enter the refresh token:    ')
    else:
        refreshToken = 0

    myAccount = Account.Account('Account #Here')
    myAccount.get_account(accessed, refreshToken)
    
    # 2. Retrieve stock data from yahoo finance
    update = input('Would you like to update the stock data? (Y/N)  ')
    
    #Data.get_raw_data()
    
    # 3. Find trading opportunities and put them in the Orders csv file
    print('Searching stocks...')
    # change this to the last business day
    r.scan(myAccount, 1, dt.date(2020, 5, 8))

    print("END PROGRAM")
   
    
    


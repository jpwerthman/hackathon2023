import pandas as pd
from pandas import json_normalize

data = {
        "transactions": [
        {
            "id": 10445599011,
            "amount": -400.00,
            "accountId": 7010861877,
            "customerId": 7006556796,
            "status": "active",
            "description": "Transfer to SAVINGS",
            "postedDate": 1665230400,
            "transactionDate": 1665230400,
            "createdDate": 1697321501,
            "categorization": {
                "normalizedPayeeName": "transfer",
                "category": "Transfer",
                "bestRepresentation": "TRANSFER TO SAVINGS",
                "country": "USA"
            }
        },
        {
            "id": 10445598891,
            "amount": 400.00,
            "accountId": 7010861876,
            "customerId": 7006556796,
            "status": "active",
            "description": "Transfer to SAVINGS",
            "postedDate": 1665230400,
            "transactionDate": 1665230400,
            "createdDate": 1697321500,
            "categorization": {
                "normalizedPayeeName": "transfer",
                "category": "Transfer",
                "bestRepresentation": "TRANSFER TO SAVINGS",
                "country": "USA"
            }
        },
        {
            "id": 10445599065,
            "amount": 3858.00,
            "accountId": 7010861877,
            "customerId": 7006556796,
            "status": "active",
            "description": "IRS TREAS 310 TAX REF",
            "memo": "PPD ID: 1234567897",
            "postedDate": 1665057600,
            "transactionDate": 1665057600,
            "createdDate": 1697321501,
            "categorization": {
                "normalizedPayeeName": "Irs Treas",
                "category": "Federal Tax",
                "bestRepresentation": "IRS TREAS TAX REF PPD ID",
                "country": "USA"
            }
        },
        {
            "id": 10445598999,
            "amount": 1189.51,
            "accountId": 7010861877,
            "customerId": 7006556796,
            "status": "active",
            "description": "Mad Science Research PR PAYMENT",
            "memo": "PPD ID: 1234567899",
            "postedDate": 1665057600,
            "transactionDate": 1665057600,
            "createdDate": 1697321501,
            "categorization": {
                "normalizedPayeeName": "Mad Science Research",
                "category": "Paycheck",
                "bestRepresentation": "MAD SCIENCE RESEARCH PR PAYMENT PPD ID",
                "country": "USA"
            }
        },
        {
            "id": 10445598433,
            "amount": 300.00,
            "accountId": 7010861874,
            "customerId": 7006556796,
            "status": "active",
            "description": "Employee Contribution",
            "postedDate": 1664971200,
            "transactionDate": 1664971200,
            "createdDate": 1697321497,
            "categorization": {
                "normalizedPayeeName": "Contribution",
                "category": "Dividend & Cap Gains",
                "bestRepresentation": "EMPLOYEE CONTRIBUTION",
                "country": "USA"
            },
            "investmentTransactionType": "contribution"
        },
        {
            "id": 10445599098,
            "amount": 760.00,
            "accountId": 7010861877,
            "customerId": 7006556796,
            "status": "active",
            "description": "REMOTE ONLINE DEPOSIT #",
            "memo": "1",
            "postedDate": 1664712000,
            "transactionDate": 1664712000,
            "createdDate": 1697321501,
            "categorization": {
                "normalizedPayeeName": "Remote Online",
                "category": "Deposit",
                "bestRepresentation": "REMOTE ONLINE DEPOSIT",
                "country": "USA"
            }
        },
        {
            "id": 10445598981,
            "amount": 2013.69,
            "accountId": 7010861877,
            "customerId": 7006556796,
            "status": "active",
            "description": "ROCKET SURGERY PAYROLL",
            "memo": "PPD ID: 1234567892",
            "postedDate": 1664625600,
            "transactionDate": 1664625600,
            "createdDate": 1697321501,
            "categorization": {
                "normalizedPayeeName": "Rocket Surgery",
                "category": "Paycheck",
                "bestRepresentation": "ROCKET SURGERY PAYROLL PPD ID",
                "country": "USA"
            }
        },
        {
            "id": 10445598517,
            "amount": 26.63,
            "accountId": 7010861875,
            "customerId": 7006556796,
            "status": "active",
            "description": "Income Dividend Reinvestment",
            "postedDate": 1664452800,
            "transactionDate": 1664452800,
            "createdDate": 1697321498,
            "categorization": {
                "normalizedPayeeName": "Reinvestment",
                "category": "Dividend & Cap Gains",
                "bestRepresentation": "INCOME DIVIDEND REINVESTMENT",
                "country": "USA"
            },
            "investmentTransactionType": "reinvestOfIncome"
        },
    ]
}

def JSONtoCSV(data):
    # Normalize the json data
    df = json_normalize(data['transactions'])

    # print(df.columns)

    selected_columns = ['amount', 'description',
        'postedDate', 'transactionDate', 'createdDate',
        'categorization.normalizedPayeeName', 'categorization.category',
        'categorization.bestRepresentation', 'categorization.country']
    new_df = df[selected_columns]
    csv_string = new_df.to_csv(index=False)
    print(csv_string)
    return csv_string

JSONtoCSV(data)
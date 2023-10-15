import openai
import json
import os


key = os.environ.get("OPENAI_API_KEY")


print(key)
class Bot:
    def __init__(self):
        self.available_functions = {
            "get_transaction_info": self.get_transaction_info,
        }
        self.transaction_data = '''
amount,description,postedDate,transactionDate,createdDate,categorization.normalizedPayeeName,categorization.category,categorization.bestRepresentation,categorization.country
-400.0,Transfer to SAVINGS,1665230400,1665230400,1697321501,transfer,Transfer,TRANSFER TO SAVINGS,USA
400.0,Transfer to SAVINGS,1665230400,1665230400,1697321500,transfer,Transfer,TRANSFER TO SAVINGS,USA
3858.0,IRS TREAS 310 TAX REF,1665057600,1665057600,1697321501,Irs Treas,Federal Tax,IRS TREAS TAX REF PPD ID,USA
1189.51,Mad Science Research PR PAYMENT,1665057600,1665057600,1697321501,Mad Science Research,Paycheck,MAD SCIENCE RESEARCH PR PAYMENT PPD ID,USA
300.0,Employee Contribution,1664971200,1664971200,1697321497,Contribution,Dividend & Cap Gains,EMPLOYEE CONTRIBUTION,USA
760.0,REMOTE ONLINE DEPOSIT #,1664712000,1664712000,1697321501,Remote Online,Deposit,REMOTE ONLINE DEPOSIT,USA
2013.69,ROCKET SURGERY PAYROLL,1664625600,1664625600,1697321501,Rocket Surgery,Paycheck,ROCKET SURGERY PAYROLL PPD ID,USA
26.63,Income Dividend Reinvestment,1664452800,1664452800,1697321498,Reinvestment,Dividend & Cap Gains,INCOME DIVIDEND REINVESTMENT,USA'''

    def get_transaction_info(self):
        return self.transaction_data

    def run_conversation(self, initial_message):
        # The initial message is the user's message

        templateMessage = f'''
                You are an expert financial manager and you are a helpful AI that will help users with questions about their transactional data, you are given a csv file as a string with the following data: amount, description of transaction, etc..
                User's question:
                {initial_message}

                Data:
                {self.transaction_data} 

                You will respond to the user like you are talking to them,
                for example: if they ask, tell me about my transfers
                you will respond with the following:
                it looks like you have made 2 transfers, the first one was for 400 dollars and the second one was for 400 dollars... this is just an example of how you would respond to the user
                other than that, you can respond to the user however you want, just make sure you are answering their question
                '''
        messages = [{"role": "system", "content": templateMessage}]
        messages.append({"role": "user", "content": initial_message})

        # Using the chat completion method for the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )

        response_message = response.choices[0].message
        if "get_transaction_info" in response_message["content"]:
            function_name = "get_transaction_info"
            function_response = self.available_functions[function_name]()

            messages.extend([
                response_message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            ])
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )
            return second_response.choices[0].message["content"]
        else:
            return response_message["content"]
The instructions on the provided document were slightly vague, I have made the following assumtions to deal with this.

The list of fruits and vegetables was missing so I have labled the training data and stored it in the file as a dictonary.
The REST API input and output format was not specified so I have assumed that files will still be provided as input and the output
needs in JSON format. For this I have used swagger UI so you can test the returned JSON objects as you wish.

Setup Instructions:
Create a MySQL database with any name on your local machine under localhost.
Open a terminal window in the directory of the repositoy and run:
python api.py <MySQL_username> <MySQL_password> <MySQL_DataBase> <Location of people.json> <Location of companies.json>
This line takes 5 arguments:
First argument is your MySQL Username
Second argument is you MySQL Password
Thrid argument is your MySQL database name
Fourth argument is the location of the people.json file
Fifth argument is the location of the companies.json file

For the last 2 arguments to make it easier you can simply move the files into the repository and just pass the names of the files isntead of location
Example: python api.py root root hive people.json companies.json

Next either open in the browser the address http://127.0.0.1:8000/ or you can open the file API_Page in the repository

Usage Instructions:
Click on the default dropdown and you should be able to use 3 functions.
To test the API simply selecct a fucntion to try out and click the 'Try it out' button
You will be prompted for the required parameters.
All other usefull information about the API is also listed in this interface, along with the result.

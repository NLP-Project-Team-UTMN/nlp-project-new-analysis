<p align="center">
      <img src="logotype.png" width="700">
</p>


## About

Analysis of the tonality of the text of oil and gas industry news and their impact on quotes.

Made as part of a training project on the discipline of natural language processing.


## Developers

- Khrupin Danila (https://github.com/DanilaStanislavovich)
- Tamerlan Muradov (https://github.com/Tam7k)
- Ovchinnikova Anna (https://github.com/OvchinnikovAnna)

## Description of files
<p>
      <a href="/parser.py">parser.py</a> - the code of the site parser for the purpose of collecting news for the year.
      In this case, the year variable is the desired year. As a result of its execution, a csv file is created where the name of the news with the release time is      
      indicated.
</p>   
<p>
      <a href="/addition_of_the_table.py">addition_of_the_table.py</a> - code to supplement the table with such data as: the text of the news, the stock price at the time of the news release, the time in 3 hours, the stock price 3 hours after the news release, as well as calculating the difference in this interval and classifying the news into good and bad (depending on the price change)
</p>

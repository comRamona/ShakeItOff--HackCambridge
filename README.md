https://devpost.com/software/receipt2fitbit 

To run: 
```
pip install -r requiremenets.txt
```
Set the API keys in `./runcommand.sh`, then run:
```
source ./runcommand.sh
```


## Inspiration
Tracking your diet is a good way to stay fit and healthy, but the major apps require that you type in what you have written. This is a huge inconvenience and can be very annoying. We envision a way to simplify this process by providing a way to extract all the information from your receipts and working out how many calories you need to burn after that delicious brownie that you just really needed to get. 

## What it does
 
We provide a clean and easy to use UI that allows you to take a picture of your receipt. Our app analyses the receipt and works out how many calories are in every item you ordered. From this, we work out what your daily step goal should be to make sure you're staying healthy and integrate with FitBit to upload your daily goal so you can keep track of your progress and stay motivated. This requires minimal user effort, as all they need to do is snap a pic and they will receive a customised exercise goal on their FitBit. 

## How we built it

We split our task in 7 big tasks:

**Parsing Receipts**
We use the _Microsoft Azure OCR API_ to extract text from pictures of the receipt. We developed an _Azure ML Studio_ pipeline to clean our data and delete items that we were very confident wouldn't represent food items: prices, tax information, payment information, etc.

**SpellChecking**
We use the _Bing SpellCheck API_ to correct OCR errors. 

**Classifying items**
The next step is to look at all the items we identified and figure out which ones represent food items and which ones are just miscellaneous items. We used _Azure ML Studio_ to train an _SVM_ that labels items as food or not food. 

**Analysing the nutritional information**
We used a nutrition database provided by Nutritionix to look up calories. 

**Computing your fitness goals**
We worked out a formula to convert the number of extra calories into a fitness goal that will motivate you for the day. 

**Integrating with FitBit**
We want our users to have easy access to insights into how their food habits affect their calorie intake. Integrating with FitBit seems like an obvious step to provide useful, real-time updates on their calorie and exercise goals, tailored to their specific diet. 

**Building a lovely, user-friendly web interface**
Lastly, we wanted to round off our project with a clean, easy to use and responsive UI. We use a webapp hosted on flask and made public through ngrock for convenience.

## Next Steps
We have a quite a few ideas to take this further:

**1.** We would like to add support for other fitness trackers and smart watches

**2.** Bill Splitting - we know people often go out for meals and we want to find a way to itemise the receipt and assign items to the right person beforing computing the calorie amount

**3.** Giving users a more customised experience by analysing trends in their calorie intake so that our app can help them meet their goals faster.

## Challenges we ran into

Fitbit API documentation is very much out of date. 


## Accomplishments that we're proud of

We're very pleased with out idea and managing to stay awake all night! Also, happy that it all integrates together really well!

## What we learned

It was our first time using a fitbit and the FitBit API, so there were lots of challenges getting it all set up. 



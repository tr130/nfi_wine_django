#! /bin/bash

if [[ $1 == "test" ]]
then
  PSQL="psql --username=nfi_wine --dbname=nfi_wine_test -t --no-align -c"
else
  PSQL="psql --username=nfi_wine --dbname=nfi_wine -t --no-align -c"
fi

# Do not change code above this line. Use the PSQL variable above to query your database.
echo $($PSQL "TRUNCATE TABLE shopfront_wine")
cat stock.csv | while IFS="," read ID COLOR VARIETY COUNTRY YEAR NAME PRICE STOCKLEVEL DESCRIPTION
do
  if [[ $ID != id ]]
  then
    VAT=$PRICE*0.2
    TOTAL=$PRICE+$VAT
    INSERTED = $($PSQL "INSERT INTO shopfront_wine(name, year, color, variety, country, price_exvat, vat, price_incvat, stock_level, description) VALUES('$NAME', $YEAR, '$COLOR', '$VARIETY', '$COUNTRY', $PRICE, $VAT, $TOTAL, $STOCKLEVEL, '$DESCRIPTION')")
  fi
done

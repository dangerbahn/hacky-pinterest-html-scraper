EXTRACT TCIN data

run ```python soup.py```
the results will be stored in tcins.csv

if a TCIN exists in the pin description, use that TCIN.

if there is no TCIN in the pin description, check the pin link URL for a TCIN.

if there is no TCIN in either the pin description or the pin link URL, use the description text as a search term and grab the TCIN from the first result.

if the pin description text has less than 8 characters do not search for anything. There is not enough data to determine a TCIN.

if a TCIN is found and the Target API has returned product data for that TCIN, determine if that TCIN has color variations.

if the product has color variations, find one child TCIN for each color that exists.

A row is created for each TCIN found based on these rules.

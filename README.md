# AusAddressMatch

Address Matching for Australian Addresses. Compare Address A to Address B.

## Functionality

- Match postcode
- Match state (abbreviated and non abbreviated)
- Account for abbreviations ie `Street` and `St`
- Remove "noise" ie `Unit` `tower` `au`
- Remove punctuation

## Usage

```
from aussieaddress import Address


address1 = "U54 Loggins St, Kennytown, QLD 4123"
address2 = "U54 Loggins Street Kennytown 4123 Queensland"

# Initalise the Address Class
matcher = Address(address1=address1, address2=address2)

# Run Matching
matcher.run()

result = matcher.matched

# Show all options
print(matcher.__str__())

```

## Options

You can turn off postcode_check and state_check functionality, on by default

```
matcher.postcode_check = False
matcher.state_check = False
```


You can also set the match threshold which by default is 75

`matcher.threshold = 80`


### Updaing Replacements and Removals

To check the current removals

`matcher.removals`

Adding a new removal

`matcher.removals = "Plank"`


To check the current replacements

`matcher.replacements`

Adding a new replacement

`matcher.replacements = ["Stroad", "strd"]`


Note: with replacements each array is checked individually, with index 0 becoming the replacement value

Ie. `["Street", "st"]` with `123 test st` will become `123 test street`



## Authors

Jack Jorgensen
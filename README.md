# ufixtures
Utilities package to create fixtures for API test

## vcrpy  
Sanitize any part of `vcrpy` fixtures using regex
```python
from ufixtures.UfixVcr import *

ufixtures = UfixVcr(cassette_dir='fixtures/cassettes')
vcr = ufixtures.sanitize(attributes=['regex', 'for', 'attributes'],
                         targets=['other regex', 'for', 'targets'])

with vcr.use_cassette('fixture_name.yml'):
    # your request here
```
Your cassette will have 'OBSCURED' string in place of the info you want to hide.  
`attributes` is a list of `yaml` sections you want to search  
`targets` is a list of substrings in the **values** of `yaml` which you want to obscure from your cassette  
In any case 'OBSCURED' will replace the (sub-)strings in the values of your `yaml` cassette.  


## betamax  
Sanitize **headers** in the betamax fixtures. Filtering other parts of cassette is in development.  
# gender-gap

Prototype to analyze gender gap using Linkedin info.

## Run the scrapper

You need git, python3 and firefox (geckodriver).

```sh
git clone git@github.com:palmerabollo/gender-gap.git
cd gender-gap

pip3 install -r requirements.txt
export LINKEDIN_USERNAME=xxx
export LINKEDIN_PASSWORD=xxx

# scrape data from Linkedin. DO NOT run this because it might go against the terms of service.
python3 scrapper.py > output.log
cat output.log | grep -v "DEBUG" | grep . > output_filtered.log

# analyze the results and generate a report
python3 parser.py
```

## Example output

<img src="/examples/gender_gap_valladolid.png" alt="Gender gap in Valladolid (Spain)" />

Thanks to [Javier García](https://github.com/jgarciab) for his contributions.

## LICENSE

GNU General Public License.
Some parts of the code are based on [eracle/linkedin](https://github.com/eracle/linkedin).

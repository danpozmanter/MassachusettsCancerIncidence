# Massachusetts Cancer Incidence

Processes word documents divided by city/town groupings into generated json files,
adding in relevant data (averages, rankings by standardized incidence ratio, and combined male/female data for an overview of rates across sexes).

Provides a simple static site using Bootstrap 5 and JQuery to make make it easier to see relevant data in context on a city by city basis to help get a rough sense of cancer incidence across Massachusetts.

**Disclaimer** This data is sourced from [MA Cancer Incidence City Town Supplement](https://www.mass.gov/lists/cancer-incidence-city-town-supplement) with additional data (averages, combined data, and rankings) provided "as-is". The reasons for an elevated rate (overall or for a specific cancer) could vary wildly - so take this data as a starting point, and not any sort of definitive assessment of cancer risk for a city.

## Instructions

### Update Data

Load up your virtual environment, and `pip install -r requirements.txt`.

From the root directory:

`update.sh`

### Run Locally

From the site directory:

`python3 -m http.server 8000`


## Information

### Observed and Expected Case Counts

The **observed** case count (Obs) for a particular type of cancer in a city/town is the actual number
of newly diagnosed cases among residents of that city/town for a given time period.

A city/town’s **expected** case count (Exp) for a certain type of cancer for this time period is a
calculated number based on that city/town’s population distribution (by sex and among eighteen
age groups) for the time period 2011-2015, and the corresponding statewide average annual agespecific incidence rates.
The source of the city and town population data for the 2011-2015 period was the US Census American Community Survey (ACS), an ongoing national survey that provides demographic estimates on a yearly basis.

### Standardized Incidence Ratios

A **Standardized Incidence Ratio (SIR)** is an indirect method of adjustment for age and sex that describes in numerical terms how a city/town’s cancer experience in a given time period compares with that of the state as a whole.

* An SIR of exactly 100 indicates that a city/town’s incidence of a certain type of cancer is
equal to that expected based on statewide average age-specific incidence rates.

* An SIR of more than 100 indicates that a city/town’s incidence of a certain type of cancer
is higher than expected for that type of cancer based on statewide average annual agespecific incidence rates. For example, an SIR of 105 indicates that a city/town’s cancer
incidence is 5% higher than expected based on statewide average annual age-specific
incidence rates.

* An SIR of less than 100 indicates that a city/town’s incidence of a certain type of cancer is
lower than expected based on statewide average age-specific incidence rates. For
example, an SIR of 85 indicates that a city/town’s cancer incidence is 15% lower than
expected based on statewide average annual age-specific incidence rates.

### Statistical Significance and Interpretation of SIRs

The interpretation of the SIR depends on both how large it is and how stable it is. Stability in this
context refers to how much the SIR changes when there are small increases or decreases in the
observed or expected number of cases. Two SIRs may have the same size but not the same
stability. For example, an SIR of 150 may represent 6 observed cases and 4 expected cases, or
600 observed cases and 400 expected cases. Both represent a 50 percent excess of observed
cases. However, in the first instance, one or two fewer cases would change the SIR a great deal,
whereas in the second instance, even if there were several fewer cases, the SIR would only
change minimally. When the observed and expected numbers of cases are relatively small, their
ratio is easily affected by one or two cases. Conversely, when the observed and expected
numbers of cases are relatively large, the value of the SIR is stable.

A 95 percent confidence interval (CI) has been presented for each SIR in this report (when the
observed number of cases is at least 5), to indicate if the observed number of cases is significantly
different from the expected number, or if the difference is most likely due to chance. A
confidence interval is a range of values around a measurement that indicates the precision of the
measurement. In this report, the 95% confidence interval is the range of estimated SIR values
that has a 95% probability of including the true SIR for a specific city or town. If the 95%
confidence interval range does not include the value 100.0, then the number of observed cases is
significantly different from the expected number of cases. “Significantly different” means there
is at most a 5% chance that the difference between the number of observed and expected cancer
cases is due solely to chance alone. If the confidence interval does contain the value 100.0, there
is no significant difference between the observed and expected numbers. Statistically, the width
of the interval reflects the size of the population and the number of events; smaller populations
and smaller observed numbers of cases yield less precise estimates that have wider confidence
intervals. Wide confidence intervals indicate instability, meaning that small changes in the
observed or expected number of cases would change the SIR a great deal.

- https://www.mass.gov/doc/cancer-incidence-in-massachusetts-citytown-supplement-2011-2015/download
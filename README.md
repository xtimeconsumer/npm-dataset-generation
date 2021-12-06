# NPM Repository Data Set Genertion

This was a dataset generated to pull public repository attributes about a the top 10,000 most popular NPM packages for analysis. The initial goal was numeric prediction and nominal classification around security advisories to identify key attributes for consideration in just-in-time supply chain analysis of third party dependencies. Ultimately there were know key public attributes that were statistically significant enough to build confidence to a packages overall security posture. 

## How The Data Was Generated

The data was generated using various APIs and then aggregated, including [Deps.dev - OSI](https://deps.dev), [GitHub API](https://api.github.com), and [npms.io](https://api.npms.io). Each API was chosen for the data consistency and reliability and that the data was fed downstream from overlapping sources. Here is how the scripts put this together.

1. **scrape-npm-couchdb.js**
	* This was an initial attempt to pull data directly out of NPM. Ultimately the event stream did not seem to refresh at a reasonable rate and it was to unreliable. A downstream project, called `all-the-package-names` was selected for convience as the package names were already sorted by depdenants.
2. **select-10000-package-names.js**
	* Simple script to pull the top 10,000 packages and push them into a JSON file.
3. **pull-initial-npm-git-data.sh**
	* This file takes the package names from above and reaches out to npms.io to pull a baseline set of data that has most of the github and repository information.
4. **repository-urls-sparse.sh**
	* Takes files where the initial url data was empty and pulls the repository URL. It then was normalized with regex as some of the URLS were in a git or git+https format. This data pull allowed us to identify some non-GitHub projects which were ultimately discarded.
5. **enhance-github-details.sh**
	* Some of the GitHub data from npms.io was missing so repos that had missing data such as stars, watchers, forks, etc. were re-pulled directly from the GitLab API.
6. **fixed-moved-repos.sh**
	* On the GitLab API response from the step above, if a repo is moved it will generate a JSON response that has the new URL. So data that retuned an empty set when Jq attempted the parse. This script parsed out the redirect url. At this step, URLs that were empty with no data were considered `abandoned` which means they were either deleted or the URL was unmappable. This was a strategic choice since the URL from NPM was what most folks would use to find the dependency.
7. **github-details-updated-links.sh**
	* Similar to step five, this goes back and fixes the sparse data from the redirect links. A potential improvement would be to have steps 5-7 be combined in one python script that handles REST response codes properly and marks the data accordingly.
8. **scrape-security-advisories.py**
	* Because [deps.dev](https://deps.dev) lacks a public API and is a javascript driven site, we had to use a Selenium Chromium driver to pull the advisory count.

## Data Challanges

The dataset represents a point in time of the security advisories and is not a complete picture of the security health of overall project. Further only 13% of the entire dataset has an advisories. As such it's really difficult to draw any accurate conclusions and the data poorly correlates.

## Future Considerations

I think this set serves as a good starting point for others who are interested in deriving more information about repositories such as if there are other attributes in the dataset that correlate or if additional APIs could bring more attributes into the fold. For exmaple, topic tagging wold be ideal. Potential problems in the future might be around assessing project health and DevOps related to repository popularity.

## Dataset

Available on [kaggle](https://www.kaggle.com/mikelanciano/top-npm-github-repositories).

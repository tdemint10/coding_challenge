# Coding Challenge App

A coding challenge solution to get the Git Profile for a user/organization

## Install:

Create the virtual environment with conda:
```
conda env create -f environment.yaml
source activate user-profiles
```

Add the requirements:
```
pip install -r requirements.txt
```

*Note: I have not used conda in the past, so I am not sure whether the* requirements.txt *contents could have been combined in the* environment.yaml *. Due to this, the pip install step is necessary for setup.*

## Running the code

### Spin up the service

```
# start up local server
python -m run
```


### Health Check

```
curl -i "http://127.0.0.1:5000/health-check"
```

## Request Examples

### Bitbucket Profile Request

```
curl -i GET "http://127.0.0.1:5000/api/bitbucket/profile?team=mailchimp"
```

**Params**
- team **(required)** - Name of the Bitbucket team that you want to retrieve the profile of


### GitHub Profile Request

```
curl -i GET "http://127.0.0.1:5000/api/github/profile?organization=mailchimp" \
--header "X-GITHUB-TOKEN: {{token}}"
```

**Headers**
- X-GITHUB-TOKEN - User generated token from GitHub. Recommended to avoid rate limits on the GitHub API. Create token here: [GitHub Tokens](https://github.com/settings/tokens)

**Params**
- organization **(required)** - Name of the GitHub organization that you want to retrieve the profile of


### Git Profile Request

```
curl -i GET "http://127.0.0.1:5000/api/profile?githubOrganization=mailchimp&bitbucketTeam=mailchimp" \
--header "X-GITHUB-TOKEN: {{token}}"
```

**Headers**
- X-GITHUB-TOKEN - User generated token from GitHub. Recommended to avoid rate limits on the GitHub API. Create token here: [GitHub Tokens](https://github.com/settings/tokens)

**Params**
- bitbucketTeam **(required)** - Name of the Bitbucket team that you want to retrieve the profile of
- githubOrganization **(required)** - Name of the GitHub organization that you want to retrieve the profile of


## Next Steps

- Implement caching on requests to improve speed
- Implement retry logic for failed API requests
- Improve error handling for different possible API responses
- Increase negative path testing

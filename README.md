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
- Run GitHub requests in parallel to improve speed
- Implement retry logic for failed API requests
- Improve error handling to cover more possible errors
- Increase negative path testing

## Testing Plan

### GitHub / Bitbucket Modules

**service.py**
- Mock external API calls
- Happy Path - 200 Status, data returned - profile returned successfully
- Negative Path - 200 Status, no data returned - empty profile returned
- Negative Path - 403 Status - throw ForbiddenException
- Negative Path - Connection error - throw Exception
- Negative Path - Internal error - throw Exception

**schema.py**
- Happy path - pass in correctly formatted dict - schema created successfully
- Negative path - pass in improperly formatted dict - throw error

**controller.py**
- Mock internal service calls
- Happy path - correct request - profile returned successfully, 200 Status
- Negative Path - args not included - throw error, 400 Status
- Negative Path - Forbidden thrown - throw error, 403 Status
- Negative Path - Internal error - throw error, 500 Status

### Profile Module

**service.py**
- Mock internal service calls
- Happy Path - data returned from modules - combined profile returned successfully
- Negative Path - module failed - throw Exception
- Negative Path - module throws ForbiddenException - throw ForbiddenException
- Negative Path - Internal error - throw Exception

**schema.py**
- Happy path - pass in correctly formatted dict - schema created successfully
- Negative path - pass in improperly formatted dict - throw error

**controller.py**
- Mock internal service calls
- Happy path - correct request - profile returned successfully, 200 Status
- Negative Path - args not included - throw error, 400 Status
- Negative Path - GitHub forbidden - throw error, 403 Status
- Negative Path - Bitbucket forbidden - throw error, 403 Status
- Negative Path - internal error - throw error, 500 Status

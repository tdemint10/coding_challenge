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

### Swagger

[Git Profile API](http://127.0.0.1:5000/)

The Git Profile API Documentation can be seen generated automatically on this Swagger page. The requests can also be run directly here.

## Request Examples

*Note: I highly recommend generating a GitHub Token ([Create Token](https://github.com/settings/tokens)), otherwise the rate limit will greatly reduce the amount of times you can run these requests*

### Bitbucket Profile Request

```
curl -i "http://127.0.0.1:5000/bitbucket/profile?team=mailchimp"
```

**Params**
- team **(required)** - Name of the Bitbucket team that you want to retrieve the profile of


### GitHub Profile Request

```
curl -i "http://127.0.0.1:5000/github/profile?organization=mailchimp" \
--header "X-GITHUB-TOKEN: {{token}}"
```

**Headers**
- X-GITHUB-TOKEN - User generated token from GitHub. Recommended to avoid rate limits on the GitHub API. Create token here: [GitHub Tokens](https://github.com/settings/tokens)

**Params**
- organization **(required)** - Name of the GitHub organization that you want to retrieve the profile of


### Git Profile Request

```
curl -i "http://127.0.0.1:5000/profile/?githubOrganization=mailchimp&bitbucketTeam=mailchimp" \
--header "X-GITHUB-TOKEN: {{token}}"
```

**Headers**
- X-GITHUB-TOKEN - User generated token from GitHub. Recommended to avoid rate limits on the GitHub API. Create token here: [GitHub Tokens](https://github.com/settings/tokens)

**Params**
- bitbucketTeam **(required)** - Name of the Bitbucket team that you want to retrieve the profile of
- githubOrganization **(required)** - Name of the GitHub organization that you want to retrieve the profile of


## Next Steps

- Improve speed
  - Add caching
  - Run external requests in parallel
- Error handling
  - Add retry logic on failed external requests (when necessary)
  - Extend Exceptions to handle more cases
  - Improve error messages
- Functionality
  - Add header for Bitbucket API access token
  - Input validation
  - Abstract individual modules from the GitProfileService to simplify extending in the future
- Testing (see below)

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

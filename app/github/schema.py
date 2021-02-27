from marshmallow import fields, Schema


class GitHubProfileSchema(Schema):
    """ GitHub Profile Schema """

    user = fields.String(attribute="user")
    followerCount = fields.Integer(attribute="follower_count")
    repoCount = fields.Integer(attribute="repo_count")
    originalRepoCount = fields.Integer(attribute="original_repo_count")
    forkedRepoCount = fields.Integer(attribute="forked_repo_count")
    languages = fields.List(fields.String(), attribute="languages")
    topics = fields.List(fields.String(), attribute="topics")
    watchersCount = fields.Integer(attribute="watchers_count")

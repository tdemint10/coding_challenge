from marshmallow import fields, Schema


class BitbucketProfileSchema(Schema):
    """ Bitbucket Profile Schema """

    repoCount = fields.Integer(attribute="repo_count")
    languages = fields.List(fields.String(), attribute="languages")
    watchersCount = fields.Integer(attribute="watchers_count")

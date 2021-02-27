from marshmallow import fields, Schema


class GitProfileSchema(Schema):
    """ Git Profile Schema """

    followerCount = fields.Integer(attribute="follower_count")
    repoCount = fields.Integer(attribute="repo_count")
    originalRepoCount = fields.Integer(attribute="original_repo_count")
    forkedRepoCount = fields.Integer(attribute="forked_repo_count")
    languages = fields.List(fields.String(), attribute="languages")
    languageCount = fields.Integer(attribute="language_count")
    topics = fields.List(fields.String(), attribute="topics")
    topicCount = fields.Integer(attribute="topic_count")
    watchersCount = fields.Integer(attribute="watchers_count")

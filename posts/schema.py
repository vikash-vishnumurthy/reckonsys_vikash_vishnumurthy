import graphene
from graphene_django import DjangoObjectType
from .models import Post,Comment
import datetime

#####  TYPES #####

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id','post','text','author')

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id','title','description','publish_date','author','comments','age_of_post')
    
    age_of_post = graphene.String()
    comments = graphene.List(CommentType)

    def resolve_comments(self,info):
        return Comment.objects.filter(post=self.id)    

    def resolve_age_of_post(self,info):
        year = int(self.publish_date.strftime("%Y"))
        month = int(self.publish_date.strftime("%m"))
        date = int(self.publish_date.strftime("%d"))
        return 'Old Post' if datetime.datetime(year,month,date) < datetime.datetime(2021,1,29) else 'New Post'

#####  QUERIES #####

class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType,id=graphene.Int())

    def resolve_posts(self,info):
        return Post.objects.all()

    def resolve_all_comments(self,info):
        return Comment.objects.all()

    def resolve_post(self,info,id):
        if id is not None:
            return Post.objects.get(pk=id)

#####  MUTATIONS #####

class PostCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        author = graphene.String(required=True)

    post = graphene.Field(PostType)
    
    def mutate(self, info, title, description, author):
        post = Post.objects.create(title = title, description = description, author = author)
        return PostCreateMutation(post=post)

class PostUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        title = graphene.String()
        description = graphene.String()
        author = graphene.String()

    post = graphene.Field(PostType)
    
    def mutate(self, info, id, title=None, description=None, author=None):
        try:
            post = Post.objects.get(pk = id)
            if title is not None:
                post.title = title
            if description is not None:
                post.description = description
            if author is not None:
                post.author = author
            post.save()
            return PostUpdateMutation(post=post)
        except :
            raise ValueError('The Post that you are trying to update does not exists')

class CommentCreateMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        text = graphene.String(required=True)
        author = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    
    def mutate(self, info, post_id, text, author):
        try:
            post_object = Post.objects.get(pk=post_id)
            comment = Comment.objects.create(post = post_object, text = text, author = author)
            return CommentCreateMutation(comment=comment)
        except :
            raise ValueError('The Post that you are trying to comment does not exists')

class CommentDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)

    deleted_comment = graphene.Field(CommentType)

    def mutate(self,info,id):
        try:
            delete_comment_object = Comment.objects.get(pk=id)
            Comment.objects.get(pk=id).delete()
            return CommentDeleteMutation(deleted_comment = delete_comment_object)
        except :
            raise ValueError('This Comment does not exists or it has been already deleted')

class Mutation:
    create_post = PostCreateMutation.Field()
    update_post = PostUpdateMutation.Field()
    create_comment = CommentCreateMutation.Field()
    delete_comment = CommentDeleteMutation.Field()


    

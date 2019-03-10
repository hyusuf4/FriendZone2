from django.db import models
import uuid

# Create your models here.

class Author(models.Model):
    author_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    firstName=models.CharField(max_length=30)
    lastName=models.CharField(max_length=30)
    userName=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    hostName=models.URLField()
    githubUrl=models.URLField()
    
    def __str__(self):
        return self.userName



class FriendRequest(models.Model):
    from_author= models.ForeignKey(Author,on_delete=models.CASCADE, related_name="friend_request_sent",null=True)
    to_author=models.ForeignKey(Author,on_delete=models.CASCADE, related_name="friend_request_recieved",null=True)
    created=models.DateTimeField()
    accepted=models.BooleanField(default=False)
    regected=models.BooleanField(default=False)
    
    def __str__(self):
        return "You recieved a friend request from %s to %s"%(self.from_author, self.to_author)

class Friends(models.Model):
    author1=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='friend1',null=True)
    author2=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='friend2',null=True)
    date=models.DateTimeField()

class Post(models.Model):
    PERMISSION_OPTIONS = (
        ("M", "me"),
        ("L", "permitted authors"),
        ("F", "my friends"),
        ("FF", "friends of friends"),
        ("FH", "friends on my host"),
        ("P", "public")
    )
    contentTypeChoice = (
        ('text/markdown', 'text/markdown'),
        ('text/plain', 'text/plain'),
        ('application/base64', 'application/base64'),
        ('image/png;base64', 'image/png;base64'),
        ('image/jpeg;base64', 'image/jpeg;base64'),
    )
    postid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.URLField(null=True, blank=True)
    origin = models.URLField(null=True, blank=True)
    contentType = models.CharField(max_length=32, choices=contentTypeChoice,default='text/plain' )
    publicationDate=models.DateTimeField(db_column='publicationDate')
    content=models.TextField()
    title=models.CharField(max_length=50)
    permission = models.CharField(max_length=2, choices=PERMISSION_OPTIONS, default='P')
    permitted_authors = models.TextField(null=True) 
    unlisted=models.BooleanField(default=False)
    author= models.ForeignKey(Author,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    contentTypeChoice = (
        ('text/markdown', 'text/markdown'),
        ('text/plain', 'text/plain'),
        ('application/base64', 'application/base64'),
        ('image/png;base64', 'image/png;base64'),
        ('image/jpeg;base64', 'image/jpeg;base64'),
    )
    comment=models.TextField()
    contentType = models.CharField(max_length=32, choices=contentTypeChoice,default='text/plain' )
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author=models.ForeignKey(Author, on_delete=models.CASCADE,null=True)
    postid=models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    published=models.DateTimeField('date published')
    
    def __str__(self):
        return self.comment

# class Image(models.Model):

#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
#     img = models.ImageField(null=True) 



from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField     
from read_statistics.models import ReadNumExpandMethod
'''
class test():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
'''
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):  #这个很关键，有了它，前端页面就能让文字很好显示出来

        return self.type_name
        


class Blog(models.Model,ReadNumExpandMethod):
    title=models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content=RichTextUploadingField()    #它控制后台的富文本编辑样式
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    '''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    '''    

    def __str__(self):

        return "<Blog：%s>" %self.title

    class Meta:
        ordering = ['-create_time']

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog,on_delete=models.DO_NOTHING)
'''
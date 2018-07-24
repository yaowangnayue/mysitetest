import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.utils import timezone
from django.db.models import Sum


def read_statistics_once_read(request,obj):
	ct = ContentType.objects.get_for_model(obj)
	key = "%s_%s_read" %(ct.model,obj.pk)
	if not request.COOKIES.get(key):
		#总阅读数+1 
		readnum,created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
		readnum.read_num += 1
		readnum.save()
		#当前阅读数+1
		date = timezone.now().date()
		readDetail,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
		readDetail.read_num += 1
		readDetail.save()
	return key


# def read_statistics_once_read(request,obj):
# 	ct = ContentType.objects.get_for_model(obj)
# 	key = "%s_%s_read" %(ct.model,obj.pk)
# 	if not request.COOKIES.get(key):
# 		if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
# 			readnum = ReadNum.objects.get(content_type=ct,object_id=obj.pk)
# 		else:
# 			readnum = ReadNum(content_type=ct,object_id=obj.pk)
# 		readnum.read_num += 1
# 		readnum.save()

# 		date = timezone.now().date()
# 		if ReadDetail.objects.filter(content_type=ct,boject_id=obj.pk,date=date).count():
# 			readDetail = ReadDetail.objects.get(content_type=ct,boject_id=obj.pk,date=date)
# 		else:
# 			readDetail = ReadDetail(content_type=ct,boject_id=obj.pk,date=date)


# 		readDetail.read_num += 1
# 		readDetail.save()
# 	return key


def get_sever_days_read_data(content_type):
	today = timezone.now().date()
	dates = []
	read_nums = []
	for i in range(7,0,-1):
		date = today - datetime.timedelta(days=i)
		dates.append(date.strftime('%m/%d'))
		read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
		result = read_details.aggregate(read_num_sum=Sum('read_num') )
		read_nums.append(result['read_num_sum'] or 0)
	return dates,read_nums

 
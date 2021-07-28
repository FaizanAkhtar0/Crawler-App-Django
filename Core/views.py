import json
import threading

from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_protect

from Core.Scrapper_libs.crawler import Crawler
from Core.models import Image, Document, SubURL, Content, MasterURL

cr = Crawler()
cr.set_thread()

def admin_dashboard(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def admin_crawl_status(request):
    if request.method == 'GET':
        sub_links = cr.queue
        return render(request, 'crawling-status.html', {'links': sub_links})


def start_crawler(request):
    if request.method == 'GET':
        if cr.start_queue_thread():
            return HttpResponse(json.dumps({'message': 'Crawler has started the Queue Thread!'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'message': 'Queue Thread is already executing...'}), content_type="application/json")
    else:
        return Http404


def stop_crawler(request):
    if request.method == 'GET':
        cr.stop_queue()
        return HttpResponse(json.dumps({'message': 'Crawler Service has been stopped!'}), content_type="application/json")
    else:
        return Http404


def get_updated_queue(request):
    if request.method == 'GET':
        queue_list = [model_to_dict(i) for i in cr.queue]
        return HttpResponse(json.dumps({'queue': queue_list}), content_type="application/json")


def create_dict(model):
    ret_dict = model_to_dict(model)
    ret_dict['content'] = model_to_dict(model.content)
    ret_dict['images'] = [model_to_dict(img) for img in Image.objects.filter(content=model.content)]
    ret_dict['documents'] = [model_to_dict(doc) for doc in Document.objects.filter(content=model.content)]
    return ret_dict


def get_updated_dequeue(request):
    if request.method == 'GET':
        dequeue_list = [create_dict(i) for i in SubURL.objects.filter(completed=True)]
        return HttpResponse(json.dumps({'dequeue': dequeue_list}), content_type="application/json")


def admin_url_status(request):
    if request.method == 'GET':
        return render(request, 'url-status.html')


def create_master_crawled_stats(model):
    master_id = model.id
    ret_dict = model_to_dict(model)
    ret_dict['page_count'] = SubURL.objects.filter(master_url=master_id).count()
    ret_dict['status'] = SubURL.objects.filter(completed=True).count()
    return ret_dict


def create_sub_crawled_stats(model):
    ret_dict = model_to_dict(model)
    ret_dict['images'] = Image.objects.filter(content=model.content).count()
    ret_dict['documents'] = Document.objects.filter(content=model.content).count()
    return ret_dict


def admin_crawled_data(request):
    if request.method == 'GET':
        master_links = [create_master_crawled_stats(master) for master in MasterURL.objects.all()]
        sub_links = [create_sub_crawled_stats(sub) for sub in SubURL.objects.all()]
        return render(request, 'crawled-data.html', {'master_links': master_links, 'sub_links': sub_links})



@csrf_protect
def index(request):
    if request.method == 'GET':
        return render(request, 'user-index.html')


def user_link_post(request):
    if request.method == 'POST':
        web_link = request.POST.get('web_link')
        page_depth = int(request.POST.get('page_depth'))

        cr.set_link_thread(web_link, page_depth)
        if cr.start_link_acquisition_thread():
            return render(request, 'user-index.html', {
                'message': 'MasterURL with the provided page depth has been submitted to the server!'})
        else:
            return render(request, 'user-index.html', {
                'message': 'Server is already processing the previously provided MasterURL'})
    elif request.method == 'GET':
        return render(request, 'user-index.html')
    else:
        Http404


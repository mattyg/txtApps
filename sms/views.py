from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import logging

from sms.models import Message, Gateway

@csrf_exempt
def update_delivery_status(request):
    logging.debug("Status update received.")
    logging.debug("%s" % request.GET)
    data = {}
    for k,v in request.GET.items():
        if isinstance(v, list) and len(v) == 1:
            data[k] = v[0]
        else:
            data[k] = v
    
    logging.debug('%s' % data)
    
    msg = Message.objects.get_matching_message(data)
    
    if not msg:
        logging.error("%s" % data)
        logging.error("Message could not be found.")
        return HttpResponse('OK')
        
    logging.debug("Found message %i" % msg.pk)
    gateway = msg.gateway
    
    if  not gateway.status_mapping or (
        request.GET.get(gateway.status_status) not in gateway.status_mapping.keys()
    ):
        msg.status = "Failed"
    else:
        msg.status = gateway.status_mapping[data.get(gateway.status_status)]
    logging.debug("Updated status to %s" % msg.status)
    if msg.status == "Delivered":
        if gateway.status_date_format:
            msg.delivery_date = datetime.datetime.strptime(
                data.get(gateway.status_date),
                gateway.status_date_format,
            )
        else:
            msg.delivery_date = datetime.datetime.fromtimestamp(
                float(data.get(gateway.status_date))
            )
        logging.debug("Message was delivered at %s" % msg.delivery_date)
    else:
        msg.status_message = data.get(gateway.status_error_code)
        logging.debug("Error message was %s" % msg.status_message)
    msg.save()
    return HttpResponse('OK')

@csrf_exempt
def handle_reply(request):
    logging.debug("SMS Reply received.")
    data = {}
    for k,v in request.GET.items():
        if isinstance(v, list) and len(v) == 1:
            data[k] = v[0]
        else:
            data[k] = v
    
    msg = Message.objects.get_original_for_reply(data)
    
    if not msg:
        logging.error("%s" % data)
        logging.error("Original message could not be found.")
        return HttpResponse('OK')
        
    logging.debug("Found message %i" % msg.pk)
    gateway = msg.gateway
    if gateway.reply_date_format:
        reply_date = datetime.datetime.strptime(
            data.get(gateway.reply_date),
            gateway.reply_date_format,
        )
    else:
        reply_date = datetime.datetime.fromtimestamp(float(
            data.get(gateway.reply_date)
        ))
        
    reply = msg.replies.create(
        content=data.get(gateway.reply_content),
        date=reply_date,
    )
    logging.debug("Reply created")

    logging.debug("Message content was: %s" % reply.content)
    
    if msg.reply_callback:
        logging.debug("Callback found, running that.")
        msg.reply_callback(reply)
    
    return HttpResponse('OK')
from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

import uuidfield.fields
import picklefield

from gateway import Gateway

class MessageManager(models.Manager):
    def get_matching_message(self, datadict):
        for gateway in Gateway.objects.all():
            try:
                return Message.objects.get(
                    gateway_message_id=datadict.get(gateway.status_msg_id),
                    gateway=gateway,
                )
            except Message.DoesNotExist:
                pass
    
    def get_original_for_reply(self, datadict):
        for gateway in Gateway.objects.all():
            try:
                return Message.objects.get(
                    uuid=datadict.get(gateway.uuid_keyword),
                    gateway=gateway
                )
            except Message.DoesNotExist:
                pass
        # This may have been a message sent from another phone, but
        # there may be a reply-code that was added in.
        return self.custom_reply_matcher(datadict)
    
    def custom_reply_matcher(self, datadict):
        # Designed to be overridden.
        return None
                
MESSAGE_STATUSES = (
    ('Unsent', 'Unsent'),
    ('Sent', 'Sent'),
    ('Delivered', 'Delivered'),
    ('Failed', 'Failed'),
)
class Message(models.Model):
    """
    A Message.
    
    We have a uuid, which is our reference. We also have a gateway_message_id,
    which is their reference.  This is required by some systems so we can 
    pass in a unique value that will allow us to match up replies to original
    messages.
    """
    
    content = models.TextField(help_text=_(u'The body of the message.'))
    recipient_number = models.CharField(max_length=32, 
        help_text=_(u'The international number of the recipient, without the leading +'))
    
    sender = models.ForeignKey('auth.User', related_name='sent_sms_messages')
    send_date = models.DateTimeField(null=True, blank=True, editable=False)
    delivery_date = models.DateTimeField(null=True, blank=True, editable=False)
    uuid = uuidfield.fields.UUIDField(auto=True, help_text=_(u'Used for associating replies.'))
    
    status = models.CharField(max_length=16, choices=MESSAGE_STATUSES,
        default="Unsent",
    )
    status_message = models.CharField(max_length=128, null=True, blank=True)
    billed = models.BooleanField(default=False)
    
    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    billee = generic.GenericForeignKey()
    
    gateway = models.ForeignKey('sms.Gateway', 
        null=True, blank=True, editable=False)
    gateway_message_id = models.CharField(max_length=128, 
        blank=True, null=True, editable=False)
    
    reply_callback = picklefield.PickledObjectField(null=True, blank=True)
    
    objects = MessageManager()
    
    class Meta:
        app_label = 'sms'
        permissions = (
            ('view_message', 'Can view message'),
        )
    
    def send(self, gateway):
        gateway.send(self)
    
    @property
    def length(self):
        return len(self.content) / 160 + 1
    
    def __unicode__(self):
        return "[%s] Sent to %s by %s at %s [%i]" % (
            self.status,
            self.recipient_number,
            self.sender,
            self.send_date,
            self.length
        )
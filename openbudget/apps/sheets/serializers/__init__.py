from rest_framework import serializers
from openbudget.apps.accounts.serializers import AccountMin
from openbudget.apps.sheets import models
from openbudget.commons.serializers import UUIDRelatedField


class SheetItemCommentBaseSerializer(serializers.ModelSerializer):
    """
    Base SheetItemComment serializer, for creating new SheetItemComment instances.
    """

    user = UUIDRelatedField()

    class Meta:
        model = models.SheetItemComment
        fields = ['comment', 'user']


class SheetItemCommentReadSerializer(SheetItemCommentBaseSerializer):
    """
    Read SheetItemComment serializer, for listing/retrieving SheetItemComment instances.
    """

    user = AccountMin()

    class Meta(SheetItemCommentBaseSerializer.Meta):
        fields = SheetItemCommentBaseSerializer.Meta.fields +\
                 ['uuid', 'item', 'created_on', 'last_modified']

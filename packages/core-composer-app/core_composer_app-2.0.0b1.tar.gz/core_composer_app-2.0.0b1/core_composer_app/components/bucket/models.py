"""Bucket model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

from core_composer_app.components.type_version_manager.models import TypeVersionManager
from core_main_app.commons import exceptions


class Bucket(models.Model):
    """Bucket class to store types by domain."""

    label = models.CharField(unique=True, max_length=200)
    color = models.CharField(unique=True, max_length=7, default=None)
    types = models.ManyToManyField(TypeVersionManager, default=[], blank=True)

    @staticmethod
    def get_by_id(bucket_id):
        """Return a bucket given its id.

        Args:
            bucket_id:

        Returns:

        """
        try:
            return Bucket.objects.get(pk=str(bucket_id))
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Return all buckets.

        Returns:

        """
        return Bucket.objects.all()

    @staticmethod
    def get_colors():
        """Return all colors.

        Returns:

        """
        return Bucket.objects.values_list("color", flat=True)

    def save_object(self):
        """Custom save

        Returns:

        """
        try:
            return self.save()
        except IntegrityError as e:
            raise exceptions.NotUniqueError(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def add_type(self, type_version_manager):
        """Add type to bucket.

        Args:
            type_version_manager:

        Returns:

        """
        self.types.add(type_version_manager)

    def remove_type(self, type_version_manager):
        """Remove type from bucket.

        Args:
            type_version_manager:

        Returns:

        """
        self.types.remove(type_version_manager)

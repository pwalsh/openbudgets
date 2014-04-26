import re
import datetime
import ckanclient
from django.conf import settings
from fabfile.utilities import notify
from openbudgets.apps.entities import models
from . import Push, PushFactory


class CKANPushFactory(PushFactory):

    """Push data to CKAN backends."""

    def __init__(self):
        sites = self.get_all_sites()
        #Syncs every site
        for index, site in enumerate(sites):
            self.factory(site)(index).sync()

    def get_all_sites(self):
        return [site['name'] for site in settings.OPENBUDGETS_CKAN_BACKENDS]

    def factory(self,class_name):
        #Return an objects of the sites that we want to sync
        classes = {
            'DataHub': DataHubPush
        }
        return classes[class_name]


class CKANPush(Push):

    """Push data to the given CKAN backend."""

    def __init__(self, site_index):
        self.site_index = site_index
        self.ckan = ckanclient.CkanClient(
            base_location=settings.OPENBUDGETS_CKAN_BACKENDS[site_index]['base_url'],
            api_key=settings.OPENBUDGETS_CKAN_BACKENDS[site_index]['api_key'])

    def sync(self):
        #connetes to the site
        entities = models.Entity.objects.all()
        #goes over all the entities and creates/updates them
        for entity in entities:
            sheets = entity.sheets.all()
            if sheets:
                package_name = self.parse_package_name(entity.name)
                try:

                    #Trying to get the entity
                    self.ckan.package_entity_get(package_name+'13')
                    package_entity = self.ckan.last_message

                #Creating a new entity if it does not exist
                except ckanclient.CkanApiNotFoundError:
                    package_entity = self.get_package_fields(package_name, entity.name)
                    try:
                        self.ckan.package_register_post(package_entity)
                        notify("Successfully created the new entity: %s" % package_name)
                    except ckanclient.CkanApiConflictError:
                        raise Exception('Entity name is not legal - %s' % package_name)
                        continue

                #Adding a new sheets to the package
                for sheet in sheets:
                    excited = False
                    #Checking if the sheet already exists in the entity
                    if 'resources' not in package_entity:continue
                    for resource in package_entity['resources']:

                        #Update the sheet in the package if it's not update
                        if str(sheet.period) in str(resource['name']):
                            excited = True
                            created = datetime.datetime.strptime(resource['created'], "%Y-%m-%dT%H:%M:%S.%f")

                            #Checking if the sheet in the entity its updated
                            if created <= sheet.created_on.replace(tzinfo=None):
                                package_entity['resources'].remove(resource)
                                self.ckan.package_entity_put(package_entity)
                                package_entity = self.update_resource(entity, sheet, package_name)
                            break

                    #If we need to create new sheet.
                    if not excited or not package_entity['resources']:
                        package_entity = self.update_resource(entity, sheet, package_name)
                    notify('Updated %s' % package_name)
        notify('Finished to push all the data!!!')

    def get_package_fields(self, package_name, entity_name ):
        """
        Return a dic that contains all the keys for the package
        """
        package_entity = {
            'name': package_name+'13',
            'notes': '%s %s' % (settings.OPENBUDGETS_CKAN_CONFIG['notes'], entity_name),
            'tags': settings.OPENBUDGETS_CKAN_CONFIG['tags'],
            'owner_org': settings.OPENBUDGETS_CKAN_CONFIG['owner_org'],
        }
        return package_entity

    def parse_package_name(self, name):
        """ Parsing the package name according to the rules of the site
        """
        return name

    def update_resource(self, entity, sheet, package_name):
        """ Update the resource of a given entity.
        """
        try:
            path = 'dev.openmuni.org.il/transport/export/sheet/%s/csv' % str(sheet.id)
            resource_name = '%s Budget and Actual %s' %(entity.name, str(sheet.period))
            descriptions = '%s %s for the year %s in a cav format' %(settings.OPENBUDGETS_CKAN_CONFIG['notes'], entity.name, str(sheet.period))
            self.ckan.add_package_resource(package_name, path, name=resource_name, description=descriptions, format='csv')
            self.ckan.package_entity_get(package_name)
            return self.ckan.last_message
        except ckanclient.CkanApiNotAuthorizedError:
            raise Exception('Not Authorized to edit the entity %s' % package_name)


class DataHubPush(CKANPush):

    """Push data to DataHub."""

    def parse_package_name(self, name):
        try:
            package_name = re.sub('[^0-9a-zA-Z_-]+', '', name.lower())+'-'
        except UnicodeEncodeError:
            package_name = str(name).replace("'", "").replace(" ", "-") + '-'
        return package_name

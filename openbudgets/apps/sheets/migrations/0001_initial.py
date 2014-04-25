# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('entities', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'Template'
        db.create_table(u'sheets_template', (
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, primary_key=True, db_index=True)),
            ('period_start', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('blueprint', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='instances', null=True, to=orm['sheets.Template'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sheets', ['Template'])

        # Adding M2M table for field divisions on 'Template'
        m2m_table_name = db.shorten_name(u'sheets_template_divisions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('template', models.ForeignKey(orm[u'sheets.template'], null=False)),
            ('division', models.ForeignKey(orm[u'entities.division'], null=False))
        ))
        db.create_unique(m2m_table_name, ['template_id', 'division_id'])

        # Adding model 'TemplateNode'
        db.create_table(u'sheets_templatenode', (
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['sheets.TemplateNode'])),
            ('id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, primary_key=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('comparable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('direction', self.gf('django.db.models.fields.CharField')(default='REVENUE', max_length=15, db_index=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sheets', ['TemplateNode'])

        # Adding M2M table for field inverse on 'TemplateNode'
        m2m_table_name = db.shorten_name(u'sheets_templatenode_inverse')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_templatenode', models.ForeignKey(orm[u'sheets.templatenode'], null=False)),
            ('to_templatenode', models.ForeignKey(orm[u'sheets.templatenode'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_templatenode_id', 'to_templatenode_id'])

        # Adding M2M table for field backwards on 'TemplateNode'
        m2m_table_name = db.shorten_name(u'sheets_templatenode_backwards')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_templatenode', models.ForeignKey(orm[u'sheets.templatenode'], null=False)),
            ('to_templatenode', models.ForeignKey(orm[u'sheets.templatenode'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_templatenode_id', 'to_templatenode_id'])

        # Adding model 'TemplateNodeRelation'
        db.create_table(u'sheets_templatenoderelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheets.Template'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sheets.TemplateNode'])),
        ))
        db.send_create_signal(u'sheets', ['TemplateNodeRelation'])

        # Adding unique constraint on 'TemplateNodeRelation', fields ['node', 'template']
        db.create_unique(u'sheets_templatenoderelation', ['node_id', 'template_id'])

        # Adding model 'Sheet'
        db.create_table(u'sheets_sheet', (
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, primary_key=True, db_index=True)),
            ('period_start', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('period_end', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sheets', to=orm['entities.Entity'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sheets', to=orm['sheets.Template'])),
            ('budget', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=26, decimal_places=2, blank=True)),
            ('actual', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=26, decimal_places=2, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(db_index=True, blank=True)),
        ))
        db.send_create_signal(u'sheets', ['Sheet'])

        # Adding model 'SheetItem'
        db.create_table(u'sheets_sheetitem', (
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['sheets.SheetItem'])),
            ('id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, primary_key=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('comparable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('direction', self.gf('django.db.models.fields.CharField')(default='REVENUE', max_length=15, db_index=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('budget', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=26, decimal_places=2, blank=True)),
            ('actual', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=26, decimal_places=2, blank=True)),
            ('sheet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['sheets.Sheet'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['sheets.TemplateNode'])),
            ('has_comments', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'sheets', ['SheetItem'])

        # Adding unique constraint on 'SheetItem', fields ['sheet', 'node']
        db.create_unique(u'sheets_sheetitem', ['sheet_id', 'node_id'])

        # Adding model 'SheetItemComment'
        db.create_table(u'sheets_sheetitemcomment', (
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, primary_key=True, db_index=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='discussion', to=orm['sheets.SheetItem'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item_comments', to=orm['accounts.Account'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'sheets', ['SheetItemComment'])


    def backwards(self, orm):
        # Removing unique constraint on 'SheetItem', fields ['sheet', 'node']
        db.delete_unique(u'sheets_sheetitem', ['sheet_id', 'node_id'])

        # Removing unique constraint on 'TemplateNodeRelation', fields ['node', 'template']
        db.delete_unique(u'sheets_templatenoderelation', ['node_id', 'template_id'])

        # Deleting model 'Template'
        db.delete_table(u'sheets_template')

        # Removing M2M table for field divisions on 'Template'
        db.delete_table(db.shorten_name(u'sheets_template_divisions'))

        # Deleting model 'TemplateNode'
        db.delete_table(u'sheets_templatenode')

        # Removing M2M table for field inverse on 'TemplateNode'
        db.delete_table(db.shorten_name(u'sheets_templatenode_inverse'))

        # Removing M2M table for field backwards on 'TemplateNode'
        db.delete_table(db.shorten_name(u'sheets_templatenode_backwards'))

        # Deleting model 'TemplateNodeRelation'
        db.delete_table(u'sheets_templatenoderelation')

        # Deleting model 'Sheet'
        db.delete_table(u'sheets_sheet')

        # Deleting model 'SheetItem'
        db.delete_table(u'sheets_sheetitem')

        # Deleting model 'SheetItemComment'
        db.delete_table(u'sheets_sheetitemcomment')


    models = {
        u'accounts.account': {
            'Meta': {'ordering': "['email', 'created_on']", 'object_name': 'Account'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'he'", 'max_length': '2'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'entities.division': {
            'Meta': {'ordering': "['index', 'name']", 'unique_together': "(('name', 'domain'),)", 'object_name': 'Division'},
            'budgeting': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'divisions'", 'to': u"orm['entities.Domain']"}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'index': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'entities.domain': {
            'Meta': {'ordering': "['name']", 'object_name': 'Domain'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'usd'", 'max_length': '3'}),
            'ground_surface_unit': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '25'}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'measurement_system': ('django.db.models.fields.CharField', [], {'default': "'metric'", 'max_length': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'entities.entity': {
            'Meta': {'ordering': "('division__domain', 'division__index', 'name')", 'unique_together': "(('name', 'parent', 'division'),)", 'object_name': 'Entity'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'to': u"orm['entities.Division']"}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['entities.Entity']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'sheets.sheet': {
            'Meta': {'ordering': "('entity', 'period_start')", 'object_name': 'Sheet'},
            'actual': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '26', 'decimal_places': '2', 'blank': 'True'}),
            'budget': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '26', 'decimal_places': '2', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sheets'", 'to': u"orm['entities.Entity']"}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'period_end': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'period_start': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sheets'", 'to': u"orm['sheets.Template']"})
        },
        u'sheets.sheetitem': {
            'Meta': {'ordering': "['node']", 'unique_together': "(('sheet', 'node'),)", 'object_name': 'SheetItem'},
            'actual': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '26', 'decimal_places': '2', 'blank': 'True'}),
            'budget': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '26', 'decimal_places': '2', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'comparable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'default': "'REVENUE'", 'max_length': '15', 'db_index': 'True'}),
            'has_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['sheets.TemplateNode']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sheets.SheetItem']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'sheet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['sheets.Sheet']"})
        },
        u'sheets.sheetitemcomment': {
            'Meta': {'ordering': "['user', 'last_modified']", 'object_name': 'SheetItemComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discussion'", 'to': u"orm['sheets.SheetItem']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item_comments'", 'to': u"orm['accounts.Account']"})
        },
        u'sheets.template': {
            'Meta': {'ordering': "['name']", 'object_name': 'Template'},
            'blueprint': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'instances'", 'null': 'True', 'to': u"orm['sheets.Template']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'divisions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'templates'", 'symmetrical': 'False', 'to': u"orm['entities.Division']"}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'period_start': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'sheets.templatenode': {
            'Meta': {'ordering': "['code', 'name']", 'object_name': 'TemplateNode'},
            'backwards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'forwards'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['sheets.TemplateNode']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'comparable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'default': "'REVENUE'", 'max_length': '15', 'db_index': 'True'}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'inverse': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'inverse_rel_+'", 'null': 'True', 'to': u"orm['sheets.TemplateNode']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sheets.TemplateNode']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'templates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nodes'", 'symmetrical': 'False', 'through': u"orm['sheets.TemplateNodeRelation']", 'to': u"orm['sheets.Template']"})
        },
        u'sheets.templatenoderelation': {
            'Meta': {'ordering': "['template__name', 'node__name']", 'unique_together': "(('node', 'template'),)", 'object_name': 'TemplateNodeRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sheets.TemplateNode']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sheets.Template']"})
        }
    }

    complete_apps = ['sheets']

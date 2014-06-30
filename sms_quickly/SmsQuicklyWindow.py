# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# !!!NOTES!!!
# - Jei rasomas tel nr, tai jam ir siusti, o ne ieskoti str(telnr) tarp kontaktu
# - messaging indicator integracija

from locale import gettext as _
from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('sms_quickly')
from sms_quickly_lib import Window
from sms_quickly.AboutSmsQuicklyDialog import AboutSmsQuicklyDialog
from sms_quickly.PreferencesSmsQuicklyDialog import PreferencesSmsQuicklyDialog

import os 
import sqlite3
import commands
import subprocess
import time

workplace = commands.getoutput('pwd')

# EXTRACTING DATABASES FROM SDCARD TO WORKING DIRECTORY AND OPENING THEM
os.system(workplace+"/./smsin.sh")
contactsDB = sqlite3.connect(workplace+'/databases/contacts2.db')
contactsDB.text_factory = str
c = contactsDB.cursor()
messageDB = sqlite3.connect(workplace+'/databases/mmssms.db')
messageDB.text_factory = str
sqlite3.enable_callback_tracebacks(True)
c2 = messageDB.cursor()

class SmsQuicklyWindow(Window):
    __gtype_name__ = "SmsQuicklyWindow"    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(SmsQuicklyWindow, self).finish_initializing(builder)
        self.AboutDialog = AboutSmsQuicklyDialog
        self.PreferencesDialog = PreferencesSmsQuicklyDialog
        # Code for other initialization actions should be added here.
        self.cnt = self.builder.get_object("cnt")
        self.cnt.connect('changed', self.on_cnt_enter)
        self.msg = self.builder.get_object("msg")
        
        # CONTACT COMPLETION
        global CompletionStore
        CompletionStore = Gtk.ListStore(str)
        completion = Gtk.EntryCompletion()
        completion.set_model(CompletionStore)
        completion.set_text_column(0)
        self.builder.get_object('cnt').set_completion(completion)

        # MESAGES LIST
        self.treeview = self.builder.get_object("treeview")
        self.listview = self.builder.get_object("liststore")
        # EXTRACT MESSAGES FRMO SQL
		c2.execute('SELECT body FROM sms ORDER BY date')
		messages = []
		senders = []
		# EXTRACT NAMES FOR MESSAGES
		for x in c2.execute('SELECT person from sms ORDER BY date'):
			item = str(x[0])
			if (item == 'None') or not item:
				item = "159"
			else:
				pass
			item = tuple([item])
			c.execute('SELECT display_name from raw_contacts where _id=?',item)
			item = (c.fetchone()[0])
			senders.append(item)
		for x in c2.execute('SELECT body FROM sms ORDER BY date'):
			messages.append(x[0],)
		messages = messages[::-1]
		senders = senders[::-1]
		for x in range(len(messages)):
			self.listview.append([messages[x],senders[x]])

	def on_msg_activate(self, widget):
		message = widget.get_text()
		contact = (self.cnt.get_text(),)
        c.execute('SELECT _id from raw_contacts where display_name=?', contact)
        contact_id = (c.fetchone()[0],)
        c.execute('SELECT normalized_number from phone_lookup where raw_contact_id=?', contact_id)
        contact_nr = c.fetchone()[0]

		#INSERT SENT MESSAGE RECORD BACK TO DATABASE
		# c2.execute('SELECT MAX(_id) FROM sms')
		# _id = (c2.fetchone()[0])
		# if not _id:
		# 	_id = 1
		# else:
		# 	_id_old = _id
		# 	_id = _id+1
		# print '_id_old = '+ str(_id_old)
		# print '_id = '+ str(_id)
		# c2.execute('SELECT address FROM sms WHERE _id = ?', (_id_old,))
		# address_to = c2.fetchone()[0]
		# print 'address_to = '+ str(address_to)
		# address_to = list(address_to)
		# for x in range(len(address_to)):
		# 	address_to[x] = address_to[x]+'%'
		# address_to = ''.join(address_to)
		# c2.execute('SELECT _id FROM canonical_addresses where address LIKE ?', (address_to,))
		# thread_id = c2.fetchone()[0]
		# print 'thread_id = '+str(thread_id)
		# if thread_id is None:
		# 	thread_id = 1
		# else:
		# 	pass
		# # print thread_id
		# time_sent = int(time.time() * 1000)
		# new_message = [(_id), (thread_id), (contact_nr), (""), (time_sent), (time_sent), (""), (1), (-1), (2), (""), (""), (message), (""), ("0"), ("0"), ("0")]
		# c2.execute('INSERT INTO sms VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', new_message)
		# new_words = [(_id),(message),(_id),(_id)]
		# c2.execute('INSERT INTO words VALUES (?,?,?,?)', new_words)
		# messageDB.commit()
		# messageDB.close()

		# os.system(workplace+"/./smsout.sh")
		
		ip = open("ip.txt").read().replace('\n','')
		smsend = "service call isms 5 s16 '"+contact_nr+"' i32 0 i32 0 s16 '"+message+"'"
		subprocess.Popen(["ssh","%s" % ip, smsend], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		subprocess.call('notify-send -u critical -i mail-generic Message sent.', shell=True)
        Window.destroy(0)
       
	def on_cnt_enter(self, widget):
		display_name = widget.get_text()
		c.execute('SELECT display_name from raw_contacts where display_name LIKE ?', ('%'+display_name+'%',))
		display_name = (c.fetchall(),)
		display_name = display_name[0]
		CompletionStore.clear()
		for x in range(len(display_name)):
        	CompletionStore.append([display_name[x][0]])

   	def on_sms_quickly_window_destroy(self,	 widget):
    	pass
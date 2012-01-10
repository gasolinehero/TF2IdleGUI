import Config
from PyQt4 import QtCore, QtGui
from sets import Set

class Ui_GroupsDialog(object):
	def __init__(self, GroupsDialog):
		self.settings = Config.settings
		
		# Create dialog
		self.GroupsDialog = GroupsDialog
		self.GroupsDialog.setWindowModality(QtCore.Qt.NonModal)
		self.GroupsDialog.resize(250, 450)
		self.GroupsDialog.setMinimumSize(QtCore.QSize(self.GroupsDialog.width(), self.GroupsDialog.height()))
		GroupsDialog.setWindowTitle('Select groups')
		
		# Add layout widget
		self.gridLayoutWidget = QtGui.QWidget(GroupsDialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(25, 10, self.GroupsDialog.width()-50, self.GroupsDialog.height()-40))
		
		self.gridLayout = QtGui.QVBoxLayout(self.gridLayoutWidget)
		self.gridLayout.setMargin(0)
		
		# Generate groups dict
		self.groupsDict = {}
		for account in list(Set(self.settings.get_sections()) - Set(['Settings'])):
			self.settings.set_section(account)
			groups = self.settings.get_option('groups')
			groups = groups.split(',')
			for group in groups:
				if group == '':
					pass
				else:
					if group in self.groupsDict:
						self.groupsDict[group].append(self.settings.get_option('steam_username'))
					else:
						self.groupsDict[group] = []
						self.groupsDict[group].append(self.settings.get_option('steam_username'))
		
		# Add group checkboxes
		self.groupButtons = []
		if len(self.groupsDict) == 0:
			self.Label = QtGui.QLabel(self.gridLayoutWidget)
			self.Label.setText('You have no groups set up. Try adding an account to a group.')
			self.Label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
			self.Label.setWordWrap(True)
			self.gridLayout.addWidget(self.Label)
		else:
			for group in self.groupsDict:
				self.commandLinkButton = QtGui.QCommandLinkButton(self.gridLayoutWidget)
				self.commandLinkButton.setText(group)
				membersString = ''
				for member in self.groupsDict[group]:
					membersString += member + '\n'
				self.commandLinkButton.setDescription(membersString)
				self.commandLinkButton.setCheckable(True)
				self.gridLayout.addWidget(self.commandLinkButton)
				self.groupButtons.append(self.commandLinkButton)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(self.gridLayoutWidget)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setCenterButtons(True)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.gridLayout.addWidget(self.buttonBox)
		
		# Signal connections
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), GroupsDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(GroupsDialog)
		
		self.accountsList = []
	
	def accept(self):
		for button in self.groupButtons:
			if button.isChecked():
				self.accountsList += self.groupsDict[str(button.text())]
		self.GroupsDialog.close()

	def returnAccounts(self):
		return self.accountsList
		
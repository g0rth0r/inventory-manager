import sys, os
from PyQt4 import QtGui, QtCore
from Ui_Window import Ui_MainWindow
from Ui_SearchPart import Ui_Dialog
from mongohandler import mongoDatabase

class PartPicker(QtGui.QDialog, Ui_Dialog):
    def __init__(self, db):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.db = db
        self.bindActions()
        self.loadParts()
        #self.exec_()

    def bindActions(self):
        # bind button actions
        self.searchLine.textChanged.connect(self.loadParts)
        
        

    def loadParts(self):
        # load list of parts into the picker
        self.listResults.clear()
        for res in self.db.getPartList(self.searchLine.text()):
            item = QtGui.QListWidgetItem(res['partNumber'])
            item.pid = res['_id']
            self.listResults.addItem(item)
        

class Window(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.bindActions()
        self.isLoading = False
        

        #connect to DB
        self.default_database = "inventory"
        self.db = mongoDatabase(self.default_database)

        #load comboboxes
        self.loadComboBox()
    
        #default settings
        self.IMGDIR = "images"
        
        self.isEditing = False
        self.loadedPart = None
        
        self.item_default = {"partNumber" : "",
                         "primaryImage": "no-image-icon-15.png",
                         "category" : "",
                         "supplier" : "",
                         "location" : "",
                         "model" : "",
                         "priceCAD" : "",
                         "priceUSD" : "",
                         "description" : "",
                         "instock" : "",
                         "discontinued" : False,
                         "isDiscontinued" : "",
                         "reorderLevel" : "",
                         "tagetStockLevel" : "",
                         "file3d" : ""}

        self.clearAction()
        
    def loadComboBox(self):

        locations = self.db.getAllLocations()
        categories =  self.db.getAllCategories()
        suppliers = self.db.getAllSuppliers()

        self.location.addItem("")
        self.category.addItem("")
        self.supplier.addItem("")
        
        for loc in locations:
            self.location.addItem(loc)

        for cat in categories:
            self.category.addItem(cat)

        for sup in suppliers:
            self.supplier.addItem(sup)

    def bindActions(self):

        # Bind Menus
        self.actionClose.triggered.connect(self.close_application)
        self.actionLoad.triggered.connect(self.loadPartPicker)
        self.actionSave.triggered.connect(self.saveAction)

        #Bind Buttons Click
        self.itemLoadButton.clicked.connect(self.loadPartPicker)
        self.saveButton.clicked.connect(self.saveAction)
        self.clearButton.clicked.connect(self.clearAction)

        # Bind Buttons edit
        self.itemField.textEdited.connect(self.isEdited)
        self.inStock.textEdited.connect(self.isEdited)
        self.model.textEdited.connect(self.isEdited)
        self.reorderLevel.textEdited.connect(self.isEdited)
        self.tagetStockLevel.textEdited.connect(self.isEdited)
        self.priceCAD.textEdited.connect(self.isEdited)
        self.priceUSD.textEdited.connect(self.isEdited)
        self.file3d.textEdited.connect(self.isEdited)
        self.description.textChanged.connect(self.isEdited)
        self.category.currentIndexChanged.connect(self.isEdited)
        self.location.currentIndexChanged.connect(self.isEdited)
        self.supplier.currentIndexChanged.connect(self.isEdited)
        self.isDiscontinued.stateChanged.connect(self.isEdited)

    def isEdited(self):
        # Define if one of the field was edited.
        if not self.isLoading:
            self.isEditing = False
            self.saveButton.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.actionSave_and_New.setEnabled(True)

    def loadPartPicker(self):
        dialog = PartPicker(self.db)
        if dialog.exec():
            print(dialog.listResults.currentItem().pid, dialog.listResults.currentItem().text())
            self.load_part(dialog.listResults.currentItem().pid)
            
    def load_part(self, pid):
        print(f"Loading part {pid}...")

        self.isLoading = True
        data = self.db.getByPartId(pid)
        self.loadedPart = data["_id"]
        self.updateItemData(data)
        self.isLoading = False

    def gatherFormData(self):
        prepData = dict()

        prepData["partNumber"] = self.itemField.text()
        
        elements = self.itemInfoGroupBox.findChildren(QtGui.QWidget)
        for elem in elements:
            if isinstance(elem, QtGui.QLineEdit):
                prepData[elem.objectName()] = elem.text()

            elif isinstance(elem, QtGui.QComboBox):
                prepData[elem.objectName()] = elem.currentText()

            elif isinstance(elem, QtGui.QCheckBox):
                prepData[elem.objectName()] = elem.isChecked()

            elif isinstance(elem, QtGui.QTextEdit):
                prepData[elem.objectName()] = elem.toPlainText()
            elif elem.objectName() == "imageLabel":
                prepData["primaryImage"] =  elem.fileName

        return prepData
        
    def saveState(self):
         self.isEditing = False
         self.saveButton.setEnabled(False)
         self.actionSave.setEnabled(False)
         self.actionSave_and_New.setEnabled(False)

    def saveAction(self):
        data = self.gatherFormData()

        if self.loadedPart:
            res = self.db.updatePartbyId(self.loadedPart, data)
            if res.modified_count:
                msgBox = QtGui.QMessageBox.information(self, "Saved","Part has been successfully saved.\n")
                self.saveState()
        else:
            res = self.db.insertNewItem(data)
            if res.inserted_id :
                msgBox = QtGui.QMessageBox.information(self, "Saved","Part has been successfully saved.\n")
                self.loadedPart = res.inserted_id
                self.saveState()
 

    def clearAction(self):
         self.updateItemData(self.mergeDefaultDict(self.item_default, self.item_default))
         self.isEditing = False
         self.loadedPart = None
         self.saveButton.setEnabled(False)
         self.actionSave.setEnabled(False)
         self.actionSave_and_New.setEnabled(False)
         

    def updateItemData(self, partData):
        #merge the default values with the ones available in the data
        update = self.mergeDefaultDict(partData, self.item_default)
        
        
    
        #update all the fields

        #partNumber
        self.itemField.setText(update["partNumber"])

        #Cetegory
        cid = self.category.findText(update["category"])
        self.category.setCurrentIndex(cid)

        #Supplier
        sid = self.supplier.findText(update["supplier"])
        self.supplier.setCurrentIndex(sid)

        #Location
        lid = self.location.findText(update["location"])
        self.location.setCurrentIndex(lid)

        #Model
        self.model.setText(update["model"])

        #priceCAD
        self.priceCAD.setText(update["priceCAD"])

        #priceUSD
        self.priceUSD.setText(update["priceUSD"])

        #description
        self.description.setText(update["description"])

        #instock
        self.inStock.setText(update["instock"])

        #reorderlevel
        self.reorderLevel.setText(update["reorderLevel"])

        #tagrgetstock
        self.tagetStockLevel.setText(update["tagetStockLevel"])

        #file3d
        self.file3d.setText(update["file3d"])

        #discontinued
        if update["isDiscontinued"]:
            self.isDiscontinued.setCheckState(2)
        else:
            self.isDiscontinued.setCheckState(0)

        
        #primary image
        if update["primaryImage"]:
            primaryPixmap = QtGui.QPixmap(
                os.path.join(self.IMGDIR,update["primaryImage"]))
            self.imageLabel.setPixmap(primaryPixmap)
            self.imageLabel.fileName = update["primaryImage"]
        
        
    def mergeDefaultDict(self, d1, default):
        res = default.copy()
        for k,v in default.items():
            if k in d1:
                res[k] = d1[k]
        return res

    def new_part(self):
        print("CREATING NEW PART")

    def close_application(self):
        if self.isEditing:
            choice = QtGui.QMessageBox.question(self, "Save work?", "You have unsaved data. Do you wish to exit?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if choice == QtGui.QMessageBox.Yes:
                print("Exiting....")
                sys.exit()
            else:
                pass
        else:
            sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

run()

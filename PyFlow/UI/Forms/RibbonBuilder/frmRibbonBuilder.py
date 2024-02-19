from ProjectManager.Packages.ProgramBase.Database.dbFormBuilder import *

#790410062-RC001
#790410062-RT001

import re
import sys

from qtpy import QtGui
from qtpy import QtCore
from qtpy.QtWidgets import *
import os

from qtpy import QtUiTools

from ProjectManager import Packages
basePackagePath = os.path.dirname(os.path.abspath(__file__))
packageRoot = Packages.__path__[0]

uiFile = os.path.join(basePackagePath, 'frmFormBuilder.ui')

from ProjectManager.Database import DatabaseTools
from ProjectManager.Packages.ProgramBase.Database.dbBase import *
from ProjectManager.Packages.ProgramBase.Database.dbMasterTables import *
from ProjectManager.Packages.ProgramBase.Database.dbAllLists import *
from ProjectManager.Packages.ProgramBase.Database.dbAllTables import *

from qtalchemy import *

class FormBuilder(QMdiSubWindow):

    def get_filenames(self, directory):
        file_names = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                file_names.append(filename)  # Add it to the list.

        return file_names  # Self-explanatory.

    def get_filepaths(self, directory):
        """
        https://realpython.com/working-with-files-in-python/

        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).

        # List all files in a directory using os.listdir
        basepath = 'my_directory/'
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
        print(entry)

        # List all files in a directory using scandir()
        basepath = 'my_directory/'
        with os.scandir(basepath) as entries:
            for entry in entries:
                if entry.is_file():
            print(entry.name)

        from pathlib import Path

        # List all files in directory using pathlib
        basepath = Path('my_directory/')
        files_in_basepath = (entry for entry in basepath.iterdir() if entry.is_file())
        for item in files_in_basepath:
            print(item.name)

        """
        file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

        return file_paths  # Self-explanatory.

    def __init__(self, main, parent):
        QMdiSubWindow.__init__(self)
        self.ui = QtUiTools.QUiLoader().load(uiFile)
        self.PackageName = "FormBuilder"

        self.instanceDict = main.sqlRegister.instanceDict
        self.baseDict = main.sqlRegister.instanceDict["ProgramBase"].base
        self.engineDict = main.sqlRegister.instanceDict["ProgramBase"].engine

        #region loadStuff
        self.loadBaseList()
        self.loadSessionList()
        self.loadMasterTable()
    #endregion

    #region Initilize Sections
        self.initRecordGroup()
        self.init_Widgets()
        self.init_FormItems()
        self.init_FunctionTemplate()
        self.init_FITTemplate()
    #endregion

    #region SetEvents
        self.ui.tblTTable.clicked.connect(self.on_tblTTable_clicked)
        self.ui.tblWidgets.clicked.connect(self.on_tblWidgets_clicked)
        self.ui.tblRecordGroup.clicked.connect(self.on_tblRecordGroup_clicked)
        self.ui.tblFormItems.clicked.connect(self.on_tblFormItems_clicked)
        self.ui.tblFunctionTemplate.clicked.connect(self.on_tblFunctionTemplate_clicked)
        #self.ui.txtFunctionTemplateCode.textChanged.connect(self.on_txtFunctionTemplateCode_textChanged)

        #self.ui.cmbFITSession.currentIndexChanged.connect(self.on_cmbFITSession_currentIndexChanged)

        self.ui.cmbFormName.currentIndexChanged.connect(self.on_cmbFormName_currentIndexChanged)
        self.ui.cmdCreateForm.clicked.connect(self.on_cmdCreateForm_clicked)
        self.ui.lstForms.clicked.connect(self.on_lstForms_clicked)

        self.ui.txtFormPath.setText(basePackagePath)
        self.ui.cmdCreateFormBaseClass.clicked.connect(self.on_cmdCreateFormBaseClass_clicked)
        self.ui.cmdFTSaveCode.clicked.connect(self.on_cmdFTSaveCode_clicked)
        self.ui.spnFunctionOrder.valueChanged.connect(self.on_spnFunctionOrder_valueChanged)

        print("Initiated")
    #endregion

    def scanTables(self):
        pass

    def scanForm(self):
        pass

    def loadTableField(self, Base, table_fullname):

        lario.get_fields_by_tablename(Base, table_fullname)


    def loadBaseList(self):
        qrybaselist = self.instanceDict["ProgramBase"].session.query(SessionBase.id, SessionBase.NameText) #139
        self.ui.lstBases.setModel(QueryTableModel(qrybaselist))
        self.ui.lstBases.setModelColumn(1)

    def loadSessionList(self):
        qrysessionlist = self.instanceDict["ProgramBase"].session.query(SessionNames.id, SessionNames.NameText) #139
        self.ui.lstSession.setModel(QueryTableModel(qrysessionlist))
        self.ui.lstSession.setModelColumn(1)

        self.ui.lstTSessions.setModel(QueryTableModel(qrysessionlist))
        self.ui.lstTSessions.setModelColumn(1)

    def loadMasterTable(self, FilterName=None):

        qryMasterTable = self.instanceDict["ProgramBase"].session.query(MasterTable.id, SessionBase.NameText.label("Base"), SessionNames.NameText.label("Session"), MasterTable.TableName)\
                                        .join(SessionBase, MasterTable.Base == SessionBase.id)\
                                        .join(SessionNames, MasterTable.Session == SessionNames.id)
        if FilterName is not None:
            qryMasterTable = qryMasterTable.filter(MasterTable.TableName.like("%" + str(FilterName) + "%"))

        self.ui.tblTTable.setModel(QueryTableModel(qryMasterTable))

    @QtCore.Slot()
    def on_tblTTable_clicked(self):
        data = {}
        data["row"] = self.ui.tblTTable.selectionModel().currentIndex().row()
        data["column"] = self.ui.tblTTable.selectionModel().currentIndex().column()
        data["column"] = self.ui.tblTTable.selectionModel().currentIndex().column()
        data["Value"] = self.ui.tblTTable.model().index(data["row"], data["column"], None).data()
        data["Master_id"] = self.ui.tblTTable.model().index(data["row"], 0, None).data()

        BaseName = self.ui.tblTTable.model().index(data["row"], 1, None).data()
        table_fullname = self.ui.tblTTable.model().index(data["row"], 3, None).data()

        fieldInformation = DatabaseTools.get_fields_by_tablename(bases[BaseName], table_fullname)

        fieldModel = QStandardItemModel(0,2)

        if fieldInformation is not None:
            for row, key in enumerate(fieldInformation):
                fieldModel.setItem(row, 0, QStandardItem(str(row)))
                fieldModel.setItem(row, 1, QStandardItem(str(key)))
                fieldModel.setItem(row, 2, QStandardItem(str(fieldInformation[key])))

            fieldModel.setHeaderData(0, Qt.Horizontal, 'id', role=Qt.DisplayRole)
            fieldModel.setHeaderData(1, Qt.Horizontal, 'Field', role=Qt.DisplayRole)
            fieldModel.setHeaderData(2, Qt.Horizontal, 'DataType', role=Qt.DisplayRole)

        self.ui.tblTFields.setModel(fieldModel)
        self.ui.tblTFields.resizeColumnsToContents()
        self.ui.tblTFields.setColumnWidth(0, 0)

    # region Record Group
    def initRecordGroup(self):
        self.blockRGSignals(True)
        self.on_RGTable_load()
        self.on_RGForm_load()
        self.on_RGParentGroup_load()
        self.on_RGSession_load()
        self.on_RGMasterTable_load()
        self.blockRGSignals(False)

    def on_RGTable_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroup)
        self.ui.tblRecordGroup.setModel(QueryTableModel(qryRecord))
        qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroup.id, RecordGroup.Title)
        self.ui.cmbRGParentGroup.setModel(QueryTableModel(qryRecord))
        self.ui.cmbRGParentGroup.setModelColumn(1)

    def on_RGForm_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormInformation.id, FormInformation.FileName)
        self.ui.cmbRGForm.setModel(QueryTableModel(qryRecord))
        self.ui.cmbRGForm.setModelColumn(1)

        qryEquipmentProjectRecord = self.instanceDict["ProgramBase"].session.query(ProjectEquipment.id, Equipment.Manufacturer, Equipment.Model,
                                                  Equipment.Serial, Equipment.Unit) \
            .join(Equipment, ProjectEquipment.equipment_id == Equipment.id) \

    def on_RGParentGroup_load(self, Group_id=None):
        if Group_id is not None:
            qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroupParents.id, RecordGroup.Title, RecordGroupParents.ParentFieldID, RecordGroupParents.ChildFieldID)\
                                    .join(RecordGroup, RecordGroupParents.ParentGroupID == RecordGroup.id)\
                                     .filter(RecordGroupParents.RecordGroupID==Group_id)

            self.ui.tblRGParentGroup.setModel(QueryTableModel(qryRecord))
        else:
            self.ui.tblRGParentGroup.setModel(None)

        self.ui.tblRGParentGroup.resizeColumnsToContents()
        self.ui.tblRGParentGroup.setColumnWidth(0, 0)

    def on_RGSession_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(SessionNames.id, SessionNames.NameText)
        self.ui.cmbRGSession.setModel(QueryTableModel(qryRecord))
        self.ui.cmbRGSession.setModelColumn(1)

    def on_RGMasterTable_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable.id, MasterTable.TableName)
        self.ui.cmbRGMasterTable.setModel(QueryTableModel(qryRecord))
        self.ui.cmbRGMasterTable.setModelColumn(1)

    @QtCore.Slot()
    def on_tblRecordGroup_clicked(self):
        data = {}
        data["row"] = self.ui.tblRecordGroup.selectionModel().currentIndex().row()
        data["column"] = self.ui.tblRecordGroup.selectionModel().currentIndex().column()
        data["column"] = self.ui.tblRecordGroup.selectionModel().currentIndex().column()
        data["Value"] = self.ui.tblRecordGroup.model().index(data["row"], data["column"], None).data()
        data["id"] = self.ui.tblRecordGroup.model().index(data["row"], 0, None).data()
        self.ui.txtRG_id.setText(str(data["id"]))
        self.initRGDict()
        self.createRGDictFromDatabase(int(data["id"]))
        self.loadRGForm(int(data["id"]))

    @QtCore.Slot()
    def on_cmdCreateNewRecordGroup_clicked(self):
        self.initRGForm()
        self.initRGDict()
        self.instanceDict["ProgramBase"].session.begin()
        qryRecordGroup = RecordGroup()
        self.instanceDict["ProgramBase"].session.add(qryRecordGroup)
        self.instanceDict["ProgramBase"].session.commit()
        self.instanceDict["ProgramBase"].session.flush()

        self.on_RGTable_load()
        self.ui.txtRG_id.setText(str(qryRecordGroup.id))

    def createsaveRecordGroup(self, record_id = None):
        currentdatetime = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')

        if record_id is None:
            self.instanceDict["ProgramBase"].session.begin()
            qryRecord = RecordGroup(Date_Created=currentdatetime,
                                    Date_Modified=currentdatetime,
                                    Date_Accessed=currentdatetime)
            self.instanceDict["ProgramBase"].session.add(qryRecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroup).filter_by(id=record_id).first()
            self.instanceDict["ProgramBase"].session.begin()

            if self.RGDict["Title"] != "": qryRecord.Title = self.RGDict["Title"]
            if self.RGDict["FormID"] != -1: qryRecord.FormID = self.RGDict["FormID"]
            if self.RGDict["Abbreviation"] != "": qryRecord.Abbreviation = self.RGDict["Abbreviation"]
            if self.RGDict["SessionID"] != -1: qryRecord.SessionID = self.RGDict["SessionID"]
            if self.RGDict["TableID"] != -1: qryRecord.TableID = self.RGDict["TableID"]
            '''qryRecord.IDWidgetName = self.RGDict["IDWidgetName"]
            qryRecord.IDWidgetType = self.RGDict["IDWidgetType"]
            qryRecord.NewItemWidgetName = self.RGDict["NewItemWidgetName"]
            qryRecord.NewItemWidgetType = self.RGDict["NewItemWidgetType"]
            qryRecord.CreateDictFunction = self.RGDict["CreateDictFunction"]'''

            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        self.on_RGTable_load()
        return qryRecord.id

    def initRGForm(self):
        self.blockRGSignals(True)
        self.ui.txtRG_id.setText("")
        self.ui.txtRGGroupName.setText("")
        self.ui.cmbRGForm.setCurrentIndex(-1)
        self.ui.cmbRGParentGroup.setCurrentIndex(-1)
        self.ui.txtRGAbbreviation.setText("")
        self.ui.cmbRGSession.setCurrentIndex(-1)
        self.ui.cmbRGMasterTable.setCurrentIndex(-1)
        self.ui.txtRGTableName.setText("")
        self.ui.txtRGFieldID.setText("")
        self.ui.txtRGDisplayTable.setText("")
        self.ui.txtRGCreateNewItem.setText("")
        self.ui.txtRGCreateDictionary.setText("")
        self.ui.txtRGListForDisplay.setText("")
        self.ui.txtRGListLClicked.setText("")
        self.ui.txtRGBlockSignals.setText("")
        self.ui.txtRGClearRecords.setText("")
        self.ui.txtRGCreateSave.setText("")
        self.blockRGSignals(False)

    def loadRGForm(self, id):
        self.initRGForm()
        self.blockRGSignals(True)

        qryRecordGroup = self.instanceDict["ProgramBase"].session.query(RecordGroup).filter_by(id=id).first()
        self.ui.txtRG_id.setText(str(qryRecordGroup.id))
        self.ui.txtRGGroupName.setText(qryRecordGroup.Title)

        for row in range(self.ui.cmbRGForm.model().rowCount()):
            if qryRecordGroup.FormID is not None:
                if int(self.ui.cmbRGForm.model().index(row, 0, None).data()) == int(qryRecordGroup.FormID):
                    self.ui.cmbRGForm.setCurrentIndex(row)
                    break

        self.ui.txtRGAbbreviation.setText(qryRecordGroup.Abbreviation)

        for row in range(self.ui.cmbRGSession.model().rowCount()):
            if qryRecordGroup.SessionID is not None:
                if int(self.ui.cmbRGSession.model().index(row, 0, None).data()) == int(qryRecordGroup.SessionID):
                    self.ui.cmbRGSession.setCurrentIndex(row)
                    break

        for row in range(self.ui.cmbRGMasterTable.model().rowCount()):
            if qryRecordGroup.TableID is not None:
                if int(self.ui.cmbRGMasterTable.model().index(row, 0, None).data()) == int(qryRecordGroup.TableID):
                    self.ui.cmbRGMasterTable.setCurrentIndex(row)
                    break

        self.on_RGParentGroup_load(Group_id=qryRecordGroup.id)

        self.ui.txtRGTableName.setText("")
        self.ui.txtRGFieldID.setText("")
        self.ui.txtRGDisplayTable.setText("")
        self.ui.txtRGCreateNewItem.setText("")
        self.ui.txtRGCreateDictionary.setText("")
        self.ui.txtRGListForDisplay.setText("")
        self.ui.txtRGListLClicked.setText("")
        self.ui.txtRGBlockSignals.setText("")
        self.ui.txtRGClearRecords.setText("")
        self.ui.txtRGCreateSave.setText("")
        self.updateFunctionNames()

        self.blockRGSignals(False)

    def initRGDict(self):
        #id = int(self.ui.txtRG_id.text())
        self.RGDict = {}
        self.RGDict["id"] = -1
        self.RGDict["RecordGroup"] = ""
        self.RGDict["FormID"] = -1
        self.RGDict["Abbreviation"] = ""
        self.RGDict["ParentGroup"] = []
        self.RGDict["SessionID"] = -1
        self.RGDict["TableID"] = -1
        self.RGDict["IDWidgetName"] = ""
        self.RGDict["IDWidgetType"] = ""
        self.RGDict["NewItemWidgetName"] = ""
        self.RGDict["NewItemWidgetType"] = ""
        self.RGDict["CreateDictFunction"] = ""

    def createRGDictFromForm(self):
        id = int(self.ui.self.ui.txtRG_id.text())
        self.RGDict = {}
        self.RGDict["id"] = id
        self.RGDict["RecordGroup"] = self.ui.txtRGGroupName.text()
        self.RGDict["FormID"] = self.ui.cmbRGForm
        self.RGDict["Abbreviation"] = self.ui.txtRGAbbreviation
        self.RGDict["SessionID"] = self.ui.cmbRGSession
        '''self.RGDict["TableID"] = qryRecord.TableID
        self.RGDict["IDWidgetName"] = qryRecord.IDWidgetName
        self.RGDict["IDWidgetType"] = qryRecord.IDWidgetType
        self.RGDict["NewItemWidgetName"] = qryRecord.NewItemWidgetName
        self.RGDict["NewItemWidgetType"] = qryRecord.NewItemWidgetType
        self.RGDict["CreateDictFunction"] = qryRecord.CreateDictFunction'''

    def createRGDictFromDatabase(self, record_id):
        qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroup).filter_by(id=record_id).first()

        self.RGDict = {}
        self.RGDict["id"] = id
        self.RGDict["Title"] = qryRecord.Title
        self.RGDict["FormID"] = qryRecord.FormID
        self.RGDict["Abbreviation"] = qryRecord.Abbreviation
        self.RGDict["SessionID"] = qryRecord.SessionID

        self.RGDict["TableID"] = qryRecord.TableID
        if qryRecord.TableID is not None:
            qryMainTable = self.instanceDict["ProgramBase"].session.query(MasterTable).filter_by(id=qryRecord.TableID).first()
            self.RGDict["Table"] = qryMainTable.TableName

        self.RGDict["IDWidgetName"] = qryRecord.IDWidgetName
        self.RGDict["IDWidgetType"] = qryRecord.IDWidgetType
        self.RGDict["NewItemWidgetName"] = qryRecord.NewItemWidgetName
        self.RGDict["NewItemWidgetType"] = qryRecord.NewItemWidgetType
        self.RGDict["CreateDictFunction"] = qryRecord.CreateDictFunction

    def blockRGSignals(self, Value):
        self.ui.txtRG_id.blockSignals(Value)
        self.ui.txtRGGroupName.blockSignals(Value)
        self.ui.cmbRGForm.blockSignals(Value)
        self.ui.cmbRGParentGroup.blockSignals(Value)
        self.ui.txtRGAbbreviation.blockSignals(Value)
        self.ui.cmbRGSession.blockSignals(Value)
        self.ui.cmbRGMasterTable.blockSignals(Value)
        self.ui.txtRGTableName.blockSignals(Value)
        self.ui.txtRGFieldID.blockSignals(Value)
        self.ui.txtRGDisplayTable.blockSignals(Value)
        self.ui.txtRGCreateNewItem.blockSignals(Value)
        self.ui.txtRGCreateDictionary.blockSignals(Value)
        self.ui.txtRGListForDisplay.blockSignals(Value)
        self.ui.txtRGListLClicked.blockSignals(Value)
        self.ui.txtRGBlockSignals.blockSignals(Value)
        self.ui.txtRGClearRecords.blockSignals(Value)
        self.ui.txtRGCreateSave.blockSignals(Value)

    def on_txtRGGroupName_textChanged(self, value):
        self.RGDict["RecordGroup"] = value
        capletters = re.findall('([A-Z])', value)
        abbrv = ""
        for i in capletters:
            abbrv += i

        self.ui.txtRGAbbreviation.setText(abbrv)

        if self.ui.chkRGGroupName.isChecked():
            self.loadRGTable()
        else:
            if self.ui.txtRG_id.text() != "":
                record_id = int(self.ui.txtRG_id.text())
                self.createsaveRecordGroup(record_id)

    @QtCore.Slot(int)
    def on_cmbRGForm_currentIndexChanged(self, index):
        if self.ui.txtRG_id.text() != "":
            self.RGDict["FormID"] = self.ui.cmbRGForm.model().index(index, 0, None).data()
            print(self.ui.cmbRGForm.model().index(index, 0, None).data())
            if self.ui.chkRGGroupName.isChecked():
                self.loadRGTable()
            else:
                if self.ui.txtRG_id.text() != "":
                    record_id = int(self.ui.txtRG_id.text())
                    self.createsaveRecordGroup(record_id)

    def on_txtRGAbbreviation_textChanged(self, value):
        self.RGDict["Abbreviation"] = value
        if self.ui.chkRGAbbreviation.isChecked():
            self.loadRGTable()
        else:
            if self.ui.txtRG_id.text() != "":
                record_id = int(self.ui.txtRG_id.text())
                self.createsaveRecordGroup(record_id)

        self.updateFunctionNames()

    @QtCore.Slot()
    def on_cmdAddRGParentGroup_clicked(self):
        id = int(self.ui.txtRG_id.text())
        if self.ui.cmbRGParentGroup.model().index(self.ui.cmbRGParentGroup.currentIndex(), 0, None).data() is not None:
            parent_id = int(self.ui.cmbRGParentGroup.model().index(self.ui.cmbRGParentGroup.currentIndex(), 0, None).data())

            qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroupParents).filter_by(RecordGroupID=id).filter_by(ParentGroupID=parent_id).first()
            if qryRecord is None:
                self.instanceDict["ProgramBase"].session.begin()
                qryRecord = RecordGroupParents(RecordGroupID=id, ParentGroupID=parent_id)
                self.instanceDict["ProgramBase"].session.add(qryRecord)
                self.instanceDict["ProgramBase"].session.commit()
                self.instanceDict["ProgramBase"].session.flush()

            self.on_RGParentGroup_load(Group_id=id)

    @QtCore.Slot(int)
    def on_cmbRGSession_currentIndexChanged(self, index):
        if self.ui.txtRG_id.text() != "":
            self.RGDict["SessionID"] = self.ui.cmbRGSession.model().index(index, 0, None).data()
            if self.ui.chkRGSession.isChecked():
                self.loadRGTable()
            else:
                if self.ui.txtRG_id.text() != "":
                    record_id = int(self.ui.txtRG_id.text())
                    self.createsaveRecordGroup(record_id)

    @QtCore.Slot(int)
    def on_cmbRGMasterTable_currentIndexChanged(self, index):
        if self.ui.txtRG_id.text() != "":
            self.RGDict["TableID"] = self.ui.cmbRGMasterTable.model().index(index, 0, None).data()
        if self.ui.chkRGMasterTable.isChecked():
            self.loadRGTable()
        else:
            if self.ui.txtRG_id.text() != "":
                record_id = int(self.ui.txtRG_id.text())
                self.createsaveRecordGroup(record_id)

    def on_txtRGTableName_textChanged(self, value):
        self.RGDict["Abbreviation"] = value
        if self.ui.chkRGGroupName.isChecked():
            self.loadRGTable()
        else:
            if self.ui.txtRG_id.text() != "":
                record_id = int(self.ui.txtRG_id.text())
                self.createsaveRecordGroup(record_id)

    def on_chkRGFieldID_stateChanged(self):
        self.loadRGTable()

    def on_chkRGDisplayTable_stateChanged(self):
        self.loadRGTable()

    def on_chkRGCreateNewItem_stateChanged(self):
        self.loadRGTable()

    def on_chkRGCreateDictionary_stateChanged(self):
        self.loadRGTable()

    def on_chkRGListForDisplay_stateChanged(self):
        self.loadRGTable()

    def on_chkRGListLClicked_stateChanged(self):
        self.loadRGTable()

    def on_chkRGBlockSignals_stateChanged(self):
        self.loadRGTable()

    def on_chkRGClearRecords_stateChanged(self):
        self.loadRGTable()

    def on_chkRGCreateSave_stateChanged(self):
        self.loadRGTable()

    # customFunctions
    def updateFunctionNames(self):

        abbr = self.RGDict["Abbreviation"]
        #createsaveRecordGroup
        #on_tblRecordGroup_clicked
        '''load_RGTable
        load_RGForm
        load_RGParentGroup
        load_RGSession
        load_RGMasterTable
        on_tblRecordGroup_clicked
        on_cmdCreateNewRG_clicked
        createsave_RG
        init_RGForm
        load_RGForm
        init_RGDict
        create_RGDict_fromTable
        create_RGDict_FromDatabase
        block_RG_Signals'''

        self.ui.txtRGDisplayTable.setText("tbl" + abbr + "Display")
        self.ui.txtRGCreateNewItem.setText("createsave" + abbr)
        self.ui.txtRGCreateDictionary.setText("create" + abbr + "Dict")
        self.ui.txtRGListForDisplay.setText("tbl" + abbr + "Display")
        self.ui.txtRGListLClicked.setText("tbl" + abbr + "Display")
        self.ui.txtRGBlockSignals.setText("block" + abbr + "Signals")
        self.ui.txtRGClearRecords.setText("init" + abbr + "Form")
        self.ui.txtRGCreateSave.setText("createSave" + abbr)

    @QtCore.Slot()
    def on_cmdLoadForms_clicked(self):
        fpath = QFileDialog.getExistingDirectory()
        formsearchfolders = self.get_filepaths(fpath)

        for filepath in formsearchfolders:
            folderpath, filename = os.path.split(filepath)
            filejunk, file_extension = os.path.splitext(filepath)
            if file_extension == ".ui":
                qryForm = self.instanceDict["ProgramBase"].session.query(FormInformation).filter_by(FilePath=folderpath).filter_by(FileName=filename).first()
                if qryForm is None:
                    self.instanceDict["ProgramBase"].session.begin()
                    qryForm = FormInformation(FilePath=folderpath, FileName=filename)
                    self.instanceDict["ProgramBase"].session.add(qryForm)
                    self.instanceDict["ProgramBase"].session.commit()
                    self.instanceDict["ProgramBase"].session.flush()

                f = open(filepath, "r")
                contents = f.read()
                widgetlist = set(re.findall('\<widget.*?\>', contents)) #<widget class="QLabel" name="label_31">
                for widgetline in widgetlist:
                    wclass = re.search('class=\".*?\"', widgetline).group()[7:-1]
                    wname = re.search('name=\".*?\"', widgetline).group()[6:-1]

                    qryWidgetType = self.instanceDict["ProgramBase"].session.query(WidgetData).filter_by(Title=wclass).first()
                    if qryWidgetType is None:
                        self.instanceDict["ProgramBase"].session.begin()
                        qryWidgetType = WidgetData(Title=wclass)
                        self.instanceDict["ProgramBase"].session.add(qryWidgetType)
                        self.instanceDict["ProgramBase"].session.commit()
                        self.instanceDict["ProgramBase"].session.flush()

                    qryWidgetData = self.instanceDict["ProgramBase"].session.query(WidgetData).filter_by(Title=wclass).first()
                    if qryWidgetData is None:
                        self.instanceDict["ProgramBase"].session.begin()
                        qryWidgetData = WidgetData(Title=wclass)
                        self.instanceDict["ProgramBase"].session.add(qryWidgetData)
                        self.instanceDict["ProgramBase"].session.commit()
                        self.instanceDict["ProgramBase"].session.flush()

                    qryFormWidget = self.instanceDict["ProgramBase"].session.query(FormWidgets).filter_by(Form=qryForm.id).filter_by(WidgetName=wname).first()
                    if qryFormWidget is None:
                        self.instanceDict["ProgramBase"].session.begin()
                        qryFormWidget = FormWidgets(Form=qryForm.id, WidgetType=qryWidgetData.id, WidgetName=wname)
                        self.instanceDict["ProgramBase"].session.add(qryFormWidget)
                        self.instanceDict["ProgramBase"].session.commit()
                        self.instanceDict["ProgramBase"].session.flush()

        self.on_RGForm_load()
    # end customFunctions

    # endregion

    #region Widgets
    def init_Widgets(self):
        self.init_WDict()
        self.blockWSignals(True)
        self.on_WTable_load()
        self.on_WForm_load()
        self.on_WDatatType_load()
        self.blockWSignals(False)

    def on_WTable_load(self):
        qryWidget = self.instanceDict["ProgramBase"].session.query(WidgetData.id, WidgetData.Title, WidgetData.Abbreviation).order_by(WidgetData.Title)
        self.ui.tblWidgets.setModel(QueryTableModel(qryWidget))
        self.ui.tblWidgets.resizeColumnsToContents()
        self.ui.tblWidgets.setColumnWidth(0, 0)

    def on_WDatatType_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(DataType.id, DataType.NameText)
        self.ui.cmbWSVDataType.setModel(QueryTableModel(qryRecord))
        self.ui.cmbWSVDataType.setModelColumn(1)
        self.ui.cmbWGVDataType.setModel(QueryTableModel(qryRecord))
        self.ui.cmbWGVDataType.setModelColumn(1)
        self.ui.cmbWUVDataType.setModel(QueryTableModel(qryRecord))
        self.ui.cmbWUVDataType.setModelColumn(1)

    def on_WForm_load(self):
        pass

    def on_WSVTable_load(self):
        id = int(self.ui.txtWidgetID.text())
        qryrecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.WidgetID, WidgetDataHandling.Command, DataType.NameText.label("DataType"), WidgetDataHandling.DataTypeFormat, WidgetDataHandling.Description, WidgetDataHandling.Preferred)\
                                .join(DataType, WidgetDataHandling.DataType == DataType.id)\
                                .filter(WidgetDataHandling.WidgetID==id, WidgetDataHandling.Direction==1)

        self.ui.tblWSCommands.setModel(QueryTableModel(qryrecord))
        self.ui.tblWSCommands.resizeColumnsToContents()
        self.ui.tblWSCommands.setColumnWidth(0, 0)
        self.ui.tblWSCommands.setColumnWidth(1, 0)

    def on_WGVTable_load(self):
        id = int(self.ui.txtWidgetID.text())
        qryrecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.WidgetID, WidgetDataHandling.Command,
                                  DataType.NameText.label("DataType"), WidgetDataHandling.DataTypeFormat, WidgetDataHandling.Description,
                                  WidgetDataHandling.Preferred)\
                                .join(DataType, WidgetDataHandling.DataType == DataType.id)\
                                .filter(WidgetDataHandling.WidgetID==id, WidgetDataHandling.Direction == 2)
        self.ui.tblWGCommands.setModel(QueryTableModel(qryrecord))
        self.ui.tblWGCommands.resizeColumnsToContents()
        self.ui.tblWGCommands.setColumnWidth(0, 0)
        self.ui.tblWGCommands.setColumnWidth(1, 0)

    def on_WUVTable_load(self):
        id = int(self.ui.txtWidgetID.text())
        qryrecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.WidgetID, WidgetDataHandling.Command,
                                  DataType.NameText.label("DataType"), WidgetDataHandling.DataTypeFormat, WidgetDataHandling.Description,
                                  WidgetDataHandling.Preferred) \
                                .outerjoin(DataType, WidgetDataHandling.DataType == DataType.id) \
                                .filter(WidgetDataHandling.WidgetID == id, WidgetDataHandling.Direction == 3)

        self.ui.tblWUCommands.setModel(QueryTableModel(qryrecord))
        self.ui.tblWUCommands.resizeColumnsToContents()
        self.ui.tblWUCommands.setColumnWidth(0, 0)
        self.ui.tblWUCommands.setColumnWidth(1, 0)

    def on_cmdCreateNewWidget_clicked(self):
        pass

    def createsaveWidget(self, record_id=None):

        if record_id is None:
            self.instanceDict["ProgramBase"].session.begin()
            qryRecord = WidgetData()
            self.instanceDict["ProgramBase"].session.add(qryRecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetData).filter_by(id=record_id).first()
            self.instanceDict["ProgramBase"].session.begin()

            if self.WDict["Item"] != "": qryRecord.Title = self.WDict["Item"]
            if self.WDict["Abbrev"] != "": qryRecord.Abbreviation = self.WDict["Abbrev"]

            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        self.on_WTable_load()
        return qryRecord.id


    def blockWSignals(self, value):
        self.ui.txtWItem.blockSignals(value)
        self.ui.txtWAbbrev.blockSignals(value)


    def init_WidgetForm(self):
        self.blockWSignals(True)
        self.ui.txtWItem.setText("")
        self.ui.txtWAbbrev.setText("")
        self.ui.txtWSetValue.setText("")
        self.ui.txtWGetValue.setText("")
        self.ui.txtWUpdateValue.setText("")
        self.ui.cmbWSVDataType.setCurrentIndex(-1)
        self.ui.cmbWGVDataType.setCurrentIndex(-1)
        self.ui.cmbWUVDataType.setCurrentIndex(-1)

        self.blockWSignals(False)

    def init_WDict(self):
        self.WDict = {}
        self.WDict["Item"] = ""
        self.WDict["Abbrev"] = ""

    def createWDictFromForm(self):
        self.WDict["Item"] = self.ui.txtWItem.text()
        self.WDict["Abbrev"] = self.ui.txtWAbbrev.text()

    def createWDictFromDatabase(self, id):
        qryWidget = self.instanceDict["ProgramBase"].session.query(WidgetData).filter_by(id = int(id)).first()
        self.WDict["Item"] = qryWidget.Title
        self.WDict["Abbrev"] = qryWidget.Abbreviation

    @QtCore.Slot()
    def on_tblWidgets_clicked(self):
        self.init_WidgetForm()
        self.blockWSignals(True)
        data = {}
        data["row"] = self.ui.tblWidgets.selectionModel().currentIndex().row()
        data["column"] = self.ui.tblWidgets.selectionModel().currentIndex().column()
        data["column"] = self.ui.tblWidgets.selectionModel().currentIndex().column()
        data["Value"] = self.ui.tblWidgets.model().index(data["row"], data["column"], None).data()
        data["id"] = self.ui.tblWidgets.model().index(data["row"], 0, None).data()

        self.ui.txtWidgetID.setText(str(data["id"]))

        qryWidget = self.instanceDict["ProgramBase"].session.query(WidgetData).filter_by(id = int(data["id"])).first()
        self.ui.txtWItem.setText(qryWidget.Title)
        self.ui.txtWAbbrev.setText(qryWidget.Abbreviation)

        self.on_WSVTable_load()
        self.on_WGVTable_load()
        self.on_WUVTable_load()

        self.blockWSignals(False)

    @QtCore.Slot()
    def on_cmdNewWidget_clicked(self):
        print("hi")

    @QtCore.Slot()
    def on_cmdWSV_add_clicked(self):
        id = int(self.ui.txtWidgetID.text())
        Command = self.ui.txtWSetValue.text()
        datatype = self.ui.cmbWSVDataType.model().index(self.ui.cmbWSVDataType.currentIndex(), 0, None).data()

        qryrecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling).filter_by(WidgetID=id, Command=Command, Direction=1).first()

        if qryrecord is None:
            self.instanceDict["ProgramBase"].session.begin(subtransactions=True)
            qryrecord = WidgetDataHandling(WidgetID=id,
                                           Command=Command,
                                           Direction=1,
                                           DataType=datatype)
            self.instanceDict["ProgramBase"].session.add(qryrecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        self.on_WSVTable_load()

    @QtCore.Slot()
    def on_cmdWGV_add_clicked(self):

        id = int(self.ui.txtWidgetID.text())
        Command = self.ui.txtWGetValue.text()
        datatype = self.ui.cmbWGVDataType.model().index(self.ui.cmbWGVDataType.currentIndex(), 0, None).data()

        qryrecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling).filter_by(WidgetID=id, Command=Command, Direction=1).first()

        if qryrecord is None:
            self.instanceDict["ProgramBase"].session.begin(subtransactions=True)
            qryrecord = WidgetDataHandling(WidgetID=id,
                                           Command=Command,
                                           Direction=2,
                                           DataType=datatype)
            self.instanceDict["ProgramBase"].session.add(qryrecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        self.on_WGVTable_load()

    @QtCore.Slot()
    def on_cmdWUV_add_clicked(self):
        id = int(self.ui.txtWidgetID.text())
        Command = self.ui.txtWUpdateValue.text()
        datatype = self.ui.cmbWUVDataType.model().index(self.ui.cmbWUVDataType.currentIndex(), 0, None).data()

        qryrecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling).filter_by(WidgetID=id, Command=Command, Direction=1).first()

        if qryrecord is None:
            self.instanceDict["ProgramBase"].session.begin(subtransactions=True)
            qryrecord = WidgetDataHandling(WidgetID=id,
                                           Command=Command,
                                           Direction=3,
                                           DataType=datatype)
            self.instanceDict["ProgramBase"].session.add(qryrecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        self.on_WUVTable_load()

    @QtCore.Slot(str)
    def on_txtWAbbrev_textChanged(self, value):
        self.WDict["Abbrev"] = value
        if self.ui.chkWItem.isChecked():
            self.load_WTable()
        else:
            if self.ui.txtWidgetID.text() != "":
                record_id = int(self.ui.txtWidgetID.text())
                self.createsaveWidget(record_id)
    #endregion

    #region Form Items
    def init_FormItems(self):
        self.blockFISignals(True)
        self.on_FISession_load()
        self.on_FITable_load()
        self.on_cmbFormType_load()
        self.on_cmbFormName_load()
        self.on_tblFormItems_load()
        self.on_tvFormItems_load()

        self.on_FIRSession_load()

        self.on_FIDataGroup_load()
        self.on_FIWidgetType_load()
        self.on_FISetValue_load()
        self.on_FIGetValue_load()
        self.on_FIUpdateValue_load()
        self.blockFISignals(False)

        self.init_FIForm()

    def on_FISession_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(SessionNames.id, SessionNames.NameText)
        self.ui.cmbFISession.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFISession.setModelColumn(1)

    def on_FITable_load(self, Session=None):
        if Session is None:
            qryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable.id, MasterTable.TableName)
            self.ui.cmbFITable.setModel(QueryTableModel(qryRecord))
            self.ui.cmbFITable.setModelColumn(1)
        else:
            queryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable.id, MasterTable.TableName).filter_by(Session=Session).order_by(MasterTable.TableName)
            self.ui.cmbFITable.setModel(QueryTableModel(queryRecord))
            self.ui.cmbFITable.setModelColumn(1)

    def on_FIRSession_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(SessionNames.id, SessionNames.NameText)
        self.ui.cmbFIRSession.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFIRSession.setModelColumn(1)

    def on_FIRTable_load(self, Session_id=None):
        self.blockFISignals(True)
        if Session is None:
            qryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable.id, MasterTable.TableName)
            self.ui.cmbFIRTable.setModel(QueryTableModel(qryRecord))
            self.ui.cmbFIRTable.setModelColumn(1)
        else:
            queryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable.id, MasterTable.TableName).filter_by(Session=Session_id).order_by(MasterTable.TableName)
            self.ui.cmbFIRTable.setModel(QueryTableModel(queryRecord))
            self.ui.cmbFIRTable.setModelColumn(1)
        self.blockFISignals(False)

    def on_FIRField_load(self, Table_id=None):
        queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation.id, FieldInformation.FieldName).filter_by(TableID=Table_id).order_by(FieldInformation.FieldName)
        self.blockFISignals(True)
        if queryRecord.first() is None:
            qryTable = self.instanceDict["ProgramBase"].session.query(MasterTable).filter_by(id=Table_id).first()

            if qryTable is not None:
                qryBase = self.instanceDict["ProgramBase"].session.query(SessionBase).filter_by(id=qryTable.Base).first()
                if qryBase is not None:
                    myColumnList = DatabaseTools.get_fields_by_tablename(bases[qryBase.NameText], qryTable.TableName)

                    for key, value in enumerate(myColumnList):
                        qryTableField = self.instanceDict["ProgramBase"].session.query(FieldInformation).filter_by(TableID=Table_id, FieldName=value).first()

                        if qryTableField is None:
                            self.instanceDict["ProgramBase"].session.begin()
                            qryTableField = FieldInformation(TableID=int(Table_id),
                                                             FieldName=str(value),
                                                             DataType_Value=str(myColumnList[value]))
                            self.instanceDict["ProgramBase"].session.add(qryTableField)
                            self.instanceDict["ProgramBase"].session.commit()
                            self.instanceDict["ProgramBase"].session.flush()

                        queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation.id, FieldInformation.FieldName).filter_by(
                            TableID=Table_id).order_by(FieldInformation.FieldName)
                        self.ui.cmbFIRField.setModel(QueryTableModel(queryRecord))
                        self.ui.cmbFIRField.setModelColumn(1)
        else:
            self.ui.cmbFIRField.setModel(QueryTableModel(queryRecord))
            self.ui.cmbFIRField.setModelColumn(1)

        self.blockFISignals(False)


    def on_cmbFormType_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormDesignPrimaryGroup.id, FormDesignPrimaryGroup.NameText)
        self.ui.cmbFormType.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFormType.setModelColumn(1)
        #self.ui.cmbFormType.setCurrentIndex(1)

    @QtCore.Slot(int)
    def on_cmbFormName_currentIndexChanged(self, index):
       self.on_tblFormItems_load(index)

    @QtCore.Slot()
    def on_cmdCreateForm_clicked(self):
       print("hi")

    def dictFormImport(self, formfileName):
        importDict = {}

        importDict["re"] = "import re"
        importDict["sys"] = "import sys"
        importDict["os"] = "import os"

        importDict["QtGui"] = "from qtpy import QtGui"
        importDict["QtCore"]= "from qtpy import QtCore"
        importDict["QtWidgets"] = "from qtpy.QtWidgets import *"

        importDict["QtUiTools"] = "from qtpy import QtUiTools"
        importDict["qtalchemy"] = "from qtalchemyPySide import *"

        importDict["uiFile"] = "uiFile = os.path.join(basePackagePath, %s)" % (formfileName)

        TableImport = []
        TableImport.append("from ProjectManager.Database import DatabaseTools")
        TableImport.append("from ProjectManager.Packages.ProgramBase.Database.dbBase import *")
        TableImport.append("from ProjectManager.Packages.ProgramBase.Database.dbMasterTables import *")
        TableImport.append("from ProjectManager.Packages.ProgramBase.Database.dbAllLists import *")
        TableImport.append("from ProjectManager.Packages.ProgramBase.Database.dbAllTables import *")

        importDict["TableImport"] = TableImport

        return importDict

    @QtCore.Slot()
    def on_cmdCreateFormBaseClass_clicked(self):
        formName = self.ui.lstForms.model().index(self.ui.lstForms.currentIndex().row(), 1).data()
        exportPath = self.ui.txtFormPath.text()

        copyrightyear = "2020-2021"
        copyrightauthor = "David Lario"
        copyrightAuthor = "## Copyright %s %s" % (copyrightyear, copyrightauthor)
        compileDate = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')

        fileName = "frm" + formName
        filefullpath = Packages.__path__[0] + "\\"

        filefullpath = os.path.join(exportPath, formName + ".py")

        copywritepath = os.path.join(basePackagePath, "gnu.txt")

        importblock = self.dictFormImport(fileName+ ".ui")

        classline = "class %s(QMdiSubWindow):\n" % (fileName)
        classline += "    def __init__(self, packageName):\n"
        classline += "        super(%s, self).__init__(packageName)\n" % (fileName)

        spaces = "    "
        with open(filefullpath, 'w') as f:

            f.write(copyrightAuthor + "\n")
            f.write("## " + compileDate+ "\n\n")

            f2 = open(copywritepath, "r")

            for index, lineitem in enumerate(f2):
                if lineitem == '\n':
                    f.write(lineitem)
                else:
                    f.write("## " + lineitem)

            f.write("\n\n")

            for row, importItem in enumerate(importblock):
                if importItem == "TableImport":
                    for importItem2 in importblock[importItem]:
                        f.write(importItem2 + "\n")
                else:
                    f.write(importblock[importItem] + "\n")

            f.write("\n")
            f.write(classline)
            qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate.id,
                                                                              FormFunctionTemplate.FunctionName)
            form_id = 1
            selectedItems = self.ui.lstFormFunctions.selectionModel().selectedIndexes()

            for itemsselected in selectedItems:
                template_id = self.ui.lstFormFunctions.model().index(itemsselected.row(), 0).data()

                if len(self.on_GetTemplate(form_id, template_id)):

                    f.write(self.on_GetTemplate(form_id, template_id))
                    f.write("\n\n")

        print("Done")

    def on_GetTemplate(self, rg_id, Record_id):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(id=Record_id).first()
        spaces = "    "
        if qryRecord.Filename is not None:
            f2 = open(os.path.join(qryRecord.FunctionPath, qryRecord.Filename), "r")
            self.ui.txtFunctionTemplateCode.setPlainText(f2.read())


        #rg_id = self.ui.cmbFITRecordGroup.model().index(self.ui.cmbFITRecordGroup.currentIndex(), 0).data()
        #frm_id = self.ui.cmbFITRecordGroup.model().index(self.ui.cmbFITRecordGroup.currentIndex(), 0).data()

        self.createRGDictFromDatabase(rg_id)

        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(id=Record_id).first()
        qryFormRecord = self.instanceDict["ProgramBase"].session.query(FormItemData).filter_by(RecordGroupID=int(rg_id)).all()

        if qryRecord.Filename is not None:
            f = open(os.path.join(qryRecord.FunctionPath, qryRecord.Filename), "r")
            textbody = ""

            processdelay = False
            bufferlist = []
            f2 = [spaces + textline for textline in f] #Add spaces

            for textline in f2:
                if processdelay == False:
                    if "{BeginWidgetList}" in textline:
                        bufferlist = []
                        processdelay = True
                    else:
                        #Process the Line Item
                        itemlist = set(re.findall('\{.*?\}', textline))
                        for item in itemlist:
                            if "RecordGroup." in item:
                                if item[13:-1] in self.RGDict:
                                    #print("found", item[13:-1], self.RGDict[item[13:-1]])
                                    itemdictname = self.RGDict[item[13:-1]]
                                    textline = textline.replace(item, itemdictname)
                                else:
                                    print("not found", self.RGDict)
                            else:
                                print(textline)
                        textbody += textline
                else:
                    if "{EndWidgetList}" in textline:

                        # Process the Block
                        #self.createFIDictFromDatabase(record.id)
                        for record in qryFormRecord:
                            FormRecordDict = record.__dict__
                            '''print(FormRecordDict)'''
                            print(bufferlist)
                            for bufferitem in bufferlist:
                                itemlist = set(re.findall('\{.*?\}', bufferitem))
                                textline = bufferitem
                                for item in itemlist:
                                    if "SubFunction" in item:
                                        textline = ""
                                        FunctionName = re.search('\((.*)\[', bufferitem).group(0)
                                        RegionName = re.search('\[\{(.*)\}\]', bufferitem).group(0)

                                        if "RecordGroup.Form." in RegionName:
                                            if RegionName[19:-2] in FormRecordDict:
                                                itemdictname = FormRecordDict[RegionName[19:-2]]
                                                if RegionName[19:-2] == "WidgetType":
                                                    qryWidgetType = self.instanceDict["ProgramBase"].session.query(WidgetData).filter_by(id=int(itemdictname)).first()
                                                    RegionNameValue = qryWidgetType.Title

                                        sublist = self.SubFunction(FunctionName[1:-1], RegionNameValue)
                                        print(FormRecordDict["ItemName"], FunctionName[1:-1], RegionNameValue, bufferitem)
                                        for subitem in sublist:
                                            #print(subitem)
                                            textline = subitem
                                            itemlist2 = set(re.findall('\{.*?\}', subitem))
                                            for item2 in itemlist2:
                                                #print(item2)
                                                if "RecordGroup.Form." in item2:
                                                    if item2[18:-1] in FormRecordDict:
                                                        itemdictname = FormRecordDict[item2[18:-1]]
                                                        #print(item2)
                                                        if itemdictname is not None:
                                                            textline = textline.replace(item2, itemdictname)
                                                        else:
                                                            textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                            print("Item Not FoundS2", FormRecordDict, bufferitem, item, itemdictname)

                                                elif "RecordGroup." in item2:
                                                    if item2[13:-1] in self.RGDict:
                                                        itemdictname = self.RGDict[item2[13:-1]]

                                                        if itemdictname is not None:
                                                            textline = textline.replace(item2, itemdictname)
                                                        else:
                                                            textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                            print("Item Not FoundS2", FormRecordDict, bufferitem, item, itemdictname)

                                                    else:
                                                        print("not found", item)

                                            textbody += textline
                                        textline = ""
                                        textbody += "\n"

                                    elif "RecordGroup.Form." in item:
                                        if item[18:-1] in FormRecordDict:
                                            itemdictname = FormRecordDict[item[18:-1]]
                                            if itemdictname is not None:
                                                textline = textline.replace(item, str(itemdictname))
                                            else:
                                                textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                print("Item Not Found1", FormRecordDict, bufferitem, item, itemdictname)

                                    elif "RecordGroup." in item:
                                        #print("test", item[13:-1])
                                        if item[13:-1] in self.RGDict:
                                            #print("found", item[13:-1], self.RGDict[item[13:-1]])
                                            itemdictname = self.RGDict[item[13:-1]]
                                            if itemdictname is not None:
                                                textline = textline.replace(item, itemdictname)
                                            else:
                                                textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                print("Item Not Found2", FormRecordDict, bufferitem, item, itemdictname)
                                        else:
                                            print("not found", item)

                            textbody += textline
                        bufferlist = []
                        processdelay = False
                        textbody += "\n\n"
                    else:
                        #Build the Block
                        bufferlist.append(textline)
            return textbody

    @QtCore.Slot()
    def on_lstForms_clicked(self):
        form_id = self.ui.lstForms.model().index(self.ui.lstForms.currentIndex().row(), 0).data()
        self.on_lstFormFields_load(form_id)

    def on_lstFormFields_load(self, formIndex=None):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormItemData.id, FormItemData.RecordGroupID, FormItemData.ItemName)
        if formIndex:
            qryRecord = qryRecord.filter_by(RecordGroupID=formIndex)
        self.ui.lstFormFields.setModel(QueryTableModel(qryRecord))
        self.ui.lstFormFields.setModelColumn(2)

    def on_cmbFormName_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormDesignSecondaryGroup.id, FormDesignSecondaryGroup.NameText)
        self.ui.cmbFormName.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFormName.setModelColumn(1)

        self.ui.lstForms.setModel(QueryTableModel(qryRecord))
        self.ui.lstForms.setModelColumn(1)

    def on_tblFormItems_load(self, formIndex=None):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormItemData.id, FormItemData.RecordGroupID, FormItemData.ItemName)
        if formIndex:
            qryRecord = qryRecord.filter_by(RecordGroupID=formIndex)
        self.ui.tblFormItems.setModel(QueryTableModel(qryRecord))
        self.ui.tblFormItems.setColumnWidth(0,0)

    def initFTTreeView(self):
        self.tvFTdict = {}


    def on_FITreeView_load(self):
        pass

    def on_cmdAdvanceFormItemsTreeView_clicked(self):
        self.initFTTreeView()
        self.NewMeetingManager = TreeBuilderEntity(self.tvFTdict, "tblTaskSettings", sessions, bases, FormBuilder)

    def on_FIDataGroup_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroup.id, RecordGroup.Title)
        self.ui.cmbFIDataGroup.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFIDataGroup.setModelColumn(1)

    def on_FIWidgetType_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetData.id, WidgetData.Title)
        self.ui.cmbFIWidgetType.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFIWidgetType.setModelColumn(1)

    def on_FISetValue_load(self, Widget_id=None):
        if Widget_id is None:
            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(Direction=1)
        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(WidgetID=Widget_id, Direction=1)

        self.ui.cmbFISetValue.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFISetValue.setModelColumn(1)

    def on_FIGetValue_load(self, Widget_id=None):
        if Widget_id is None:
            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(Direction=2)
        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(WidgetID=Widget_id, Direction=2)

        self.ui.cmbFIGetValue.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFIGetValue.setModelColumn(1)

    def on_FIUpdateValue_load(self, Widget_id=None):
        if Widget_id is None:
            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(Direction=3)
        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(WidgetID=Widget_id, Direction=3)

        self.ui.cmbFIUpdateValue.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFIUpdateValue.setModelColumn(1)

    def on_FIField_load(self, Table_id):
        queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation.id, FieldInformation.FieldName).filter_by(TableID=Table_id).order_by(FieldInformation.FieldName)

        if queryRecord.first() is None:
            qryTable = self.instanceDict["ProgramBase"].session.query(MasterTable).filter_by(id=Table_id).first()

            if qryTable is not None:
                qryBase = self.instanceDict["ProgramBase"].session.query(SessionBase).filter_by(id=qryTable.Base).first()
                if qryBase is not None:
                    myColumnList = DatabaseTools.get_fields_by_tablename(bases[qryBase.NameText], qryTable.TableName)

                    for key, value in enumerate(myColumnList):
                        qryTableField = self.instanceDict["ProgramBase"].session.query(FieldInformation).filter_by(TableID=Table_id, FieldName=value).first()

                        if qryTableField is None:
                            self.instanceDict["ProgramBase"].session.begin()
                            print(Table_id, value, myColumnList[value])
                            qryTableField = FieldInformation(TableID=int(Table_id),
                                                             FieldName=str(value),
                                                             DataType_Value=str(myColumnList[value]))
                            self.instanceDict["ProgramBase"].session.add(qryTableField)
                            self.instanceDict["ProgramBase"].session.commit()
                            self.instanceDict["ProgramBase"].session.flush()

                        queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation.id, FieldInformation.FieldName).filter_by(TableID=Table_id).order_by(FieldInformation.FieldName)
                        self.ui.cmbFIField.setModel(QueryTableModel(queryRecord))
                        self.ui.cmbFIField.setModelColumn(1)
        else:
            self.ui.cmbFIField.setModel(QueryTableModel(queryRecord))
            self.ui.cmbFIField.setModelColumn(1)

    def on_FIForm_load(self, Record_id):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormItemData).filter_by(id=Record_id).first()
        self.init_FIDict()
        self.init_FIForm()
        self.blockFISignals(True)

        if qryRecord.RecordGroupID is not None:
            for row in range(self.ui.cmbFIDataGroup.model().rowCount()):
                if int(self.ui.cmbFIDataGroup.model().index(row, 0, None).data()) == int(qryRecord.RecordGroupID):
                    self.ui.cmbFIDataGroup.setCurrentIndex(row)
                    break
            self.FormItemDict["RecordGroup"] = {"Record_id": qryRecord.RecordGroupID,
                                              "Value": self.ui.cmbFIDataGroup.model().index(row, 1, None).data(),
                                              "Row": row}

        qryRecordGroup = self.instanceDict["ProgramBase"].session.query(RecordGroup).filter_by(id=qryRecord.RecordGroupID).first()

        if qryRecordGroup is not None:
            for row in range(self.ui.cmbFISession.model().rowCount()):
                if int(self.ui.cmbFISession.model().index(row, 0, None).data()) == int(qryRecordGroup.SessionID):
                    self.ui.cmbFISession.setCurrentIndex(row)
                    break

            if qryRecordGroup.TableID is not None:
                self.on_FITable_load(Session=qryRecordGroup.SessionID)
                self.on_FIField_load(qryRecordGroup.TableID)

                for row in range(self.ui.cmbFITable.model().rowCount()):
                    if int(self.ui.cmbFITable.model().index(row, 0, None).data()) == int(qryRecordGroup.TableID):
                        self.ui.cmbFITable.setCurrentIndex(row)
                        break
            else:
                self.ui.cmbFITable.setCurrentIndex(-1)

        if qryRecord.WidgetType is not None:
            for row in range(self.ui.cmbFIWidgetType.model().rowCount()):
                if int(self.ui.cmbFIWidgetType.model().index(row, 0, None).data()) == int(qryRecord.WidgetType):
                    self.ui.cmbFIWidgetType.setCurrentIndex(row)
                    break
            self.FormItemDict["WidgetType"] = {"Record_id": qryRecord.WidgetType,
                                              "Value": self.ui.cmbFIWidgetType.model().index(row, 1, None).data(),
                                              "Row": row}

            if self.FormItemDict["WidgetType"]["Record_id"] == 7:
                self.ui.gbFITreeView.setMaximumHeight(16777215)
            else:
                self.ui.gbFITreeView.setMaximumHeight(0)

            qryRecord3 = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(Direction=3, WidgetID=qryRecord.WidgetType)

            self.ui.cmbFIUpdateValue.setModel(QueryTableModel(qryRecord3))
            self.ui.cmbFIUpdateValue.setModelColumn(1)
            self.ui.cmbFIUpdateValue.setCurrentIndex(-1)

        if qryRecord.ItemName is not None:
            self.ui.txtFIItemName.setText(qryRecord.ItemName)
            self.FormItemDict["ItemName"] = {"Value": qryRecord.ItemName}

        if qryRecord.DefaultValue is not None:
            self.ui.txtFIDefaultValue.setText(qryRecord.DefaultValue)
            self.FormItemDict["DefaultValue"] = {"Value": qryRecord.DefaultValue}

        if qryRecord.WidgetName is not None:
            self.ui.txtFIWidgetName.setText(qryRecord.WidgetName)
            self.FormItemDict["WidgetName"] = {"Value": qryRecord.WidgetName}

        self.on_FISetValue_load(qryRecord.WidgetType)

        if qryRecord.SetValue is not None:
            for row in range(self.ui.cmbFISetValue.model().rowCount()):

                if int(self.ui.cmbFISetValue.model().index(row, 0, None).data()) == int(qryRecord.SetValue):
                    self.ui.cmbFISetValue.setCurrentIndex(row)
                    setString = str(self.ui.cmbFISetValue.model().index(row, 1, None).data())
                    self.FormItemDict["SetValue"] = {"Record_id": qryRecord.SetValue,
                                                     "Value": setString,
                                                     "Row": row}

                    self.ui.txtFISetString.setText("self.ui." + self.ui.txtFIWidgetName.text() + setString)

                    if qryRecord.DefaultValue is not None:
                        self.ui.txtFISetString.setText("self.ui." + self.ui.txtFIWidgetName.text() + "." + setString)
                        newcommand = setString.replace("value", str(qryRecord.DefaultValue))
                        self.ui.txtFIClearWidget.setText("self.ui." + self.ui.txtFIWidgetName.text() + "." + newcommand)

                    break
        else:
            self.ui.cmbFISetValue.setCurrentIndex(-1)

        self.on_FIGetValue_load()
        if qryRecord.GetValue is not None:
            for row in range(self.ui.cmbFIGetValue.model().rowCount()):
                if int(self.ui.cmbFIGetValue.model().index(row, 0, None).data()) == int(qryRecord.GetValue):
                    self.ui.cmbFIGetValue.setCurrentIndex(row)
                    getString = str(self.ui.cmbFIGetValue.model().index(row, 1, None).data())
                    self.FormItemDict["GetValue"] = {"Record_id": qryRecord.GetValue,
                                                     "Value": str(self.ui.cmbFIGetValue.model().index(row, 1, None).data()),
                                                     "Row": row}
                    self.ui.txtFIGetString.setText("self.ui." + self.ui.txtFIWidgetName.text() + "." + getString)
                    break

        if qryRecord.UpdateValue is not None:
            for row in range(self.ui.cmbFIUpdateValue.model().rowCount()):
                if int(self.ui.cmbFIUpdateValue.model().index(row, 0, None).data()) == int(qryRecord.UpdateValue):
                    self.ui.cmbFIUpdateValue.setCurrentIndex(row)
                    updateString = str(self.ui.cmbFIUpdateValue.model().index(row, 1, None).data())
                    self.FormItemDict["UpdateValue"] = {"Record_id": qryRecord.UpdateValue,
                                                        "Value": self.ui.cmbFIUpdateValue.model().index(row, 1, None).data(),
                                                        "Row": row}
                    self.ui.txtFIUpdateString.setText("self.ui." + self.ui.txtFIWidgetName.text() + "." + updateString)
                    break


        if qryRecord.QueryRecord is not None:
            self.ui.txtFIQueryRecord.setText(qryRecord.QueryRecord)
            self.FormItemDict["QueryRecord"] = {"Value": qryRecord.QueryRecord}

        if qryRecord.ClearWidget is not None:
            self.ui.txtFIClearWidget.setText(qryRecord.ClearWidget)
            self.FormItemDict["ClearWidget"] = {"Value": qryRecord.ClearWidget}

        if qryRecord.FilterCheckBox is not None:
            self.ui.txtFIFilterCheck.setText(qryRecord.FilterCheckBox)
            self.FormItemDict["FilterCheck"] = {"Value": qryRecord.FilterCheckBox}

        if qryRecord.Description is not None:
            self.ui.txtFIDescription.setText(qryRecord.Description)
            self.FormItemDict["Description"] = {"Value": qryRecord.Description}

        if qryRecord.DatabaseField is not None:
            for row in range(self.ui.cmbFIField.model().rowCount()):
                if int(self.ui.cmbFIField.model().index(row, 0, None).data()) == int(qryRecord.DatabaseField):
                    self.ui.cmbFIField.setCurrentIndex(row)
                    self.FormItemDict["DatabaseField"] = {"Record_id": qryRecord.DatabaseField,
                                                          "Value": self.ui.cmbFIField.model().index(row, 1, None).data(),
                                                          "Row": row}
                    queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation).filter_by(
                        id=int(qryRecord.DatabaseField)).first()
                    self.ui.txtFIDatabaseFieldType.setText(queryRecord.DataType_Value)

                    break


        if qryRecord.ViewOrder is not None:
            self.ui.txtFIViewOrder.setText(str(qryRecord.ViewOrder))
            self.FormItemDict["ViewOrder"] = {"Value": qryRecord.ViewOrder}

        if qryRecord.Label is not None:
            self.ui.txtFILabel.setText(qryRecord.Label)
            self.FormItemDict["Label"] = {"Value": qryRecord.Label}

        if qryRecord.ReferenceSession is not None:
            for row in range(self.ui.cmbFIRSession.model().rowCount()):
                if int(self.ui.cmbFIRSession.model().index(row, 0, None).data()) == int(qryRecord.ReferenceSession):
                    self.ui.cmbFIRSession.setCurrentIndex(row)
                    self.FormItemDict["ReferenceSession"] = {"Record_id": qryRecord.ReferenceSession,
                                                             "Value": self.ui.cmbFIRSession.model().index(row, 1, None).data(),
                                                             "Row": row}
                    self.on_FIRTable_load(qryRecord.ReferenceSession)
                    break


        if qryRecord.ReferenceTable is not None:
            for row in range(self.ui.cmbFIRTable.model().rowCount()):
                if int(self.ui.cmbFIRTable.model().index(row, 0, None).data()) == int(qryRecord.ReferenceTable):
                    self.ui.cmbFIRTable.setCurrentIndex(row)
                    self.FormItemDict["ReferenceTable"] = {"Record_id": qryRecord.ReferenceTable,
                                                           "Value": self.ui.cmbFIRTable.model().index(row, 1, None).data(),
                                                           "Row": row}
                    self.on_FIRField_load(qryRecord.ReferenceTable)
                    break


        if qryRecord.ReferenceField is not None:
            for row in range(self.ui.cmbFIRField.model().rowCount()):
                if int(self.ui.cmbFIRField.model().index(row, 0, None).data()) == int(qryRecord.ReferenceField):
                    self.ui.cmbFIRField.setCurrentIndex(row)
                    self.FormItemDict["ReferenceField"] = {"Record_id": qryRecord.ReferenceField,
                                                           "Value": self.ui.cmbFIRField.model().index(row, 1, None).data(),
                                                           "Row": row}
                    break

        if qryRecord.JoinVariable is not None:
            self.ui.txtFIJoinVariable.setText(qryRecord.JoinVariable)
            self.FormItemDict["JoinVariable"] = {"Value": qryRecord.JoinVariable}

        self.blockFISignals(False)

    def on_tvFormItems_load(self):
        self.initFTTreeView()
        self.ui.tvFormItems.setModel(None)
        '''self.tvFormItemsmodel = TreeViewAlchemy2.linkedtreemodel(self.MasterData, treedicts["FormBuilder"], header="Dave Rocks")

        if False:
            treepath = []
            taglist = []
            MasterTable_id = 29
            Parent_id = "(0)"
            GenerateParent_id = 0
            ItemLevel = -1

            querytreepath = sessions["ProjectManager"].query(FormDesignTree).filter_by(PrimaryGroup_id=1, SecondaryGroup_id=876, ParentTree_id="(0)").first()

            self.tvFormItemsmodel.readtvtreebranch(treepath, taglist, querytreepath.Tree_id, ItemLevel)

        else:
            self.tvFormItemsmodel = TreeViewAlchemy2.linkedtreemodel(self.MasterData, treedicts["FormBuilder"], header="Dave Rocks")
            mrilist = []
            querytreepath = sessions["ProjectManager"].query(FormDesignTree).filter_by(PrimaryGroup_id=1, ParentTree_id="(0)").all()

            for records in querytreepath:
                SecondaryGroup_id = records.SecondaryGroup_id
                PrimaryGroup_id = records.PrimaryGroup_id
                modelrootitem = sessions["ProjectManager"].query(FormDesignTree).filter_by(
                    ParentTree_id="(0)") \
                    .filter_by(PrimaryGroup_id=PrimaryGroup_id) \
                    .filter_by(SecondaryGroup_id=SecondaryGroup_id) \
                    .order_by(self.tvFTdict["TreeItems"].ItemOrder) \
                    .order_by(self.tvFTdict["TreeItems"].DisplayName).first()

                if modelrootitem is not None:
                    data = {}
                    data["root_id"] = modelrootitem.id
                    data["SourcePG"] = PrimaryGroup_id
                    data["SourceSG"] = modelrootitem.SecondaryGroup_id
                    data["DestinationPG"] = None
                    data["DestinationSG"] = None

                    mrilist.append(data)

            if mrilist != []:
                self.tvFormItemsmodel.setupModelData(sessions["ProjectManager"], FormDesignTree, mrilist)

        self.ui.tvFormItems.setModel(self.tvFormItemsmodel)'''

    def on_cmdRefreshFormItemsTreeView_clicked(self):
        self.createTreeFromData()

    def on_tvFormItems_clicked(self, index):
        itemselected = index.internalPointer()
        TreePath = itemselected.TreeClassItem.TreePath
        # print(itemselected.TreeClassItem.Tree_id, itemselected.TreeClassItem.TreePath)
        if TreePath != None:
            sTreePath = DatabaseTools.myListToStr(TreePath)
            record = self.tvFTdict["Session"].query(self.tvFTdict["TreeItems"]).filter(self.tvFTdict["TreeItems"].TreePath==sTreePath).first()
            if record:
                if record.ItemTable_id == 514:
                    self.init_WidgetForm()
                    self.blockWSignals(True)
                    self.ui.txtFormItem_id.setText(str(record.Item_id))
                    self.on_FIForm_load(int(record.Item_id))

                self.blockWSignals(False)

    def createTreeFromData(self):
        #Root Record Group
        sessions["ProjectManager"].begin()
        treerecords = sessions["ProjectManager"].query(FormDesignTree)
        treerecords.delete(synchronize_session=False)
        sessions["ProjectManager"].commit()


        self.initFTTreeView()

        AddLevel = None
        self.TVTreeGroup = TreeViewAlchemy2.linkedtreemodel(bases, sessions, self.tvFTdict, header="Tree Stuff")

        #Create the first Record as Blank
        queryPrimaryGroup = self.tvFTdict["Session"].query(self.tvFTdict["PrimaryGroup"]).all()
        if queryPrimaryGroup is None:
            self.tvFTdict["Session"].begin()
            queryPrimaryGroup = self.tvFTdict["PrimaryGroup"]()
            self.tvFTdict["Session"].add(queryPrimaryGroup)
            self.tvFTdict["Session"].commit()
            self.tvFTdict["Session"].flush()

        # Add Category if Not there
        queryPrimaryGroup = self.tvFTdict["Session"].query(self.tvFTdict["PrimaryGroup"]).filter_by(NameText="By Form Group").first()
        if queryPrimaryGroup is None:
            self.tvFTdict["Session"].begin()
            queryPrimaryGroup = self.tvFTdict["PrimaryGroup"](NameText="By Form Group")
            self.tvFTdict["Session"].add(queryPrimaryGroup)
            self.tvFTdict["Session"].commit()
            self.tvFTdict["Session"].flush()

        SecondaryGroup_id = self.tvFTdict["Session"].query(self.tvFTdict["SecondaryGroup"]).filter_by(PrimaryGroup_id=queryPrimaryGroup.id).count()
        # Add Blank Zero Record
        querySecondaryGroup = self.tvFTdict["Session"].query(self.tvFTdict["SecondaryGroup"]).filter_by(PrimaryGroup_id=queryPrimaryGroup.id).first()

        #Create the First Secondary Group if it does Not Exist
        if querySecondaryGroup is None:
            SecondaryGroup_id = 1
            self.tvFTdict["Session"].begin()
            querySecondaryGroup = self.tvFTdict["SecondaryGroup"](NameText="", PrimaryGroup_id=queryPrimaryGroup.id, SecondaryGroup_id=SecondaryGroup_id)
            self.tvFTdict["Session"].add(querySecondaryGroup)
            self.tvFTdict["Session"].commit()
            self.tvFTdict["Session"].flush()

        #Build The Tree
        queryRecordGroup = sessions["ProjectManager"].query(RecordGroup).order_by(RecordGroup.Title).all()

        #Top Level is The Record Groups
        for record in queryRecordGroup:

            #Each Category is a Separate SecondaryGroup_i
            SecondaryGroup_id += 1
            self.tvFTdict["Session"].begin()
            NewSecondaryGroup = self.tvFTdict["SecondaryGroup"](NameText=record.Title, PrimaryGroup_id=queryPrimaryGroup.id,
                                                                SecondaryGroup_id=SecondaryGroup_id)
            self.tvFTdict["Session"].add(NewSecondaryGroup)
            self.tvFTdict["Session"].commit()
            self.tvFTdict["Session"].flush()

            newtreeitemdata = self.TVTreeGroup.defaultTreeItem()
            newtreeitemdata['PrimaryGroup_id'] = 1
            newtreeitemdata['SecondaryGroup_id'] = SecondaryGroup_id
            newtreeitemdata['DestinationPG'] = 1
            newtreeitemdata['DestinationSG'] = SecondaryGroup_id

            newtreeitemdata['ParentTree_id'] = "(0)"

            newtreeitemdata["id"] = record.id
            newtreeitemdata["ItemTable_id"] = 520
            newtreeitemdata['Item_id'] = record.id
            newtreeitemdata["ItemMaster_id"] = 673
            newtreeitemdata["MasterTable_id"] = 673
            newtreeitemdata['DisplayName'] = record.Title
            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['Header'] = None

            GenerateTable = self.tvFTdict["TreeItems"]
            treedata = self.TVTreeGroup.AddTreeRoot("Ginger", [], newtreeitemdata=newtreeitemdata, LinkedTable=GenerateTable)

            queryRecordGroup = sessions["ProjectManager"].query(FormItemData.id, FormItemData.ItemName, WidgetType.NameText) \
                .outerjoin(WidgetType, FormItemData.WidgetType == WidgetType.id) \
                .filter(FormItemData.RecordGroupID == record.id) \
                .order_by(WidgetType.NameText, FormItemData.ItemName).all()

            parenttreepath = ["(0)"]

            for record2 in queryRecordGroup:

                newtreeitemdata2 = self.TVTreeGroup.defaultTreeItem()
                newtreeitemdata2['PrimaryGroup_id'] = 1
                newtreeitemdata2['SecondaryGroup_id'] = SecondaryGroup_id
                newtreeitemdata2['DestinationPG'] = 1
                newtreeitemdata2['DestinationSG'] = SecondaryGroup_id

                newtreeitemdata2['id'] = record2.id
                newtreeitemdata2['TreePath'] = [treedata["Tree_id"]]
                newtreeitemdata2['ParentTree_id'] = treedata["Tree_id"]
                newtreeitemdata2["ItemTable_id"] = 514
                newtreeitemdata2['Item_id'] = record2.id
                newtreeitemdata2['DisplayName'] = record2.ItemName
                newtreeitemdata2["ItemMaster_id"] = 673 #Regressed
                newtreeitemdata2["MasterTable_id"] = 673
                newtreeitemdata2['ItemLevel'] = 1
                newtreeitemdata2['Header'] = None

                print(newtreeitemdata2['ParentTree_id'])
                treeid2 = self.TVTreeGroup.addTreeItem(GenerateTable, newtreeitemdata2)

        self.ui.tvFormItems.setModel(self.TVTreeGroup)

    @QtCore.Slot()
    def on_tblFormItems_clicked(self):
        self.init_WidgetForm()
        self.blockWSignals(True)
        data = {}
        data["row"] = self.ui.tblFormItems.selectionModel().currentIndex().row()
        data["column"] = self.ui.tblFormItems.selectionModel().currentIndex().column()
        data["column"] = self.ui.tblFormItems.selectionModel().currentIndex().column()
        data["Value"] = self.ui.tblFormItems.model().index(data["row"], data["column"], None).data()
        data["id"] = self.ui.tblFormItems.model().index(data["row"], 0, None).data()

        self.ui.txtFormItem_id.setText(str(data["id"]))

        if data["id"] is not None:
            self.on_FIForm_load(int(data["id"]))

        self.blockWSignals(False)

    @QtCore.Slot()
    def on_cmdCreateNewFormItem_clicked(self):
        self.createsaveFormItem(None, None, None)

    @QtCore.Slot()
    def on_cmdCreateNewFormItem_2_clicked(self):
        DG_id = int(self.ui.cmbFIDataGroup.model().index(self.ui.cmbFIDataGroup.currentIndex(), 0, None).data())
        self.createsaveFormItem(None, DG_id, None)

    @QtCore.Slot()
    def on_cmdCreateNewVCombobox_clicked(self):
        self.createsaveFormItem(None, None, "ComboBox")

    @QtCore.Slot()
    def on_cmdCreateNewVSpnBox_clicked(self):
        self.createsaveFormItem(None, None, "SpnBox")

    @QtCore.Slot()
    def on_cmdCreateNewVDateTime_clicked(self):
        self.createsaveFormItem(None, None, "DateTime")

    @QtCore.Slot()
    def on_cmdCreateNewVTreeView_clicked(self):
        self.createsaveFormItem(None, None, "TreeView")

    @QtCore.Slot()
    def on_cmdCreateNewVTable_clicked(self):
        self.createsaveFormItem(None, None, "Table")

    @QtCore.Slot()
    def on_cmdCreateNewVList_clicked(self):
        self.createsaveFormItem(None, None, "List")

    @QtCore.Slot()
    def on_cmdCreateNewVCheckBox_clicked(self):
        self.createsaveFormItem(None, None, "CheckBox")


    def createsaveFormItem(self, record_id=None, DataGroup_id=None, Widget=None):

        if record_id is None:
            WidgetType = None

            if Widget == "ComboBox":
                WidgetType = 6

            if Widget == "SpnBox":
                WidgetType = 16

            if Widget == "DateTime":
                WidgetType = 10

            if Widget == "TreeView":
                WidgetType = 7

            if Widget == "Table":
                WidgetType = 14

            if Widget == "List":
                WidgetType = 19

            if Widget == "CheckBox":
                WidgetType = 2

            self.instanceDict["ProgramBase"].session.begin()

            qryRecord = FormItemData(RecordGroupID=DataGroup_id, WidgetType=WidgetType)
            self.instanceDict["ProgramBase"].session.add(qryRecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(FormItemData).filter_by(id=record_id).first()
            self.instanceDict["ProgramBase"].session.begin()

            if self.FormItemDict["RecordGroup"] is not None: qryRecord.RecordGroupID = self.FormItemDict["RecordGroup"]["Record_id"]
            if self.FormItemDict["WidgetType"] is not None: qryRecord.WidgetType = self.FormItemDict["WidgetType"]["Record_id"]
            if self.FormItemDict["ItemName"] is not None: qryRecord.ItemName = str(self.FormItemDict["ItemName"]["Value"])
            if self.FormItemDict["DefaultValue"] is not None: qryRecord.DefaultValue = str(self.FormItemDict["DefaultValue"]["Value"])
            if self.FormItemDict["WidgetName"] is not None: qryRecord.WidgetName = str(self.FormItemDict["WidgetName"]["Value"])
            if self.FormItemDict["SetValue"] is not None: qryRecord.SetValue = self.FormItemDict["SetValue"]["Record_id"]
            if self.FormItemDict["GetValue"] is not None: qryRecord.GetValue = self.FormItemDict["GetValue"]["Record_id"]
            if self.FormItemDict["GetString"] is not None: qryRecord.GetString = str(self.FormItemDict["GetString"]["Value"])
            if self.FormItemDict["UpdateValue"] is not None: qryRecord.UpdateValue = self.FormItemDict["UpdateValue"]["Record_id"]
            if self.FormItemDict["QueryRecord"] is not None: qryRecord.QueryRecord = str(self.FormItemDict["QueryRecord"]["Value"])
            #if self.FormItemDict["ClearWidget"] is not None: qryRecord.ClearWidget = str(self.FormItemDict["ClearWidget"]["Value"])
            if self.FormItemDict["FilterCheck"] is not None: qryRecord.FilterCheckBox = str(self.FormItemDict["FilterCheck"]["Value"])
            if self.FormItemDict["Description"] is not None: qryRecord.Description = str(self.FormItemDict["Description"]["Value"])
            if self.FormItemDict["DatabaseField"] is not None: qryRecord.DatabaseField = str(self.FormItemDict["DatabaseField"]["Record_id"])
            if self.FormItemDict["ViewOrder"] is not None: qryRecord.ViewOrder = str(self.FormItemDict["ViewOrder"]["Value"])
            if self.FormItemDict["Label"] is not None: qryRecord.Label = str(self.FormItemDict["Label"]["Value"])
            if self.FormItemDict["ReferenceSession"] is not None: qryRecord.ReferenceSession = str(self.FormItemDict["ReferenceSession"]["Record_id"])
            if self.FormItemDict["ReferenceTable"] is not None: qryRecord.ReferenceTable = str(self.FormItemDict["ReferenceTable"]["Record_id"])
            if self.FormItemDict["ReferenceField"] is not None: qryRecord.ReferenceField = str(self.FormItemDict["ReferenceField"]["Record_id"])
            if self.FormItemDict["JoinVariable"] is not None: qryRecord.JoinVariable = str(self.FormItemDict["JoinVariable"]["Value"])

            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        self.on_tblFormItems_load()
        return qryRecord.id

    def init_FIForm(self):
        self.blockFISignals(True)
        self.ui.cmbFIDataGroup.setCurrentIndex(-1)
        self.ui.cmbFIWidgetType.setCurrentIndex(-1)
        self.ui.txtFIItemName.setText("")
        self.ui.txtFIDefaultValue.setText("")
        self.ui.txtFIWidgetName.setText("")
        self.ui.cmbFISetValue.setCurrentIndex(-1)
        self.ui.txtFISetString.setText("")
        self.ui.cmbFIGetValue.setCurrentIndex(-1)
        self.ui.txtFIGetString.setText("")
        self.ui.cmbFIUpdateValue.setCurrentIndex(-1)
        self.ui.txtFIUpdateString.setText("")
        self.ui.txtFIQueryRecord.setText("")
        self.ui.txtFIClearWidget.setText("")
        self.ui.txtFIFilterCheck.setText("")
        self.ui.txtFIDescription.setText("")
        self.ui.cmbFITable.setCurrentIndex(-1)
        self.ui.cmbFIField.setCurrentIndex(-1)
        self.ui.txtFIViewOrder.setText("")
        self.ui.txtFILabel.setText("")
        self.ui.cmbFIRSession.setCurrentIndex(-1)
        self.ui.cmbFIRTable.setCurrentIndex(-1)
        self.ui.cmbFIRField.setCurrentIndex(-1)
        self.ui.txtFIJoinVariable.setText("")
        self.blockFISignals(False)

    def loadFIForm(self):
        self.blockFISignals(True)
        self.ui.cmbFIDataGroup.setCurrentIndex(-1)
        self.ui.cmbFIWidgetType.setCurrentIndex(-1)
        self.ui.txtFIItemName.setText("")
        self.ui.txtFIDefaultValue.setText("")
        self.ui.txtFIWidgetName.setText("")
        self.ui.cmbFISetValue.setCurrentIndex(-1)
        self.ui.txtFISetString.setText("")
        self.ui.cmbFIGetValue.setCurrentIndex(-1)
        self.ui.txtFIGetString.setText("")
        self.ui.cmbFIUpdateValue.setCurrentIndex(-1)
        self.ui.txtFIUpdateString.setText("")
        self.ui.txtFIQueryRecord.setText("")
        self.ui.txtFIClearWidget.setText("")
        self.ui.txtFIFilterCheck.setText("")
        self.ui.txtFIDescription.setText("")
        self.ui.cmbFITable.setCurrentIndex(-1)
        self.ui.cmbFIField.setCurrentIndex(-1)
        self.ui.txtFIViewOrder.setText("")
        self.ui.txtFILabel.setText("")
        self.ui.cmbFIRSession.setCurrentIndex(-1)
        self.ui.cmbFIRTable.setCurrentIndex(-1)
        self.ui.cmbFIRField.setCurrentIndex(-1)
        self.ui.txtFIJoinVariable.setText("")
        self.blockFISignals(False)

    def init_FIDict(self):
        self.FormItemDict = {}
        self.FormItemDict["RecordGroup"] = None
        self.FormItemDict["WidgetType"] = None
        self.FormItemDict["ItemName"] = None
        self.FormItemDict["DefaultValue"] = None
        self.FormItemDict["WidgetName"] = None
        self.FormItemDict["SetValue"] = None
        self.FormItemDict["GetValue"] = None
        self.FormItemDict["GetString"] = None
        self.FormItemDict["UpdateValue"] = None
        self.FormItemDict["QueryRecord"] = None
        self.FormItemDict["ClearWidget"] = None
        self.FormItemDict["FilterCheck"] = None
        self.FormItemDict["Description"] = None
        self.FormItemDict["Database"] = None
        self.FormItemDict["DatabaseField"] = None
        self.FormItemDict["ViewOrder"] = None
        self.FormItemDict["Label"] = None
        self.FormItemDict["ReferenceSession"] = None
        self.FormItemDict["ReferenceTable"] = None
        self.FormItemDict["ReferenceField"] = None
        self.FormItemDict["JoinVariable"] = None

    def createFIDictFromTable(self):
        pass

    def createFIDictFromDatabase(self, record_id):
        qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroup).filter_by(id=record_id).first()
        self.init_FIDict()
        if qryRecord.RecordGroupID is not None: self.FormItemDict["RecordGroup"] = qryRecord.RecordGroupID
        if qryRecord.WidgetType is not None: self.FormItemDict["WidgetType"] = qryRecord.WidgetType
        if qryRecord.ItemName is not None: self.FormItemDict["ItemName"] = qryRecord.ItemName
        if qryRecord.DefaultValue is not None: self.FormItemDict["DefaultValue"] = qryRecord.DefaultValue
        if qryRecord.WidgetName is not None: self.FormItemDict["WidgetName"] = qryRecord.WidgetName
        if qryRecord.SetValue is not None: self.FormItemDict["SetValue"] = qryRecord.SetValue
        if qryRecord.GetValue is not None: self.FormItemDict["GetValue"] = qryRecord.GetValue
        if qryRecord.GetString is not None: self.FormItemDict["GetString"] = qryRecord.GetString
        if qryRecord.UpdateValue is not None: self.FormItemDict["UpdateValue"] = qryRecord.UpdateValue
        if qryRecord.QueryRecord is not None: self.FormItemDict["QueryRecord"] = qryRecord.QueryRecord
        if qryRecord.ClearWidget is not None: self.FormItemDict["ClearWidget"] = qryRecord.ClearWidget
        if qryRecord.FilterCheck is not None: self.FormItemDict["FilterCheck"] = qryRecord.FilterCheck
        if qryRecord.Description is not None: self.FormItemDict["Description"] = qryRecord.Description
        if qryRecord.Database is not None: self.FormItemDict["Database"] = qryRecord.Database
        if qryRecord.DatabaseField is not None: self.FormItemDict["DatabaseField"] = qryRecord.DatabaseValue
        if qryRecord.ViewOrder is not None: self.FormItemDict["ViewOrder"] = qryRecord.ViewOrder
        if qryRecord.Label is not None: self.FormItemDict["Label"] = qryRecord.Label
        if qryRecord.ReferenceSession is not None: self.FormItemDict["ReferenceSession"] = qryRecord.ReferenceSession
        if qryRecord.ReferenceTable is not None: self.FormItemDict["ReferenceTable"] = qryRecord.ReferenceTable
        if qryRecord.ReferenceField is not None: self.FormItemDict["ReferenceField"] = qryRecord.ReferenceField
        if qryRecord.JoinVariable is not None: self.FormItemDict["JoinVariable"] = qryRecord.JoinVariable


    def blockFISignals(self, Value):
        self.ui.cmbFIDataGroup.blockSignals(Value)
        self.ui.cmbFIWidgetType.blockSignals(Value)
        self.ui.txtFIItemName.blockSignals(Value)
        self.ui.txtFIDefaultValue.blockSignals(Value)
        self.ui.txtFIWidgetName.blockSignals(Value)
        self.ui.cmbFISetValue.blockSignals(Value)
        self.ui.cmbFIGetValue.blockSignals(Value)
        self.ui.txtFIGetString.blockSignals(Value)
        self.ui.cmbFIUpdateValue.blockSignals(Value)
        self.ui.txtFIQueryRecord.blockSignals(Value)
        self.ui.txtFIClearWidget.blockSignals(Value)
        self.ui.txtFIFilterCheck.blockSignals(Value)
        self.ui.txtFIDescription.blockSignals(Value)
        self.ui.cmbFITable.blockSignals(Value)
        self.ui.cmbFIField.blockSignals(Value)
        self.ui.txtFIViewOrder.blockSignals(Value)
        self.ui.txtFILabel.blockSignals(Value)
        self.ui.cmbFIRSession.blockSignals(Value)
        self.ui.cmbFIRTable.blockSignals(Value)
        self.ui.cmbFIRField.blockSignals(Value)
        self.ui.txtFIJoinVariable.blockSignals(Value)

    @QtCore.Slot(int)
    def on_cmbFIDataGroup_currentIndexChanged(self, value):
        if self.ui.chkFIDataGroup.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["RecordGroup"] = {"Record_id": self.ui.cmbFIDataGroup.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFIDataGroup.model().index(value, 1, None).data(),
                                              "Row": value}

                qryRecordGroup = self.instanceDict["ProgramBase"].session.query(RecordGroup).filter_by(id=self.ui.cmbFIDataGroup.model().index(value, 0, None).data()).first()
                if qryRecordGroup is not None:
                    queryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable).filter_by(Session=qryRecordGroup.SessionID).order_by(MasterTable.TableName)
                    self.ui.cmbFITable.setModel(QueryTableModel(queryRecord))
                    self.ui.cmbFITable.setModelColumn(1)

                    if qryRecordGroup.SessionID is not None:
                        for row in range(self.ui.cmbFISession.model().rowCount()):
                            if int(self.ui.cmbFISession.model().index(row, 0, None).data()) == int(qryRecordGroup.SessionID):
                                self.ui.cmbFISession.setCurrentIndex(row)
                                break

                        self.on_FITable_load(qryRecordGroup.SessionID)
                        if qryRecordGroup.TableID is not None:
                            for row in range(self.ui.cmbFITable.model().rowCount()):
                                if int(self.ui.cmbFITable.model().index(row, 0, None).data()) == int(qryRecordGroup.TableID):
                                    self.ui.cmbFITable.setCurrentIndex(row)
                                    break
                        else:
                            self.ui.cmbFITable.setCurrentIndex(-1)
                self.createsaveFormItem(record_id)


    @QtCore.Slot(int)
    def on_cmbFIWidgetType_currentIndexChanged(self, value):

        if self.ui.chkRGMasterTable.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.createsaveFormItem(record_id)
                self.FormItemDict["WidgetType"] = {"Record_id": self.ui.cmbFIWidgetType.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFIWidgetType.model().index(value, 1, None).data(),
                                              "Row": value}
                self.createsaveFormItem(record_id)

            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(Direction=2, WidgetID=self.ui.cmbFIWidgetType.model().index(value, 0, None).data())

            self.ui.cmbFIGetValue.setModel(QueryTableModel(qryRecord))
            self.ui.cmbFIGetValue.setModelColumn(1)

            qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                .order_by(WidgetDataHandling.Command).filter_by(Direction=3, WidgetID=self.ui.cmbFIWidgetType.model().index(value, 0, None).data())

            self.ui.cmbFIUpdateValue.setModel(QueryTableModel(qryRecord))
            self.ui.cmbFIUpdateValue.setModelColumn(1)

        self.updateFormNames()

    @QtCore.Slot(str)
    def on_txtFIItemName_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["ItemName"] = {"Value": value}
                self.updateFormNames()
                #self.createsaveFormItem(record_id)

    def updateFormNames(self):
        value = self.ui.txtFIItemName.text()
        rg_id = self.ui.cmbFIDataGroup.model().index(self.ui.cmbFIDataGroup.currentIndex(), 0, None).data()
        if rg_id is not None:
            queryDataGroup = self.instanceDict["ProgramBase"].session.query(RecordGroup).filter_by(id=int(rg_id)).first()
            Abbr = queryDataGroup.Abbreviation

            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                if self.ui.cmbFIWidgetType.model().index(self.ui.cmbFIWidgetType.currentIndex(), 0, None).data() is not None:
                    queryItemRecord = self.instanceDict["ProgramBase"].session.query(FormItemData).filter_by(id=record_id).first()

                    qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                        .order_by(WidgetDataHandling.Command).filter_by(id=queryItemRecord.SetValue).first()
                    qryRecord2 = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                        .order_by(WidgetDataHandling.Command).filter_by(id=queryItemRecord.GetValue).first()
                    qryRecord3 = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling.id, WidgetDataHandling.Command, WidgetDataHandling.Direction)\
                        .order_by(WidgetDataHandling.Command).filter_by(id=queryItemRecord.UpdateValue).first()

                    widgetName = Abbr + value.replace(" ", "")

                    self.FormItemDict["WidgetName"] = {"Value": widgetName}
                    self.ui.txtFIWidgetName.setText(widgetName)

                    if qryRecord is not None:
                        setString = "self.ui." + widgetName + "." + qryRecord.Command
                        self.FormItemDict["SetString"] = {"Value": setString}
                        self.ui.txtFISetString.setText(setString)

                        for row in range(self.ui.cmbFISetValue.model().rowCount()):
                            if int(self.ui.cmbFISetValue.model().index(row, 0, None).data()) == int(queryItemRecord.SetValue):
                                self.ui.cmbFISetValue.setCurrentIndex(row)
                                setString = "self.ui." + widgetName + "." + str(self.ui.cmbFISetValue.model().index(self.ui.cmbFISetValue.currentIndex(), 1, None).data())

                                self.FormItemDict["SetString"] = {"Record_id": self.ui.cmbFISetValue.model().index(self.ui.cmbFISetValue.currentIndex(), 0, None).data(),
                                                                  "Value": setString,
                                                                  "Row": row}
                                self.ui.txtFISetString.setText(setString)
                                newcommand = setString.replace("value", value)
                                self.ui.txtFIClearWidget.setText("self.ui." + self.ui.txtFIWidgetName.text() + "." + newcommand)
                                self.FormItemDict["ClearWidget"] = "self.ui." + self.ui.txtFIWidgetName.text() + "." + newcommand
                                break

                    if qryRecord2 is not None:
                        for row in range(self.ui.cmbFIGetValue.model().rowCount()):
                            if int(self.ui.cmbFIGetValue.model().index(row, 0, None).data()) == int(queryItemRecord.GetValue):
                                self.ui.cmbFIGetValue.setCurrentIndex(row)
                                getString = "self.ui." + widgetName + "." + str(self.ui.cmbFIGetValue.model().index(self.ui.cmbFIGetValue.currentIndex(), 1, None).data())

                                self.FormItemDict["GetString"] = {"Record_id": self.ui.cmbFIGetValue.model().index(self.ui.cmbFIGetValue.currentIndex(), 0, None).data(),
                                                                  "Value": getString,
                                                                  "Row": row}
                                self.ui.txtFIGetString.setText(getString)
                                break

                    if qryRecord3 is not None:
                        for row in range(self.ui.cmbFIUpdateValue.model().rowCount()):
                            if int(self.ui.cmbFIUpdateValue.model().index(row, 0, None).data()) == int(queryItemRecord.UpdateValue):
                                self.ui.cmbFIUpdateValue.setCurrentIndex(row)
                                getString = "self.ui." + widgetName + "." + str(self.ui.cmbFIUpdateValue.model().index(self.ui.cmbFIUpdateValue.currentIndex(), 1, None).data())

                                self.FormItemDict["GetString"] = {"Record_id": self.ui.cmbFIUpdateValue.model().index(self.ui.cmbFIUpdateValue.currentIndex(), 0, None).data(),
                                                                  "Value": getString,
                                                                  "Row": row}
                                self.ui.txtFIUpdateString.setText(getString)
                                break

                    self.FormItemDict["FilterCheck"] = {"Value": "chk" + Abbr + value + "_Filter"}
                    self.ui.txtFIFilterCheck.setText("chk" + Abbr + value + "_Filter")
                    self.ui.txtFILabel.setText("lbl" + Abbr + value + "_Filter")

                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIDefaultValue_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["DefaultValue"] = {"Value": value}

                qryRecord = self.instanceDict["ProgramBase"].session.query(FormItemData).filter_by(id=record_id).first()
                qryRecord2 = self.instanceDict["ProgramBase"].session.query(WidgetDataHandling).filter_by(Direction=1, WidgetID=qryRecord.WidgetType).first()
                if qryRecord.DefaultValue is not None:
                    newcommand = qryRecord2.Command.replace("value", value)
                    self.ui.txtFIClearWidget.setText("self.ui." + self.ui.txtFIWidgetName.text() + "." + newcommand)

                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIWidgetName_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["WidgetName"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(int)
    def on_cmbFISetValue_currentIndexChanged(self, value):
        if self.ui.chkRGMasterTable.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                setString = str(self.ui.cmbFISetValue.model().index(value, 1, None).data())
                self.FormItemDict["SetValue"] = {"Record_id": self.ui.cmbFISetValue.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFISetValue.model().index(value, 1, None).data(),
                                              "Row": value}

                self.ui.txtFISetString.setText(self.ui.txtFIWidgetName.text() + setString)
                self.createsaveFormItem(record_id)


    @QtCore.Slot(int)
    def on_cmbFIGetValue_currentIndexChanged(self, value):
        if self.ui.chkRGMasterTable.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                getString = str(self.ui.cmbFIGetValue.model().index(value, 1, None).data())
                self.FormItemDict["GetValue"] = {"Record_id": self.ui.cmbFIGetValue.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFIGetValue.model().index(value, 1, None).data(),
                                              "Row": value}

                self.ui.txtFIGetString.setText(self.ui.txtFIWidgetName.text() + getString)
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIGetString_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["GetString"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(int)
    def on_cmbFIUpdateValue_currentIndexChanged(self, value):
        if self.ui.chkRGMasterTable.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                updateString = str(self.ui.cmbFIUpdateValue.model().index(value, 1, None).data())
                self.FormItemDict["UpdateValue"] = {"Record_id": self.ui.cmbFIUpdateValue.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFIUpdateValue.model().index(value, 1, None).data(),
                                              "Row": value}
                self.ui.txtFIUpdateString.setText(self.ui.txtFIWidgetName.text() + updateString)
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIQueryRecord_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["QueryRecord"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIClearWidget_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["ClearWidget"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIFilterCheck_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["FilterCheck"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIDescription_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["Description"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(int)
    def on_cmbFISession_currentIndexChanged(self, value):
        session_id = self.ui.cmbFISession.model().index(value, 0).data()
        queryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable).filter_by(Session=session_id).order_by(MasterTable.TableName)
        self.ui.cmbFITable.setModel(QueryTableModel(queryRecord))
        self.ui.cmbFITable.setModelColumn(1)

    @QtCore.Slot(int)
    def on_cmbFITable_currentIndexChanged(self, value):
        table_id = self.ui.cmbFITable.model().index(value, 0, None).data()
        self.on_FIField_load(table_id)

    @QtCore.Slot(int)
    def on_cmbFIField_currentIndexChanged(self, value):
        if self.ui.chkFIDatabaseField.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["DatabaseField"] = {"Record_id": self.ui.cmbFIField.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFIField.model().index(value, 1, None).data(),
                                              "Row": value}

                queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation).filter_by(id=int(self.ui.cmbFIField.model().index(value, 0, None).data())).first()
                self.ui.txtFIDatabaseFieldType.setText(queryRecord.DataType_Value)
                self.createsaveFormItem(record_id)

    @QtCore.Slot(int)
    def on_cmbFIRSession_currentIndexChanged(self, value):
        session_id = self.ui.cmbFIRSession.model().index(value, 0, None).data()
        record_id = int(self.ui.txtFormItem_id.text())

        self.on_FIRTable_load(session_id)
        self.FormItemDict["ReferenceSession"] = {"Record_id": self.ui.cmbFIRSession.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFIRSession.model().index(value, 1, None).data(),
                                              "Row": value}
        self.createsaveFormItem(record_id)

    @QtCore.Slot(int)
    def on_cmbFIRTable_currentIndexChanged(self, value):
        table_id =  self.ui.cmbFIRTable.model().index(value, 0, None).data()
        record_id = int(self.ui.txtFormItem_id.text())

        self.on_FIRField_load(table_id)
        self.FormItemDict["ReferenceTable"] = {"Record_id": self.ui.cmbFIRTable.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFIRTable.model().index(value, 1, None).data(),
                                              "Row": value}
        self.createsaveFormItem(record_id)

    @QtCore.Slot(int)
    def on_cmbFIRField_currentIndexChanged(self, value):
        table_id = self.ui.cmbFIRField.model().index(value, 0, None).data()
        record_id = int(self.ui.txtFormItem_id.text())

        #self.on_FIRField_load(table_id)
        self.FormItemDict["ReferenceField"] = {"Record_id": self.ui.cmbFIRField.model().index(value, 0, None).data(),
                                               "Value": self.ui.cmbFIRField.model().index(value, 1, None).data(),
                                               "Row": value}
        self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIViewOrder_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["ViewOrder"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFILabel_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["Label"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIReferenceTable_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["ReferenceTable"] = {"Value": value}
                self.createsaveFormItem(record_id)

    @QtCore.Slot(str)
    def on_txtFIJoinVariable_textChanged(self, value):
        if self.ui.chkRGGroupName.isChecked():
            self.on_tblFormItems_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["JoinVariable"] = {"Value": value}
                self.createsaveFormItem(record_id)
    #endregion

    #region Form Functions
    def on_FFTable_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate.id, FormFunctionTemplate.FunctionName)
        self.ui.tblFormFunctions.setModel(QueryTableModel(qryRecord))
        self.ui.tblFormFunctions.setColumnWidth(0,0)

    def on_FFForm_load(self):
        self.ui.txtFFName.setText("")
        self.ui.txtFFPath.setText("")
        self.ui.lstFFVariables.setText("")
        self.ui.txtFFFunction.setText("")

    def on_tblFormFunction_clicked(self):
        self.init_WidgetForm()
        self.blockWSignals(True)
        data = {}
        data["row"] = self.ui.tblFormFunctions.selectionModel().currentIndex().row()
        data["column"] = self.ui.tblFormFunctions.selectionModel().currentIndex().column()
        data["column"] = self.ui.tblFormFunctions.selectionModel().currentIndex().column()
        data["Value"] = self.ui.tblFormFunctions.model().index(data["row"], data["column"], None).data()
        data["id"] = self.ui.tblFormFunctions.model().index(data["row"], 0, None).data()

        self.ui.txtFFID.setText(str(data["id"]))

        self.on_FIFormFunction_load(int(data["id"]))

    def on_cmdCreateNewFormFunction_clicked(self):
        pass

    def createsaveFormFunction(self, record_id=None):
        if record_id is None:
            self.instanceDict["ProgramBase"].session.begin()
            qryRecord = FormFunctionTemplate()
            self.instanceDict["ProgramBase"].session.add(qryRecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(id=record_id).first()
            self.instanceDict["ProgramBase"].session.begin()

            if self.FormFunctionDict["RecordGroup"] is not None: qryRecord.RecordGroupID = self.FormItemDict["RecordGroup"][
                "Record_id"]

    def initFFForm(self):
        pass

    def on_FIFormFunction_load(self, Record_id):
        pass

    def initFFDict(self):
        pass

    def createFFDictFromTable(self):
        pass

    def createFFDictFromDatabase(self):
        pass

    def blockFFSignals(self):
        pass
    #endregion


    #region Function Template

    def init_FunctionTemplate(self):
        self.on_FTTable_load()
        self.on_lstFTVariables_load()
        self.on_lstFTProcesses_load()
        self.ui.cmdFTSaveCode.setEnabled(True)
        self.on_VariableList_load()
        self.on_FunctionList_load()
        self.ui.lstFTVariables.clicked.connect(self.on_lstFTVariables_clicked)
        self.ui.lstFTProcesses.clicked.connect(self.on_lstFTProcesses_clicked)
        self.doc = self.ui.txtFunctionTemplateCode.document()
        self.cursor = QtGui.QTextCursor(self.doc)

        self.on_cmbFITRecordGroup_load()

    def on_FTTable_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate.id, FormFunctionTemplate.FunctionName, FormFunctionTemplate.DefaultOrder).filter_by(SubFunction=0)
        self.ui.tblFunctionTemplate.setModel(QueryTableModel(qryRecord))
        self.ui.tblFunctionTemplate.resizeColumnsToContents()
        self.ui.tblFunctionTemplate.setColumnWidth(0,0)

        self.ui.lstFormFunctions.setModel(QueryTableModel(qryRecord))
        self.ui.lstFormFunctions.setModelColumn(1)

    def on_VariableList_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(VariableList.id, VariableList.ItemName).order_by(VariableList.ItemName)
        self.ui.lstFTVariables.setModel(QueryTableModel(qryRecord))
        self.ui.lstFTVariables.setModelColumn(1)

    def on_FunctionList_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(FunctionList.id, FunctionList.ItemName)
        self.ui.lstFTProcesses.setModel(QueryTableModel(qryRecord))
        self.ui.lstFTProcesses.setModelColumn(1)

    def on_cmbFITRecordGroup_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(RecordGroup.id, RecordGroup.Title)
        self.ui.cmbFITRecordGroup.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFITRecordGroup.setModelColumn(1)

    def on_FTForm_load(self):
        self.ui.txtFTName.setText("")
        self.ui.txtFTPath.setText("")
        self.ui.lstFTVariables.setText("")
        self.ui.txtFTFunction.setText("")
        self.ui.txtFunctionTemplateCode.setText("")
        self.ui.chkSubFunction.setCheckState(0)
        self.FunctionTemplateCode = "Clean"

        # Setup the QTextEdit editor configuration
        self.ui.txtFunctionTemplateCode.setAutoFormatting(QtGui.QTextEdit.AutoAll)
        self.ui.txtFunctionTemplateCode.selectionChanged.connect(self.update_format)
        # Initialize default font size.
        font = QtGui.QFont('Arial', 12)
        self.ui.txtFunctionTemplateCode.setFont(font)
        # We need to repeat the size to init the current format.
        self.ui.txtFunctionTemplateCode.setFontPointSize(12)

        self.ui.cmdFTSaveCode.setEnabled(True)

    @QtCore.Slot()
    def on_tblFunctionTemplate_clicked(self):
        self.init_WidgetForm()
        self.blockWSignals(True)
        data = {}
        data["row"] = self.ui.tblFunctionTemplate.selectionModel().currentIndex().row()
        data["column"] = self.ui.tblFunctionTemplate.selectionModel().currentIndex().column()
        data["column"] = self.ui.tblFunctionTemplate.selectionModel().currentIndex().column()
        data["Value"] = self.ui.tblFunctionTemplate.model().index(data["row"], data["column"], None).data()
        data["id"] = self.ui.tblFunctionTemplate.model().index(data["row"], 0, None).data()

        self.ui.txtFTID.setText(str(data["id"]))

        self.on_FTForm_load(int(data["id"]))

        self.ui.cmdFTSaveCode.setEnabled(True)

    def on_cmdCreateNewFunctionTemplate_clicked(self):
        pass

    def createsaveFunctionTemplate(self, record_id=None):
        if record_id is None:
            self.instanceDict["ProgramBase"].session.begin()
            qryRecord = FormFunctionTemplate()
            self.instanceDict["ProgramBase"].session.add(qryRecord)
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

        else:
            qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(id=record_id).first()
            self.instanceDict["ProgramBase"].session.begin()

            if self.FunctionTemplateDict["RecordGroup"] is not None: qryRecord.RecordGroupID = self.FormItemDict["RecordGroup"][
                "Record_id"]

    def initFTForm(self):
        self.ui.txtFTName.setText("")
        self.ui.txtFTPath.setText("")
        self.ui.txtFTFilename.setText("")

    def on_FTForm_load(self, Record_id):
        self.initFTForm()
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(id=Record_id).first()

        if qryRecord.Filename is not None:
            self.ui.txtFTName.setText(qryRecord.FunctionName)
            self.ui.txtFTDescription.setText(qryRecord.Description)
            self.ui.txtFTPath.setText(qryRecord.FunctionPath)
            self.ui.txtFTFilename.setText(qryRecord.Filename)
            self.ui.chkSubFunction.setChecked(qryRecord.SubFunction)
            self.ui.spnFunctionOrder.setValue(qryRecord.DefaultOrder)
            f2 = open(os.path.join(qryRecord.FunctionPath, qryRecord.Filename), "r")
            self.ui.txtFunctionTemplateCode.setPlainText(f2.read())
            self.on_txtFunctionTemplateCode_2_load(Record_id)

    @QtCore.Slot(int)
    def on_spnFunctionOrder_valueChanged(self, value):
        print(value)

    @QtCore.Slot()
    def on_cmdFTSaveCode_clicked(self):
        filefullpath = self.ui.txtFTPath.text()
        fname = self.ui.txtFTFilename.text()
        filefullpath = os.path.join(filefullpath, fname)

        Record_id = self.ui.txtFTID.text()

        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(id=Record_id).first()

        if qryRecord.Filename is None:
            None
        else:
            self.instanceDict["ProgramBase"].session.begin()
            qryRecord.FunctionName = self.ui.txtFTName.text()
            qryRecord.Description = self.ui.txtFTDescription.text()
            qryRecord.FunctionPath = self.ui.txtFTPath.text()
            qryRecord.Filename = self.ui.txtFTFilename.text()
            qryRecord.SubFunction = self.ui.chkSubFunction.isChecked()
            qryRecord.DefaultOrder = self.ui.spnFunctionOrder.value()
            self.instanceDict["ProgramBase"].session.commit()
            self.instanceDict["ProgramBase"].session.flush()

            f2 = open(os.path.join(qryRecord.FunctionPath, qryRecord.Filename), "r")
            self.ui.txtFunctionTemplateCode.setPlainText(f2.read())

        with open(filefullpath, 'w') as f:
            f.write(self.ui.txtFunctionTemplateCode.toPlainText())

        self.on_txtFunctionTemplateCode_2_load(Record_id)

        self.FunctionTemplateCode = "Clean"
        self.ui.cmdFTSaveCode.setEnabled(True)


    @QtCore.Slot()
    def on_txtFunctionTemplateCode_textChanged(self):
        if not self.ui.chkFTAutoSaveCode.checkState():
            self.FunctionTemplateCode = "Dirty"
            self.ui.cmdFTSaveCode.setEnabled(True)
        else:
            self.on_cmdFTSaveCode_clicked()

    @QtCore.Slot()
    def on_cmdFTSaveCode_selectionChanged(self):
        print()

    def on_lstFTVariables_load(self):
        pass

    def on_lstFTProcesses_load(self):
        pass

    def initFTDict(self):
        self.FTDict = {}
        self.FTDict["FTName"] = ""
        self.FTDict["FTPath"] = ""
        self.FTDict["FTFilename"] = ""
        self.FTDict["txtFunctionTemplateCode"] = ""

    def createFTDictFromTable(self):
        pass

    def createFTDictFromDatabase(self):
        pass

    def blockFTSignals(self, Value):
        self.ui.txtFTName.blockSignals(Value)
        self.ui.txtFTPath.blockSignals(Value)
        self.ui.txtFTFilename.blockSignals(Value)
        self.ui.txtFunctionTemplateCode.blockSignals(Value)

    @QtCore.Slot()
    def on_lstFTVariables_clicked(self):

        newtext = str(self.ui.lstFTVariables.model().index(self.ui.lstFTVariables.currentIndex().row(), 1).data())
        self.ui.txtFunctionTemplateCode.textCursor().insertText("{" + newtext + "}")

    @QtCore.Slot()
    def on_lstFTProcesses_clicked(self):
        self.ui.txtFTDescription.setText(str(self.ui.lstFTProcesses.model().index(self.ui.lstFTProcesses.currentIndex().row(), 1).data()))

        newtext = str(self.ui.lstFTVariables.model().index(self.ui.lstFTVariables.currentIndex().row(), 1).data())
        self.ui.txtFunctionTemplateCode.textCursor().insertText("{" + newtext + "}")

    def on_txtFunctionTemplateCode_2_load(self, Record_id):

        rg_id = self.ui.cmbFITRecordGroup.model().index(self.ui.cmbFITRecordGroup.currentIndex(), 0).data()
        frm_id = self.ui.cmbFITRecordGroup.model().index(self.ui.cmbFITRecordGroup.currentIndex(), 0).data()

        self.createRGDictFromDatabase(rg_id)

        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(id=Record_id).first()
        qryFormRecord = self.instanceDict["ProgramBase"].session.query(FormItemData).filter_by(RecordGroupID=int(3)).all()

        if qryRecord.Filename is not None:
            self.ui.txtFTName.setText(qryRecord.FunctionName)
            self.ui.txtFTDescription.setText(qryRecord.Description)
            self.ui.txtFTPath.setText(qryRecord.FunctionPath)
            self.ui.txtFTFilename.setText(qryRecord.Filename)

            f = open(os.path.join(qryRecord.FunctionPath, qryRecord.Filename), "r")
            textbody = ""

            processdelay = False
            bufferlist = []
            ignore = False
            findcase = None

            for textline in f:
                if processdelay == False:
                    if "{BeginWidgetList}" in textline:
                        bufferdict = {}
                        bufferlist = []
                        processdelay = True
                    else:
                        #Process the Line Item
                        itemlist = set(re.findall('\{.*?\}', textline))
                        for item in itemlist:
                            if "RecordGroup." in item:
                                if item[13:-1] in self.RGDict:
                                    #print("found", item[13:-1], self.RGDict[item[13:-1]])
                                    itemdictname = self.RGDict[item[13:-1]]
                                    textline = textline.replace(item, itemdictname)
                                else:
                                    print("not found", self.RGDict)
                            else:
                                print(textline)
                        textbody += textline
                else:
                    if "{EndWidgetList}" in textline:

                        # Process the Block
                        #self.createFIDictFromDatabase(record.id)
                        for record in qryFormRecord:
                            FormRecordDict = record.__dict__
                            '''print(FormRecordDict)'''


                            for bufferitem in bufferlist:
                                itemlist = set(re.findall('\{.*?\}', bufferitem))
                                textline = bufferitem
                                for item in itemlist:
                                    if "SubFunction" in item:
                                        textline = ""
                                        FunctionName = re.search('\((.*)\[', bufferitem).group(0)
                                        RegionName = re.search('\[\{(.*)\}\]', bufferitem).group(0)

                                        if "RecordGroup.Form." in RegionName:
                                            if RegionName[19:-2] in FormRecordDict:
                                                itemdictname = FormRecordDict[RegionName[19:-2]]
                                                if RegionName[19:-2] == "WidgetType":
                                                    qryWidgetType = self.instanceDict["ProgramBase"].session.query(WidgetData).filter_by(id=int(itemdictname)).first()
                                                    RegionNameValue = qryWidgetType.Title

                                        sublist = self.SubFunction(FunctionName[1:-1], RegionNameValue)
                                        print(FormRecordDict["ItemName"], FunctionName[1:-1], RegionNameValue, bufferitem)
                                        for subitem in sublist:
                                            #print(subitem)
                                            textline = subitem
                                            itemlist2 = set(re.findall('\{.*?\}', subitem))
                                            for item2 in itemlist2:
                                                #print(item2)
                                                if "RecordGroup.Form." in item2:
                                                    if item2[18:-1] in FormRecordDict:
                                                        itemdictname = FormRecordDict[item2[18:-1]]
                                                        #print(item2)
                                                        if itemdictname is not None:
                                                            textline = textline.replace(item2, itemdictname)
                                                        else:
                                                            textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                            print("Item Not FoundS2", FormRecordDict, bufferitem, item, itemdictname)

                                                elif "RecordGroup." in item2:
                                                    if item2[13:-1] in self.RGDict:
                                                        itemdictname = self.RGDict[item2[13:-1]]

                                                        if itemdictname is not None:
                                                            textline = textline.replace(item2, itemdictname)
                                                        else:
                                                            textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                            print("Item Not FoundS2", FormRecordDict, bufferitem, item, itemdictname)

                                                    else:
                                                        print("not found", item)

                                            textbody += textline
                                        textline = ""
                                        textbody += "\n"

                                    elif "RecordGroup.Form." in item:
                                        if item[18:-1] in FormRecordDict:
                                            itemdictname = FormRecordDict[item[18:-1]]
                                            if itemdictname is not None:
                                                textline = textline.replace(item, str(itemdictname))
                                            else:
                                                textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                print("Item Not Found1", FormRecordDict, bufferitem, item, itemdictname)

                                    elif "RecordGroup." in item:
                                        #print("test", item[13:-1])
                                        if item[13:-1] in self.RGDict:
                                            #print("found", item[13:-1], self.RGDict[item[13:-1]])
                                            itemdictname = self.RGDict[item[13:-1]]
                                            if itemdictname is not None:
                                                textline = textline.replace(item, itemdictname)
                                            else:
                                                textline = textline.replace("}", "(" + FormRecordDict["ItemName"] + ")}")
                                                print("Item Not Found2", FormRecordDict, bufferitem, item, itemdictname)
                                        else:
                                            print("not found", item)

                                    elif "Select Case WidgetType" in item:
                                        pass

                            textbody += textline
                        bufferlist = []
                        processdelay = False
                    else:
                        #Build the Block
                        if "If WidgetType" in textline:
                            ignore = True
                            findcase = textline[len("{If WidgetType"):-1]
                            caselines = []

                        if ignore == False:
                            bufferlist.append(textline)
                        else:
                            if "End If" in textline:
                                #This only works with on position for choices
                                bufferdict[findcase] = caselines
                                ignore = False


            self.ui.txtFunctionTemplateCode_2.setPlainText(textbody)
        record_id = 2
        #self.createRGDictFromDatabase(record_id)
        '''
        self.RGDict
        id
        RecordGroup
        FormID
        Abbreviation
        SessionID
        TableID
        IDWidgetName
        IDWidgetType
        NewItemWidgetName
        NewItemWidgetType
        CreateDictFunction'''

    def init_FITTemplate(self):
        self.blockFITSignals(True)
        self.on_FITSession_load()
        self.on_FITTable_load()
        self.on_FITField_load()

        #self.on_FITDataGroup_load()
        self.on_FITWidgetType_load()

        self.blockFITSignals(False)

    def blockFITSignals(self, Value):
        self.ui.cmbFITSession.blockSignals(Value)
        self.ui.cmbFITTable.blockSignals(Value)
        self.ui.cmbFITField.blockSignals(Value)
        self.ui.cmbFITForm.blockSignals(Value)
        self.ui.cmbFITWidgetName.blockSignals(Value)
        self.ui.lstFITWidgetName.blockSignals(Value)
        self.ui.cmbFITWidgetType.blockSignals(Value)

    def on_FITSession_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(SessionNames.id, SessionNames.NameText)
        self.ui.cmbFITSession.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFITSession.setModelColumn(1)

    def on_FITTable_load(self, Session_id=None):
        self.blockFITSignals(True)
        if Session is None:
            qryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable.id, MasterTable.TableName)
            self.ui.cmbFITTable.setModel(QueryTableModel(qryRecord))
            self.ui.cmbFITTable.setModelColumn(1)
        else:
            queryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable.id, MasterTable.TableName).filter_by(Session=Session_id).order_by(MasterTable.TableName)
            self.ui.cmbFITTable.setModel(QueryTableModel(queryRecord))
            self.ui.cmbFITTable.setModelColumn(1)
        self.blockFITSignals(False)

    def on_FITField_load(self, Table_id=None):
        queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation.id, FieldInformation.FieldName).filter_by(TableID=Table_id).order_by(FieldInformation.FieldName)
        self.blockFITSignals(True)
        if queryRecord.first() is None:
            qryTable = self.instanceDict["ProgramBase"].session.query(MasterTable).filter_by(id=Table_id).first()

            if qryTable is not None:
                qryBase = self.instanceDict["ProgramBase"].session.query(SessionBase).filter_by(id=qryTable.Base).first()
                if qryBase is not None:
                    myColumnList = DatabaseTools.get_fields_by_tablename(bases[qryBase.NameText], qryTable.TableName)

                    for key, value in enumerate(myColumnList):
                        qryTableField = self.instanceDict["ProgramBase"].session.query(FieldInformation).filter_by(TableID=Table_id, FieldName=value).first()

                        if qryTableField is None:
                            self.instanceDict["ProgramBase"].session.begin()
                            qryTableField = FieldInformation(TableID=int(Table_id),
                                                             FieldName=str(value),
                                                             DataType_Value=str(myColumnList[value]))
                            self.instanceDict["ProgramBase"].session.add(qryTableField)
                            self.instanceDict["ProgramBase"].session.commit()
                            self.instanceDict["ProgramBase"].session.flush()

                        queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation.id, FieldInformation.FieldName).filter_by(
                            TableID=Table_id).order_by(FieldInformation.FieldName)
                        self.ui.cmbFITField.setModel(QueryTableModel(queryRecord))
                        self.ui.cmbFITField.setModelColumn(1)
        else:
            self.ui.cmbFITField.setModel(QueryTableModel(queryRecord))
            self.ui.cmbFITField.setModelColumn(1)

        self.blockFITSignals(False)

    def on_FITWidgetType_load(self):
        qryRecord = self.instanceDict["ProgramBase"].session.query(WidgetData.id, WidgetData.Title)
        self.ui.cmbFITWidgetType.setModel(QueryTableModel(qryRecord))
        self.ui.cmbFITWidgetType.setModelColumn(1)


    @QtCore.Slot(int)
    def on_cmbFITSession_currentIndexChanged(self, value):
        session_id = self.ui.cmbFITSession.model().index(value, 0).data()
        queryRecord = self.instanceDict["ProgramBase"].session.query(MasterTable).filter_by(Session=session_id).order_by(MasterTable.TableName)
        self.ui.cmbFITTable.setModel(QueryTableModel(queryRecord))
        self.ui.cmbFITTable.setModelColumn(1)

        self.ui.on_FITTable_load(session_id)

    @QtCore.Slot(int)
    def on_cmbFITTable_currentIndexChanged(self, value):
        table_id =  self.ui.cmbFITTable.model().index(value, 0, None).data()
        self.on_FITField_load(table_id)

    @QtCore.Slot(int)
    def on_cmbFITField_currentIndexChanged(self, value):
        if self.ui.chkFIDatabaseField.isChecked():
            self.on_FITTable_load()
        else:
            if self.ui.txtFormItem_id.text() != "":
                record_id = int(self.ui.txtFormItem_id.text())
                self.FormItemDict["DatabaseField"] = {"Record_id": self.ui.cmbFITField.model().index(value, 0, None).data(),
                                              "Value": self.ui.cmbFITField.model().index(value, 1, None).data(),
                                              "Row": value}

                queryRecord = self.instanceDict["ProgramBase"].session.query(FieldInformation).filter_by(id=int(self.ui.cmbFITField.model().index(value, 0, None).data())).first()
                self.ui.txtFITDatabaseFieldType.setText(queryRecord.DataType_Value)
                self.createsaveFormItem(record_id)


    #endregion

    def SubFunction(self, FunctionName, RegionName):
        filename = FunctionName + ".txt"
        qryRecord = self.instanceDict["ProgramBase"].session.query(FormFunctionTemplate).filter_by(Filename=filename).first()
        if qryRecord.Filename is not None:
            self.ui.txtFTName.setText(qryRecord.FunctionName)
            self.ui.txtFTDescription.setText(qryRecord.Description)
            self.ui.txtFTPath.setText(qryRecord.FunctionPath)
            self.ui.txtFTFilename.setText(qryRecord.Filename)

            f = open(os.path.join(qryRecord.FunctionPath, qryRecord.Filename), "r")
            RegionList = []
            InRegion = False
            for textline in f:
                if InRegion == False:
                    if "region " in textline and RegionName in textline:
                        InRegion = True
                else:
                    if "endregion" in textline:
                        break
                    else:
                        RegionList.append(textline)

            return(RegionList)

def main():
    app = QApplication(sys.argv)
    widget = FormBuilder()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
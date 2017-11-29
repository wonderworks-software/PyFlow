#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui

import classwizard_rc


class ClassWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(ClassWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(ClassInfoPage())
        self.addPage(CodeStylePage())
        self.addPage(OutputFilesPage())
        self.addPage(ConclusionPage())

        self.setPixmap(QtGui.QWizard.BannerPixmap,
                QtGui.QPixmap(':/images/banner.png'))
        self.setPixmap(QtGui.QWizard.BackgroundPixmap,
                QtGui.QPixmap(':/images/background.png'))

        self.setWindowTitle("Class Wizard")

    def accept(self):
        className = self.field('className')
        baseClass = self.field('baseClass')
        macroName = self.field('macroName')
        baseInclude = self.field('baseInclude')

        outputDir = self.field('outputDir')
        header = self.field('header')
        implementation = self.field('implementation')

        block = ''

        if self.field('comment'):
            block += '/*\n'
            block += '    ' + header + '\n'
            block += '*/\n'
            block += '\n'

        if self.field('protect'):
            block += '#ifndef ' + macroName + '\n'
            block += '#define ' + macroName + '\n'
            block += '\n'

        if self.field('includeBase'):
            block += '#include ' + baseInclude + '\n'
            block += '\n'

        block += 'class ' + className
        if baseClass:
            block += ' : public ' + baseClass

        block += '\n'
        block += '{\n'

        if self.field('qobjectMacro'):
            block += '    Q_OBJECT\n'
            block += '\n'

        block += 'public:\n'

        if self.field('qobjectCtor'):
            block += '    ' + className + '(QObject *parent = 0);\n'
        elif self.field('qwidgetCtor'):
            block += '    ' + className + '(QWidget *parent = 0);\n'
        elif self.field('defaultCtor'):
            block += '    ' + className + '();\n'

            if self.field('copyCtor'):
                block += '    ' + className + '(const ' + className + ' &other);\n'
                block += '\n'
                block += '    ' + className + ' &operator=' + '(const ' + className + ' &other);\n'

        block += '};\n'

        if self.field('protect'):
            block += '\n'
            block += '#endif\n'

        headerFile = QtCore.QFile(outputDir + '/' + header)

        if not headerFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(None, "Class Wizard",
                    "Cannot write file %s:\n%s" % (headerFile.fileName(), headerFile.errorString()))
            return

        headerFile.write(str(block))

        block = ''

        if self.field('comment'):
            block += '/*\n'
            block += '    ' + implementation + '\n'
            block += '*/\n'
            block += '\n'

        block += '#include "' + header + '"\n'
        block += '\n'

        if self.field('qobjectCtor'):
            block += className + '::' + className + '(QObject *parent)\n'
            block += '    : ' + baseClass + '(parent)\n'
            block += '{\n'
            block += '}\n'
        elif self.field('qwidgetCtor'):
            block += className + '::' + className + '(QWidget *parent)\n'
            block += '    : ' + baseClass + '(parent)\n'
            block += '{\n'
            block += '}\n'
        elif self.field('defaultCtor'):
            block += className + '::' + className + '()\n'
            block += '{\n'
            block += '    // missing code\n'
            block += '}\n'

            if self.field('copyCtor'):
                block += '\n'
                block += className + '::' + className + '(const ' + className + ' &other)\n'
                block += '{\n'
                block += '    *this = other;\n'
                block += '}\n'
                block += '\n'
                block += className + ' &' + className + '::operator=(const ' + className + ' &other)\n'
                block += '{\n'

                if baseClass:
                    block += '    ' + baseClass + '::operator=(other);\n'

                block += '    // missing code\n'
                block += '    return *this;\n'
                block += '}\n'

        implementationFile = QtCore.QFile(outputDir + '/' + implementation)

        if not implementationFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(None, "Class Wizard",
                    "Cannot write file %s:\n%s" % (implementationFile.fileName(), implementationFile.errorString()))
            return

        implementationFile.write(str(block))

        super(ClassWizard, self).accept()


class IntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                QtGui.QPixmap(':/images/watermark1.png'))

        label = QtGui.QLabel("This wizard will generate a skeleton C++ class "
                "definition, including a few functions. You simply need to "
                "specify the class name and set a few options to produce a "
                "header file and an implementation file for your new C++ "
                "class.")
        label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class ClassInfoPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(ClassInfoPage, self).__init__(parent)

        self.setTitle("Class Information")
        self.setSubTitle("Specify basic information about the class for "
                "which you want to generate skeleton source code files.")
        self.setPixmap(QtGui.QWizard.LogoPixmap,
                QtGui.QPixmap(':/images/logo1.png'))

        classNameLabel = QtGui.QLabel("&Class name:")
        classNameLineEdit = QtGui.QLineEdit()
        classNameLabel.setBuddy(classNameLineEdit)

        baseClassLabel = QtGui.QLabel("B&ase class:")
        baseClassLineEdit = QtGui.QLineEdit()
        baseClassLabel.setBuddy(baseClassLineEdit)

        qobjectMacroCheckBox = QtGui.QCheckBox("Generate Q_OBJECT &macro")

        groupBox = QtGui.QGroupBox("C&onstructor")

        qobjectCtorRadioButton = QtGui.QRadioButton("&QObject-style constructor")
        qwidgetCtorRadioButton = QtGui.QRadioButton("Q&Widget-style constructor")
        defaultCtorRadioButton = QtGui.QRadioButton("&Default constructor")
        copyCtorCheckBox = QtGui.QCheckBox("&Generate copy constructor and operator=")

        defaultCtorRadioButton.setChecked(True)

        defaultCtorRadioButton.toggled.connect(copyCtorCheckBox.setEnabled)

        self.registerField('className*', classNameLineEdit)
        self.registerField('baseClass', baseClassLineEdit)
        self.registerField('qobjectMacro', qobjectMacroCheckBox)
        self.registerField('qobjectCtor', qobjectCtorRadioButton)
        self.registerField('qwidgetCtor', qwidgetCtorRadioButton)
        self.registerField('defaultCtor', defaultCtorRadioButton)
        self.registerField('copyCtor', copyCtorCheckBox)

        groupBoxLayout = QtGui.QVBoxLayout()
        groupBoxLayout.addWidget(qobjectCtorRadioButton)
        groupBoxLayout.addWidget(qwidgetCtorRadioButton)
        groupBoxLayout.addWidget(defaultCtorRadioButton)
        groupBoxLayout.addWidget(copyCtorCheckBox)
        groupBox.setLayout(groupBoxLayout)

        layout = QtGui.QGridLayout()
        layout.addWidget(classNameLabel, 0, 0)
        layout.addWidget(classNameLineEdit, 0, 1)
        layout.addWidget(baseClassLabel, 1, 0)
        layout.addWidget(baseClassLineEdit, 1, 1)
        layout.addWidget(qobjectMacroCheckBox, 2, 0, 1, 2)
        layout.addWidget(groupBox, 3, 0, 1, 2)
        self.setLayout(layout)


class CodeStylePage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(CodeStylePage, self).__init__(parent)

        self.setTitle("Code Style Options")
        self.setSubTitle("Choose the formatting of the generated code.")
        self.setPixmap(QtGui.QWizard.LogoPixmap,
                QtGui.QPixmap(':/images/logo2.png'))

        commentCheckBox = QtGui.QCheckBox("&Start generated files with a "
                "comment")
        commentCheckBox.setChecked(True)

        protectCheckBox = QtGui.QCheckBox("&Protect header file against "
                "multiple inclusions")
        protectCheckBox.setChecked(True)

        macroNameLabel = QtGui.QLabel("&Macro name:")
        self.macroNameLineEdit = QtGui.QLineEdit()
        macroNameLabel.setBuddy(self.macroNameLineEdit)

        self.includeBaseCheckBox = QtGui.QCheckBox("&Include base class "
                "definition")
        self.baseIncludeLabel = QtGui.QLabel("Base class include:")
        self.baseIncludeLineEdit = QtGui.QLineEdit()
        self.baseIncludeLabel.setBuddy(self.baseIncludeLineEdit)

        protectCheckBox.toggled.connect(macroNameLabel.setEnabled)
        protectCheckBox.toggled.connect(self.macroNameLineEdit.setEnabled)
        self.includeBaseCheckBox.toggled.connect(self.baseIncludeLabel.setEnabled)
        self.includeBaseCheckBox.toggled.connect(self.baseIncludeLineEdit.setEnabled)

        self.registerField('comment', commentCheckBox)
        self.registerField('protect', protectCheckBox)
        self.registerField('macroName', self.macroNameLineEdit)
        self.registerField('includeBase', self.includeBaseCheckBox)
        self.registerField('baseInclude', self.baseIncludeLineEdit)

        layout = QtGui.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(commentCheckBox, 0, 0, 1, 3)
        layout.addWidget(protectCheckBox, 1, 0, 1, 3)
        layout.addWidget(macroNameLabel, 2, 1)
        layout.addWidget(self.macroNameLineEdit, 2, 2)
        layout.addWidget(self.includeBaseCheckBox, 3, 0, 1, 3)
        layout.addWidget(self.baseIncludeLabel, 4, 1)
        layout.addWidget(self.baseIncludeLineEdit, 4, 2)
        self.setLayout(layout)

    def initializePage(self):
        className = self.field('className')
        self.macroNameLineEdit.setText(className.upper() + "_H")

        baseClass = self.field('baseClass')
        is_baseClass = bool(baseClass)

        self.includeBaseCheckBox.setChecked(is_baseClass)
        self.includeBaseCheckBox.setEnabled(is_baseClass)
        self.baseIncludeLabel.setEnabled(is_baseClass)
        self.baseIncludeLineEdit.setEnabled(is_baseClass)

        if not is_baseClass:
            self.baseIncludeLineEdit.clear()
        elif QtCore.QRegExp('Q[A-Z].*').exactMatch(baseClass):
            self.baseIncludeLineEdit.setText('<' + baseClass + '>')
        else:
            self.baseIncludeLineEdit.setText('"' + baseClass.lower() + '.h"')


class OutputFilesPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(OutputFilesPage, self).__init__(parent)

        self.setTitle("Output Files")
        self.setSubTitle("Specify where you want the wizard to put the "
                "generated skeleton code.")
        self.setPixmap(QtGui.QWizard.LogoPixmap,
                QtGui.QPixmap(':/images/logo3.png'))

        outputDirLabel = QtGui.QLabel("&Output directory:")
        self.outputDirLineEdit = QtGui.QLineEdit()
        outputDirLabel.setBuddy(self.outputDirLineEdit)

        headerLabel = QtGui.QLabel("&Header file name:")
        self.headerLineEdit = QtGui.QLineEdit()
        headerLabel.setBuddy(self.headerLineEdit)

        implementationLabel = QtGui.QLabel("&Implementation file name:")
        self.implementationLineEdit = QtGui.QLineEdit()
        implementationLabel.setBuddy(self.implementationLineEdit)

        self.registerField('outputDir*', self.outputDirLineEdit)
        self.registerField('header*', self.headerLineEdit)
        self.registerField('implementation*', self.implementationLineEdit)

        layout = QtGui.QGridLayout()
        layout.addWidget(outputDirLabel, 0, 0)
        layout.addWidget(self.outputDirLineEdit, 0, 1)
        layout.addWidget(headerLabel, 1, 0)
        layout.addWidget(self.headerLineEdit, 1, 1)
        layout.addWidget(implementationLabel, 2, 0)
        layout.addWidget(self.implementationLineEdit, 2, 1)
        self.setLayout(layout)

    def initializePage(self):
        className = self.field('className')
        self.headerLineEdit.setText(className.lower() + '.h')
        self.implementationLineEdit.setText(className.lower() + '.cpp')
        self.outputDirLineEdit.setText(QtCore.QDir.convertSeparators(QtCore.QDir.tempPath()))


class ConclusionPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("Conclusion")
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                QtGui.QPixmap(':/images/watermark2.png'))

        self.label = QtGui.QLabel()
        self.label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QtGui.QWizard.FinishButton)
        finishText.replace('&', '')
        self.label.setText("Click %s to generate the class skeleton." % finishText)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = ClassWizard()
    wizard.show()
    sys.exit(app.exec_())

/*
 * This file is part of PySide: Python for Qt
 *
 * Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * version 2.1 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 * 02110-1301 USA
 *
 */



#ifndef SBK_QTGUI_PYTHON_H
#define SBK_QTGUI_PYTHON_H

#include <sbkpython.h>
#include <conversions.h>
#include <sbkenum.h>
#include <basewrapper.h>
#include <bindingmanager.h>
#include <memory>

#include <pysidesignal.h>
// Module Includes
#include <pyside_qtcore_python.h>

// Binded library includes
#include <qwhatsthis.h>
#include <qtransform.h>
#include <qtextobject.h>
#include <qquaternion.h>
#include <qpen.h>
#include <qcleanlooksstyle.h>
#include <qabstractprintdialog.h>
#include <qpolygon.h>
#include <qcolordialog.h>
#include <qsortfilterproxymodel.h>
#include <qcursor.h>
#include <qtextcursor.h>
#include <qprintpreviewdialog.h>
#include <qevent.h>
#include <qlabel.h>
#include <qinputdialog.h>
#include <qsizegrip.h>
#include <qabstractbutton.h>
#include <qtabbar.h>
#include <qradiobutton.h>
#include <qtoolbar.h>
#include <qtreewidget.h>
#include <qwizard.h>
#include <qiconengine.h>
#include <QTextEdit>
#include <qundoview.h>
#include <qplastiquestyle.h>
#include <qboxlayout.h>
#include <qfont.h>
#include <qundogroup.h>
#include <qgraphicsanchorlayout.h>
#include <qpushbutton.h>
#include <qgraphicsitemanimation.h>
#include <qsplashscreen.h>
#include <qgesturerecognizer.h>
#include <qpixmap.h>
#include <qprinterinfo.h>
#include <qprogressbar.h>
#include <qpainterpath.h>
#include <qtoolbox.h>
#include <qlcdnumber.h>
#include <QPainter>
#include <qprogressdialog.h>
#include <qabstractscrollarea.h>
#include <qabstractspinbox.h>
#include <qgraphicsscene.h>
#include <qtextbrowser.h>
#include <qfileiconprovider.h>
#include <qlistwidget.h>
#include <qundostack.h>
#include <qworkspace.h>
#include <qicon.h>
#include <qdirmodel.h>
#include <qformlayout.h>
#include <QAbstractTextDocumentLayout>
#include <qitemselectionmodel.h>
#include <qtextdocumentfragment.h>
#include <qclipboard.h>
#include <qgroupbox.h>
#include <qinputcontextfactory.h>
#include <qregion.h>
#include <qcolumnview.h>
#include <qwidget.h>
#include <qgraphicsproxywidget.h>
#include <qabstractslider.h>
#include <qtextformat.h>
#include <qitemdelegate.h>
#include <qkeyeventtransition.h>
#include <qgenericmatrix.h>
#include <qpalette.h>
#include <qpixmapcache.h>
#include <qfontdatabase.h>
#include <qtextlist.h>
#include <qmdisubwindow.h>
#include <qvector4d.h>
#include <qgraphicswidget.h>
#include <qgraphicstransform.h>
#include <qsound.h>
#include <qwidgetaction.h>
#include <qbuttongroup.h>
#include <qfocusframe.h>
#include <qstyleditemdelegate.h>
#include <qerrormessage.h>
#include <qstringlistmodel.h>
#include <qplaintextedit.h>
#include <qdockwidget.h>
#include <qproxymodel.h>
#include <qtabwidget.h>
#include <qabstractitemview.h>
#include <qspinbox.h>
#include <qcalendarwidget.h>
#include <qmatrix4x4.h>
#include <qprintdialog.h>
#include <qitemeditorfactory.h>
#include <qrubberband.h>
#include <qdatawidgetmapper.h>
#include <qabstracttextdocumentlayout.h>
#include <qaction.h>
#include <qpytextobject.h>
#include <qvector2d.h>
#include <qimagewriter.h>
#include <qmenu.h>
#include <qtextoption.h>
#include <qmouseeventtransition.h>
#include <qtextedit.h>
#include <qinputcontext.h>
#include <qfontinfo.h>
#include <qfontmetrics.h>
#include <qtextlayout.h>
#include <qwindowsstyle.h>
#include <qvector3d.h>
#include <qlistview.h>
#include <qsyntaxhighlighter.h>
#include <qtextdocument.h>
#include <qcolor.h>
#include <qgraphicsview.h>
#include <qpaintdevice.h>
#include <qfiledialog.h>
#include <qtablewidget.h>
#include <qfilesystemmodel.h>
#include <qgraphicseffect.h>
#include <qapplication.h>
#include <qtreeview.h>
#include <qlineedit.h>
#include <qtooltip.h>
#include <qtableview.h>
#include <qimage.h>
#include <qbrush.h>
#include <qstyleoption.h>
#include <qgraphicslayoutitem.h>
#include <QPainterPath>
#include <qaccessible.h>
#include <qtoolbutton.h>
#include <qcombobox.h>
#include <qbitmap.h>
#include <QTextBlock>
#include <qpaintengine.h>
#include <qcommonstyle.h>
#include <qkeysequence.h>
#include <qstylepainter.h>
#include <qstylefactory.h>
#include <qtreewidgetitemiterator.h>
#include <qmovie.h>
#include <qimageiohandler.h>
#include <qdialogbuttonbox.h>
#include <qmotifstyle.h>
#include <qstackedwidget.h>
#include <qcheckbox.h>
#include <qstandarditemmodel.h>
#include <qabstractitemdelegate.h>
#include <qdesktopwidget.h>
#include <qgraphicssceneevent.h>
#include <qstackedlayout.h>
#include <qlayoutitem.h>
#include <QTextLayout>
#include <qmessagebox.h>
#include <qpicture.h>
#include <qdialog.h>
#include <qcommandlinkbutton.h>
#include <qfontdialog.h>
#include <qmdiarea.h>
#include <qslider.h>
#include <qcompleter.h>
#include <qprintengine.h>
#include <qlayout.h>
#include <qdial.h>
#include <qdrawutil.h>
#include <qstyle.h>
#include <qtexttable.h>
#include <qvalidator.h>
#include <qpainter.h>
#include <QTextFrame>
#include <qgraphicslayout.h>
#include <qheaderview.h>
#include <qgraphicslinearlayout.h>
#include <qstatusbar.h>
#include <qmatrix.h>
#include <qfontcombobox.h>
#include <qdrag.h>
#include <qdatetimeedit.h>
#include <qscrollarea.h>
#include <qscrollbar.h>
#include <qsystemtrayicon.h>
#include <qshortcut.h>
#include <qgraphicsitem.h>
#include <qsessionmanager.h>
#include <qabstractproxymodel.h>
#include <qdesktopservices.h>
#include <qprintpreviewwidget.h>
#include <qgridlayout.h>
#include <qsplitter.h>
#include <qframe.h>
#include <QInputMethodEvent>
#include <qactiongroup.h>
#include <qpagesetupdialog.h>
#include <qgesture.h>
#include <qimagereader.h>
#include <qprinter.h>
#include <qmenubar.h>
#include <qsizepolicy.h>
#include <qcdestyle.h>
#include <qgraphicsgridlayout.h>
#include <qabstractpagesetupdialog.h>
#include <qmainwindow.h>
// Conversion Includes - Primitive Types
#include <QStringList>
#include <qabstractitemmodel.h>
#include <QString>
#include <signalmanager.h>
#include <typeresolver.h>
#include <QtConcurrentFilter>

// Conversion Includes - Container Types
#include <QMap>
#include <QStack>
#include <QLinkedList>
#include <QVector>
#include <QSet>
#include <QPair>
#include <pysideconversions.h>
#include <QQueue>
#include <QList>
#include <QMultiMap>

// Type indices
#define SBK_QMATRIX4X3_IDX                                           329
#define SBK_QMATRIX4X2_IDX                                           328
#define SBK_QMATRIX3X4_IDX                                           327
#define SBK_QMATRIX3X3_IDX                                           326
#define SBK_QMATRIX3X2_IDX                                           325
#define SBK_QMATRIX2X4_IDX                                           324
#define SBK_QMATRIX2X3_IDX                                           323
#define SBK_QMATRIX2X2_IDX                                           322
#define SBK_QPIXMAPCACHE_IDX                                         381
#define SBK_QPIXMAPCACHE_KEY_IDX                                     382
#define SBK_QPICTUREIO_IDX                                           376
#define SBK_QIMAGEIOHANDLER_IDX                                      270
#define SBK_QIMAGEIOHANDLER_IMAGEOPTION_IDX                          271
#define SBK_QICONENGINE_IDX                                          264
#define SBK_QTEXTTABLECELL_IDX                                       673
#define SBK_QTEXTFRAGMENT_IDX                                        644
#define SBK_QTEXTDOCUMENTFRAGMENT_IDX                                634
#define SBK_QTEXTBLOCK_IDX                                           616
#define SBK_QTEXTBLOCK_ITERATOR_IDX                                  617
#define SBK_QTEXTBLOCKUSERDATA_IDX                                   620
#define SBK_QSTYLEFACTORY_IDX                                        466
#define SBK_QVECTOR3D_IDX                                            704
#define SBK_QUNDOCOMMAND_IDX                                         696
#define SBK_QDESKTOPSERVICES_IDX                                     79
#define SBK_QDESKTOPSERVICES_STANDARDLOCATION_IDX                    80
#define SBK_QPRINTENGINE_IDX                                         390
#define SBK_QPRINTENGINE_PRINTENGINEPROPERTYKEY_IDX                  391
#define SBK_QPRINTERINFO_IDX                                         408
#define SBK_QPAINTENGINE_IDX                                         354
#define SBK_QPAINTENGINE_PAINTENGINEFEATURE_IDX                      356
#define SBK_QFLAGS_QPAINTENGINE_PAINTENGINEFEATURE__IDX              137
#define SBK_QPAINTENGINE_DIRTYFLAG_IDX                               355
#define SBK_QFLAGS_QPAINTENGINE_DIRTYFLAG__IDX                       136
#define SBK_QPAINTENGINE_POLYGONDRAWMODE_IDX                         357
#define SBK_QPAINTENGINE_TYPE_IDX                                    358
#define SBK_QPAINTENGINESTATE_IDX                                    359
#define SBK_QTEXTITEM_IDX                                            652
#define SBK_QTEXTITEM_RENDERFLAG_IDX                                 653
#define SBK_QFLAGS_QTEXTITEM_RENDERFLAG__IDX                         153
#define SBK_QTILERULES_IDX                                           676
#define SBK_QVECTOR2D_IDX                                            703
#define SBK_QMATRIX4X4_IDX                                           330
#define SBK_QQUATERNION_IDX                                          415
#define SBK_QVECTOR4D_IDX                                            705
#define SBK_QTEXTLINE_IDX                                            659
#define SBK_QTEXTLINE_EDGE_IDX                                       661
#define SBK_QTEXTLINE_CURSORPOSITION_IDX                             660
#define SBK_QTEXTOBJECTINTERFACE_IDX                                 666
#define SBK_QTEXTINLINEOBJECT_IDX                                    651
#define SBK_QTEXTCURSOR_IDX                                          625
#define SBK_QTEXTCURSOR_MOVEMODE_IDX                                 626
#define SBK_QTEXTCURSOR_MOVEOPERATION_IDX                            627
#define SBK_QTEXTCURSOR_SELECTIONTYPE_IDX                            628
#define SBK_QITEMSELECTION_IDX                                       290
#define SBK_QLIST_QITEMSELECTIONRANGE_IDX                            290
#define SBK_QTREEWIDGETITEM_IDX                                      691
#define SBK_QTREEWIDGETITEM_ITEMTYPE_IDX                             693
#define SBK_QTREEWIDGETITEM_CHILDINDICATORPOLICY_IDX                 692
#define SBK_QTREEWIDGETITEMITERATOR_IDX                              694
#define SBK_QTREEWIDGETITEMITERATOR_ITERATORFLAG_IDX                 695
#define SBK_QFLAGS_QTREEWIDGETITEMITERATOR_ITERATORFLAG__IDX         155
#define SBK_QFILEICONPROVIDER_IDX                                    108
#define SBK_QFILEICONPROVIDER_ICONTYPE_IDX                           109
#define SBK_QTABLEWIDGETITEM_IDX                                     608
#define SBK_QTABLEWIDGETITEM_ITEMTYPE_IDX                            609
#define SBK_QTABLEWIDGETSELECTIONRANGE_IDX                           610
#define SBK_QITEMEDITORFACTORY_IDX                                   289
#define SBK_QITEMSELECTIONRANGE_IDX                                  293
#define SBK_QSTANDARDITEM_IDX                                        448
#define SBK_QSTANDARDITEM_ITEMTYPE_IDX                               449
#define SBK_QLISTWIDGETITEM_IDX                                      317
#define SBK_QLISTWIDGETITEM_ITEMTYPE_IDX                             318
#define SBK_QITEMEDITORCREATORBASE_IDX                               288
#define SBK_QTEXTFORMAT_IDX                                          639
#define SBK_QTEXTFORMAT_FORMATTYPE_IDX                               640
#define SBK_QTEXTFORMAT_PROPERTY_IDX                                 643
#define SBK_QTEXTFORMAT_OBJECTTYPES_IDX                              641
#define SBK_QTEXTFORMAT_PAGEBREAKFLAG_IDX                            642
#define SBK_QFLAGS_QTEXTFORMAT_PAGEBREAKFLAG__IDX                    152
#define SBK_QTEXTFRAMEFORMAT_IDX                                     647
#define SBK_QTEXTFRAMEFORMAT_POSITION_IDX                            649
#define SBK_QTEXTFRAMEFORMAT_BORDERSTYLE_IDX                         648
#define SBK_QTEXTTABLEFORMAT_IDX                                     675
#define SBK_QTEXTLISTFORMAT_IDX                                      663
#define SBK_QTEXTLISTFORMAT_STYLE_IDX                                664
#define SBK_QTEXTBLOCKFORMAT_IDX                                     618
#define SBK_QTEXTBLOCKFORMAT_LINEHEIGHTTYPES_IDX                     724
#define SBK_QTEXTLENGTH_IDX                                          657
#define SBK_QTEXTLENGTH_TYPE_IDX                                     658
#define SBK_QTEXTOPTION_IDX                                          667
#define SBK_QTEXTOPTION_TABTYPE_IDX                                  670
#define SBK_QTEXTOPTION_WRAPMODE_IDX                                 671
#define SBK_QTEXTOPTION_FLAG_IDX                                     668
#define SBK_QFLAGS_QTEXTOPTION_FLAG__IDX                             154
#define SBK_QTEXTOPTION_TAB_IDX                                      669
#define SBK_QPEN_IDX                                                 374
#define SBK_QFONTDATABASE_IDX                                        170
#define SBK_QFONTDATABASE_WRITINGSYSTEM_IDX                          171
#define SBK_QSTYLEOPTION_IDX                                         477
#define SBK_QSTYLEOPTION_OPTIONTYPE_IDX                              478
#define SBK_QSTYLEOPTION_STYLEOPTIONTYPE_IDX                         479
#define SBK_QSTYLEOPTION_STYLEOPTIONVERSION_IDX                      480
#define SBK_QSTYLEOPTIONVIEWITEM_IDX                                 579
#define SBK_QSTYLEOPTIONVIEWITEM_STYLEOPTIONTYPE_IDX                 581
#define SBK_QSTYLEOPTIONVIEWITEM_STYLEOPTIONVERSION_IDX              582
#define SBK_QSTYLEOPTIONVIEWITEM_POSITION_IDX                        580
#define SBK_QSTYLEOPTIONVIEWITEMV2_IDX                               583
#define SBK_QSTYLEOPTIONVIEWITEMV2_STYLEOPTIONVERSION_IDX            584
#define SBK_QSTYLEOPTIONVIEWITEMV2_VIEWITEMFEATURE_IDX               585
#define SBK_QFLAGS_QSTYLEOPTIONVIEWITEMV2_VIEWITEMFEATURE__IDX       149
#define SBK_QSTYLEOPTIONVIEWITEMV3_IDX                               586
#define SBK_QSTYLEOPTIONVIEWITEMV3_STYLEOPTIONVERSION_IDX            587
#define SBK_QSTYLEOPTIONTOOLBAR_IDX                                  563
#define SBK_QSTYLEOPTIONTOOLBAR_STYLEOPTIONTYPE_IDX                  564
#define SBK_QSTYLEOPTIONTOOLBAR_STYLEOPTIONVERSION_IDX               565
#define SBK_QSTYLEOPTIONTOOLBAR_TOOLBARPOSITION_IDX                  567
#define SBK_QSTYLEOPTIONTOOLBAR_TOOLBARFEATURE_IDX                   566
#define SBK_QFLAGS_QSTYLEOPTIONTOOLBAR_TOOLBARFEATURE__IDX           147
#define SBK_QSTYLEOPTIONTAB_IDX                                      542
#define SBK_QSTYLEOPTIONTAB_STYLEOPTIONTYPE_IDX                      545
#define SBK_QSTYLEOPTIONTAB_STYLEOPTIONVERSION_IDX                   546
#define SBK_QSTYLEOPTIONTAB_TABPOSITION_IDX                          547
#define SBK_QSTYLEOPTIONTAB_SELECTEDPOSITION_IDX                     544
#define SBK_QSTYLEOPTIONTAB_CORNERWIDGET_IDX                         543
#define SBK_QFLAGS_QSTYLEOPTIONTAB_CORNERWIDGET__IDX                 146
#define SBK_QSTYLEOPTIONFRAME_IDX                                    499
#define SBK_QSTYLEOPTIONFRAME_STYLEOPTIONTYPE_IDX                    500
#define SBK_QSTYLEOPTIONFRAME_STYLEOPTIONVERSION_IDX                 501
#define SBK_QSTYLEOPTIONBUTTON_IDX                                   481
#define SBK_QSTYLEOPTIONBUTTON_STYLEOPTIONTYPE_IDX                   483
#define SBK_QSTYLEOPTIONBUTTON_STYLEOPTIONVERSION_IDX                484
#define SBK_QSTYLEOPTIONBUTTON_BUTTONFEATURE_IDX                     482
#define SBK_QFLAGS_QSTYLEOPTIONBUTTON_BUTTONFEATURE__IDX             144
#define SBK_QSTYLEOPTIONTABBARBASE_IDX                               548
#define SBK_QSTYLEOPTIONTABBARBASE_STYLEOPTIONTYPE_IDX               549
#define SBK_QSTYLEOPTIONTABBARBASE_STYLEOPTIONVERSION_IDX            550
#define SBK_QSTYLEOPTIONTABBARBASEV2_IDX                             551
#define SBK_QSTYLEOPTIONTABBARBASEV2_STYLEOPTIONVERSION_IDX          552
#define SBK_QSTYLEOPTIONCOMPLEX_IDX                                  488
#define SBK_QSTYLEOPTIONCOMPLEX_STYLEOPTIONTYPE_IDX                  489
#define SBK_QSTYLEOPTIONCOMPLEX_STYLEOPTIONVERSION_IDX               490
#define SBK_QSTYLEOPTIONTOOLBUTTON_IDX                               575
#define SBK_QSTYLEOPTIONTOOLBUTTON_STYLEOPTIONTYPE_IDX               576
#define SBK_QSTYLEOPTIONTOOLBUTTON_STYLEOPTIONVERSION_IDX            577
#define SBK_QSTYLEOPTIONTOOLBUTTON_TOOLBUTTONFEATURE_IDX             578
#define SBK_QFLAGS_QSTYLEOPTIONTOOLBUTTON_TOOLBUTTONFEATURE__IDX     148
#define SBK_QSTYLEOPTIONSLIDER_IDX                                   536
#define SBK_QSTYLEOPTIONSLIDER_STYLEOPTIONTYPE_IDX                   537
#define SBK_QSTYLEOPTIONSLIDER_STYLEOPTIONVERSION_IDX                538
#define SBK_QSTYLEOPTIONSIZEGRIP_IDX                                 533
#define SBK_QSTYLEOPTIONSIZEGRIP_STYLEOPTIONTYPE_IDX                 534
#define SBK_QSTYLEOPTIONSIZEGRIP_STYLEOPTIONVERSION_IDX              535
#define SBK_QSTYLEOPTIONGROUPBOX_IDX                                 510
#define SBK_QSTYLEOPTIONGROUPBOX_STYLEOPTIONTYPE_IDX                 511
#define SBK_QSTYLEOPTIONGROUPBOX_STYLEOPTIONVERSION_IDX              512
#define SBK_QSTYLEOPTIONTITLEBAR_IDX                                 560
#define SBK_QSTYLEOPTIONTITLEBAR_STYLEOPTIONTYPE_IDX                 561
#define SBK_QSTYLEOPTIONTITLEBAR_STYLEOPTIONVERSION_IDX              562
#define SBK_QSTYLEOPTIONCOMBOBOX_IDX                                 485
#define SBK_QSTYLEOPTIONCOMBOBOX_STYLEOPTIONTYPE_IDX                 486
#define SBK_QSTYLEOPTIONCOMBOBOX_STYLEOPTIONVERSION_IDX              487
#define SBK_QSTYLEOPTIONMENUITEM_IDX                                 519
#define SBK_QSTYLEOPTIONMENUITEM_STYLEOPTIONTYPE_IDX                 522
#define SBK_QSTYLEOPTIONMENUITEM_STYLEOPTIONVERSION_IDX              523
#define SBK_QSTYLEOPTIONMENUITEM_MENUITEMTYPE_IDX                    521
#define SBK_QSTYLEOPTIONMENUITEM_CHECKTYPE_IDX                       520
#define SBK_QSTYLEOPTIONPROGRESSBAR_IDX                              524
#define SBK_QSTYLEOPTIONPROGRESSBAR_STYLEOPTIONTYPE_IDX              525
#define SBK_QSTYLEOPTIONPROGRESSBAR_STYLEOPTIONVERSION_IDX           526
#define SBK_QSTYLEOPTIONPROGRESSBARV2_IDX                            527
#define SBK_QSTYLEOPTIONPROGRESSBARV2_STYLEOPTIONTYPE_IDX            528
#define SBK_QSTYLEOPTIONPROGRESSBARV2_STYLEOPTIONVERSION_IDX         529
#define SBK_QSTYLEOPTIONHEADER_IDX                                   513
#define SBK_QSTYLEOPTIONHEADER_STYLEOPTIONTYPE_IDX                   517
#define SBK_QSTYLEOPTIONHEADER_STYLEOPTIONVERSION_IDX                518
#define SBK_QSTYLEOPTIONHEADER_SECTIONPOSITION_IDX                   514
#define SBK_QSTYLEOPTIONHEADER_SELECTEDPOSITION_IDX                  515
#define SBK_QSTYLEOPTIONHEADER_SORTINDICATOR_IDX                     516
#define SBK_QSTYLEOPTIONTOOLBOX_IDX                                  568
#define SBK_QSTYLEOPTIONTOOLBOX_STYLEOPTIONTYPE_IDX                  569
#define SBK_QSTYLEOPTIONTOOLBOX_STYLEOPTIONVERSION_IDX               570
#define SBK_QSTYLEOPTIONTABWIDGETFRAME_IDX                           557
#define SBK_QSTYLEOPTIONTABWIDGETFRAME_STYLEOPTIONTYPE_IDX           558
#define SBK_QSTYLEOPTIONTABWIDGETFRAME_STYLEOPTIONVERSION_IDX        559
#define SBK_QSTYLEOPTIONRUBBERBAND_IDX                               530
#define SBK_QSTYLEOPTIONRUBBERBAND_STYLEOPTIONTYPE_IDX               531
#define SBK_QSTYLEOPTIONRUBBERBAND_STYLEOPTIONVERSION_IDX            532
#define SBK_QSTYLEHINTRETURN_IDX                                     467
#define SBK_QSTYLEHINTRETURN_HINTRETURNTYPE_IDX                      468
#define SBK_QSTYLEHINTRETURN_STYLEOPTIONTYPE_IDX                     469
#define SBK_QSTYLEHINTRETURN_STYLEOPTIONVERSION_IDX                  470
#define SBK_QSTYLEHINTRETURNVARIANT_IDX                              474
#define SBK_QSTYLEHINTRETURNVARIANT_STYLEOPTIONTYPE_IDX              475
#define SBK_QSTYLEHINTRETURNVARIANT_STYLEOPTIONVERSION_IDX           476
#define SBK_QSTYLEHINTRETURNMASK_IDX                                 471
#define SBK_QSTYLEHINTRETURNMASK_STYLEOPTIONTYPE_IDX                 472
#define SBK_QSTYLEHINTRETURNMASK_STYLEOPTIONVERSION_IDX              473
#define SBK_QSTYLEOPTIONGRAPHICSITEM_IDX                             507
#define SBK_QSTYLEOPTIONGRAPHICSITEM_STYLEOPTIONTYPE_IDX             508
#define SBK_QSTYLEOPTIONGRAPHICSITEM_STYLEOPTIONVERSION_IDX          509
#define SBK_QSTYLEOPTIONFRAMEV2_IDX                                  502
#define SBK_QSTYLEOPTIONFRAMEV2_STYLEOPTIONVERSION_IDX               504
#define SBK_QSTYLEOPTIONFRAMEV2_FRAMEFEATURE_IDX                     503
#define SBK_QFLAGS_QSTYLEOPTIONFRAMEV2_FRAMEFEATURE__IDX             145
#define SBK_QSTYLEOPTIONFRAMEV3_IDX                                  505
#define SBK_QSTYLEOPTIONFRAMEV3_STYLEOPTIONVERSION_IDX               506
#define SBK_QSTYLEOPTIONSPINBOX_IDX                                  539
#define SBK_QSTYLEOPTIONSPINBOX_STYLEOPTIONTYPE_IDX                  540
#define SBK_QSTYLEOPTIONSPINBOX_STYLEOPTIONVERSION_IDX               541
#define SBK_QSTYLEOPTIONTOOLBOXV2_IDX                                571
#define SBK_QSTYLEOPTIONTOOLBOXV2_STYLEOPTIONVERSION_IDX             573
#define SBK_QSTYLEOPTIONTOOLBOXV2_TABPOSITION_IDX                    574
#define SBK_QSTYLEOPTIONTOOLBOXV2_SELECTEDPOSITION_IDX               572
#define SBK_QSTYLEOPTIONTABV2_IDX                                    553
#define SBK_QSTYLEOPTIONTABV2_STYLEOPTIONVERSION_IDX                 554
#define SBK_QSTYLEOPTIONTABV3_IDX                                    555
#define SBK_QSTYLEOPTIONTABV3_STYLEOPTIONVERSION_IDX                 556
#define SBK_QSTYLEOPTIONDOCKWIDGET_IDX                               491
#define SBK_QSTYLEOPTIONDOCKWIDGET_STYLEOPTIONTYPE_IDX               492
#define SBK_QSTYLEOPTIONDOCKWIDGET_STYLEOPTIONVERSION_IDX            493
#define SBK_QSTYLEOPTIONVIEWITEMV4_IDX                               588
#define SBK_QSTYLEOPTIONVIEWITEMV4_STYLEOPTIONVERSION_IDX            589
#define SBK_QSTYLEOPTIONVIEWITEMV4_VIEWITEMPOSITION_IDX              590
#define SBK_QSTYLEOPTIONDOCKWIDGETV2_IDX                             494
#define SBK_QSTYLEOPTIONDOCKWIDGETV2_STYLEOPTIONVERSION_IDX          495
#define SBK_QSTYLEOPTIONFOCUSRECT_IDX                                496
#define SBK_QSTYLEOPTIONFOCUSRECT_STYLEOPTIONTYPE_IDX                497
#define SBK_QSTYLEOPTIONFOCUSRECT_STYLEOPTIONVERSION_IDX             498
#define SBK_QINPUTCONTEXTFACTORY_IDX                                 278
#define SBK_QTOOLTIP_IDX                                             683
#define SBK_QWHATSTHIS_IDX                                           706
#define SBK_QGESTURERECOGNIZER_IDX                                   188
#define SBK_QGESTURERECOGNIZER_RESULTFLAG_IDX                        189
#define SBK_QFLAGS_QGESTURERECOGNIZER_RESULTFLAG__IDX                123
#define SBK_QFONT_IDX                                                160
#define SBK_QFONT_STYLEHINT_IDX                                      165
#define SBK_QFONT_STYLESTRATEGY_IDX                                  166
#define SBK_QFONT_HINTINGPREFERENCE_IDX                              723
#define SBK_QFONT_WEIGHT_IDX                                         167
#define SBK_QFONT_STYLE_IDX                                          164
#define SBK_QFONT_STRETCH_IDX                                        163
#define SBK_QFONT_CAPITALIZATION_IDX                                 161
#define SBK_QFONT_SPACINGTYPE_IDX                                    162
#define SBK_QTEXTCHARFORMAT_IDX                                      622
#define SBK_QTEXTCHARFORMAT_VERTICALALIGNMENT_IDX                    624
#define SBK_QTEXTCHARFORMAT_UNDERLINESTYLE_IDX                       623
#define SBK_QTEXTTABLECELLFORMAT_IDX                                 674
#define SBK_QTEXTIMAGEFORMAT_IDX                                     650
#define SBK_QFONTMETRICS_IDX                                         175
#define SBK_QPALETTE_IDX                                             370
#define SBK_QPALETTE_COLORGROUP_IDX                                  371
#define SBK_QPALETTE_COLORROLE_IDX                                   372
#define SBK_QGRADIENT_IDX                                            190
#define SBK_QGRADIENT_TYPE_IDX                                       194
#define SBK_QGRADIENT_SPREAD_IDX                                     193
#define SBK_QGRADIENT_COORDINATEMODE_IDX                             191
#define SBK_QGRADIENT_INTERPOLATIONMODE_IDX                          192
#define SBK_QLINEARGRADIENT_IDX                                      309
#define SBK_QCONICALGRADIENT_IDX                                     70
#define SBK_QRADIALGRADIENT_IDX                                      416
#define SBK_QBRUSH_IDX                                               44
#define SBK_QLAYOUTITEM_IDX                                          306
#define SBK_QWIDGETITEM_IDX                                          712
#define SBK_QCURSOR_IDX                                              73
#define SBK_QSIZEPOLICY_IDX                                          432
#define SBK_QSIZEPOLICY_POLICYFLAG_IDX                               435
#define SBK_QSIZEPOLICY_POLICY_IDX                                   434
#define SBK_QSIZEPOLICY_CONTROLTYPE_IDX                              433
#define SBK_QFLAGS_QSIZEPOLICY_CONTROLTYPE__IDX                      141
#define SBK_QSPACERITEM_IDX                                          440
#define SBK_QFONTINFO_IDX                                            174
#define SBK_QFONTMETRICSF_IDX                                        176
#define SBK_QPOLYGONF_IDX                                            388
#define SBK_QVECTOR_QPOINTF_IDX                                      388
#define SBK_QPOLYGON_IDX                                             387
#define SBK_QVECTOR_QPOINT_IDX                                       387
#define SBK_QPAINTDEVICE_IDX                                         352
#define SBK_QPAINTDEVICE_PAINTDEVICEMETRIC_IDX                       353
#define SBK_QPICTURE_IDX                                             375
#define SBK_QPRINTER_IDX                                             396
#define SBK_QPRINTER_PRINTERMODE_IDX                                 405
#define SBK_QPRINTER_ORIENTATION_IDX                                 399
#define SBK_QPRINTER_PAGESIZE_IDX                                    402
#define SBK_QPRINTER_PAGEORDER_IDX                                   401
#define SBK_QPRINTER_COLORMODE_IDX                                   397
#define SBK_QPRINTER_PAPERSOURCE_IDX                                 403
#define SBK_QPRINTER_PRINTERSTATE_IDX                                406
#define SBK_QPRINTER_OUTPUTFORMAT_IDX                                400
#define SBK_QPRINTER_PRINTRANGE_IDX                                  404
#define SBK_QPRINTER_UNIT_IDX                                        407
#define SBK_QPRINTER_DUPLEXMODE_IDX                                  398
#define SBK_QKEYSEQUENCE_IDX                                         296
#define SBK_QKEYSEQUENCE_STANDARDKEY_IDX                             299
#define SBK_QKEYSEQUENCE_SEQUENCEFORMAT_IDX                          297
#define SBK_QKEYSEQUENCE_SEQUENCEMATCH_IDX                           298
#define SBK_QCOLOR_IDX                                               57
#define SBK_QCOLOR_SPEC_IDX                                          58
#define SBK_QPAINTERPATHSTROKER_IDX                                  369
#define SBK_QTRANSFORM_IDX                                           687
#define SBK_QTRANSFORM_TRANSFORMATIONTYPE_IDX                        688
#define SBK_QMATRIX_IDX                                              321
#define SBK_QPAINTERPATH_IDX                                         366
#define SBK_QPAINTERPATH_ELEMENTTYPE_IDX                             368
#define SBK_QPAINTERPATH_ELEMENT_IDX                                 367
#define SBK_QGRAPHICSLAYOUTITEM_IDX                                  215
#define SBK_QGRAPHICSLAYOUT_IDX                                      214
#define SBK_QGRAPHICSANCHORLAYOUT_IDX                                196
#define SBK_QGRAPHICSGRIDLAYOUT_IDX                                  205
#define SBK_QGRAPHICSLINEARLAYOUT_IDX                                217
#define SBK_QTEXTLAYOUT_IDX                                          654
#define SBK_QTEXTLAYOUT_CURSORMODE_IDX                               655
#define SBK_QTEXTLAYOUT_FORMATRANGE_IDX                              656
#define SBK_QPIXMAP_IDX                                              379
#define SBK_QPIXMAP_HBITMAPFORMAT_IDX                                380
#define SBK_QIMAGE_IDX                                               267
#define SBK_QIMAGE_INVERTMODE_IDX                                    269
#define SBK_QIMAGE_FORMAT_IDX                                        268
#define SBK_QBITMAP_IDX                                              41
#define SBK_QICON_IDX                                                260
#define SBK_QICON_MODE_IDX                                           261
#define SBK_QICON_STATE_IDX                                          262
#define SBK_QICONENGINEV2_IDX                                        265
#define SBK_QICONENGINEV2_ICONENGINEHOOK_IDX                         266
#define SBK_QGRAPHICSITEM_IDX                                        206
#define SBK_QGRAPHICSITEM_GRAPHICSITEMFLAG_IDX                       210
#define SBK_QFLAGS_QGRAPHICSITEM_GRAPHICSITEMFLAG__IDX               126
#define SBK_QGRAPHICSITEM_GRAPHICSITEMCHANGE_IDX                     209
#define SBK_QGRAPHICSITEM_CACHEMODE_IDX                              207
#define SBK_QGRAPHICSITEM_PANELMODALITY_IDX                          211
#define SBK_QGRAPHICSITEM_EXTENSION_IDX                              208
#define SBK_QGRAPHICSITEMGROUP_IDX                                   213
#define SBK_QGRAPHICSLINEITEM_IDX                                    216
#define SBK_QABSTRACTGRAPHICSSHAPEITEM_IDX                           1
#define SBK_QGRAPHICSSIMPLETEXTITEM_IDX                              241
#define SBK_QGRAPHICSPATHITEM_IDX                                    220
#define SBK_QGRAPHICSELLIPSEITEM_IDX                                 204
#define SBK_QGRAPHICSRECTITEM_IDX                                    225
#define SBK_QGRAPHICSPOLYGONITEM_IDX                                 223
#define SBK_QGRAPHICSPIXMAPITEM_IDX                                  221
#define SBK_QGRAPHICSPIXMAPITEM_SHAPEMODE_IDX                        222
#define SBK_QPAINTER_IDX                                             361
#define SBK_QPAINTER_RENDERHINT_IDX                                  365
#define SBK_QFLAGS_QPAINTER_RENDERHINT__IDX                          139
#define SBK_QPAINTER_PIXMAPFRAGMENTHINT_IDX                          364
#define SBK_QFLAGS_QPAINTER_PIXMAPFRAGMENTHINT__IDX                  138
#define SBK_QPAINTER_COMPOSITIONMODE_IDX                             362
#define SBK_QPAINTER_PIXMAPFRAGMENT_IDX                              363
#define SBK_QSTYLEPAINTER_IDX                                        591
#define SBK_QDROPEVENT_IDX                                           100
#define SBK_QDRAGMOVEEVENT_IDX                                       99
#define SBK_QDRAGENTEREVENT_IDX                                      97
#define SBK_QINPUTMETHODEVENT_IDX                                    283
#define SBK_QINPUTMETHODEVENT_ATTRIBUTETYPE_IDX                      285
#define SBK_QINPUTMETHODEVENT_ATTRIBUTE_IDX                          284
#define SBK_QRESIZEEVENT_IDX                                         421
#define SBK_QICONDRAGEVENT_IDX                                       263
#define SBK_QHIDEEVENT_IDX                                           258
#define SBK_QSHOWEVENT_IDX                                           430
#define SBK_QMOVEEVENT_IDX                                           346
#define SBK_QGRAPHICSSCENEEVENT_IDX                                  234
#define SBK_QGRAPHICSSCENEDRAGDROPEVENT_IDX                          233
#define SBK_QGRAPHICSSCENERESIZEEVENT_IDX                            239
#define SBK_QGRAPHICSSCENEHOVEREVENT_IDX                             236
#define SBK_QGRAPHICSSCENEMOUSEEVENT_IDX                             237
#define SBK_QGRAPHICSSCENECONTEXTMENUEVENT_IDX                       231
#define SBK_QGRAPHICSSCENECONTEXTMENUEVENT_REASON_IDX                232
#define SBK_QGRAPHICSSCENEMOVEEVENT_IDX                              238
#define SBK_QGRAPHICSSCENEWHEELEVENT_IDX                             240
#define SBK_QGRAPHICSSCENEHELPEVENT_IDX                              235
#define SBK_QCLOSEEVENT_IDX                                          56
#define SBK_QPAINTEVENT_IDX                                          360
#define SBK_QFOCUSEVENT_IDX                                          158
#define SBK_QHOVEREVENT_IDX                                          259
#define SBK_QACCESSIBLEEVENT_IDX                                     30
#define SBK_QINPUTEVENT_IDX                                          282
#define SBK_QWHEELEVENT_IDX                                          708
#define SBK_QCONTEXTMENUEVENT_IDX                                    71
#define SBK_QCONTEXTMENUEVENT_REASON_IDX                             72
#define SBK_QMOUSEEVENT_IDX                                          344
#define SBK_QTOUCHEVENT_IDX                                          684
#define SBK_QTOUCHEVENT_DEVICETYPE_IDX                               685
#define SBK_QTOUCHEVENT_TOUCHPOINT_IDX                               686
#define SBK_QKEYEVENT_IDX                                            294
#define SBK_QTABLETEVENT_IDX                                         611
#define SBK_QTABLETEVENT_TABLETDEVICE_IDX                            613
#define SBK_QTABLETEVENT_POINTERTYPE_IDX                             612
#define SBK_QGESTUREEVENT_IDX                                        187
#define SBK_QWINDOWSTATECHANGEEVENT_IDX                              713
#define SBK_QCLIPBOARDEVENT_IDX                                      55
#define SBK_QSTATUSTIPEVENT_IDX                                      452
#define SBK_QACTIONEVENT_IDX                                         36
#define SBK_QFILEOPENEVENT_IDX                                       110
#define SBK_QSHORTCUTEVENT_IDX                                       429
#define SBK_QWHATSTHISCLICKEDEVENT_IDX                               707
#define SBK_QTOOLBARCHANGEEVENT_IDX                                  679
#define SBK_QHELPEVENT_IDX                                           257
#define SBK_QDRAGLEAVEEVENT_IDX                                      98
#define SBK_QREGION_IDX                                              419
#define SBK_QREGION_REGIONTYPE_IDX                                   420
#define SBK_QWIDGET_IDX                                              709
#define SBK_QWIDGET_RENDERFLAG_IDX                                   710
#define SBK_QFLAGS_QWIDGET_RENDERFLAG__IDX                           156
#define SBK_QWIZARDPAGE_IDX                                          720
#define SBK_QDIALOG_IDX                                              83
#define SBK_QDIALOG_DIALOGCODE_IDX                                   84
#define SBK_QABSTRACTPRINTDIALOG_IDX                                 15
#define SBK_QABSTRACTPRINTDIALOG_PRINTRANGE_IDX                      17
#define SBK_QABSTRACTPRINTDIALOG_PRINTDIALOGOPTION_IDX               16
#define SBK_QFLAGS_QABSTRACTPRINTDIALOG_PRINTDIALOGOPTION__IDX       114
#define SBK_QPRINTDIALOG_IDX                                         389
#define SBK_QPROGRESSDIALOG_IDX                                      411
#define SBK_QABSTRACTPAGESETUPDIALOG_IDX                             14
#define SBK_QPAGESETUPDIALOG_IDX                                     350
#define SBK_QPAGESETUPDIALOG_PAGESETUPDIALOGOPTION_IDX               351
#define SBK_QFLAGS_QPAGESETUPDIALOG_PAGESETUPDIALOGOPTION__IDX       135
#define SBK_QWIZARD_IDX                                              715
#define SBK_QWIZARD_WIZARDBUTTON_IDX                                 716
#define SBK_QWIZARD_WIZARDPIXMAP_IDX                                 718
#define SBK_QWIZARD_WIZARDSTYLE_IDX                                  719
#define SBK_QWIZARD_WIZARDOPTION_IDX                                 717
#define SBK_QFLAGS_QWIZARD_WIZARDOPTION__IDX                         157
#define SBK_QFONTDIALOG_IDX                                          172
#define SBK_QFONTDIALOG_FONTDIALOGOPTION_IDX                         173
#define SBK_QFLAGS_QFONTDIALOG_FONTDIALOGOPTION__IDX                 122
#define SBK_QFILEDIALOG_IDX                                          102
#define SBK_QFILEDIALOG_VIEWMODE_IDX                                 107
#define SBK_QFILEDIALOG_FILEMODE_IDX                                 105
#define SBK_QFILEDIALOG_ACCEPTMODE_IDX                               103
#define SBK_QFILEDIALOG_DIALOGLABEL_IDX                              104
#define SBK_QFILEDIALOG_OPTION_IDX                                   106
#define SBK_QFLAGS_QFILEDIALOG_OPTION__IDX                           120
#define SBK_QERRORMESSAGE_IDX                                        101
#define SBK_QPRINTPREVIEWDIALOG_IDX                                  392
#define SBK_QMESSAGEBOX_IDX                                          339
#define SBK_QMESSAGEBOX_ICON_IDX                                     341
#define SBK_QMESSAGEBOX_BUTTONROLE_IDX                               340
#define SBK_QMESSAGEBOX_STANDARDBUTTON_IDX                           342
#define SBK_QFLAGS_QMESSAGEBOX_STANDARDBUTTON__IDX                   134
#define SBK_QCOLORDIALOG_IDX                                         59
#define SBK_QCOLORDIALOG_COLORDIALOGOPTION_IDX                       60
#define SBK_QFLAGS_QCOLORDIALOG_COLORDIALOGOPTION__IDX               116
#define SBK_QWORKSPACE_IDX                                           721
#define SBK_QWORKSPACE_WINDOWORDER_IDX                               722
#define SBK_QSTATUSBAR_IDX                                           451
#define SBK_QRUBBERBAND_IDX                                          422
#define SBK_QRUBBERBAND_SHAPE_IDX                                    423
#define SBK_QTOOLBAR_IDX                                             678
#define SBK_QSPLITTERHANDLE_IDX                                      444
#define SBK_QTABWIDGET_IDX                                           603
#define SBK_QTABWIDGET_TABPOSITION_IDX                               604
#define SBK_QTABWIDGET_TABSHAPE_IDX                                  605
#define SBK_QSPLASHSCREEN_IDX                                        442
#define SBK_QTABBAR_IDX                                              599
#define SBK_QTABBAR_SHAPE_IDX                                        602
#define SBK_QTABBAR_BUTTONPOSITION_IDX                               600
#define SBK_QTABBAR_SELECTIONBEHAVIOR_IDX                            601
#define SBK_QSIZEGRIP_IDX                                            431
#define SBK_QABSTRACTSLIDER_IDX                                      20
#define SBK_QABSTRACTSLIDER_SLIDERACTION_IDX                         21
#define SBK_QABSTRACTSLIDER_SLIDERCHANGE_IDX                         22
#define SBK_QPROGRESSBAR_IDX                                         409
#define SBK_QPROGRESSBAR_DIRECTION_IDX                               410
#define SBK_QFRAME_IDX                                               181
#define SBK_QFRAME_SHAPE_IDX                                         183
#define SBK_QFRAME_SHADOW_IDX                                        182
#define SBK_QFRAME_STYLEMASK_IDX                                     184
#define SBK_QSTACKEDWIDGET_IDX                                       447
#define SBK_QABSTRACTSCROLLAREA_IDX                                  19
#define SBK_QSPLITTER_IDX                                            443
#define SBK_QTOOLBOX_IDX                                             680
#define SBK_QSCROLLAREA_IDX                                          424
#define SBK_QABSTRACTBUTTON_IDX                                      0
#define SBK_QTOOLBUTTON_IDX                                          681
#define SBK_QTOOLBUTTON_TOOLBUTTONPOPUPMODE_IDX                      682
#define SBK_QRADIOBUTTON_IDX                                         417
#define SBK_QPRINTPREVIEWWIDGET_IDX                                  393
#define SBK_QPRINTPREVIEWWIDGET_VIEWMODE_IDX                         394
#define SBK_QPRINTPREVIEWWIDGET_ZOOMMODE_IDX                         395
#define SBK_QSCROLLBAR_IDX                                           425
#define SBK_QPLAINTEXTEDIT_IDX                                       384
#define SBK_QPLAINTEXTEDIT_LINEWRAPMODE_IDX                          385
#define SBK_QTEXTEDIT_IDX                                            635
#define SBK_QTEXTEDIT_LINEWRAPMODE_IDX                               638
#define SBK_QTEXTEDIT_AUTOFORMATTINGFLAG_IDX                         636
#define SBK_QFLAGS_QTEXTEDIT_AUTOFORMATTINGFLAG__IDX                 151
#define SBK_QTEXTEDIT_EXTRASELECTION_IDX                             637
#define SBK_QTEXTBROWSER_IDX                                         621
#define SBK_QMENUBAR_IDX                                             338
#define SBK_QMENU_IDX                                                337
#define SBK_QMDISUBWINDOW_IDX                                        335
#define SBK_QMDISUBWINDOW_SUBWINDOWOPTION_IDX                        336
#define SBK_QFLAGS_QMDISUBWINDOW_SUBWINDOWOPTION__IDX                133
#define SBK_QMAINWINDOW_IDX                                          319
#define SBK_QMAINWINDOW_DOCKOPTION_IDX                               320
#define SBK_QFLAGS_QMAINWINDOW_DOCKOPTION__IDX                       131
#define SBK_QMDIAREA_IDX                                             331
#define SBK_QMDIAREA_AREAOPTION_IDX                                  332
#define SBK_QFLAGS_QMDIAREA_AREAOPTION__IDX                          132
#define SBK_QMDIAREA_WINDOWORDER_IDX                                 334
#define SBK_QMDIAREA_VIEWMODE_IDX                                    333
#define SBK_QLINEEDIT_IDX                                            307
#define SBK_QLINEEDIT_ECHOMODE_IDX                                   308
#define SBK_QINPUTDIALOG_IDX                                         279
#define SBK_QINPUTDIALOG_INPUTDIALOGOPTION_IDX                       280
#define SBK_QINPUTDIALOG_INPUTMODE_IDX                               281
#define SBK_QDESKTOPWIDGET_IDX                                       81
#define SBK_QABSTRACTITEMVIEW_IDX                                    4
#define SBK_QABSTRACTITEMVIEW_SELECTIONMODE_IDX                      12
#define SBK_QABSTRACTITEMVIEW_SELECTIONBEHAVIOR_IDX                  11
#define SBK_QABSTRACTITEMVIEW_SCROLLHINT_IDX                         9
#define SBK_QABSTRACTITEMVIEW_EDITTRIGGER_IDX                        8
#define SBK_QFLAGS_QABSTRACTITEMVIEW_EDITTRIGGER__IDX                113
#define SBK_QABSTRACTITEMVIEW_SCROLLMODE_IDX                         10
#define SBK_QABSTRACTITEMVIEW_DRAGDROPMODE_IDX                       6
#define SBK_QABSTRACTITEMVIEW_CURSORACTION_IDX                       5
#define SBK_QABSTRACTITEMVIEW_STATE_IDX                              13
#define SBK_QABSTRACTITEMVIEW_DROPINDICATORPOSITION_IDX              7
#define SBK_QTREEVIEW_IDX                                            689
#define SBK_QTREEWIDGET_IDX                                          690
#define SBK_QCOLUMNVIEW_IDX                                          61
#define SBK_QLISTVIEW_IDX                                            310
#define SBK_QLISTVIEW_MOVEMENT_IDX                                   313
#define SBK_QLISTVIEW_FLOW_IDX                                       311
#define SBK_QLISTVIEW_RESIZEMODE_IDX                                 314
#define SBK_QLISTVIEW_LAYOUTMODE_IDX                                 312
#define SBK_QLISTVIEW_VIEWMODE_IDX                                   315
#define SBK_QLISTWIDGET_IDX                                          316
#define SBK_QTABLEVIEW_IDX                                           606
#define SBK_QTABLEWIDGET_IDX                                         607
#define SBK_QHEADERVIEW_IDX                                          255
#define SBK_QHEADERVIEW_RESIZEMODE_IDX                               256
#define SBK_QCALENDARWIDGET_IDX                                      47
#define SBK_QCALENDARWIDGET_HORIZONTALHEADERFORMAT_IDX               48
#define SBK_QCALENDARWIDGET_VERTICALHEADERFORMAT_IDX                 50
#define SBK_QCALENDARWIDGET_SELECTIONMODE_IDX                        49
#define SBK_QSLIDER_IDX                                              436
#define SBK_QSLIDER_TICKPOSITION_IDX                                 437
#define SBK_QCHECKBOX_IDX                                            51
#define SBK_QABSTRACTSPINBOX_IDX                                     23
#define SBK_QABSTRACTSPINBOX_STEPENABLEDFLAG_IDX                     26
#define SBK_QFLAGS_QABSTRACTSPINBOX_STEPENABLEDFLAG__IDX             115
#define SBK_QABSTRACTSPINBOX_BUTTONSYMBOLS_IDX                       24
#define SBK_QABSTRACTSPINBOX_CORRECTIONMODE_IDX                      25
#define SBK_QDOUBLESPINBOX_IDX                                       93
#define SBK_QSPINBOX_IDX                                             441
#define SBK_QUNDOVIEW_IDX                                            699
#define SBK_QLCDNUMBER_IDX                                           300
#define SBK_QLCDNUMBER_MODE_IDX                                      301
#define SBK_QLCDNUMBER_SEGMENTSTYLE_IDX                              302
#define SBK_QLABEL_IDX                                               303
#define SBK_QGROUPBOX_IDX                                            252
#define SBK_QDOCKWIDGET_IDX                                          91
#define SBK_QDOCKWIDGET_DOCKWIDGETFEATURE_IDX                        92
#define SBK_QFLAGS_QDOCKWIDGET_DOCKWIDGETFEATURE__IDX                119
#define SBK_QFOCUSFRAME_IDX                                          159
#define SBK_QDIALOGBUTTONBOX_IDX                                     85
#define SBK_QDIALOGBUTTONBOX_BUTTONROLE_IDX                          87
#define SBK_QDIALOGBUTTONBOX_STANDARDBUTTON_IDX                      88
#define SBK_QFLAGS_QDIALOGBUTTONBOX_STANDARDBUTTON__IDX              118
#define SBK_QDIALOGBUTTONBOX_BUTTONLAYOUT_IDX                        86
#define SBK_QPUSHBUTTON_IDX                                          413
#define SBK_QDIAL_IDX                                                82
#define SBK_QCOMMANDLINKBUTTON_IDX                                   65
#define SBK_QDATETIMEEDIT_IDX                                        77
#define SBK_QDATETIMEEDIT_SECTION_IDX                                78
#define SBK_QFLAGS_QDATETIMEEDIT_SECTION__IDX                        117
#define SBK_QTIMEEDIT_IDX                                            677
#define SBK_QDATEEDIT_IDX                                            76
#define SBK_QCOMBOBOX_IDX                                            62
#define SBK_QCOMBOBOX_INSERTPOLICY_IDX                               63
#define SBK_QCOMBOBOX_SIZEADJUSTPOLICY_IDX                           64
#define SBK_QFONTCOMBOBOX_IDX                                        168
#define SBK_QFONTCOMBOBOX_FONTFILTER_IDX                             169
#define SBK_QFLAGS_QFONTCOMBOBOX_FONTFILTER__IDX                     121
#define SBK_QUNDOSTACK_IDX                                           698
#define SBK_QUNDOGROUP_IDX                                           697
#define SBK_QABSTRACTITEMDELEGATE_IDX                                2
#define SBK_QABSTRACTITEMDELEGATE_ENDEDITHINT_IDX                    3
#define SBK_QITEMDELEGATE_IDX                                        287
#define SBK_QSTYLEDITEMDELEGATE_IDX                                  592
#define SBK_QSYSTEMTRAYICON_IDX                                      596
#define SBK_QSYSTEMTRAYICON_ACTIVATIONREASON_IDX                     597
#define SBK_QSYSTEMTRAYICON_MESSAGEICON_IDX                          598
#define SBK_QPYTEXTOBJECT_IDX                                        414
#define SBK_QCOMPLETER_IDX                                           67
#define SBK_QCOMPLETER_COMPLETIONMODE_IDX                            68
#define SBK_QCOMPLETER_MODELSORTING_IDX                              69
#define SBK_QGRAPHICSEFFECT_IDX                                      201
#define SBK_QGRAPHICSEFFECT_CHANGEFLAG_IDX                           202
#define SBK_QFLAGS_QGRAPHICSEFFECT_CHANGEFLAG__IDX                   125
#define SBK_QGRAPHICSEFFECT_PIXMAPPADMODE_IDX                        203
#define SBK_QGRAPHICSCOLORIZEEFFECT_IDX                              199
#define SBK_QGRAPHICSBLUREFFECT_IDX                                  197
#define SBK_QGRAPHICSBLUREFFECT_BLURHINT_IDX                         198
#define SBK_QFLAGS_QGRAPHICSBLUREFFECT_BLURHINT__IDX                 124
#define SBK_QGRAPHICSOPACITYEFFECT_IDX                               219
#define SBK_QGRAPHICSDROPSHADOWEFFECT_IDX                            200
#define SBK_QSYNTAXHIGHLIGHTER_IDX                                   595
#define SBK_QDATAWIDGETMAPPER_IDX                                    74
#define SBK_QDATAWIDGETMAPPER_SUBMITPOLICY_IDX                       75
#define SBK_QITEMSELECTIONMODEL_IDX                                  291
#define SBK_QITEMSELECTIONMODEL_SELECTIONFLAG_IDX                    292
#define SBK_QFLAGS_QITEMSELECTIONMODEL_SELECTIONFLAG__IDX            130
#define SBK_QTEXTOBJECT_IDX                                          665
#define SBK_QTEXTBLOCKGROUP_IDX                                      619
#define SBK_QTEXTLIST_IDX                                            662
#define SBK_QTEXTFRAME_IDX                                           645
#define SBK_QTEXTFRAME_ITERATOR_IDX                                  646
#define SBK_QTEXTTABLE_IDX                                           672
#define SBK_QDRAG_IDX                                                96
#define SBK_QGRAPHICSSCENE_IDX                                       228
#define SBK_QGRAPHICSSCENE_ITEMINDEXMETHOD_IDX                       229
#define SBK_QGRAPHICSSCENE_SCENELAYER_IDX                            230
#define SBK_QFLAGS_QGRAPHICSSCENE_SCENELAYER__IDX                    127
#define SBK_QGRAPHICSVIEW_IDX                                        244
#define SBK_QGRAPHICSVIEW_VIEWPORTANCHOR_IDX                         248
#define SBK_QGRAPHICSVIEW_CACHEMODEFLAG_IDX                          245
#define SBK_QFLAGS_QGRAPHICSVIEW_CACHEMODEFLAG__IDX                  128
#define SBK_QGRAPHICSVIEW_DRAGMODE_IDX                               246
#define SBK_QGRAPHICSVIEW_VIEWPORTUPDATEMODE_IDX                     249
#define SBK_QGRAPHICSVIEW_OPTIMIZATIONFLAG_IDX                       247
#define SBK_QFLAGS_QGRAPHICSVIEW_OPTIMIZATIONFLAG__IDX               129
#define SBK_QCLIPBOARD_IDX                                           53
#define SBK_QCLIPBOARD_MODE_IDX                                      54
#define SBK_QSTYLE_IDX                                               454
#define SBK_QSTYLE_STATEFLAG_IDX                                     462
#define SBK_QFLAGS_QSTYLE_STATEFLAG__IDX                             142
#define SBK_QSTYLE_PRIMITIVEELEMENT_IDX                              459
#define SBK_QSTYLE_CONTROLELEMENT_IDX                                457
#define SBK_QSTYLE_SUBELEMENT_IDX                                    465
#define SBK_QSTYLE_COMPLEXCONTROL_IDX                                455
#define SBK_QSTYLE_SUBCONTROL_IDX                                    464
#define SBK_QFLAGS_QSTYLE_SUBCONTROL__IDX                            143
#define SBK_QSTYLE_PIXELMETRIC_IDX                                   458
#define SBK_QSTYLE_CONTENTSTYPE_IDX                                  456
#define SBK_QSTYLE_REQUESTSOFTWAREINPUTPANEL_IDX                     460
#define SBK_QSTYLE_STYLEHINT_IDX                                     463
#define SBK_QSTYLE_STANDARDPIXMAP_IDX                                461
#define SBK_QCOMMONSTYLE_IDX                                         66
#define SBK_QWINDOWSSTYLE_IDX                                        714
#define SBK_QPLASTIQUESTYLE_IDX                                      386
#define SBK_QCLEANLOOKSSTYLE_IDX                                     52
#define SBK_QMOTIFSTYLE_IDX                                          343
#define SBK_QCDESTYLE_IDX                                            46
#define SBK_QBUTTONGROUP_IDX                                         45
#define SBK_QGRAPHICSOBJECT_IDX                                      218
#define SBK_QGRAPHICSWIDGET_IDX                                      250
#define SBK_QGRAPHICSPROXYWIDGET_IDX                                 224
#define SBK_QGRAPHICSTEXTITEM_IDX                                    242
#define SBK_QVALIDATOR_IDX                                           701
#define SBK_QVALIDATOR_STATE_IDX                                     702
#define SBK_QDOUBLEVALIDATOR_IDX                                     94
#define SBK_QDOUBLEVALIDATOR_NOTATION_IDX                            95
#define SBK_QREGEXPVALIDATOR_IDX                                     418
#define SBK_QINTVALIDATOR_IDX                                        286
#define SBK_QGRAPHICSTRANSFORM_IDX                                   243
#define SBK_QGRAPHICSSCALE_IDX                                       227
#define SBK_QGRAPHICSROTATION_IDX                                    226
#define SBK_QSOUND_IDX                                               439
#define SBK_QSTANDARDITEMMODEL_IDX                                   450
#define SBK_QSTRINGLISTMODEL_IDX                                     453
#define SBK_QPROXYMODEL_IDX                                          412
#define SBK_QABSTRACTPROXYMODEL_IDX                                  18
#define SBK_QSORTFILTERPROXYMODEL_IDX                                438
#define SBK_QDIRMODEL_IDX                                            89
#define SBK_QDIRMODEL_ROLES_IDX                                      90
#define SBK_QFILESYSTEMMODEL_IDX                                     111
#define SBK_QFILESYSTEMMODEL_ROLES_IDX                               112
#define SBK_QINPUTCONTEXT_IDX                                        276
#define SBK_QINPUTCONTEXT_STANDARDFORMAT_IDX                         277
#define SBK_QMOUSEEVENTTRANSITION_IDX                                345
#define SBK_QKEYEVENTTRANSITION_IDX                                  295
#define SBK_QGRAPHICSITEMANIMATION_IDX                               212
#define SBK_QABSTRACTTEXTDOCUMENTLAYOUT_IDX                          27
#define SBK_QPLAINTEXTDOCUMENTLAYOUT_IDX                             383
#define SBK_QABSTRACTTEXTDOCUMENTLAYOUT_SELECTION_IDX                29
#define SBK_QABSTRACTTEXTDOCUMENTLAYOUT_PAINTCONTEXT_IDX             28
#define SBK_QSHORTCUT_IDX                                            428
#define SBK_QLAYOUT_IDX                                              304
#define SBK_QLAYOUT_SIZECONSTRAINT_IDX                               305
#define SBK_QSTACKEDLAYOUT_IDX                                       445
#define SBK_QSTACKEDLAYOUT_STACKINGMODE_IDX                          446
#define SBK_QFORMLAYOUT_IDX                                          177
#define SBK_QFORMLAYOUT_FIELDGROWTHPOLICY_IDX                        178
#define SBK_QFORMLAYOUT_ROWWRAPPOLICY_IDX                            180
#define SBK_QFORMLAYOUT_ITEMROLE_IDX                                 179
#define SBK_QBOXLAYOUT_IDX                                           42
#define SBK_QBOXLAYOUT_DIRECTION_IDX                                 43
#define SBK_QVBOXLAYOUT_IDX                                          700
#define SBK_QHBOXLAYOUT_IDX                                          254
#define SBK_QGRIDLAYOUT_IDX                                          251
#define SBK_QSESSIONMANAGER_IDX                                      426
#define SBK_QSESSIONMANAGER_RESTARTHINT_IDX                          427
#define SBK_QACTIONGROUP_IDX                                         37
#define SBK_QGRAPHICSANCHOR_IDX                                      195
#define SBK_QACTION_IDX                                              31
#define SBK_QACTION_MENUROLE_IDX                                     33
#define SBK_QACTION_SOFTKEYROLE_IDX                                  35
#define SBK_QACTION_PRIORITY_IDX                                     34
#define SBK_QACTION_ACTIONEVENT_IDX                                  32
#define SBK_QWIDGETACTION_IDX                                        711
#define SBK_QGESTURE_IDX                                             185
#define SBK_QGESTURE_GESTURECANCELPOLICY_IDX                         186
#define SBK_QPINCHGESTURE_IDX                                        377
#define SBK_QPINCHGESTURE_CHANGEFLAG_IDX                             378
#define SBK_QFLAGS_QPINCHGESTURE_CHANGEFLAG__IDX                     140
#define SBK_QPANGESTURE_IDX                                          373
#define SBK_QTAPGESTURE_IDX                                          615
#define SBK_QSWIPEGESTURE_IDX                                        593
#define SBK_QSWIPEGESTURE_SWIPEDIRECTION_IDX                         594
#define SBK_QTAPANDHOLDGESTURE_IDX                                   614
#define SBK_QAPPLICATION_IDX                                         38
#define SBK_QAPPLICATION_TYPE_IDX                                    40
#define SBK_QAPPLICATION_COLORSPEC_IDX                               39
#define SBK_QMOVIE_IDX                                               347
#define SBK_QMOVIE_MOVIESTATE_IDX                                    349
#define SBK_QMOVIE_CACHEMODE_IDX                                     348
#define SBK_QIMAGEWRITER_IDX                                         274
#define SBK_QIMAGEWRITER_IMAGEWRITERERROR_IDX                        275
#define SBK_QIMAGEREADER_IDX                                         272
#define SBK_QIMAGEREADER_IMAGEREADERERROR_IDX                        273
#define SBK_QTEXTDOCUMENT_IDX                                        629
#define SBK_QTEXTDOCUMENT_METAINFORMATION_IDX                        631
#define SBK_QTEXTDOCUMENT_FINDFLAG_IDX                               630
#define SBK_QFLAGS_QTEXTDOCUMENT_FINDFLAG__IDX                       150
#define SBK_QTEXTDOCUMENT_RESOURCETYPE_IDX                           632
#define SBK_QTEXTDOCUMENT_STACKS_IDX                                 633
#define SBK_QtGui_IDX_COUNT                                          725

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtGuiTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtGuiTypeConverters;

// Converter indices
#define SBK_WID_IDX                                                  0
#define SBK_QTGUI_QLIST_QBYTEARRAY_IDX                               1 // QList<QByteArray >
#define SBK_QTGUI_QLIST_QPRINTERINFO_IDX                             2 // QList<QPrinterInfo >
#define SBK_QTGUI_QLIST_QPRINTER_PAGESIZE_IDX                        3 // QList<QPrinter::PageSize >
#define SBK_QTGUI_QLIST_QITEMSELECTIONRANGE_IDX                      4 // const QList<QItemSelectionRange > &
#define SBK_QTGUI_QSET_QITEMSELECTIONRANGE_IDX                       5 // const QSet<QItemSelectionRange > &
#define SBK_QTGUI_QVECTOR_QITEMSELECTIONRANGE_IDX                    6 // const QVector<QItemSelectionRange > &
#define SBK_QTGUI_QLIST_QTREEWIDGETITEMPTR_IDX                       7 // const QList<QTreeWidgetItem * > &
#define SBK_QTGUI_QLIST_QSTANDARDITEMPTR_IDX                         8 // const QList<QStandardItem * > &
#define SBK_QTGUI_QVECTOR_QTEXTLENGTH_IDX                            9 // QVector<QTextLength >
#define SBK_QTGUI_QMAP_INT_QVARIANT_IDX                              10 // QMap<int, QVariant >
#define SBK_QTGUI_QLIST_QTEXTOPTION_TAB_IDX                          11 // const QList<QTextOption::Tab > &
#define SBK_QTGUI_QLIST_QREAL_IDX                                    12 // QList<qreal >
#define SBK_QTGUI_QVECTOR_QREAL_IDX                                  13 // QVector<qreal >
#define SBK_QTGUI_QLIST_INT_IDX                                      14 // QList<int >
#define SBK_QTGUI_QLIST_QFONTDATABASE_WRITINGSYSTEM_IDX              15 // QList<QFontDatabase::WritingSystem >
#define SBK_QTGUI_QPAIR_QREAL_QCOLOR_IDX                             16 // QPair<qreal, QColor >
#define SBK_QTGUI_QVECTOR_QPAIR_QREAL_QCOLOR_IDX                     17 // const QVector<QPair<qreal, QColor > > &
#define SBK_QTGUI_QVECTOR_QPOINTF_IDX                                18 // const QVector<QPointF > &
#define SBK_QTGUI_QLIST_QPOINTF_IDX                                  19 // const QList<QPointF > &
#define SBK_QTGUI_QVECTOR_QPOINT_IDX                                 20 // const QVector<QPoint > &
#define SBK_QTGUI_QLIST_QPOINT_IDX                                   21 // const QList<QPoint > &
#define SBK_QTGUI_QLIST_QPRINTER_PAPERSOURCE_IDX                     22 // QList<QPrinter::PaperSource >
#define SBK_QTGUI_QLIST_QKEYSEQUENCE_IDX                             23 // QList<QKeySequence >
#define SBK_QTGUI_QLIST_QPOLYGONF_IDX                                24 // QList<QPolygonF >
#define SBK_QTGUI_QLIST_QTEXTLAYOUT_FORMATRANGE_IDX                  25 // QList<QTextLayout::FormatRange >
#define SBK_QTGUI_QVECTOR_QTEXTLAYOUT_FORMATRANGE_IDX                26 // const QVector<QTextLayout::FormatRange > &
#define SBK_QTGUI_QVECTOR_UNSIGNEDINT_IDX                            27 // QVector<unsigned int >
#define SBK_QTGUI_QLIST_QSIZE_IDX                                    28 // QList<QSize >
#define SBK_QTGUI_QLIST_QGRAPHICSITEMPTR_IDX                         29 // QList<QGraphicsItem * >
#define SBK_QTGUI_QLIST_QGRAPHICSTRANSFORMPTR_IDX                    30 // const QList<QGraphicsTransform * > &
#define SBK_QTGUI_QVECTOR_QLINE_IDX                                  31 // const QVector<QLine > &
#define SBK_QTGUI_QVECTOR_QLINEF_IDX                                 32 // const QVector<QLineF > &
#define SBK_QTGUI_QVECTOR_QRECT_IDX                                  33 // const QVector<QRect > &
#define SBK_QTGUI_QVECTOR_QRECTF_IDX                                 34 // const QVector<QRectF > &
#define SBK_QTGUI_QLIST_QINPUTMETHODEVENT_ATTRIBUTE_IDX              35 // const QList<QInputMethodEvent::Attribute > &
#define SBK_QTGUI_QLIST_QTOUCHEVENT_TOUCHPOINT_IDX                   36 // const QList<QTouchEvent::TouchPoint > &
#define SBK_QTGUI_QLIST_QGESTUREPTR_IDX                              37 // const QList<QGesture * > &
#define SBK_QTGUI_QLIST_QACTIONPTR_IDX                               38 // QList<QAction * >
#define SBK_QTGUI_QLIST_QOBJECTPTR_IDX                               39 // const QList<QObject * > &
#define SBK_QTGUI_QLIST_QWIDGETPTR_IDX                               40 // const QList<QWidget * > &
#define SBK_QTGUI_QLIST_QWIZARD_WIZARDBUTTON_IDX                     41 // const QList<QWizard::WizardButton > &
#define SBK_QTGUI_QLIST_QURL_IDX                                     42 // const QList<QUrl > &
#define SBK_QTGUI_QLIST_QABSTRACTBUTTONPTR_IDX                       43 // QList<QAbstractButton * >
#define SBK_QTGUI_QLIST_QTEXTEDIT_EXTRASELECTION_IDX                 44 // QList<QTextEdit::ExtraSelection >
#define SBK_QTGUI_QLIST_QDOCKWIDGETPTR_IDX                           45 // QList<QDockWidget * >
#define SBK_QTGUI_QLIST_QMDISUBWINDOWPTR_IDX                         46 // QList<QMdiSubWindow * >
#define SBK_QTGUI_QLIST_QLISTWIDGETITEMPTR_IDX                       47 // QList<QListWidgetItem * >
#define SBK_QTGUI_QLIST_QTABLEWIDGETITEMPTR_IDX                      48 // QList<QTableWidgetItem * >
#define SBK_QTGUI_QLIST_QTABLEWIDGETSELECTIONRANGE_IDX               49 // QList<QTableWidgetSelectionRange >
#define SBK_QTGUI_QMAP_QDATE_QTEXTCHARFORMAT_IDX                     50 // QMap<QDate, QTextCharFormat >
#define SBK_QTGUI_QLIST_QUNDOSTACKPTR_IDX                            51 // QList<QUndoStack * >
#define SBK_QTGUI_QLIST_QTEXTBLOCK_IDX                               52 // QList<QTextBlock >
#define SBK_QTGUI_QLIST_QTEXTFRAMEPTR_IDX                            53 // QList<QTextFrame * >
#define SBK_QTGUI_QLIST_QRECTF_IDX                                   54 // const QList<QRectF > &
#define SBK_QTGUI_QLIST_QGRAPHICSVIEWPTR_IDX                         55 // QList<QGraphicsView * >
#define SBK_QTGUI_QHASH_INT_QBYTEARRAY_IDX                           56 // const QHash<int, QByteArray > &
#define SBK_QTGUI_QLIST_QABSTRACTANIMATIONPTR_IDX                    57 // QList<QAbstractAnimation * >
#define SBK_QTGUI_QLIST_QABSTRACTSTATEPTR_IDX                        58 // const QList<QAbstractState * > &
#define SBK_QTGUI_QPAIR_QREAL_QPOINTF_IDX                            59 // QPair<qreal, QPointF >
#define SBK_QTGUI_QLIST_QPAIR_QREAL_QPOINTF_IDX                      60 // QList<QPair<qreal, QPointF > >
#define SBK_QTGUI_QPAIR_QREAL_QREAL_IDX                              61 // QPair<qreal, qreal >
#define SBK_QTGUI_QLIST_QPAIR_QREAL_QREAL_IDX                        62 // QList<QPair<qreal, qreal > >
#define SBK_QTGUI_QLIST_QGRAPHICSWIDGETPTR_IDX                       63 // QList<QGraphicsWidget * >
#define SBK_QTGUI_QVECTOR_QTEXTFORMAT_IDX                            64 // QVector<QTextFormat >
#define SBK_QTGUI_QLIST_QVARIANT_IDX                                 65 // QList<QVariant >
#define SBK_QTGUI_QLIST_QSTRING_IDX                                  66 // QList<QString >
#define SBK_QTGUI_QMAP_QSTRING_QVARIANT_IDX                          67 // QMap<QString, QVariant >
#define SBK_QtGui_CONVERTERS_IDX_COUNT                               68

// Macros for type check

// Protected enum surrogates
enum PySide_QtGui_QGraphicsItem_Extension_Surrogate {};
enum PySide_QtGui_QAbstractSlider_SliderChange_Surrogate {};
enum PySide_QtGui_QAbstractItemView_CursorAction_Surrogate {};
enum PySide_QtGui_QAbstractItemView_State_Surrogate {};
enum PySide_QtGui_QAbstractItemView_DropIndicatorPosition_Surrogate {};

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QMatrix4x3 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX4X3_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix4x2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX4X2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix3x4 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX3X4_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix3x3 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX3X3_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix3x2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX3X2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix2x4 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX2X4_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix2x3 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX2X3_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix2x2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX2X2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPixmapCache >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPIXMAPCACHE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPixmapCache::Key >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPIXMAPCACHE_KEY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPictureIO >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPICTUREIO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QImageIOHandler::ImageOption >() { return SbkPySide_QtGuiTypes[SBK_QIMAGEIOHANDLER_IMAGEOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QImageIOHandler >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QIMAGEIOHANDLER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QIconEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QICONENGINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextTableCell >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTTABLECELL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextFragment >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTFRAGMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextDocumentFragment >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTDOCUMENTFRAGMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextBlock >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTBLOCK_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextBlock::iterator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTBLOCK_ITERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextBlockUserData >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTBLOCKUSERDATA_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleFactory >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEFACTORY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QVector3D >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QVECTOR3D_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUndoCommand >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QUNDOCOMMAND_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDesktopServices::StandardLocation >() { return SbkPySide_QtGuiTypes[SBK_QDESKTOPSERVICES_STANDARDLOCATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDesktopServices >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDESKTOPSERVICES_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPrintEngine::PrintEnginePropertyKey >() { return SbkPySide_QtGuiTypes[SBK_QPRINTENGINE_PRINTENGINEPROPERTYKEY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrintEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPRINTENGINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPrinterInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPRINTERINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPaintEngine::PaintEngineFeature >() { return SbkPySide_QtGuiTypes[SBK_QPAINTENGINE_PAINTENGINEFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QPaintEngine::PaintEngineFeature> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QPAINTENGINE_PAINTENGINEFEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QPaintEngine::DirtyFlag >() { return SbkPySide_QtGuiTypes[SBK_QPAINTENGINE_DIRTYFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QPaintEngine::DirtyFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QPAINTENGINE_DIRTYFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QPaintEngine::PolygonDrawMode >() { return SbkPySide_QtGuiTypes[SBK_QPAINTENGINE_POLYGONDRAWMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPaintEngine::Type >() { return SbkPySide_QtGuiTypes[SBK_QPAINTENGINE_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPaintEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTENGINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPaintEngineState >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTENGINESTATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextItem::RenderFlag >() { return SbkPySide_QtGuiTypes[SBK_QTEXTITEM_RENDERFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextItem::RenderFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QTEXTITEM_RENDERFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTileRules >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTILERULES_IDX]); }
template<> inline PyTypeObject* SbkType< ::QVector2D >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QVECTOR2D_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix4x4 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX4X4_IDX]); }
template<> inline PyTypeObject* SbkType< ::QQuaternion >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QQUATERNION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QVector4D >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QVECTOR4D_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextLine::Edge >() { return SbkPySide_QtGuiTypes[SBK_QTEXTLINE_EDGE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextLine::CursorPosition >() { return SbkPySide_QtGuiTypes[SBK_QTEXTLINE_CURSORPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextLine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTLINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextObjectInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTOBJECTINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextInlineObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTINLINEOBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextCursor::MoveMode >() { return SbkPySide_QtGuiTypes[SBK_QTEXTCURSOR_MOVEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextCursor::MoveOperation >() { return SbkPySide_QtGuiTypes[SBK_QTEXTCURSOR_MOVEOPERATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextCursor::SelectionType >() { return SbkPySide_QtGuiTypes[SBK_QTEXTCURSOR_SELECTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextCursor >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTCURSOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QItemSelection >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QITEMSELECTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTreeWidgetItem::ItemType >() { return SbkPySide_QtGuiTypes[SBK_QTREEWIDGETITEM_ITEMTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTreeWidgetItem::ChildIndicatorPolicy >() { return SbkPySide_QtGuiTypes[SBK_QTREEWIDGETITEM_CHILDINDICATORPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTreeWidgetItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTREEWIDGETITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTreeWidgetItemIterator::IteratorFlag >() { return SbkPySide_QtGuiTypes[SBK_QTREEWIDGETITEMITERATOR_ITERATORFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTreeWidgetItemIterator::IteratorFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QTREEWIDGETITEMITERATOR_ITERATORFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTreeWidgetItemIterator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTREEWIDGETITEMITERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFileIconProvider::IconType >() { return SbkPySide_QtGuiTypes[SBK_QFILEICONPROVIDER_ICONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFileIconProvider >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFILEICONPROVIDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTableWidgetItem::ItemType >() { return SbkPySide_QtGuiTypes[SBK_QTABLEWIDGETITEM_ITEMTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTableWidgetItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTABLEWIDGETITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTableWidgetSelectionRange >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTABLEWIDGETSELECTIONRANGE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QItemEditorFactory >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QITEMEDITORFACTORY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QItemSelectionRange >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QITEMSELECTIONRANGE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStandardItem::ItemType >() { return SbkPySide_QtGuiTypes[SBK_QSTANDARDITEM_ITEMTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStandardItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTANDARDITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QListWidgetItem::ItemType >() { return SbkPySide_QtGuiTypes[SBK_QLISTWIDGETITEM_ITEMTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QListWidgetItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLISTWIDGETITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QItemEditorCreatorBase >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QITEMEDITORCREATORBASE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextFormat::FormatType >() { return SbkPySide_QtGuiTypes[SBK_QTEXTFORMAT_FORMATTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextFormat::Property >() { return SbkPySide_QtGuiTypes[SBK_QTEXTFORMAT_PROPERTY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextFormat::ObjectTypes >() { return SbkPySide_QtGuiTypes[SBK_QTEXTFORMAT_OBJECTTYPES_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextFormat::PageBreakFlag >() { return SbkPySide_QtGuiTypes[SBK_QTEXTFORMAT_PAGEBREAKFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextFormat::PageBreakFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QTEXTFORMAT_PAGEBREAKFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextFrameFormat::Position >() { return SbkPySide_QtGuiTypes[SBK_QTEXTFRAMEFORMAT_POSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextFrameFormat::BorderStyle >() { return SbkPySide_QtGuiTypes[SBK_QTEXTFRAMEFORMAT_BORDERSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextFrameFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTFRAMEFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextTableFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTTABLEFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextListFormat::Style >() { return SbkPySide_QtGuiTypes[SBK_QTEXTLISTFORMAT_STYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextListFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTLISTFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextBlockFormat::LineHeightTypes >() { return SbkPySide_QtGuiTypes[SBK_QTEXTBLOCKFORMAT_LINEHEIGHTTYPES_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextBlockFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTBLOCKFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextLength::Type >() { return SbkPySide_QtGuiTypes[SBK_QTEXTLENGTH_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextLength >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTLENGTH_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextOption::TabType >() { return SbkPySide_QtGuiTypes[SBK_QTEXTOPTION_TABTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextOption::WrapMode >() { return SbkPySide_QtGuiTypes[SBK_QTEXTOPTION_WRAPMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextOption::Flag >() { return SbkPySide_QtGuiTypes[SBK_QTEXTOPTION_FLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextOption::Flag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QTEXTOPTION_FLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextOption >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTOPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextOption::Tab >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTOPTION_TAB_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPen >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPEN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFontDatabase::WritingSystem >() { return SbkPySide_QtGuiTypes[SBK_QFONTDATABASE_WRITINGSYSTEM_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFontDatabase >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFONTDATABASE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOption::OptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTION_OPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOption::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTION_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOption::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTION_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOption >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItem::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEM_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItem::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEM_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItem::Position >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEM_POSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV2::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV2_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV2::ViewItemFeature >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV2_VIEWITEMFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyleOptionViewItemV2::ViewItemFeature> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLEOPTIONVIEWITEMV2_VIEWITEMFEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV3::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV3_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV3 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV3_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBar::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBAR_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBar::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBAR_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBar::ToolBarPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBAR_TOOLBARPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBar::ToolBarFeature >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBAR_TOOLBARFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyleOptionToolBar::ToolBarFeature> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLEOPTIONTOOLBAR_TOOLBARFEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTab::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTAB_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTab::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTAB_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTab::TabPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTAB_TABPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTab::SelectedPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTAB_SELECTEDPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTab::CornerWidget >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTAB_CORNERWIDGET_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyleOptionTab::CornerWidget> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLEOPTIONTAB_CORNERWIDGET__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTab >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTAB_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrame::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAME_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrame::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAME_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrame >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionButton::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONBUTTON_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionButton::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONBUTTON_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionButton::ButtonFeature >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONBUTTON_BUTTONFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyleOptionButton::ButtonFeature> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLEOPTIONBUTTON_BUTTONFEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionButton >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONBUTTON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabBarBase::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABBARBASE_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabBarBase::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABBARBASE_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabBarBase >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABBARBASE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabBarBaseV2::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABBARBASEV2_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabBarBaseV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABBARBASEV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionComplex::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONCOMPLEX_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionComplex::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONCOMPLEX_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionComplex >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONCOMPLEX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolButton::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBUTTON_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolButton::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBUTTON_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolButton::ToolButtonFeature >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBUTTON_TOOLBUTTONFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyleOptionToolButton::ToolButtonFeature> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLEOPTIONTOOLBUTTON_TOOLBUTTONFEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolButton >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBUTTON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSlider::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSLIDER_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSlider::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSLIDER_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSlider >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSLIDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSizeGrip::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSIZEGRIP_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSizeGrip::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSIZEGRIP_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSizeGrip >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSIZEGRIP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionGroupBox::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONGROUPBOX_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionGroupBox::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONGROUPBOX_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionGroupBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONGROUPBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTitleBar::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTITLEBAR_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTitleBar::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTITLEBAR_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTitleBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTITLEBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionComboBox::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONCOMBOBOX_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionComboBox::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONCOMBOBOX_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionComboBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONCOMBOBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionMenuItem::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONMENUITEM_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionMenuItem::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONMENUITEM_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionMenuItem::MenuItemType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONMENUITEM_MENUITEMTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionMenuItem::CheckType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONMENUITEM_CHECKTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionMenuItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONMENUITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionProgressBar::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONPROGRESSBAR_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionProgressBar::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONPROGRESSBAR_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionProgressBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONPROGRESSBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionProgressBarV2::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONPROGRESSBARV2_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionProgressBarV2::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONPROGRESSBARV2_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionProgressBarV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONPROGRESSBARV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionHeader::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONHEADER_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionHeader::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONHEADER_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionHeader::SectionPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONHEADER_SECTIONPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionHeader::SelectedPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONHEADER_SELECTEDPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionHeader::SortIndicator >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONHEADER_SORTINDICATOR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionHeader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONHEADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBox::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBOX_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBox::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBOX_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabWidgetFrame::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABWIDGETFRAME_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabWidgetFrame::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABWIDGETFRAME_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabWidgetFrame >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABWIDGETFRAME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionRubberBand::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONRUBBERBAND_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionRubberBand::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONRUBBERBAND_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionRubberBand >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONRUBBERBAND_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturn::HintReturnType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURN_HINTRETURNTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturn::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURN_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturn::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURN_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturn >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturnVariant::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURNVARIANT_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturnVariant::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURNVARIANT_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturnVariant >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURNVARIANT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturnMask::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURNMASK_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturnMask::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURNMASK_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleHintReturnMask >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEHINTRETURNMASK_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionGraphicsItem::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONGRAPHICSITEM_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionGraphicsItem::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONGRAPHICSITEM_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionGraphicsItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONGRAPHICSITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrameV2::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAMEV2_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrameV2::FrameFeature >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAMEV2_FRAMEFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyleOptionFrameV2::FrameFeature> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLEOPTIONFRAMEV2_FRAMEFEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrameV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAMEV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrameV3::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAMEV3_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFrameV3 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFRAMEV3_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSpinBox::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSPINBOX_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSpinBox::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSPINBOX_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionSpinBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONSPINBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBoxV2::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBOXV2_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBoxV2::TabPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBOXV2_TABPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBoxV2::SelectedPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBOXV2_SELECTEDPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionToolBoxV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTOOLBOXV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabV2::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABV2_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabV3::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABV3_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionTabV3 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONTABV3_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionDockWidget::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONDOCKWIDGET_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionDockWidget::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONDOCKWIDGET_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionDockWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONDOCKWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV4::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV4_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV4::ViewItemPosition >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV4_VIEWITEMPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionViewItemV4 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONVIEWITEMV4_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionDockWidgetV2::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONDOCKWIDGETV2_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionDockWidgetV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONDOCKWIDGETV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFocusRect::StyleOptionType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFOCUSRECT_STYLEOPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFocusRect::StyleOptionVersion >() { return SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFOCUSRECT_STYLEOPTIONVERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyleOptionFocusRect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEOPTIONFOCUSRECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QInputContextFactory >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QINPUTCONTEXTFACTORY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QToolTip >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTOOLTIP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWhatsThis >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWHATSTHIS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGestureRecognizer::ResultFlag >() { return SbkPySide_QtGuiTypes[SBK_QGESTURERECOGNIZER_RESULTFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGestureRecognizer::ResultFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QGESTURERECOGNIZER_RESULTFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGestureRecognizer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGESTURERECOGNIZER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFont::StyleHint >() { return SbkPySide_QtGuiTypes[SBK_QFONT_STYLEHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont::StyleStrategy >() { return SbkPySide_QtGuiTypes[SBK_QFONT_STYLESTRATEGY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont::HintingPreference >() { return SbkPySide_QtGuiTypes[SBK_QFONT_HINTINGPREFERENCE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont::Weight >() { return SbkPySide_QtGuiTypes[SBK_QFONT_WEIGHT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont::Style >() { return SbkPySide_QtGuiTypes[SBK_QFONT_STYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont::Stretch >() { return SbkPySide_QtGuiTypes[SBK_QFONT_STRETCH_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont::Capitalization >() { return SbkPySide_QtGuiTypes[SBK_QFONT_CAPITALIZATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont::SpacingType >() { return SbkPySide_QtGuiTypes[SBK_QFONT_SPACINGTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFont >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFONT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextCharFormat::VerticalAlignment >() { return SbkPySide_QtGuiTypes[SBK_QTEXTCHARFORMAT_VERTICALALIGNMENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextCharFormat::UnderlineStyle >() { return SbkPySide_QtGuiTypes[SBK_QTEXTCHARFORMAT_UNDERLINESTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextCharFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTCHARFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextTableCellFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTTABLECELLFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextImageFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTIMAGEFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFontMetrics >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFONTMETRICS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPalette::ColorGroup >() { return SbkPySide_QtGuiTypes[SBK_QPALETTE_COLORGROUP_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPalette::ColorRole >() { return SbkPySide_QtGuiTypes[SBK_QPALETTE_COLORROLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPalette >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPALETTE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGradient::Type >() { return SbkPySide_QtGuiTypes[SBK_QGRADIENT_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGradient::Spread >() { return SbkPySide_QtGuiTypes[SBK_QGRADIENT_SPREAD_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGradient::CoordinateMode >() { return SbkPySide_QtGuiTypes[SBK_QGRADIENT_COORDINATEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGradient::InterpolationMode >() { return SbkPySide_QtGuiTypes[SBK_QGRADIENT_INTERPOLATIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGradient >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRADIENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLinearGradient >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLINEARGRADIENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QConicalGradient >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCONICALGRADIENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRadialGradient >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QRADIALGRADIENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QBrush >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QBRUSH_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLayoutItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLAYOUTITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWidgetItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWIDGETITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCursor >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCURSOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSizePolicy::PolicyFlag >() { return SbkPySide_QtGuiTypes[SBK_QSIZEPOLICY_POLICYFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSizePolicy::Policy >() { return SbkPySide_QtGuiTypes[SBK_QSIZEPOLICY_POLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSizePolicy::ControlType >() { return SbkPySide_QtGuiTypes[SBK_QSIZEPOLICY_CONTROLTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QSizePolicy::ControlType> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSIZEPOLICY_CONTROLTYPE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QSizePolicy >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSIZEPOLICY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSpacerItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSPACERITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFontInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFONTINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFontMetricsF >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFONTMETRICSF_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPolygonF >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPOLYGONF_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPolygon >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPOLYGON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPaintDevice::PaintDeviceMetric >() { return SbkPySide_QtGuiTypes[SBK_QPAINTDEVICE_PAINTDEVICEMETRIC_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPaintDevice >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTDEVICE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPicture >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPICTURE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPrinter::PrinterMode >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_PRINTERMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::Orientation >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_ORIENTATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::PageSize >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_PAGESIZE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::PageOrder >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_PAGEORDER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::ColorMode >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_COLORMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::PaperSource >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_PAPERSOURCE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::PrinterState >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_PRINTERSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::OutputFormat >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_OUTPUTFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::PrintRange >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_PRINTRANGE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::Unit >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_UNIT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter::DuplexMode >() { return SbkPySide_QtGuiTypes[SBK_QPRINTER_DUPLEXMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrinter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPRINTER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QKeySequence::StandardKey >() { return SbkPySide_QtGuiTypes[SBK_QKEYSEQUENCE_STANDARDKEY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QKeySequence::SequenceFormat >() { return SbkPySide_QtGuiTypes[SBK_QKEYSEQUENCE_SEQUENCEFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QKeySequence::SequenceMatch >() { return SbkPySide_QtGuiTypes[SBK_QKEYSEQUENCE_SEQUENCEMATCH_IDX]; }
template<> inline PyTypeObject* SbkType< ::QKeySequence >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QKEYSEQUENCE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QColor::Spec >() { return SbkPySide_QtGuiTypes[SBK_QCOLOR_SPEC_IDX]; }
template<> inline PyTypeObject* SbkType< ::QColor >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCOLOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPainterPathStroker >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTERPATHSTROKER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTransform::TransformationType >() { return SbkPySide_QtGuiTypes[SBK_QTRANSFORM_TRANSFORMATIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTransform >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTRANSFORM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMatrix >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMATRIX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPainterPath::ElementType >() { return SbkPySide_QtGuiTypes[SBK_QPAINTERPATH_ELEMENTTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPainterPath >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTERPATH_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPainterPath::Element >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTERPATH_ELEMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsLayoutItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSLAYOUTITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsAnchorLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSANCHORLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsGridLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSGRIDLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsLinearLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSLINEARLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextLayout::CursorMode >() { return SbkPySide_QtGuiTypes[SBK_QTEXTLAYOUT_CURSORMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextLayout::FormatRange >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTLAYOUT_FORMATRANGE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPixmap::HBitmapFormat >() { return SbkPySide_QtGuiTypes[SBK_QPIXMAP_HBITMAPFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPixmap >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPIXMAP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QImage::InvertMode >() { return SbkPySide_QtGuiTypes[SBK_QIMAGE_INVERTMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QImage::Format >() { return SbkPySide_QtGuiTypes[SBK_QIMAGE_FORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QImage >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QIMAGE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QBitmap >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QBITMAP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QIcon::Mode >() { return SbkPySide_QtGuiTypes[SBK_QICON_MODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QIcon::State >() { return SbkPySide_QtGuiTypes[SBK_QICON_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QIcon >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QICON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QIconEngineV2::IconEngineHook >() { return SbkPySide_QtGuiTypes[SBK_QICONENGINEV2_ICONENGINEHOOK_IDX]; }
template<> inline PyTypeObject* SbkType< ::QIconEngineV2 >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QICONENGINEV2_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsItem::GraphicsItemFlag >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEM_GRAPHICSITEMFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGraphicsItem::GraphicsItemFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QGRAPHICSITEM_GRAPHICSITEMFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsItem::GraphicsItemChange >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEM_GRAPHICSITEMCHANGE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsItem::CacheMode >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEM_CACHEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsItem::PanelModality >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEM_PANELMODALITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::PySide_QtGui_QGraphicsItem_Extension_Surrogate >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEM_EXTENSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsItemGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEMGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsLineItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSLINEITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractGraphicsShapeItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTGRAPHICSSHAPEITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSimpleTextItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSIMPLETEXTITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsPathItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSPATHITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsEllipseItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSELLIPSEITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsRectItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSRECTITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsPolygonItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSPOLYGONITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsPixmapItem::ShapeMode >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSPIXMAPITEM_SHAPEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsPixmapItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSPIXMAPITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPainter::RenderHint >() { return SbkPySide_QtGuiTypes[SBK_QPAINTER_RENDERHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QPainter::RenderHint> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QPAINTER_RENDERHINT__IDX]; }
template<> inline PyTypeObject* SbkType< ::QPainter::PixmapFragmentHint >() { return SbkPySide_QtGuiTypes[SBK_QPAINTER_PIXMAPFRAGMENTHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QPainter::PixmapFragmentHint> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QPAINTER_PIXMAPFRAGMENTHINT__IDX]; }
template<> inline PyTypeObject* SbkType< ::QPainter::CompositionMode >() { return SbkPySide_QtGuiTypes[SBK_QPAINTER_COMPOSITIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPainter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPainter::PixmapFragment >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTER_PIXMAPFRAGMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStylePainter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEPAINTER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDropEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDROPEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDragMoveEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDRAGMOVEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDragEnterEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDRAGENTEREVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QInputMethodEvent::AttributeType >() { return SbkPySide_QtGuiTypes[SBK_QINPUTMETHODEVENT_ATTRIBUTETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QInputMethodEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QINPUTMETHODEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QInputMethodEvent::Attribute >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QINPUTMETHODEVENT_ATTRIBUTE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QResizeEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QRESIZEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QIconDragEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QICONDRAGEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHideEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QHIDEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QShowEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSHOWEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMoveEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMOVEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneDragDropEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENEDRAGDROPEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneResizeEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENERESIZEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneHoverEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENEHOVEREVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneMouseEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENEMOUSEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneContextMenuEvent::Reason >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENECONTEXTMENUEVENT_REASON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneContextMenuEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENECONTEXTMENUEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneMoveEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENEMOVEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneWheelEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENEWHEELEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSceneHelpEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENEHELPEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCloseEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCLOSEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPaintEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAINTEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFocusEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFOCUSEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHoverEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QHOVEREVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAccessibleEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QACCESSIBLEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QInputEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QINPUTEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWheelEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWHEELEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QContextMenuEvent::Reason >() { return SbkPySide_QtGuiTypes[SBK_QCONTEXTMENUEVENT_REASON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QContextMenuEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCONTEXTMENUEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMouseEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMOUSEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTouchEvent::DeviceType >() { return SbkPySide_QtGuiTypes[SBK_QTOUCHEVENT_DEVICETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTouchEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTOUCHEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTouchEvent::TouchPoint >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTOUCHEVENT_TOUCHPOINT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QKeyEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QKEYEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTabletEvent::TabletDevice >() { return SbkPySide_QtGuiTypes[SBK_QTABLETEVENT_TABLETDEVICE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTabletEvent::PointerType >() { return SbkPySide_QtGuiTypes[SBK_QTABLETEVENT_POINTERTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTabletEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTABLETEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGestureEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGESTUREEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWindowStateChangeEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWINDOWSTATECHANGEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QClipboardEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCLIPBOARDEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStatusTipEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTATUSTIPEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QActionEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QACTIONEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFileOpenEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFILEOPENEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QShortcutEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSHORTCUTEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWhatsThisClickedEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWHATSTHISCLICKEDEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QToolBarChangeEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTOOLBARCHANGEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QHELPEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDragLeaveEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDRAGLEAVEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRegion::RegionType >() { return SbkPySide_QtGuiTypes[SBK_QREGION_REGIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QRegion >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QREGION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWidget::RenderFlag >() { return SbkPySide_QtGuiTypes[SBK_QWIDGET_RENDERFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QWidget::RenderFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QWIDGET_RENDERFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWizardPage >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWIZARDPAGE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDialog::DialogCode >() { return SbkPySide_QtGuiTypes[SBK_QDIALOG_DIALOGCODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractPrintDialog::PrintRange >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTPRINTDIALOG_PRINTRANGE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractPrintDialog::PrintDialogOption >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTPRINTDIALOG_PRINTDIALOGOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QAbstractPrintDialog::PrintDialogOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QABSTRACTPRINTDIALOG_PRINTDIALOGOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractPrintDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTPRINTDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPrintDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPRINTDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QProgressDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPROGRESSDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractPageSetupDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTPAGESETUPDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPageSetupDialog::PageSetupDialogOption >() { return SbkPySide_QtGuiTypes[SBK_QPAGESETUPDIALOG_PAGESETUPDIALOGOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QPageSetupDialog::PageSetupDialogOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QPAGESETUPDIALOG_PAGESETUPDIALOGOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QPageSetupDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPAGESETUPDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWizard::WizardButton >() { return SbkPySide_QtGuiTypes[SBK_QWIZARD_WIZARDBUTTON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWizard::WizardPixmap >() { return SbkPySide_QtGuiTypes[SBK_QWIZARD_WIZARDPIXMAP_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWizard::WizardStyle >() { return SbkPySide_QtGuiTypes[SBK_QWIZARD_WIZARDSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWizard::WizardOption >() { return SbkPySide_QtGuiTypes[SBK_QWIZARD_WIZARDOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QWizard::WizardOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QWIZARD_WIZARDOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QWizard >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWIZARD_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFontDialog::FontDialogOption >() { return SbkPySide_QtGuiTypes[SBK_QFONTDIALOG_FONTDIALOGOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QFontDialog::FontDialogOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QFONTDIALOG_FONTDIALOGOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QFontDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFONTDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFileDialog::ViewMode >() { return SbkPySide_QtGuiTypes[SBK_QFILEDIALOG_VIEWMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFileDialog::FileMode >() { return SbkPySide_QtGuiTypes[SBK_QFILEDIALOG_FILEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFileDialog::AcceptMode >() { return SbkPySide_QtGuiTypes[SBK_QFILEDIALOG_ACCEPTMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFileDialog::DialogLabel >() { return SbkPySide_QtGuiTypes[SBK_QFILEDIALOG_DIALOGLABEL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFileDialog::Option >() { return SbkPySide_QtGuiTypes[SBK_QFILEDIALOG_OPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QFileDialog::Option> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QFILEDIALOG_OPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QFileDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFILEDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QErrorMessage >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QERRORMESSAGE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPrintPreviewDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPRINTPREVIEWDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMessageBox::Icon >() { return SbkPySide_QtGuiTypes[SBK_QMESSAGEBOX_ICON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMessageBox::ButtonRole >() { return SbkPySide_QtGuiTypes[SBK_QMESSAGEBOX_BUTTONROLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMessageBox::StandardButton >() { return SbkPySide_QtGuiTypes[SBK_QMESSAGEBOX_STANDARDBUTTON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QMessageBox::StandardButton> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QMESSAGEBOX_STANDARDBUTTON__IDX]; }
template<> inline PyTypeObject* SbkType< ::QMessageBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMESSAGEBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QColorDialog::ColorDialogOption >() { return SbkPySide_QtGuiTypes[SBK_QCOLORDIALOG_COLORDIALOGOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QColorDialog::ColorDialogOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QCOLORDIALOG_COLORDIALOGOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QColorDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCOLORDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWorkspace::WindowOrder >() { return SbkPySide_QtGuiTypes[SBK_QWORKSPACE_WINDOWORDER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWorkspace >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWORKSPACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStatusBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTATUSBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRubberBand::Shape >() { return SbkPySide_QtGuiTypes[SBK_QRUBBERBAND_SHAPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QRubberBand >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QRUBBERBAND_IDX]); }
template<> inline PyTypeObject* SbkType< ::QToolBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTOOLBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSplitterHandle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSPLITTERHANDLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTabWidget::TabPosition >() { return SbkPySide_QtGuiTypes[SBK_QTABWIDGET_TABPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTabWidget::TabShape >() { return SbkPySide_QtGuiTypes[SBK_QTABWIDGET_TABSHAPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTabWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTABWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSplashScreen >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSPLASHSCREEN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTabBar::Shape >() { return SbkPySide_QtGuiTypes[SBK_QTABBAR_SHAPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTabBar::ButtonPosition >() { return SbkPySide_QtGuiTypes[SBK_QTABBAR_BUTTONPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTabBar::SelectionBehavior >() { return SbkPySide_QtGuiTypes[SBK_QTABBAR_SELECTIONBEHAVIOR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTabBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTABBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSizeGrip >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSIZEGRIP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractSlider::SliderAction >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTSLIDER_SLIDERACTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::PySide_QtGui_QAbstractSlider_SliderChange_Surrogate >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTSLIDER_SLIDERCHANGE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSlider >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTSLIDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QProgressBar::Direction >() { return SbkPySide_QtGuiTypes[SBK_QPROGRESSBAR_DIRECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QProgressBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPROGRESSBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFrame::Shape >() { return SbkPySide_QtGuiTypes[SBK_QFRAME_SHAPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFrame::Shadow >() { return SbkPySide_QtGuiTypes[SBK_QFRAME_SHADOW_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFrame::StyleMask >() { return SbkPySide_QtGuiTypes[SBK_QFRAME_STYLEMASK_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFrame >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFRAME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStackedWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTACKEDWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractScrollArea >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTSCROLLAREA_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSplitter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSPLITTER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QToolBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTOOLBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScrollArea >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSCROLLAREA_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractButton >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTBUTTON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QToolButton::ToolButtonPopupMode >() { return SbkPySide_QtGuiTypes[SBK_QTOOLBUTTON_TOOLBUTTONPOPUPMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QToolButton >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTOOLBUTTON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRadioButton >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QRADIOBUTTON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPrintPreviewWidget::ViewMode >() { return SbkPySide_QtGuiTypes[SBK_QPRINTPREVIEWWIDGET_VIEWMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrintPreviewWidget::ZoomMode >() { return SbkPySide_QtGuiTypes[SBK_QPRINTPREVIEWWIDGET_ZOOMMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPrintPreviewWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPRINTPREVIEWWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScrollBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSCROLLBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPlainTextEdit::LineWrapMode >() { return SbkPySide_QtGuiTypes[SBK_QPLAINTEXTEDIT_LINEWRAPMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QPlainTextEdit >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPLAINTEXTEDIT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextEdit::LineWrapMode >() { return SbkPySide_QtGuiTypes[SBK_QTEXTEDIT_LINEWRAPMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextEdit::AutoFormattingFlag >() { return SbkPySide_QtGuiTypes[SBK_QTEXTEDIT_AUTOFORMATTINGFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextEdit::AutoFormattingFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QTEXTEDIT_AUTOFORMATTINGFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextEdit >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTEDIT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextEdit::ExtraSelection >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTEDIT_EXTRASELECTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextBrowser >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTBROWSER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMenuBar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMENUBAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMenu >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMENU_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMdiSubWindow::SubWindowOption >() { return SbkPySide_QtGuiTypes[SBK_QMDISUBWINDOW_SUBWINDOWOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QMdiSubWindow::SubWindowOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QMDISUBWINDOW_SUBWINDOWOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QMdiSubWindow >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMDISUBWINDOW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMainWindow::DockOption >() { return SbkPySide_QtGuiTypes[SBK_QMAINWINDOW_DOCKOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QMainWindow::DockOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QMAINWINDOW_DOCKOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QMainWindow >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMAINWINDOW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMdiArea::AreaOption >() { return SbkPySide_QtGuiTypes[SBK_QMDIAREA_AREAOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QMdiArea::AreaOption> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QMDIAREA_AREAOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QMdiArea::WindowOrder >() { return SbkPySide_QtGuiTypes[SBK_QMDIAREA_WINDOWORDER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMdiArea::ViewMode >() { return SbkPySide_QtGuiTypes[SBK_QMDIAREA_VIEWMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMdiArea >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMDIAREA_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLineEdit::EchoMode >() { return SbkPySide_QtGuiTypes[SBK_QLINEEDIT_ECHOMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLineEdit >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLINEEDIT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QInputDialog::InputDialogOption >() { return SbkPySide_QtGuiTypes[SBK_QINPUTDIALOG_INPUTDIALOGOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QInputDialog::InputMode >() { return SbkPySide_QtGuiTypes[SBK_QINPUTDIALOG_INPUTMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QInputDialog >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QINPUTDIALOG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDesktopWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDESKTOPWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractItemView::SelectionMode >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_SELECTIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractItemView::SelectionBehavior >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_SELECTIONBEHAVIOR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractItemView::ScrollHint >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_SCROLLHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractItemView::EditTrigger >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_EDITTRIGGER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QAbstractItemView::EditTrigger> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QABSTRACTITEMVIEW_EDITTRIGGER__IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractItemView::ScrollMode >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_SCROLLMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractItemView::DragDropMode >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_DRAGDROPMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::PySide_QtGui_QAbstractItemView_CursorAction_Surrogate >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_CURSORACTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::PySide_QtGui_QAbstractItemView_State_Surrogate >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::PySide_QtGui_QAbstractItemView_DropIndicatorPosition_Surrogate >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_DROPINDICATORPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractItemView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTreeView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTREEVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTreeWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTREEWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QColumnView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCOLUMNVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QListView::Movement >() { return SbkPySide_QtGuiTypes[SBK_QLISTVIEW_MOVEMENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QListView::Flow >() { return SbkPySide_QtGuiTypes[SBK_QLISTVIEW_FLOW_IDX]; }
template<> inline PyTypeObject* SbkType< ::QListView::ResizeMode >() { return SbkPySide_QtGuiTypes[SBK_QLISTVIEW_RESIZEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QListView::LayoutMode >() { return SbkPySide_QtGuiTypes[SBK_QLISTVIEW_LAYOUTMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QListView::ViewMode >() { return SbkPySide_QtGuiTypes[SBK_QLISTVIEW_VIEWMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QListView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLISTVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QListWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLISTWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTableView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTABLEVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTableWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTABLEWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHeaderView::ResizeMode >() { return SbkPySide_QtGuiTypes[SBK_QHEADERVIEW_RESIZEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHeaderView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QHEADERVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCalendarWidget::HorizontalHeaderFormat >() { return SbkPySide_QtGuiTypes[SBK_QCALENDARWIDGET_HORIZONTALHEADERFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QCalendarWidget::VerticalHeaderFormat >() { return SbkPySide_QtGuiTypes[SBK_QCALENDARWIDGET_VERTICALHEADERFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QCalendarWidget::SelectionMode >() { return SbkPySide_QtGuiTypes[SBK_QCALENDARWIDGET_SELECTIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QCalendarWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCALENDARWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSlider::TickPosition >() { return SbkPySide_QtGuiTypes[SBK_QSLIDER_TICKPOSITION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSlider >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSLIDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCheckBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCHECKBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractSpinBox::StepEnabledFlag >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTSPINBOX_STEPENABLEDFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QAbstractSpinBox::StepEnabledFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QABSTRACTSPINBOX_STEPENABLEDFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSpinBox::ButtonSymbols >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTSPINBOX_BUTTONSYMBOLS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSpinBox::CorrectionMode >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTSPINBOX_CORRECTIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSpinBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTSPINBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDoubleSpinBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDOUBLESPINBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSpinBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSPINBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUndoView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QUNDOVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLCDNumber::Mode >() { return SbkPySide_QtGuiTypes[SBK_QLCDNUMBER_MODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLCDNumber::SegmentStyle >() { return SbkPySide_QtGuiTypes[SBK_QLCDNUMBER_SEGMENTSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLCDNumber >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLCDNUMBER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLabel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLABEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGroupBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGROUPBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDockWidget::DockWidgetFeature >() { return SbkPySide_QtGuiTypes[SBK_QDOCKWIDGET_DOCKWIDGETFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QDockWidget::DockWidgetFeature> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QDOCKWIDGET_DOCKWIDGETFEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::QDockWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDOCKWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFocusFrame >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFOCUSFRAME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDialogButtonBox::ButtonRole >() { return SbkPySide_QtGuiTypes[SBK_QDIALOGBUTTONBOX_BUTTONROLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDialogButtonBox::StandardButton >() { return SbkPySide_QtGuiTypes[SBK_QDIALOGBUTTONBOX_STANDARDBUTTON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QDialogButtonBox::StandardButton> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QDIALOGBUTTONBOX_STANDARDBUTTON__IDX]; }
template<> inline PyTypeObject* SbkType< ::QDialogButtonBox::ButtonLayout >() { return SbkPySide_QtGuiTypes[SBK_QDIALOGBUTTONBOX_BUTTONLAYOUT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDialogButtonBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDIALOGBUTTONBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPushButton >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPUSHBUTTON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDial >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDIAL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCommandLinkButton >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCOMMANDLINKBUTTON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDateTimeEdit::Section >() { return SbkPySide_QtGuiTypes[SBK_QDATETIMEEDIT_SECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QDateTimeEdit::Section> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QDATETIMEEDIT_SECTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QDateTimeEdit >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDATETIMEEDIT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTimeEdit >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTIMEEDIT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDateEdit >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDATEEDIT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QComboBox::InsertPolicy >() { return SbkPySide_QtGuiTypes[SBK_QCOMBOBOX_INSERTPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QComboBox::SizeAdjustPolicy >() { return SbkPySide_QtGuiTypes[SBK_QCOMBOBOX_SIZEADJUSTPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QComboBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCOMBOBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFontComboBox::FontFilter >() { return SbkPySide_QtGuiTypes[SBK_QFONTCOMBOBOX_FONTFILTER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QFontComboBox::FontFilter> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QFONTCOMBOBOX_FONTFILTER__IDX]; }
template<> inline PyTypeObject* SbkType< ::QFontComboBox >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFONTCOMBOBOX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUndoStack >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QUNDOSTACK_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUndoGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QUNDOGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractItemDelegate::EndEditHint >() { return SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMDELEGATE_ENDEDITHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractItemDelegate >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTITEMDELEGATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QItemDelegate >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QITEMDELEGATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyledItemDelegate >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLEDITEMDELEGATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSystemTrayIcon::ActivationReason >() { return SbkPySide_QtGuiTypes[SBK_QSYSTEMTRAYICON_ACTIVATIONREASON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSystemTrayIcon::MessageIcon >() { return SbkPySide_QtGuiTypes[SBK_QSYSTEMTRAYICON_MESSAGEICON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSystemTrayIcon >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSYSTEMTRAYICON_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPyTextObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPYTEXTOBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCompleter::CompletionMode >() { return SbkPySide_QtGuiTypes[SBK_QCOMPLETER_COMPLETIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QCompleter::ModelSorting >() { return SbkPySide_QtGuiTypes[SBK_QCOMPLETER_MODELSORTING_IDX]; }
template<> inline PyTypeObject* SbkType< ::QCompleter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCOMPLETER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsEffect::ChangeFlag >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSEFFECT_CHANGEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGraphicsEffect::ChangeFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QGRAPHICSEFFECT_CHANGEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsEffect::PixmapPadMode >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSEFFECT_PIXMAPPADMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsEffect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSEFFECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsColorizeEffect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSCOLORIZEEFFECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsBlurEffect::BlurHint >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSBLUREFFECT_BLURHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGraphicsBlurEffect::BlurHint> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QGRAPHICSBLUREFFECT_BLURHINT__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsBlurEffect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSBLUREFFECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsOpacityEffect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSOPACITYEFFECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsDropShadowEffect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSDROPSHADOWEFFECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSyntaxHighlighter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSYNTAXHIGHLIGHTER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDataWidgetMapper::SubmitPolicy >() { return SbkPySide_QtGuiTypes[SBK_QDATAWIDGETMAPPER_SUBMITPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDataWidgetMapper >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDATAWIDGETMAPPER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QItemSelectionModel::SelectionFlag >() { return SbkPySide_QtGuiTypes[SBK_QITEMSELECTIONMODEL_SELECTIONFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QItemSelectionModel::SelectionFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QITEMSELECTIONMODEL_SELECTIONFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QItemSelectionModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QITEMSELECTIONMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTOBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextBlockGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTBLOCKGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextList >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTLIST_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextFrame >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTFRAME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextFrame::iterator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTFRAME_ITERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextTable >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTTABLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDrag >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDRAG_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsScene::ItemIndexMethod >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENE_ITEMINDEXMETHOD_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsScene::SceneLayer >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENE_SCENELAYER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGraphicsScene::SceneLayer> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QGRAPHICSSCENE_SCENELAYER__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsScene >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCENE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsView::ViewportAnchor >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSVIEW_VIEWPORTANCHOR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsView::CacheModeFlag >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSVIEW_CACHEMODEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGraphicsView::CacheModeFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QGRAPHICSVIEW_CACHEMODEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsView::DragMode >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSVIEW_DRAGMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsView::ViewportUpdateMode >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSVIEW_VIEWPORTUPDATEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsView::OptimizationFlag >() { return SbkPySide_QtGuiTypes[SBK_QGRAPHICSVIEW_OPTIMIZATIONFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGraphicsView::OptimizationFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QGRAPHICSVIEW_OPTIMIZATIONFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGraphicsView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QClipboard::Mode >() { return SbkPySide_QtGuiTypes[SBK_QCLIPBOARD_MODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QClipboard >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCLIPBOARD_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStyle::StateFlag >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_STATEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyle::StateFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLE_STATEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::PrimitiveElement >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_PRIMITIVEELEMENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::ControlElement >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_CONTROLELEMENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::SubElement >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_SUBELEMENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::ComplexControl >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_COMPLEXCONTROL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::SubControl >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_SUBCONTROL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QStyle::SubControl> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QSTYLE_SUBCONTROL__IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::PixelMetric >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_PIXELMETRIC_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::ContentsType >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_CONTENTSTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::RequestSoftwareInputPanel >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_REQUESTSOFTWAREINPUTPANEL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::StyleHint >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_STYLEHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle::StandardPixmap >() { return SbkPySide_QtGuiTypes[SBK_QSTYLE_STANDARDPIXMAP_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStyle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTYLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCommonStyle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCOMMONSTYLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWindowsStyle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWINDOWSSTYLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPlastiqueStyle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPLASTIQUESTYLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCleanlooksStyle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCLEANLOOKSSTYLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMotifStyle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMOTIFSTYLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCDEStyle >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QCDESTYLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QButtonGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QBUTTONGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSOBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsProxyWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSPROXYWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsTextItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSTEXTITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QValidator::State >() { return SbkPySide_QtGuiTypes[SBK_QVALIDATOR_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QValidator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QVALIDATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDoubleValidator::Notation >() { return SbkPySide_QtGuiTypes[SBK_QDOUBLEVALIDATOR_NOTATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDoubleValidator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDOUBLEVALIDATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRegExpValidator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QREGEXPVALIDATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QIntValidator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QINTVALIDATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsTransform >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSTRANSFORM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsScale >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSSCALE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsRotation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSROTATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSound >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSOUND_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStandardItemModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTANDARDITEMMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStringListModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTRINGLISTMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QProxyModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPROXYMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractProxyModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTPROXYMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSortFilterProxyModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSORTFILTERPROXYMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDirModel::Roles >() { return SbkPySide_QtGuiTypes[SBK_QDIRMODEL_ROLES_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDirModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QDIRMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFileSystemModel::Roles >() { return SbkPySide_QtGuiTypes[SBK_QFILESYSTEMMODEL_ROLES_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFileSystemModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFILESYSTEMMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QInputContext::StandardFormat >() { return SbkPySide_QtGuiTypes[SBK_QINPUTCONTEXT_STANDARDFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QInputContext >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QINPUTCONTEXT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMouseEventTransition >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMOUSEEVENTTRANSITION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QKeyEventTransition >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QKEYEVENTTRANSITION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsItemAnimation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSITEMANIMATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractTextDocumentLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTTEXTDOCUMENTLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPlainTextDocumentLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPLAINTEXTDOCUMENTLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractTextDocumentLayout::Selection >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTTEXTDOCUMENTLAYOUT_SELECTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractTextDocumentLayout::PaintContext >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QABSTRACTTEXTDOCUMENTLAYOUT_PAINTCONTEXT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QShortcut >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSHORTCUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLayout::SizeConstraint >() { return SbkPySide_QtGuiTypes[SBK_QLAYOUT_SIZECONSTRAINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStackedLayout::StackingMode >() { return SbkPySide_QtGuiTypes[SBK_QSTACKEDLAYOUT_STACKINGMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStackedLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSTACKEDLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFormLayout::FieldGrowthPolicy >() { return SbkPySide_QtGuiTypes[SBK_QFORMLAYOUT_FIELDGROWTHPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFormLayout::RowWrapPolicy >() { return SbkPySide_QtGuiTypes[SBK_QFORMLAYOUT_ROWWRAPPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFormLayout::ItemRole >() { return SbkPySide_QtGuiTypes[SBK_QFORMLAYOUT_ITEMROLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFormLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QFORMLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QBoxLayout::Direction >() { return SbkPySide_QtGuiTypes[SBK_QBOXLAYOUT_DIRECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QBoxLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QBOXLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QVBoxLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QVBOXLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHBoxLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QHBOXLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGridLayout >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRIDLAYOUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSessionManager::RestartHint >() { return SbkPySide_QtGuiTypes[SBK_QSESSIONMANAGER_RESTARTHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSessionManager >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSESSIONMANAGER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QActionGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QACTIONGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsAnchor >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGRAPHICSANCHOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAction::MenuRole >() { return SbkPySide_QtGuiTypes[SBK_QACTION_MENUROLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAction::SoftKeyRole >() { return SbkPySide_QtGuiTypes[SBK_QACTION_SOFTKEYROLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAction::Priority >() { return SbkPySide_QtGuiTypes[SBK_QACTION_PRIORITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAction::ActionEvent >() { return SbkPySide_QtGuiTypes[SBK_QACTION_ACTIONEVENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAction >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QACTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWidgetAction >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QWIDGETACTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGesture::GestureCancelPolicy >() { return SbkPySide_QtGuiTypes[SBK_QGESTURE_GESTURECANCELPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGesture >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QGESTURE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPinchGesture::ChangeFlag >() { return SbkPySide_QtGuiTypes[SBK_QPINCHGESTURE_CHANGEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QPinchGesture::ChangeFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QPINCHGESTURE_CHANGEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QPinchGesture >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPINCHGESTURE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPanGesture >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QPANGESTURE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTapGesture >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTAPGESTURE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSwipeGesture::SwipeDirection >() { return SbkPySide_QtGuiTypes[SBK_QSWIPEGESTURE_SWIPEDIRECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSwipeGesture >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QSWIPEGESTURE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTapAndHoldGesture >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTAPANDHOLDGESTURE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QApplication::Type >() { return SbkPySide_QtGuiTypes[SBK_QAPPLICATION_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QApplication::ColorSpec >() { return SbkPySide_QtGuiTypes[SBK_QAPPLICATION_COLORSPEC_IDX]; }
template<> inline PyTypeObject* SbkType< ::QApplication >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QAPPLICATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMovie::MovieState >() { return SbkPySide_QtGuiTypes[SBK_QMOVIE_MOVIESTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMovie::CacheMode >() { return SbkPySide_QtGuiTypes[SBK_QMOVIE_CACHEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMovie >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QMOVIE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QImageWriter::ImageWriterError >() { return SbkPySide_QtGuiTypes[SBK_QIMAGEWRITER_IMAGEWRITERERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QImageWriter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QIMAGEWRITER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QImageReader::ImageReaderError >() { return SbkPySide_QtGuiTypes[SBK_QIMAGEREADER_IMAGEREADERERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QImageReader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QIMAGEREADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextDocument::MetaInformation >() { return SbkPySide_QtGuiTypes[SBK_QTEXTDOCUMENT_METAINFORMATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextDocument::FindFlag >() { return SbkPySide_QtGuiTypes[SBK_QTEXTDOCUMENT_FINDFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextDocument::FindFlag> >() { return SbkPySide_QtGuiTypes[SBK_QFLAGS_QTEXTDOCUMENT_FINDFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextDocument::ResourceType >() { return SbkPySide_QtGuiTypes[SBK_QTEXTDOCUMENT_RESOURCETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextDocument::Stacks >() { return SbkPySide_QtGuiTypes[SBK_QTEXTDOCUMENT_STACKS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextDocument >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtGuiTypes[SBK_QTEXTDOCUMENT_IDX]); }

} // namespace Shiboken

#endif // SBK_QTGUI_PYTHON_H


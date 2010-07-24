#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import pygtk
pygtk.require("2.0")
import gtk
import gobject
import pygphotoshot as pyshot
import gphotoparser as poc

gphoto2shootcommand = "gphoto2 --capture-image-and-download"


class TemplateCombo():
    def __init__(self,label="choice",choices=[]):
        self.widbuilder = gtk.Builder()
        self.widbuilder.add_from_file('ui/ChoiceWidget.xml')
        self.pureWidget = self.widbuilder.get_object('ChoiceWidget')
        
        self.label = self.widbuilder.get_object('selectLabel')
        self.label.set_text(label)
        self.combo = self.widbuilder.get_object('selectComboChoices')
        self.comboModel = gtk.ListStore(gobject.TYPE_STRING)
        for choice in choices:
            self.comboModel.append([choice])
        self.combo.set_model(self.comboModel)
        cell = gtk.CellRendererText()
        self.combo.pack_start(cell, True)
        self.combo.add_attribute(cell, 'text',0)
        self.pureWidget.child_set_property(self.combo,"expand",False)
        self.pureWidget.child_set_property(self.label,"expand",False)
    def getWidget(self):
        return self.pureWidget
    def getCombo(self):
        return self.combo

class ParamCombo():
    def __init__(self,param):
        self.myparam = param
        self.mycombp = TemplateCombo(param['label'],param['choices'].values())
        #self.reversemap = dict ([(v,k) for (k,v) in self.myparam['choices']])

        self.mycombp.getCombo().set_active(self.myparam['choices'].values().index(self.myparam['current']))
        
    def getWidget(self):
        return self.mycombp.getWidget()

        
class monprogramme:
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
    
    def __init__(self,inputdata):
        self.builder = gtk.Builder()
        self.builder.add_from_file('ui/pygphotoshot.xml')
#,"window1")
        self.window = self.builder.get_object('window1')
        self.hpaned = self.builder.get_object('hpaned1')
        self.vbox = self.builder.get_object('vbox2')
        self.subsections = gtk.Notebook()
        self.vbox.add(self.subsections)
        self.vbox.reorder_child(self.subsections,0)

#        f = open('eos.txt')
        self.params = poc.parseParams(inputdata)
#        f.close()
        poc.displaylevel(self.params)
        sectionCnt,levels = poc.extractSubsections(self.params)
        self.places={}
        for item in levels['main']:
            
            label = gtk.Label("_%s%s"%(item[0].upper(),item[1:]))
            label.set_use_underline(True)
            frame = gtk.Frame(item)
            cnt = len(self.params['main'][item])
            self.places[item]=gtk.VBox(1,cnt+2) #+1 because we want to pack widgets
            pos = 0
            for param in self.params['main'][item]:
                
                if self.params['main'][item][param]['type']=='TOGGLE':
                    widget = gtk.CheckButton(self.params['main'][item][param]['label'])
                    widget.show()
                    self.places[item].add(widget)#,0,1,pos,pos+1)
                elif self.params['main'][item][param]['type']=='TEXT':
                    widget = gtk.Label("%s:%s"%(self.params['main'][item][param]['label'],self.params['main'][item][param]['current']))
                    widget.show()
                    self.places[item].add(widget)#,0,1,pos,pos+1)
                elif self.params['main'][item][param]['type']=='RADIO':
                    print self.params['main'][item][param]['label'], self.params['main'][item][param]['choices'].values()

                    widget = ParamCombo(self.params['main'][item][param]).getWidget()
                    self.places[item].add(widget)#,0,1,pos,pos+1)
                self.places[item].child_set_property(widget,"expand",True)
                self.places[item].child_set_property(widget,"fill",False)
                self.places[item].child_set_property(widget,"pack-type",gtk.PACK_START)
                pos = pos + 1
            self.places[item].show()
            frame.add(self.places[item])

            frame.show()
            label.show()
            self.subsections.append_page(frame,label)


        self.image = gtk.Image()
        self.image.set_from_stock(gtk.STOCK_MISSING_IMAGE,gtk.ICON_SIZE_LARGE_TOOLBAR)
        self.image.show()
        self.scrolled = gtk.ScrolledWindow()

        self.scrolled.add_with_viewport(self.image)
        self.scrolled.show()
        self.hpaned.add2(self.scrolled)
        self.subsections.show()
        
        
        #mycombo = TemplateCombo('test',[ "label %d"%a for a in range(0,10)])
        #table = self.builder.get_object('table1')
        #table.attach(mycombo.getWidget(),0,4,2,3)
        
        self.builder.connect_signals(self)

    
        
    def delete(self, source=None, event=None):
	gtk.main_quit()

    def on_takeShot_clicked(self, widget):
        filename = pyshot.takePhoto()
        self.image.set_from_file(filename)


       
if __name__ == '__main__':
    #f = open('eos.txt')
    #app = monprogramme(f)
    #f.close()
    data = pyshot.getCameraInfos()
    print data
    app = monprogramme(data)
    gtk.main()

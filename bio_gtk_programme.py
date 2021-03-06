#!/usr/bin/env python3

#CRASHES WHEN TRYING TO GET LARGE FILES FROM ENTREZ e.g. whole chromosomes, fine with single genes

import webbrowser
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from Bio import Entrez, SeqIO, Medline
Entrez.email = "A.N.Other@example.com" 
from Bio.SeqUtils import GC

class LnFrame(Gtk.Bin):
    def __init__(self, open_sequences, seq_liststore):
        Gtk.Bin.__init__(self)

        self.open_sequences = open_sequences
        self.seq_liststore = seq_liststore
        self.builder = Gtk.Builder()
        self.builder.add_from_file("seqlen-page-glade.glade")
        self.sl_box = self.builder.get_object("SeqLen-box")
        self.add(self.sl_box)
        self.cbox = self.builder.get_object("SeqLen-cbox")
        self.label = self.builder.get_object("SeqLen-result")
        self.button = self.builder.get_object("SeqLen-button")
        self.button.connect("clicked", self.clicked_callback)
        
        renderer = Gtk.CellRendererText()
        self.cbox.pack_start(renderer, True)
        self.cbox.add_attribute(renderer, "text", 0)
        self.cbox.set_model(seq_liststore)
        
    def seq_len(self): #gives the length of the sequence
        iterator = self.cbox.get_active_iter()
        seq_id = self.seq_liststore.get_value(iterator, 0)
        seq = (self.open_sequences[seq_id])
        len_result = len(seq)
        self.label.set_markup("Sequence <b>%s</b> is " %(seq_id) + str(len_result) + " bases long.")
        
    def clicked_callback(self, button): #runs function when button is clicked
        self.seq_len()
        

class CmFrame(Gtk.Bin):
    def __init__(self, open_sequences, seq_liststore):
        Gtk.Bin.__init__(self)

        self.open_sequences = open_sequences
        self.seq_liststore = seq_liststore
        self.builder = Gtk.Builder()
        self.builder.add_from_file("seqcomp-page-glade.glade")
        self.cm_box = self.builder.get_object("SeqComp-box")
        self.add(self.cm_box)
        self.cbox1 = self.builder.get_object("SeqComp-cbox1")
        self.cbox2 = self.builder.get_object("SeqComp-cbox2")
        self.label = self.builder.get_object("SeqComp-result")
        self.button = self.builder.get_object("SeqComp-button")
        self.button.connect("clicked", self.clicked_callback)
        
        renderer = Gtk.CellRendererText()
        self.cbox1.pack_start(renderer, True)
        self.cbox1.add_attribute(renderer, "text", 0)
        self.cbox1.set_model(seq_liststore)
        self.cbox2.pack_start(renderer, True)
        self.cbox2.add_attribute(renderer, "text", 0)
        self.cbox2.set_model(seq_liststore)
        
    def seq_comp(self): #compares two sequences
        iterator1 = self.cbox1.get_active_iter()
        seq_id1 = self.seq_liststore.get_value(iterator1, 0)
        seq1 = self.open_sequences[seq_id1]
        iterator2 = self.cbox2.get_active_iter()
        seq_id2 = self.seq_liststore.get_value(iterator2, 0)
        seq2 = self.open_sequences[seq_id2]
        comp_result = ((seq1) == (seq2))
        if comp_result == True:
            self.label.set_text(str(comp_result) + ", these sequences match")
        elif comp_result == False:
            self.label.set_text(str(comp_result) + ", these sequences do not match")
        

    def clicked_callback(self, button): #runs function when button is clicked
        self.seq_comp()
        

class GcFrame(Gtk.Bin):
    def __init__(self, open_sequences, seq_liststore):
        Gtk.Bin.__init__(self)

        self.open_sequences = open_sequences
        self.seq_liststore = seq_liststore
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gc-page-glade.glade")
        self.gc_box = self.builder.get_object("GC-box")
        self.add(self.gc_box)
        self.cbox = self.builder.get_object("GC-cbox")
        self.label = self.builder.get_object("GC-result")
        self.button = self.builder.get_object("GC-button")
        self.button.connect("clicked", self.clicked_callback)
        
        renderer = Gtk.CellRendererText()
        self.cbox.pack_start(renderer, True)
        self.cbox.add_attribute(renderer, "text", 0)
        self.cbox.set_model(seq_liststore)
        
    def gc_content(self): #calculates gc % of sequence
        iterator = self.cbox.get_active_iter()
        seq_id = self.seq_liststore.get_value(iterator, 0)
        seq = self.open_sequences[seq_id]
        gc_result = round(GC(seq), 2)
        self.label.set_markup(str(gc_result) + "%% of bases in sequence <b>%s</b>" %(seq_id)+ " are G or C.")

    def clicked_callback(self, button): #runs function when button is clicked
        self.gc_content()
        

class RcFrame(Gtk.Bin):
    def __init__(self, open_sequences, seq_liststore):
        Gtk.Bin.__init__(self)

        self.open_sequences = open_sequences
        self.seq_liststore = seq_liststore
        self.builder = Gtk.Builder()
        self.builder.add_from_file("revcomp-page-glade.glade")
        self.rc_box = self.builder.get_object("RevComp-box")
        self.add(self.rc_box)
        self.cbox = self.builder.get_object("RevComp-cbox")
        self.label = self.builder.get_object("RevComp-result")
        self.button = self.builder.get_object("RevComp-button")
        self.button.connect("clicked", self.clicked_callback)
        self.checkbutton = self.builder.get_object("checkbutton")
        self.checkbutton.set_mode(draw_indicator=True)
        self.checkbutton1 = self.builder.get_object("checkbutton1")
        self.checkbutton1.set_mode(draw_indicator=True)
        
        renderer = Gtk.CellRendererText()
        self.cbox.pack_start(renderer, True)
        self.cbox.add_attribute(renderer, "text", 0)
        self.cbox.set_model(seq_liststore)

    def rev_comp(self): #gives the reverse complement of DNA sequence
        iterator = self.cbox.get_active_iter()
        self.seq_id = self.seq_liststore.get_value(iterator, 0)
        seq = self.open_sequences[self.seq_id]
        self.rc_result = seq.reverse_complement()
        self.label.set_text("Tick box for results")
        
        tv = Gtk.TextView()
        tb = tv.get_buffer()
        tb.set_text(str(self.rc_result))
        tag = tb.create_tag("bold", weight=Pango.Weight.BOLD)
        start = tb.get_start_iter()
        end = tb.get_end_iter()
        tb.apply_tag(tag, start, end)
        tv.set_editable(False)
        tv.set_justification(Gtk.Justification.FILL)
        tv.set_wrap_mode(Gtk.WrapMode.CHAR)
        sw = Gtk.ScrolledWindow()
        sw.set_size_request(300,200)
        sw.add(tv)
        w = Gtk.Window(title = "Reverse complement result for sequence %s " %(self.seq_id))                                                                                                                                                                                                                                                
        w.add(sw)
        self.connect("delete-event", self.on_quit)

        def on_button_toggled(checkbutton, name):
            if self.checkbutton.get_active():
                state = "on"
                if state == "on":
                    w.show_all()
                    self.disconnect_checkbutton()
            else:
                state = "off"
                
        self.checkbutton_connect = self.checkbutton.connect("toggled", on_button_toggled, "1")

        def on_button_toggled(checkbutton1, name):
            if self.checkbutton1.get_active():
                state = "on"
                if state == "on":#writes to text file, want to write to fasta file
                    filename = (self.seq_id + ("-revcomp.html"))
                    file_open = open(filename, "w+")
                    file_open.write(str(self.rc_result))
                    file_open.close()
                    webbrowser.open_new_tab(filename)
                    self.label.set_text(str("Written to text file %s ") % (filename))
                    self.disconnect_checkbutton1()
            else:
                state = "off"
                
        self.checkbutton1_connect = self.checkbutton1.connect("toggled", on_button_toggled, "1")

    def disconnect_checkbutton(self):
        if self.checkbutton_connect > 0:
            self.checkbutton.disconnect(self.checkbutton_connect)
            self.checkbutton_connect = 0
            
    def disconnect_checkbutton1(self):
        if self.checkbutton1_connect > 0:
            self.checkbutton1.disconnect(self.checkbutton1_connect)
            self.checkbutton1_connect = 0
        
    def on_quit(self, widget, event):
        Gtk.main_quit() 

    def clicked_callback(self, button): #runs function when button is clicked
        self.rev_comp()


class TrFrame(Gtk.Bin):
    def __init__(self, open_sequences, seq_liststore):
        Gtk.Bin.__init__(self)

        self.open_sequences = open_sequences
        self.seq_liststore = seq_liststore
        self.builder = Gtk.Builder()
        self.builder.add_from_file("transl-page-glade.glade")
        self.tr_box = self.builder.get_object("Transl-box")
        self.add(self.tr_box)
        self.cbox = self.builder.get_object("Transl-cbox")
        self.label = self.builder.get_object("Transl-result")
        self.button1 = self.builder.get_object("Transl-button")
        self.button1.connect("clicked", self.clicked_callback1)
        self.button2 = self.builder.get_object("Codon-button")
        self.button2.connect("clicked", self.clicked_callback2)
        self.checkbutton = self.builder.get_object("checkbutton")
        self.checkbutton.set_mode(draw_indicator=True)
        self.checkbutton1 = self.builder.get_object("checkbutton1")
        self.checkbutton1.set_mode(draw_indicator=True)
        
        renderer = Gtk.CellRendererText()
        self.cbox.pack_start(renderer, True)
        self.cbox.add_attribute(renderer, "text", 0)
        self.cbox.set_model(seq_liststore)
        
    def translation(self): #translates sequence into protein
        iterator = self.cbox.get_active_iter()
        self.seq_id = self.seq_liststore.get_value(iterator, 0)
        seq = self.open_sequences[self.seq_id]
        mrna = seq.transcribe()
        self.tr_result = mrna.translate()
        if len(mrna) % 3 != 0:
            self.label.set_text("Warning, incomplete codon")

        tv = Gtk.TextView()
        tb = tv.get_buffer()
        tb.set_text(str(self.tr_result))
        tag = tb.create_tag("bold", weight=Pango.Weight.BOLD)
        start = tb.get_start_iter()
        end = tb.get_end_iter()
        tb.apply_tag(tag, start, end)
        tv.set_editable(False)
        tv.set_justification(Gtk.Justification.FILL)
        tv.set_wrap_mode(Gtk.WrapMode.CHAR)
        sw = Gtk.ScrolledWindow()
        sw.set_size_request(400,300)
        sw.add(tv)
        w = Gtk.Window(title = "Translation result for sequence %s " %(self.seq_id))
        w.add(sw)
        self.connect("delete-event", self.on_quit)

        def on_button_toggled(checkbutton, name):
            if self.checkbutton.get_active():
                state = "on"
                if state == "on":
                    w.show_all()
                    self.disconnect_checkbutton()
            else:
                state = "off"
                
        self.checkbutton_connect = self.checkbutton.connect("toggled", on_button_toggled, "1")

        def on_button_toggled(checkbutton1, name):
            if self.checkbutton1.get_active():
                state = "on"
                if state == "on":
                    filename = str(self.seq_id + ("-translation.html"))
                    file_open = open(filename, "w+")
                    file_open.write(str(self.tr_result))
                    file_open.close()
                    webbrowser.open_new_tab(filename)
                    self.label.set_text(str("Written to text file %s ") % (filename))
                    self.disconnect_checkbutton1()
            else:
                state = "off"
                
        self.checkbutton1_connect = self.checkbutton1.connect("toggled", on_button_toggled, "1")

    def disconnect_checkbutton(self):
        if self.checkbutton_connect > 0:
            self.checkbutton.disconnect(self.checkbutton_connect)
            self.checkbutton_connect = 0

    def disconnect_checkbutton1(self):
        if self.checkbutton1_connect > 0:
            self.checkbutton1.disconnect(self.checkbutton1_connect)
            self.checkbutton1_connect = 0
            
    def on_quit(self, widget, event):
        Gtk.main_quit()

    def clicked_callback1(self, button1): #runs function when button is clicked
        self.translation()

    def codon(self):
        from Bio.Data import CodonTable
        standard_table = CodonTable.unambiguous_dna_by_name["Standard"]
        self.label.set_text(str(standard_table))

    def clicked_callback2(self, button2):
        self.codon()
        

class OsFrame(Gtk.Bin): #opens sequences for later use
    def __init__(self, open_sequences, seq_liststore):

        Gtk.Bin.__init__(self)

        self.open_sequences = open_sequences
        self.seq_liststore = seq_liststore
        self.builder = Gtk.Builder()
        self.builder.add_from_file("openseq-page.glade")
        self.os_box = self.builder.get_object("Open-box")
        self.add(self.os_box)
        self.cbox = self.builder.get_object("Open-cbox")
        self.fbox = self.builder.get_object("Open-file")
        self.fbox.connect("file_set", self.on_file_selected)
        self.entry = self.builder.get_object("Entrez-entry")
        self.button = self.builder.get_object("Entrez-button")
        self.button.connect("clicked", self.clicked_callback)
        self.label = self.builder.get_object("Entrez-label")
        self.label1 = self.builder.get_object("Entrez-label1")
        
        renderer = Gtk.CellRendererText()
        self.cbox.pack_start(renderer, True)
        self.cbox.add_attribute(renderer, "text", 0)
        self.cbox.set_model(seq_liststore)
        self.cbox.set_active(0)
                
    def on_file_selected(self, entry): #opens a file and adds it to list store
        file = open(self.fbox.get_filename())
        for seq_record in SeqIO.parse(file, "fasta"):
            self.open_sequences[seq_record.id] = seq_record.seq # Add the id and sequence to the sequences dict
            self.seq_liststore.append([seq_record.id]) # Add the id to the liststore so we can look it up later

    def entrez_db(self): #finds details from Entrez database
        entry_text = Entrez.efetch(db = "nucleotide", id = [self.entry.get_text()], rettype = "fasta")
        en_result = SeqIO.read(entry_text, "fasta")
        self.label1.set_text(str("Written to file (%s) ") % (en_result.id))
        SeqIO.write(en_result, en_result.id, "fasta")
        self.label.set_text(str(en_result.description))
        
    def clicked_callback(self, button): #runs function when button is clicked
        self.entrez_db()
        

class PbFrame(Gtk.Bin): #opens sequences for later use
    def __init__(self):

        Gtk.Bin.__init__(self)

        self.builder = Gtk.Builder()
        self.builder.add_from_file("pbmd-search.glade")
        self.pb_box = self.builder.get_object("Pbmd-box")
        self.add(self.pb_box)
        self.label = self.builder.get_object("Pbmd-result")
        self.label1 = self.builder.get_object("Pbmd-label")
        self.label2 = self.builder.get_object("Pbmd-result1")
        self.bbox = self.builder.get_object("Pbmd-buttonbox")
        self.entry = self.builder.get_object("Pbmd-entry")
        self.entry1 = self.builder.get_object("Pbmd-entry1")
        self.button = self.builder.get_object("Pbmd-button")
        self.button.connect("clicked", self.clicked_callback)
        self.button1 = self.builder.get_object("Pbmd-button1")
        self.button1.connect("clicked", self.clicked_callback1)
        self.checkbutton = self.builder.get_object("checkbutton")
        self.checkbutton.set_mode(draw_indicator=True)
        self.checkbutton1 = self.builder.get_object("checkbutton1")
        self.checkbutton1.set_mode(draw_indicator=True)
                
    def pbmd_search(self): #searches pubmed database, using Biopython documentation
        user_input = self.entry.get_text()
        handle = Entrez.egquery(term=user_input)
        self.record = Entrez.read(handle)
        for row in self.record["eGQueryResult"]:
            if row["DbName"]=="pubmed":
                self.label.set_text(str(row["Count"]) + " records returned")
                
        handle = Entrez.esearch(db="pubmed", term=user_input, retmax=463)
        self.record = Entrez.read(handle)
        idlist = self.record["IdList"]
        handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
        self.records = Medline.parse(handle)
        self.records = list(self.records)
        self.records_str = []
        for self.record in self.records:
                self.records_str += "Title: %s <br> \nAuthors: %s <br> \nSource: %s\n\n <br><br>" %(self.record.get("TI"), ", ".join(self.record.get("AU")), self.record.get("SO"))
                self.search_result = ("".join(self.records_str)) #this causes a typeerror when some words are searched e.g. heart, lung  

        code = (self.search_result)
        html = """\
        <html>
          <head></head>
          <body>
            <p>{code}</p>
          </body>
        </html>
        """.format(code=code)

        self.connect("delete-event", self.on_quit)

        def on_button_toggled(checkbutton, name):
            if self.checkbutton.get_active():
                state = "on"
                if state == "on":
                    filename = ("pubmedresults.html")
                    file_open = open(filename, "w+")      
                    file_open.write(str(html))
                    file_open.close()
                    webbrowser.open_new_tab(filename)
                    self.disconnect_checkbutton()
            else:
                state = "off"
                
        self.checkbutton_connect = self.checkbutton.connect("toggled", on_button_toggled, "1")
    
                    
    def search(self):
        search_author = self.entry1.get_text()
        author_result = []
        for self.record in self.records:
            if not "AU" in self.record:
                continue
            if search_author in self.record["AU"]:
                author_result+=("Title: %s \nAuthors: %s \nSource: %s\n\n" %(self.record.get("TI"), ", ".join(self.record.get("AU")), self.record.get("SO")))
                self.label2.set_text(search_author)
            else:
                if search_author not in self.record["AU"]:
                    self.label2.set_text("Author not found")
                
        self.author_result = ("".join(author_result))
        
        code = (self.author_result)
        html = """\
        <html>
          <head></head>
          <body>
            <p>{code}</p>
          </body>
        </html>
        """.format(code=code)
        self.connect("delete-event", self.on_quit)

        def on_button_toggled(checkbutton1, name):
            if self.checkbutton1.get_active():
                state = "on"
                if state == "on":
                    filename = ("authorresults.html")
                    file_open = open(filename, "w+")      
                    file_open.write(str(html))
                    file_open.close()
                    webbrowser.open_new_tab(filename)
                    self.disconnect_checkbutton1()
            else:
                state = "off"
                
        self.checkbutton1_connect = self.checkbutton1.connect("toggled", on_button_toggled, "1")
    
    def on_quit(self, widget, event):
        Gtk.main_quit()
        
    def disconnect_checkbutton(self):
        if self.checkbutton_connect > 0:
            self.checkbutton.disconnect(self.checkbutton_connect)
            self.checkbutton_connect = 0
            
    def disconnect_checkbutton1(self):
        if self.checkbutton1_connect > 0:
            self.checkbutton1.disconnect(self.checkbutton1_connect)
            self.checkbutton1_connect = 0

    def clicked_callback(self, button): #runs function when button is clicked
        self.pbmd_search()
    def clicked_callback1(self, button1):
        self.search()
        
        
class MyWindow(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_size_request(300, 300)
        
        vbox = Gtk.VBox()       
        nbook = Gtk.Notebook()
        nbook.set_tab_pos(Gtk.PositionType.LEFT)
        nbook.set_scrollable(True)
        vbox.add(nbook)
        self.open_sequences = {}
        self.seq_liststore = Gtk.ListStore(str)
        self.set_title("Bio Programme")
                          
        os_box = OsFrame(self.open_sequences, self.seq_liststore)
        pb_box = PbFrame()
        sl_box = LnFrame(self.open_sequences, self.seq_liststore)
        cm_box = CmFrame(self.open_sequences, self.seq_liststore)
        gc_box = GcFrame(self.open_sequences, self.seq_liststore)
        rc_box = RcFrame(self.open_sequences, self.seq_liststore)
        tr_box = TrFrame(self.open_sequences, self.seq_liststore)
        
        nbook.append_page(os_box)
        nbook.append_page(pb_box)
        nbook.append_page(sl_box)
        nbook.append_page(cm_box)
        nbook.append_page(gc_box)
        nbook.append_page(rc_box)
        nbook.append_page(tr_box)
        
        nbook.set_tab_label_text(os_box, "Get Sequences")
        nbook.set_tab_label_text(pb_box, "Search Pubmed")
        nbook.set_tab_label_text(sl_box, "Sequence Length")
        nbook.set_tab_label_text(cm_box, "Sequence Comparison")
        nbook.set_tab_label_text(gc_box, "GC Content")
        nbook.set_tab_label_text(rc_box, "Reverse Complement")
        nbook.set_tab_label_text(tr_box, "Translate Sequence")
        self.add(vbox)
        
        self.show_all()
        self.connect("delete-event", self.on_quit)
        

    def on_quit(self, widget, event):
        Gtk.main_quit()

       
window = MyWindow()

Gtk.main()

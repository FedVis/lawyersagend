# -*- coding: iso-8859-1 -*-
#classe contenente il programma leg richiamato da serv6.py

from os import environ,getenv,tmpfile
from cgi import parse_qs
from Cookie import SimpleCookie
#import StringIO
from string import find, replace
import sqlite3 as sqlite
import sys
from time import localtime

def fresp(stringa):
    """string ---> file object"""
    tmpFileObj = tmpfile()
    tmpFileObj.write(stringa)
    tmpFileObj.flush()
    tmpFileObj.seek(0, 0)
    return (tmpFileObj)

class LEG:

    db='leg.db'
    voci=["Clienti","Colleghi","Giudici","Cause","Udienze","Scadenze"]
    chiavi=["id_cli","id_col","id_giu","id_cau","id_udi","id_sca"]
    dict_voci={'index':['Impostazioni','Copyrigth','Stop Server','Logout'],
               voci[0]:['Ricerca','Inserimento'],
               voci[1]:['Ricerca','Inserimento'],
               voci[2]:['Ricerca','Inserimento'],
               voci[3]:['Ricerca','Inserimento'],
               voci[4]:['Calendario','Ricerca','Inserimento'],
               voci[5]:['Calendario','Ricerca','Inserimento'],}
    chiavi_cook=["h1_fs","h1_ff","h1_c","h2_fs","h2_ff","h2_c","bg","tab","h3_c","print"]
    default_cook=["35","arial","green","25","verdana","black","white","800","brown","700"]
    chiavecod='piva'
    
    
    
    def __init__(self,server):
        #self.commento='eccolocommento'
        #leggi utenti e pass e inizializzo un dizionario self.pw
        self.pw={}
        fd=open('pw.txt','r')
        app=fd.readlines()
        fd.close()
        for x in app:
            if (len(x)>2)and(x[0]<>'#'):
                ind=find(x,'\t')
                st1=x[:ind]
                st2=replace(x[ind+1:],'\n','')
                st2=replace(st2,'\r','')
                self.pw[st1]=st2
        ##########
	self.server=server
    
    def esegui(self,comando):
        #sys.stderr.write('esegui')
        cmd='resp=self.'+comando+'()'
        exec cmd
        #sys.stderr.write('fine esegui')
        #return(resp)    
            
    def head(self):
        """produce i cookie e la parte iniziale di tutte le pagine web"""
        c=SimpleCookie()
        sw=1
        try:
            c.load(environ["HTTP_COOKIE"])
        except KeyError:
            pass
        chiavi=self.chiavi_cook
        default=self.default_cook
        sw=1
        #sys.stderr.write(c['bg'].value+' 1 \n')
        for x in range(0,len(chiavi)):
            if chiavi[x] not in c.keys():
                c[chiavi[x]]=default[x]
                #sys.stderr.write('reimpostato %s\n'%chiavi[x])
                sw=0
        if 1:#sw
            for x in c.keys():
                if x not in ('user','pass'):
                    c[x]["expires"]=157680000
            #sys.stderr.write(c['bg'].value+'\n')
            print c
        qs=getenv("QUERY_STRING")
        if (qs<>None)and(qs<>''):
            #sys.stderr.write("\nqs: '%s'\n"%qs)
            qs=parse_qs(qs)
            #for x in qs:
            #    sys.stderr.write("%s : %s\n"%(x,qs[x]))
        else:
            qs={}
        ###controllo pass
        sw=1
        if ("user" in qs.keys())and("pass" in qs.keys()):
            if (qs["user"][0]in self.pw.keys())and(qs["pass"][0]==self.pw[qs["user"][0]]):
                c["user"]=qs["user"][0]
                #c["user"]["expires"]=None
                c["pass"]=qs["pass"][0]
                #c["pass"]["expires"]=None
                #print c["user"]
                #print c["pass"]
                print c
                sw=0
        elif ("user" in c.keys())and("pass" in c.keys()):
            if (c["user"].value in self.pw.keys())and(c["pass"].value==self.pw[c["user"].value]):
                sw=0
        if sw:
            print "Content-Type: text/html\n"
            print"""<html>
<head>
<meta http-equiv="Author" content="Federico Visconti - federico.visconti@gmail.com">
<meta http-equiv="Content-Language" content="it">
<meta http-equiv="Content-Type" content="text/html">
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<META HTTP-EQUIV="Expires" CONTENT="-1">
<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
</head><body><center><h1>Gestione Legale</h1><br><br>
<form action=index.html method=get>username <input type=text name=user value=""><br><br>
password <input type=text name=pass value=""><br><br>
<input type=submit value=OK></form></center></body></html>"""
            return(0,0)
        ###fine controllo pass
        print "Content-Type: text/html\n"
        print"""<html>
<head>
<meta http-equiv="Author" content="Federico Visconti">
<meta http-equiv="Content-Language" content="it">
<meta http-equiv="Content-Type" content="text/html">
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<META HTTP-EQUIV="Expires" CONTENT="-1">
<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
<STYLE TYPE=text/css>
h1 { font-size:%spx; font-family:%s; color:%s }
h2 { font-size:%spx; font-family:%s; color:%s }
h3 { font-size:%spx; font-family:%s; color:%s; font-weight: bold }
body {background: %s;}
</STYLE>
</head>"""%(c["h1_fs"].value,c["h1_ff"].value,c["h1_c"].value,
            c["h2_fs"].value,c["h2_ff"].value,c["h2_c"].value,
            c["h2_fs"].value,c["h2_ff"].value,c["h3_c"].value,
            c["bg"].value)
        print"""<body>
<center>
<a href=index.html><h1>Gestione Legale</h1></a>
<table cellpadding="2" cellspacing="2"
 style="width: %spx; text-align: center; margin-left: auto; margin-right: auto;">
<tr>"""%c["tab"].value
        if 'voce0' in qs.keys():
            voce=int(qs['voce0'][0])
        else:
            voce=-1
        for x in range(0,len(self.voci)):
            if x<>voce:
                print"<td><a href=index.html?voce0=%d&voce1=0><h2>%s</h2></a></td>"%(x,self.voci[x])
            else:
                print'<td><a href=index.html?voce0=%d&voce1=0><h3>%s</h3></a></td>'%(x,self.voci[x])
        print "</tr></table>"
        return(c,qs)

    def tab1(self,c,qs):
        print """<table cellpadding="2" cellspacing="2" border="0"
style="width: %spx; text-align: left; margin-left: auto; margin-right: auto;">
<tr>
<td style="vertical-align: top; width: 20%s">"""%(c["tab"].value,'%')
        if ('voce0' in qs.keys()):
            voce0=int(qs['voce0'][0])
            if voce0<>-1:
                ind=self.voci[voce0]
            else:
                ind='index'
        else:
            voce0=-1
            ind='index'
        #print 'ind=',ind,qs
        if ind in self.dict_voci.keys():
            if "voce1" in qs.keys():
                voce1=int(qs['voce1'][0])
            else:
                voce1=-1
            for x in range(0,len(self.dict_voci[ind])):
                if x<>voce1:
                    print "<a href=index.html?voce0=%d&voce1=%d><h2>%s</h2></a>"%(voce0,x,self.dict_voci[ind][x])
                else:
                    print "<a href=index.html?voce0=%d&voce1=%d><h3>%s</h3></a>"%(voce0,x,self.dict_voci[ind][x])
        print """</td>
<td>"""
        #creazione delcontenuto richiesto
        self.tab2(c,qs,voce0,voce1)
        ###
        print """</td>
</tr>
</table>"""

    def index(self):
        #prima di tutto controlla se sono state cambiate le impostazioni e salva il cookie
        qs=parse_qs(getenv("QUERY_STRING"))
        if 'impostaz' in qs.keys():
            #sys.stderr.write('passato\n')
            c=SimpleCookie()
            for x in range(0,len(self.chiavi_cook)):
                c[self.chiavi_cook[x]]=qs[self.chiavi_cook[x]][0]
                if qs[self.chiavi_cook[x]][0]<>'':
                    self.default_cook[x]=qs[self.chiavi_cook[x]][0]
                if qs[self.chiavi_cook[x]][0]=='':
                    #sys.stderr.write('def1111\n')
                    c[self.chiavi_cook[x]]=self.default_cook[x]
            #sys.stderr.write( c['bg'].value+'\n')
            print c
        #######                    
        c,qs=self.head()
        ##se non convalida user
        if c==0:
            #immettere user
            return()
        #fine convalida user
        self.tab1(c,qs)
##        print """<br>ciao<br>
##</center>
##<a href=stop>stoppare</a>
##</body>
##</html>"""
        print """</center></body></html>"""

    def impostaz(self):
        qs=parse_qs(getenv("QUERY_STRING"))
        if 'impostaz' in qs.keys():
            #sys.stderr.write('passato\n')
            c=SimpleCookie()
            for x in range(0,len(self.chiavi_cook)):
                c[self.chiavi_cook[x]]=qs[self.chiavi_cook[x]][0]
                if qs[self.chiavi_cook[x]][0]<>'':
                    self.default_cook[x]=qs[self.chiavi_cook[x]][0]
                if qs[self.chiavi_cook[x]][0]=='':
                    #sys.stderr.write('def1111\n')
                    c[self.chiavi_cook[x]]=self.default_cook[x]
            #sys.stderr.write( c['bg'].value+'\n')
            print c
        print "Content-Type: text/html\n"
        print"""<html>
<head>
<meta http-equiv="Author" content="Federico Visconti">
<meta http-equiv="Content-Language" content="it">
<meta http-equiv="Content-Type" content="text/html">
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<META HTTP-EQUIV="Expires" CONTENT="-1">
<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
</head>
</body>
<SCRIPT LANGUAGE="JavaScript">
<!-- 
window.location="index.html?voce0=-1&voce1=0";
// -->
</script>
</body>
</html>"""

    def tab2(self,c,qs,voce0,voce1):
        #############################
        if [voce0,voce1]==[-1,0]:
            #impostazioni
            print """<center>
<h2>Scegli le impostazioni che preferisci</h2>
<form action=impostaz.html method=get>
<input type=hidden name=impostaz value=1>
<table cellpadding="2" cellspacing="2" border="1"
 style="text-align: center; width: 100%;">"""
            app=c.keys()
            app.sort()
            for x in app:
                print '<tr>'
                print '<td style="text-align: center;"><h3>%s</h3></td>'%x
                print '<td style="text-align: center;"><h3><input type=text name=%s  value=%s></h3></td>'%(x,c[x].value)
                print '</tr>'
            print """</table>
<input type=submit value=Conferma>
</form>"""
        #############################    
        elif [voce0,voce1]==[-1,1]:
            #copyrigth
            print """<center><h3>Software realizzato da<br>
Federico Visconti<br>
Qualsiasi uso non autorizzato e' punibile ai sensi di legge</h3></center>"""
        #############################    
        elif [voce0,voce1]==[-1,2]:
            #stop
            print "<center><h3>Server fermato</h3></center>"
            self.server.sf=0
        ###########logout
        elif [voce0,voce1]==[-1,3]:
            print "<center><a href=logout.html><h3>Clicca qui per effettuare il logout</h3></a></center>"
        #############################
        elif [voce0,voce1] in ([0,0],[1,0],[2,0],[3,0]):
            if not 'tab'in qs.keys():
                #ricerca
                self.ricerca(voce0,voce1,qs)
            else:
                #visualizza risultati ricerca clienti
                if voce0==0:
                    ordine='Cognome'
                else:
                    ordine=None
                self.ris_ricerca(voce0,voce1,qs,ordine)
        elif [voce0,voce1] in ([0,1],[1,1],[2,1]):
            if not 'tab'in qs.keys():
                #inserimento
                self.inserimento(voce0,voce1,qs)
            else:
                #conferma inserimento
                self.conf_inserimento(voce0,voce1,qs)
        elif [voce0,voce1]==[3,1]:
            if not 'tab'in qs.keys():
                #inserimento causa
                self.inscausa(voce0,voce1,qs)
            else:
                #print 'tab',qs['tab'][0]
                if qs['tab'][0]<>'4':
                    self.conf_inserimento(voce0,voce1,qs)
                else:
                    self.ris_ricerca(voce0,voce1,qs,None)
        elif [voce0,voce1]in([4,3],[5,3]):
            if not 'tab'in qs.keys():
                #inserimento/modifica udienze/scadenze
                self.insmodudsc(voce0,voce1,qs)
            else:
                sw=0
                if 'data' not in qs.keys():
                    sw=1
                else:
                    if len(qs['data'][0])<>16:
                        sw=1
                    else:
                        if [qs['data'][0][4],qs['data'][0][7],qs['data'][0][10],qs['data'][0][13],]<>['/','/','-',':']:
                            sw=1
                if sw==0:
                    try:
                        appint=int(qs['data'][0][:4])
                        appint=int(qs['data'][0][5:7])
                        if appint not in range(1,13):
                            sw=1
                        appint=int(qs['data'][0][8:10])
                        if appint not in range(1,32):
                            sw=1
                        appint=int(qs['data'][0][11:13])
                        if appint not in range(0,24):
                            sw=1
                        appint=int(qs['data'][0][14:])
                        if appint not in range(0,60):
                            sw=1
                    except:
                        sw=1
                if sw:
                    print """<SCRIPT language="javascript">
                    alert("Formato della data non valido es.: 2005/06/28-18:45");
                    history.back();
                    </script>"""
                    #print '<center><h3>Formato della data non valido</h3></center>'
                    #self.insmodudsc(voce0,voce1,qs)
                    return
                if qs['tab'][0]<>'4':
                    self.conf_inserimento(voce0,voce1,qs)
                else:
                    self.ris_ricerca(voce0,voce1,qs,None)
        elif [voce0,voce1]in([4,2],[5,2]):
            print "<center>Puoi inserire una nuova udienza o una nuova scadenza dalla relativa causa</center>"
        elif [voce0,voce1]in([4,0],[5,0]):
            #calendario scadenze,udienze
            self.calendario(voce0,voce1,qs,localtime())
        elif [voce0,voce1]in([4,1],[5,1]):
            #ricerca scad/ud per data
            self.ricscadud(voce0,voce1,qs)

    def logout(self):
        c=SimpleCookie()
        c["pass"]=""
        c["pass"]["expires"]=0
        c["user"]=""
        c["user"]["expires"]=0
        print c
        print "Content-Type: text/html\n"
        print """<html><body><center>logout effettuato</center></body></html>"""

    def ricscadud(self,voce0,voce1,qs):
        sw=0
        val=''
        if 'd1' in qs.keys():
            val=qs['d1'][0]
        print '<center><br><form action=index.html method=get>\
        Data iniziale (inclusa): (aaaa/mm/gg) <input name=d1 type=text value=%s><br>'%val
        val=''
        if 'd2' in qs.keys():
            val=qs['d2'][0]
        print 'Data finale (esclusa): (aaaa/mm/gg) <input type name=d2 type=text value=%s><br>'%val
        print '<input type=hidden name=voce0 value=%d><input type=hidden name=voce1 value=%d>'%(voce0,voce1)
        print '<br><input type=submit value=cerca></form><br>'
        sw=0
        t1=0
        if ('d1' in qs.keys()):
            sw=1
            #self.stdata((int(qs['d1'][0][:4]),int(qs['d1'][0][5:7]),int(qs['d1'][0][8:10])))
            try:
                self.stdata((int(qs['d1'][0][:4]),int(qs['d1'][0][5:7]),int(qs['d1'][0][8:10])))
            except:
                print '<h3>Formato della data non corretto</h3>'
                return
            else:
                t1=(int(qs['d1'][0][:4]),int(qs['d1'][0][5:7]),int(qs['d1'][0][8:10]),)
        t2=0
        if ('d2' in qs.keys()):
            sw=1
            try:
                self.stdata((int(qs['d2'][0][:4]),int(qs['d2'][0][5:7]),int(qs['d2'][0][9:11])))
            except:
                print '<h3>Formato della data non corretto</h3>'
                return
            else:
                t2=(int(qs['d2'][0][:4]),int(qs['d2'][0][5:7]),int(qs['d2'][0][9:11]),)
        if not t1:
            t1=None
        if not t2:
            t2=None           
        print '</center>'
        if sw:
            self.calendario(voce0,voce1,qs,t1=t1,t2=t2)        
        

    def calendario(self,voce0,voce1,qs,t1=None,t2=None,wp="100%"):
        """Stampa il calendario ud./scad"""
        if voce1<>-1:
            st="<a href=stampa.html?voce0=%s&voce1=-1 target=blank>Versione di stampa</a><br>"%voce0
        else:
            st=''
        print '<center>%s<h2>Calendario %s</h2>'%(st,self.voci[voce0])
        lcon,lcur=self.connect(self.voci[voce0],self.chiavi[voce0])
        #print self.stdata(localtime())
        st=''
        if t1<>None:
            st+="data >= '%s'"%self.stdata(t1)
        if (t1<>None) and (t2<>None):
            st+=' and '
        if t2<>None:
            st+="data <= '%s'"%self.stdata(t2)
        lcur.execute("select data,descrizione,%s from %s where %s order by data"%(self.chiavi[voce0],self.voci[voce0],st,))
        ris=lcur.fetchall()
        print '<table cellpadding="0" cellspacing="0" border="1" style="text-align: center; width: %s;">'%wp
        print "<tr><td>Data</td><td>Cliente</td><td>Autorita'</td><td>Citta'</td><td>Sez.</td><td>Nome Giudice</td><td>NRG</td><td>Descr.</td></tr>"
        lcur2=lcon.cursor()
        for x in ris:
            print '<tr>'
            lcur2.execute("select %s.data,Clienti.Cognome,Clienti.Nome,Giudici.Autorita,Giudici.citta,\
                          Cause.Sezione,Cause.Giudice,Cause.NRG,%s.descrizione,Cause.id_cau,Cause.id_cli,Cause.id_giu \
                          from %s,%s,%s,%s where %s.%s='%s' \
                          and Cause.id_cau=%s.id_cau and Giudici.id_giu=Cause.id_giu and \
                          Clienti.id_cli=Cause.id_cli\
                          "%(self.voci[voce0],self.voci[voce0],self.voci[voce0],self.voci[3],self.voci[2],
                             self.voci[0],self.voci[voce0],self.chiavi[voce0],x[2],self.voci[voce0]))
            ris2=lcur2.fetchone()
            if voce1<>-1:
                print "<td><a href=index.html?voce0=%d&voce1=3&%s=%s>%s</a></td><td><a href=index.html?voce0=0&voce1=0&tab=2&%s=%s>%s %s</a></td>\
                <td><a href=index.html?voce0=2&voce1=0&tab=2&%s=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td><a href=index.html?voce0=3&voce1=0&tab=2&%s=%s>%s</a></td>\
                <td>%s</td>"%(voce0,self.chiavi[voce0],x[2],ris2[0],self.chiavi[0],ris2[10],ris2[1],ris2[2],self.chiavi[2],
                              ris2[11],ris2[3],ris2[4],ris2[5],ris2[6],self.chiavi[3],ris2[9],ris2[7],ris2[8],)
            else:
                print "<td>%s</td><td>%s %s</td>\
                <td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>\
                <td>%s</td>"%(ris2[0],ris2[1],ris2[2],ris2[3],ris2[4],ris2[5],ris2[6],ris2[7],ris2[8],)
            print '</tr>'
        print '</table></center>'
        lcur2.close()
        self.closeconn(lcon,lcur)
        
    def stdata(self,t):
        """prende una tupla anno,mese,giorno e ritorna una stringa"""
        return (str(t[0])+'/'+str(t[1]+100)[1:]+'/'+str(t[2]+100)[1:]+'-00:00')
        
    def insmodudsc(self,voce0,voce1,qs):
        print "<center>"
        sw=0
        if self.chiavi[voce0] in qs.keys():
            sw=1
        if sw:
            print "<h2>Modifica %s</h2>"%self.voci[voce0]
        else:
            print "<h2>Inserisci %s</h2>"%self.voci[voce0]
        if sw:
            lcon,lcur=self.connect(self.voci[voce0],self.chiavi[voce0])
            lcur.execute("select data , descrizione from %s where %s = '%s'"%(self.voci[voce0],self.chiavi[voce0],qs[self.chiavi[voce0]][0]))
            ris=lcur.fetchone()
            qs['data']=[ris[0],]
            qs['descrizione']=[ris[1],]
        else:
            qs['data']=['aaaa/mm/gg-hh:mm',]
            qs['descrizione']=['',]
        print '<br><form name=mioform action=index.html method=get><table cellpadding="0" cellspacing="0" border="0" style="text-align: center; width: 100%;">'
        for x in ('data','descrizione'):
            if x=='data':
                print '<tr><td>%s</td><td>(aaaa/mm/gg-hh:mm)<br><input type=text name=%s value=%s></td></tr>'%(x,x,qs[x][0])
            else:
                print '<tr><td>%s</td><td><input type=text name=%s value=%s></td></tr>'%(x,x,qs[x][0])
        print "</table><br>"
        if sw:
            print '<input type=hidden name=tab value=4>'
            print '<input type=hidden name=%s value=%s>'%(self.chiavi[voce0],qs[self.chiavi[voce0]][0])
        else:
            print '<input type=hidden name=tab value=2>'
            print '<input type=hidden name=%s value=%s>'%(self.chiavi[3],qs[self.chiavi[3]][0])
        print '<input type=hidden name=voce0 value=%d>'%voce0
        print '<input type=hidden name=voce1 value=%d>'%voce1
        print '<input type=submit value=invia></form></center>'
        
        

    
    def inscausa(self,voce0,voce1,qs):
        """schermata per inserire una nuova causa"""
        if self.chiavi[3] in qs.keys():
            #vuol dire che si cerca di effettuare delle modifiche
            lcon,lcur=self.connect(self.voci[0],self.chiavi[0])
            lcur.execute("select * from Cause where %s = '%s'"%(self.chiavi[3],qs[self.chiavi[3]][0]))
            ris=lcur.fetchone()
            #print 'row',lcur.rowcount
            for x in range(0,len(lcur.description)):
                qs[lcur.description[x][0]]=[ris[x],]
            self.closeconn(lcon,lcur)
            #print qs
            ###
        #per mantenere id vari per inserimento
        st=''
        sw=0
        for x in self.chiavi[:3]:
            if x in qs.keys():
                st+='&%s=%s'%(x,qs[x][0])
                sw+=1
        if sw==3:
            sw=0
        else:
            sw=1            
        ###
        print '<center>'
        if sw:
            print 'Per inserire una nuova causa devi scegliere il relativo<br>'
            print "cliente, giudice e difensore della controparte<br>che devono essere gia' presenti nell'archivio<br>"
        if self.chiavi[0] not in qs.keys():
            print "<br><a href=index.html?voce0=0&voce1=0&cau=1%s>Scegli il cliente</a><br>"%st
        else:
            lcon,lcur=self.connect(self.voci[0],self.chiavi[0])
            lcur.execute("select Cognome, Nome from Clienti where id_cli = '%s'"%qs[self.chiavi[0]][0])
            ris=lcur.fetchone()
            ris=map(None,ris)
            self.closeconn(lcon,lcur)
            for x in range(0,len(ris)):
                if ris[x]==None:
                    ris[x]='_'
            print "<br>Cliente:  %s %s   <a href=index.html?voce0=0&voce1=0&cau=1%s>(cambia)</a><br>"%(ris[0],ris[1],st)
        if self.chiavi[1] not in qs.keys():
            print "<br><a href=index.html?voce0=1&voce1=0&cau=1%s>Scegli il Difensore della controparte</a><br>"%st
        else:
            lcon,lcur=self.connect(self.voci[1],self.chiavi[1])
            lcur.execute("select titolo, contatti from Colleghi where id_col = '%s'"%qs[self.chiavi[1]][0])
            ris=lcur.fetchone()
            ris=map(None,ris)
            self.closeconn(lcon,lcur)
            for x in range(0,len(ris)):
                if ris[x]==None:
                    ris[x]='_'
            print "<br>Difensore controparte:  %s %s   <a href=index.html?voce0=0&voce1=0&cau=1%s>(cambia)</a><br>"%(ris[0],ris[1],st)
        if self.chiavi[2] not in qs.keys():
            print "<br><a href=index.html?voce0=2&voce1=0&cau=1%s>Scegli il Giudice</a><br>"%st
        else:
            lcon,lcur=self.connect(self.voci[2],self.chiavi[2])
            lcur.execute("select Autorita, citta from Giudici where id_giu = '%s'"%qs[self.chiavi[2]][0])
            ris=lcur.fetchone()
            ris=map(None,ris)
            self.closeconn(lcon,lcur)
            for x in range(0,len(ris)):
                if ris[x]==None:
                    ris[x]='_'
            print "<br>Giudice:  %s %s   <a href=index.html?voce0=0&voce1=0&cau=1%s>(cambia)</a><br>"%(ris[0],ris[1],st)
        if not sw:
            print "<form action=index.html method=get><input type=hidden name=voce0 value=%s><input type=hidden name=voce1 value=%s>"%(voce0,voce1)
            for x in self.chiavi[:3]:
                print "<input type=hidden name=%s value=%s>"%(x,qs[x][0])
            print '<br><table cellpadding="0" cellspacing="0" border="0" style="text-align: center; width: 100%;">'
            for x in ('Sezione','Giudice','Controparte','Oggetto','NRG'):
                if x in qs.keys():
                    val=qs[x][0]
                else:
                    val="''"
                print '<tr><td>%s</td><td><input type=text name=%s value=%s></td></tr>'%(x,x,val)
            if self.chiavi[3] in qs.keys():
                if qs['Stato'][0]=='aperta':
                    appval='chiusa'
                else:
                    appval='aperta'
                print '<tr><td>Stato</td><td><select name=Stato><option>%s<option>%s</select></td></tr>'%(qs['Stato'][0],appval)
            if self.chiavi[3] in qs.keys():
                val=4
            else:
                val=0
            print "</table><input type=hidden name=tab value=%d>"%val
            if self.chiavi[3] in qs.keys():
                print "<input type=hidden name=%s value=%s>"%(self.chiavi[3],qs[self.chiavi[3]][0])
            print "<input type=submit value=Invia></form>"
        print '</center>'
        
    def connect(self,tabella, chiave):
        """esegue la connessione al db e ritorna con e cur)"""
        con=sqlite.connect(self.db)
        cur=con.cursor()
        cur.execute("select * from %s where %s='0'"%(tabella,chiave))
        return (con,cur)
    
    def closeconn(self,con,cur):
        """chiude la connessione aperta da connect"""
        cur.close()
        con.close()

    def ricerca(self,voce0,voce1,qs):
        """stampa la pagina di ricerca in una tabella"""
        #per mantenere id vari per inserimento
        if 'cau' in qs.keys():
            st=''
            for x in self.chiavi[:3]:
                if (x in qs.keys())and(x<>self.chiavi[voce0]):
                    st+='<input type=hidden name=%s value=%s>'%(x,qs[x][0])
        ###
            print "<center><h2>Ricerca per inserimento causa</h2><form action=index.html method=get><input type=submit value=Avvia><table><input type=hidden name=tab value=0><input type=hidden name=cau value=1>"+st
        else:
            print """<center><form action=index.html method=get><input type=submit value=Avvia><table><input type=hidden name=tab value=0>"""
        print "<input type=hidden name=voce0 value=%d>"%voce0
        print "<input type=hidden name=voce1 value=%d>"%voce1
        lcon,lcur=self.connect(self.voci[voce0],self.chiavi[voce0])
        self.closeconn(lcon,lcur)
        for x in lcur.description:
            if not ((voce0==3)and(x[0]=='Stato')):
                print "<tr><td>%s</td><td><input type=text name=%s value=''></td></tr>"%(x[0],x[0])
            else:
                print "<tr><td>%s</td><td><select name=Stato><option>aperta<option>chiusa</select></td></tr>"%(x[0])
        print "</table></form></center>"

    def ris_ricerca(self,voce0,voce1,qs,ordine=None):
        """visualizza i risultati della ricerca"""
        tab=qs['tab'][0]
        if tab=='3':
            print "<center><h2>Modifica i dati</h2>"
        else:
            print "<center><h2>Risultati ricerca</h2>"
        #per mantenere id vari per inserimento cause
        if 'cau' in qs.keys():
            stcau=''
            for x in self.chiavi[:3]:
                if (x in qs.keys()) and (self.chiavi.index(x)<>voce0):
                    stcau+='&%s=%s'%(x,qs[x][0])
        ###
        lcon,lcur=self.connect(self.voci[voce0],self.chiavi[voce0])
        st=''
        sw=0
        for x in lcur.description:
            if (x[0] in qs.keys())and([x[0]][0]<>''):
                if sw==1:
                    st+='and '
                if find(qs[x[0]][0],'*')==-1:
                    st+="%s like '%s%s' "%(x[0],qs[x[0]][0],"%")
                else:
                    st+="%s like '%s' "%(x[0],replace(qs[x[0]][0],'*','%'))
                sw=1
        if sw==1:
            st='where '+st
        lcur=lcon.cursor()
        if qs['tab'][0]<>'4':
            st1=''
            if ordine<>None:
                st1=' order by %s'%ordine
            #print "select * from %s %s %s"%(self.voci[voce0],st,st1)
            lcur.execute("select * from %s %s %s"%(self.voci[voce0],st,st1))
            if lcur.rowcount==0:
                print '<h3>Nessun elemento trovato</h3>'
            else:
                res=lcur.fetchall()
                #print res,'<br>'
                if qs['tab'][0]=='3':
                    print """<form action=index.html method=get><input type=hidden name=tab value=4>"""
                    print "<input type=hidden name=voce0 value=%d>"%voce0
                    print "<input type=hidden name=voce1 value=%d>"%voce1
                cont=0
                for x in res:
                    cont+=1
                    if qs['tab'][0]=='0':
                        print '<div style="text-align: left;">%ld)</div><br>'%cont
                    print '<table cellpadding="0" cellspacing="0" border="1" style="text-align: center; width: 100%;">'
                    for y in range(0,len(lcur.description)):
                        if x[y]==None:
                            appprint='_'
                        else:
                            appprint=x[y]
                        if qs['tab'][0] not in ('2','3','4'):
                            if appprint <>'_':
                                if 'cau' not in qs.keys():
                                    print '<tr><td><a href=index.html?voce0=%d&voce1=%d&tab=2&%s=%s>%s</a></td><td>%s</td></tr>'%(voce0,voce1,self.chiavi[voce0],x[0],lcur.description[y][0],appprint)
                                    ###
                                    if (voce0==3)and(lcur.description[y][0] in self.chiavi[:3]):
                                        appind=self.chiavi.index(lcur.description[y][0])
                                        lcur2=lcon.cursor()
                                        appsql=(['Cognome','Nome',self.voci[0],self.chiavi[0],'Cliente'],
                                                ['titolo','contatti',self.voci[1],self.chiavi[1],'Difensore controparte'],
                                                ['Autorita','citta',self.voci[2],self.chiavi[2],'Giudice'])
                                        lcur2.execute("select %s, %s from %s where %s='%s'"%(appsql[appind][0],appsql[appind][1],appsql[appind][2],appsql[appind][3],appprint))
                                        ris2=lcur2.fetchone()
                                        lcur2.close()
                                        print '<tr><td>%s</td><td>%s %s</td></tr>'%(appsql[appind][4],ris2[0],ris2[1]) 
                                    ###
                                else:
                                    #per mantenere id vari per inserimento cause
                                    print '<tr><td><a href=index.html?voce0=3&voce1=1&%s=%s%s>%s</a></td><td>%s</td></tr>'%(self.chiavi[voce0],x[0],stcau,lcur.description[y][0],appprint)
                        elif qs['tab'][0]=='2':
                            if (voce0==3)and(lcur.description[y][0] in self.chiavi[:3]):
                                appind=self.chiavi.index(lcur.description[y][0])
                                print '<tr><td>%s</td><td><a href=index.html?voce0=%d&voce1=0&tab=2&%s=%s>%s</a></td></tr>'%(lcur.description[y][0],appind,lcur.description[y][0],appprint,appprint)
                                lcur2=lcon.cursor()
                                appsql=(['Cognome','Nome',self.voci[0],self.chiavi[0],'Cliente'],
                                        ['titolo','contatti',self.voci[1],self.chiavi[1],'Difensore controparte'],
                                        ['Autorita','citta',self.voci[2],self.chiavi[2],'Giudice'])
                                lcur2.execute("select %s, %s from %s where %s='%s'"%(appsql[appind][0],appsql[appind][1],appsql[appind][2],appsql[appind][3],appprint))
                                ris2=lcur2.fetchone()
                                lcur2.close()
                                print '<tr><td>%s</td><td>%s %s</td></tr>'%(appsql[appind][4],ris2[0],ris2[1]) 
                            else:
                                print '<tr><td>%s</td><td>%s</td></tr>'%(lcur.description[y][0],appprint)
                        elif qs['tab'][0]=='3':
                            if appprint=='_':
                                appprint=''
                            if lcur.description[y][0]<>self.chiavi[voce0]:
                                print '<tr><td>%s</td><td><input type=text name=%s value="%s"></td></tr>'%(lcur.description[y][0],lcur.description[y][0],appprint)
                            else:
                                print '<input type=hidden name=%s value=%s>'%(lcur.description[y][0],qs[lcur.description[y][0]][0])
                    print "</table></br>"
                if qs['tab'][0]=='3':
                    print '<input type=submit value=Aggiorna>\n</form>'
        else:
            print '<center>'
            st1=''
            for x in qs.keys():
                if x not in ('voce0','voce1','tab',self.voci[voce0]):
                    if st1<>'':
                        st1+=', '
                    st1+="%s = '%s'"%(x,qs[x][0])
            #print "update %s set %s where %s='%s'"%(self.voci[voce0],st1,self.chiavi[voce0],qs[self.chiavi[voce0]][0])
            try:
                lcur.execute("update %s set %s where %s='%s'"%(self.voci[voce0],st1,self.chiavi[voce0],qs[self.chiavi[voce0]][0]))
                lcon.commit()
            except:
                print "<h3>Errore nell'aggiornamento</h3>"
            else:
                print "<h3>Aggiornamento effettuato</h3>"
            #print '</center>'
        #print "%s"%qs['id_cli'][0]
        if (qs['tab'][0]=='2'):
            print"""<table cellpadding="0" cellspacing="0" border="0" style="text-align: center; width: 100%;">"""
            if voce0<>3:
                print "<tr><td><a href=index.html?voce0=%d&voce1=%d&tab=3&%s=%s>Modifica</a></td>"%(voce0,voce1,self.chiavi[voce0],qs[self.chiavi[voce0]][0])
            else:
                print "<tr><td><a href=index.html?voce0=%d&voce1=%d&%s=%s>Modifica</a></td>"%(voce0,1,self.chiavi[voce0],qs[self.chiavi[voce0]][0])
            print "<td><a href=index.html?voce0=%d&voce1=%d&tab=4&%s=%s>Elimina</a></td></tr></table><br><br>"%(voce0,voce1,self.chiavi[voce0],qs[self.chiavi[voce0]][0])
            if voce0<3:
                print '<br><br><a href=index.html?voce0=3&voce1=1&%s=%s>Nuova Causa</a>'%(self.chiavi[voce0],qs[self.chiavi[voce0]][0])
                print '<h2>Cause aperte</h2>'
                lcur.execute("select %s,controparte,oggetto,nrg from cause where stato='aperta' and %s='%s'"%(self.chiavi[voce0],self.chiavi[voce0],qs[self.chiavi[voce0]][0]))
                ris=lcur.fetchall()
                if lcur.rowcount==0:
                    print 'Nessuna'
                else:
                    print"""<table cellpadding="0" cellspacing="0" border="0" style="text-align: center; width: 100%;">"""
                    print '<tr><td>codice causa</td><td>controparte</td><td>oggetto</td><td>nrg</td></tr>'
                    for x in ris:
                        print '<tr>'
                        sw=1
                        for y in x:
                            if sw:
                                sw=0
                                print '<td><a href=index.html?voce0=3&voce1=0&tab=2&%s=%s>%s</td>'%(self.chiavi[3],y,y)
                            else:
                                print '<td>%s</td>'%y
                        print'</tr>'
                    print '</table>'
            elif voce0==3:
                #scadenze e udienze
                print '<a href=index.html?voce0=4&voce1=3&%s=%s>Nuova Udienza</a>'%(self.chiavi[3],qs[self.chiavi[3]][0])
                print '<h2>Udienze</h2>'
                lcur2=lcon.cursor()
                #print "select data , descrizione from %s where id_cau='%s' order by data"%(self.voci[4],qs[self.chiavi[3]][0])
                lcur2.execute("select data , descrizione, %s from %s where id_cau='%s' order by data"%(self.chiavi[4],self.voci[4],qs[self.chiavi[3]][0]))
                ris2=lcur2.fetchall()
                #print ris2
                lcur2.close()
                #print lcur2.rowcount
                if lcur2.rowcount<1:
                    print 'Nessuna'
                else:
                    print """<table cellpadding="0" cellspacing="0" border="0" style="text-align: center; width: 100%;"><tr>"""
                    #print lcur2.description
                    for x in lcur2.description[:-1]:
                        print "<td>%s</td>"%x[0],
                    print"</tr>"
                    for x in ris2:
                        print '<tr>'
                        for y in range(0,len(x)-1):
                            print "<td><a href=index.html?voce0=4&voce1=3&%s=%s>%s</a></td>"%(self.chiavi[4],x[-1],x[y]),
                        print "</tr>"
                    print "</table><br>"
                print '<br><a href=index.html?voce0=5&voce1=3&%s=%s>Nuova Scadenza</a>'%(self.chiavi[3],qs[self.chiavi[3]][0])
                print '<h2>Scadenze</h2>'
                lcur2=lcon.cursor()
                #print "select data , descrizione from %s where id_cau='%s' order by data"%(self.voci[4],qs[self.chiavi[3]][0])
                lcur2.execute("select data , descrizione, %s from %s where id_cau='%s' order by data"%(self.chiavi[3],self.voci[5],qs[self.chiavi[3]][0]))
                ris2=lcur2.fetchall()
                #print ris2
                lcur2.close()
                #print lcur2.rowcount
                if lcur2.rowcount<1:
                    print 'Nessuna'
                else:
                    print """<table cellpadding="0" cellspacing="0" border="0" style="text-align: center; width: 100%;"><tr>"""
                    #print lcur2.description
                    for x in lcur2.description[:-1]:
                        print "<td>%s</td>"%x[0],
                    print"</tr>"
                    for x in ris2:
                        print '<tr>'
                        for y in range(0,len(x)-1):
                            print "<td><a href=index.html?voce0=5&voce1=3&%s=%s>%s</a></td>"%(self.chiavi[5],x[-1],x[y]),
                        print "</tr>"
                    print "</table>"
        print "</center>"
        self.closeconn(lcon,lcur)

    def inserimento(self,voce0,voce1,qs):
        #inserimento clienti
        lcon,lcur=self.connect(self.voci[voce0],self.chiavi[voce0])
        print "<center><form action=index.html method=get><input type=hidden name=tab value=0>"
        print "<input type=hidden name=voce0 value=%d>"%voce0
        print "<input type=hidden name=voce1 value=%d>"%voce1
        print '<table cellpadding="2" cellspacing="2" border="1" style="text-align: center; width: 100%;">'
        for x in lcur.description:
            if x[0]<>self.chiavi[voce0]:
                print "<tr><td>%s</td><td><input type=text name=%s value=''></td></tr>"%(x[0],x[0])
        print '</table><input type=submit value=Conferma></form></center>'
        self.closeconn(lcon,lcur)

    def conf_inserimento(self,voce0,voce1,qs):
        lcon,lcur=self.connect(self.voci[voce0],self.chiavi[voce0])
        st1=''
        st2=''
        for x in qs.keys():
            if x not in ('voce0','voce1','tab'):
                if st1<>'':
                    st1+=', '
                    st2+=', '
                st1+="%s"%x
                st2+="'%s'"%qs[x][0]
        #print "insert into Clienti (%s) values (%s)"%(st1,st2)
        print '<center>'
        if 'NRG' in qs.keys():
            #controllo 'lunicita' del NRG per l'inserimento delle cause
            lcur.execute("select * from %s where NRG='%s'"%(self.voci[voce0],qs['NRG'][0]))
            if lcur.rowcount>=1:
                print """<SCRIPT language="javascript">
                alert("NRG gia' presente");
                history.back();
                </script>"""
                return            
        try:
            lcur.execute("insert into %s (%s) values (%s)"%(self.voci[voce0],st1,st2))
            lcon.commit()
        except:
            print "<h3>Errore nell'inserimento</h3>"
        else:
            print "<h3>Inserimento effettuato</h3>"
        print '</center>'
        self.closeconn(lcon,lcur)

    def stampa(self):
        """genera la pagina di stampa per i calendari"""
        c=SimpleCookie()
        sw=1
        c.load(environ["HTTP_COOKIE"])
        if "print" in c.keys():
            wp=int(c["print"].value)
        else:
            wp='800'
        qs=parse_qs(getenv("QUERY_STRING"))
        #sys.stderr.write("qs: '%s'"%qs)
        print "Content-Type: text/html\n"
        print """<html>
<head>
<meta http-equiv="Author" content="Federico Visconti">
<meta http-equiv="Content-Language" content="it">
<meta http-equiv="Content-Type" content="text/html">
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<META HTTP-EQUIV="Expires" CONTENT="-1">
<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
<title>Stampa Calendario</title>
</head><body>"""        
        self.calendario(int(qs['voce0'][0]),-1,qs,localtime(),wp='%spx'%wp)
        print "</body></html>"
                            
        
        

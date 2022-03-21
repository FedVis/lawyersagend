#!/usr/local/bin/python

import CGIHTTPServer
import BaseHTTPServer
import SimpleHTTPServer
import os
import sys
import urllib
import select
import string
import sys
import copy
import StringIO

import CLEG

class CRH(CGIHTTPServer.CGIHTTPRequestHandler):
    ###variabili modificate per alterare la variabile "Server versio"
    sys_version = ''
    server_version = "Federico Visconti - Leg-Server"
    
    ###funzione modificata per non stampare i log a terminale
    ###toglierla o rinominarla per ristamparli
    def log_message1(self, format, *args):
        pass
    ############
    def do_POST(self):
        self.run_cgi()

    #
    def send_head(self):
        """Version of send_head that support CGI scripts"""
##        if self.is_cgi():
##            pass
        return self.run_cgi()
    
    def run_cgi(self):
        """Execute a CGI script."""        

        
        dir, rest = self.path[:1],self.path[1:]
        print 'dir,rest %s "%s"'%(dir,rest)
        if rest=='stop':
            self.server.sf=0
        if rest=="":
            rest="index.html"
            
        i = rest.rfind('?')
        if i >= 0:
            rest, query = rest[:i], rest[i+1:]
        else:
            query = ''
        i = rest.find('/')
        if i >= 0:
            script, rest = rest[:i], rest[i:]
        else:
            script, rest = rest, ''
        scriptname = dir + '/' + script
        scriptfile = self.translate_path(scriptname)

        #print 'script',script,scriptname,scriptfile

        indice=string.find(script,'.')
        if indice<>-1:
            script=script[:indice]
        
        if not(script in __builtins__.dir(self.server.leg)):
            self.send_error(404, "No such CGI script (%s)" % `scriptname`)
            return

        # Reference: http://hoohoo.ncsa.uiuc.edu/cgi/env.html
        # XXX Much of the following could be prepared ahead of time!
        env = {}
        env['SERVER_SOFTWARE'] = self.version_string()
        env['SERVER_NAME'] = self.server.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PROTOCOL'] = self.protocol_version
        env['SERVER_PORT'] = str(self.server.server_port)
        env['REQUEST_METHOD'] = self.command
        uqrest = urllib.unquote(rest)
        env['PATH_INFO'] = uqrest
        env['PATH_TRANSLATED'] = self.translate_path(uqrest)
        env['SCRIPT_NAME'] = scriptname
        
        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host
        env['REMOTE_ADDR'] = self.client_address[0]
        # XXX AUTH_TYPE
        # XXX REMOTE_USER
        # XXX REMOTE_IDENT
        if self.headers.typeheader is None:
            env['CONTENT_TYPE'] = self.headers.type
        else:
            env['CONTENT_TYPE'] = self.headers.typeheader
        length = self.headers.getheader('content-length')
        if length:
            env['CONTENT_LENGTH'] = length
        accept = []
        for line in self.headers.getallmatchingheaders('accept'):
            if line[:1] in "\t\n\r ":
                accept.append(line.strip())
            else:
                accept = accept + line[7:].split(',')
        env['HTTP_ACCEPT'] = ','.join(accept)
        ua = self.headers.getheader('user-agent')
        if ua:
            env['HTTP_USER_AGENT'] = ua
        co = filter(None, self.headers.getheaders('cookie'))
        if co:
            env['HTTP_COOKIE'] = ', '.join(co)

        ############
        try:
                nbytes = int(length)
        except (TypeError, ValueError):
            nbytes = 0
        if query:
            env['QUERY_STRING'] = query
        else:
            if self.command.lower() == "post" and nbytes > 0:
                env['QUERY_STRING'] = self.rfile.read(nbytes)
        ############
        # XXX Other HTTP_* headers
        # Since we're setting the env in the parent, provide empty
        # values to override previously set values
        for k in ('QUERY_STRING', 'REMOTE_HOST', 'CONTENT_LENGTH',
                  'HTTP_USER_AGENT', 'HTTP_COOKIE'):
            env.setdefault(k, "")
        os.environ.update(env)

        self.send_response(200, "Script output follows")

        decoded_query = query.replace('+', ' ')

        ########
        #print "fino qui"
##        if (self.have_popen2 or self.have_popen3):
##            # Windows -- use popen2 or popen3 to create a subprocess
##            #print "in win"
##            #import shutil
##            if self.have_popen3:
##                popenx = os.popen3
##            else:
##                popenx = os.popen2
##            cmdline = scriptfile
##            cmdline=cmdline[string.rfind(cmdline,'\\')+1:string.find(cmdline,'.')]
##            self.log_message("command: %s", cmdline)
##            save_stdout = sys.stdout
##            sys.stdout = self.wfile
##            fo=StringIO.StringIO(self.server.leg.esegui(cmdline))
##            sys.stdout = save_stdout            
##            sts = fo.close()
##            if sts:
##                self.log_error("CGI script exit status %#x", sts)
##            else:
##                self.log_message("CGI script exited OK")
##            #print "fine win"
##        ###########
        
        if 1:
            # Other O.S. -- execute script in this process
            #print 'no win'
            save_argv = sys.argv
            save_stdin = sys.stdin
            save_stdout = sys.stdout
            save_stderr = sys.stderr
            try:
                try:
                    #print '----script: "%s"'%script
                    sys.argv = [scriptfile]
                    if '=' not in decoded_query:
                        sys.argv.append(decoded_query)
                    sys.stdout = self.wfile
                    sys.stdin = self.rfile
                    #execfile(scriptfile, {"__name__": "__main__"})
                    self.server.leg.esegui(script)
                finally:
                    sys.argv = save_argv
                    sys.stdin = save_stdin
                    sys.stdout = save_stdout
                    sys.stderr = save_stderr
            except SystemExit, sts:
                self.log_error("CGI script exit status %s", str(sts))
            else:
                self.log_message("CGI script exited OK")


class Chttpserver(BaseHTTPServer.HTTPServer):
    
    def __init__(self, server_address, RequestHandlerClass):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.contatore=1
        self.sf=1
        self.leg=CLEG.LEG(self)

    def serve_forever(self):
        """Handle one request at a time until doomsday."""
        while self.sf:
            self.handle_request()

#main#
HandlerClass=CRH
ServerClass=Chttpserver
SimpleHTTPServer.test(HandlerClass, ServerClass)
###        


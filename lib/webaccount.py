## $Id$
## CDSware User account information implementation.  Useful for youraccount pages.

## This file is part of the CERN Document Server Software (CDSware).
## Copyright (C) 2002 CERN.
##
## The CDSware is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## The CDSware is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.  
##
## You should have received a copy of the GNU General Public License
## along with CDSware; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

## $Id$
## DO NOT EDIT THIS FILE!  IT WAS AUTOMATICALLY GENERATED FROM CDSware WML SOURCES.

## read config variables:
#include "config.wml"
#include "configbis.wml"

import sys
import cgi
from config import *
from webpage import page
from dbquery import run_sql	
from webuser import getUid,isGuestUser

imagesurl = "%s/img" % weburl

# perform_info(): display the main features of CDS personalize
def perform_info(req):
    out = ""
    uid = getUid(req)

    out += """<P>The CDS Search offers you a possibility to personalize the interface, to set up your own personal library
    of documents, or to set up an automatic alert query that would run periodically and would notify you of search
    results by email.</P>

    <blockquote>
    <dl>

    <dt>
    <A href="./set">Your Settings</A>
    <dd>Set or change your account Email address or password.
    Specify your preferences about the way the interface looks like.
    
    <dt><A href="../youralerts.py/display">Your Searches</A>
    <dd>View all the searches you performed during the last 30 days.

    <dt><A href="../yourbaskets.py/display">Your Baskets</A>
    <dd>With baskets you can define specific collections of items,
    store interesting records you want to access later or share with others."""
    if isGuestUser(uid):
        out+= warning_guest_user(type="baskets")
    out += """
    <dt><A href="../youralerts.py/list">Your Alerts</A>
    <dd>Subscribe to a search which will be run periodically by our service.  The result can be sent to you
    via Email or stored in one of your baskets."""
    if isGuestUser(uid):
	 out+= warning_guest_user(type="alerts")
         
    if cfg_cern_site:
        out += """
        <dt><A href="http://weblib.cern.ch/cgi-bin/checkloan?uid=&version=2">Your Loans</A>
        <dd>Check out book you have on load, submit borrowing requests, etc.  Requires CERN ID."""

    out += """
    </dl>
    </blockquote>"""

    return out

# perform_display_account(): display a dynamic page that shows the user's account
def perform_display_account(req,data,bask,aler,sear):
    uid = getUid(req)
    #your account 	
    if isGuestUser(uid):
 	user ="guest"	
	accBody = """You are logged in as guest. You may want to <A href="../youraccount.py/login">login</A> as a regular user <BR><BR>
		  """	
	bask=aler="""The <strong class=headline>guest</strong> users need to <A href="../youraccount.py/login">register</A>&nbspfirst"""
	sear="No queries found"
    else:
 	user = data[0]
        accBody ="""You are logged in as %s. You may want to a) <A href="../youraccount.py/logout">logout</A>; b) edit your <A href="../youraccount.py/set">email address or password</a>.<BR><BR>
		 """%user			
    out =""
    out +=template_account("Your Account",accBody)
    #your baskets
    out +=template_account("Your Baskets",bask)
    out +=template_account("Your Alert Searches",aler)
    out +=template_account("Your Searches",sear)
    out +=template_account("Your Submissions",
                           """You can consult the list of <a href="%s/yoursubmissions.py">your submissions</a>
                              and inquire about their status.""" % weburl)
    out +=template_account("Your Approvals",
                           """You can consult the list of <a href="%s/yourapprovals.py">your approvals</a>
                              with the documents you approved or refereed.""" % weburl)
    return out

# template_account() : it is a template for print each of the options from the user's account	
def template_account(title,body):	
    out =""	
    out +="""
	 	      <table class="searchbox" width="100%%" summary=""	>	
                       <thead>
                        <tr>
                         <th class="portalboxheader">%s</th>
                        </tr>		
                       </thead>
                       <tbody>
                        <tr>
                         <td class="portalboxbody">%s</td>
                        </tr>
                       </tbody>
                      </table>""" % (title, body)
    return out 

# warning_guest_user(): It returns an alert message,showing that the user is a guest user and should log into the system
def warning_guest_user(type):

    msg="""You are logged in as a guest user, so your %s will disappear at the end of the current session. If you wish you can
           <a href="../youraccount.py/login">login or register here</a>.
	"""%type
    return """<table class="errorbox" width="100%%" summary="">
                       <thead>
                        <tr>
                         <th class="errorboxheader">%s</th>
                        </tr>
                       </thead>
                      </table>""" % msg
 
## perform_delete():delete  the account of the user, not implement yet
def perform_delete():
    out = """<p>Deleting your account"""
    return out

## perform_set(email,password): edit your account parameters, email and password.
def perform_set(email,password):

    text = """
        <body>
        <p><big><strong class=headline>Edit account parameters</strong></big>
	<form method="post" action="../youraccount.py/change">
		<p>If you want to change your email address or password, please set new values in the form below.
		<table>
			<tr><td align=right><strong>New email address:</strong><br><small class=important>(mandatory)</small></td><td><input type="text" size="25" name="email" value="%s"><br><small><span class=quicknote>Example:</span> <span class=example>johndoe@example.com</span></small></td><td></td></tr>
			<tr><td align=right><strong>New password:</strong></td><td align=left><input type="password" size="25" name="password" value="%s"><br><small><span class=quicknote>Note:</span> The password phrase may contain punctuation, spaces, etc.</small></td><td><input type="hidden" name="action" value="edit"></td></tr>
				<tr><td align=center colspan=3><code class=blocknote><input class="formbutton" type="submit" value="Set new values"></code>&nbsp;&nbsp;&nbsp;</td></tr>
		</table>
        </form>
      </body>	
      """%(email,password)
    return text                    				
		
##  perform_ask(): ask for the user's email and password, for login into the system
def perform_ask(referer=''):
    text = """
              <p>If you already have an account, please log in by choosing the <strong class=headline>login
              </strong> button below. <br>If you don't own an account yet, please enter the values of your preference and choose the <strong class=headline>register</strong> button.

              <form method="post" action="../youraccount.py/login">
              <input type="hidden" name="referer" value="%s">

              <table>
                <tr>
		 <td align=right><strong>Email address:</strong><br><small class=important>(mandatory)</small>
		 </td>
                 <td><input type="text" size="25" name="p_email" value="">
			<br><small><span class=quicknote>Example:</span> <span class=example>johndoe@example.com</span></small></td>
		 <td></td>
	       </tr>
	       <tr>
		 <td align=right><strong>Password:</strong>	
			<br><small class=quicknote>(optional)</small>	
		</td>
		<td align=left><input type="password" size="25" name="p_pw" value="">
			<br><small><span class=quicknote>Note:
					</span> The password phrase may contain punctuation, spaces, etc.
				</small>
		 </td>
                 <td>
		 </td>
                </tr>
                <tr>
		 <td align=center colspan=3><code class=blocknote><input class="formbutton" type="submit" name="action" value="login"></code>&nbsp;&nbsp;&nbsp;<code class=blocknote><input class="formbutton" type="submit" name="action" value="register"></code>&nbsp;&nbsp;&nbsp;(<a href="./lost">Lost your password?</a>)
		 </td>
                </tr>
              </table>
              <p><strong>Note:</strong> Please do not use valuable passwords such as your Unix, AFS or NICE passwords with this service. Your email address will stay strictly confidential and will not be disclosed to any third party. It will be used to identify you for personal services of %s. For example, you may set up an automatic alert search that will look for new preprints and will notify you daily of new arrivals by email.
             </form>
           """ % (cgi.escape(referer), cdsname)
    return text


# perform_logout: display the message of not longer authorized, 
def perform_logout(req):
    out =""
    out+="""    
            You are no longer recognized.  If you wish you can <A href="./login">login here</A>.
         """
    return out

#def perform_lost: ask the user for his email, in order to send him the lost password	
def perform_lost():
    out =""
    out +="""
	  <body>
		<big><strong class=headline>Lost your password?</strong></big>
		<form  method="post" action="../youraccount.py/send_email">
		 If you have lost your password string, please enter the email address of your cds.cern.ch account. 
		 The lost password will be emailed to the owner of that account.
		<table>		
	    		<tr>
				<td align=right><strong>Email address:</strong></td>
				<td><input type="text" size="25" name="p_email" value=""><br><IMG src="%s/r.gif" alt="">&nbsp<small><span class=quicknote>Example:</span> <span class=example>johndoe@example.com</span></small></td>
				<td><input type="hidden" name="action" value="lost"></td>
			</tr>
			<tr>
				<td align=center colspan=3><code class=blocknote><input class="formbutton" type="submit" value="Fetch password"></code></td>
			</tr>
		</table>
			
		</form>
	  </body>
	  """%imagesurl
    return out

# perform_emailSent(email): confirm that the password has been emailed to 'email' address
def perform_emailSent(email):

    out =""
    out +="Okay, password has been emailed to %s"%email
    return out

# peform_emailMessage : display a error message when the email introduced is not correct, and sugest to try again
def perform_emailMessage(eMsg):

    out =""
    out +="""
	  <body>
		   %s <A href="../youraccount.py/lost">Try again</A>

          </body>

   	  """%eMsg 
    return out 

# perform_back(): template for return to a previous page, used for login,register and setting 
def perform_back(mess,act): 
    out =""
    out+="""
          <body>
             <table>
                <tr>
                  <td align=center>%s
                   <A href="./%s">%s</A></td>
                </tr>
             </table>
            </body>
         """%(mess,act,act)
    
    return out

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re

import datasploit.config as cfg

from datasploit.emails import email_basic_checks
from datasploit.emails import email_fullcontact
from datasploit.emails import email_haveibeenpwned

from datasploit.username import username_gituserdetails
from datasploit.username import username_keybase
from datasploit.username import username_twitterdetails


def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def osint_process(email):
    """
    Main OSINT process

    Collect information from the OSINT process using different sources.
    For this POC we use datasploit.

    Args:
        email: Email to analyze.

    Returns:
        A list of data collected.

    Raises:
        A joke data set.
    """

    datas = "["
    defpic = "static/fontawesome/info-circle.png"
    np = """
    {
        "name-node": "%s",
        "tittle": "%s",
        "Desc": "%s",
        "picture": "%s",
        "link": "%s"
    },"""

    # Validate the API Keys
    if (cfg.github_access_token == ""):
        if (datas == "["):
            datas = datas + np % ('Config','Config','Misconfiguration', 'static/fontawesome/gears.png', 'Config')
        datas = datas + np % ('Config1','GitHub','github_access_token', 'static/fontawesome/github-alt.png', 'Config')
    if (cfg.twitter_consumer_key == ""):
        if (datas == "["):
            datas = datas + np % ('Config','Config','Misconfiguration', 'static/fontawesome/gears.png', 'Config')
        datas = datas + np % ('Config2','Twitter Consumer Key','twitter_consumer_key', 'static/fontawesome/twitter-square.png', 'Config')
    if (cfg.twitter_consumer_secret == ""):
        if (datas == "["):
            datas = datas + np % ('Config','Config','Misconfiguration', 'static/fontawesome/gears.png', 'Config')
        datas = datas + np % ('Config3','Twitter Consumer Secret','twitter_consumer_secret', 'static/fontawesome/twitter-square.png', 'Config')
    if (cfg.twitter_access_token == ""):
        if (datas == "["):
            datas = datas + np % ('Config','Config','Misconfiguration', 'static/fontawesome/gears.png', 'Config')
        datas = datas + np % ('Config4','Twitter Token','twitter_access_token', 'static/fontawesome/twitter-square.png', 'Config')
    if (cfg.twiter_access_token_secret == ""):
        if (datas == "["):
            datas = datas + np % ('Config','Config','Misconfiguration', 'static/fontawesome/gears.png', 'Config')
        datas = datas + np % ('Config5','Twitter Token Secret','twiter_access_token_secret', 'static/fontawesome/twitter-square.png', 'Config')
    if (cfg.fullcontact_api == ""):
        if (datas == "["):
            datas = datas + np % ('Config','Config','Misconfiguration', 'static/fontawesome/gears.png', 'Config')
        datas = datas + np % ('Config6','FullContact','fullcontact_api', 'static/fontawesome/id-card.png', 'Config')
    if (cfg.mailboxlayer_api == ""):
        if (datas == "["):
            datas = datas + np % ('Config','Config','Misconfiguration', 'static/fontawesome/gears.png', 'Config')
        datas = datas + np % ('Config7','MailBoxLAyer','mailboxlayer_api', 'static/fontawesome/envelope-open.png', 'Config')
    if (datas != "["):
        datas = datas[:-1] + "]"
        return datas

    # Basic Checks
    data_basic_checks = email_basic_checks.main(email) # json
    if ((data_basic_checks == -1) or not(data_basic_checks['smtp_check'] == True)):
        print " No es un mail valido "
        datas = datas + np % ('Wrong','Wrong','', 'static/fontawesome/warning.png', 'Wrong')
        datas = datas + np % ('Wrong1','Invalid mail','', 'static/fontawesome/ban.png', 'Wrong')
        datas = datas + np % ('Wrong2','get out of here','', 'static/fontawesome/window-close.png', 'Wrong')
        datas = datas + np % ('Wrong3','Are you kidding me?','', 'static/fontawesome/thumbs-down.png', 'Wrong')
        datas = datas + np % ('Wrong4','Are you drunk?','', 'static/fontawesome/beer.png', 'Wrong')
        datas = datas + np % ('Wrong5','Try again','', 'static/fontawesome/bullseye.png', 'Wrong')
        datas = datas[:-1] + "]"
        return datas

    username = email.split('@')[0]
    domain = email.split('@')[1]

    # FullContact
    data_fullcontact = email_fullcontact.main(email)
    datas = datas + np % ('mail',username, domain, 'static/fontawesome/envelope-square.png', username)
    if ('demographics' in data_fullcontact.keys()):
        # Gender
        if ('gender' in data_fullcontact['demographics']):
            datas = datas + np % ('gender','Gender', data_fullcontact['demographics']['gender'], 'static/fontawesome/intersex.png', username)
        # Locacion
        if ('locationGeneral' in data_fullcontact['demographics'].keys()):
            datas = datas + np % ('location','City', data_fullcontact['demographics']['locationGeneral'], 'static/fontawesome/globe.png', username)
        elif ('locationDeduced' in data_fullcontact['demographics']):
            if ('normalizedLocation' in data_fullcontact['demographics']['locationDeduced'].keys()):
                datas = datas + np % ('location','City', data_fullcontact['demographics']['locationDeduced']['normalizedLocation'], 'static/fontawesome/globe.png', username)

    # Name
    if ('contactInfo' in data_fullcontact):
        if ('fullName' in data_fullcontact['contactInfo']):
            datas = datas + np % ('name','Name', data_fullcontact['contactInfo']['fullName'], 'static/fontawesome/user-circle.png', username)
        if ('websites' in data_fullcontact['contactInfo']):
            datas = datas + np % ('name','Website', data_fullcontact['contactInfo']['websites'][0]['url'], 'static/fontawesome/html5.png', username)

    # Organization
    if ('organizations' in data_fullcontact):
        for i in range(len(data_fullcontact['organizations'])):
            if ('name' in data_fullcontact['organizations'][i]):
                datas = datas + np % ('Org','Organization', data_fullcontact['organizations'][i]['name'], 'static/fontawesome/building.png', username)

    # Photos
    pictureA = []
    if ('photos' in data_fullcontact):
        if (len(data_fullcontact['photos']) > 0):
            datas = datas + np % ('Photos','Photos', '', 'static/fontawesome/camera.png', 'Photos')
        for i in range(len(data_fullcontact['photos'])):
            if ('url' in data_fullcontact['photos'][i]):
                picture = data_fullcontact['photos'][i]['url']
                service = data_fullcontact['photos'][i]['typeName']
                if (picture not in pictureA):
                    pictureA.append(picture)
                    datas = datas + np % ('Foto' + str(i), service, '', picture, 'Photos')

    # Social
    if ('socialProfiles' in data_fullcontact):
        datas = datas + np % ('Social','Social', 'Profiles', 'static/fontawesome/users.png', 'Social')
        for i in range(len(data_fullcontact['socialProfiles'])):
            if ('type' in data_fullcontact['socialProfiles'][i]):
                servicio = data_fullcontact['socialProfiles'][i]['type']
            if ('username' in data_fullcontact['socialProfiles'][i]):
                user = data_fullcontact['socialProfiles'][i]['username']
            elif ('id' in data_fullcontact['socialProfiles'][i]):
                user = data_fullcontact['socialProfiles'][i]['id']
            else:
                user = username
            if (os.path.isfile('./static/fontawesome/'+servicio+'.png')):
                datas = datas + np % (servicio + 'S',servicio, user, 'static/fontawesome/'+servicio+'.png', 'Social')
            else:
                datas = datas + np % (servicio + 'S',servicio, user, defpic, 'Social')

    # DigitalFootprint
    if ('digitalFootprint' in data_fullcontact):
        datas = datas + np % ('Love','Love', '', 'static/fontawesome/gratipay.png', 'Love')
        if ('topics' in data_fullcontact['digitalFootprint']):
            for i in range(len(data_fullcontact['digitalFootprint']['topics'])):
                if ('value' in data_fullcontact['digitalFootprint']['topics'][i]):
                    valor = data_fullcontact['digitalFootprint']['topics'][i]['value']
                    datas = datas + np % ('Love' + str(i), valor, '', 'static/fontawesome/gratipay.png', 'Love')

    # Haveibeenpwned
    data_haveibeenpwned = email_haveibeenpwned.main(email)
    if (len(data_haveibeenpwned) > 0):
        datas = datas + np % ('Data Breach','Data Breach', '', 'static/fontawesome/hibp.png', 'Data Breach')
        for i in range(len(data_haveibeenpwned)):
            if ('Name' in data_haveibeenpwned[i]):
                servicioL = data_haveibeenpwned[i]['Name']
            if ('BreachDate' in data_haveibeenpwned[i]):
                fecha = data_haveibeenpwned[i]['BreachDate']
            if (os.path.isfile('./static/fontawesome/'+servicioL.lower()+'.png')):
                datas = datas + np % ('Data Breach'+str(i), 'Pwned ' + servicioL, fecha, 'static/fontawesome/'+servicioL.lower()+'.png', 'Data Breach')
            else:
                datas = datas + np % ('Data Breach'+str(i), 'Pwned ' + servicioL, fecha, defpic, 'Data Breach')

    # GitUserDetails
    data_gituserdetails = username_gituserdetails.main(username)
    if ('message' not in data_gituserdetails):
        datas = datas + np % ('Github','Github', '', 'static/fontawesome/github.png', 'Github')
        if ('public_repos' in data_gituserdetails):
            datas = datas + np % ('ReposGit','Repos', data_gituserdetails['public_repos'], 'static/fontawesome/folder.png', 'Github')
        if ('followers' in data_gituserdetails):
            datas = datas + np % ('FollowersGit','Followers', data_gituserdetails['followers'], 'static/fontawesome/user.png', 'Github')
        if ('following' in data_gituserdetails):
            datas = datas + np % ('followingGit','Following', data_gituserdetails['following'], 'static/fontawesome/user.png', 'Github')
        if ('company' in data_gituserdetails and data_gituserdetails['company'] != None):
            datas = datas + np % ('companyGit','Company', data_gituserdetails['company'], 'static/fontawesome/building-o.png', 'Github')
        # import ipdb; ipdb.set_trace()
        if ('name' in data_gituserdetails and data_gituserdetails['name'] != None):
            datas = unicode(datas) + unicode(np) % ('nameGit','Git Name', data_gituserdetails['name'], 'static/fontawesome/user-circle.png', 'Github')

    datas = datas[:-1] + "]"
    return datas

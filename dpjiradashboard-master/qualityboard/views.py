from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from requests.auth import HTTPBasicAuth
from .models import DP, DPExternal, DPM, DPMExternal, ImpactAreas, ImpactApplications, EDACurrentMonth, EDAPreviousMonth, EDALearnings, CFD, IFD, CFDDPM,CFDMOB
from .form import DPForm, DPExternalForm, DPM, DPMExternal,MOB,MOBExternal,ImpactAreaForm, ImpactApplicationForm, EDAPreviousMonthForm, EDACurrentMonthForm, EDALearningsForm, CFDForm, IFDForm


import sys
from operator import itemgetter
import requests
import json
from datetime import datetime, date, timedelta
import datetime, calendar
from collections import OrderedDict
from pytz import timezone
import time
import pandas as pd
import numpy as np
import re

import os
import environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(SECRET_KEY = str,)
environ.Env.read_env(os.path.join(BASE_DIR,'.env'))

import warnings
warnings.filterwarnings("ignore")


def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    elif ('dialpad.com' not in request.user.email):
        print("Not A Dialpad User:", request.user)
        logout(request)
        return render(request, 'login.html', {
            "message": "Invalid User Permission !!!"
        })

    else:
        dp = DP.objects.get(id=1)
        dpexternal = DPExternal.objects.get(id=1)
        dpm = DPM.objects.get(id=1)
        dpmexternal = DPMExternal.objects.get(id=1)

        lastupdatedon = dp.LastUpdate

        dpdailyjira = [dp.One,dp.Two,dp.Three,dp.Four,dp.Five,dp.Six,dp.Seven,dp.Eight,dp.Nine,dp.Ten,dp.Eleven,dp.Twelve,dp.Thirteen,dp.Fourteen, \
                       dp.Fifteen,dp.Sixteen,dp.Seventeen,dp.Eighteen,dp.Nineteen,dp.Twenty,dp.Twentyone,dp.Twentytwo,dp.Twentythree,dp.Twentyfour, \
                       dp.Twentyfive,dp.Twentysix,dp.Twentyseven,dp.Twentyeight,dp.Twentynine,dp.Thirty,dp.Thirtyone,\
                       ]
        totaldpdailyjira = list(map(int, dpdailyjira))

        dpdailysealteam = {
            'AccountBilling': int(dp.AccountBilling), 'Analytics': int(dp.Analytics), 'BackendInfrastructure': int(dp.BackendInfrastructure), 'CallExperience': int(dp.CallExperience), 'CallingFeatures': int(dp.CallingFeatures), \
            'ContactCenter': int(dp.ContactCenter), 'CustomerAgentAssist': int(dp.CustomerAgentAssist), 'DataInsights': int(dp.DataInsights), 'DeveloperPlatform': int(dp.DeveloperPlatform), 'Devices': int(dp.Devices), 'DialpadTalk': int(dp.DialpadTalk), \
            'DigitalExperience': int(dp.DigitalExperience), 'EngineeringProductivity': int(dp.EngineeringProductivity), 'FrontendInfrastructure': int(dp.FrontendInfrastructure), 'Growth': int(dp.Growth), 'Integrations': int(dp.Integrations), \
            'Messaging': int(dp.Messaging), 'Mobile': int(dp.Mobile), 'ProductionSupport': int(dp.ProductionSupport), 'UberConference': int(dp.UberConference), 'VoiceIntelligence': int(dp.VoiceIntelligence), 'Website': int(dp.Website), \
           }
        internaltop5sealteam = dict(sorted(dpdailysealteam.items(), key = itemgetter(1), reverse = True)[:5])

        dpdailystatus = {
            'Backlog': int(dp.Backlog), 'Blocked': int(dp.Blocked), 'CodeReview': int(dp.CodeReview), 'Closed': int(dp.Closed), 'InProgress': int(dp.InProgress), \
            'NeedsTriage': int(dp.NeedsTriage), 'Open': int(dp.Open), 'ReadyforTesting': int(dp.ReadyforTesting), 'ReadyforProduction': int(dp.ReadyforProduction), 'ToDo': int(dp.ToDo),
            }
        internaltop5status = dict(sorted(dpdailystatus.items(), key=itemgetter(1), reverse=True)[:5])

        dpexternaldailyjira = [dpexternal.One, dpexternal.Two, dpexternal.Three, dpexternal.Four, dpexternal.Five, dpexternal.Six, dpexternal.Seven, dpexternal.Eight, dpexternal.Nine, dpexternal.Ten, dpexternal.Eleven,
                       dpexternal.Twelve, dpexternal.Thirteen, dpexternal.Fourteen, \
                       dpexternal.Fifteen, dpexternal.Sixteen, dpexternal.Seventeen, dpexternal.Eighteen, dpexternal.Nineteen, dpexternal.Twenty, dpexternal.Twentyone,
                       dpexternal.Twentytwo, dpexternal.Twentythree, dpexternal.Twentyfour, \
                       dpexternal.Twentyfive, dpexternal.Twentysix, dpexternal.Twentyseven, dpexternal.Twentyeight, dpexternal.Twentynine, dpexternal.Thirty, dpexternal.Thirtyone, \
                       ]
        totaldpexternaldailyjira = list(map(int, dpexternaldailyjira))
        dpexternaldailysealteam = {
            'AccountBilling': int(dpexternal.AccountBilling), 'Analytics': int(dpexternal.Analytics),'BackendInfrastructure': int(dpexternal.BackendInfrastructure), 'CallExperience': int(dpexternal.CallExperience), 'CallingFeatures': int(dpexternal.CallingFeatures), \
            'ContactCenter': int(dpexternal.ContactCenter), 'CustomerAgentAssist': int(dpexternal.CustomerAgentAssist), 'DataInsights': int(dpexternal.DataInsights), 'DeveloperPlatform': int(dpexternal.DeveloperPlatform), 'Devices': int(dpexternal.Devices), 'DialpadTalk': int(dpexternal.DialpadTalk), \
            'DigitalExperience': int(dpexternal.DigitalExperience), 'EngineeringProductivity': int(dpexternal.EngineeringProductivity), 'FrontendInfrastructure': int(dpexternal.FrontendInfrastructure), 'Growth': int(dpexternal.Growth), 'Integrations': int(dpexternal.Integrations), \
            'Messaging': int(dpexternal.Messaging), 'Mobile': int(dpexternal.Mobile), 'ProductionSupport': int(dpexternal.ProductionSupport), 'UberConference': int(dpexternal.UberConference), 'VoiceIntelligence': int(dpexternal.VoiceIntelligence), 'Website': int(dpexternal.Website), \
            }
        externaltop5sealteam = dict(sorted(dpexternaldailysealteam.items(), key=itemgetter(1), reverse=True)[:5])

        dpexternaldailystatus = {
            'Backlog': int(dpexternal.Backlog), 'Blocked': int(dpexternal.Blocked), 'CodeReview': int(dpexternal.CodeReview), 'Closed': int(dpexternal.Closed), 'InProgress': int(dpexternal.InProgress), \
            'NeedsTriage': int(dpexternal.NeedsTriage), 'Open': int(dpexternal.Open), 'ReadyforTesting': int(dpexternal.ReadyforTesting), 'ReadyforProduction': int(dpexternal.ReadyforProduction), 'ToDo': int(dpexternal.ToDo),
        }
        externaltop5status = dict(sorted(dpexternaldailystatus.items(), key=itemgetter(1), reverse=True)[:5])

        return render(request,'index.html', {
            "lastupdatedon": lastupdatedon,
            "dpdailyjira": dpdailyjira,
            "dpexternaldailyjira": dpexternaldailyjira,
            "internaltop5sealteamkeys": list(internaltop5sealteam.keys()),
            "internaltop5sealteamvalues": list(internaltop5sealteam.values()),
            "internaltop5statuskeys":list(internaltop5status.keys()),
            "internaltop5statusvalues": list(internaltop5status.values()),
            "externaltop5sealteamkeys": list(externaltop5sealteam.keys()),
            "externaltop5sealteamvalues": list(externaltop5sealteam.values()),
            "externaltop5statuskeys": list(externaltop5status.keys()),
            "externaltop5statusvalues": list(externaltop5status.values()),
            "totaldpdailyjira": sum(totaldpdailyjira),
            "totaldpexternaldailyjira": sum(totaldpexternaldailyjira),
            })



def dpm(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        dpm = DPM.objects.get(id=1)
        dpmexternal = DPMExternal.objects.get(id=1)

        lastdpmupdatedon = dpm.LastUpdate
        dpmdailyjira = [dpm.One, dpm.Two, dpm.Three, dpm.Four, dpm.Five, dpm.Six, dpm.Seven, dpm.Eight, dpm.Nine, dpm.Ten, dpm.Eleven, dpm.Twelve, dpm.Thirteen, dpm.Fourteen, \
                       dpm.Fifteen, dpm.Sixteen, dpm.Seventeen, dpm.Eighteen, dpm.Nineteen, dpm.Twenty, dpm.Twentyone, dpm.Twentytwo, dpm.Twentythree, dpm.Twentyfour, \
                       dpm.Twentyfive, dpm.Twentysix, dpm.Twentyseven, dpm.Twentyeight, dpm.Twentynine, dpm.Thirty, dpm.Thirtyone, \
                       ]
        totaldpmdailyjira = list(map(int, dpmdailyjira))

        dpmdailystatus = {
            'Backlog': int(dpm.Backlog), 'Blocked': int(dpm.Blocked), 'CodeReview': int(dpm.CodeReview), 'Closed': int(dpm.Closed), 'InProgress': int(dpm.InProgress), \
            'NeedsTriage': int(dpm.NeedsTriage), 'Open': int(dpm.Open), 'ReadyforTesting': int(dpm.ReadyforTesting), 'ReadyforProduction': int(dpm.ReadyforProduction), 'ToDo': int(dpm.ToDo),
        }
        internaltop5dpmstatus = dict(sorted(dpmdailystatus.items(), key=itemgetter(1), reverse=True)[:5])

        dpmexternaldailyjira = [dpmexternal.One, dpmexternal.Two, dpmexternal.Three, dpmexternal.Four, dpmexternal.Five, dpmexternal.Six, dpmexternal.Seven, dpmexternal.Eight, dpmexternal.Nine, dpmexternal.Ten, \
                               dpmexternal.Eleven, dpmexternal.Twelve, dpmexternal.Thirteen, dpmexternal.Fourteen, dpmexternal.Fifteen, dpmexternal.Sixteen, dpmexternal.Seventeen, dpmexternal.Eighteen, \
                               dpmexternal.Nineteen, dpmexternal.Twenty, dpmexternal.Twentyone, dpmexternal.Twentytwo, dpmexternal.Twentythree, dpmexternal.Twentyfour, \
                               dpmexternal.Twentyfive, dpmexternal.Twentysix, dpmexternal.Twentyseven, dpmexternal.Twentyeight, dpmexternal.Twentynine, dpmexternal.Thirty, dpmexternal.Thirtyone, \
                               ]
        totaldpmexternaldailyjira = list(map(int, dpmexternaldailyjira))

        dpmexternaldailystatus = {
            'Backlog': int(dpmexternal.Backlog), 'Blocked': int(dpmexternal.Blocked), 'CodeReview': int(dpmexternal.CodeReview), 'Closed': int(dpmexternal.Closed), 'InProgress': int(dpmexternal.InProgress), \
            'NeedsTriage': int(dpmexternal.NeedsTriage), 'Open': int(dpmexternal.Open), 'ReadyforTesting': int(dpmexternal.ReadyforTesting), 'ReadyforProduction': int(dpmexternal.ReadyforProduction), 'ToDo': int(dpmexternal.ToDo),
        }
        externaltop5dpmstatus = dict(sorted(dpmexternaldailystatus.items(), key=itemgetter(1), reverse=True)[:5])

    return render(request,'dpm.html', {
        "lastdpmupdatedon": lastdpmupdatedon,
        "dpmdailyjira": dpmdailyjira,
        "dpmexternaldailyjira": dpmexternaldailyjira,
        "internaltop5dpmstatuskeys": list(internaltop5dpmstatus.keys()),
        "internaltop5dpmstatusvalues": list(internaltop5dpmstatus.values()),
        "externaltop5dpmstatuskeys": list(externaltop5dpmstatus.keys()),
        "externaltop5dpmstatusvalues": list(externaltop5dpmstatus.values()),
        "totaldpmdailyjira": sum(totaldpmdailyjira),
        "totaldpmexternaldailyjira": sum(totaldpmexternaldailyjira),

    })


def mob(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        mob = MOB.objects.get(id=1)
        mobexternal = MOBExternal.objects.get(id=1)

        lastmobupdatedon = mob.LastUpdate
        mobdailyjira = [mob.One, mob.Two, mob.Three, mob.Four, mob.Five, mob.Six, mob.Seven, mob.Eight, mob.Nine, mob.Ten, mob.Eleven, mob.Twelve, mob.Thirteen, mob.Fourteen, \
                        mob.Fifteen, mob.Sixteen, mob.Seventeen, mob.Eighteen, mob.Nineteen, mob.Twenty, mob.Twentyone, mob.Twentytwo, mob.Twentythree, mob.Twentyfour, \
                        mob.Twentyfive, mob.Twentysix, mob.Twentyseven, mob.Twentyeight, mob.Twentynine, mob.Thirty, mob.Thirtyone, \
                        ]
        totalmobdailyjira = list(map(int, mobdailyjira))

        mobdailystatus = {
            'Backlog': int(mob.Backlog), 'Blocked': int(mob.Blocked), 'CodeReview': int(mob.CodeReview), 'Closed': int(mob.Closed), 'InProgress': int(mob.InProgress), \
            'NeedsTriage': int(mob.NeedsTriage), 'Open': int(mob.Open), 'ReadyforTesting': int(mob.ReadyforTesting), 'ReadyforProduction': int(mob.ReadyforProduction), 'ToDo': int(mob.ToDo),
        }
        internaltop5mobstatus = dict(sorted(mobdailystatus.items(), key=itemgetter(1), reverse=True)[:5])

        mobexternaldailyjira = [mobexternal.One, mobexternal.Two, mobexternal.Three, mobexternal.Four, mobexternal.Five, mobexternal.Six, mobexternal.Seven, mobexternal.Eight, mobexternal.Nine, mobexternal.Ten, \
                                mobexternal.Eleven, mobexternal.Twelve, mobexternal.Thirteen, mobexternal.Fourteen, mobexternal.Fifteen, mobexternal.Sixteen, mobexternal.Seventeen, mobexternal.Eighteen, \
                                mobexternal.Nineteen, mobexternal.Twenty, mobexternal.Twentyone, mobexternal.Twentytwo, mobexternal.Twentythree, mobexternal.Twentyfour, \
                                mobexternal.Twentyfive, mobexternal.Twentysix, mobexternal.Twentyseven, mobexternal.Twentyeight, mobexternal.Twentynine, mobexternal.Thirty, mobexternal.Thirtyone, \
                                ]
        totalmobexternaldailyjira = list(map(int, mobexternaldailyjira))

        mobexternaldailystatus = {
            'Backlog': int(mobexternal.Backlog), 'Blocked': int(mobexternal.Blocked), 'CodeReview': int(mobexternal.CodeReview), 'Closed': int(mobexternal.Closed), 'InProgress': int(mobexternal.InProgress), \
            'NeedsTriage': int(mobexternal.NeedsTriage), 'Open': int(mobexternal.Open), 'ReadyforTesting': int(mobexternal.ReadyforTesting), 'ReadyforProduction': int(mobexternal.ReadyforProduction), 'ToDo': int(mobexternal.ToDo), \
        }
        externaltop5mobstatus = dict(sorted(mobexternaldailystatus.items(), key=itemgetter(1), reverse=True)[:5])

        return render(request, 'mob.html', {
            "lastmobupdatedon": lastmobupdatedon,
            "mobdailyjira": mobdailyjira,
            "mobexternaldailyjira": mobexternaldailyjira,
            "internaltop5mobstatuskeys": list(internaltop5mobstatus.keys()),
            "internaltop5mobstatusvalues": list(internaltop5mobstatus.values()),
            "externaltop5mobstatuskeys": list(externaltop5mobstatus.keys()),
            "externaltop5mobstatusvalues": list(externaltop5mobstatus.values()),
            "totalmobdailyjira": sum(totalmobdailyjira),
            "totalmobexternaldailyjira": sum(totalmobexternaldailyjira),
        })

def eda(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        month = datetime.datetime.now().strftime("%B")
        dictimpactareas = {}
        dictimpactapplication = {}
        dictedapreviousmonth = {}
        dictedacurrentmonth = {}
        dictedalaernings = {}

        countarea = 1
        while countarea <= 5:
            impactareas = ImpactAreas.objects.get(id=countarea)
            dictimpactareas[impactareas.Area] = impactareas.Number
            countarea += 1
        impactareaskeys = list(dictimpactareas.keys())
        impactareasvalues = list(dictimpactareas.values())

        countapplication = 1
        while countapplication <= 5:
            impactapplication = ImpactApplications.objects.get(id=countapplication)
            dictimpactapplication[impactapplication.Application] = impactapplication.Number
            countapplication += 1
        impactapplicationskeys = list(dictimpactapplication.keys())
        impactapplicationsvalues = list(dictimpactapplication.values())

        countprevousmonth = 1
        while countprevousmonth <= 7:
            edapreviousmonth = EDAPreviousMonth.objects.get(id=countprevousmonth)
            dictedapreviousmonth[edapreviousmonth.EDAType] = edapreviousmonth.Number
            countprevousmonth += 1
        edapreviousmonthkeys = list(dictedapreviousmonth.keys())
        edapreviousmonthvalues = list(dictedapreviousmonth.values())
        totalpreviousmonth = list(map(int, edapreviousmonthvalues))

        countcurrentmonth = 1
        while countcurrentmonth <= 7:
            edacurrentmonth = EDACurrentMonth.objects.get(id=countcurrentmonth)
            dictedacurrentmonth[edacurrentmonth.EDAType] = edacurrentmonth.Number
            countcurrentmonth += 1
        edacurrentmonthkeys = list(dictedacurrentmonth.keys())
        edacurrentmonthvalues = list(dictedacurrentmonth.values())
        totalcurrentmonth = list(map(int, edacurrentmonthvalues))

        edalearning = EDALearnings.objects.get(id=1)
        dictedalaernings["ActionItems"] = edalearning.ActionItem
        dictedalaernings["PreviousMonths"] = edalearning.PreviousMonth
        dictedalaernings["CurrentMonth"] = edalearning.CurrentMonth

        edalearningkeys = list(dictedalaernings.keys())
        edalearningvalues = list(dictedalaernings.values())

        return render(request, 'eda.html',{
            "month": month,
            "impactareaskeys": impactareaskeys,
            "impactareasvalues": impactareasvalues,
            "impactapplicationskeys": impactapplicationskeys,
            "impactapplicationsvalues": impactapplicationsvalues,
            "edapreviousmonthkeys": edapreviousmonthkeys,
            "edapreviousmonthvalues": edapreviousmonthvalues,
            "edacurrentmonthkeys": edacurrentmonthkeys,
            "edacurrentmonthvalues": edacurrentmonthvalues,
            "totalpreviousmonth": sum(totalpreviousmonth),
            "totalcurrentmonth": sum(totalcurrentmonth),
            "edalearning": edalearningvalues[0],
            "previousmonth": edalearningvalues[1],
            "currentmonth": edalearningvalues[2],            
        })

def dialpad(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        TotalFixed_CFD = []
        TotalBackLog_CFD = []
        TotalNoise_CFD = []
        TotalMRT_CFD = []
        CFDtotalPriorityHigh = []
        CFDtotalPriorityMedium = []
        CFDtotalPriorityLow = []
        CFDtotalPriorityUrgent = []
        CFDTotalTalk = []
        CFDTotalCC = []
        CFDTotalINT = []
        CFDTotalOTH = []
        TotalFixed_IFD = []
        TotalBackLog_IFD = []
        TotalNoise_IFD = []
        TotalMRT_IFD = []

        dialpadoverall = CFD.objects.get(id=1)

        CFDtotalJiras = dialpadoverall.CFDtotalJiras.split(",")
        CFDtotalJiras = list(map(int, CFDtotalJiras))
        CFDtotalFixed = dialpadoverall.CFDtotalFixed.split(",")
        CFDtotalFixed = list(map(int, CFDtotalFixed))
        CFDtotalMRT = dialpadoverall.CFDtotalMRT.split(" ")
        CFDtotalMRT = list(filter(None, CFDtotalMRT))
        CFDtotalMRT = list(map(float, CFDtotalMRT))
        CFDtotalNotClosed = dialpadoverall.CFDtotalNotClosed.split(",")
        CFDtotalNotClosed = list(map(int, CFDtotalNotClosed))
        CFDtotalCurrentFix = dialpadoverall.CFDtotalCurrentFix.split(",")
        CFDtotalCurrentFix = list(map(int, CFDtotalCurrentFix))
        CFDtotalNoise = dialpadoverall.CFDtotalNoise.split(",")
        CFDtotalNoise = list(map(int, CFDtotalNoise))
        CFDtotalPriorityH = dialpadoverall.CFDtotalPriorityH.split(",")
        CFDtotalPriorityH = list(map(int, CFDtotalPriorityH))
        CFDtotalPriorityM = dialpadoverall.CFDtotalPriorityM.split(",")
        CFDtotalPriorityM = list(map(int, CFDtotalPriorityM))
        CFDtotalPriorityL = dialpadoverall.CFDtotalPriorityL.split(",")
        CFDtotalPriorityL = list(map(int, CFDtotalPriorityL))
        CFDtotalPriorityU = dialpadoverall.CFDtotalPriorityU.split(",")
        CFDtotalPriorityU = list(map(int, CFDtotalPriorityU))
        CFDtalkJiras = dialpadoverall.CFDtalkJiras.split(",")
        CFDtalkJiras = list(map(int, CFDtalkJiras))
        CFDCCJiras = dialpadoverall.CFDCCJiras.split(",")
        CFDCCJiras = list(map(int, CFDCCJiras))
        CFDINTJiras = dialpadoverall.CFDINTJiras.split(",")
        CFDINTJiras = list(map(int, CFDINTJiras))

        ifd_dialpadoverall = IFD.objects.get(id=1)
        IFDtotalJiras = ifd_dialpadoverall.IFDtotalJiras.split(",")
        IFDtotalJiras = list(map(int, IFDtotalJiras))
        IFDtotalFixed = ifd_dialpadoverall.IFDtotalFixed.split(",")
        IFDtotalFixed = list(map(int, IFDtotalFixed))
        IFDtotalMRT = ifd_dialpadoverall.IFDtotalMRT.split(" ")
        IFDtotalMRT = list(filter(None, IFDtotalMRT))
        IFDtotalMRT = list(map(float, IFDtotalMRT))
        IFDtotalNotClosed = ifd_dialpadoverall.IFDtotalNotClosed.split(",")
        IFDtotalNotClosed = list(map(int, IFDtotalNotClosed))
        IFDtotalCurrentFix = ifd_dialpadoverall.IFDtotalCurrentFix.split(",")
        IFDtotalCurrentFix = list(map(int, IFDtotalCurrentFix))
        IFDtotalNoise = ifd_dialpadoverall.IFDtotalNoise.split(",")
        IFDtotalNoise = list(map(int, IFDtotalNoise))
        CFDLastUpdate = dialpadoverall.CFDLastUpdate

        for i in range(len(CFDtotalJiras)):
            if CFDtotalJiras[i] == 0:
                CFDtotalJiras[i] = 1
            else:
                pass
        for i in range(len(IFDtotalJiras)):
            if IFDtotalJiras[i] == 0:
                IFDtotalJiras[i] = 1
            else:
                pass

        for i in range(len(CFDtotalMRT)):
            if np.isnan(CFDtotalMRT[i]):
                CFDtotalMRT[i] = 0.25
            else:
                pass
        for i in range(len(IFDtotalMRT)):
            if np.isnan(IFDtotalMRT[i]):
                IFDtotalMRT[i] = 0.25
            else:
                pass

        TotalFixedPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtotalFixed, CFDtotalJiras)]
        TotalBackLogPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtotalNotClosed, CFDtotalJiras)]
        TotalNoisePer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtotalNoise, CFDtotalJiras)]
        CFDtotalPriorityHPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtotalPriorityH, CFDtotalJiras)]
        CFDtotalPriorityMPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtotalPriorityM, CFDtotalJiras)]
        CFDtotalPriorityLPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtotalPriorityL, CFDtotalJiras)]
        CFDtotalPriorityUPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtotalPriorityU, CFDtotalJiras)]
        TotalTalkPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkJiras, CFDtotalJiras)]
        TotalCCPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCJiras, CFDtotalJiras)]
        TotalINTPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTJiras, CFDtotalJiras)]
        TotalOTHPer = [np.round((100 - a - b - c) , 2) for a, b,c in zip(TotalTalkPer,TotalCCPer,TotalINTPer)]

        TotalFixedPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDtotalFixed, IFDtotalJiras)]
        TotalBackLogPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDtotalNotClosed, IFDtotalJiras)]
        TotalNoisePer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDtotalNoise, IFDtotalJiras)]

        TotalFixed_CFD.append(np.round(np.mean(TotalFixedPer[:-1]),2))
        TotalFixed_CFD.append(np.round(np.mean(TotalFixedPer[-4:-1]), 2))
        TotalFixed_CFD.append(TotalFixedPer[-2])
        TotalFixed_CFD.append(TotalFixedPer[-1])

        TotalBackLog_CFD.append(np.round(np.mean(TotalBackLogPer[:-1]), 2))
        TotalBackLog_CFD.append(np.round(np.mean(TotalBackLogPer[-4:-1]), 2))
        TotalBackLog_CFD.append(TotalBackLogPer[-2])
        TotalBackLog_CFD.append(TotalBackLogPer[-1])

        TotalNoise_CFD.append(np.round(np.mean(TotalNoisePer[:-1]), 2))
        TotalNoise_CFD.append(np.round(np.mean(TotalNoisePer[-4:-1]), 2))
        TotalNoise_CFD.append(TotalNoisePer[-2])
        TotalNoise_CFD.append(TotalNoisePer[-1])

        TotalMRT_CFD.append(np.round(np.mean(CFDtotalMRT[:-1]), 2))
        TotalMRT_CFD.append(np.round(np.mean(CFDtotalMRT[-4:-1]), 2))
        TotalMRT_CFD.append(CFDtotalMRT[-2])
        TotalMRT_CFD.append(CFDtotalMRT[-1])

        TotalFixed_IFD.append(np.round(np.mean(TotalFixedPer_IFD[:-1]), 2))
        TotalFixed_IFD.append(np.round(np.mean(TotalFixedPer_IFD[-4:-1]), 2))
        TotalFixed_IFD.append(TotalFixedPer_IFD[-2])
        TotalFixed_IFD.append(TotalFixedPer_IFD[-1])

        TotalBackLog_IFD.append(np.round(np.mean(TotalBackLogPer_IFD[:-1]), 2))
        TotalBackLog_IFD.append(np.round(np.mean(TotalBackLogPer_IFD[-4:-1]), 2))
        TotalBackLog_IFD.append(TotalBackLogPer_IFD[-2])
        TotalBackLog_IFD.append(TotalBackLogPer_IFD[-1])

        TotalNoise_IFD.append(np.round(np.mean(TotalNoisePer_IFD[:-1]), 2))
        TotalNoise_IFD.append(np.round(np.mean(TotalNoisePer_IFD[-4:-1]), 2))
        TotalNoise_IFD.append(TotalNoisePer_IFD[-2])
        TotalNoise_IFD.append(TotalNoisePer_IFD[-1])

        TotalMRT_IFD.append(np.round(np.mean(IFDtotalMRT[:-1]), 2))
        TotalMRT_IFD.append(np.round(np.mean(IFDtotalMRT[-4:-1]), 2))
        TotalMRT_IFD.append(IFDtotalMRT[-2])
        TotalMRT_IFD.append(IFDtotalMRT[-1])

        #print("CFDtotalPriorityH",CFDtotalPriorityH)
        #print("CFDtotalPriorityM", CFDtotalPriorityM)
        #print("CFDtotalPriorityL", CFDtotalPriorityL)
        #print("CFDtotalPriorityU", CFDtotalPriorityU)

        CFDtotalPriorityHigh.append(np.round(np.mean(CFDtotalPriorityHPer[:-1]), 2))
        CFDtotalPriorityHigh.append(np.round(np.mean(CFDtotalPriorityHPer[-4:-1]), 2))
        CFDtotalPriorityHigh.append(CFDtotalPriorityHPer[-2])
        CFDtotalPriorityHigh.append(CFDtotalPriorityHPer[-1])

        CFDtotalPriorityMedium.append(np.round(np.mean(CFDtotalPriorityMPer[:-1]), 2))
        CFDtotalPriorityMedium.append(np.round(np.mean(CFDtotalPriorityMPer[-4:-1]), 2))
        CFDtotalPriorityMedium.append(CFDtotalPriorityMPer[-2])
        CFDtotalPriorityMedium.append(CFDtotalPriorityMPer[-1])

        CFDtotalPriorityLow.append(np.round(np.mean(CFDtotalPriorityLPer[:-1]), 2))
        CFDtotalPriorityLow.append(np.round(np.mean(CFDtotalPriorityLPer[-4:-1]), 2))
        CFDtotalPriorityLow.append(CFDtotalPriorityLPer[-2])
        CFDtotalPriorityLow.append(CFDtotalPriorityLPer[-1])

        CFDtotalPriorityUrgent.append(np.round(np.mean(CFDtotalPriorityUPer[:-1]), 2))
        CFDtotalPriorityUrgent.append(np.round(np.mean(CFDtotalPriorityUPer[-4:-1]), 2))
        CFDtotalPriorityUrgent.append(CFDtotalPriorityUPer[-2])
        CFDtotalPriorityUrgent.append(CFDtotalPriorityUPer[-1])

        CFDTotalTalk.append(np.round(np.mean(TotalTalkPer[:-1]), 2))
        CFDTotalTalk.append(np.round(np.mean(TotalTalkPer[-4:-1]), 2))
        CFDTotalTalk.append(TotalTalkPer[-2])
        CFDTotalTalk.append(TotalTalkPer[-1])

        CFDTotalCC.append(np.round(np.mean(TotalCCPer[:-1]), 2))
        CFDTotalCC.append(np.round(np.mean(TotalCCPer[-4:-1]), 2))
        CFDTotalCC.append(TotalCCPer[-2])
        CFDTotalCC.append(TotalCCPer[-1])

        CFDTotalINT.append(np.round(np.mean(TotalINTPer[:-1]), 2))
        CFDTotalINT.append(np.round(np.mean(TotalINTPer[-4:-1]), 2))
        CFDTotalINT.append(TotalINTPer[-2])
        CFDTotalINT.append(TotalINTPer[-1])

        CFDTotalOTH.append(np.round(np.mean(TotalOTHPer[:-1]), 2))
        CFDTotalOTH.append(np.round(np.mean(TotalOTHPer[-4:-1]), 2))
        CFDTotalOTH.append(TotalOTHPer[-2])
        CFDTotalOTH.append(TotalOTHPer[-1])


        expectedMRT = (TotalMRT_CFD[1]/TotalFixed_CFD[1])*TotalFixed_CFD[2]
        deltaMRT = np.round((expectedMRT - TotalMRT_CFD[2]),2)
        if deltaMRT >= 0:
            deltasign = 1
        else:
            deltasign = 0

        for i in range(len(TotalMRT_CFD)):
            if np.isnan(TotalMRT_CFD[i]):
                TotalMRT_CFD[i] = 0
            else:
                pass
        for i in range(len(TotalMRT_IFD)):
            if np.isnan(TotalMRT_IFD[i]):
                TotalMRT_IFD[i] = 0
            else:
                pass



    return render(request, 'dialpad.html', {
        "lastupdatedon": CFDLastUpdate,
        "TotalFixed_CFD": TotalFixed_CFD,
        "TotalBackLog_CFD": TotalBackLog_CFD,
        "TotalNoise_CFD": TotalNoise_CFD,
        "TotalMRT_CFD": TotalMRT_CFD,
        "CFDTotalTalk": CFDTotalTalk,
        "CFDTotalCC": CFDTotalCC,
        "CFDTotalINT": CFDTotalINT,
        "CFDTotalOTH": CFDTotalOTH,
        "CFDtotalPriorityHigh": CFDtotalPriorityHigh,
        "CFDtotalPriorityMedium": CFDtotalPriorityMedium,
        "CFDtotalPriorityLow": CFDtotalPriorityLow,
        "CFDtotalPriorityUrgent": CFDtotalPriorityUrgent,
        "deltaMRT": deltaMRT,
        "deltasign": deltasign,
        "TotalFixed_IFD": TotalFixed_IFD,
        "TotalBackLog_IFD": TotalBackLog_IFD,
        "TotalNoise_IFD": TotalNoise_IFD,
        "TotalMRT_IFD": TotalMRT_IFD,


    })


def talk(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        TalkJiras_CFD = []
        TalkFixed_CFD = []
        TalkBackLog_CFD = []
        TalkNoise_CFD = []
        TalkMRT_CFD = []
        CFDTalkPriorityHigh = []
        CFDTalkPriorityMedium = []
        CFDTalkPriorityLow = []
        CFDTalkPriorityUrgent = []
        TalkFixed_IFD = []
        TalkBackLog_IFD = []
        TalkNoise_IFD = []
        TalkMRT_IFD = []

        dialpadoverall = CFD.objects.get(id=1)
        CFDtalkJiras = dialpadoverall.CFDtalkJiras.split(",")
        CFDtalkJiras = list(map(int, CFDtalkJiras))
        CFDtalkFixed = dialpadoverall.CFDtalkFixed.split(",")
        CFDtalkFixed = list(map(int, CFDtalkFixed))
        CFDtalkMRT = dialpadoverall.CFDtalkMRT.split(" ")
        CFDtalkMRT = list(filter(None, CFDtalkMRT))
        CFDtalkMRT = list(map(float, CFDtalkMRT))
        CFDtalkNotClosed = dialpadoverall.CFDtalkNotClosed.split(",")
        CFDtalkNotClosed = list(map(int, CFDtalkNotClosed))
        CFDtalkCurrentFix = dialpadoverall.CFDtalkCurrentFix.split(",")
        CFDtalkCurrentFix = list(map(int, CFDtalkCurrentFix))
        CFDtalkNoise = dialpadoverall.CFDtalkNoise.split(",")
        CFDtalkNoise = list(map(int, CFDtalkNoise))
        CFDtalkPriorityH = dialpadoverall.CFDtalkPriorityH.split(",")
        CFDtalkPriorityH = list(map(int, CFDtalkPriorityH))
        CFDtalkPriorityM = dialpadoverall.CFDtalkPriorityM.split(",")
        CFDtalkPriorityM = list(map(int, CFDtalkPriorityM))
        CFDtalkPriorityL = dialpadoverall.CFDtalkPriorityL.split(",")
        CFDtalkPriorityL = list(map(int, CFDtalkPriorityL))
        CFDtalkPriorityU = dialpadoverall.CFDtalkPriorityU.split(",")
        CFDtalkPriorityU = list(map(int, CFDtalkPriorityU))

        ifd_dialpadoverall = IFD.objects.get(id=1)
        IFDtalkJiras = ifd_dialpadoverall.IFDtalkJiras.split(",")
        IFDtalkJiras = list(map(int, IFDtalkJiras))
        IFDtalkFixed = ifd_dialpadoverall.IFDtalkFixed.split(",")
        IFDtalkFixed = list(map(int, IFDtalkFixed))
        IFDtalkMRT = ifd_dialpadoverall.IFDtalkMRT.split(" ")
        IFDtalkMRT = list(filter(None, IFDtalkMRT))
        IFDtalkMRT = list(map(float, IFDtalkMRT))
        IFDtalkNotClosed = ifd_dialpadoverall.IFDtalkNotClosed.split(",")
        IFDtalkNotClosed = list(map(int, IFDtalkNotClosed))
        IFDtalkCurrentFix = ifd_dialpadoverall.IFDtalkCurrentFix.split(",")
        IFDtalkCurrentFix = list(map(int, IFDtalkCurrentFix))
        IFDtalkNoise = ifd_dialpadoverall.IFDtalkNoise.split(",")
        IFDtalkNoise = list(map(int, IFDtalkNoise))
        CFDLastUpdate = dialpadoverall.CFDLastUpdate

        for i in range(len(CFDtalkJiras)):
            if CFDtalkJiras[i] == 0:
                CFDtalkJiras[i] = 1
            else:
                pass
        for i in range(len(IFDtalkJiras)):
            if IFDtalkJiras[i] == 0:
                IFDtalkJiras[i] = 1
            else:
                pass

        for i in range(len(CFDtalkMRT)):
            if np.isnan(CFDtalkMRT[i]):
                CFDtalkMRT[i] = 0.05
            else:
                pass
        for i in range(len(IFDtalkMRT)):
            if np.isnan(IFDtalkMRT[i]):
                IFDtalkMRT[i] = 0.05
            else:
                pass

        TalkFixedPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkFixed, CFDtalkJiras)]
        TalkBackLogPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkNotClosed, CFDtalkJiras)]
        TalkNoisePer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkNoise, CFDtalkJiras)]
        CFDTalkPriorityHPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkPriorityH, CFDtalkJiras)]
        CFDTalkPriorityMPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkPriorityM, CFDtalkJiras)]
        CFDTalkPriorityLPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkPriorityL, CFDtalkJiras)]
        CFDTalkPriorityUPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDtalkPriorityU, CFDtalkJiras)]

        TalkFixedPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDtalkFixed, IFDtalkJiras)]
        TalkBackLogPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDtalkNotClosed, IFDtalkJiras)]
        TalkNoisePer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDtalkNoise, IFDtalkJiras)]

        TalkJiras_CFD.append(np.round(np.mean(CFDtalkJiras[:-1]), 2))
        TalkJiras_CFD.append(np.round(np.mean(CFDtalkJiras[-4:-1]), 2))
        TalkJiras_CFD.append(CFDtalkJiras[-2])
        TalkJiras_CFD.append(CFDtalkJiras[-1])

        TalkFixed_CFD.append(np.round(np.mean(TalkFixedPer[:-1]),2))
        TalkFixed_CFD.append(np.round(np.mean(TalkFixedPer[-4:-1]), 2))
        TalkFixed_CFD.append(TalkFixedPer[-2])
        TalkFixed_CFD.append(TalkFixedPer[-1])

        TalkBackLog_CFD.append(np.round(np.mean(TalkBackLogPer[:-1]), 2))
        TalkBackLog_CFD.append(np.round(np.mean(TalkBackLogPer[-4:-1]), 2))
        TalkBackLog_CFD.append(TalkBackLogPer[-2])
        TalkBackLog_CFD.append(TalkBackLogPer[-1])

        TalkNoise_CFD.append(np.round(np.mean(TalkNoisePer[:-1]), 2))
        TalkNoise_CFD.append(np.round(np.mean(TalkNoisePer[-4:-1]), 2))
        TalkNoise_CFD.append(TalkNoisePer[-2])
        TalkNoise_CFD.append(TalkNoisePer[-1])

        TalkMRT_CFD.append(np.round(np.mean(CFDtalkMRT[:-1]), 2))
        TalkMRT_CFD.append(np.round(np.mean(CFDtalkMRT[-4:-1]), 2))
        TalkMRT_CFD.append(CFDtalkMRT[-2])
        TalkMRT_CFD.append(CFDtalkMRT[-1])

        TalkFixed_IFD.append(np.round(np.mean(TalkFixedPer_IFD[:-1]), 2))
        TalkFixed_IFD.append(np.round(np.mean(TalkFixedPer_IFD[-4:-1]), 2))
        TalkFixed_IFD.append(TalkFixedPer_IFD[-2])
        TalkFixed_IFD.append(TalkFixedPer_IFD[-1])

        TalkBackLog_IFD.append(np.round(np.mean(TalkBackLogPer_IFD[:-1]), 2))
        TalkBackLog_IFD.append(np.round(np.mean(TalkBackLogPer_IFD[-4:-1]), 2))
        TalkBackLog_IFD.append(TalkBackLogPer_IFD[-2])
        TalkBackLog_IFD.append(TalkBackLogPer_IFD[-1])

        TalkNoise_IFD.append(np.round(np.mean(TalkNoisePer_IFD[:-1]), 2))
        TalkNoise_IFD.append(np.round(np.mean(TalkNoisePer_IFD[-4:-1]), 2))
        TalkNoise_IFD.append(TalkNoisePer_IFD[-2])
        TalkNoise_IFD.append(TalkNoisePer_IFD[-1])

        TalkMRT_IFD.append(np.round(np.mean(IFDtalkMRT[:-1]), 2))
        TalkMRT_IFD.append(np.round(np.mean(IFDtalkMRT[-4:-1]), 2))
        TalkMRT_IFD.append(IFDtalkMRT[-2])
        TalkMRT_IFD.append(IFDtalkMRT[-1])

        CFDTalkPriorityHigh.append(np.round(np.mean(CFDTalkPriorityHPer[:-1]), 2))
        CFDTalkPriorityHigh.append(np.round(np.mean(CFDTalkPriorityHPer[-4:-1]), 2))
        CFDTalkPriorityHigh.append(CFDTalkPriorityHPer[-2])
        CFDTalkPriorityHigh.append(CFDTalkPriorityHPer[-1])

        CFDTalkPriorityMedium.append(np.round(np.mean(CFDTalkPriorityMPer[:-1]), 2))
        CFDTalkPriorityMedium.append(np.round(np.mean(CFDTalkPriorityMPer[-4:-1]), 2))
        CFDTalkPriorityMedium.append(CFDTalkPriorityMPer[-2])
        CFDTalkPriorityMedium.append(CFDTalkPriorityMPer[-1])

        CFDTalkPriorityLow.append(np.round(np.mean(CFDTalkPriorityLPer[:-1]), 2))
        CFDTalkPriorityLow.append(np.round(np.mean(CFDTalkPriorityLPer[-4:-1]), 2))
        CFDTalkPriorityLow.append(CFDTalkPriorityLPer[-2])
        CFDTalkPriorityLow.append(CFDTalkPriorityLPer[-1])

        CFDTalkPriorityUrgent.append(np.round(np.mean(CFDTalkPriorityUPer[:-1]), 2))
        CFDTalkPriorityUrgent.append(np.round(np.mean(CFDTalkPriorityUPer[-4:-1]), 2))
        CFDTalkPriorityUrgent.append(CFDTalkPriorityUPer[-2])
        CFDTalkPriorityUrgent.append(CFDTalkPriorityUPer[-1])

        expectedMRT = (TalkMRT_CFD[1] / TalkFixed_CFD[1]) * TalkFixed_CFD[2]
        deltaMRT = np.round((expectedMRT - TalkMRT_CFD[2]), 2)
        if deltaMRT >= 0:
            deltasign = 1
        else:
            deltasign = 0

        for i in range(len(TalkMRT_CFD)):
            if np.isnan(TalkMRT_CFD[i]):
                TalkMRT_CFD[i] = 0
            else:
                pass
        for i in range(len(TalkMRT_IFD)):
            if np.isnan(TalkMRT_IFD[i]):
                TalkMRT_IFD[i] = 0
            else:
                pass

    return render(request, 'talk.html', {
        "lastupdatedon": CFDLastUpdate,
        "TalkFixed_CFD": TalkFixed_CFD,
        "TalkBackLog_CFD": TalkBackLog_CFD,
        "TalkNoise_CFD": TalkNoise_CFD,
        "TalkMRT_CFD": TalkMRT_CFD,
        "TalkJiras_CFD": TalkJiras_CFD,
        "CFDTalkPriorityHigh": CFDTalkPriorityHigh,
        "CFDTalkPriorityMedium": CFDTalkPriorityMedium,
        "CFDTalkPriorityLow": CFDTalkPriorityLow,
        "CFDTalkPriorityUrgent": CFDTalkPriorityUrgent,
        "deltaMRT": deltaMRT,
        "deltasign": deltasign,
        "TalkFixed_IFD": TalkFixed_IFD,
        "TalkBackLog_IFD": TalkBackLog_IFD,
        "TalkNoise_IFD": TalkNoise_IFD,
        "TalkMRT_IFD": TalkMRT_IFD,


    })

def contactcenter(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        CCJiras_CFD = []
        CCFixed_CFD = []
        CCBackLog_CFD = []
        CCNoise_CFD = []
        CCMRT_CFD = []
        CFDCCPriorityHigh = []
        CFDCCPriorityMedium = []
        CFDCCPriorityLow = []
        CFDCCPriorityUrgent = []
        CCFixed_IFD = []
        CCBackLog_IFD = []
        CCNoise_IFD = []
        CCMRT_IFD = []

        dialpadoverall = CFD.objects.get(id=1)
        CFDCCJiras = dialpadoverall.CFDCCJiras.split(",")
        CFDCCJiras = list(map(int, CFDCCJiras))
        CFDCCFixed = dialpadoverall.CFDCCFixed.split(",")
        CFDCCFixed = list(map(int, CFDCCFixed))
        CFDCCMRT = dialpadoverall.CFDCCMRT.split(" ")
        CFDCCMRT = list(filter(None, CFDCCMRT))
        CFDCCMRT = list(map(float, CFDCCMRT))
        CFDCCNotClosed = dialpadoverall.CFDCCNotClosed.split(",")
        CFDCCNotClosed = list(map(int, CFDCCNotClosed))
        CFDCCCurrentFix = dialpadoverall.CFDCCCurrentFix.split(",")
        CFDCCCurrentFix = list(map(int, CFDCCCurrentFix))
        CFDCCNoise = dialpadoverall.CFDCCNoise.split(",")
        CFDCCNoise = list(map(int, CFDCCNoise))
        CFDCCPriorityH = dialpadoverall.CFDCCPriorityH.split(",")
        CFDCCPriorityH = list(map(int, CFDCCPriorityH))
        CFDCCPriorityM = dialpadoverall.CFDCCPriorityM.split(",")
        CFDCCPriorityM = list(map(int, CFDCCPriorityM))
        CFDCCPriorityL = dialpadoverall.CFDCCPriorityL.split(",")
        CFDCCPriorityL = list(map(int, CFDCCPriorityL))
        CFDCCPriorityU = dialpadoverall.CFDCCPriorityU.split(",")
        CFDCCPriorityU = list(map(int, CFDCCPriorityU))

        ifd_dialpadoverall = IFD.objects.get(id=1)
        IFDCCJiras = ifd_dialpadoverall.IFDCCJiras.split(",")
        IFDCCJiras = list(map(int, IFDCCJiras))
        IFDCCFixed = ifd_dialpadoverall.IFDCCFixed.split(",")
        IFDCCFixed = list(map(int, IFDCCFixed))
        IFDCCMRT = ifd_dialpadoverall.IFDCCMRT.split(" ")
        IFDCCMRT = list(filter(None, IFDCCMRT))
        IFDCCMRT = list(map(float, IFDCCMRT))
        IFDCCNotClosed = ifd_dialpadoverall.IFDCCNotClosed.split(",")
        IFDCCNotClosed = list(map(int, IFDCCNotClosed))
        IFDCCCurrentFix = ifd_dialpadoverall.IFDCCCurrentFix.split(",")
        IFDCCCurrentFix = list(map(int, IFDCCCurrentFix))
        IFDCCNoise = ifd_dialpadoverall.IFDCCNoise.split(",")
        IFDCCNoise = list(map(int, IFDCCNoise))
        CFDLastUpdate = dialpadoverall.CFDLastUpdate

        for i in range(len(CFDCCJiras)):
            if CFDCCJiras[i] == 0:
                CFDCCJiras[i] = 1
            else:
                pass
        for i in range(len(IFDCCJiras)):
            if IFDCCJiras[i] == 0:
                IFDCCJiras[i] = 1
            else:
                pass

        for i in range(len(CFDCCMRT)):
            if np.isnan(CFDCCMRT[i]):
                CFDCCMRT[i] = 0.05
            else:
                pass
        for i in range(len(IFDCCMRT)):
            if np.isnan(IFDCCMRT[i]):
                IFDCCMRT[i] = 0.05
            else:
                pass

        CCFixedPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCFixed, CFDCCJiras)]
        CCBackLogPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCNotClosed, CFDCCJiras)]
        CCNoisePer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCNoise, CFDCCJiras)]
        CFDCCPriorityHPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCPriorityH, CFDCCJiras)]
        CFDCCPriorityMPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCPriorityM, CFDCCJiras)]
        CFDCCPriorityLPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCPriorityL, CFDCCJiras)]
        CFDCCPriorityUPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDCCPriorityU, CFDCCJiras)]

        CCFixedPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDCCFixed, IFDCCJiras)]
        CCBackLogPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDCCNotClosed, IFDCCJiras)]
        CCNoisePer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDCCNoise, IFDCCJiras)]

        CCJiras_CFD.append(np.round(np.mean(CFDCCJiras[:-1]), 2))
        CCJiras_CFD.append(np.round(np.mean(CFDCCJiras[-4:-1]), 2))
        CCJiras_CFD.append(CFDCCJiras[-2])
        CCJiras_CFD.append(CFDCCJiras[-1])

        CCFixed_CFD.append(np.round(np.mean(CCFixedPer[:-1]),2))
        CCFixed_CFD.append(np.round(np.mean(CCFixedPer[-4:-1]), 2))
        CCFixed_CFD.append(CCFixedPer[-2])
        CCFixed_CFD.append(CCFixedPer[-1])

        CCBackLog_CFD.append(np.round(np.mean(CCBackLogPer[:-1]), 2))
        CCBackLog_CFD.append(np.round(np.mean(CCBackLogPer[-4:-1]), 2))
        CCBackLog_CFD.append(CCBackLogPer[-2])
        CCBackLog_CFD.append(CCBackLogPer[-1])

        CCNoise_CFD.append(np.round(np.mean(CCNoisePer[:-1]), 2))
        CCNoise_CFD.append(np.round(np.mean(CCNoisePer[-4:-1]), 2))
        CCNoise_CFD.append(CCNoisePer[-2])
        CCNoise_CFD.append(CCNoisePer[-1])

        CCMRT_CFD.append(np.round(np.mean(CFDCCMRT[:-1]), 2))
        CCMRT_CFD.append(np.round(np.mean(CFDCCMRT[-4:-1]), 2))
        CCMRT_CFD.append(CFDCCMRT[-2])
        CCMRT_CFD.append(CFDCCMRT[-1])

        CCFixed_IFD.append(np.round(np.mean(CCFixedPer_IFD[:-1]), 2))
        CCFixed_IFD.append(np.round(np.mean(CCFixedPer_IFD[-4:-1]), 2))
        CCFixed_IFD.append(CCFixedPer_IFD[-2])
        CCFixed_IFD.append(CCFixedPer_IFD[-1])

        CCBackLog_IFD.append(np.round(np.mean(CCBackLogPer_IFD[:-1]), 2))
        CCBackLog_IFD.append(np.round(np.mean(CCBackLogPer_IFD[-4:-1]), 2))
        CCBackLog_IFD.append(CCBackLogPer_IFD[-2])
        CCBackLog_IFD.append(CCBackLogPer_IFD[-1])

        CCNoise_IFD.append(np.round(np.mean(CCNoisePer_IFD[:-1]), 2))
        CCNoise_IFD.append(np.round(np.mean(CCNoisePer_IFD[-4:-1]), 2))
        CCNoise_IFD.append(CCNoisePer_IFD[-2])
        CCNoise_IFD.append(CCNoisePer_IFD[-1])

        CCMRT_IFD.append(np.round(np.mean(IFDCCMRT[:-1]), 2))
        CCMRT_IFD.append(np.round(np.mean(IFDCCMRT[-4:-1]), 2))
        CCMRT_IFD.append(IFDCCMRT[-2])
        CCMRT_IFD.append(IFDCCMRT[-1])

        CFDCCPriorityHigh.append(np.round(np.mean(CFDCCPriorityHPer[:-1]), 2))
        CFDCCPriorityHigh.append(np.round(np.mean(CFDCCPriorityHPer[-4:-1]), 2))
        CFDCCPriorityHigh.append(CFDCCPriorityHPer[-2])
        CFDCCPriorityHigh.append(CFDCCPriorityHPer[-1])

        CFDCCPriorityMedium.append(np.round(np.mean(CFDCCPriorityMPer[:-1]), 2))
        CFDCCPriorityMedium.append(np.round(np.mean(CFDCCPriorityMPer[-4:-1]), 2))
        CFDCCPriorityMedium.append(CFDCCPriorityMPer[-2])
        CFDCCPriorityMedium.append(CFDCCPriorityMPer[-1])

        CFDCCPriorityLow.append(np.round(np.mean(CFDCCPriorityLPer[:-1]), 2))
        CFDCCPriorityLow.append(np.round(np.mean(CFDCCPriorityLPer[-4:-1]), 2))
        CFDCCPriorityLow.append(CFDCCPriorityLPer[-2])
        CFDCCPriorityLow.append(CFDCCPriorityLPer[-1])

        CFDCCPriorityUrgent.append(np.round(np.mean(CFDCCPriorityUPer[:-1]), 2))
        CFDCCPriorityUrgent.append(np.round(np.mean(CFDCCPriorityUPer[-4:-1]), 2))
        CFDCCPriorityUrgent.append(CFDCCPriorityUPer[-2])
        CFDCCPriorityUrgent.append(CFDCCPriorityUPer[-1])

        expectedMRT = (CCMRT_CFD[1] / CCFixed_CFD[1]) * CCFixed_CFD[2]
        deltaMRT = np.round((expectedMRT - CCMRT_CFD[2]), 2)
        if deltaMRT >= 0:
            deltasign = 1
        else:
            deltasign = 0

        for i in range(len(CCMRT_CFD)):
            if np.isnan(CCMRT_CFD[i]):
                CCMRT_CFD[i] = 0
            else:
                pass
        for i in range(len(CCMRT_IFD)):
            if np.isnan(CCMRT_IFD[i]):
                CCMRT_IFD[i] = 0
            else:
                pass

    return render(request, 'contactcenter.html', {
        "lastupdatedon": CFDLastUpdate,
        "CCFixed_CFD": CCFixed_CFD,
        "CCBackLog_CFD": CCBackLog_CFD,
        "CCNoise_CFD": CCNoise_CFD,
        "CCMRT_CFD": CCMRT_CFD,
        "CCJiras_CFD": CCJiras_CFD,
        "CFDCCPriorityHigh": CFDCCPriorityHigh,
        "CFDCCPriorityMedium": CFDCCPriorityMedium,
        "CFDCCPriorityLow": CFDCCPriorityLow,
        "CFDCCPriorityUrgent": CFDCCPriorityUrgent,
        "deltaMRT": deltaMRT,
        "deltasign": deltasign,
        "CCFixed_IFD": CCFixed_IFD,
        "CCBackLog_IFD": CCBackLog_IFD,
        "CCNoise_IFD": CCNoise_IFD,
        "CCMRT_IFD": CCMRT_IFD,


    })

def integration(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        INTJiras_CFD = []
        INTFixed_CFD = []
        INTBackLog_CFD = []
        INTNoise_CFD = []
        INTMRT_CFD = []
        CFDINTPriorityHigh = []
        CFDINTPriorityMedium = []
        CFDINTPriorityLow = []
        CFDINTPriorityUrgent = []
        INTFixed_IFD = []
        INTBackLog_IFD = []
        INTNoise_IFD = []
        INTMRT_IFD = []

        dialpadoverall = CFD.objects.get(id=1)
        CFDINTJiras = dialpadoverall.CFDINTJiras.split(",")
        CFDINTJiras = list(map(int, CFDINTJiras))
        CFDINTFixed = dialpadoverall.CFDINTFixed.split(",")
        CFDINTFixed = list(map(int, CFDINTFixed))
        CFDINTMRT = dialpadoverall.CFDINTMRT.split(" ")
        CFDINTMRT = list(filter(None, CFDINTMRT))
        CFDINTMRT = list(map(float, CFDINTMRT))
        CFDINTNotClosed = dialpadoverall.CFDINTNotClosed.split(",")
        CFDINTNotClosed = list(map(int, CFDINTNotClosed))
        CFDINTCurrentFix = dialpadoverall.CFDINTCurrentFix.split(",")
        CFDINTCurrentFix = list(map(int, CFDINTCurrentFix))
        CFDINTNoise = dialpadoverall.CFDINTNoise.split(",")
        CFDINTNoise = list(map(int, CFDINTNoise))
        CFDINTPriorityH = dialpadoverall.CFDINTPriorityH.split(",")
        CFDINTPriorityH = list(map(int, CFDINTPriorityH))
        CFDINTPriorityM = dialpadoverall.CFDINTPriorityM.split(",")
        CFDINTPriorityM = list(map(int, CFDINTPriorityM))
        CFDINTPriorityL = dialpadoverall.CFDINTPriorityL.split(",")
        CFDINTPriorityL = list(map(int, CFDINTPriorityL))
        CFDINTPriorityU = dialpadoverall.CFDINTPriorityU.split(",")
        CFDINTPriorityU = list(map(int, CFDINTPriorityU))

        ifd_dialpadoverall = IFD.objects.get(id=1)
        IFDINTJiras = ifd_dialpadoverall.IFDINTJiras.split(",")
        IFDINTJiras = list(map(int, IFDINTJiras))
        IFDINTFixed = ifd_dialpadoverall.IFDINTFixed.split(",")
        IFDINTFixed = list(map(int, IFDINTFixed))
        IFDINTMRT = ifd_dialpadoverall.IFDINTMRT.split(" ")
        IFDINTMRT = list(filter(None, IFDINTMRT))
        IFDINTMRT = list(map(float, IFDINTMRT))
        IFDINTNotClosed = ifd_dialpadoverall.IFDINTNotClosed.split(",")
        IFDINTNotClosed = list(map(int, IFDINTNotClosed))
        IFDINTCurrentFix = ifd_dialpadoverall.IFDINTCurrentFix.split(",")
        IFDINTCurrentFix = list(map(int, IFDINTCurrentFix))
        IFDINTNoise = ifd_dialpadoverall.IFDINTNoise.split(",")
        IFDINTNoise = list(map(int, IFDINTNoise))
        CFDLastUpdate = dialpadoverall.CFDLastUpdate

        for i in range(len(CFDINTJiras)):
            if CFDINTJiras[i] == 0:
                CFDINTJiras[i] = 1
            else:
                pass
        for i in range(len(IFDINTJiras)):
            if IFDINTJiras[i] == 0:
                IFDINTJiras[i] = 1
            else:
                pass

        for i in range(len(CFDINTMRT)):
            if np.isnan(CFDINTMRT[i]):
                CFDINTMRT[i] = 0.05
            else:
                pass
        for i in range(len(IFDINTMRT)):
            if np.isnan(IFDINTMRT[i]):
                IFDINTMRT[i] = 0.05
            else:
                pass

        INTFixedPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTFixed, CFDINTJiras)]
        INTBackLogPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTNotClosed, CFDINTJiras)]
        INTNoisePer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTNoise, CFDINTJiras)]
        CFDINTPriorityHPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTPriorityH, CFDINTJiras)]
        CFDINTPriorityMPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTPriorityM, CFDINTJiras)]
        CFDINTPriorityLPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTPriorityL, CFDINTJiras)]
        CFDINTPriorityUPer = [np.round((a / b) * 100, 2) for a, b in zip(CFDINTPriorityU, CFDINTJiras)]

        INTFixedPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDINTFixed, IFDINTJiras)]
        INTBackLogPer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDINTNotClosed, IFDINTJiras)]
        INTNoisePer_IFD = [np.round((a / b) * 100, 2) for a, b in zip(IFDINTNoise, IFDINTJiras)]

        INTJiras_CFD.append(np.round(np.mean(CFDINTJiras[:-1]), 2))
        INTJiras_CFD.append(np.round(np.mean(CFDINTJiras[-4:-1]), 2))
        INTJiras_CFD.append(CFDINTJiras[-2])
        INTJiras_CFD.append(CFDINTJiras[-1])

        INTFixed_CFD.append(np.round(np.mean(INTFixedPer[:-1]),2))
        INTFixed_CFD.append(np.round(np.mean(INTFixedPer[-4:-1]), 2))
        INTFixed_CFD.append(INTFixedPer[-2])
        INTFixed_CFD.append(INTFixedPer[-1])

        INTBackLog_CFD.append(np.round(np.mean(INTBackLogPer[:-1]), 2))
        INTBackLog_CFD.append(np.round(np.mean(INTBackLogPer[-4:-1]), 2))
        INTBackLog_CFD.append(INTBackLogPer[-2])
        INTBackLog_CFD.append(INTBackLogPer[-1])

        INTNoise_CFD.append(np.round(np.mean(INTNoisePer[:-1]), 2))
        INTNoise_CFD.append(np.round(np.mean(INTNoisePer[-4:-1]), 2))
        INTNoise_CFD.append(INTNoisePer[-2])
        INTNoise_CFD.append(INTNoisePer[-1])

        INTMRT_CFD.append(np.round(np.mean(CFDINTMRT[:-1]), 2))
        INTMRT_CFD.append(np.round(np.mean(CFDINTMRT[-4:-1]), 2))
        INTMRT_CFD.append(CFDINTMRT[-2])
        INTMRT_CFD.append(CFDINTMRT[-1])

        INTFixed_IFD.append(np.round(np.mean(INTFixedPer_IFD[:-1]), 2))
        INTFixed_IFD.append(np.round(np.mean(INTFixedPer_IFD[-4:-1]), 2))
        INTFixed_IFD.append(INTFixedPer_IFD[-2])
        INTFixed_IFD.append(INTFixedPer_IFD[-1])

        INTBackLog_IFD.append(np.round(np.mean(INTBackLogPer_IFD[:-1]), 2))
        INTBackLog_IFD.append(np.round(np.mean(INTBackLogPer_IFD[-4:-1]), 2))
        INTBackLog_IFD.append(INTBackLogPer_IFD[-2])
        INTBackLog_IFD.append(INTBackLogPer_IFD[-1])

        INTNoise_IFD.append(np.round(np.mean(INTNoisePer_IFD[:-1]), 2))
        INTNoise_IFD.append(np.round(np.mean(INTNoisePer_IFD[-4:-1]), 2))
        INTNoise_IFD.append(INTNoisePer_IFD[-2])
        INTNoise_IFD.append(INTNoisePer_IFD[-1])

        INTMRT_IFD.append(np.round(np.mean(IFDINTMRT[:-1]), 2))
        INTMRT_IFD.append(np.round(np.mean(IFDINTMRT[-4:-1]), 2))
        INTMRT_IFD.append(IFDINTMRT[-2])
        INTMRT_IFD.append(IFDINTMRT[-1])

        CFDINTPriorityHigh.append(np.round(np.mean(CFDINTPriorityHPer[:-1]), 2))
        CFDINTPriorityHigh.append(np.round(np.mean(CFDINTPriorityHPer[-4:-1]), 2))
        CFDINTPriorityHigh.append(CFDINTPriorityHPer[-2])
        CFDINTPriorityHigh.append(CFDINTPriorityHPer[-1])

        CFDINTPriorityMedium.append(np.round(np.mean(CFDINTPriorityMPer[:-1]), 2))
        CFDINTPriorityMedium.append(np.round(np.mean(CFDINTPriorityMPer[-4:-1]), 2))
        CFDINTPriorityMedium.append(CFDINTPriorityMPer[-2])
        CFDINTPriorityMedium.append(CFDINTPriorityMPer[-1])

        CFDINTPriorityLow.append(np.round(np.mean(CFDINTPriorityLPer[:-1]), 2))
        CFDINTPriorityLow.append(np.round(np.mean(CFDINTPriorityLPer[-4:-1]), 2))
        CFDINTPriorityLow.append(CFDINTPriorityLPer[-2])
        CFDINTPriorityLow.append(CFDINTPriorityLPer[-1])

        CFDINTPriorityUrgent.append(np.round(np.mean(CFDINTPriorityUPer[:-1]), 2))
        CFDINTPriorityUrgent.append(np.round(np.mean(CFDINTPriorityUPer[-4:-1]), 2))
        CFDINTPriorityUrgent.append(CFDINTPriorityUPer[-2])
        CFDINTPriorityUrgent.append(CFDINTPriorityUPer[-1])

        expectedMRT = (INTMRT_CFD[1] / INTFixed_CFD[1]) * INTFixed_CFD[2]
        deltaMRT = np.round((expectedMRT - INTMRT_CFD[2]), 2)
        if deltaMRT >= 0:
            deltasign = 1
        else:
            deltasign = 0

        for i in range(len(INTMRT_CFD)):
            if np.isnan(INTMRT_CFD[i]):
                INTMRT_CFD[i] = 0
            else:
                pass
        for i in range(len(INTMRT_IFD)):
            if np.isnan(INTMRT_IFD[i]):
                INTMRT_IFD[i] = 0
            else:
                pass

    return render(request, 'integration.html', {
        "lastupdatedon": CFDLastUpdate,
        "INTFixed_CFD": INTFixed_CFD,
        "INTBackLog_CFD": INTBackLog_CFD,
        "INTNoise_CFD": INTNoise_CFD,
        "INTMRT_CFD": INTMRT_CFD,
        "INTJiras_CFD": INTJiras_CFD,
        "CFDINTPriorityHigh": CFDINTPriorityHigh,
        "CFDINTPriorityMedium": CFDINTPriorityMedium,
        "CFDINTPriorityLow": CFDINTPriorityLow,
        "CFDINTPriorityUrgent": CFDINTPriorityUrgent,
        "deltaMRT": deltaMRT,
        "deltasign": deltasign,
        "INTFixed_IFD": INTFixed_IFD,
        "INTBackLog_IFD": INTBackLog_IFD,
        "INTNoise_IFD": INTNoise_IFD,
        "INTMRT_IFD": INTMRT_IFD,


    })


def dpmcfd(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        DPM_CFDtotalJiras = []
        DPM_TotalFixed_CFD = []
        DPM_TotalBackLog_CFD = []
        DPM_TotalNoise_CFD = []
        DPM_TotalMRT_CFD = []
        DPM_CFDtotalPriorityHigh = []
        DPM_CFDtotalPriorityMedium = []
        DPM_CFDtotalPriorityLow = []
        DPM_CFDtotalPriorityUrgent = []

        dialpadoverall = CFDDPM.objects.get(id=1)

        DPMCFDtotalJiras = dialpadoverall.DPMCFDtotalJiras.split(",")
        DPMCFDtotalJiras = list(map(int, DPMCFDtotalJiras))
        DPMCFDtotalFixed = dialpadoverall.DPMCFDtotalFixed.split(",")
        DPMCFDtotalFixed = list(map(int, DPMCFDtotalFixed))
        DPMCFDtotalMRT = dialpadoverall.DPMCFDtotalMRT.split(" ")
        DPMCFDtotalMRT = list(filter(None, DPMCFDtotalMRT))
        DPMCFDtotalMRT = list(map(float, DPMCFDtotalMRT))
        DPMCFDtotalNotClosed = dialpadoverall.DPMCFDtotalNotClosed.split(",")
        DPMCFDtotalNotClosed = list(map(int, DPMCFDtotalNotClosed))
        DPMCFDtotalCurrentFix = dialpadoverall.DPMCFDtotalCurrentFix.split(",")
        DPMCFDtotalCurrentFix = list(map(int, DPMCFDtotalCurrentFix))
        DPMCFDtotalNoise = dialpadoverall.DPMCFDtotalNoise.split(",")
        DPMCFDtotalNoise = list(map(int, DPMCFDtotalNoise))
        DPMCFDtotalPriorityH = dialpadoverall.DPMCFDtotalPriorityH.split(",")
        DPMCFDtotalPriorityH = list(map(int, DPMCFDtotalPriorityH))
        DPMCFDtotalPriorityM = dialpadoverall.DPMCFDtotalPriorityM.split(",")
        DPMCFDtotalPriorityM = list(map(int, DPMCFDtotalPriorityM))
        DPMCFDtotalPriorityL = dialpadoverall.DPMCFDtotalPriorityL.split(",")
        DPMCFDtotalPriorityL = list(map(int, DPMCFDtotalPriorityL))
        DPMCFDtotalPriorityU = dialpadoverall.DPMCFDtotalPriorityU.split(",")
        DPMCFDtotalPriorityU = list(map(int, DPMCFDtotalPriorityU))
        DPMCFDLastUpdate = dialpadoverall.DPMCFDLastUpdate


        for i in range(len(DPMCFDtotalJiras)):
            if DPMCFDtotalJiras[i] == 0:
                DPMCFDtotalJiras[i] = 1
            else:
                pass

        for i in range(len(DPMCFDtotalMRT)):
            if np.isnan(DPMCFDtotalMRT[i]):
                DPMCFDtotalMRT[i] = 0.25
            else:
                pass

        DPMTotalFixedPer = [np.round((a / b) * 100, 2) for a, b in zip(DPMCFDtotalFixed, DPMCFDtotalJiras)]
        DPMTotalBackLogPer = [np.round((a / b) * 100, 2) for a, b in zip(DPMCFDtotalNotClosed, DPMCFDtotalJiras)]
        DPMTotalNoisePer = [np.round((a / b) * 100, 2) for a, b in zip(DPMCFDtotalNoise, DPMCFDtotalJiras)]
        DPMCFDtotalPriorityHPer = [np.round((a / b) * 100, 2) for a, b in zip(DPMCFDtotalPriorityH, DPMCFDtotalJiras)]
        DPMCFDtotalPriorityMPer = [np.round((a / b) * 100, 2) for a, b in zip(DPMCFDtotalPriorityM, DPMCFDtotalJiras)]
        DPMCFDtotalPriorityLPer = [np.round((a / b) * 100, 2) for a, b in zip(DPMCFDtotalPriorityL, DPMCFDtotalJiras)]
        DPMCFDtotalPriorityUPer = [np.round((a / b) * 100, 2) for a, b in zip(DPMCFDtotalPriorityU, DPMCFDtotalJiras)]

        DPM_CFDtotalJiras.append(np.round(np.mean(DPMCFDtotalJiras[:-1]), 2))
        DPM_CFDtotalJiras.append(np.round(np.mean(DPMCFDtotalJiras[-4:-1]), 2))
        DPM_CFDtotalJiras.append(DPMCFDtotalJiras[-2])
        DPM_CFDtotalJiras.append(DPMCFDtotalJiras[-1])

        DPM_TotalFixed_CFD.append(np.round(np.mean(DPMTotalFixedPer[:-1]), 2))
        DPM_TotalFixed_CFD.append(np.round(np.mean(DPMTotalFixedPer[-4:-1]), 2))
        DPM_TotalFixed_CFD.append(DPMTotalFixedPer[-2])
        DPM_TotalFixed_CFD.append(DPMTotalFixedPer[-1])

        DPM_TotalBackLog_CFD.append(np.round(np.mean(DPMTotalBackLogPer[:-1]), 2))
        DPM_TotalBackLog_CFD.append(np.round(np.mean(DPMTotalBackLogPer[-4:-1]), 2))
        DPM_TotalBackLog_CFD.append(DPMTotalBackLogPer[-2])
        DPM_TotalBackLog_CFD.append(DPMTotalBackLogPer[-1])

        DPM_TotalNoise_CFD.append(np.round(np.mean(DPMTotalNoisePer[:-1]), 2))
        DPM_TotalNoise_CFD.append(np.round(np.mean(DPMTotalNoisePer[-4:-1]), 2))
        DPM_TotalNoise_CFD.append(DPMTotalNoisePer[-2])
        DPM_TotalNoise_CFD.append(DPMTotalNoisePer[-1])

        DPM_TotalMRT_CFD.append(np.round(np.mean(DPMCFDtotalMRT[:-1]), 2))
        DPM_TotalMRT_CFD.append(np.round(np.mean(DPMCFDtotalMRT[-4:-1]), 2))
        DPM_TotalMRT_CFD.append(DPMCFDtotalMRT[-2])
        DPM_TotalMRT_CFD.append(DPMCFDtotalMRT[-1])

        DPM_CFDtotalPriorityHigh.append(np.round(np.mean(DPMCFDtotalPriorityHPer[:-1]), 2))
        DPM_CFDtotalPriorityHigh.append(np.round(np.mean(DPMCFDtotalPriorityHPer[-4:-1]), 2))
        DPM_CFDtotalPriorityHigh.append(DPMCFDtotalPriorityHPer[-2])
        DPM_CFDtotalPriorityHigh.append(DPMCFDtotalPriorityHPer[-1])

        DPM_CFDtotalPriorityMedium.append(np.round(np.mean(DPMCFDtotalPriorityMPer[:-1]), 2))
        DPM_CFDtotalPriorityMedium.append(np.round(np.mean(DPMCFDtotalPriorityMPer[-4:-1]), 2))
        DPM_CFDtotalPriorityMedium.append(DPMCFDtotalPriorityMPer[-2])
        DPM_CFDtotalPriorityMedium.append(DPMCFDtotalPriorityMPer[-1])

        DPM_CFDtotalPriorityLow.append(np.round(np.mean(DPMCFDtotalPriorityLPer[:-1]), 2))
        DPM_CFDtotalPriorityLow.append(np.round(np.mean(DPMCFDtotalPriorityLPer[-4:-1]), 2))
        DPM_CFDtotalPriorityLow.append(DPMCFDtotalPriorityLPer[-2])
        DPM_CFDtotalPriorityLow.append(DPMCFDtotalPriorityLPer[-1])

        DPM_CFDtotalPriorityUrgent.append(np.round(np.mean(DPMCFDtotalPriorityUPer[:-1]), 2))
        DPM_CFDtotalPriorityUrgent.append(np.round(np.mean(DPMCFDtotalPriorityUPer[-4:-1]), 2))
        DPM_CFDtotalPriorityUrgent.append(DPMCFDtotalPriorityUPer[-2])
        DPM_CFDtotalPriorityUrgent.append(DPMCFDtotalPriorityUPer[-1])

        expectedMRT = (DPM_TotalMRT_CFD[1] / DPM_TotalFixed_CFD[1]) * DPM_TotalFixed_CFD[2]
        deltaMRT = np.round((expectedMRT - DPM_TotalMRT_CFD[2]), 2)
        if deltaMRT >= 0:
            deltasign = 1
        else:
            deltasign = 0

        for i in range(len(DPM_TotalMRT_CFD)):
            if np.isnan(DPM_TotalMRT_CFD[i]):
                DPM_TotalMRT_CFD[i] = 0
            else:
                pass
        for i in range(len(DPM_TotalMRT_CFD)):
            if np.isnan(DPM_TotalMRT_CFD[i]):
                DPM_TotalMRT_CFD[i] = 0
            else:
                pass

        return render(request, 'dpmcfd.html', {
            "lastupdatedon": DPMCFDLastUpdate,
            "DPM_CFDtotalJiras": DPM_CFDtotalJiras,
            "DPM_TotalFixed_CFD": DPM_TotalFixed_CFD,
            "DPM_TotalBackLog_CFD": DPM_TotalBackLog_CFD,
            "DPM_TotalNoise_CFD": DPM_TotalNoise_CFD,
            "DPM_TotalMRT_CFD": DPM_TotalMRT_CFD,
            "DPM_CFDtotalPriorityHigh": DPM_CFDtotalPriorityHigh,
            "DPM_CFDtotalPriorityMedium": DPM_CFDtotalPriorityMedium,
            "DPM_CFDtotalPriorityLow": DPM_CFDtotalPriorityLow,
            "DPM_CFDtotalPriorityUrgent": DPM_CFDtotalPriorityUrgent,
            "deltaMRT": deltaMRT,
            "deltasign": deltasign,

})


def mobcfd(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:
        MOB_CFDtotalJiras = []
        MOB_TotalFixed_CFD = []
        MOB_TotalBackLog_CFD = []
        MOB_TotalNoise_CFD = []
        MOB_TotalMRT_CFD = []
        MOB_CFDtotalPriorityHigh = []
        MOB_CFDtotalPriorityMedium = []
        MOB_CFDtotalPriorityLow = []
        MOB_CFDtotalPriorityUrgent = []

        dialpadoverall = CFDMOB.objects.get(id=1)

        MOBCFDtotalJiras = dialpadoverall.MOBCFDtotalJiras.split(",")
        MOBCFDtotalJiras = list(map(int, MOBCFDtotalJiras))
        MOBCFDtotalFixed = dialpadoverall.MOBCFDtotalFixed.split(",")
        MOBCFDtotalFixed = list(map(int, MOBCFDtotalFixed))
        MOBCFDtotalMRT = dialpadoverall.MOBCFDtotalMRT.split(" ")
        MOBCFDtotalMRT = list(filter(None, MOBCFDtotalMRT))
        MOBCFDtotalMRT = list(map(float, MOBCFDtotalMRT))
        MOBCFDtotalNotClosed = dialpadoverall.MOBCFDtotalNotClosed.split(",")
        MOBCFDtotalNotClosed = list(map(int, MOBCFDtotalNotClosed))
        MOBCFDtotalCurrentFix = dialpadoverall.MOBCFDtotalCurrentFix.split(",")
        MOBCFDtotalCurrentFix = list(map(int, MOBCFDtotalCurrentFix))
        MOBCFDtotalNoise = dialpadoverall.MOBCFDtotalNoise.split(",")
        MOBCFDtotalNoise = list(map(int, MOBCFDtotalNoise))
        MOBCFDtotalPriorityH = dialpadoverall.MOBCFDtotalPriorityH.split(",")
        MOBCFDtotalPriorityH = list(map(int, MOBCFDtotalPriorityH))
        MOBCFDtotalPriorityM = dialpadoverall.MOBCFDtotalPriorityM.split(",")
        MOBCFDtotalPriorityM = list(map(int, MOBCFDtotalPriorityM))
        MOBCFDtotalPriorityL = dialpadoverall.MOBCFDtotalPriorityL.split(",")
        MOBCFDtotalPriorityL = list(map(int, MOBCFDtotalPriorityL))
        MOBCFDtotalPriorityU = dialpadoverall.MOBCFDtotalPriorityU.split(",")
        MOBCFDtotalPriorityU = list(map(int, MOBCFDtotalPriorityU))
        MOBCFDLastUpdate = dialpadoverall.MOBCFDLastUpdate


        for i in range(len(MOBCFDtotalJiras)):
            if MOBCFDtotalJiras[i] == 0:
                MOBCFDtotalJiras[i] = 1
            else:
                pass

        for i in range(len(MOBCFDtotalMRT)):
            if np.isnan(MOBCFDtotalMRT[i]):
                MOBCFDtotalMRT[i] = 0.25
            else:
                pass

        MOBTotalFixedPer = [np.round((a / b) * 100, 2) for a, b in zip(MOBCFDtotalFixed, MOBCFDtotalJiras)]
        MOBTotalBackLogPer = [np.round((a / b) * 100, 2) for a, b in zip(MOBCFDtotalNotClosed, MOBCFDtotalJiras)]
        MOBTotalNoisePer = [np.round((a / b) * 100, 2) for a, b in zip(MOBCFDtotalNoise, MOBCFDtotalJiras)]
        MOBCFDtotalPriorityHPer = [np.round((a / b) * 100, 2) for a, b in zip(MOBCFDtotalPriorityH, MOBCFDtotalJiras)]
        MOBCFDtotalPriorityMPer = [np.round((a / b) * 100, 2) for a, b in zip(MOBCFDtotalPriorityM, MOBCFDtotalJiras)]
        MOBCFDtotalPriorityLPer = [np.round((a / b) * 100, 2) for a, b in zip(MOBCFDtotalPriorityL, MOBCFDtotalJiras)]
        MOBCFDtotalPriorityUPer = [np.round((a / b) * 100, 2) for a, b in zip(MOBCFDtotalPriorityU, MOBCFDtotalJiras)]

        MOB_CFDtotalJiras.append(np.round(np.mean(MOBCFDtotalJiras[:-1]), 2))
        MOB_CFDtotalJiras.append(np.round(np.mean(MOBCFDtotalJiras[-4:-1]), 2))
        MOB_CFDtotalJiras.append(MOBCFDtotalJiras[-2])
        MOB_CFDtotalJiras.append(MOBCFDtotalJiras[-1])

        MOB_TotalFixed_CFD.append(np.round(np.mean(MOBTotalFixedPer[:-1]), 2))
        MOB_TotalFixed_CFD.append(np.round(np.mean(MOBTotalFixedPer[-4:-1]), 2))
        MOB_TotalFixed_CFD.append(MOBTotalFixedPer[-2])
        MOB_TotalFixed_CFD.append(MOBTotalFixedPer[-1])

        MOB_TotalBackLog_CFD.append(np.round(np.mean(MOBTotalBackLogPer[:-1]), 2))
        MOB_TotalBackLog_CFD.append(np.round(np.mean(MOBTotalBackLogPer[-4:-1]), 2))
        MOB_TotalBackLog_CFD.append(MOBTotalBackLogPer[-2])
        MOB_TotalBackLog_CFD.append(MOBTotalBackLogPer[-1])

        MOB_TotalNoise_CFD.append(np.round(np.mean(MOBTotalNoisePer[:-1]), 2))
        MOB_TotalNoise_CFD.append(np.round(np.mean(MOBTotalNoisePer[-4:-1]), 2))
        MOB_TotalNoise_CFD.append(MOBTotalNoisePer[-2])
        MOB_TotalNoise_CFD.append(MOBTotalNoisePer[-1])

        MOB_TotalMRT_CFD.append(np.round(np.mean(MOBCFDtotalMRT[:-1]), 2))
        MOB_TotalMRT_CFD.append(np.round(np.mean(MOBCFDtotalMRT[-4:-1]), 2))
        MOB_TotalMRT_CFD.append(MOBCFDtotalMRT[-2])
        MOB_TotalMRT_CFD.append(MOBCFDtotalMRT[-1])

        MOB_CFDtotalPriorityHigh.append(np.round(np.mean(MOBCFDtotalPriorityHPer[:-1]), 2))
        MOB_CFDtotalPriorityHigh.append(np.round(np.mean(MOBCFDtotalPriorityHPer[-4:-1]), 2))
        MOB_CFDtotalPriorityHigh.append(MOBCFDtotalPriorityHPer[-2])
        MOB_CFDtotalPriorityHigh.append(MOBCFDtotalPriorityHPer[-1])

        MOB_CFDtotalPriorityMedium.append(np.round(np.mean(MOBCFDtotalPriorityMPer[:-1]), 2))
        MOB_CFDtotalPriorityMedium.append(np.round(np.mean(MOBCFDtotalPriorityMPer[-4:-1]), 2))
        MOB_CFDtotalPriorityMedium.append(MOBCFDtotalPriorityMPer[-2])
        MOB_CFDtotalPriorityMedium.append(MOBCFDtotalPriorityMPer[-1])

        MOB_CFDtotalPriorityLow.append(np.round(np.mean(MOBCFDtotalPriorityLPer[:-1]), 2))
        MOB_CFDtotalPriorityLow.append(np.round(np.mean(MOBCFDtotalPriorityLPer[-4:-1]), 2))
        MOB_CFDtotalPriorityLow.append(MOBCFDtotalPriorityLPer[-2])
        MOB_CFDtotalPriorityLow.append(MOBCFDtotalPriorityLPer[-1])

        MOB_CFDtotalPriorityUrgent.append(np.round(np.mean(MOBCFDtotalPriorityUPer[:-1]), 2))
        MOB_CFDtotalPriorityUrgent.append(np.round(np.mean(MOBCFDtotalPriorityUPer[-4:-1]), 2))
        MOB_CFDtotalPriorityUrgent.append(MOBCFDtotalPriorityUPer[-2])
        MOB_CFDtotalPriorityUrgent.append(MOBCFDtotalPriorityUPer[-1])

        expectedMRT = (MOB_TotalMRT_CFD[1] / MOB_TotalFixed_CFD[1]) * MOB_TotalFixed_CFD[2]
        deltaMRT = np.round((expectedMRT - MOB_TotalMRT_CFD[2]), 2)
        if deltaMRT >= 0:
            deltasign = 1
        else:
            deltasign = 0

        for i in range(len(MOB_TotalMRT_CFD)):
            if np.isnan(MOB_TotalMRT_CFD[i]):
                MOB_TotalMRT_CFD[i] = 0
            else:
                pass
        for i in range(len(MOB_TotalMRT_CFD)):
            if np.isnan(MOB_TotalMRT_CFD[i]):
                MOB_TotalMRT_CFD[i] = 0
            else:
                pass

        return render(request, 'mobcfd.html', {
            "lastupdatedon": MOBCFDLastUpdate,
            "MOB_CFDtotalJiras": MOB_CFDtotalJiras,
            "MOB_TotalFixed_CFD": MOB_TotalFixed_CFD,
            "MOB_TotalBackLog_CFD": MOB_TotalBackLog_CFD,
            "MOB_TotalNoise_CFD": MOB_TotalNoise_CFD,
            "MOB_TotalMRT_CFD": MOB_TotalMRT_CFD,
            "MOB_CFDtotalPriorityHigh": MOB_CFDtotalPriorityHigh,
            "MOB_CFDtotalPriorityMedium": MOB_CFDtotalPriorityMedium,
            "MOB_CFDtotalPriorityLow": MOB_CFDtotalPriorityLow,
            "MOB_CFDtotalPriorityUrgent": MOB_CFDtotalPriorityUrgent,
            "deltaMRT": deltaMRT,
            "deltasign": deltasign,

})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('qualityboard:index')
        else:
            return render(request, 'login.html', {
                "message": "Incorrect Credentials !!!"
            })

    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html', {
        "message": "Logged Out !!!"
    })

def convert_date_month(i):
    pattern = '([0-9]+)-([0-9]+)-([0-9]+)'
    result = re.match(pattern, str(i))
    if result:
        return(result.group(2).lstrip('0'))
    else:
        pass


def jira_data(username, token, flag, url, project, duration):
    jira_filter = {}
    status = {}
    components = {}
    totals = {}
    numofissues = []
    dateofmonth = []
    # startat = [0,101,201,301,401,501,601]
    startat = [0, 101, 201, 301, 401, 501, 601, 701, 801, 901, 1001]
    error_flag = 0

    monthcount = int(duration)
    now = time.localtime()
    month_year_list = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in
                       range(monthcount)]

    for i in month_year_list:
        print("Executing for:", project, i[0], i[1])
        num_days = calendar.monthrange(i[0], i[1])[1]
        days = [datetime.date(i[0], i[1], day) for day in range(1, num_days + 1)]
        next_date = days[-1] + timedelta(days=1)
        #print("The 1st day of the next month", next_date)
        startdate = days[0]
        enddate = days[-1]

        #print("Start End and Next Date:", startdate, enddate, next_date)

        # First 100 Jiras
        #print("Getting Jira data starting from {}. Time - {}".format(startat[0], datetime.datetime.now()))
        if flag == 'internal':
            #api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(startdate) + " and created <= " + str(enddate) + " and project = DP and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and reporter in (5c82e34fe6e3160b9b6fe340, 5f4c1666fdc3f5003f1f5ed5, 5df828459a14250cb69ebf5c, 623aaefca2f6400069eac666, 61d700337c6f9800706434f3, currentUser(), 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5d1c6ad2cdf26a0d349c8e4b, 61437a3534599600714b6f9a, 62da40205eeecd39350a588a, 6050684490f2880070e03fd0, 5d85053f1fcbda0da1348072, 62591db7c23e5b006ab4e4ee, 5ca7c177e623ae19ec5509f3, 6020ffa6e6124800694a5ea1, 6204c621506317006b08a010, 5ff423bab66825010ea3ecb3, 5c57d0a5b287111683605746, 5ce2a47e48f7b90dbfd62f42, 6020ffa77db80e006a04234c, 5c82e2bb29592211228c8ad6, 5d0a687201a78b0c4e014b76, 6116df671e9ac7006816f5bc, 5df82840336e9e0cad16a003, 624e9b98f3824d006a5cfd47, 5ca6a83d3270b449b4fed5b2, 5f97df2299b42e00698ce0e8, 5ca66ffa1b65666cbad29e71, 62a83068cb3cb7006990ad9c, 5b33fa796b94db70b4d76a90, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469) order by created desc&maxResults=100"
            api_url = url+"jql=created >= " + str(startdate) + " and created <= " + str(enddate) + " and project = "+ project +" and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and reporter in (5c82e34fe6e3160b9b6fe340, 5f4c1666fdc3f5003f1f5ed5, 5df828459a14250cb69ebf5c, 623aaefca2f6400069eac666, 61d700337c6f9800706434f3, currentUser(), 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5d1c6ad2cdf26a0d349c8e4b, 61437a3534599600714b6f9a, 62da40205eeecd39350a588a, 6050684490f2880070e03fd0, 5d85053f1fcbda0da1348072, 62591db7c23e5b006ab4e4ee, 5ca7c177e623ae19ec5509f3, 6020ffa6e6124800694a5ea1, 6204c621506317006b08a010, 5ff423bab66825010ea3ecb3, 5c57d0a5b287111683605746, 5ce2a47e48f7b90dbfd62f42, 6020ffa77db80e006a04234c, 5c82e2bb29592211228c8ad6, 5d0a687201a78b0c4e014b76, 6116df671e9ac7006816f5bc, 5df82840336e9e0cad16a003, 624e9b98f3824d006a5cfd47, 5ca6a83d3270b449b4fed5b2, 5f97df2299b42e00698ce0e8, 5ca66ffa1b65666cbad29e71, 62a83068cb3cb7006990ad9c, 5b33fa796b94db70b4d76a90, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469) order by created desc&maxResults=100"
            #print("JIRA URL:",api_url)

        if flag == 'external':
            #api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(startdate) + " and created <= " + str(enddate) + " and project = DP and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and labels in (jira_escalated, pse, EAPRequest) order by created desc&maxResults=100"
            api_url = url+"jql=created >= " + str(startdate) + " and created <= " + str(enddate) + " and project = "+ project +" and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and labels in (jira_escalated, pse, EAPRequest) order by created desc&maxResults=100"
            #print("JIRA URL:", api_url)
        #if flag == 'features':
        #    api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(startdate) + " and created <= " + str(enddate) + " and project = DP and issuetype in (Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) order by created desc&maxResults=100"

        r = requests.get(api_url, auth=HTTPBasicAuth(username, token))

        try:
            json_content = r.json()
        except ValueError:
            print("Error:", ValueError)
            error_flag = 1

        if json_content['total'] != 0:
            for i in json_content['issues']:

                jira_id_data = []
                jira_id = i['key']
                if project == 'DP':
                    jira_component = i['fields']['customfield_12136']['value']
                jira_createddate = i['fields']['created'].split('T')[0]
                jira_status = i['fields']['status']['name']
                jira_priority = i['fields']['priority']['name']

                if (i['fields']['resolution']) is not None:
                    jira_resolution = i['fields']['resolution']['name']
                    pattern = '(.*),"lastUpdated":"([0-9-]+)(.*)'
                    result = re.match(pattern, i['fields']['customfield_10900'])
                    if result:
                        jira_resolution_date = result.group(2)
                    else:
                        if len(i['fields']['fixVersions']) != 0:
                            try:
                                jira_resolution_date = i['fields']['fixVersions'][0]['releaseDate']
                            except:
                                if i['fields']['statuscategorychangedate'] is not None:
                                    jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]
                                else:
                                    jira_resolution_date = str(date.today()).split(" ")[0]
                        else:
                            if i['fields']['statuscategorychangedate'] is not None:
                                jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]
                            else:
                                jira_resolution_date = str(date.today()).split(" ")[0]

                else:
                    # jira_resolution = ""
                    # jira_resolution_date = str(date.today()).split(" ")[0]
                    if jira_status == "Ready for Production":
                        jira_resolution = jira_status
                    else:
                        jira_resolution = ""
                    jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]

                try:
                    date_created_obj = datetime.datetime.strptime(jira_createddate, '%Y-%m-%d')
                    date_resolution_obj = datetime.datetime.strptime(jira_resolution_date, '%Y-%m-%d')
                    delta = date_resolution_obj - date_created_obj
                except Exception as e:
                    delta = ""
                    pass

                jira_id_data.append(jira_id)
                if project == 'DP':
                    jira_id_data.append(jira_component)
                jira_id_data.append(jira_createddate)
                jira_id_data.append(jira_priority)
                jira_id_data.append(jira_status)
                jira_id_data.append(jira_resolution)
                jira_id_data.append(jira_resolution_date)
                if type(delta) == str:
                    jira_id_data.append(delta)
                else:
                    jira_id_data.append(delta.days)

                if not jira_createddate in totals:
                    totals[jira_createddate] = 1
                else:
                    totals[jira_createddate] += 1

                jira_filter[jira_id] = jira_id_data

        total_jiras = json_content['total']
        iterations = int(total_jiras / 100)
        if total_jiras % 100:
            iterations = iterations + 1

        count = 1

        # Remaining 100s Jiras
        while count <= iterations - 1:
            #print("Getting Jira data starting from {}. Time - {}".format(startat[count], datetime.datetime.now()))
            if flag == 'internal':
                #api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = DP and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and reporter in (5c82e34fe6e3160b9b6fe340, 5f4c1666fdc3f5003f1f5ed5, 5df828459a14250cb69ebf5c, 623aaefca2f6400069eac666, 61d700337c6f9800706434f3, currentUser(), 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5d1c6ad2cdf26a0d349c8e4b, 61437a3534599600714b6f9a, 62da40205eeecd39350a588a, 6050684490f2880070e03fd0, 5d85053f1fcbda0da1348072, 62591db7c23e5b006ab4e4ee, 5ca7c177e623ae19ec5509f3, 6020ffa6e6124800694a5ea1, 6204c621506317006b08a010, 5ff423bab66825010ea3ecb3, 5c57d0a5b287111683605746, 5ce2a47e48f7b90dbfd62f42, 6020ffa77db80e006a04234c, 5c82e2bb29592211228c8ad6, 5d0a687201a78b0c4e014b76, 6116df671e9ac7006816f5bc, 5df82840336e9e0cad16a003, 624e9b98f3824d006a5cfd47, 5ca6a83d3270b449b4fed5b2, 5f97df2299b42e00698ce0e8, 5ca66ffa1b65666cbad29e71, 62a83068cb3cb7006990ad9c, 5b33fa796b94db70b4d76a90, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469) order by created desc&startAt=" + str(startat[count]) + "&maxResults=100"
                api_url = url+"jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = "+ project +" and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and reporter in (5c82e34fe6e3160b9b6fe340, 5f4c1666fdc3f5003f1f5ed5, 5df828459a14250cb69ebf5c, 623aaefca2f6400069eac666, 61d700337c6f9800706434f3, currentUser(), 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5d1c6ad2cdf26a0d349c8e4b, 61437a3534599600714b6f9a, 62da40205eeecd39350a588a, 6050684490f2880070e03fd0, 5d85053f1fcbda0da1348072, 62591db7c23e5b006ab4e4ee, 5ca7c177e623ae19ec5509f3, 6020ffa6e6124800694a5ea1, 6204c621506317006b08a010, 5ff423bab66825010ea3ecb3, 5c57d0a5b287111683605746, 5ce2a47e48f7b90dbfd62f42, 6020ffa77db80e006a04234c, 5c82e2bb29592211228c8ad6, 5d0a687201a78b0c4e014b76, 6116df671e9ac7006816f5bc, 5df82840336e9e0cad16a003, 624e9b98f3824d006a5cfd47, 5ca6a83d3270b449b4fed5b2, 5f97df2299b42e00698ce0e8, 5ca66ffa1b65666cbad29e71, 62a83068cb3cb7006990ad9c, 5b33fa796b94db70b4d76a90, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469) order by created desc&startAt=" + str(startat[count]) + "&maxResults=100"


            if flag == 'external':
                #api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = DP and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and labels in (jira_escalated, pse, EAPRequest) order by created desc&startAt=" + str(startat[count]) + "&maxResults=100"
                api_url = url+"jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = "+ project +" and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and labels in (jira_escalated, pse, EAPRequest) order by created desc&startAt=" + str(startat[count]) + "&maxResults=100"

            #if flag == 'features':
            #    api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(
            #        startdate) + " and created <= " + str(
            #        next_date) + " and project = DP and issuetype in (Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) order by created desc&startAt=" + str(
            #        startat[count]) + "&maxResults=100"

            r = requests.get(api_url, auth=HTTPBasicAuth(username, token))
            #soup = BeautifulSoup(r.content, 'html5lib')
            #content = soup.get_text()

            try:
                json_content = r.json()
            except ValueError:
                print("Error:", ValueError)
                error_flag = 1

            if json_content['total'] != 0:
                for i in json_content['issues']:
                    jira_id_data = []
                    jira_id = i['key']
                    if project == 'DP':
                        jira_component = i['fields']['customfield_12136']['value']
                    jira_createddate = i['fields']['created'].split('T')[0]
                    jira_status = i['fields']['status']['name']
                    jira_priority = i['fields']['priority']['name']

                    if (i['fields']['resolution']) is not None:
                        jira_resolution = i['fields']['resolution']['name']
                        pattern = '(.*),"lastUpdated":"([0-9-]+)(.*)'
                        result = re.match(pattern, i['fields']['customfield_10900'])
                        if result:
                            jira_resolution_date = result.group(2)
                        else:
                            if len(i['fields']['fixVersions']) != 0:
                                try:
                                    jira_resolution_date = i['fields']['fixVersions'][0]['releaseDate']
                                except:
                                    if i['fields']['statuscategorychangedate'] is not None:
                                        jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]
                                    else:
                                        jira_resolution_date = str(date.today()).split(" ")[0]
                            else:
                                if i['fields']['resolutiondate'] is not None:
                                    jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]
                                else:
                                    jira_resolution_date = str(date.today()).split(" ")[0]

                    else:
                        # jira_resolution = ""
                        # jira_resolution_date = str(date.today()).split(" ")[0]
                        if jira_status == "Ready for Production":
                            jira_resolution = jira_status
                        else:
                            jira_resolution = ""
                        jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]

                    try:
                        date_created_obj = datetime.datetime.strptime(jira_createddate, '%Y-%m-%d')
                        date_resolution_obj = datetime.datetime.strptime(jira_resolution_date, '%Y-%m-%d')
                        delta = date_resolution_obj - date_created_obj
                    except:
                        delta = ""
                        pass

                    jira_id_data.append(jira_id)
                    if project == 'DP':
                        jira_id_data.append(jira_component)
                    jira_id_data.append(jira_createddate)
                    jira_id_data.append(jira_priority)
                    jira_id_data.append(jira_status)
                    jira_id_data.append(jira_resolution)
                    jira_id_data.append(jira_resolution_date)
                    if type(delta) == str:
                        jira_id_data.append(delta)
                    else:
                        jira_id_data.append(delta.days)

                    if not jira_createddate in totals:
                        totals[jira_createddate] = 1
                    else:
                        totals[jira_createddate] += 1

                    jira_filter[jira_id] = jira_id_data

            count += 1

        # Month Last Day Jiras
        #print("Getting Jira data for the last day of the month. Time - {}".format(datetime.datetime.now()))
        if flag == 'internal':
            #api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = DP and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and reporter in (5c82e34fe6e3160b9b6fe340, 5f4c1666fdc3f5003f1f5ed5, 5df828459a14250cb69ebf5c, 623aaefca2f6400069eac666, 61d700337c6f9800706434f3, currentUser(), 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5d1c6ad2cdf26a0d349c8e4b, 61437a3534599600714b6f9a, 62da40205eeecd39350a588a, 6050684490f2880070e03fd0, 5d85053f1fcbda0da1348072, 62591db7c23e5b006ab4e4ee, 5ca7c177e623ae19ec5509f3, 6020ffa6e6124800694a5ea1, 6204c621506317006b08a010, 5ff423bab66825010ea3ecb3, 5c57d0a5b287111683605746, 5ce2a47e48f7b90dbfd62f42, 6020ffa77db80e006a04234c, 5c82e2bb29592211228c8ad6, 5d0a687201a78b0c4e014b76, 6116df671e9ac7006816f5bc, 5df82840336e9e0cad16a003, 624e9b98f3824d006a5cfd47, 5ca6a83d3270b449b4fed5b2, 5f97df2299b42e00698ce0e8, 5ca66ffa1b65666cbad29e71, 62a83068cb3cb7006990ad9c, 5b33fa796b94db70b4d76a90, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469) order by created desc&maxResults=100"
            api_url = url+"jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = DP and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and reporter in (5c82e34fe6e3160b9b6fe340, 5f4c1666fdc3f5003f1f5ed5, 5df828459a14250cb69ebf5c, 623aaefca2f6400069eac666, 61d700337c6f9800706434f3, currentUser(), 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5d1c6ad2cdf26a0d349c8e4b, 61437a3534599600714b6f9a, 62da40205eeecd39350a588a, 6050684490f2880070e03fd0, 5d85053f1fcbda0da1348072, 62591db7c23e5b006ab4e4ee, 5ca7c177e623ae19ec5509f3, 6020ffa6e6124800694a5ea1, 6204c621506317006b08a010, 5ff423bab66825010ea3ecb3, 5c57d0a5b287111683605746, 5ce2a47e48f7b90dbfd62f42, 6020ffa77db80e006a04234c, 5c82e2bb29592211228c8ad6, 5d0a687201a78b0c4e014b76, 6116df671e9ac7006816f5bc, 5df82840336e9e0cad16a003, 624e9b98f3824d006a5cfd47, 5ca6a83d3270b449b4fed5b2, 5f97df2299b42e00698ce0e8, 5ca66ffa1b65666cbad29e71, 62a83068cb3cb7006990ad9c, 5b33fa796b94db70b4d76a90, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469) order by created desc&maxResults=100"


        if flag == 'external':
            #api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = DP and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and labels in (jira_escalated, pse, EAPRequest) order by created desc&maxResults=100"
            api_url = url+"jql=created >= " + str(startdate) + " and created <= " + str(next_date) + " and project = "+ project +" and issuetype in (Bug, Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) and labels in (jira_escalated, pse, EAPRequest) order by created desc&maxResults=100"

        #if flag == 'features':
        #    api_url = "https://dialpad.atlassian.net/rest/api/2/search?jql=created >= " + str(
        #        startdate) + " and created <= " + str(
        #        next_date) + " and project = DP and issuetype in (Documentation, Epic, Improvement, 'New Feature', Story, Task, Sub-task) order by created desc&maxResults=100"

        r = requests.get(api_url, auth=HTTPBasicAuth(username, token))
        #soup = BeautifulSoup(r.content, 'html5lib')
        #content = soup.get_text()

        try:
            json_content = r.json()
        except ValueError:
            print("Error:", ValueError)
            error_flag = 1

        if json_content['total'] != 0:
            for i in json_content['issues']:
                jira_id_data = []
                jira_id = i['key']
                if project == 'DP':
                    jira_component = i['fields']['customfield_12136']['value']
                jira_createddate = i['fields']['created'].split('T')[0]
                jira_status = i['fields']['status']['name']
                jira_priority = i['fields']['priority']['name']

                if (i['fields']['resolution']) is not None:
                    jira_resolution = i['fields']['resolution']['name']
                    pattern = '(.*),"lastUpdated":"([0-9-]+)(.*)'
                    result = re.match(pattern, i['fields']['customfield_10900'])
                    if result:
                        jira_resolution_date = result.group(2)
                    else:
                        if len(i['fields']['fixVersions']) != 0:
                            try:
                                jira_resolution_date = i['fields']['fixVersions'][0]['releaseDate']
                            except:
                                if i['fields']['statuscategorychangedate'] is not None:
                                    jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]
                                else:
                                    jira_resolution_date = str(date.today()).split(" ")[0]
                        else:
                            if i['fields']['statuscategorychangedate'] is not None:
                                jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]
                            else:
                                jira_resolution_date = str(date.today()).split(" ")[0]

                else:
                    # jira_resolution = ""
                    # jira_resolution_date = str(date.today()).split(" ")[0]
                    if jira_status == "Ready for Production":
                        jira_resolution = jira_status
                    else:
                        jira_resolution = ""
                    jira_resolution_date = i['fields']['statuscategorychangedate'].split('T')[0]

                try:
                    date_created_obj = datetime.datetime.strptime(jira_createddate, '%Y-%m-%d')
                    date_resolution_obj = datetime.datetime.strptime(jira_resolution_date, '%Y-%m-%d')
                    delta = date_resolution_obj - date_created_obj
                except:
                    delta = ""
                    pass

                jira_id_data.append(jira_id)
                if project == 'DP':
                    jira_id_data.append(jira_component)
                jira_id_data.append(jira_createddate)
                jira_id_data.append(jira_priority)
                jira_id_data.append(jira_status)
                jira_id_data.append(jira_resolution)
                jira_id_data.append(jira_resolution_date)
                if type(delta) == str:
                    jira_id_data.append(delta)
                else:
                    jira_id_data.append(delta.days)

                if not jira_createddate in totals:
                    totals[jira_createddate] = 1
                else:
                    totals[jira_createddate] += 1

                jira_filter[jira_id] = jira_id_data

    return jira_filter


def process_jira_data(jira_filter_data, duration):
    totalJiras = []
    totalFixed = []
    totalMRT = []
    totalNotClosed = []
    totalBLMRT = []
    totalCurrentFix = []
    totalNoise = []
    totalPriorityH = []
    totalPriorityL = []
    totalPriorityM = []
    totalPriorityU = []
    talkJiras = []
    talkFixed = []
    talkMRT = []
    talkBLMRT = []
    talkNotClosed = []
    talkCurrentFix = []
    talkNoise = []
    talkPriorityH = []
    talkPriorityL = []
    talkPriorityM = []
    talkPriorityU = []
    CCJiras = []
    CCFixed = []
    CCMRT = []
    CCNotClosed = []
    CCBLMRT = []
    CCCurrentFix = []
    CCNoise = []
    CCPriorityH = []
    CCPriorityL = []
    CCPriorityM = []
    CCPriorityU = []
    INTJiras = []
    INTFixed = []
    INTMRT = []
    INTNotClosed = []
    INTBLMRT = []
    INTCurrentFix = []
    INTNoise = []
    INTPriorityH = []
    INTPriorityL = []
    INTPriorityM = []
    INTPriorityU = []

    data_df = pd.DataFrame.from_dict(jira_filter_data, orient='index')
    data_df.columns = ['JiraID', 'Component', 'CreateDate','Priority', 'Status', 'Resolution', 'ResolutionDate', 'Delta']
    data_df = data_df.reset_index()

    data_df['createdMonth'] = data_df['CreateDate'].map(convert_date_month)
    data_df['resolutionMonth'] = data_df['ResolutionDate'].map(convert_date_month)
    groupby_month = data_df.groupby('createdMonth')
    # print(data_df)

    monthcount = int(duration)
    now = time.localtime()
    month_year_list = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(monthcount)]

    for i in month_year_list:
        #print("Processing for:", i[1])
        data = groupby_month.get_group(str(i[1]))

        totalJiras_v = data.count()[0]
        totalFixed_v = data[(data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production")].count()[0]
        totalMRT_v = data[(data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production")]["Delta"].mean()
        totalNotClosed_v = (data['Resolution'] == "").sum()
        totalBLMRT_v = data[(data['Resolution'] == "")]["Delta"].mean()
        totalCurrentfix_v = data[((data['createdMonth'] == str(i[1])) & (data['resolutionMonth'] == str(i[1]))) & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        totalNoise_v = totalJiras_v - totalFixed_v - totalNotClosed_v
        totalPriorityH_v = (data['Priority'] == "High").sum()
        totalPriorityL_v = (data['Priority'] == "Low").sum()
        totalPriorityM_v = (data['Priority'] == "Medium").sum()
        totalPriorityU_v = (data['Priority'] == "Urgent").sum()
        totalJiras.append(totalJiras_v)
        totalFixed.append(totalFixed_v)
        totalMRT.append(totalMRT_v)
        totalNotClosed.append(totalNotClosed_v)
        totalBLMRT.append(totalBLMRT_v)
        totalCurrentFix.append(totalCurrentfix_v)
        totalNoise.append(totalNoise_v)
        totalPriorityH.append(totalPriorityH_v)
        totalPriorityL.append(totalPriorityL_v)
        totalPriorityM.append(totalPriorityM_v)
        totalPriorityU.append(totalPriorityU_v)

        #talkJiras_v = data[(data.Component == "Dialpad Talk")].count()[0]
        talkJiras_v = data[(data.Component == "Core UX")].count()[0]
        talkFixed_v = data[(data.Component == "Core UX") & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        talkMRT_v = data[(data.Component == "Core UX") & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))]["Delta"].mean()
        talkNotClosed_v = data[(data.Component == "Core UX") & (data['Resolution'] == "")].count()[0]
        talkBLMRT_v = data[(data.Component == "Core UX") & (data['Resolution'] == "")]["Delta"].mean()
        talkCurrentfix_v = data[(data.Component == "Core UX") & ((data['createdMonth'] == str(i[1])) & (data['resolutionMonth'] == str(i[1]))) & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        talkNoise_v = talkJiras_v - talkFixed_v - talkNotClosed_v
        talkPriorityH_v = data[(data.Component == "Core UX") & (data['Priority'] == "High")].count()[0]
        talkPriorityM_v = data[(data.Component == "Core UX") & (data['Priority'] == "Medium")].count()[0]
        talkPriorityL_v = data[(data.Component == "Core UX") & (data['Priority'] == "Low")].count()[0]
        talkPriorityU_v = data[(data.Component == "Core UX") & (data['Priority'] == "Urgent")].count()[0]
        talkJiras.append(talkJiras_v)
        talkFixed.append(talkFixed_v)
        talkMRT.append(talkMRT_v)
        talkNotClosed.append(talkNotClosed_v)
        talkBLMRT.append(talkBLMRT_v)
        talkCurrentFix.append(talkCurrentfix_v)
        talkNoise.append(talkNoise_v)
        talkPriorityH.append(talkPriorityH_v)
        talkPriorityL.append(talkPriorityL_v)
        talkPriorityM.append(talkPriorityM_v)
        talkPriorityU.append(talkPriorityU_v)

        CCJiras_v = data[(data.Component == "Contact Center")].count()[0]
        CCFixed_v = data[(data.Component == "Contact Center") & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        CCMRT_v = data[(data.Component == "Contact Center") & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))]["Delta"].mean()
        CCNotClosed_v = data[(data.Component == "Contact Center") & (data['Resolution'] == "")].count()[0]
        CCBLMRT_v = data[(data.Component == "Contact Center") & (data['Resolution'] == "")]["Delta"].mean()
        CCCurrentfix_v = data[(data.Component == "Contact Center") & ((data['createdMonth'] == str(i[1])) & (data['resolutionMonth'] == str(i[1]))) & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        CCNoise_v = CCJiras_v - CCFixed_v - CCNotClosed_v
        CCPriorityH_v = data[(data.Component == "Contact Center") & (data['Priority'] == "High")].count()[0]
        CCPriorityM_v = data[(data.Component == "Contact Center") & (data['Priority'] == "Medium")].count()[0]
        CCPriorityL_v = data[(data.Component == "Contact Center") & (data['Priority'] == "Low")].count()[0]
        CCPriorityU_v = data[(data.Component == "Contact Center") & (data['Priority'] == "Urgent")].count()[0]
        CCJiras.append(CCJiras_v)
        CCFixed.append(CCFixed_v)
        CCMRT.append(CCMRT_v)
        CCNotClosed.append(CCNotClosed_v)
        CCBLMRT.append(CCBLMRT_v)
        CCCurrentFix.append(CCCurrentfix_v)
        CCNoise.append(CCNoise_v)
        CCPriorityH.append(CCPriorityH_v)
        CCPriorityL.append(CCPriorityL_v)
        CCPriorityM.append(CCPriorityM_v)
        CCPriorityU.append(CCPriorityU_v)

        INTJiras_v = data[(data.Component == "Integrations")].count()[0]
        INTFixed_v = data[(data.Component == "Integrations") & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        INTMRT_v = data[(data.Component == "Integrations") & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))]["Delta"].mean()
        INTNotClosed_v = data[(data.Component == "Integrations") & (data['Resolution'] == "")].count()[0]
        INTBLMRT_v = data[(data.Component == "Integrations") & (data['Resolution'] == "")]["Delta"].mean()
        INTCurrentfix_v = data[(data.Component == "Integrations") & ((data['createdMonth'] == str(i[1])) & (data['resolutionMonth'] == str(i[1]))) & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        INTNoise_v = INTJiras_v - INTFixed_v - INTNotClosed_v
        INTPriorityH_v = data[(data.Component == "Integrations") & (data['Priority'] == "High")].count()[0]
        INTPriorityM_v = data[(data.Component == "Integrations") & (data['Priority'] == "Medium")].count()[0]
        INTPriorityL_v = data[(data.Component == "Integrations") & (data['Priority'] == "Low")].count()[0]
        INTPriorityU_v = data[(data.Component == "Integrations") & (data['Priority'] == "Urgent")].count()[0]
        INTJiras.append(INTJiras_v)
        INTFixed.append(INTFixed_v)
        INTMRT.append(INTMRT_v)
        INTNotClosed.append(INTNotClosed_v)
        INTBLMRT.append(INTBLMRT_v)
        INTCurrentFix.append(INTCurrentfix_v)
        INTNoise.append(INTNoise_v)
        INTPriorityH.append(INTPriorityH_v)
        INTPriorityL.append(INTPriorityL_v)
        INTPriorityM.append(INTPriorityM_v)
        INTPriorityU.append(INTPriorityU_v)

    # return totalJiras,totalFixed,np.round(totalMRT,2),totalNotClosed,np.round(totalBLMRT,2),totalCurrentFix,totalNoise,talkJiras,talkFixed,np.round(talkMRT,2),talkNotClosed,np.round(talkBLMRT,2),talkCurrentFix,talkNoise,CCJiras,CCFixed,np.round(CCMRT,2),CCNotClosed,np.round(CCBLMRT,2),CCCurrentFix,CCNoise,INTJiras,INTFixed,np.round(INTMRT,2),INTNotClosed,np.round(INTBLMRT,2),INTCurrentFix,INTNoise
    return totalJiras[::-1], totalFixed[::-1], np.round(totalMRT[::-1], 2), totalNotClosed[::-1], totalCurrentFix[::-1], totalNoise[::-1], totalPriorityH[::-1],totalPriorityM[::-1],totalPriorityL[::-1],totalPriorityU[::-1],talkJiras[::-1], talkFixed[::-1], \
           np.round(talkMRT[::-1], 2), talkNotClosed[::-1], talkCurrentFix[::-1], talkNoise[::-1], talkPriorityH[::-1],talkPriorityM[::-1],talkPriorityL[::-1],talkPriorityU[::-1],CCJiras[::-1], CCFixed[::-1], np.round(CCMRT[::-1], 2), CCNotClosed[::-1], \
           CCCurrentFix[::-1], CCNoise[::-1], CCPriorityH[::-1],CCPriorityM[::-1],CCPriorityL[::-1],CCPriorityU[::-1],INTJiras[::-1], INTFixed[::-1], np.round(INTMRT[::-1], 2), INTNotClosed[::-1], INTCurrentFix[::-1], INTNoise[::-1],INTPriorityH[::-1],INTPriorityM[::-1],INTPriorityL[::-1],INTPriorityU[::-1]


def process_dpm_data(jira_filter_data, duration):
    totalJiras = []
    totalFixed = []
    totalMRT = []
    totalNotClosed = []
    totalBLMRT = []
    totalCurrentFix = []
    totalNoise = []
    totalPriorityH = []
    totalPriorityL = []
    totalPriorityM = []
    totalPriorityU = []

    data_df = pd.DataFrame.from_dict(jira_filter_data, orient='index')
    data_df.columns = ['JiraID', 'CreateDate','Priority', 'Status', 'Resolution', 'ResolutionDate', 'Delta']
    data_df = data_df.reset_index()

    data_df['createdMonth'] = data_df['CreateDate'].map(convert_date_month)
    data_df['resolutionMonth'] = data_df['ResolutionDate'].map(convert_date_month)
    groupby_month = data_df.groupby('createdMonth')
    # print(data_df)

    monthcount = int(duration)
    now = time.localtime()
    month_year_list = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(monthcount)]

    for i in month_year_list:
        #print("Processing for:", i[1])
        data = groupby_month.get_group(str(i[1]))

        totalJiras_v = data.count()[0]
        totalFixed_v = data[(data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production")].count()[0]
        totalMRT_v = data[(data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production")]["Delta"].mean()
        totalNotClosed_v = (data['Resolution'] == "").sum()
        totalBLMRT_v = data[(data['Resolution'] == "")]["Delta"].mean()
        totalCurrentfix_v = data[((data['createdMonth'] == str(i[1])) & (data['resolutionMonth'] == str(i[1]))) & ((data.Resolution == "Fixed") | (data.Resolution == "Done") | (data.Resolution == "Ready for Production"))].count()[0]
        totalNoise_v = totalJiras_v - totalFixed_v - totalNotClosed_v
        totalPriorityH_v = (data['Priority'] == "High").sum()
        totalPriorityL_v = (data['Priority'] == "Low").sum()
        totalPriorityM_v = (data['Priority'] == "Medium").sum()
        totalPriorityU_v = (data['Priority'] == "Urgent").sum()
        totalJiras.append(totalJiras_v)
        totalFixed.append(totalFixed_v)
        totalMRT.append(totalMRT_v)
        totalNotClosed.append(totalNotClosed_v)
        totalBLMRT.append(totalBLMRT_v)
        totalCurrentFix.append(totalCurrentfix_v)
        totalNoise.append(totalNoise_v)
        totalPriorityH.append(totalPriorityH_v)
        totalPriorityL.append(totalPriorityL_v)
        totalPriorityM.append(totalPriorityM_v)
        totalPriorityU.append(totalPriorityU_v)

    # return totalJiras,totalFixed,np.round(totalMRT,2),totalNotClosed,np.round(totalBLMRT,2),totalCurrentFix,totalNoise,talkJiras,talkFixed,np.round(talkMRT,2),talkNotClosed,np.round(talkBLMRT,2),talkCurrentFix,talkNoise,CCJiras,CCFixed,np.round(CCMRT,2),CCNotClosed,np.round(CCBLMRT,2),CCCurrentFix,CCNoise,INTJiras,INTFixed,np.round(INTMRT,2),INTNotClosed,np.round(INTBLMRT,2),INTCurrentFix,INTNoise
    return totalJiras[::-1], totalFixed[::-1], np.round(totalMRT[::-1], 2), totalNotClosed[::-1], totalCurrentFix[::-1], totalNoise[::-1], totalPriorityH[::-1],totalPriorityM[::-1],totalPriorityL[::-1],totalPriorityU[::-1]



def get_product_health_metrics():
    username = env('DJANGO_JIRA_USER')
    token = env('DJANGO_JIRA_TOKEN')
    url = "https://dialpad.atlassian.net/rest/api/2/search?"

    duration = int(12)

    CFDjira_filter_data = jira_data(username, token, 'external', url, 'DP' ,duration)
    CFDtotalJiras, CFDtotalFixed, CFDtotalMRT, CFDtotalNotClosed, CFDtotalCurrentFix, CFDtotalNoise, CFDtotalPriorityH,CFDtotalPriorityM,CFDtotalPriorityL,CFDtotalPriorityU, CFDtalkJiras, CFDtalkFixed, CFDtalkMRT, CFDtalkNotClosed, CFDtalkCurrentFix, CFDtalkNoise, CFDtalkPriorityH,CFDtalkPriorityM,CFDtalkPriorityL,CFDtalkPriorityU, CFDCCJiras, CFDCCFixed, CFDCCMRT, CFDCCNotClosed, CFDCCCurrentFix, CFDCCNoise, CFDCCPriorityH,CFDCCPriorityM,CFDCCPriorityL,CFDCCPriorityU, CFDINTJiras, CFDINTFixed, CFDINTMRT, CFDINTNotClosed, CFDINTCurrentFix, CFDINTNoise,CFDINTPriorityH,CFDINTPriorityM,CFDINTPriorityL,CFDINTPriorityU = process_jira_data(CFDjira_filter_data, duration)

    ##IFDjira_filter_data = jira_data(username, token, 'internal', url, 'DP' ,duration)
    ##IFDtotalJiras, IFDtotalFixed, IFDtotalMRT, IFDtotalNotClosed, IFDtotalCurrentFix, IFDtotalNoise, IFDtalkJiras, IFDtalkFixed, IFDtalkMRT, IFDtalkNotClosed, IFDtalkCurrentFix, IFDtalkNoise, IFDCCJiras, IFDCCFixed, IFDCCMRT, IFDCCNotClosed, IFDCCCurrentFix, IFDCCNoise, IFDINTJiras, IFDINTFixed, IFDINTMRT, IFDINTNotClosed, IFDINTCurrentFix, IFDINTNoise = process_jira_data(IFDjira_filter_data, duration)

    ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    #print("Log Jira data to database at {}".format(ind_time))

    CFDtotalJiras = str(CFDtotalJiras)[1:-1]
    CFDtotalFixed = str(CFDtotalFixed)[1:-1]
    CFDtotalMRT = str(CFDtotalMRT)[1:-1]
    CFDtotalNotClosed = str(CFDtotalNotClosed)[1:-1]
    CFDtotalCurrentFix = str(CFDtotalCurrentFix)[1:-1]
    CFDtotalNoise = str(CFDtotalNoise)[1:-1]
    CFDtotalPriorityH = str(CFDtotalPriorityH)[1:-1]
    CFDtotalPriorityM = str(CFDtotalPriorityM)[1:-1]
    CFDtotalPriorityL = str(CFDtotalPriorityL)[1:-1]
    CFDtotalPriorityU = str(CFDtotalPriorityU)[1:-1]
    CFDtalkJiras = str(CFDtalkJiras)[1:-1]
    CFDtalkFixed = str(CFDtalkFixed)[1:-1]
    CFDtalkMRT = str(CFDtalkMRT)[1:-1]
    CFDtalkNotClosed = str(CFDtalkNotClosed)[1:-1]
    CFDtalkCurrentFix = str(CFDtalkCurrentFix)[1:-1]
    CFDtalkNoise = str(CFDtalkNoise)[1:-1]
    CFDtalkPriorityH = str(CFDtalkPriorityH)[1:-1]
    CFDtalkPriorityM = str(CFDtalkPriorityM)[1:-1]
    CFDtalkPriorityL = str(CFDtalkPriorityL)[1:-1]
    CFDtalkPriorityU = str(CFDtalkPriorityU)[1:-1]
    CFDCCJiras = str(CFDCCJiras)[1:-1]
    CFDCCFixed = str(CFDCCFixed)[1:-1]
    CFDCCMRT = str(CFDCCMRT)[1:-1]
    CFDCCNotClosed = str(CFDCCNotClosed)[1:-1]
    CFDCCCurrentFix = str(CFDCCCurrentFix)[1:-1]
    CFDCCNoise = str(CFDCCNoise)[1:-1]
    CFDCCPriorityH = str(CFDCCPriorityH)[1:-1]
    CFDCCPriorityM = str(CFDCCPriorityM)[1:-1]
    CFDCCPriorityL = str(CFDCCPriorityL)[1:-1]
    CFDCCPriorityU = str(CFDCCPriorityU)[1:-1]
    CFDINTJiras = str(CFDINTJiras)[1:-1]
    CFDINTFixed = str(CFDINTFixed)[1:-1]
    CFDINTMRT = str(CFDINTMRT)[1:-1]
    CFDINTNotClosed = str(CFDINTNotClosed)[1:-1]
    CFDINTCurrentFix = str(CFDINTCurrentFix)[1:-1]
    CFDINTNoise = str(CFDINTNoise)[1:-1]
    CFDINTPriorityH = str(CFDINTPriorityH)[1:-1]
    CFDINTPriorityM = str(CFDINTPriorityM)[1:-1]
    CFDINTPriorityL = str(CFDINTPriorityL)[1:-1]
    CFDINTPriorityU = str(CFDINTPriorityU)[1:-1]

    try:
        jira_cfd = CFD.objects.get(id=1)
        jira_cfd.CFDtotalJiras = CFDtotalJiras
        jira_cfd.CFDtotalFixed = CFDtotalFixed
        jira_cfd.CFDtotalMRT = CFDtotalMRT
        jira_cfd.CFDtotalNotClosed = CFDtotalNotClosed
        jira_cfd.CFDtotalCurrentFix = CFDtotalCurrentFix
        jira_cfd.CFDtotalNoise = CFDtotalNoise
        jira_cfd.CFDtotalPriorityH = CFDtotalPriorityH
        jira_cfd.CFDtotalPriorityM = CFDtotalPriorityM
        jira_cfd.CFDtotalPriorityL = CFDtotalPriorityL
        jira_cfd.CFDtotalPriorityU = CFDtotalPriorityU
        jira_cfd.CFDtalkJiras = CFDtalkJiras
        jira_cfd.CFDtalkFixed = CFDtalkFixed
        jira_cfd.CFDtalkMRT = CFDtalkMRT
        jira_cfd.CFDtalkNotClosed = CFDtalkNotClosed
        jira_cfd.CFDtalkCurrentFix = CFDtalkCurrentFix
        jira_cfd.CFDtalkNoise = CFDtalkNoise
        jira_cfd.CFDtalkPriorityH = CFDtalkPriorityH
        jira_cfd.CFDtalkPriorityM = CFDtalkPriorityM
        jira_cfd.CFDtalkPriorityL = CFDtalkPriorityL
        jira_cfd.CFDtalkPriorityU = CFDtalkPriorityU
        jira_cfd.CFDCCJiras = CFDCCJiras
        jira_cfd.CFDCCFixed = CFDCCFixed
        jira_cfd.CFDCCMRT = CFDCCMRT
        jira_cfd.CFDCCNotClosed = CFDCCNotClosed
        jira_cfd.CFDCCCurrentFix = CFDCCCurrentFix
        jira_cfd.CFDCCNoise = CFDCCNoise
        jira_cfd.CFDCCPriorityH = CFDCCPriorityH
        jira_cfd.CFDCCPriorityM = CFDCCPriorityM
        jira_cfd.CFDCCPriorityL = CFDCCPriorityL
        jira_cfd.CFDCCPriorityU = CFDCCPriorityU
        jira_cfd.CFDINTJiras = CFDINTJiras
        jira_cfd.CFDINTFixed = CFDINTFixed
        jira_cfd.CFDINTMRT = CFDINTMRT
        jira_cfd.CFDINTNotClosed = CFDINTNotClosed
        jira_cfd.CFDINTCurrentFix = CFDINTCurrentFix
        jira_cfd.CFDINTNoise = CFDINTNoise
        jira_cfd.CFDINTPriorityH = CFDINTPriorityH
        jira_cfd.CFDINTPriorityM = CFDINTPriorityM
        jira_cfd.CFDINTPriorityL = CFDINTPriorityL
        jira_cfd.CFDINTPriorityU = CFDINTPriorityU
        jira_cfd.CFDLastUpdate = ind_time

        jira_cfd.save()
        print("CFD Health Metric Saved....")
    except:
        print("CFD - Oops!", sys.exc_info()[0], "occurred.")
        pass


    DPMCFDjira_filter_data = jira_data(username, token, 'external', url, 'UC', duration)
    DPMCFDtotalJiras, DPMCFDtotalFixed, DPMCFDtotalMRT, DPMCFDtotalNotClosed, DPMCFDtotalCurrentFix, DPMCFDtotalNoise, DPMCFDtotalPriorityH, DPMCFDtotalPriorityM, DPMCFDtotalPriorityL, DPMCFDtotalPriorityU = process_dpm_data(DPMCFDjira_filter_data, duration)

    DPMCFDtotalJiras = str(DPMCFDtotalJiras)[1:-1]
    DPMCFDtotalFixed = str(DPMCFDtotalFixed)[1:-1]
    DPMCFDtotalMRT = str(DPMCFDtotalMRT)[1:-1]
    DPMCFDtotalNotClosed = str(DPMCFDtotalNotClosed)[1:-1]
    DPMCFDtotalCurrentFix = str(DPMCFDtotalCurrentFix)[1:-1]
    DPMCFDtotalNoise = str(DPMCFDtotalNoise)[1:-1]
    DPMCFDtotalPriorityH = str(DPMCFDtotalPriorityH)[1:-1]
    DPMCFDtotalPriorityM = str(DPMCFDtotalPriorityM)[1:-1]
    DPMCFDtotalPriorityL = str(DPMCFDtotalPriorityL)[1:-1]
    DPMCFDtotalPriorityU = str(DPMCFDtotalPriorityU)[1:-1]

    try:
        jira_cfddpm = CFDDPM.objects.get(id=1)
        jira_cfddpm.DPMCFDtotalJiras = DPMCFDtotalJiras
        jira_cfddpm.DPMCFDtotalFixed = DPMCFDtotalFixed
        jira_cfddpm.DPMCFDtotalMRT = DPMCFDtotalMRT
        jira_cfddpm.DPMCFDtotalNotClosed = DPMCFDtotalNotClosed
        jira_cfddpm.DPMCFDtotalCurrentFix = DPMCFDtotalCurrentFix
        jira_cfddpm.DPMCFDtotalNoise = DPMCFDtotalNoise
        jira_cfddpm.DPMCFDtotalPriorityH = DPMCFDtotalPriorityH
        jira_cfddpm.DPMCFDtotalPriorityM = DPMCFDtotalPriorityM
        jira_cfddpm.DPMCFDtotalPriorityL = DPMCFDtotalPriorityL
        jira_cfddpm.DPMCFDtotalPriorityU = DPMCFDtotalPriorityU
        jira_cfddpm.DPMCFDLastUpdate = ind_time

        jira_cfddpm.save()
        print("CFDDPM Health Metric Saved....")
    except:
        print("CFDDPM - Oops!", sys.exc_info()[0], "occurred.")
        pass


    MOBCFDjira_filter_data = jira_data(username, token, 'external', url, 'MOB', duration)
    MOBCFDtotalJiras, MOBCFDtotalFixed, MOBCFDtotalMRT, MOBCFDtotalNotClosed, MOBCFDtotalCurrentFix, MOBCFDtotalNoise, MOBCFDtotalPriorityH, MOBCFDtotalPriorityM, MOBCFDtotalPriorityL, MOBCFDtotalPriorityU = process_dpm_data(MOBCFDjira_filter_data, duration)

    MOBCFDtotalJiras = str(MOBCFDtotalJiras)[1:-1]
    MOBCFDtotalFixed = str(MOBCFDtotalFixed)[1:-1]
    MOBCFDtotalMRT = str(MOBCFDtotalMRT)[1:-1]
    MOBCFDtotalNotClosed = str(MOBCFDtotalNotClosed)[1:-1]
    MOBCFDtotalCurrentFix = str(MOBCFDtotalCurrentFix)[1:-1]
    MOBCFDtotalNoise = str(MOBCFDtotalNoise)[1:-1]
    MOBCFDtotalPriorityH = str(MOBCFDtotalPriorityH)[1:-1]
    MOBCFDtotalPriorityM = str(MOBCFDtotalPriorityM)[1:-1]
    MOBCFDtotalPriorityL = str(MOBCFDtotalPriorityL)[1:-1]
    MOBCFDtotalPriorityU = str(MOBCFDtotalPriorityU)[1:-1]


    try:
        jira_cfdmob = CFDMOB.objects.get(id=1)
        jira_cfdmob.MOBCFDtotalJiras = MOBCFDtotalJiras
        jira_cfdmob.MOBCFDtotalFixed = MOBCFDtotalFixed
        jira_cfdmob.MOBCFDtotalMRT = MOBCFDtotalMRT
        jira_cfdmob.MOBCFDtotalNotClosed = MOBCFDtotalNotClosed
        jira_cfdmob.MOBCFDtotalCurrentFix = MOBCFDtotalCurrentFix
        jira_cfdmob.MOBCFDtotalNoise = MOBCFDtotalNoise
        jira_cfdmob.MOBCFDtotalPriorityH = MOBCFDtotalPriorityH
        jira_cfdmob.MOBCFDtotalPriorityM = MOBCFDtotalPriorityM
        jira_cfdmob.MOBCFDtotalPriorityL = MOBCFDtotalPriorityL
        jira_cfdmob.MOBCFDtotalPriorityU = MOBCFDtotalPriorityU
        jira_cfdmob.MOBCFDLastUpdate = ind_time

        jira_cfdmob.save()
        print("CFDMOB Health Metric Saved....")
    except:
        print("CFDMOB - Oops!", sys.exc_info()[0], "occurred.")
        pass

    return


def get_custom_data(start_date,end_date,project,username,token,url):
    components = {}
    totals = {}
    status = {}
    numofissues = []
    dateofmonth = []
    startat = [0, 101, 201, 301, 401]
    error_flag = 0

    api_url=url+"?jql=created >= " + str(start_date) + " and created <= " + str(
        end_date) + " and project = " + project + " and issuetype in (Bug, Improvement, Task) and labels in (jira_escalated, EAPRequest) order by created desc&maxResults=100"

    r = requests.get(api_url, auth=HTTPBasicAuth(username, token))

    try:
        json_content = r.json()
    except ValueError:
        print("Error:", ValueError)
        error_flag = 1

    if json_content['total'] != 0:
        for i in json_content['issues']:
            if (project == 'DP'):
                jira_component = i['fields']['customfield_12136']['value']
            jira_createddate = i['fields']['created'].split('T')[0]
            jira_status = i['fields']['status']['name']

            if (project == 'DP'):
                if not jira_component in components:
                    components[jira_component] = 1
                else:
                    components[jira_component] += 1

            if not jira_createddate in totals:
                totals[jira_createddate] = 1
            else:
                totals[jira_createddate] += 1
            if not jira_status in status:
                status[jira_status] = 1
            else:
                status[jira_status] += 1

    total_jiras = json_content['total']
    iterations = int(total_jiras / 100)
    if total_jiras % 100:
        iterations = iterations + 1

    count = 1
    while count <= iterations - 1:
        api_url = url+"?jql=created >= " + str(start_date) + " and created <= " + str(
            end_date) + " and project = " + project + " and issuetype in (Bug, Improvement, Task) and labels in (jira_escalated, EAPRequest) order by created desc&startAt="+str(startat[count])+"&maxResults=100"

        r = requests.get(api_url, auth=HTTPBasicAuth(username, token))

        try:
            json_content = r.json()
        except ValueError:
            print("Error:", ValueError)
            error_flag = 1

        if json_content['total'] != 0:
            for i in json_content['issues']:
                if (project == 'DP'):
                    jira_component = i['fields']['customfield_12136']['value']
                jira_createddate = i['fields']['created'].split('T')[0]
                jira_status = i['fields']['status']['name']

                if (project == 'DP'):
                    if not jira_component in components:
                        components[jira_component] = 1
                    else:
                        components[jira_component] += 1

                if not jira_createddate in totals:
                    totals[jira_createddate] = 1
                else:
                    totals[jira_createddate] += 1
                if not jira_status in status:
                    status[jira_status] = 1
                else:
                    status[jira_status] += 1

        count += 1

    return components, totals, status, error_flag


def custom(request):
    month = datetime.datetime.now().strftime("%B")
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qualityboard:login'))

    else:

        if request.method == 'POST':
            if request.POST['year'] != 'Year' and request.POST['month'] != 'Month' and request.POST['project'] != 'Project':
                year = int(request.POST['year'])
                month = int(request.POST['month'])
                project = request.POST['project']
                num_days = calendar.monthrange(year, month)[1]
                days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
                start_date = str(year)+"-"+str(month)+"-"+"01"
                end_date = days[-1] + timedelta(days=1)

                url = 'https://dialpad.atlassian.net/rest/api/2/search'
                username = env('DJANGO_JIRA_USER')
                token = env('DJANGO_JIRA_TOKEN')

                components, totals, status, error_flag = get_custom_data(start_date,end_date,project,username,token,url)
                
                if not bool(totals):
                    message = "No Jira Data Available. Please check the presets !!!"
                    return render(request, 'custom.html', {
                        "messages": message,
                    })
                else:
                    reversetotals = OrderedDict(reversed(list(totals.items())))
                    reversetotalsKeys = list(reversetotals.keys())
                    reversetotalsValues = list(reversetotals.values())

                    externaltop5components = dict(sorted(components.items(), key=itemgetter(1), reverse=True)[:5])
                    externaltop5status = dict(sorted(status.items(), key=itemgetter(1), reverse=True)[:5])

                    return render(request, 'custom.html', {
                        "flag": True,
                        "reversetotalsKeys": reversetotalsKeys,
                        "reversetotalsValues": reversetotalsValues,
                        "totalreversetotalsValues": sum(reversetotalsValues),
                        "externaltop5componentskeys": list(externaltop5components.keys()),
                        "externaltop5componentsvalues": list(externaltop5components.values()),
                        "externaltop5statuskeys": list(externaltop5status.keys()),
                        "externaltop5statusvalues": list(externaltop5status.values()),
                        "project": project,
                        "messages": "",
                    })
            message = "No Jira Data Available. Please check the presets !!!"
            return render(request, 'custom.html', {
                "messages": message,
            })

    return render(request, 'custom.html', {
        "messages": "",
            })



def get_dp_data(project,startdate,enddate,username,token,next_date,labels,url):
    components = {}
    totals = {}
    status = {}
    numofissues = []
    dateofmonth = []
    startat = [0, 101, 201, 301, 401]
    error_flag = 0

    if len(labels) == 0:

        api_url= url+"?jql=created >= " + str(startdate) + " and created <= " + str(
            next_date) + " and project = "+project+" and issuetype in (Bug, Improvement) and reporter in (5d1c6ad2cdf26a0d349c8e4b, 5ca66ffa1b65666cbad29e71, 5ce2a47e48f7b90dbfd62f42, 6020ffa6e6124800694a5ea1, 5c82e2bb29592211228c8ad6, 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5ca7c177e623ae19ec5509f3, 6050684490f2880070e03fd0, 5c82e34fe6e3160b9b6fe340, 5d85053f1fcbda0da1348072, 6116df671e9ac7006816f5bc, 6020ffa77db80e006a04234c, currentUser(), 61437a3534599600714b6f9a, 5df828459a14250cb69ebf5c, 5d0a687201a78b0c4e014b76, 5df82840336e9e0cad16a003, 5ca6a83d3270b449b4fed5b2, 5c57d0a5b287111683605746, 5ff423bab66825010ea3ecb3, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469, 5f4c1666fdc3f5003f1f5ed5, 5b33fa796b94db70b4d76a90, 5f97df2299b42e00698ce0e8) order by created desc&maxResults=100"
    else:
        api_url = url+"?jql=created >= " + str(startdate) + " and created <= " + str(
            next_date) + " and project = "+project+" and issuetype in (Bug, Improvement, Task) and labels in (jira_escalated, EAPRequest) order by created desc&maxResults=100"

    r = requests.get(api_url, auth=HTTPBasicAuth(username, token))

    try:
        json_content = r.json()
    except ValueError:
        print("Error:", ValueError)
        error_flag = 1

    if json_content['total'] != 0:
        for i in json_content['issues']:
            if (project == 'DP'):
                jira_component = i['fields']['customfield_12136']['value']
            jira_createddate = i['fields']['created'].split('T')[0]
            jira_status = i['fields']['status']['name']

            if (project == 'DP'):
                if not jira_component in components:
                    components[jira_component] = 1
                else:
                    components[jira_component] += 1

            if not jira_createddate in totals:
                totals[jira_createddate] = 1
            else:
                totals[jira_createddate] += 1
            if not jira_status in status:
                status[jira_status] = 1
            else:
                status[jira_status] += 1

    total_jiras = json_content['total']
    iterations = int(total_jiras / 100)
    if total_jiras % 100:
        iterations = iterations + 1

    count = 1

    while count <= iterations - 1:
        if len(labels) == 0:
            api_url = url+"?jql=created >= " + str(startdate) + " and created <= " + str(
                next_date) + " and project = "+project+" and issuetype in (Bug, Improvement) and reporter in (5d1c6ad2cdf26a0d349c8e4b, 5ca66ffa1b65666cbad29e71, 5ce2a47e48f7b90dbfd62f42, 6020ffa6e6124800694a5ea1, 5c82e2bb29592211228c8ad6, 557058:53b57946-01ca-4125-9e92-b1cbb4c62182, 5ca7c177e623ae19ec5509f3, 6050684490f2880070e03fd0, 5c82e34fe6e3160b9b6fe340, 5d85053f1fcbda0da1348072, 6116df671e9ac7006816f5bc, 6020ffa77db80e006a04234c, currentUser(), 61437a3534599600714b6f9a, 5df828459a14250cb69ebf5c, 5d0a687201a78b0c4e014b76, 5df82840336e9e0cad16a003, 5ca6a83d3270b449b4fed5b2, 5c57d0a5b287111683605746, 5ff423bab66825010ea3ecb3, 5d11b4e3a3e35a0c8cd30d16, 61534c382f6aed0068476469, 5f4c1666fdc3f5003f1f5ed5, 5b33fa796b94db70b4d76a90, 5f97df2299b42e00698ce0e8) order by created desc&startAt=" + str(
                startat[count]) + "&maxResults=100"
        else:
            api_url = url+"?jql=created >= " + str(startdate) + " and created <= " + str(
                next_date) + " and project = "+project+" and issuetype in (Bug, Improvement, Task) and labels in (jira_escalated, EAPRequest) order by created desc&startAt="+str(startat[count])+"&maxResults=100"

        r = requests.get(api_url, auth=HTTPBasicAuth(username, token))

        try:
            json_content = r.json()
        except ValueError:
            print("Error:", ValueError)
            error_flag = 1

        if json_content['total'] != 0:
            for i in json_content['issues']:
                if (project == 'DP'):
                    jira_component = i['fields']['customfield_12136']['value']
                jira_createddate = i['fields']['created'].split('T')[0]
                jira_status = i['fields']['status']['name']

                if (project == 'DP'):
                    if not jira_component in components:
                        components[jira_component] = 1
                    else:
                        components[jira_component] += 1

                if not jira_createddate in totals:
                    totals[jira_createddate] = 1
                else:
                    totals[jira_createddate] += 1
                if not jira_status in status:
                    status[jira_status] = 1
                else:
                    status[jira_status] += 1

        count += 1

    
    return components, totals, status, error_flag


def save_dp_data(days,components,totals,status,project):
    all_components = {
        'AccountBilling': 0,
        'Analytics': 0,
        'BackendInfrastructure': 0,
        'CallExperience': 0,
        'CallingFeatures': 0,
        'ContactCenter': 0,
        'CustomerAgentAssist': 0,
        'DataInsights': 0,
        'DeveloperPlatform': 0,
        'Devices': 0,
        'DialpadTalk': 0,
        'DigitalExperience': 0,
        'EngineeringProductivity': 0,
        'FrontendInfrastructure': 0,
        'Growth': 0,
        'Integrations': 0,
        'Messaging': 0,
        'Mobile': 0,
        'ProductionSupport': 0,
        'UberConference': 0,
        'VoiceIntelligence': 0,
        'Website': 0,
    }
    all_status = {

        'Backlog': 0,
        'Blocked': 0,
        'CodeReview': 0,
        'Closed': 0,
        'InProgress': 0,
        'NeedsTriage': 0,
        'Open': 0,
        'ReadyforTesting': 0,
        'ReadyforProduction': 0,
        'ToDo': 0,
    }
    datetotal = {}

    for i in days:
        if str(i) in totals:
            datetotal[str(i)] = totals[str(i)]
        else:
            datetotal[str(i)] = 0

    while len(datetotal) != 31:
        datetotal[len(datetotal) + 1] = 0

    if (project == 'DP') or (project == 'DPExternal'):
        for i, j in components.items():
            cleanString = str(i)
            cleanString = ''.join(e for e in cleanString if e.isalnum())
            if cleanString in all_components.keys():
                all_components[cleanString] = components[i]

    for i, j in status.items():
        cleanString = str(i)
        cleanString = ''.join(e for e in cleanString if e.isalnum())
        if cleanString in all_status.keys():
            all_status[cleanString] = status[i]

    month_jira = list(datetotal.values())
    month_component = list(all_components.values())
    month_status = list(all_status.values())

    ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    print("Log Jira data to database at {}".format(ind_time))

    try:
        if project == 'DP':
            jira = DP.objects.get(id=1)
        if project == 'DPExternal':
            jira = DPExternal.objects.get(id=1)
        if project == 'DPM':
            jira = DPM.objects.get(id=1)
        if project == 'DPMExternal':
            jira = DPMExternal.objects.get(id=1)
        if project == 'MOB':
            jira = MOB.objects.get(id=1)
        if project == 'MOBExternal':
            jira = MOBExternal.objects.get(id=1)

        jira.One = month_jira[0]
        jira.Two = month_jira[1]
        jira.Three = month_jira[2]
        jira.Four = month_jira[3]
        jira.Five = month_jira[4]
        jira.Six = month_jira[5]
        jira.Seven = month_jira[6]
        jira.Eight = month_jira[7]
        jira.Nine = month_jira[8]
        jira.Ten = month_jira[9]
        jira.Eleven = month_jira[10]
        jira.Twelve = month_jira[11]
        jira.Thirteen = month_jira[12]
        jira.Fourteen = month_jira[13]
        jira.Fifteen = month_jira[14]
        jira.Sixteen = month_jira[15]
        jira.Seventeen = month_jira[16]
        jira.Eighteen = month_jira[17]
        jira.Nineteen = month_jira[18]
        jira.Twenty = month_jira[19]
        jira.Twentyone = month_jira[20]
        jira.Twentytwo = month_jira[21]
        jira.Twentythree = month_jira[22]
        jira.Twentyfour = month_jira[23]
        jira.Twentyfive = month_jira[24]
        jira.Twentysix = month_jira[25]
        jira.Twentyseven = month_jira[26]
        jira.Twentyeight = month_jira[27]
        jira.Twentynine = month_jira[28]
        jira.Thirty = month_jira[29]
        jira.Thirtyone = month_jira[30]
        jira.AccountBilling = month_component[0]
        jira.Analytics = month_component[1]
        jira.BackendInfrastructure = month_component[2]
        jira.CallExperience = month_component[3]
        jira.CallingFeatures = month_component[4]
        jira.ContactCenter = month_component[5]
        jira.CustomerAgentAssist = month_component[6]
        jira.DataInsights = month_component[7]
        jira.DeveloperPlatform = month_component[8]
        jira.Devices = month_component[9]
        jira.DialpadTalk = month_component[10]
        jira.DigitalExperience = month_component[11]
        jira.EngineeringProductivity = month_component[12]
        jira.FrontendInfrastructure = month_component[13]
        jira.Growth = month_component[14]
        jira.Integrations = month_component[15]
        jira.Messaging = month_component[16]
        jira.Mobile = month_component[17]
        jira.ProductionSupport = month_component[18]
        jira.UberConference = month_component[19]
        jira.VoiceIntelligence = month_component[20]
        jira.Website = month_component[21]
        jira.Backlog = month_status[0]
        jira.Blocked = month_status[1]
        jira.CodeReview = month_status[2]
        jira.Closed = month_status[3]
        jira.InProgress = month_status[4]
        jira.NeedsTriage = month_status[5]
        jira.Open = month_status[6]
        jira.ReadyforTesting = month_status[7]
        jira.ReadyforProduction = month_status[8]
        jira.ToDo = month_status[9]
        jira.LastUpdate = ind_time

        jira.save()
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        pass

    return



def save_jira_data():
    year = date.today().year
    month = date.today().month
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
    next_date = days[-1] + timedelta(days=1)
    url = 'https://dialpad.atlassian.net/rest/api/2/search'
    username = env('DJANGO_JIRA_USER')
    token = env('DJANGO_JIRA_TOKEN')
    #print("Get Data from Jira")
    internal_dp_labels = []
    int_components, int_totals, int_status, int_error_flag = get_dp_data("DP",days[0], days[-1], username, token, next_date,internal_dp_labels,url)
    save_dp_data(days,int_components,int_totals,int_status,'DP')

    time.sleep(2)

    external_dp_labels = ['jira_escalated', 'EAPRequest']
    ext_components, ext_totals, ext_status, ext_error_flag = get_dp_data("DP", days[0], days[-1], username, token, next_date,external_dp_labels,url)
    save_dp_data(days, ext_components, ext_totals, ext_status, 'DPExternal')

    time.sleep(2)

    internal_dp_labels = []
    int_dpm_components, int_dpm_totals, int_dpm_status, int_dpm_error_flag = get_dp_data("UC", days[0], days[-1],username,token,next_date, internal_dp_labels,url)
    save_dp_data(days, int_dpm_components, int_dpm_totals, int_dpm_status, 'DPM')

    time.sleep(2)

    external_dp_labels = ['jira_escalated', 'EAPRequest']
    ext_dpm_components, ext_dpm_totals, ext_dpm_status, ext_dpm_error_flag = get_dp_data("UC", days[0], days[-1],username,token,next_date, external_dp_labels,url)
    save_dp_data(days, ext_dpm_components, ext_dpm_totals, ext_dpm_status, 'DPMExternal')

    internal_dp_labels = []
    int_mob_components, int_mob_totals, int_mob_status, int_mob_error_flag = get_dp_data("MOB", days[0], days[-1],username, token,next_date, internal_dp_labels,url)
    save_dp_data(days, int_mob_components, int_mob_totals, int_mob_status, 'MOB')

    time.sleep(2)

    external_dp_labels = ['jira_escalated', 'EAPRequest']
    ext_mob_components, ext_mob_totals, ext_mob_status, ext_mob_error_flag = get_dp_data("MOB", days[0], days[-1],username, token,next_date, external_dp_labels,url)
    save_dp_data(days, ext_mob_components, ext_mob_totals, ext_mob_status, 'MOBExternal')


    return



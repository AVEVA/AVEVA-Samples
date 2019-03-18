# program - panda.py
#
# Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
#
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
#
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
#
# OSIsoft, LLC
# 1600 Alvarado St, San Leandro, CA 94577

from sdspy import *
import configparser
import datetime
import time
import math
import inspect
import collections

import pandas as pd
import numpy as np # linear algebra

from random import sample



######################################################################################################
# The following define the identifiers we'll use throughout
######################################################################################################


def get_input_matrix(train):
    return np.swapaxes(np.column_stack((train.season, train.mnth, train.hr, train.holiday, train.weekday, train.workingday, train.yr, train.temp, train.atemp, train.windspeed, train.hum)),0,1)
   
sampleDataViewId = "s"

try:
    config = configparser.ConfigParser()
    config.read('config - panda.ini')


    print("------------------------------------------")
    print("  _________    .___     __________        ")        
    print(" /   _____/  __| _/_____\______   \___.__.")
    print(" \_____  \  / __ |/  ___/|     ___<   |  |")
    print(" /        \/ /_/ |\___ \ |    |    \___  |")
    print("/_______  /\____ /____  >|____|    / ____|")
    print("        \/      \/    \/           \/     ")	
    print("------------------------------------------")

    client = SdsClient(config.get('Access', 'Tenant'), config.get('Access', 'Address'), config.get('Credentials', 'Resource'),
                      config.get('Credentials', 'Authority'), config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

    sampleDataviewId = "s11"
    namespaceId = config.get('Configurations', 'Namespace')
    dv = None
    try:
        dv = client.getDataview(namespaceId,sampleDataviewId)   
    except Exception as ex:
        print(("Encountered Error getting dataview: {error}".format(error = ex)))
        dv = None

    if dv == None:
        try:
            print("making one")

            dataview = Dataview()
            dataview.Id = sampleDataviewId
            dg  = DataviewGroupRule()
            dg.Id = "Default"
            dg.Type = "StreamTag"
            dataview.GroupRules = []
            dataview.GroupRules.append(dg) 
            query  = DataviewQuery()
            query.Id = sampleDataviewId
            queryQuery = DataviewQueryQuery()
            queryQuery.Type = 'StreamName'
            queryQuery.Value =  'bicycle'
            queryQuery.Operator = 'Contains'
            query.Query = queryQuery
            dataview.Queries = []
            dataview.Queries.append(query)
            map = DataviewMapping()
            map.IsDefault = True
            dataview.Mappings = map
            dataview.IndexDataType = "datetime"	      
            indexConfig = DataviewIndexConfig()
            indexConfig.IsDefault = False
            indexConfig.StartIndex = "2011-01-01T00:00:00Z"
            indexConfig.EndIndex = "2011-08-01T00:00:00Z"
            indexConfig.Interval = "01:00:00"
            indexConfig.Mode = "interpolated"
            dataview.IndexConfig = indexConfig
            dataviews = client.postDataview(namespaceId, dataview)
        
        except Exception as ex:
            print(("Encountered Error making a dataview: {error}".format(error = ex)))     
  
    data = client.getDataviewPreview(namespaceId, sampleDataviewId)
    df = pd.DataFrame(data)
    msk = np.random.rand(len(df)) < 0.8
    train_df = df[msk]
    test_df = df[~msk]

    #print(df.head)

    cntColumn  = train_df['cnt']
    test_cntColumn  = test_df['cnt']

    col = np.column_stack(get_input_matrix(train_df))
    test_col = np.column_stack(get_input_matrix(test_df))

    (w, a, b, c) = np.linalg.lstsq(col, cntColumn, rcond = None)
    print(w)

    cnt_predictions = np.matmul(col, w).round(decimals = 0)
    test_cnt_predictions = np.matmul(test_col, w).round(decimals = 0)

    #jupter notebooks
    #plt.plot((cnt_predictions - cntColumn).abs())
    #plt.plot((test_cnt_predictions - test_cntColumn).abs())

    #print(cnt_predictions)
    #print(cntColumn)
    #print(((cnt_predictions - cntColumn).abs()).mean())

    print(((test_cnt_predictions - test_cntColumn).abs()).mean())

except Exception as ex:
    print(("Encountered Error: {error}".format(error = ex)))

finally:
    print(("Done"))
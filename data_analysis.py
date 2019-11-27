import pandas as pd
import numpy as np



type= input("please enter the type (2g or 3g or 4g):-")

def two():
    print("Reading Excel files....")
    df1 = pd.read_csv('2g\\2g_pre.csv', index_col=2, skiprows=6)

    df2 = pd.read_csv('2g\\2g_post.csv', index_col=2, skiprows=6)

    print("Excel files has been read..")
    threshold_path = pd.read_csv('2g\\2g_threshold.csv', index_col=False, header=None, skiprows=1)
    ultimate = pd.ExcelWriter("2g\\2G Ultimate.xlsx", engine='openpyxl')

    print("Taking the threshold values....")
    th_list = list(threshold_path[1])
    tch, voice_tf, tf_900, tf_1800, mpd, call_drops, sdcch, tch_cong, download_data, data_tp, handover, trx_num, trx_avail = th_list

    site_path = pd.read_csv('2g\\2g_site_list.csv', index_col=False, header=None, skiprows=1)

    site_list = list(site_path[0])

    # list1=['SYKDB2C', 'SYIDG2C', 'SYCM1MB', 'SYLMB2B', 'NGKZM1C', 'SKKRD1B', 'SRNLB2C','DHMKT2C', 'GPBNC1C' , 'DHUH2PG']

    list2 = ['TCH Availability', 'Voice Traffic_Sum(Erl)', '900M TCH Traffic(Erl)', '1800M TCH Traffic(Erl)',
             'Minutes Per Drop, MPD',
             'CM3303A:Number of Call Drops on TCH (Before Disconnection)', 'SDCCH Congestion Rate(%)',
             'TCH Congestion Rate(%)',
             'Download Combined Data Volume_MB', 'Data Throughput (Kbps)', 'Handover Success Rate, Intra BSC',
             'S3655:Number of configured TRXs in a cell',
             'S3656:Number of available TRXs in a cell']

    list9= ['TCH Availability', 'Voice Traffic_Sum(Erl)', '900M TCH Traffic(Erl)', '1800M TCH Traffic(Erl)',
             'Minutes Per Drop, MPD',
             'CM3303A:Number of Call Drops on TCH (Before Disconnection)', 'SDCCH Congestion Rate(%)',
             'TCH Congestion Rate(%)',
             'Download Combined Data Volume_MB', 'Data Throughput (Kbps)', 'Handover Success Rate, Intra BSC']

    list3 = ['Time', 'GBSC', 'CellIndex', 'Site Name', 'Integrity', 'Cell availability']

    list4 = ['Time', 'GBSC']

    list5 = ['Cell availability', 'TCH Availability', 'Voice Traffic_Sum(Erl)', '900M TCH Traffic(Erl)',
             '1800M TCH Traffic(Erl)', 'Minutes Per Drop, MPD',
             'CM3303A:Number of Call Drops on TCH (Before Disconnection)', 'SDCCH Congestion Rate(%)',
             'TCH Congestion Rate(%)',
             'Download Combined Data Volume_MB', 'Data Throughput (Kbps)', 'Handover Success Rate, Intra BSC', 'TRX status']

    list6= ['Time', 'GBSC','Cell availability', 'TCH Availability', 'Voice Traffic_Sum(Erl)', '900M TCH Traffic(Erl)',
             '1800M TCH Traffic(Erl)', 'Minutes Per Drop, MPD',
             'CM3303A:Number of Call Drops on TCH (Before Disconnection)', 'SDCCH Congestion Rate(%)',
             'TCH Congestion Rate(%)',
             'Download Combined Data Volume_MB', 'Data Throughput (Kbps)', 'Handover Success Rate, Intra BSC',
             'TRX status']
    list7 = ['zero(no change)', 'Extra TRX', 'Performance degraded', 'TRX Down', 'TRX Added', 'TRX Deleted',
             'Cell is Down', 'Performance degraded(pre-value= 0)']

    list8 =['Cell', 'TCH', 'VoiceTraffic', '900M)',
             '1800M', 'MPD',
             'CallDrops', 'SDCCH CR',
             'TCH CR',
             'Download Data', 'Data Throughput', 'Handover',
             'TRX status']

    df1.replace(to_replace='/0', value=0.00, inplace=True)
    df2.replace(to_replace='/0', value=0.00, inplace=True)


    df1[list2] = df1[list2].apply(pd.to_numeric)
    df2[list2] = df2[list2].apply(pd.to_numeric)



    filtered1 = df1[df1['Site Name'].isin(site_list)].sort_values(by=['Cell Name'])

    filtered2 = df2[df2['Site Name'].isin(site_list)].sort_values(by=['Cell Name'])

    filtered1.set_index('Cell Name', inplace=True)
    filtered2.set_index('Cell Name', inplace=True)


    print(filtered2)
    print("the whole network dump is filtered & sorted...")

    info1 = filtered1[list3]
    info2 = filtered2[list3]

    tf_sum1 = filtered1[list9]
    tf_sum2 = filtered2[list9]

    result1 = (tf_sum2 - tf_sum1) * 100 / tf_sum1
    result2= pd.DataFrame()
    result2['TRX status']= filtered2['S3656:Number of available TRXs in a cell']- filtered2['S3655:Number of configured TRXs in a cell']
    print(result2)

    result= pd.concat([result1,result2], axis=1)
    result.replace([np.inf, -np.inf], 999, inplace=True)
    print("Calculation done...")
    # final = info2.join(result)

    final= pd.concat([info2,result],axis=1)


    # final.replace([np.inf, -np.inf], 999, inplace=True)
    final.dropna(how='all', inplace=True)
    final.fillna(8888, inplace=True)

    final.to_excel(ultimate, sheet_name='raw')
    # final.to_csv('2g\\2G_Raw report.csv')
    print("2G Raw data inserted to excel-->>")
    df_f = final

    print("applying the threshold values...")

    df_f['Cell availability'] = np.where(df_f['Cell availability'] == 0, 'Cell is Down', df_f['Cell availability'])
    df_f['TCH Availability'] = np.where(df_f['TCH Availability'] < -tch, 'Performance degraded',
                                        df_f['TCH Availability'])
    df_f['Voice Traffic_Sum(Erl)'] = np.where((df_f['Voice Traffic_Sum(Erl)'] < -voice_tf), 'Performance degraded',
                                              np.where((df_f['Voice Traffic_Sum(Erl)'] == 8888), 'zero(no change)',
                                                       df_f['Voice Traffic_Sum(Erl)']))
    df_f['900M TCH Traffic(Erl)'] = np.where((df_f['900M TCH Traffic(Erl)'] < -tf_900), 'Performance degraded',
                                             np.where((df_f['900M TCH Traffic(Erl)'] == 8888), 'zero(no change)',
                                                      df_f['900M TCH Traffic(Erl)']))
    df_f['1800M TCH Traffic(Erl)'] = np.where((df_f['1800M TCH Traffic(Erl)'] < -tf_1800), 'Performance degraded',
                                              np.where((df_f['1800M TCH Traffic(Erl)'] == 8888), 'zero(no change)',
                                                       df_f['1800M TCH Traffic(Erl)']))
    df_f['Minutes Per Drop, MPD'] = np.where((df_f['Minutes Per Drop, MPD'] < -mpd), 'Performance degraded',
                                             np.where((df_f['Minutes Per Drop, MPD'] == 8888), 'zero(no change)',
                                                      df_f['Minutes Per Drop, MPD']))
    df_f['CM3303A:Number of Call Drops on TCH (Before Disconnection)'] = np.where(
        (df_f['CM3303A:Number of Call Drops on TCH (Before Disconnection)'] < -call_drops), 'Performance degraded',
        np.where((df_f['CM3303A:Number of Call Drops on TCH (Before Disconnection)'] == 8888), 'zero(no change)',
                 df_f['CM3303A:Number of Call Drops on TCH (Before Disconnection)']))

    df_f['SDCCH Congestion Rate(%)'] = np.where(
        (df_f['SDCCH Congestion Rate(%)'] > sdcch) & (df_f['SDCCH Congestion Rate(%)'] != 999) & (
                    df_f['SDCCH Congestion Rate(%)'] != 8888), 'Performance degraded',
        np.where(df_f['SDCCH Congestion Rate(%)'] == 8888, 'zero(no change)',
                 np.where(df_f['SDCCH Congestion Rate(%)'] == 999, 'Performance degraded(pre-value= 0)',
                          df_f['SDCCH Congestion Rate(%)'])))
    df_f['TCH Congestion Rate(%)'] = np.where(
        (df_f['TCH Congestion Rate(%)'] > tch_cong) & (df_f['TCH Congestion Rate(%)'] != 8888) & (
                    df_f['TCH Congestion Rate(%)'] != 999), 'Performance degraded',
        np.where(df_f['TCH Congestion Rate(%)'] == 8888, 'zero(no change)',
                 np.where(df_f['TCH Congestion Rate(%)'] == 999, 'Performance degraded(pre-value= 0)',
                          df_f['TCH Congestion Rate(%)'])))

    df_f['Download Combined Data Volume_MB'] = np.where((df_f['Download Combined Data Volume_MB'] < -download_data),
                                                        'Performance degraded',
                                                        np.where((df_f['Download Combined Data Volume_MB'] == 8888),
                                                                 'zero(no change)',
                                                                 df_f['Download Combined Data Volume_MB']))
    df_f['Data Throughput (Kbps)'] = np.where((df_f['Data Throughput (Kbps)'] < -data_tp), 'Performance degraded',
                                              np.where((df_f['Data Throughput (Kbps)'] == 8888), 'zero(no change)',
                                                       df_f['Data Throughput (Kbps)']))
    df_f['Handover Success Rate, Intra BSC'] = np.where((df_f['Handover Success Rate, Intra BSC'] < -handover),
                                                        'Performance degraded',
                                                        np.where((df_f['Handover Success Rate, Intra BSC'] == 8888),
                                                                 'zero(no change)',
                                                                 df_f['Handover Success Rate, Intra BSC']))


    df_f['TRX status'] = np.where(
        (df_f['TRX status'] < trx_avail), 'TRX Down',
        np.where((df_f['TRX status'] == 8888), 'zero(no change)',
                 np.where((df_f['TRX status'] > trx_avail), 'Extra TRX',
                          df_f['TRX status'])))

    # df_f.to_csv('2g\\2G Mid-level report.csv')
    # print("2G Mid-level report.csv is created-->>")

    # tab = []
    # unavail=[]
    # cell_list = list(df_f['Cell Name'])
    # for i in cell_list:
    #     a = df_f.loc[df_f['Cell Name'] == i]
    #     if a.empty == False:
    #         a_info = a[list4]
    #
    #         b = a[(a.iloc[:, 5:] == 'zero(no change)') | (a.iloc[:, 5:] == 'Extra TRX') | (
    #                     a.iloc[:, 5:] == 'Performance degraded')
    #               | (a.iloc[:, 5:] == 'TRX Down') | (a.iloc[:, 5:] == 'TRX Added') | (a.iloc[:, 5:] == 'TRX Deleted') |
    #               (a.iloc[:, 5:] == 'Cell is Down') | (a.iloc[:, 5:] == 'Performance degraded(pre-value= 0)')]
    #
    #         b.dropna(axis=1, inplace=True)
    #
    #         # d = a_info.join(b)
    #         d= pd.concat([a_info,b], axis=1)
    #         d.set_index('Cell Name', inplace=True)
    #         e = d.transpose()
    #         table = tb(e, headers='keys', tablefmt='psql')
    #         tab.append(table)
    #         tab.append('\n\n')
    #     else:
    #         unavail.append(i)
    #         unavail.append('\n')
    # print('unavailable:-', unavail)
    #
    # with open('2g\\unavailable.txt', 'w') as g:
    #     g.writelines(unavail)
    #
    # with open('2g\\2G Final report_2.txt', 'w') as f:
    #     f.writelines(tab)

    df_ff = df_f[(df_f.iloc[:, 5:] == 'zero(no change)') | (df_f.iloc[:, 5:] == 'Extra TRX') | (
                df_f.iloc[:, 5:] == 'Performance degraded')
                 | (df_f.iloc[:, 5:] == 'TRX Down') | (df_f.iloc[:, 5:] == 'TRX Added') | (
                             df_f.iloc[:, 5:] == 'TRX Deleted') |
                 (df_f.iloc[:, 5:] == 'Cell is Down') | (df_f.iloc[:, 5:] == 'Performance degraded(pre-value= 0)')]



    df_info = df_f[list4]
    df_ff.fillna(' ', inplace=True)
    df_half = df_ff[list5]

    # g = df_info.join(df_half)
    g = pd.concat([df_info, df_half], axis=1)
    # g.set_index('Cell Name', inplace=True)
    # g.to_csv('2g\\2G Final report.csv')

    # j=0
    # for i in list5:
    #     ultra_filt = g[g[i].isin(list7)]
    #     ultra_filt[i].to_excel(ultimate, sheet_name=list8[j])
    #     j+=1





    rounded_res = result.round(decimals=2)
    res_ext = filtered2['Cell availability'].to_frame()

    fin_res = pd.concat([res_ext, rounded_res], axis=1)

    x = df_half.astype(str) + " <" + fin_res.astype(str) + ">"

    h = pd.concat([df_info, x], axis=1)
    # h.set_index('Cell Name', inplace=True)
    h = h[list6]


    j=0
    for i in list5:
        ultra_filt = h[h[i].str.contains('[A-Za-z]+',na=False, regex=True)]
        # ultra_filt.fillna(' ', inplace=True)
        ultra_filt[i].to_excel(ultimate, sheet_name=list8[j])
        j+=1


    # test= h[h[list5[1]].str.contains('[A-Za-z\s]+', regex=True)]
    # print(test[list5[1]])


    # h.to_csv("2g\\2G ultra.csv")
    h.to_excel(ultimate, sheet_name='ultra')
    print("2G Final modified data is inserted-->>")
    ultimate.save()

def three():
    print("Reading Excel files....")
    df1 = pd.read_csv('3g\\3g_pre.csv', index_col=2, skiprows=6)
    df2 = pd.read_csv('3g\\3g_post.csv', index_col=2, skiprows=6)
    print("Excel files has been read..")
    threshold_path = pd.read_csv('3g\\3g_threshold.csv', index_col=False, header=None, skiprows=1)

    ultimate = pd.ExcelWriter("3g\\3G Ultimate.xlsx", engine='openpyxl')

    print("Taking the threshold values....")
    th_list = list(threshold_path[1])
    voice_tf, mpd, call_drops, rrc, csrab, psrab, data_vol, cell_tp, soft_handover, hard_handover = th_list

    site_path = pd.read_csv('3g\\3g_site_list.csv', index_col=False, header=None, skiprows=1)

    site_list = list(site_path[0])
    # list1=['SYKDB2C', 'SYIDG2C', 'SYCM1MB', 'SYLMB2B', 'NGKZM1C', 'SKKRD1B', 'SRNLB2C','DHMKT2C', 'GPBNC1C' , 'DHUH2PG']

    list2 = ['Voice Traffic (Erl)(Erl)', '3G Voice MPD(min)', 'CS Call Drop Rate (Total)(%)',
             'RRC Congestion(%)', 'CS RAB Congestion(%)', 'PS RAB Congestion(%)',
             '3G Total Data Volume (GB)', 'HSDPA Cell Throughput (kbit/s)', 'Soft Handover Success Rate(%)',
             'IRAT Hard Handover Success Rate(%)']

    list3 = ['Time', 'RNC', 'NodeB Name', 'Integrity', '3G Cell Availability']

    list4 = ['Time', 'RNC']

    list5 = ['3G Cell Availability', 'Voice Traffic (Erl)(Erl)', '3G Voice MPD(min)', 'CS Call Drop Rate (Total)(%)',
             'RRC Congestion(%)', 'CS RAB Congestion(%)', 'PS RAB Congestion(%)',
             '3G Total Data Volume (GB)', 'HSDPA Cell Throughput (kbit/s)', 'Soft Handover Success Rate(%)',
             'IRAT Hard Handover Success Rate(%)']

    list6 = ['Time', 'RNC','3G Cell Availability', 'Voice Traffic (Erl)(Erl)', '3G Voice MPD(min)', 'CS Call Drop Rate (Total)(%)',
             'RRC Congestion(%)', 'CS RAB Congestion(%)', 'PS RAB Congestion(%)',
             '3G Total Data Volume (GB)', 'HSDPA Cell Throughput (kbit/s)', 'Soft Handover Success Rate(%)',
             'IRAT Hard Handover Success Rate(%)']

    list7 = ['zero(no change)', 'Extra TRX', 'Performance degraded', 'TRX Down', 'TRX Added', 'TRX Deleted',
             'Cell is Down', 'Performance degraded(pre-value= 0)']

    list8 = ['Cell Avail', 'Voice Traffic', 'MPD', 'CS Call Drop',
             'RRC', 'CS RAB', 'PS RAB',
             'Data Volume(GB)', 'HSDPA Throughput', 'Soft Handover',
             'Hard Handover']


    df1.replace(to_replace='/0', value=0.00, inplace=True)
    df2.replace(to_replace='/0', value=0.00, inplace=True)

    df1[list2] = df1[list2].apply(pd.to_numeric)
    df2[list2] = df2[list2].apply(pd.to_numeric)

    filtered1 = df1[df1['Cell Name'].isin(site_list)].sort_values(by=['Cell Name'])
    filtered2 = df2[df2['Cell Name'].isin(site_list)].sort_values(by=['Cell Name'])

    filtered1.set_index('Cell Name', inplace=True)
    filtered2.set_index('Cell Name', inplace=True)




    print(filtered2)
    print("the whole network dump is filtered & sorted...")

    info1 = filtered1[list3]
    info2 = filtered2[list3]

    tf_sum1 = filtered1[list2]
    tf_sum2 = filtered2[list2]

    print(info2)

    result = (tf_sum2 - tf_sum1) * 100 / tf_sum1
    result.replace([np.inf, -np.inf], 999, inplace=True)
    print(result)
    print("Calculation done...")
    final= pd.concat([info2,result],axis=1)

    # final.replace([np.inf, -np.inf], 999, inplace=True)
    final.dropna(how='all', inplace =True)

    final.fillna(8888, inplace=True)
    print(final)
    final.to_excel(ultimate, sheet_name='raw')
    # final.to_csv('3g\\3G Raw report.csv')
    print("3G Raw data inserted to excel-->>")
    df_f = final

    print("applying the threshold values...")

    df_f['3G Cell Availability'] = np.where(df_f['3G Cell Availability'] != 100, 'Cell is Down',
                                            df_f['3G Cell Availability'])

    df_f['Voice Traffic (Erl)(Erl)'] = np.where((df_f['Voice Traffic (Erl)(Erl)'] < -voice_tf), 'Performance degraded',
                                                np.where((df_f['Voice Traffic (Erl)(Erl)'] == 8888), 'zero(no change)',
                                                         df_f['Voice Traffic (Erl)(Erl)']))

    df_f['3G Voice MPD(min)'] = np.where((df_f['3G Voice MPD(min)'] < -mpd), 'Performance degraded',
                                         np.where((df_f['3G Voice MPD(min)'] == 8888), 'zero(no change)',
                                                  df_f['3G Voice MPD(min)']))

    df_f['CS Call Drop Rate (Total)(%)'] = np.where(
        (df_f['CS Call Drop Rate (Total)(%)'] > call_drops) & (df_f['CS Call Drop Rate (Total)(%)'] != 999) & (
                    df_f['CS Call Drop Rate (Total)(%)'] != 8888), 'Performance degraded',
        np.where(df_f['CS Call Drop Rate (Total)(%)'] == 8888, 'zero(no change)',
                 np.where(df_f['CS Call Drop Rate (Total)(%)'] == 999, 'Performance degraded(pre-value= 0)',
                          df_f['CS Call Drop Rate (Total)(%)'])))
    df_f['RRC Congestion(%)'] = np.where(
        (df_f['RRC Congestion(%)'] > rrc) & (df_f['RRC Congestion(%)'] != 8888) & (df_f['RRC Congestion(%)'] != 999),
        'Performance degraded',
        np.where(df_f['RRC Congestion(%)'] == 8888, 'zero(no change)',
                 np.where(df_f['RRC Congestion(%)'] == 999, 'Performance degraded(pre-value= 0)',
                          df_f['RRC Congestion(%)'])))

    df_f['CS RAB Congestion(%)'] = np.where(
        (df_f['CS RAB Congestion(%)'] > csrab) & (df_f['CS RAB Congestion(%)'] != 8888) & (
                    df_f['CS RAB Congestion(%)'] != 999), 'Performance degraded',
        np.where(df_f['CS RAB Congestion(%)'] == 8888, 'zero(no change)',
                 np.where(df_f['CS RAB Congestion(%)'] == 999, 'Performance degraded(pre-value= 0)',
                          df_f['CS RAB Congestion(%)'])))

    df_f['PS RAB Congestion(%)'] = np.where(
        (df_f['PS RAB Congestion(%)'] > psrab) & (df_f['PS RAB Congestion(%)'] != 8888) & (
                    df_f['PS RAB Congestion(%)'] != 999), 'Performance degraded',
        np.where(df_f['PS RAB Congestion(%)'] == 8888, 'zero(no change)',
                 np.where(df_f['PS RAB Congestion(%)'] == 999, 'Performance degraded(pre-value= 0)',
                          df_f['PS RAB Congestion(%)'])))

    df_f['3G Total Data Volume (GB)'] = np.where((df_f['3G Total Data Volume (GB)'] < -data_vol),
                                                 'Performance degraded',
                                                 np.where((df_f['3G Total Data Volume (GB)'] == 8888),
                                                          'zero(no change)',
                                                          df_f['3G Total Data Volume (GB)']))

    df_f['HSDPA Cell Throughput (kbit/s)'] = np.where((df_f['HSDPA Cell Throughput (kbit/s)'] < -cell_tp),
                                                      'Performance degraded',
                                                      np.where((df_f['HSDPA Cell Throughput (kbit/s)'] == 8888),
                                                               'zero(no change)',
                                                               df_f['HSDPA Cell Throughput (kbit/s)']))

    df_f['Soft Handover Success Rate(%)'] = np.where((df_f['Soft Handover Success Rate(%)'] < -soft_handover),
                                                     'Performance degraded',
                                                     np.where((df_f['Soft Handover Success Rate(%)'] == 8888),
                                                              'zero(no change)',
                                                              df_f['Soft Handover Success Rate(%)']))

    df_f['IRAT Hard Handover Success Rate(%)'] = np.where((df_f['IRAT Hard Handover Success Rate(%)'] < -hard_handover),
                                                          'Performance degraded',
                                                          np.where((df_f['IRAT Hard Handover Success Rate(%)'] == 8888),
                                                                   'zero(no change)',
                                                                   df_f['IRAT Hard Handover Success Rate(%)']))

    # df_f.to_csv('3g\\3G Mid-level report.csv')
    # print("3G Mid-level report.csv is created-->>")

    # tab = []
    # unavail= []
    #
    # for i in site_list:
    #
    #     a = df_f.loc[df_f['Cell Name'] == i]
    #     if a.empty==False:
    #         a_info = a[list4]
    #
    #         b = a[(a.iloc[:, 4:] == 'zero(no change)') | (a.iloc[:, 4:] == 'Extra TRX') | (
    #                     a.iloc[:, 4:] == 'Performance degraded')
    #               | (a.iloc[:, 4:] == 'TRX Down') | (a.iloc[:, 4:] == 'TRX Added') | (a.iloc[:, 4:] == 'TRX Deleted') |
    #               (a.iloc[:, 4:] == 'Cell is Down') | (a.iloc[:, 4:] == 'Performance degraded(pre-value= 0)')]
    #
    #         b.dropna(axis=1, inplace=True)
    #
    #         d = pd.concat([a_info, b], axis=1)
    #         d.set_index('Cell Name', inplace=True)
    #         e = d.transpose()
    #         table = tb(e, headers='keys', tablefmt='psql')
    #         tab.append(table)
    #         tab.append('\n\n')
    #     else:
    #
    #         unavail.append(i)
    #         unavail.append('\n')
    #
    # print('unavailable:-',unavail)
    # with open('3g\\unavailable.txt', 'w') as g:
    #     g.writelines(unavail)
    #
    # with open('3g\\3G Final report.txt', 'w') as f:
    #     f.writelines(tab)

    df_ff = df_f[(df_f.iloc[:, 4:] == 'zero(no change)') | (df_f.iloc[:, 4:] == 'Extra TRX') | (
                df_f.iloc[:, 4:] == 'Performance degraded')
                 | (df_f.iloc[:, 4:] == 'TRX Down') | (df_f.iloc[:, 4:] == 'TRX Added') | (
                             df_f.iloc[:, 4:] == 'TRX Deleted') |
                 (df_f.iloc[:, 4:] == 'Cell is Down') | (df_f.iloc[:, 4:] == 'Performance degraded(pre-value= 0)')]

    # print(df_ff)

    df_info = df_f[list4]
    df_ff.fillna(' ', inplace=True)
    df_half = df_ff[list5]

    g= pd.concat([df_info, df_half],axis=1)
    # g.set_index('Cell Name', inplace=True)
    # g.to_csv('3g\\3G Final report.csv')

    # j=0
    # for i in list5:
    #     ultra_filt = g[g[i].isin(list7)]
    #     ultra_filt[i].to_excel(ultimate, sheet_name=list8[j])
    #     j+=1

    rounded_res = result.round(decimals=2)

    res_ext = filtered2['3G Cell Availability'].to_frame()

    fin_res = pd.concat([res_ext, rounded_res], axis=1)

    x = df_half.astype(str) + " <" + fin_res.astype(str) + ">"
    h = pd.concat([df_info, x], axis=1)

    # h.set_index('Cell Name', inplace=True)
    h = h[list6]

    j=0
    for i in list5:
        ultra_filt = h[h[i].str.contains('[A-Za-z]+',na=False, regex=True)]
        # ultra_filt.fillna(' ', inplace=True)
        ultra_filt[i].to_excel(ultimate, sheet_name=list8[j])
        j+=1

    # h.to_csv("3g\\3G ultra.csv")
    h.to_excel(ultimate, sheet_name='ultra')
    print("3G Final data  is inserted-->>")
    ultimate.save()

def lte():
    print("Reading Excel files....")
    df1 = pd.read_csv('4g\\4g_pre.csv', index_col=5, skiprows=6)
    df2 = pd.read_csv('4g\\4g_post.csv', index_col=5, skiprows=6)
    print("Excel files has been read..")
    threshold_path = pd.read_csv('4g\\4g_threshold.csv', index_col=False, header=None, skiprows=1)

    ultimate = pd.ExcelWriter("4g\\4G Ultimate.xlsx", engine='openpyxl')

    print("Taking the threshold values....")
    th_list = list(threshold_path[1])
    rrc, erab, aun, data_vol, user_tp = th_list

    site_path = pd.read_csv('4g\\4g_site_list.csv', index_col=False, header=None, skiprows=1)

    site_list = list(site_path[0])
    # list1=['SYKDB2C', 'SYIDG2C', 'SYCM1MB', 'SYLMB2B', 'NGKZM1C', 'SKKRD1B', 'SRNLB2C','DHMKT2C', 'GPBNC1C' , 'DHUH2PG']

    list2 = ['RRC Setup SR %(%)', 'eRAB Setup SR(%)', 'Average User Number (per cell)',
             'DL Data Volume (MB)(MB)', 'DL Avg User Throughput (kbps)']

    list3 = ['Time', 'LocalCell Id', 'Integrity', 'Cell Availablility (%)']

    list4 = ['Time', 'LocalCell Id']

    list5 = ['Cell Availablility (%)', 'RRC Setup SR %(%)', 'eRAB Setup SR(%)', 'Average User Number (per cell)',
             'DL Data Volume (MB)(MB)', 'DL Avg User Throughput (kbps)']

    list6 = ['Time', 'LocalCell Id', 'Cell Availablility (%)', 'RRC Setup SR %(%)', 'eRAB Setup SR(%)',
             'Average User Number (per cell)',
             'DL Data Volume (MB)(MB)', 'DL Avg User Throughput (kbps)']

    list7 = ['zero(no change)', 'Extra TRX', 'Performance degraded', 'TRX Down', 'TRX Added', 'TRX Deleted',
             'Cell is Down', 'Performance degraded(pre-value= 0)']

    list8 = ['Cell Availablility', 'RRC', 'eRAB', 'Avg User No',
             'DL Data', 'DL Throughput']


    df1.replace(to_replace='/0', value=0.00, inplace=True)
    df2.replace(to_replace='/0', value=0.00, inplace=True)

    df1[list2] = df1[list2].apply(pd.to_numeric)
    df2[list2] = df2[list2].apply(pd.to_numeric)

    filtered1 = df1[df1['eNodeB Name'].isin(site_list)].sort_values(by=['Cell Name'])
    filtered2 = df2[df2['eNodeB Name'].isin(site_list)].sort_values(by=['Cell Name'])

    filtered1.set_index('Cell Name', inplace=True)
    filtered2.set_index('Cell Name', inplace=True)


    print(filtered2)
    print("the whole network dump is filtered & sorted...")

    info1 = filtered1[list3]
    info2 = filtered2[list3]

    tf_sum1 = filtered1[list2]
    tf_sum2 = filtered2[list2]

    result = (tf_sum2 - tf_sum1) * 100 / tf_sum1
    result.replace([np.inf, -np.inf], 999, inplace=True)

    print("Calculation done...")
    final= pd.concat([info2,result],axis=1)


    final.dropna(how='all', inplace=True)
    final.fillna(8888, inplace=True)

    final.to_excel(ultimate, sheet_name='raw')

    # final.to_csv('4g\\4G Raw report.csv')
    print("4G Raw data is inserted to excel-->>")
    df_f = final

    print("applying the threshold values...")

    df_f['Cell Availablility (%)'] = np.where(df_f['Cell Availablility (%)'] != 100, 'Cell is Down',
                                              df_f['Cell Availablility (%)'])

    df_f['RRC Setup SR %(%)'] = np.where((df_f['RRC Setup SR %(%)'] < -rrc), 'Performance degraded',
                                         np.where((df_f['RRC Setup SR %(%)'] == 8888), 'zero(no change)',
                                                  df_f['RRC Setup SR %(%)']))

    df_f['eRAB Setup SR(%)'] = np.where((df_f['eRAB Setup SR(%)'] < -erab), 'Performance degraded',
                                        np.where((df_f['eRAB Setup SR(%)'] == 8888), 'zero(no change)',
                                                 df_f['eRAB Setup SR(%)']))

    df_f['Average User Number (per cell)'] = np.where((df_f['Average User Number (per cell)'] < -aun),
                                                      'Performance degraded',
                                                      np.where((df_f['Average User Number (per cell)'] == 8888),
                                                               'zero(no change)',
                                                               df_f['Average User Number (per cell)']))

    df_f['DL Data Volume (MB)(MB)'] = np.where((df_f['DL Data Volume (MB)(MB)'] < -data_vol), 'Performance degraded',
                                               np.where((df_f['DL Data Volume (MB)(MB)'] == 8888), 'zero(no change)',
                                                        df_f['DL Data Volume (MB)(MB)']))

    df_f['DL Avg User Throughput (kbps)'] = np.where((df_f['DL Avg User Throughput (kbps)'] < -user_tp),
                                                     'Performance degraded',
                                                     np.where((df_f['DL Avg User Throughput (kbps)'] == 8888),
                                                              'zero(no change)', df_f['DL Avg User Throughput (kbps)']))

    # df_f.to_csv('4g\\4G Mid-level report.csv')
    # print("4G Mid-level report.csv is created-->>")

    # tab = []
    # unavail=[]
    # cell_list = list(df_f['Cell Name'])
    # for i in cell_list:
    #
    #     a = df_f.loc[df_f['Cell Name'] == i]
    #     if a.empty==False:
    #
    #
    #         a_info = a[list4]
    #
    #         b = a[(a.iloc[:, 4:] == 'zero(no change)') | (a.iloc[:, 4:] == 'Extra TRX') | (
    #                     a.iloc[:, 4:] == 'Performance degraded')
    #               | (a.iloc[:, 4:] == 'TRX Down') | (a.iloc[:, 4:] == 'TRX Added') | (a.iloc[:, 4:] == 'TRX Deleted') |
    #               (a.iloc[:, 4:] == 'Cell is Down') | (a.iloc[:, 4:] == 'Performance degraded(pre-value= 0)')]
    #
    #         b.dropna(axis=1, inplace=True)
    #
    #         d = pd.concat([a_info, b], axis=1)
    #         d.set_index('Cell Name', inplace=True)
    #         e = d.transpose()
    #         table = tb(e, headers='keys', tablefmt='psql')
    #         tab.append(table)
    #         tab.append('\n\n')
    #     else:
    #         unavail.append(i)
    #         unavail.append('\n')
    # print(unavail)
    #
    # with open('4g\\Unavailable.txt', 'w') as f:
    #     f.writelines(unavail)
    #
    #
    # with open('4g\\4G Final report.txt', 'w') as f:
    #     f.writelines(tab)

    df_ff = df_f[(df_f.iloc[:, 4:] == 'zero(no change)') | (df_f.iloc[:, 4:] == 'Extra TRX') | (
                df_f.iloc[:, 4:] == 'Performance degraded')
                 | (df_f.iloc[:, 4:] == 'TRX Down') | (df_f.iloc[:, 4:] == 'TRX Added') | (
                             df_f.iloc[:, 4:] == 'TRX Deleted') |
                 (df_f.iloc[:, 4:] == 'Cell is Down') | (df_f.iloc[:, 4:] == 'Performance degraded(pre-value= 0)')]

    # print(df_ff)

    df_info = df_f[list4]
    df_ff.fillna(' ', inplace=True)
    df_half = df_ff[list5]

    g= pd.concat([df_info, df_half],axis=1)
    # g.set_index('Cell Name', inplace=True)

    # j=0
    # for i in list5:
    #     ultra_filt = g[g[i].isin(list7)]
    #     ultra_filt[i].to_excel(ultimate, sheet_name=list8[j])
    #     j+=1

    # g.to_csv('4g\\4G Final report.csv')
    rounded_res = result.round(decimals=2)

    res_ext = filtered2['Cell Availablility (%)'].to_frame()

    fin_res = pd.concat([res_ext, rounded_res], axis=1)


    x = df_half.astype(str) + " <" + fin_res.astype(str) + ">"

    h = pd.concat([df_info, x], axis=1)

    # h.set_index('Cell Name', inplace=True)
    h = h[list6]

    j=0
    for i in list5:
        ultra_filt = h[h[i].str.contains('[A-Za-z]+',na=False, regex=True)]
        # ultra_filt.fillna(' ', inplace=True)
        ultra_filt[i].to_excel(ultimate, sheet_name=list8[j])
        j+=1


    # h.to_csv("4g\\4G ultra.csv")
    h.to_excel(ultimate, sheet_name='ultra')
    ultimate.save()
    print("4G Final data is inserted-->>")


if type == '2g':
    two()
elif type =='3g':
    three()
else:
    lte()

input("Press ENTER to exit the application")
#!/usr/bin/python
# -*-coding:utf-8 -*-
import smtplib
import MySQLdb
import datetime
import types
from email.mime.text import MIMEText
from email.header import Header
class query:
    def __init__(self,dbHost,dbUser,dbPasswd,dbDatabase,dbSql):
        self.dbHost = dbHost
        self.dbUser = dbUser
        self.dbPasswd = dbPasswd
        self.dbDatabase = dbDatabase
        self.dbSql = dbSql
    def queryDb(self):
        try:
            db = MySQLdb.connect(self.dbHost,self.dbUser,self.dbPasswd,self.dbDatabase,charset='utf8')
            cursor = db.cursor()
            cursor.execute(self.dbSql)
            results = cursor.fetchall()
            cursor.close()
            return results
        except:
            return "Error: unable to fecth data"
    def queryDbResults(self):
        try:
            db = MySQLdb.connect(self.dbHost,self.dbUser,self.dbPasswd,self.dbDatabase,charset='utf8')
            cursor = db.cursor()
            cursor.execute(self.dbSql)
            results = cursor.fetchall()
            for row in results:
                results = row[0]
            cursor.close()
            return str(results)
        except:
            return "Error: unable to fecth data"
class html:
    def __init__(self,th):
        self.th = th
    def htmlPageCore(self,results,key):
        td =''
        for row in results:
            td = td +'<td bgcolor="#F79646">' + key + '</td><td>'+ str(row[0]) +'</td>'
        htmlCore = td
        return htmlCore
    def htmlPageRowspan(self,results):
        td =''
        for row in results:
            td = td +'<td rowspan=2>'+ str(row[0]) +'</td>'
        htmlRowspan = td
        return htmlRowspan
    def htmlPageRate(self,results,newRegRate,oldRegRate):
        td = ''
        j = 0
        for row in results:
            j = j + 1
            for i in range (len(row)):
                if type(row[i]) is types.LongType or type(row[i]) is types.FloatType:
                    if i == 0:
                        td = td + '<tr><td>' + str(row[i]) + '</td>'
                    elif i == len(row) - 1:
                        td = td + '<td>' + str(row[i]) + '</td></tr>'
                    elif i == 7:
                        if j == 1:
                            td = td + newRegRate
                        elif j == 3:
                            td = td + oldRegRate
                        else:
                            td = td +''
                    else :
                        td = td + '<td>' + str(row[i]) + '</td>'
                else:
                    if i == 0:
                        td = td + '<tr><td>' + row[i] + '</td>'
                    elif i == len(row) - 1:
                        td = td + '<td>' + row[i] + '</td></tr>'
                    else:
                        td = td + '<td>' + row[i] + '</td>'
        td = td.encode('utf8')
        tail='</table>'
        htmlPageRate = self.th + td + tail
        return htmlPageRate
    def htmlPage(self,results):
        td = ''
        for row in results:
            for i in range (len(row)):
                if type(row[i]) is types.LongType or type(row[i]) is types.FloatType:
                    if i == 0:
                        td = td + '<tr><td>' + str(row[i]) + '</td>'
                    elif i == len(row) - 1:
                        td = td + '<td>' + str(row[i]) + '</td></tr>'
                    else :
                        td = td + '<td>' + str(row[i]) + '</td>'
                else:
                    if i == 0:
                        td = td + '<tr><td>' + row[i] + '</td>'
                    elif i == len(row) - 1:
                        td = td + '<td>' + row[i] + '</td></tr>'
                    else:
                        td = td + '<td>' + row[i] + '</td>'
        td = td.encode('utf8')
        tail='</table>'
        htmlPage = self.th + td + tail
        return htmlPage
    def htmlPageRow(self,results,key):
        td =''
        for row in results:
            for i in range (len(row)) :
                if key[i] == 'AP异常下线量':
                    td = td + '<tr><td>' + key[i] + '</td><td>' + str(row[i]) + '（因网关：'+apOffline.queryDbResults()+'）</td><tr>'
                elif key[i] =='AP恢复上线量':
                    td = td + '<tr><td>' + key[i] + '</td><td>' + str(row[i]) + '（因网关：'+apOnline.queryDbResults()+'）</td><tr>'
                elif key[i] =='网关总量':
                    td = td + '<tr><td>' + key[i] + '</td><td>' + str(row[i]) + '（未激活：'+unableSn.queryDbResults()+'）</td><tr>'
                else:
                    td = td + '<tr><td>' + key[i] + '</td><td>' + str(row[i]) + '</td><tr>'
        tail='</table>'
        htmlPageRow = self.th + td + tail
        return htmlPageRow
def sendEmail(sender,passwd,host,port,receivers,date,mail) :
    message = MIMEText(mail, 'html', 'utf-8')
    message['From'] = Header("数据业务部<"+sender+">", 'utf-8')
    subject = str(date) + ' Daily Report'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(host,port)
        smtpObj.ehlo()
        smtpObj.login(sender,passwd)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
if __name__ == '__main__' :
    sender = 'liucl@helianhealth.com'
    passwd = 'L'
    host = 'smtp.exmail.qq.com'
    port = 465
    receivers = ['shenjin@helianhealth.com','zhengcong@helianhealth.com','laide@helianhealth.com','songyw@helianhealth.com','liucl@helianhealth.com','lailei@helianhealth.com'\
                 ,'songjt@helianhealth.com','liuhuan@helianwifi.com','lizg@helianhealth.com','zhangkuan@helianhealth.com','wuqiong@helianwifi.com','yangjz@helianwifi.com','chengxc@helianhealth.com'\
                 ,'zhangyy@helianhealth.com','yeap@helianwifi.com','lvzl@helianwifi.com','sy@helianwifi.com','js@helianhealth.com','hc@helianwifi.com','yc@helianwifi.com']
    yesterday = (datetime.date.today() - datetime.timedelta(days=1) ). strftime('%Y%m%d')
    dbHost = 'rm-bp1067f3o504q78v3o.mysql.rds.aliyuncs.com'
    dbUser = 'rfpn8e67h2'
    dbPasswd = 'Hl0301wf'
    dbDatabase = 'helian_statistic'
    sqlFeedback='select feedback_date,station_id,station_name,ifnull(level,\'\'),type,content,status,days ' \
                    'from dwd_user_common_type_feedback_d where ds='+yesterday+' and days<=7 and status=\'未解决\' order by days,station_id;'
    sqlCoreUnsolved = 'select count(1) from dwd_user_common_type_feedback_d where ds='+yesterday+' and status=\'未解决\';'
    sqlCoreSchemed = 'select count(1) from dwd_user_common_type_feedback_d where ds='+yesterday+' and status=\'已有解决方案\';'
    sqlCoreNewFeedback = 'select discontent_num from hpif_user_common_discontent_feedback_d where ds='+yesterday+';'
    sqlCoreSolved = 'select solve_num from hpif_user_common_feedback_solve_d where ds='+yesterday+';'
    htmlHeader = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' \
                 '<center><font size="6">Daily Report</font></center>' \
                 '<center><font size="4">(' + str(yesterday) + ')</center></head><br /><body>'
    htmlTail = '<br /><center><font size="6">--------End--------<font></center></body></html>'
    unsolved = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreUnsolved)
    schemed = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreSchemed)
    htmlThFeedback = '<br/><div><font size="5">' + '用户问题反馈（未解决：'+unsolved.queryDbResults()+'，已有方案：'+schemed.queryDbResults()+'）:</font>' \
             '<br/>（以下问题显示最近7天）</div>' \
             '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="90%">' \
             '<tr bgcolor="#F79646" align="left" >' \
             '<th>反馈日期</th>' \
             '<th>医院编码</th>' \
             '<th>医院名称</th>' \
             '<th>医院等级</th>' \
             '<th>反馈类型</th>' \
             '<th>反馈内容</th>' \
             '<th>问题状态</th>' \
             '<th>已过天数</th>' \
             '</tr>'
    sqlUserApp = 'select ds,type,is_reg,open_user,wifi_user,concat(round(wifi_rate*100,2),\'%\'),reg_user,reg_rate,portal_user,concat(round(portal_rate*100,2),\'%\')' \
                 ' from hpif_user_online_experience_d where ds='+yesterday+' order by type,is_reg;'
    sqlNewUserRegRate = 'select concat(round(sum(case when is_reg=\'是\' then open_user else 0 end)/sum(open_user)*100,2),\'%\')' \
                     ' from hpif_user_online_experience_d where ds='+yesterday+' and type=\'新用户\';'
    sqlOldUserRegRate = 'select concat(round(sum(case when is_reg=\'是\' then open_user else 0 end)/sum(open_user)*100,2),\'%\')' \
                     ' from hpif_user_online_experience_d where ds='+yesterday+' and type=\'老用户\';'
    sqlUserdau = 'select sum(open_user) from hpif_user_online_experience_d where ds='+yesterday+';'
    sqlUserInDau = 'select in_uv from hpif_user_in_out_active_d where ds='+yesterday+';'
    sqlUserOutDau = 'select out_uv from hpif_user_in_out_active_d where ds='+yesterday+';'
    sqlUserDauReg = 'select sum(reg_user) from hpif_user_online_experience_d where ds='+yesterday+';'
    sqlUserReg = 'select user_reg from hpif_reg_user_d where ds='+yesterday+';'
    userDau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUserdau)
    userInDau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUserInDau)
    userOutDau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUserOutDau)
    userDauReg = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUserDauReg)
    userReg = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUserReg)
    userNewRegRate = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlNewUserRegRate)
    userOldRegRate = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlOldUserRegRate)
    htmlThUserApp = '<br/><div><font size="5">' + '健康APP相关（DAU：'+ userDau.queryDbResults() +'，院内DAU：' + userInDau.queryDbResults()+'，院外DAU：' \
             + userOutDau.queryDbResults()+'，活跃注册量：'+userDauReg.queryDbResults()+'，当日注册量：' \
             + userReg.queryDbResults()+'）：</font></div>' \
             '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="90%">' \
             '<tr bgcolor="#F79646" align="left" >' \
             '<th>日期</th>' \
             '<th>用户类型</th>' \
             '<th>是否注册</th>' \
             '<th>APP打开量</th>' \
             '<th>蹭网成功量</th>' \
             '<th>蹭网成功率</th>' \
             '<th>注册量</th>' \
             '<th>注册率</th>' \
             '<th>PORTAL成功量</th>' \
             '<th>PORTAL成功率</th>' \
             '</tr>'
    sqlDocApp = 'select ds,type,is_reg,open_user,wifi_user,concat(round(wifi_rate*100,2),\'%\'),reg_user,reg_rate,auth_user,concat(round(auth_rate*100,2),\'%\'),portal_user,concat(round(portal_rate*100,2),\'%\')' \
                 ' from hpif_doc_online_experience_d where ds='+yesterday+' order by type,is_reg;'
    sqlDocdau = 'select sum(open_user) from hpif_doc_online_experience_d where ds='+yesterday+';'
    sqlDocInDau = 'select in_uv from hpif_doc_in_out_active_d where ds='+yesterday+';'
    sqlDocOutDau = 'select out_uv from hpif_doc_in_out_active_d where ds='+yesterday+';'
    sqlDocDauReg = 'select sum(reg_user) from hpif_doc_online_experience_d where ds='+yesterday+';'
    sqlDocDauAuth = 'select sum(auth_user) from hpif_doc_online_experience_d where ds='+yesterday+';'
    sqlDocReg = 'select doc_reg from hpif_reg_user_d where ds='+yesterday+';'
    sqlDocAuth = 'select doc_auth from hpif_reg_user_d where ds='+yesterday+';'
    sqlNewDocRegRate = 'select concat(round(sum(case when is_reg=\'是\' then open_user else 0 end)/sum(open_user)*100,2),\'%\')' \
                     ' from hpif_doc_online_experience_d where ds='+yesterday+' and type=\'新用户\';'
    sqlOldDocRegRate = 'select concat(round(sum(case when is_reg=\'是\' then open_user else 0 end)/sum(open_user)*100,2),\'%\')' \
                     ' from hpif_doc_online_experience_d where ds='+yesterday+' and type=\'老用户\';'
    docDau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocdau)
    docInDau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocInDau)
    docOutDau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocOutDau)
    docDauReg = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocDauReg)
    docDauAuth = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocDauAuth)
    docReg = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocReg)
    docAuth = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocAuth)
    docNewRegRate = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlNewDocRegRate)
    docOldRegRate = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlOldDocRegRate)
    htmlThDocApp = '<br /><div><font size="5">' + '医护APP相关（DAU：'+docDau.queryDbResults()+'，院内DAU：' + docInDau.queryDbResults()+'，院外DAU：' \
             + docOutDau.queryDbResults()+'，活跃注册量：'+docDauReg.queryDbResults()+'，活跃认证量：'+docDauAuth.queryDbResults()+ \
             '，当日注册量：'+docReg.queryDbResults()+'，当日认证量：'+docAuth.queryDbResults()+'）:</font></div>' \
             '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="90%">' \
             '<tr bgcolor="#F79646" align="left" >' \
             '<th>日期</th>' \
             '<th>用户类型</th>' \
             '<th>是否注册</th>' \
             '<th>APP打开量</th>' \
             '<th>蹭网成功量</th>' \
             '<th>蹭网成功率</th>' \
             '<th>注册量</th>' \
             '<th>注册率</th>' \
             '<th>认证量</th>' \
             '<th>认证率</th>' \
             '<th>PORTAL成功量</th>' \
             '<th>PORTAL成功率</th>' \
             '</tr>'
    sqlAp = 'select new,total,exception,recover,online,concat(round(on_rate*100,2),\'%\'),total-lower,concat(round((1-lower_rate)*100,2),\'%\')' \
            '  from dw_ap_report_d where ds='+yesterday+';'
    sqlApOffline = 'select outsn_apnum from dw_ap_report_d where ds='+yesterday+';'
    sqlApOnline = 'select sn_apnum from dw_ap_report_d where ds='+yesterday+';'
    apOffline = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlApOffline)
    apOnline = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlApOnline)
    htmlThAp = '<br/><div><font size="5">' + 'AP相关:</font></div>' \
             '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="40%">' \
             '<tr bgcolor="#F79646" align="left">' \
             '<th width="60%">指标</th>' \
             '<th>数值</th>' \
             '</tr>'
    apKey = ['新增AP量','AP总量','AP异常下线量','AP恢复上线量','AP在线量','AP在线率','有效AP量（AP≥10）','有效AP率（AP≥10）']
    sqlSn = 'select newsn,gateway_num,gateway_exception_outline,gateway_recover_online,gateway_online_num,concat(round(rate*100,2),\'%\'),newget,upget,notnull,total' \
            ' from dw_gateway_report_d where ds='+yesterday+';'
    sqlUnableSn = 'select unable_snnum from dw_gateway_report_d where ds='+yesterday+';'
    unableSn = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUnableSn)
    snKey = ['新增网关量','网关总量','较昨日网关异常下线量','较昨日网关恢复上线量','网关在线量','网关在线率','网关版本新增量','网关版本更新量','网关版本覆盖量','网关版本量']
    htmlThSn = '<br/><div><font size="5">' + '网关相关:</font></div>' \
             '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="40%">' \
             '<tr bgcolor="#F79646" align="left" >' \
             '<th width="60%">指标</th>' \
             '<th>数值</th>' \
             '</tr>'
    sqlZabbix = 'select lastchange,station_id,station_name,ifnull(station_level,\'\'),information,description,status,days' \
                ' from dw_zabbix_issue_alert_d  where ds='+yesterday+' and information in (\'严重\',\'灾难\') and days<=7 order by days,station_id;'
    sqlZabbixNum = 'select count(1) from dw_zabbix_issue_alert_d where ds='+yesterday+' and information in (\'严重\',\'灾难\') ;'
    zabbixNum = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlZabbixNum)
    htmlThZabbix = '<br/><div><font size="5">' + 'zabbix报警（未解决：'+zabbixNum.queryDbResults()+'）:</font>' \
             '<br/>（以下告警显示最近7天）</div>' \
             '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="90%">' \
             '<tr bgcolor="#F79646" align="left" >' \
             '<th>告警日期</th>' \
             '<th>医院编码</th>' \
             '<th>医院名称</th>' \
             '<th>医院等级</th>' \
             '<th>告警类型</th>' \
             '<th>告警内容</th>' \
             '<th>告警状态</th>' \
             '<th>已过天数</th>' \
             '</tr>'
    htmlThCore ='<br/><div><font size="5">' + '核心指标:</font></div>' \
                '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="40%">'
    htmlThRisk = '<br/><div><font size="5">' + '风险评估:</font></div>' \
             '<br/><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="40%">' \
             '<tr bgcolor="#F79646" align="left" >' \
             '<th>网关下线量</th>' \
             '<th>影响DAU</th>' \
             '</tr>'
    sqlCoreAp = 'select total from dw_ap_report_d where ds='+yesterday+';'
    sqlCoreNewstation = 'select newstation_id from hpif_station_remove_bandwidth_d where ds='+yesterday+';'
    sqlCoreUpperApRate = 'select concat(round((1-lower_rate)*100,2),\'%\') from dw_ap_report_d where ds='+yesterday+';'
    sqlCoreFreeboard = 'select freeboard from hpif_station_remove_bandwidth_d where ds='+yesterday+';'
    sqlCoreDevice = 'select concat(round((sum(on_rate)+sum(rate))/2*100,2),\'%\')' \
                    ' from (select on_rate,0 rate  from dw_ap_report_d where ds='+yesterday+\
                    ' union all select 0 on_rate,rate from dw_gateway_report_d where ds='+yesterday+') t;'
    sqlCoreSn = 'select gateway_num from dw_gateway_report_d where ds='+yesterday+';'
    sqlCoreWifi = 'select wifi_connect from hpif_user_flow_d where ds='+yesterday+';'
    sqlRiskSn = 'select outline_snnum,lost_uv from dw_gateway_report_d where ds='+yesterday+';'
    keyCoreAp ='AP总量'
    keyCoreNewStation = '新增医院（2017）'
    keyCoreFreeboard ='去宽带医院（2017）'
    keyCoreUpperApRate ='有效AP率（AP≥10）'
    keyCoreUserdau = '健康APP DAU'
    keyCoreDocdau = '医护APP DAU'
    keyCoreUnsolved = '未解决问题'
    keyCoreSchemed = '已有方案问题'
    keyCoreNewFeedback = '昨日新增问题'
    keyCoreSolved = '昨日已解决问题'
    keyCoreDevice = '设备在线率'
    keyCoreSn = '网关总量'
    keyCoreWifi = 'WiFi用户'
    feedback = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlFeedback)
    userApp = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUserApp)
    docApp = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocApp)
    ap = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlAp)
    sn = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlSn)
    zabbix = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlZabbix)
    coreAp = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreAp)
    coreNewStation = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreNewstation)
    coreUpperApRate = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreUpperApRate)
    coreFreeboard = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreFreeboard)
    coreUserdau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlUserdau)
    coreDocdau = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlDocdau)
    coreUnsolved = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreUnsolved)
    coreSchemed = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreSchemed)
    coreNewFeedback = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreNewFeedback)
    coreSolved = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreSolved)
    coreDevice = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreDevice)
    coreSn = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreSn)
    coreWifi = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlCoreWifi)
    riskSn = query(dbHost,dbUser,dbPasswd,dbDatabase,sqlRiskSn)
    core = html(htmlThCore)
    risk = html(htmlThRisk)
    htmlFeedback = html(htmlThFeedback)
    htmlUserApp = html(htmlThUserApp)
    htmlDocApp = html(htmlThDocApp)
    htmlAp = html(htmlThAp)
    htmlSn = html(htmlThSn)
    htmlZabbix = html(htmlThZabbix)
    mailNewUserRegRate = core.htmlPageRowspan(userNewRegRate.queryDb())
    mailOldUserRegRate = core.htmlPageRowspan(userOldRegRate.queryDb())
    mailNewDocRegRate = core.htmlPageRowspan(docNewRegRate.queryDb())
    mailOldDocRegRate = core.htmlPageRowspan(docOldRegRate.queryDb())
    mailFeedback = htmlFeedback.htmlPage(feedback.queryDb())
    mailZabbix = htmlZabbix.htmlPage(zabbix.queryDb())
    mailUserApp = htmlUserApp.htmlPageRate(userApp.queryDb(),mailNewUserRegRate,mailOldUserRegRate)
    mailDocApp = htmlDocApp.htmlPageRate(docApp.queryDb(),mailNewDocRegRate,mailOldDocRegRate)
    mailAp = htmlAp.htmlPageRow(ap.queryDb(),apKey)
    mailSn = htmlSn.htmlPageRow(sn.queryDb(),snKey)
    mailCoreAp = core.htmlPageCore(coreAp.queryDb(),keyCoreAp)
    mailCoreNewStation = core.htmlPageCore(coreNewStation.queryDb(),keyCoreNewStation)
    mailCoreUpperAp = core.htmlPageCore(coreUpperApRate.queryDb(),keyCoreUpperApRate)
    mailCoreFreeboard = core.htmlPageCore(coreFreeboard.queryDb(),keyCoreFreeboard)
    mailCoreUserdau = core.htmlPageCore(coreUserdau.queryDb(),keyCoreUserdau)
    mailCoreDocdau = core.htmlPageCore(coreDocdau.queryDb(),keyCoreDocdau)
    mailCoreUnsolved = core.htmlPageCore(coreUnsolved.queryDb(),keyCoreUnsolved)
    mailCoreSchemed = core.htmlPageCore(coreSchemed.queryDb(),keyCoreSchemed)
    mailCoreNewFeedback = core.htmlPageCore(coreNewFeedback.queryDb(),keyCoreNewFeedback)
    mailCoreSolved = core.htmlPageCore(coreSolved.queryDb(),keyCoreSolved)
    mailCoreDevice = core.htmlPageCore(coreDevice.queryDb(),keyCoreDevice)
    mailCoreSn = core.htmlPageCore(coreSn.queryDb(),keyCoreSn)
    mailCoreWifi = core.htmlPageCore(coreWifi.queryDb(),keyCoreWifi)
    mailRiskSn = risk.htmlPage(riskSn.queryDb())
    mail = htmlHeader + htmlThCore + \
          '<tr>' + mailCoreSn + mailCoreNewStation +'</tr><tr>'+ mailCoreAp + mailCoreFreeboard+ '</tr>'\
          '<tr>' + mailCoreUpperAp + mailCoreDevice + '</tr><tr>' +mailCoreUserdau + mailCoreDocdau +'</tr>'\
          '<tr>' + mailCoreUnsolved +mailCoreSchemed+'</tr><tr>'+ mailCoreNewFeedback + mailCoreSolved +'</tr>' \
          '<tr>' + mailCoreWifi + '</tr></table>' \
           + mailRiskSn + mailAp + mailSn + mailUserApp + mailDocApp + mailFeedback + mailZabbix + htmlTail
    #print mail
    sendEmail(sender,passwd,host,port,receivers,yesterday,mail)

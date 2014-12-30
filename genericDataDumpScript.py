from bs4 import BeautifulSoup
import numpy as np
import urllib2
import time
import httplib
import traceback
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
import requests

elite_dump = open("elite_dump","w")
normal_dump = open("normal_dump","w")
elite_drop = open("elite_drop","w")
normal_drop = open("normal_drop","w")
corporate_drop = open("corporate_drop","w")
corporate_dump = open("corporate_dump","w")

initialUrl = "http://www.timingindia.com/beta/includes/details.php?encode=no&bib="
midUrl = "&tble="
tableName = "timing_r1312_delhm_open#head"

for bibNumber in range(1,52599):
    try:
        url = initialUrl+str(bibNumber)+midUrl+tableName
        html = requests.get(url,timeout = 5).text
        data=BeautifulSoup(html)
        headerCategory = str(data.find('h3').text.strip()).split('~')[1].split()[0] #"Elite","Open","DHL" 
        table_content = data.find('table',class_="table table-curved tborder")
        rows = table_content.find_all('tr')
        values = [td.text.strip() for row in rows for td in row.find_all('td')]
        isDrop = False
        time_speed = ""
        bib = "";name = "";gender = "";cat="";rank="0";totalFinishers="0";catRank="0";totalCatFinishers="0";genderRank="0";totalGenderFinishers="0"
        netTime="0";netSpeed="0"

        for idx in range(0,len(values),2):
            next_val = values[idx+1]
            if(values[idx] == "Bib Number"):
                bib = next_val
            elif(values[idx] == "Name"):
                name = next_val
            elif(values[idx] == "Gender"):
                gender = next_val
            elif(values[idx] == "Category"):
                cat = next_val
            elif(values[idx] == "Rank"):
                rank = next_val.replace('/',' ').split()[0]
                totalFinishers = next_val.replace('/',' ').split()[1]
            elif(values[idx] == "Category Rank" or values[idx] == "Team Rank"):
                catRank = next_val.replace('/',' ').split()[0]
                totalCatFinishers = next_val.replace('/',' ').split()[1]
            elif(values[idx] == "Gender Rank"):
                genderRank = next_val.replace('/',' ').split()[0]
                totalGenderFinishers = next_val.replace('/',' ').split()[1]
            elif(values[idx].startswith("Split@")):
                value = next_val.replace('/',' ').replace(',',' ').split()
                if(len(value) >= 10):
                    time_speed += value[0] + "\t" + value[6] + "\t"
                else: #It's a drop case
                    isDrop = True
            elif(values[idx] == "Net Time" or  values[idx] == "Gross Time"):
                if(netTime == "0" and len(next_val.replace(',',' ').split()) >= 6):
                    netTime = next_val.replace(',',' ').split()[0]
                    netSpeed = next_val.replace(',',' ').split()[6]
            else:
                continue

        isCorporate = False; isElite = False; isOpen = False
        
        if(headerCategory == "Elite"):
            cat = "ELITE"
            isElite = True
        elif(headerCategory != "Open" and headerCategory != "HALF"): 
            cat = "CORPORATE"
            isCorporate = True
        else:
            isOpen = True

        if(isDrop):
            if(isCorporate):
                corporate_drop.write(values[5]+"\t"+bib+"\t" + name+"\t"+gender+"\t"+cat+"\t"+rank+"\t"+totalFinishers + "\n")
            elif(isElite):
                elite_drop.write(bib+"\t" + name+"\t"+gender+"\t"+cat+"\t"+rank+"\t"+totalFinishers + "\n")
            else:
                normal_drop.write(bib+"\t"+name+"\t"+gender+"\t"+cat+"\t"+rank+"\t"+totalFinishers+"\t"+catRank+"\t"+totalCatFinishers+"\t"+genderRank+"\t"+totalGenderFinishers + "\n")
        else:
            if(isCorporate):
                corporate_dump.write(values[5]+"\t"+bib+"\t"+name+"\t"+gender+"\t"+cat+"\t"+rank+"\t"+totalFinishers+"\t"+catRank+"\t"+totalCatFinishers+"\t"+genderRank+"\t"+totalGenderFinishers+"\t"+ time_speed + netTime+"\t"+netSpeed + "\n")
            elif(isElite):
                elite_dump.write(bib+"\t"+name+"\t"+gender+"\t"+cat+"\t"+rank+"\t"+totalFinishers+"\t"+catRank+"\t"+totalCatFinishers+"\t"+genderRank+"\t"+totalGenderFinishers+"\t"+time_speed + netTime+"\t"+netSpeed + "\n")
            else:
                normal_dump.write(bib+"\t"+name+"\t"+gender+"\t"+cat+"\t"+rank+"\t"+totalFinishers+"\t"+catRank+"\t"+totalCatFinishers+"\t"+genderRank+"\t"+totalGenderFinishers+"\t"+time_speed + netTime+"\t"+netSpeed + "\n")
        time.sleep(1)
    except urllib2.HTTPError, e:
        print 'ERROR:HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        print 'ERROR:URLError = ' + str(e.reason)
    except httplib.HTTPException, e:
        print 'ERROR:HTTPException'
    except requests.exceptions.RequestException as e:    # This is the correct synta
        print e
    except Exception:
        print 'ERROR:generic exception: ' + traceback.format_exc()
    except (UnicodeDecodeError,UnicodeEncodeError), e:
         print 'Encoding.Decoding Error:' + str(e.reason) + str(e.message)
    except urllib2.HTTPError, e:
        print 'ERROR:HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        print 'ERROR:URLError = ' + str(e.reason)
    except httplib.HTTPException, e:
        print 'ERROR:HTTPException'
    except Exception:
        print 'ERROR:generic exception: ' + traceback.format_exc()
    except requests.exceptions.RequestException as e:    # This is the correct syntax
        print e
    finally:
        print url
        pass

normal_dump.close()
elite_dump.close()
normal_drop.close()
elite_drop.close()
corporate_dump.close()
corporate_drop.close()

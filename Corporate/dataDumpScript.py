from bs4 import BeautifulSoup
import urllib2
import httplib
import traceback
import sys
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
tableName = "results_2013_adhm13open#head"

for bibNumber in range(19000,19200):
    try:
        url = initialUrl+str(bibNumber)+midUrl+tableName
        html = requests.get(url,timeout = 5).text
        data=BeautifulSoup(html)
        table_content = data.find('table',class_="table table-curved tborder")
        rows = table_content.find_all('tr')
        values = [td.text.strip() for row in rows for td in row.find_all('td')]

        indexBin = 1
        indexName = 3
        indexGender = 5
        indexCategory = 7
        indexRank = 9
        indexCategoryRank = 11
        indexGenderRank = 13
        indexSplitStart = 15

        indexSplitTime = 0
        indexSplitSpeed = 6
        indexSplitGenderRank = 10
        indexSplitCategoryRank = 16

        isCorporate = False

        bib = values[indexBin]
        name = values[indexName]
        gender = values[indexGender]
        if(values[6] != "Category"):
            cat = "CORPORATE"
            indexRank = 7
            indexGenderRank = 9
            indexCategoryRank = -1
            indexSplitStart = 11
            isCorporate = True
            indexSplitCategoryRank = 10
        else:
            cat = values[indexCategory]


        rank = values[indexRank].replace('/',' ').split()[0]
        totalFinishers = values[indexRank].replace('/',' ').split()[1]
       
        if(indexCategoryRank > 0):
            catRank = values[indexCategoryRank].replace('/',' ').split()[0]
            totalCatFinishers = values[indexCategoryRank].replace('/',' ').split()[1]
        else:
            catRank = "0"
            totalCatFinishers = "0"
        
        genderRank = values[indexGenderRank].replace('/',' ').split()[0]
        totalGenderFinishers = values[indexGenderRank].replace('/',' ').split()[1]


        if(rank == "0" and not isCorporate):
            indexSplitCategoryRank = 15

        if(str(cat).find("ELITE") < 0 and str(cat).find("CORPORATE") < 0):
            value = values[indexSplitStart].replace('/',' ').replace(',',' ').split() 
            if(len(value) >= indexSplitCategoryRank):
                _5kmTime = value[indexSplitTime]
                _5kmSpeed = value[indexSplitSpeed]
                _5kmGenderRank = value[indexSplitGenderRank]
                _5kmCatRank = value[indexSplitCategoryRank]
            else:
                normal_drop.write(bib + "\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + catRank + "\t" + totalCatFinishers + "\t" +genderRank + "\t" +totalGenderFinishers + "\n") 
                continue

            value = values[indexSplitStart+2].replace('/',' ').replace(',',' ').split()
            if(len(value) >= indexSplitCategoryRank):
                _10kmTime = value[indexSplitTime]
                _10kmSpeed = value[indexSplitSpeed]
                _10kmGenderRank = value[indexSplitGenderRank]
                _10kmCatRank = value[indexSplitCategoryRank]
            else:
                normal_drop.write(bib + "\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + catRank + "\t" + totalCatFinishers + "\t" +genderRank + "\t" +totalGenderFinishers + "\t" + _5kmTime + "\t" + _5kmSpeed + "\t" + _5kmGenderRank  + "\t" + _5kmCatRank + "\n") 
                continue

            value = values[indexSplitStart+4].replace('/',' ').replace(',',' ').split()
            if(len(value) >= indexSplitCategoryRank):
                _15kmTime = value[indexSplitTime]
                _15kmSpeed = value[indexSplitSpeed]
                _15kmGenderRank = value[indexSplitGenderRank]
                _15kmCatRank = value[indexSplitCategoryRank]
            else:
                normal_drop.write(bib + "\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + catRank + "\t" + totalCatFinishers + "\t" +genderRank + "\t" +totalGenderFinishers + "\t" + _5kmTime + "\t" + _5kmSpeed + "\t" + _5kmGenderRank  + "\t" + _5kmCatRank  + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _10kmGenderRank  + "\t" + _10kmCatRank + "\n")
                continue

            netTime = values[indexSplitStart+6].replace(',',' ').split()[0]
            netSpeed = values[indexSplitStart+6].replace(',',' ').split()[6]

            normal_dump.write(bib + "\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + catRank + "\t" + totalCatFinishers + "\t" +genderRank + "\t" +totalGenderFinishers + "\t" + _5kmTime + "\t" + _5kmSpeed + "\t" + _5kmGenderRank  + "\t" + _5kmCatRank  + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _10kmGenderRank  + "\t" + _10kmCatRank + "\t" + _15kmTime + "\t" + _15kmSpeed + "\t" + _15kmGenderRank + "\t" + _15kmCatRank + "\t" + netTime + "\t" + netSpeed + "\n")
        else:
            value = values[indexSplitStart].replace('/',' ').replace(',',' ').split()
            if(len(value) >= indexSplitCategoryRank):
                _7kmTime = value[indexSplitTime]
                _7kmSpeed = value[indexSplitSpeed]
                _7kmGenderRank = value[indexSplitGenderRank]
                _7kmCatRank = value[indexSplitCategoryRank]
            else:
                if(isCorporate):
                    corporate_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\n")
                else:
                    elite_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\n")
                continue
           
            value = values[indexSplitStart+2].replace('/',' ').replace(',',' ').split()
            if(len(value) >= indexSplitCategoryRank):
                _10kmTime = value[indexSplitTime]
                _10kmSpeed = value[indexSplitSpeed]
                _10kmGenderRank = value[indexSplitGenderRank]
                _10kmCatRank = value[indexSplitCategoryRank]
            else:
                if(isCorporate):
                    corporate_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\n")
                else:
                    elite_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\n")
                continue
            
            value = values[indexSplitStart+4].replace('/',' ').replace(',',' ').split()
            if(len(value) >= indexSplitCategoryRank):
                _13kmTime = value[indexSplitTime]
                _13kmSpeed = value[indexSplitSpeed]
                _13kmGenderRank = value[indexSplitGenderRank]
                _13kmCatRank = value[indexSplitCategoryRank]
            else:
                if(isCorporate):
                    corporate_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _10kmTime + "\t" + _10kmSpeed + "\n")
                else:
                    elite_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _10kmTime + "\t" + _10kmSpeed + "\n")
                continue
            
            value = values[indexSplitStart+6].replace('/',' ').replace(',',' ').split()
            if(len(value) >= indexSplitCategoryRank):
                _14kmTime = value[indexSplitTime]
                _14kmSpeed = value[indexSplitSpeed]
                _14kmGenderRank = value[indexSplitGenderRank]
                _14kmCatRank = value[indexSplitCategoryRank]
            else:
                if(isCorporate):
                    corporate_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _13kmTime + "\t" + _13kmSpeed + "\n")
                else:
                    elite_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _13kmTime + "\t" + _13kmSpeed + "\n")
                continue
            
            value = values[indexSplitStart+8].replace('/',' ').replace(',',' ').split()
            if(len(value) >= indexSplitCategoryRank):
                _17kmTime = value[indexSplitTime]
                _17kmSpeed = value[indexSplitSpeed]
                _17kmGenderRank = value[indexSplitGenderRank]
                _17kmCatRank = value[indexSplitCategoryRank]
            else:
                if(isCorporate):
                    corporate_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _13kmTime + "\t" + _13kmSpeed + "\t" + _14kmTime + "\t" + _14kmSpeed + "\n")
                else:
                    elite_drop.write(bib+"\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _13kmTime + "\t" + _13kmSpeed + "\t" + _14kmTime + "\t" + _14kmSpeed + "\n")
                continue
            
            netTime = values[indexSplitStart+10].replace(',',' ').split()[0]
            netSpeed = values[indexSplitStart+10].replace(',',' ').split()[6]
            
            if(isCorporate):
                corporate_dump.write(bib + "\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + catRank + "\t" + totalCatFinishers + "\t" +genderRank + "\t" +totalGenderFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _7kmGenderRank  + "\t" + _7kmCatRank  + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _10kmGenderRank  + "\t" + _10kmCatRank + "\t" + _13kmTime + "\t" + _13kmSpeed + "\t" + _13kmGenderRank + "\t" + _13kmCatRank + "\t" + _14kmTime + "\t" + _14kmSpeed + "\t" + _14kmGenderRank  + "\t" + _14kmCatRank  + "\t" + _17kmTime + "\t" + _17kmSpeed + "\t" + _17kmGenderRank  + "\t" + _17kmCatRank + "\t" + netTime + "\t" + netSpeed + "\n")
            else:
                elite_dump.write(bib + "\t" + name + "\t" + gender + "\t" + cat + "\t" + rank + "\t" + totalFinishers + "\t" + catRank + "\t" + totalCatFinishers + "\t" +genderRank + "\t" +totalGenderFinishers + "\t" + _7kmTime + "\t" + _7kmSpeed + "\t" + _7kmGenderRank  + "\t" + _7kmCatRank  + "\t" + _10kmTime + "\t" + _10kmSpeed + "\t" + _10kmGenderRank  + "\t" + _10kmCatRank + "\t" + _13kmTime + "\t" + _13kmSpeed + "\t" + _13kmGenderRank + "\t" + _13kmCatRank + "\t" + _14kmTime + "\t" + _14kmSpeed + "\t" + _14kmGenderRank  + "\t" + _14kmCatRank  + "\t" + _17kmTime + "\t" + _17kmSpeed + "\t" + _17kmGenderRank  + "\t" + _17kmCatRank + "\t" + netTime + "\t" + netSpeed + "\n")

        #time.sleep(25)
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

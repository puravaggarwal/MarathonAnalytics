dict = {}
dict["65 YRS and MEN"]=[6654,21,6111]
dict["60 YRS TO  WOMEN"]=[6654,1,543]
dict["60 YRS TO  MEN"]=[6654,37,6111]
dict["55 YRS TO  WOMEN"]=[6654,3,543]
dict["55 YRS TO  MEN"]=[6654,81,6111]
dict["50 YRS TO  WOMEN"]=[6654,11,543]
dict["50 YRS TO  MEN"]=[6654,200,6111]
dict["45 YRS TO  WOMEN"]=[6654,44,543]
dict["45 YRS TO  MEN"]=[6654,465,6111]
dict["40 YRS TO  WOMEN"]=[6654,93,543]
dict["40 YRS TO  MEN"]=[6654,822,6111]
dict["35 YRS TO  WOMEN"]=[6654,122,543]
dict["35 YRS TO  MEN"]=[6654,962,6111]
dict["OPEN MEN"]=[6654,3523,6111]
dict["OPEN WOMEN"]=[6654,269,543]

file = open("normal_drop","r")
data = file.read()
datas = data.splitlines()
out = open("processed_normal_drops","w")

for i in range(0,len(datas)):
    #print(datas[i])
    value = datas[i].split("\t")
    if(value[4] == "0"):
        value[6] = "0"
        value[7] = dict[value[3]][1]
        value[8] = "0"
        value[9] = dict[value[3]][2]

        if(len(value) >= 12):
            value[12] = "0"
            value[13] = "0"
            if(len(value) >= 16):
                value[16] = "0"
                value[17] = "0"
                if(len(value) >= 20):
                    value[20] = "0"
                    value[21] = "0"

    for j in value:
        out.write(str(j)+"\t")
    out.write("\n")
out.close()

dict = {}
dict["ELITE WOMEN"]=[61,28,28]
dict["ELITE MEN"]=[61,33,33]

file = open("elite_dump","r")
data = file.read()
datas = data.splitlines()
out = open("processed_elite_dumps","w")

for i in range(0,len(datas)):
    #print(datas[i])
    value = datas[i].split("\t")
    if(value[4] == "0"):
        value[6] = "0"
        value[7] = dict[value[3]][1]
        value[8] = "0"
        value[9] = dict[value[3]][2]
        value[12] = "0"
        value[13] = "0"
        value[16] = "0"
        value[17] = "0"
        value[20] = "0"
        value[21] = "0"
        value[24] = "0"
        value[25] = "0"
        value[28] = "0"
        value[29] = "0"

    for j in value:
        out.write(str(j)+"\t")
    out.write("\n")
out.close()

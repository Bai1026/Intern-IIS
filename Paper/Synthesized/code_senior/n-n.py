# This is the code of openke

from tqdm import tqdm

lef = {}
rig = {}
rellef = {}
relrig = {}

with open("../data/3_openKE/train2id.txt", "r") as triple:
    tot = int(triple.readline())
    for i in tqdm(range(tot), desc="Processing train data"):
        content = triple.readline()
        h, t, r = content.strip().split()
        if not (h, r) in lef:
            lef[(h, r)] = []
        if not (r, t) in rig:
            rig[(r, t)] = []
        lef[(h, r)].append(t)
        rig[(r, t)].append(h)
        if not r in rellef:
            rellef[r] = {}
        if not r in relrig:
            relrig[r] = {}
        rellef[r][h] = 1
        relrig[r][t] = 1

# 处理验证数据
with open("../data/3_openKE/valid2id.txt", "r") as valid:
    tot = int(valid.readline())
    for i in tqdm(range(tot), desc="Processing validation data"):
        content = valid.readline()
        h, t, r = content.strip().split()
        if not (h, r) in lef:
            lef[(h, r)] = []
        if not (r, t) in rig:
            rig[(r, t)] = []
        lef[(h, r)].append(t)
        rig[(r, t)].append(h)
        if not r in rellef:
            rellef[r] = {}
        if not r in relrig:
            relrig[r] = {}
        rellef[r][h] = 1
        relrig[r][t] = 1

# 处理测试数据
with open("../data/3_openKE/test2id.txt", "r") as test:
    tot = int(test.readline())
    for i in tqdm(range(tot), desc="Processing test data"):
        content = test.readline()
        h, t, r = content.strip().split()
        if not (h, r) in lef:
            lef[(h, r)] = []
        if not (r, t) in rig:
            rig[(r, t)] = []
        lef[(h, r)].append(t)
        rig[(r, t)].append(h)
        if not r in rellef:
            rellef[r] = {}
        if not r in relrig:
            relrig[r] = {}
        rellef[r][h] = 1
        relrig[r][t] = 1

# 保存类型约束
with open("../data/3_openKE/type_constrain.txt", "w") as f:
    f.write("%d\n" % (len(rellef)))
    for i in rellef:
        f.write("%s\t%d" % (i, len(rellef[i])))
        for j in rellef[i]:
            f.write("\t%s" % (j))
        f.write("\n")
        f.write("%s\t%d" % (i, len(relrig[i])))
        for j in relrig[i]:
            f.write("\t%s" % (j))
        f.write("\n")

# 清空并准备计算关系
rellef = {}
totlef = {}
relrig = {}
totrig = {}
for i in lef:
    if not i[1] in rellef:
        rellef[i[1]] = 0
        totlef[i[1]] = 0
    rellef[i[1]] += len(lef[i])
    totlef[i[1]] += 1.0

for i in rig:
    if not i[0] in relrig:
        relrig[i[0]] = 0
        totrig[i[0]] = 0
    relrig[i[0]] += len(rig[i])
    totrig[i[0]] += 1.0

s11 = 0
s1n = 0
sn1 = 0
snn = 0

# 计算关系类型
with open("../data/3_openKE/test2id.txt", "r") as f:
    tot = int(f.readline())
    for i in tqdm(range(tot), desc="Calculating relation types"):
        content = f.readline()
        h, t, r = content.strip().split()
        rign = rellef[r] / totlef[r]
        lefn = relrig[r] / totrig[r]
        if (rign < 1.5 and lefn < 1.5):
            s11 += 1
        if (rign >= 1.5 and lefn < 1.5):
            s1n += 1
        if (rign < 1.5 and lefn >= 1.5):
            sn1 += 1
        if (rign >= 1.5 and lefn >= 1.5):
            snn += 1

# 分类测试数据
with open("../data/3_openKE/test2id.txt", "r") as f, \
     open("../data/3_openKE/1-1.txt", "w") as f11, \
     open("../data/3_openKE/1-n.txt", "w") as f1n, \
     open("../data/3_openKE/n-1.txt", "w") as fn1, \
     open("../data/3_openKE/n-n.txt", "w") as fnn, \
     open("../data/3_openKE/test2id_all.txt", "w") as fall:

    tot = int(f.readline())
    fall.write("%d\n" % tot)
    f11.write("%d\n" % s11)
    f1n.write("%d\n" % s1n)
    fn1.write("%d\n" % sn1)
    fnn.write("%d\n" % snn)

    for i in tqdm(range(tot), desc="Sorting test data"):
        content = f.readline()
        h, t, r = content.strip().split()
        rign = rellef[r] / totlef[r]
        lefn = relrig[r] / totrig[r]
        if (rign < 1.5 and lefn < 1.5):
            f11.write(content)
            fall.write("0\t" + content)
        if (rign >= 1.5 and lefn < 1.5):
            f1n.write(content)
            fall.write("1\t" + content)
        if (rign < 1.5 and lefn >= 1.5):
            fn1.write(content)
            fall.write("2\t" + content)
        if (rign >= 1.5 and lefn >= 1.5):
            fnn.write(content)
            fall.write("3\t" + content)


# from tqdm import tqdm

# lef = {}
# rig = {}
# rellef = {}
# relrig = {}

# triple = open("train2id.txt", "r")
# valid = open("valid2id.txt", "r")
# test = open("test2id.txt", "r")

# tot = (int)(triple.readline())
# for i in range(tot):
# 	content = triple.readline()
# 	h,t,r = content.strip().split()
# 	if not (h,r) in lef:
# 		lef[(h,r)] = []
# 	if not (r,t) in rig:
# 		rig[(r,t)] = []
# 	lef[(h,r)].append(t)
# 	rig[(r,t)].append(h)
# 	if not r in rellef:
# 		rellef[r] = {}
# 	if not r in relrig:
# 		relrig[r] = {}
# 	rellef[r][h] = 1
# 	relrig[r][t] = 1

# tot = (int)(valid.readline())
# for i in range(tot):
# 	content = valid.readline()
# 	h,t,r = content.strip().split()
# 	if not (h,r) in lef:
# 		lef[(h,r)] = []
# 	if not (r,t) in rig:
# 		rig[(r,t)] = []
# 	lef[(h,r)].append(t)
# 	rig[(r,t)].append(h)
# 	if not r in rellef:
# 		rellef[r] = {}
# 	if not r in relrig:
# 		relrig[r] = {}
# 	rellef[r][h] = 1
# 	relrig[r][t] = 1

# tot = (int)(test.readline())
# for i in range(tot):
# 	content = test.readline()
# 	h,t,r = content.strip().split()
# 	if not (h,r) in lef:
# 		lef[(h,r)] = []
# 	if not (r,t) in rig:
# 		rig[(r,t)] = []
# 	lef[(h,r)].append(t)
# 	rig[(r,t)].append(h)
# 	if not r in rellef:
# 		rellef[r] = {}
# 	if not r in relrig:
# 		relrig[r] = {}
# 	rellef[r][h] = 1
# 	relrig[r][t] = 1

# test.close()
# valid.close()
# triple.close()

# f = open("type_constrain.txt", "w")
# f.write("%d\n"%(len(rellef)))
# for i in rellef:
# 	f.write("%s\t%d"%(i,len(rellef[i])))
# 	for j in rellef[i]:
# 		f.write("\t%s"%(j))
# 	f.write("\n")
# 	f.write("%s\t%d"%(i,len(relrig[i])))
# 	for j in relrig[i]:
# 		f.write("\t%s"%(j))
# 	f.write("\n")
# f.close()

# rellef = {}
# totlef = {}
# relrig = {}
# totrig = {}
# # lef: (h, r)
# # rig: (r, t)
# for i in lef:
# 	if not i[1] in rellef:
# 		rellef[i[1]] = 0
# 		totlef[i[1]] = 0
# 	rellef[i[1]] += len(lef[i])
# 	totlef[i[1]] += 1.0

# for i in rig:
# 	if not i[0] in relrig:
# 		relrig[i[0]] = 0
# 		totrig[i[0]] = 0
# 	relrig[i[0]] += len(rig[i])
# 	totrig[i[0]] += 1.0

# s11=0
# s1n=0
# sn1=0
# snn=0
# f = open("test2id.txt", "r")
# tot = (int)(f.readline())
# for i in range(tot):
# 	content = f.readline()
# 	h,t,r = content.strip().split()
# 	rign = rellef[r] / totlef[r]
# 	lefn = relrig[r] / totrig[r]
# 	if (rign < 1.5 and lefn < 1.5):
# 		s11+=1
# 	if (rign >= 1.5 and lefn < 1.5):
# 		s1n+=1
# 	if (rign < 1.5 and lefn >= 1.5):
# 		sn1+=1
# 	if (rign >= 1.5 and lefn >= 1.5):
# 		snn+=1
# f.close()


# f = open("test2id.txt", "r")
# f11 = open("1-1.txt", "w")
# f1n = open("1-n.txt", "w")
# fn1 = open("n-1.txt", "w")
# fnn = open("n-n.txt", "w")
# fall = open("test2id_all.txt", "w")
# tot = (int)(f.readline())
# fall.write("%d\n"%(tot))
# f11.write("%d\n"%(s11))
# f1n.write("%d\n"%(s1n))
# fn1.write("%d\n"%(sn1))
# fnn.write("%d\n"%(snn))
# for i in range(tot):
# 	content = f.readline()
# 	h,t,r = content.strip().split()
# 	rign = rellef[r] / totlef[r]
# 	lefn = relrig[r] / totrig[r]
# 	if (rign < 1.5 and lefn < 1.5):
# 		f11.write(content)
# 		fall.write("0"+"\t"+content)
# 	if (rign >= 1.5 and lefn < 1.5):
# 		f1n.write(content)
# 		fall.write("1"+"\t"+content)
# 	if (rign < 1.5 and lefn >= 1.5):
# 		fn1.write(content)
# 		fall.write("2"+"\t"+content)
# 	if (rign >= 1.5 and lefn >= 1.5):
# 		fnn.write(content)
# 		fall.write("3"+"\t"+content)
# fall.close()
# f.close()
# f11.close()
# f1n.close()
# fn1.close()
# fnn.close()

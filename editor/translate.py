BPM = 128.000
SEC_BEAT = 60. / BPM
N_DANCER = 7
N_PART = 13

def bbf2sec(bbf):
    tokens = bbf.split('-')
    bar = int(tokens[0]) - 1
    beat = int(tokens[1]) - 1
    frac = 0
    if len(tokens) >= 3:
        a, b = tokens[2].split('/')
        frac = float(a) / float(b)
    sec = (bar * 4 + beat + frac) * SEC_BEAT
    return sec

def parse_single_part(s):
    res = []
    for i in range(N_DANCER):
        for j in range(N_PART):
            if chr(ord('1')+i) in s and (chr(ord('A')+j) in s or 'Z' in s):
                res.append((i, j))
    return res

def parse_parts(s):
    res = []
    parts = s.split('+')
    for p in parts:
        res += parse_single_part(p)
    return list(set(res))

def translate(fname):
    lst = [x.strip() for x in open(fname)]
    res = []
    for i in range(N_DANCER):
        v = []
        for j in range(N_PART):
            v.append([])
        res.append(v)

    for line in lst:
        if line.strip() == '' or line[0] == '#':
            continue
        tokens = line.split()
        start = bbf2sec(tokens[0])
        end = bbf2sec(tokens[1])
        parts = parse_parts(tokens[2])
        #print(start, end, parts)
        ltype = 1 # 1=ON, 2=Fade in, 3=Fade out
        if len(tokens) >= 4:
            if tokens[3] == 'FI':
                ltype = 2
            elif tokens[3] == 'FO':
                ltype = 3
        for i, j in parts:
            res[i][j].append((start, end, ltype))

    return res

def translate_pos(fname):
    lst = [x.strip() for x in open(fname)]
    res = []
    for i in range(N_DANCER):
        res.append([])

    tm = 0
    sm = False
    for line in lst:
        if line.strip() == '' or line[0] == '#':
            continue
        tokens = line.split()
        if len(tokens) <= 2:
            tm = bbf2sec(tokens[0])
            sm = (len(tokens) >= 2)
        else:
            num = int(tokens[0]) - 1
            bx = int(tokens[1])
            by = int(tokens[2])
            if not sm:
                res[num].append((tm, res[num][-1][1], res[num][-1][2]))
            res[num].append((tm, bx, by))

    return res

if __name__ == '__main__':
    import json
    import time

    while True:
        res = translate('test.in')
        s = json.dumps(res)
        f = open('light.js', 'w')
        f.write("var Data = \"")
        f.write(s)
        f.write("\";")
        f.close()
        
        res = translate_pos('test.pos')
        s = json.dumps(res)
        f = open('pos.js', 'w')
        f.write("var Pos = \"")
        f.write(s)
        f.write("\";")
        f.close()
        time.sleep(2)

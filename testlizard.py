from lizard import analyze, preprocessing

r = analyze(["c.cpp"], None, 1, [preprocessing])
for i in r:
    print "-----file--------"
    print i.filename
    print i.function_list

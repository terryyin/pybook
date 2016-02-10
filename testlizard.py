from lizard import analyze, preprocessing, CLikeReader, FileInfoBuilder

r = analyze(["c.cpp"], None, 1, [preprocessing])
for i in r:
    print "-----file--------"
    print i.filename
    print i.function_list

def analyze_source_code(filename):
    context = FileInfoBuilder(filename)
    reader = CLikeReader(context)
    with open(filename) as f:
        tokens = reader.generate_tokens(f.read())
    for _ in reader(tokens, reader):
        pass
    return context.fileinfo


i = analyze_source_code("c.cpp")
print i.filename
print i.function_list

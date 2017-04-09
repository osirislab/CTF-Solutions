import subprocess, string

wanted = "82a386a3b7983198313b363293399232349892369a98323692989a313493913036929a303abf"

known = "ASIS{"
#known = "ASIS{d2d2791c6a18da9ed19ade28cb09ae05}"

for pos in range(40):
    for char in '0123456789abcdef':
        attempt = known + char + 'AA'
        res = subprocess.check_output(["gdb", "-x", "gdb_s", "--args", "./wandere", attempt])
        res = res.split('\n')[-2].split('"')[1]
        print attempt, res
        if wanted.startswith(res[:-4]):
            known += char
            print "GOT NEW CHAR"
            print known
            break

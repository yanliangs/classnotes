import os, sys, glob

pdfs = " ".join(sorted(list(glob.glob('./*/*.pdf'))))

if len(sys.argv) == 1:
    os.system("pdftk %s output ../../Dropbox/Public/skfiles/multivar_calculus.pdf" % pdfs)
    exit()    
elif sys.argv[1] == 'all':
    for a in sorted(glob.glob("calc*")):
        os.chdir(a)
        os.system("pdflatex -shell-escape %s" % glob.glob("calc_*.tex")[0] )
        os.chdir("..")
elif sys.argv[1] == 'clean':
    os.system("find . -name '_region_*' | xargs rm  -rf")
    os.system("find . -name '_minted-*' | xargs rm  -rf")
    os.system("find . -name '*.log' | xargs rm  -rf")
    os.system("find . -name '*.aux' | xargs rm  -rf")
    os.system("find . -name '*.out' | xargs rm  -rf")

elif sys.argv[1] == 'tex':
    file = glob.glob('calc_multi_*.tex')
    os.system("pdflatex -shell-escape %s" % file[0])
    
    

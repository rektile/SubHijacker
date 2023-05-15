from SubHijacker import SubHijacker
import sys

if len(sys.argv < 2):
    print("[!] No domain given")

domain = sys.argv[1].strip()

SH = SubHijacker(domain)
SH.run()




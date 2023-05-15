import subprocess
import os
import dns.resolver

class SubHijacker:
    def __init__(self, _domain):
        self.foundSubsFileName = "foundSubs.txt"
        self.takeoverFileName = "vulnerable.txt"
        self.domain = _domain

    def findSubs(self):
        p = subprocess.Popen(["subfinder", "-d", self.domain, "-o", self.foundSubsFileName], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate()

    def getAllDomainsFromFile(self):
        if not os.path.exists(self.foundSubsFileName):
            return []

        with open(self.foundSubsFileName, "r") as f:
            return f.readlines()

    def getAllVulnerable(self):
        if not os.path.exists(self.takeoverFileName):
            return []

        with open(self.takeoverFileName, "r") as f:
            return f.readlines()

    def findTakeover(self):
        p = subprocess.Popen(["subjack", "-w", self.foundSubsFileName, "-t", "100", "-ssl", "-o", self.takeoverFileName], shell=False,
                             stderr=subprocess.DEVNULL)
        p.communicate()

    def showCnameForDomains(self, domains):

        for domain in domains:
            domain = domain.split()[1].replace("\n", "")
            answer = dns.resolver.resolve(domain, "Cname")
            try:
                for data in answer:
                    print(f"[-] {domain} --> {data}")
            except:
                continue

    def removeAllFiles(self):
        if os.path.exists(self.takeoverFileName):
            os.remove(self.takeoverFileName)

        if os.path.exists(self.foundSubsFileName):
            os.remove(self.foundSubsFileName)

    def run(self):
        print(f"[*] Finding subdomains of {self.domain}")
        self.findSubs()

        domains = self.getAllDomainsFromFile()

        print(f"[*] Found {len(domains)} subdomains")

        if not domains:
            self.removeAllFiles()
            return

        print(f"[*] Scanning for takeover")

        self.findTakeover()

        takeoverDomains = self.getAllVulnerable()

        if not takeoverDomains:
            print("[!] None found")
            self.removeAllFiles()
            return

        print(f"[*] Found {len(domains)} subdomains")

        self.showCnameForDomains(takeoverDomains)

        self.removeAllFiles()
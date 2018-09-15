#!/usr/bin/env python3
#-*-coding: utf-8 -*-

#########################################
#########################################
###  yazar  : burakbüyükyüksel        ###
###  e-mail : bbuyukyuksel@gmail.com  ###
###  tarih  : 15.09.2018              ###
#########################################
#########################################

import sys
uidnumber = 1000;

nereden = "OU=Kullanici,OU=Sehir,OU=Bolum,OU=Tasra,OU=NET,DC=NET,DC=GOV,DC=TR"
nereye = "ou=Ankara,ou=Tasra,ou=Kullanıcılar,dc=site,dc=gov,dc=tr"
samba_ou = "samba-ou";
ldap_ou = "ldap-ou";
domain = "domain";
guid = "guid";
homefolder = "homefolder";

loginShell = "loginShell: /bin/bash\n"
homeDirectory_fmt = "homeDirectory: /home/{}/{}"
uidnumber_fmt = "uidnumber: {}\n"

cur_state = 0
states = 8


def start_progress():
    global homefolder, guid, domain, uidnumber, samba_ou, ldap_ou
    print("\033[01;33m ")

    print("{} : {}".format("Nereden", nereden))
    print("{} : {}".format("Nereye", nereye))
    print("{} : {}".format("samba_ou", samba_ou))
    print("{} : {}".format("ldap_ou", ldap_ou))
    print("{} : {}".format("domain", domain))
    print("{} : {}".format("guid", guid))
    print("{} : {}".format("homefolder", homefolder))
    print("\033[00m")

    try:
        with open("kullanicilar_org.ldf", "r") as fout :
            print("#Progress is started")
            with open ("kullanicilar_new.ldf", "w") as fin:
                for line in fout:
                    if  nereden in line:
                        line = line.replace(nereden,nereye)
                    if "objectClass: user" in line:
                        line = line.replace("user", "posixAccount")
                    if "cn" in line:
                        line_sn_copy = line.replace("cn", "sn")
                        fin.write(line)
                        fin.write(line_sn_copy)
                        continue

                    if "sAMAccountName" in line:
                        line = line.replace("sAMAccountName", "uid")
                        uid_info = line.split(" ")
                        fin.write(line)

                        #HomeDirectory
                        homeDirectory = homeDirectory_fmt.format(domain, uid_info[1])
                        fin.write(homeDirectory)

                        #loginShell
                        fin.write(loginShell)

                        #uidnumber
                        _uidnumber = uidnumber_fmt.format(str(uidnumber))
                        uidnumber += 1
                        fin.write(_uidnumber)
                        continue
                    if "userPrincipalName" in line:
                        line = line.replace("userPrincipalName", "mail")

                    fin.write(line)



    except:
        print("Beklenmedik Hata:", sys.exc_info()[1])
        raise

def state_progress():
    global cur_state, states
    sure = input("\033[01;32mBilgilerinizin doğruluğundan emin misiniz? [E/h/go] : \033[00m")
    # H/h
    if (sure.lower() == "h"):
        print("\033[01;31m #Bilgilerinizi Tekrardan Giriniz \033[00m")
        return "same"
    # GO,go
    elif ("go" in sure.lower()):
    # Dallanıyor
        cmd, state_no = sure.split(":")
        state_no = int(state_no)
        if (state_no >= 0 and state_no <= states):
            cur_state = state_no
            return "other"
        else:
            print("\033[01;31m #Hatalı Adım Numarası [{}] \033[00m".format(str(state_no)))

    # E/e
    else:
        if cur_state < states:
            cur_state += 1
            return "next"
        else:
            exit()

if __name__ == "__main__":

    while(True):
        print("\033[01;35m #Adım[{}] \033[00m".format(str(cur_state)))
        if(cur_state == 0):
            print("\033[01;34m Hoş Geldiniz \033[00m\n")
            print("\033[00;34m")
            print("Adım[{}] -> {}".format("1", "Nereden"))
            print("Adım[{}] -> {}".format("2", "Nereye"))
            print("Adım[{}] -> {}".format("3", "SAMBA OU"))
            print("Adım[{}] -> {}".format("4", "LDAP OU"))
            print("Adım[{}] -> {}".format("5", "Domain"))
            print("Adım[{}] -> {}".format("6", "GUID"))
            print("Adım[{}] -> {}".format("7", "Home Folder"))
            print("Adım[{}] -> {}".format("8", "Progress"))
            print("\033[00m")
            cur_state += 1

        elif(cur_state == 1):
            print("Örnek -> ", nereden)
            temp = input("Nereden taşınacak : ")
            status = state_progress()
            if(status == "next"):
                nereden = temp

        elif(cur_state == 2):
            print("Örnek -> ", nereye)
            temp = input("Nereye taşınacak : ")
            status = state_progress()
            if(status == "next"):
                nereye = temp

        elif(cur_state == 3):
            print("Örnek -> ", samba_ou)
            temp = input("SAMBA OU : ")
            status = state_progress()
            if(status == "next"):
                samba_ou = temp

        elif(cur_state == 4):
            print("Örnek -> ", ldap_ou)
            temp = input("LDAP OU : ")
            status = state_progress()
            if(status == "next"):
                ldap_ou = temp

        elif (cur_state == 5):
            print("Örnek -> /home/<domain>",)
            temp = input("Domain : ")
            status = state_progress()
            if (status == "next"):
                domain = temp
        elif (cur_state == 6):
            print("Örnek -> ", guid)
            temp = input("GUID : ")
            status = state_progress()
            if (status == "next"):
                guid = temp

        elif (cur_state == 7):
            print("Örnek -> ", homefolder)
            temp = input("Home Folder : ")
            status = state_progress()
            if (status == "next"):
                homefolder = temp
        elif(cur_state == 8):
            print("\033[01;31m#Progress is started.. \033[00m")
            start_progress()
            print("\033[01;31m#Progress is finished.. \033[00m")
            break
print("\033[01;32m- END - \033[00m")